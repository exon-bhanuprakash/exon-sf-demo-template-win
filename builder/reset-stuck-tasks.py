#!/usr/bin/env python3
"""
Reset Stuck IN_PROGRESS Tasks

Finds tasks marked as IN_PROGRESS but have no completion notes,
and resets them back to TODO status.
"""

import sys
import re
from pathlib import Path


def reset_stuck_tasks(todo_file: Path):
    """Reset IN_PROGRESS tasks with no completion notes back to TODO"""

    if not todo_file.exists():
        print(f"❌ TODO.md not found: {todo_file}")
        return False

    content = todo_file.read_text(encoding='utf-8')
    original_content = content

    # Find all task sections
    task_pattern = r'(### Task (\d+\.\d+): .+?)(?=\n### Task |\n## |$)'

    changes = []

    def process_task(match):
        task_content = match.group(0)
        task_id = match.group(2)

        # Check if IN_PROGRESS
        if '🟡 IN_PROGRESS' not in task_content:
            return task_content  # No change

        # Check if has meaningful completion notes
        notes_match = re.search(
            r'\*\*Completion Notes:\*\*\n(.+?)(?=\n---|\n###|$)',
            task_content,
            re.DOTALL
        )

        if notes_match:
            notes = notes_match.group(1).strip()
            # If notes are just the placeholder, consider it incomplete
            if notes and notes != '(To be added when task is completed)':
                return task_content  # Has notes, keep as-is

        # Reset to TODO
        updated = task_content.replace('🟡 IN_PROGRESS', '🔴 TODO')
        changes.append(task_id)
        return updated

    updated_content = re.sub(task_pattern, process_task, content, flags=re.DOTALL)

    if changes:
        print(f"\n✅ Resetting {len(changes)} stuck tasks to TODO:")
        for task_id in changes:
            print(f"   - Task {task_id}")

        # Write updated content
        todo_file.write_text(updated_content, encoding='utf-8')
        print(f"\n✅ TODO.md updated")
        return True
    else:
        print("✅ No stuck tasks found")
        return False


def main():
    if len(sys.argv) < 2:
        print("Usage: python reset-stuck-tasks.py /path/to/project")
        sys.exit(1)

    project_root = Path(sys.argv[1]).resolve()
    todo_file = project_root / 'TODO.md'

    print(f"🔍 Checking: {todo_file}\n")
    reset_stuck_tasks(todo_file)


if __name__ == '__main__':
    main()
