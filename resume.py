#!/usr/bin/env python3
"""
Exonpro Template - Resume Build
Cross-platform Python script for resuming interrupted builds
"""

import os
import sys
import json
import subprocess
from pathlib import Path

# Fix Windows encoding for Unicode characters
if sys.platform == 'win32':
    import io
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')
    sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding='utf-8', errors='replace')


# ANSI color codes for terminal output
class Colors:
    BLUE = '\033[0;34m'
    GREEN = '\033[0;32m'
    YELLOW = '\033[1;33m'
    RED = '\033[0;31m'
    NC = '\033[0m'  # No Color

    @staticmethod
    def is_windows():
        return sys.platform == 'win32'

    @staticmethod
    def init_colors():
        """Initialize colors for Windows"""
        if Colors.is_windows():
            try:
                # Enable ANSI colors on Windows 10+
                import ctypes
                kernel32 = ctypes.windll.kernel32
                kernel32.SetConsoleMode(kernel32.GetStdHandle(-11), 7)
            except:
                # Fallback: disable colors on older Windows
                Colors.BLUE = Colors.GREEN = Colors.YELLOW = Colors.RED = Colors.NC = ''


def print_blue(text):
    print(f"{Colors.BLUE}{text}{Colors.NC}")

def print_green(text):
    print(f"{Colors.GREEN}{text}{Colors.NC}")

def print_yellow(text):
    print(f"{Colors.YELLOW}{text}{Colors.NC}")

def print_red(text):
    print(f"{Colors.RED}{text}{Colors.NC}")


def get_template_dir():
    """Get the template directory (where this script is located)"""
    return Path(__file__).parent.absolute()


def main():
    # Initialize colors
    Colors.init_colors()

    # Header
    print_blue("╔════════════════════════════════════════╗")
    print_blue("║   Exonpro - Resume Build               ║")
    print_blue("╚════════════════════════════════════════╝")
    print()

    template_dir = get_template_dir()
    os.chdir(template_dir)

    # Ask for project directory
    if len(sys.argv) > 1:
        project_dir = Path(sys.argv[1])
    else:
        project_path = input("Enter project directory path: ").strip()
        project_dir = Path(project_path)

    # Check if project directory exists
    if not project_dir.exists():
        print_red(f"ERROR: Project directory not found: {project_dir}")
        sys.exit(1)

    # Check if state file exists
    state_file = project_dir / ".exon" / "phases" / "state.json"
    if not state_file.exists():
        print_red("ERROR: No build state found")
        print()
        print(f"Cannot resume - no previous build found in {project_dir}")
        print("Use 'python start.py' to start a new build.")
        sys.exit(1)

    # Show current state
    print_blue("Build State:")
    print()

    try:
        with open(state_file, 'r', encoding='utf-8') as f:
            state_data = json.load(f)

        current_phase = state_data.get('current_phase', 'unknown')
        completed_phases = state_data.get('completed_phases', [])
        completed_str = ', '.join(completed_phases) if completed_phases else 'none'
        phase_status = state_data.get('phase_status', {})

        print(f"  Current phase: {current_phase}")
        print(f"  Completed: {completed_str}")

        # Show phase status if current phase has failed
        if current_phase in phase_status and phase_status[current_phase] == 'failed':
            print(f"  [!] Last phase failed - will retry from phase {current_phase}")

    except Exception as e:
        print_red(f"  Error reading state: {e}")
        sys.exit(1)

    print()

    # Show incomplete TODOs from CLAUDE.md
    claude_md = project_dir / "CLAUDE.md"
    if claude_md.exists():
        print_yellow("Incomplete TODOs (first 10):")
        print()

        try:
            with open(claude_md, 'r', encoding='utf-8') as f:
                lines = f.readlines()

            incomplete_todos = []
            complete_count = 0
            incomplete_count = 0

            for line_num, line in enumerate(lines, 1):
                if line.strip().startswith('- [ ]'):
                    incomplete_count += 1
                    if len(incomplete_todos) < 10:
                        incomplete_todos.append((line_num, line.strip()))
                elif line.strip().startswith('- [x]'):
                    complete_count += 1

            for line_num, todo in incomplete_todos:
                print(f"  {line_num}: {todo}")

            print()
            print(f"  Total: {complete_count} completed, {incomplete_count} remaining")
            print()

        except Exception as e:
            print(f"  Could not read TODOs: {e}")
            print()

    # Check for Python venv
    venv_dir = template_dir / "builder" / "venv"
    if not venv_dir.exists():
        print_yellow("WARNING: Creating Python virtual environment...")
        os.chdir(template_dir / "builder")

        # Create venv
        subprocess.run([sys.executable, "-m", "venv", "venv"], check=True)

        # Install requirements
        if sys.platform == 'win32':
            pip_path = venv_dir / "Scripts" / "pip.exe"
        else:
            pip_path = venv_dir / "bin" / "pip"

        subprocess.run([str(pip_path), "install", "-q", "-r", "requirements.txt"], check=True)
        os.chdir(template_dir)

    print_green("OK: Claude Agent SDK ready")
    print_green(f"OK: Project directory: {project_dir}")
    print()
    print_yellow("Resuming build from last checkpoint...")
    print()
    input("Press Enter to resume, or Ctrl+C to cancel...")
    print()

    # Run the Python builder with --resume flag
    os.environ['PYTHONIOENCODING'] = 'utf-8'

    if sys.platform == 'win32':
        python_path = template_dir / "builder" / "venv" / "Scripts" / "python.exe"
    else:
        python_path = template_dir / "builder" / "venv" / "bin" / "python"

    build_script = template_dir / "builder" / "build.py"

    exit_code = subprocess.run([
        str(python_path),
        str(build_script),
        str(project_dir),
        "--resume"
    ]).returncode

    print()
    if exit_code == 0:
        print_green("╔════════════════════════════════════════╗")
        print_green("║   OK: Build Complete                   ║")
        print_green("╚════════════════════════════════════════╝")
        print()
        print("Build resumed and completed successfully!")
    else:
        print_red("╔════════════════════════════════════════╗")
        print_red("║   ERROR: Build Failed                  ║")
        print_red("╚════════════════════════════════════════╝")
        print()
        print(f"Build failed. Check logs in: {project_dir}/.exon/logs/")

    print()


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print()
        print_yellow("Interrupted by user")
        sys.exit(1)
    except Exception as e:
        print()
        print_red(f"ERROR: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)
