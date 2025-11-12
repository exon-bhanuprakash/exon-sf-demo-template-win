#!/usr/bin/env python3
"""
TODO-Driven Builder - Executes tasks from existing TODO.md

Simple automation that:
1. Reads TODO.md from a project
2. Gets next task via todo-helper.sh
3. Generates Claude prompt from task details
4. Spawns Claude Code session
5. Updates TODO.md when complete
"""

import sys
import asyncio
import argparse
import logging
from pathlib import Path
from datetime import datetime

# Import our TODO manager
from shared.todo_manager import TodoManager

try:
    from claude_agent_sdk import query, ClaudeAgentOptions
except ImportError:
    print("❌ Error: claude-agent-sdk not installed.")
    print("Install with: pip install claude-agent-sdk")
    sys.exit(1)


class TodoBuilder:
    """Execute tasks from TODO.md using Claude Code"""

    def __init__(self, project_root: Path, dry_run: bool = False):
        self.project_root = Path(project_root).resolve()
        self.dry_run = dry_run
        self.todo_manager = TodoManager(self.project_root)

        # Files we need
        self.claude_md = self.project_root / 'CLAUDE.md'
        self.requirements_dir = self.project_root / 'requirements'

        # Setup logging
        self.log_dir = self.project_root / '.exon' / 'logs'
        self.log_dir.mkdir(parents=True, exist_ok=True)

        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        self.log_file = self.log_dir / f'builder_{timestamp}.log'

        # Configure logging (both file and console)
        self.logger = logging.getLogger('TodoBuilder')
        self.logger.setLevel(logging.INFO)

        # File handler (detailed logs)
        file_handler = logging.FileHandler(self.log_file, encoding='utf-8')
        file_handler.setLevel(logging.DEBUG)
        file_formatter = logging.Formatter(
            '%(asctime)s [%(levelname)s] %(message)s',
            datefmt='%Y-%m-%d %H:%M:%S'
        )
        file_handler.setFormatter(file_formatter)

        # Console handler (summary)
        console_handler = logging.StreamHandler(sys.stdout)
        console_handler.setLevel(logging.INFO)
        console_formatter = logging.Formatter('%(message)s')
        console_handler.setFormatter(console_formatter)

        self.logger.addHandler(file_handler)
        self.logger.addHandler(console_handler)

        self.logger.info(f"Log file: {self.log_file}")

    def validate_project(self) -> bool:
        """Validate project has required files"""
        self.logger.info("🔍 Validating project structure...")

        if not self.project_root.exists():
            self.logger.error(f"❌ Project directory not found: {self.project_root}")
            return False

        if not self.todo_manager.exists():
            self.logger.error(f"❌ TODO.md not found in {self.project_root}")
            return False

        if not self.claude_md.exists():
            self.logger.error(f"❌ CLAUDE.md not found in {self.project_root}")
            return False

        # Validate TODO.md format
        valid, errors = self.todo_manager.validate()
        if not valid:
            self.logger.error(f"❌ TODO.md validation failed:")
            for error in errors:
                self.logger.error(f"   - {error}")
            return False

        self.logger.info("✅ Project structure valid")
        return True

    def load_context(self) -> dict:
        """Load project context (CLAUDE.md, requirements, etc.)"""
        self.logger.info("📚 Loading project context...")

        context = {
            'claude_md': '',
            'requirements': {}
        }

        # Load CLAUDE.md
        if self.claude_md.exists():
            context['claude_md'] = self.claude_md.read_text(encoding='utf-8')
            self.logger.debug(f"Loaded CLAUDE.md ({len(context['claude_md'])} chars)")

        # Load requirements files
        if self.requirements_dir.exists():
            for req_file in self.requirements_dir.glob('*.md'):
                phase_name = req_file.stem  # e.g., 'PHASE-0-REQUIREMENTS'
                context['requirements'][phase_name] = req_file.read_text(encoding='utf-8')
                self.logger.debug(f"Loaded {phase_name} ({len(context['requirements'][phase_name])} chars)")

        self.logger.info(f"✅ Loaded context: CLAUDE.md + {len(context['requirements'])} requirement docs")
        return context

    def build_task_prompt(self, task, context: dict) -> str:
        """Build Claude prompt for a specific task"""

        # Get phase requirements if available
        phase_requirements = ""
        phase_key = f"PHASE-{task.phase.split()[-1]}-REQUIREMENTS"
        if phase_key in context['requirements']:
            phase_requirements = f"""
## PHASE REQUIREMENTS
{context['requirements'][phase_key]}
"""

        # Format acceptance criteria
        criteria_list = "\n".join([f"- [ ] {c}" for c in task.acceptance_criteria])

        # Format dependencies
        deps_text = "None" if not task.dependencies else ", ".join(task.dependencies)

        # Build the prompt
        prompt = f"""
# PROJECT CONTEXT

You are working on the following project. Read CLAUDE.md below for complete context:

{context['claude_md']}

---

# CURRENT TASK

**Task ID:** {task.id}
**Task:** {task.title}
**Phase:** {task.phase}
**Priority:** {task.priority}
**Estimated Time:** {task.estimated_time}
**Dependencies:** {deps_text}

## Description
{task.description}

## Acceptance Criteria (YOUR CHECKLIST)
{criteria_list}

{phase_requirements}

## Commands Reference
{task.commands if task.commands else "No specific commands provided"}

---

# INSTRUCTIONS

**MANDATORY FIRST STEP:** Read CLAUDE.md in the project root to understand:
- Project architecture and structure
- Development commands
- Coding standards and conventions
- Testing requirements

**YOUR TASK:**
1. Work through each acceptance criterion systematically
2. Follow the exact specifications in CLAUDE.md
3. Create/modify files as needed
4. Test your changes
5. Ensure all acceptance criteria are met

**IMPORTANT:**
- This is Task {task.id} - do NOT proceed to other tasks
- Follow CLAUDE.md guidelines exactly
- Add detailed inline comments
- Ensure code quality and testing
- Do NOT skip any acceptance criteria

**When complete:**
- Summarize what you implemented
- List files created/modified
- Mention any issues or notes for future work

Your working directory is: {self.project_root}
"""
        return prompt

    async def execute_task(self, task, context: dict) -> bool:
        """Execute a single task using Claude Code"""

        self.logger.info(f"\n{'='*60}")
        self.logger.info(f"📋 Task {task.id}: {task.title}")
        self.logger.info(f"   Priority: {task.priority} | Estimated: {task.estimated_time}")
        self.logger.info(f"{'='*60}\n")

        if self.dry_run:
            self.logger.info("[DRY RUN] Would execute task with Claude Code")
            return True

        # Mark task as in progress
        self.logger.info(f"🟡 Marking task {task.id} as IN_PROGRESS...")
        self.todo_manager.mark_in_progress(task.id)

        # Build prompt
        self.logger.info("📝 Building task prompt...")
        prompt = self.build_task_prompt(task, context)
        self.logger.debug(f"Prompt length: {len(prompt)} chars")

        # Execute with Claude Code
        self.logger.info(f"🤖 Starting Claude Code session for Task {task.id}...")
        self.logger.info("   (Streaming Claude's work in real-time...)\n")

        try:
            # Create Claude options
            options = ClaudeAgentOptions(
                permission_mode='bypassPermissions',
                cwd=str(self.project_root),
                setting_sources=["project"]  # Use project's .claude/settings.json
            )

            # Execute query with real-time streaming
            response_text = ""
            message_count = 0

            async for message in query(prompt=prompt, options=options):
                message_count += 1

                # Extract text from message
                message_text = ""
                if isinstance(message, str):
                    message_text = message
                    response_text += message
                elif isinstance(message, dict):
                    text = message.get('text') or message.get('content') or ''
                    message_text = str(text)
                    response_text += message_text
                elif hasattr(message, 'text'):
                    message_text = str(message.text)
                    response_text += message_text
                elif hasattr(message, 'content'):
                    content = message.content
                    if isinstance(content, list):
                        for block in content:
                            if isinstance(block, dict):
                                text = block.get('text', '')
                                message_text += text
                                response_text += text
                            elif hasattr(block, 'text'):
                                text = str(block.text)
                                message_text += text
                                response_text += text
                    else:
                        message_text = str(content)
                        response_text += message_text

                # Stream output to console in real-time
                if message_text.strip():
                    # Log to console (INFO level shows on screen)
                    print(f"   💬 {message_text[:200]}{'...' if len(message_text) > 200 else ''}", flush=True)
                    # Full message to file
                    self.logger.debug(f"Message {message_count}: {message_text}")

            self.logger.info(f"\n✅ Claude Code session completed")
            self.logger.info(f"   Messages: {message_count} | Response length: {len(response_text)} chars\n")
            self.logger.debug(f"Full response:\n{response_text}")

            # Mark task complete
            self.logger.info(f"✅ Marking task {task.id} as DONE...")
            completion_notes = f"Completed by Claude Code automation.\n\nSummary:\n{response_text[:500]}..."
            self.todo_manager.mark_complete(task.id, completion_notes)

            return True

        except Exception as e:
            self.logger.error(f"\n❌ Task failed: {str(e)}")
            self.logger.error(f"   Task {task.id} remains IN_PROGRESS")
            import traceback
            self.logger.debug(traceback.format_exc())
            return False

    async def run(self, max_tasks: int = None) -> bool:
        """Run the builder - execute tasks from TODO.md"""

        self.logger.info("\n╔════════════════════════════════════════╗")
        self.logger.info("║   TODO-Driven Builder                  ║")
        self.logger.info("╚════════════════════════════════════════╝\n")

        # Validate project
        if not self.validate_project():
            return False

        # Load context
        context = self.load_context()

        # Show project status
        stats = self.todo_manager.get_statistics()
        self.logger.info(f"\n📊 Project Status:")
        self.logger.info(f"   Total Tasks: {stats['total']}")
        self.logger.info(f"   Completed: {stats['done']} ({stats['completion_percentage']:.1f}%)")
        self.logger.info(f"   In Progress: {stats['in_progress']}")
        self.logger.info(f"   TODO: {stats['todo']}\n")

        # Execute tasks (phase-wise continuation)
        tasks_completed = 0
        current_phase = None

        while True:
            # Get next task
            task = self.todo_manager.get_next_task()

            if not task:
                self.logger.info("✅ No more tasks to execute!")
                break

            # Check max tasks limit
            if max_tasks and tasks_completed >= max_tasks:
                self.logger.info(f"\n⏸️  Reached max tasks limit ({max_tasks})")
                self.logger.info(f"   Next task: {task.id} - {task.title}")
                break

            # Detect phase change (only ask for continuation when phase changes)
            if current_phase is not None and current_phase != task.phase:
                self.logger.info(f"\n{'='*60}")
                self.logger.info(f"✅ {current_phase} complete!")
                self.logger.info(f"📋 Next phase: {task.phase}")
                self.logger.info(f"{'='*60}\n")

                if max_tasks is None:  # Only ask if not in batch mode
                    user_input = input(f"Continue to {task.phase}? [Y/n]: ").strip().lower()
                    if user_input == 'n':
                        self.logger.info(f"⏸️  Paused by user after {current_phase}")
                        break

            # Update current phase
            if current_phase != task.phase:
                current_phase = task.phase
                self.logger.info(f"\n🎯 Starting {current_phase}")
                self.logger.info(f"{'='*60}\n")

            # Execute task
            success = await self.execute_task(task, context)

            if not success:
                self.logger.error(f"\n⚠️  Task {task.id} failed. Stopping.")
                return False

            tasks_completed += 1

        self.logger.info("\n╔════════════════════════════════════════╗")
        self.logger.info(f"║   Completed {tasks_completed} task(s)              ║")
        self.logger.info("╚════════════════════════════════════════╝\n")
        self.logger.info(f"📝 Full log saved to: {self.log_file}")

        return True


async def async_main(args):
    """Async main entry point"""

    project_root = Path(args.project_dir).resolve()

    if not project_root.exists():
        print(f"❌ Project directory not found: {project_root}")
        sys.exit(1)

    builder = TodoBuilder(
        project_root=project_root,
        dry_run=args.dry_run
    )

    try:
        success = await builder.run(max_tasks=args.max_tasks)
        sys.exit(0 if success else 1)
    except KeyboardInterrupt:
        print("\n\n⏸️  Build interrupted by user")
        sys.exit(1)
    except Exception as e:
        print(f"\n❌ Unexpected error: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)


def main():
    """Main entry point"""

    parser = argparse.ArgumentParser(
        description='TODO-Driven Builder - Execute tasks from TODO.md',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Run on exon-hr-hubv3.0
  python todo-builder.py /path/to/exon-hr-hubv3.0

  # Execute just 1 task
  python todo-builder.py /path/to/project --max-tasks 1

  # Dry run (no execution)
  python todo-builder.py /path/to/project --dry-run
        """
    )

    parser.add_argument(
        'project_dir',
        type=str,
        help='Path to project directory with TODO.md'
    )

    parser.add_argument(
        '--max-tasks',
        type=int,
        default=None,
        help='Maximum number of tasks to execute (default: ask after each)'
    )

    parser.add_argument(
        '--dry-run',
        action='store_true',
        help='Validate project but do not execute tasks'
    )

    args = parser.parse_args()

    # Run async main
    asyncio.run(async_main(args))


if __name__ == '__main__':
    main()
