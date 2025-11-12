#!/usr/bin/env python3
"""
TODO Manager - Handles TODO.md operations

This module provides functions to:
- Parse TODO.md structure
- Extract tasks and their metadata
- Update task status
- Add completion notes
- Calculate progress statistics
"""

import re
import json
import subprocess
from pathlib import Path
from typing import Dict, List, Optional, Tuple
from datetime import datetime


class Task:
    """Represents a single task from TODO.md"""

    def __init__(self, task_id: str, title: str, data: Dict):
        self.id = task_id
        self.title = title
        self.status = data.get('status', 'TODO')
        self.priority = data.get('priority', 'P1')
        self.estimated_time = data.get('estimated_time', '')
        self.assigned = data.get('assigned', '')
        self.dependencies = data.get('dependencies', [])
        self.blocks = data.get('blocks', [])
        self.description = data.get('description', '')
        self.acceptance_criteria = data.get('acceptance_criteria', [])
        self.commands = data.get('commands', '')
        self.completion_notes = data.get('completion_notes', '')
        self.phase = data.get('phase', '')

    def to_dict(self) -> Dict:
        """Convert task to dictionary"""
        return {
            'id': self.id,
            'title': self.title,
            'status': self.status,
            'priority': self.priority,
            'estimated_time': self.estimated_time,
            'assigned': self.assigned,
            'dependencies': self.dependencies,
            'blocks': self.blocks,
            'description': self.description,
            'acceptance_criteria': self.acceptance_criteria,
            'commands': self.commands,
            'completion_notes': self.completion_notes,
            'phase': self.phase
        }

    def is_todo(self) -> bool:
        return '🔴' in self.status or 'TODO' in self.status

    def is_in_progress(self) -> bool:
        return '🟡' in self.status or 'IN_PROGRESS' in self.status

    def is_done(self) -> bool:
        return '✅' in self.status or 'DONE' in self.status

    def is_blocked(self) -> bool:
        return '⏸️' in self.status or 'BLOCKED' in self.status


class TodoManager:
    """Manages TODO.md file operations"""

    def __init__(self, project_root: Path):
        self.project_root = Path(project_root)
        self.todo_file = self.project_root / 'TODO.md'
        self.todo_helper = self.project_root / 'scripts' / 'todo-helper.sh'

    def exists(self) -> bool:
        """Check if TODO.md exists"""
        return self.todo_file.exists()

    def read(self) -> str:
        """Read TODO.md content"""
        if not self.exists():
            raise FileNotFoundError(f"TODO.md not found at {self.todo_file}")
        return self.todo_file.read_text(encoding='utf-8')

    def write(self, content: str):
        """Write TODO.md content"""
        self.todo_file.write_text(content, encoding='utf-8')

    def parse_tasks(self) -> List[Task]:
        """Parse all tasks from TODO.md"""
        content = self.read()
        tasks = []

        # Find all task sections (### Task X.Y: Title)
        task_pattern = r'### Task (\d+\.\d+): (.+?)(?=\n### Task |\n## |$)'
        matches = re.finditer(task_pattern, content, re.DOTALL)

        for match in matches:
            task_id = match.group(1)
            title = match.group(2).strip()
            task_content = match.group(0)

            # Extract task metadata
            task_data = self._parse_task_content(task_content)
            task_data['phase'] = self._get_task_phase(task_id)

            tasks.append(Task(task_id, title, task_data))

        return tasks

    def _parse_task_content(self, content: str) -> Dict:
        """Parse task content to extract metadata"""
        data = {}

        # Extract status
        status_match = re.search(r'\*\*Status:\*\* (.+)', content)
        if status_match:
            data['status'] = status_match.group(1).strip()

        # Extract priority
        priority_match = re.search(r'\*\*Priority:\*\* (P\d)', content)
        if priority_match:
            data['priority'] = priority_match.group(1)

        # Extract estimated time
        time_match = re.search(r'\*\*Estimated Time:\*\* (.+)', content)
        if time_match:
            data['estimated_time'] = time_match.group(1).strip()

        # Extract assigned
        assigned_match = re.search(r'\*\*Assigned:\*\* (.+)', content)
        if assigned_match:
            data['assigned'] = assigned_match.group(1).strip()

        # Extract dependencies
        deps_match = re.search(r'\*\*Dependencies:\*\* (.+)', content)
        if deps_match:
            deps = deps_match.group(1).strip()
            if deps.lower() != 'none':
                data['dependencies'] = [d.strip() for d in deps.split(',')]
            else:
                data['dependencies'] = []

        # Extract blocks
        blocks_match = re.search(r'\*\*Blocks:\*\* (.+)', content)
        if blocks_match:
            blocks = blocks_match.group(1).strip()
            if blocks.lower() != 'none':
                data['blocks'] = [b.strip() for b in blocks.split(',')]
            else:
                data['blocks'] = []

        # Extract description
        desc_match = re.search(r'\*\*Description:\*\*\n(.+?)(?=\n\*\*|\n###|$)', content, re.DOTALL)
        if desc_match:
            data['description'] = desc_match.group(1).strip()

        # Extract acceptance criteria
        criteria_match = re.search(r'\*\*Acceptance Criteria:\*\*\n(.+?)(?=\n\*\*|\n###|$)', content, re.DOTALL)
        if criteria_match:
            criteria_text = criteria_match.group(1).strip()
            data['acceptance_criteria'] = re.findall(r'- \[[ x]\] (.+)', criteria_text)

        # Extract commands
        commands_match = re.search(r'\*\*Commands:\*\*\n```(?:bash)?\n(.+?)\n```', content, re.DOTALL)
        if commands_match:
            data['commands'] = commands_match.group(1).strip()

        # Extract completion notes
        notes_match = re.search(r'\*\*Completion Notes:\*\*\n(.+?)(?=\n---|\n###|$)', content, re.DOTALL)
        if notes_match:
            notes = notes_match.group(1).strip()
            if notes and notes != '(To be added when task is completed)':
                data['completion_notes'] = notes

        return data

    def _get_task_phase(self, task_id: str) -> str:
        """Get phase name from task ID (e.g., '1.2' -> 'PHASE 1')"""
        phase_num = task_id.split('.')[0]
        return f"PHASE {phase_num}"

    def get_next_task(self) -> Optional[Task]:
        """Get the next task to work on (highest priority TODO or first IN_PROGRESS)"""
        tasks = self.parse_tasks()

        # First check if there's already an IN_PROGRESS task (resume it)
        in_progress_tasks = [t for t in tasks if t.is_in_progress()]
        if in_progress_tasks:
            # Return the first IN_PROGRESS task (by task ID)
            in_progress_tasks.sort(key=lambda t: t.id)
            return in_progress_tasks[0]

        # If no IN_PROGRESS, filter TODO tasks
        todo_tasks = [t for t in tasks if t.is_todo()]

        if not todo_tasks:
            return None

        # Sort by priority (P0 > P1 > P2) then by task ID
        priority_order = {'P0': 0, 'P1': 1, 'P2': 2}
        todo_tasks.sort(key=lambda t: (priority_order.get(t.priority, 999), t.id))

        return todo_tasks[0]

    def get_task(self, task_id: str) -> Optional[Task]:
        """Get a specific task by ID"""
        tasks = self.parse_tasks()
        for task in tasks:
            if task.id == task_id:
                return task
        return None

    def mark_in_progress(self, task_id: str) -> bool:
        """Mark a task as IN_PROGRESS"""
        return self._run_helper('start', task_id)

    def mark_complete(self, task_id: str, completion_notes: str = '') -> bool:
        """Mark a task as DONE and add completion notes"""
        # Mark complete
        success = self._run_helper('complete', task_id)

        if success and completion_notes:
            self.add_completion_notes(task_id, completion_notes)

        return success

    def add_completion_notes(self, task_id: str, notes: str):
        """Add completion notes to a task"""
        content = self.read()

        # Find the task's completion notes section
        pattern = rf'(### Task {re.escape(task_id)}:.*?\*\*Completion Notes:\*\*\n)(.*?)(?=\n---|\n###|$)'

        def replace_notes(match):
            header = match.group(1)
            timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            new_notes = f"{notes}\n\n*Completed: {timestamp}*"
            return f"{header}{new_notes}\n"

        updated_content = re.sub(pattern, replace_notes, content, flags=re.DOTALL)
        self.write(updated_content)

    def get_phase_tasks(self, phase: str) -> List[Task]:
        """Get all tasks for a specific phase"""
        tasks = self.parse_tasks()
        return [t for t in tasks if t.phase == phase]

    def is_phase_complete(self, phase: str) -> bool:
        """Check if all tasks in a phase are complete"""
        phase_tasks = self.get_phase_tasks(phase)
        if not phase_tasks:
            return False
        return all(t.is_done() for t in phase_tasks)

    def get_statistics(self) -> Dict:
        """Get completion statistics"""
        tasks = self.parse_tasks()

        total = len(tasks)
        done = len([t for t in tasks if t.is_done()])
        in_progress = len([t for t in tasks if t.is_in_progress()])
        todo = len([t for t in tasks if t.is_todo()])
        blocked = len([t for t in tasks if t.is_blocked()])

        completion_pct = (done / total * 100) if total > 0 else 0

        # By priority
        by_priority = {}
        for priority in ['P0', 'P1', 'P2']:
            p_tasks = [t for t in tasks if t.priority == priority]
            p_done = len([t for t in p_tasks if t.is_done()])
            p_total = len(p_tasks)
            p_pct = (p_done / p_total * 100) if p_total > 0 else 0
            by_priority[priority] = {
                'total': p_total,
                'done': p_done,
                'percentage': p_pct
            }

        return {
            'total': total,
            'done': done,
            'in_progress': in_progress,
            'todo': todo,
            'blocked': blocked,
            'completion_percentage': completion_pct,
            'by_priority': by_priority
        }

    def _run_helper(self, command: str, *args) -> bool:
        """Run todo-helper.sh command"""
        if not self.todo_helper.exists():
            print(f"Warning: todo-helper.sh not found at {self.todo_helper}")
            return False

        try:
            cmd = [str(self.todo_helper), command] + list(args)
            result = subprocess.run(cmd, cwd=self.project_root, capture_output=True, text=True)
            return result.returncode == 0
        except Exception as e:
            print(f"Error running todo-helper.sh: {e}")
            return False

    def validate(self) -> Tuple[bool, List[str]]:
        """Validate TODO.md format"""
        errors = []

        if not self.exists():
            errors.append("TODO.md file not found")
            return False, errors

        content = self.read()

        # Check required sections
        required_sections = [
            'Progress Overview',
            'TODO MAINTENANCE RULES'
        ]

        for section in required_sections:
            if section not in content:
                errors.append(f"Missing required section: {section}")

        # Check tasks have required fields
        tasks = self.parse_tasks()
        for task in tasks:
            if not task.status:
                errors.append(f"Task {task.id} missing status")
            if not task.priority:
                errors.append(f"Task {task.id} missing priority")
            if not task.estimated_time:
                errors.append(f"Task {task.id} missing estimated time")

        return len(errors) == 0, errors


def get_next_task_json(project_root: Path) -> Optional[str]:
    """Get next task as JSON (for automation)"""
    manager = TodoManager(project_root)
    task = manager.get_next_task()

    if task:
        return json.dumps(task.to_dict(), indent=2)
    return None
