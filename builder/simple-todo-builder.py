#!/usr/bin/env python3
"""
Simple TODO-Driven Builder - Minimal automation

Just spawns Claude sessions with "continue next task" command.
Claude handles everything:
- Reading TODO.md
- Calling todo-helper.sh to start/complete tasks
- Updating status
- Working on implementation

This script just loops and calls Claude repeatedly.
"""

import sys
import asyncio
import argparse
from pathlib import Path
from datetime import datetime

try:
    from claude_agent_sdk import query, ClaudeAgentOptions
except ImportError:
    print("❌ Error: claude-agent-sdk not installed.")
    print("Install with: pip install claude-agent-sdk")
    sys.exit(1)


class SimpleTodoBuilder:
    """Minimal builder - just loops Claude sessions"""

    def __init__(self, project_root: Path, max_iterations: int = None):
        self.project_root = Path(project_root).resolve()
        self.max_iterations = max_iterations
        self.iteration_count = 0

    def validate_project(self) -> bool:
        """Basic validation"""
        if not self.project_root.exists():
            print(f"❌ Project not found: {self.project_root}")
            return False

        todo_file = self.project_root / 'TODO.md'
        if not todo_file.exists():
            print(f"❌ TODO.md not found in {self.project_root}")
            return False

        claude_md = self.project_root / 'CLAUDE.md'
        if not claude_md.exists():
            print(f"❌ CLAUDE.md not found in {self.project_root}")
            return False

        return True

    def build_prompt(self) -> str:
        """Simple prompt - just ask Claude to continue"""
        return """# Continue Next Task

**YOUR MISSION:**
Complete the next incomplete task from TODO.md, then STOP.

**WORKFLOW:**

1. **Find the next task to work on:**
   - Read TODO.md directly
   - Find the first task with status "🔴 TODO" OR "🟡 IN_PROGRESS"
   - Skip any tasks marked "✅ DONE"
   - This is your task for this session

2. **If task is TODO (🔴), start it:**
   ```bash
   ./scripts/todo-helper.sh start <task-id>
   ```

3. **If task is already IN_PROGRESS (🟡), just continue working on it**
   (No need to call start again)

4. **Read task requirements:**
   - Read CLAUDE.md for architecture, commands, and standards
   - Read the task's description and acceptance criteria in TODO.md
   - Understand what needs to be implemented

5. **Implement the task:**
   - Create/modify files as needed
   - Follow CLAUDE.md coding standards exactly
   - Complete ALL acceptance criteria
   - Test your changes (run tests if applicable)

6. **When ALL acceptance criteria are met:**
   ```bash
   ./scripts/todo-helper.sh complete <task-id>
   ```
   Add detailed completion notes explaining what was done.

7. **End with:** "TASK COMPLETE - Task X.Y finished"

8. **STOP** - Do NOT continue to next task.

**AVAILABLE COMMANDS:**
```bash
./scripts/todo-helper.sh list       # List all tasks
./scripts/todo-helper.sh start X.Y  # Mark task X.Y as IN_PROGRESS
./scripts/todo-helper.sh complete X.Y  # Mark task X.Y as DONE
```

**CRITICAL RULES:**
- ✅ Work on ONE task only
- ✅ Tasks can be TODO (🔴) or IN_PROGRESS (🟡) - both are fine to work on
- ✅ Skip DONE (✅) tasks
- ✅ Complete ALL acceptance criteria before marking done
- ✅ Use todo-helper.sh for status changes
- ❌ DO NOT analyze/fix TODO.md status issues - just work on the next incomplete task
- ❌ DO NOT work on multiple tasks in one session
- ❌ DO NOT skip acceptance criteria

Working directory: project root
"""

    async def run_iteration(self) -> tuple[bool, str]:
        """
        Run one Claude session

        Returns:
            (continue, message) - whether to continue and what happened
        """
        self.iteration_count += 1

        print(f"\n{'='*60}")
        print(f"📋 Iteration {self.iteration_count}")
        print(f"{'='*60}\n")

        prompt = self.build_prompt()

        try:
            # Create Claude options
            options = ClaudeAgentOptions(
                permission_mode='bypassPermissions',
                cwd=str(self.project_root),
                setting_sources=["project"]
            )

            # Execute query
            response_text = ""
            message_count = 0

            print("🤖 Starting Claude Code session...")
            print("   (Claude will read TODO.md and work on next task...)\n")

            async for message in query(prompt=prompt, options=options):
                message_count += 1

                # Extract text
                text = ""
                if isinstance(message, str):
                    text = message
                elif isinstance(message, dict):
                    text = message.get('text', '') or message.get('content', '')
                elif hasattr(message, 'text'):
                    text = str(message.text)
                elif hasattr(message, 'content'):
                    content = message.content
                    if isinstance(content, list):
                        for block in content:
                            if isinstance(block, dict):
                                text += block.get('text', '')
                            elif hasattr(block, 'text'):
                                text += str(block.text)
                    else:
                        text = str(content)

                response_text += text

                # Stream to console (first 200 chars)
                if text.strip():
                    preview = text[:200] + ('...' if len(text) > 200 else '')
                    print(f"   💬 {preview}", flush=True)

            print(f"\n✅ Session complete ({message_count} messages, {len(response_text)} chars)")

            # Don't try to parse Claude's response - just assume it worked
            # If there are no more tasks, the next iteration will detect it
            return True, "Task completed, ready for next iteration"

        except Exception as e:
            print(f"\n❌ Error: {e}")
            import traceback
            traceback.print_exc()
            return False, f"Exception: {str(e)}"

    async def run(self) -> bool:
        """Main loop - keep calling Claude until done"""

        print("\n╔════════════════════════════════════════╗")
        print("║   Simple TODO-Driven Builder           ║")
        print("╚════════════════════════════════════════╝\n")
        print(f"📁 Project: {self.project_root}")
        print(f"🔄 Max iterations: {self.max_iterations or 'unlimited'}\n")

        # Validate
        if not self.validate_project():
            return False

        print("✅ Project valid\n")

        # Loop
        while True:
            # Check iteration limit
            if self.max_iterations and self.iteration_count >= self.max_iterations:
                print(f"\n⏸️  Reached max iterations ({self.max_iterations})")
                break

            # Run one iteration
            continue_loop, message = await self.run_iteration()

            print(f"\n📊 Status: {message}\n")

            if not continue_loop:
                print(f"🏁 Stopping: {message}")
                break

            # Ask user if they want to continue (unless in batch mode)
            if not self.max_iterations:
                user_input = input("Continue to next task? [Y/n]: ").strip().lower()
                if user_input == 'n':
                    print("⏸️  Paused by user")
                    break

        print("\n╔════════════════════════════════════════╗")
        print(f"║   Completed {self.iteration_count} iteration(s)        ║")
        print("╚════════════════════════════════════════╝\n")

        return True


async def async_main(args):
    """Async entry point"""
    project_root = Path(args.project_dir).resolve()

    if not project_root.exists():
        print(f"❌ Project not found: {project_root}")
        sys.exit(1)

    builder = SimpleTodoBuilder(
        project_root=project_root,
        max_iterations=args.max_iterations
    )

    try:
        success = await builder.run()
        sys.exit(0 if success else 1)
    except KeyboardInterrupt:
        print("\n\n⏸️  Interrupted by user")
        sys.exit(1)
    except Exception as e:
        print(f"\n❌ Unexpected error: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)


def main():
    """CLI entry point"""
    parser = argparse.ArgumentParser(
        description='Simple TODO-Driven Builder - Loops Claude sessions',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Interactive mode (asks after each task)
  python simple-todo-builder.py /path/to/project

  # Batch mode (run 5 iterations)
  python simple-todo-builder.py /path/to/project --max-iterations 5

  # Run until all done
  python simple-todo-builder.py /path/to/project --max-iterations 999
        """
    )

    parser.add_argument(
        'project_dir',
        type=str,
        help='Path to project directory with TODO.md'
    )

    parser.add_argument(
        '--max-iterations',
        type=int,
        default=None,
        help='Maximum iterations (default: interactive mode)'
    )

    args = parser.parse_args()
    asyncio.run(async_main(args))


if __name__ == '__main__':
    main()
