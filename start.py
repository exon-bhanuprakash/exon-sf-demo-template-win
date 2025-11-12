#!/usr/bin/env python3
"""
Exonpro Template - Start New Project
Cross-platform Python script for creating new Salesforce projects
"""

import os
import sys
import json
import shutil
import subprocess
import re
from datetime import datetime
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


def get_default_projects_dir():
    """Get default projects directory"""
    home = Path.home()
    if sys.platform == 'win32':
        return home / "Documents" / "00_All_Work" / "ExonProProjects"
    else:
        return home / "Documents" / "00_All_Work" / "ExonProProjects"


def validate_project_name(name):
    """Validate project name (lowercase, numbers, hyphens only)"""
    return bool(re.match(r'^[a-z0-9-]+$', name))


def run_command(cmd, cwd=None, check=True):
    """Run a shell command"""
    try:
        result = subprocess.run(
            cmd,
            cwd=cwd,
            shell=True,
            check=check,
            capture_output=True,
            text=True
        )
        return result.returncode == 0
    except subprocess.CalledProcessError:
        return False


def main():
    # Initialize colors
    Colors.init_colors()

    # Header
    print_blue("╔════════════════════════════════════════╗")
    print_blue("║   Exonpro - New Project Setup         ║")
    print_blue("╚════════════════════════════════════════╝")
    print()

    template_dir = get_template_dir()
    os.chdir(template_dir)

    # Step 1: Project Name
    print_blue("Step 1: Project Information")
    print()
    project_name = input("Enter project name (lowercase, hyphens only): ").strip()

    if not validate_project_name(project_name):
        print_red("ERROR: Invalid project name. Use lowercase letters, numbers, and hyphens only.")
        sys.exit(1)

    # Step 2: Target Directory
    print()
    default_dir = get_default_projects_dir()
    target_input = input(f"Enter parent directory path [{default_dir}]: ").strip()
    target_base_dir = Path(target_input) if target_input else default_dir
    project_dir = target_base_dir / project_name

    # Check if project already exists
    if project_dir.exists():
        print_red(f"ERROR: Project directory already exists: {project_dir}")
        print()
        response = input("Delete it and start fresh? [y/N]: ").strip().lower()
        if response == 'y':
            shutil.rmtree(project_dir)
            print_green("OK: Removed existing directory")
        else:
            sys.exit(1)

    # Step 3: Tech Stack
    print()
    print_blue("Step 2: Tech Stack Selection")
    print()
    print("Available stack:")
    print()
    print("1. salesforce-lwc-apex (Salesforce Platform)")
    print("   Frontend: Lightning Web Components (LWC)")
    print("   Backend: Apex")
    print("   Database: Salesforce Objects")
    print("   Best for: Salesforce demos and applications")
    print("   Deployment: Developer Org (free)")
    print()

    stack_name = "salesforce-lwc-apex"
    print_green(f"OK: Selected: {stack_name}")

    # Step 4: Salesforce Configuration
    print()
    print_blue("Step 3: Salesforce Configuration")
    print()
    print("Get your Salesforce org info by running: sf org list")
    print()

    org_username = input("Salesforce Org Username [your@email.com]: ").strip() or "your@email.com"
    org_alias = input("Salesforce Org Alias [DevOrg]: ").strip() or "DevOrg"
    contact_email = input("Your email for project contact [kusaldip.das@exonpro.com]: ").strip() or "kusaldip.das@exonpro.com"

    # Step 5: Create Project Structure
    print()
    print_blue("Step 4: Creating Project")
    print()

    print("Creating directory structure...")
    project_dir.mkdir(parents=True, exist_ok=True)
    (project_dir / ".exon" / "config").mkdir(parents=True, exist_ok=True)
    (project_dir / ".exon" / "phases").mkdir(parents=True, exist_ok=True)
    (project_dir / ".exon" / "logs").mkdir(parents=True, exist_ok=True)
    (project_dir / ".exon" / "standards").mkdir(parents=True, exist_ok=True)
    (project_dir / ".exon" / "stacks" / stack_name).mkdir(parents=True, exist_ok=True)

    # Copy standards and stacks from template
    print("Copying framework files...")
    standards_src = template_dir / ".exon" / "standards"
    standards_dst = project_dir / ".exon" / "standards"
    if standards_src.exists():
        for item in standards_src.iterdir():
            if item.is_file():
                shutil.copy2(item, standards_dst / item.name)

    stacks_src = template_dir / ".exon" / "stacks"
    stacks_dst = project_dir / ".exon" / "stacks"
    if stacks_src.exists():
        shutil.copytree(stacks_src, stacks_dst, dirs_exist_ok=True)

    # Create requirements.md template
    print("Creating requirements.md template...")
    requirements_content = f"""# Project Name: {project_name}

## Business Problem
[What problem does this solve? 2-3 sentences]

## Solution
[How does your app solve it? 2-3 sentences]

## Target Users
- [User type 1]: [Description]
- [User type 2]: [Description]

## Key Features

### Phase 1 (MVP - Deploy First)
1. User authentication (email/password)
2. [Feature 2]
3. [Feature 3]
4. [Feature 4]
5. [Feature 5]

### Phase 2 (Post-MVP)
1. [Future feature 1]
2. [Future feature 2]

## Scale Requirements
- Expected users: 100-1,000 users in first year
- Traffic pattern: Variable during business hours
- Deployment: Salesforce Developer Org (free for development)
- Growth potential: Medium

## Technical Requirements
- Authentication: Salesforce platform authentication
- Custom Objects: [List any custom objects needed]
- Apex triggers: [List any automation needs]
- File uploads: Salesforce Files/Attachments
- Real-time features: Platform Events (if needed)
- Third-party integrations: None
- External APIs: None

## Compliance & Security
- Data compliance: None
- Security: Use Salesforce platform defaults (demo mode)
- Testing: Optional for demo, 75%+ coverage for production

## Timeline
- MVP deadline: [Date]
- Full launch: [Date]
"""
    (project_dir / "requirements.md").write_text(requirements_content, encoding='utf-8')

    # Create salesforce-config.json
    print("Creating salesforce-config.json...")
    salesforce_config = {
        "project": {
            "name": project_name,
            "description": "Salesforce application built with Exonpro",
            "version": "1.0.0"
        },
        "salesforce": {
            "org_username": org_username,
            "instance_url": "https://login.salesforce.com",
            "org_type": "developer",
            "api_version": "61.0",
            "org_alias": org_alias
        },
        "deployment": {
            "auto_deploy": False,
            "test_level": "NoTestRun",
            "deploy_on_save": True
        },
        "project_settings": {
            "source_api_version": "61.0",
            "namespace": "",
            "sfdx_login_url": "https://login.salesforce.com"
        },
        "feature_flags": {
            "generate_tests": False,
            "use_security_enforced": True,
            "bulkify_code": True,
            "pwa_support": False
        },
        "notifications": {
            "email": contact_email,
            "slack_webhook": None
        },
        "metadata_scope": {
            "include": [
                "ApexClass",
                "ApexTrigger",
                "LightningComponentBundle",
                "CustomObject",
                "CustomField",
                "PermissionSet",
                "CustomTab",
                "FlexiPage",
                "CustomApplication"
            ],
            "exclude": ["Profile"]
        },
        "demo_mode": {
            "enabled": True,
            "skip_tests": True,
            "minimal_validation": True,
            "generate_sample_data": True
        }
    }
    (project_dir / "salesforce-config.json").write_text(
        json.dumps(salesforce_config, indent=2),
        encoding='utf-8'
    )

    # Create state.json
    state_json = {
        "current_phase": None,
        "completed_phases": [],
        "phase_status": {},
        "started_at": None,
        "last_updated": None
    }
    (project_dir / ".exon" / "phases" / "state.json").write_text(
        json.dumps(state_json, indent=2),
        encoding='utf-8'
    )

    # Create project.json
    timestamp = datetime.utcnow().strftime("%Y-%m-%dT%H:%M:%SZ")
    project_json = {
        "project_name": project_name,
        "stack_template": stack_name,
        "created_at": timestamp,
        "exonpro_version": "1.0.0"
    }
    (project_dir / ".exon" / "config" / "project.json").write_text(
        json.dumps(project_json, indent=2),
        encoding='utf-8'
    )

    # Create CLAUDE.md from template
    print("Creating CLAUDE.md project brain...")
    build_timestamp = datetime.utcnow().strftime("%Y-%m-%dT%H:%M:%SZ")
    template_path = template_dir / ".exon" / "standards" / "CLAUDE.md.template"

    if template_path.exists():
        claude_template = template_path.read_text(encoding='utf-8')
        claude_content = (claude_template
            .replace('{{PROJECT_NAME}}', project_name)
            .replace('{{LAST_UPDATED}}', build_timestamp)
            .replace('{{CURRENT_PHASE}}', 'Not Started')
            .replace('{{BUILD_STARTED}}', build_timestamp)
            .replace('{{NEXT_ACTION}}', 'Start Phase 0: Configuration validation')
            .replace('{{PHASE0_STATUS}}', 'PENDING')
            .replace('{{PHASE1_STATUS}}', 'PENDING')
            .replace('{{PHASE2_STATUS}}', 'PENDING')
            .replace('{{PHASE3_STATUS}}', 'PENDING')
            .replace('{{PHASE4_STATUS}}', 'PENDING')
            .replace('{{PHASE5_STATUS}}', 'PENDING')
            .replace('{{STACK_NAME}}', stack_name)
            .replace('{{ORG_USERNAME}}', org_username)
            .replace('{{ORG_ALIAS}}', org_alias)
            .replace('{{CONTACT_EMAIL}}', contact_email)
        )
        (project_dir / "CLAUDE.md").write_text(claude_content, encoding='utf-8')

    # Initialize git
    print("Initializing git repository...")
    os.chdir(project_dir)
    run_command("git init -q", check=False)
    run_command("git checkout -b dev -q", check=False)
    run_command("git add .", check=False)

    commit_message = f"""Initial commit - {project_name}

Stack: {stack_name}
Created: {timestamp}

🤖 Initialized with Exonpro Template"""

    run_command(f'git commit -q -m "{commit_message}"', check=False)

    print_green("OK: Project created successfully")
    print()
    print(f"Project location: {project_dir}")
    print()

    # Step 6: Edit Requirements
    print_blue("Step 5: Configure Requirements")
    print()
    print("Options:")
    print("  1. Edit requirements.md now (opens editor)")
    print("  2. Copy from existing requirements file")
    print("  3. Skip editing (edit manually later)")
    print()
    req_option = input("Choose option [1-3] (default: 1): ").strip() or "1"

    if req_option == "1":
        print()
        print("Opening requirements.md for editing...")
        print("Fill in your business requirements, then save and close.")
        print()
        input("Press Enter to open editor...")

        # Open editor based on platform
        req_file = project_dir / "requirements.md"
        if sys.platform == 'win32':
            os.startfile(req_file)
        elif sys.platform == 'darwin':  # macOS
            subprocess.run(['open', req_file])
        else:  # Linux
            editor = os.environ.get('EDITOR', 'nano')
            subprocess.run([editor, req_file])

        print_green("OK: Requirements saved")

    elif req_option == "2":
        print()
        existing_req_path = input("Enter path to existing requirements file: ").strip()
        if Path(existing_req_path).exists():
            shutil.copy2(existing_req_path, project_dir / "requirements.md")
            print_green(f"OK: Requirements copied from {existing_req_path}")
        else:
            print_red(f"ERROR: File not found: {existing_req_path}")
            print("Keeping template requirements.md - please edit it manually")
        print()
        input("Press Enter to continue...")

    else:
        print_yellow("WARNING: Skipping requirements edit")
        print()
        print("IMPORTANT: Edit requirements.md before starting the build!")
        print()
        input("Press Enter to continue...")

    # Step 7: Check Python venv
    print()
    print_blue("Step 6: Preparing Builder")
    print()

    os.chdir(template_dir)

    venv_dir = template_dir / "builder" / "venv"
    if not venv_dir.exists():
        print("Creating Python virtual environment...")
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
        print_green("OK: Python venv created")

    # Step 8: Confirm and Start Build
    print()
    print_blue("╔════════════════════════════════════════╗")
    print_blue("║   Ready to Build                       ║")
    print_blue("╚════════════════════════════════════════╝")
    print()
    print_green("Project Configuration:")
    print(f"  Name: {project_name}")
    print(f"  Location: {project_dir}")
    print(f"  Stack: {stack_name}")
    print(f"  Salesforce Org: {org_username}")
    print(f"  Org Alias: {org_alias}")
    print()
    print_yellow("Build Process:")
    print("  Phase 0: Configuration validation (5-10 min)")
    print("  Phase 1: Research & feature planning (30-60 min)")
    print("  Phase 2: Architecture design (45-90 min)")
    print("  Phase 3: Code generation (2-4 hours)")
    print("  Phase 4: Testing & validation (30-60 min)")
    print("  Phase 5: Deployment to Salesforce (45-90 min)")
    print()
    print_yellow("Total estimated time: 4-6 hours")
    print()
    start_build = input("Start automated build now? [Y/n]: ").strip().lower() or 'y'

    if start_build != 'y':
        print()
        print_yellow("Build cancelled.")
        print()
        print("To start the build later:")
        print(f"  cd {template_dir}")
        print(f"  python start.py")
        print()
        sys.exit(0)

    print()
    print_green("Starting automated build...")
    print()

    # Run the Python builder
    os.environ['PYTHONIOENCODING'] = 'utf-8'

    if sys.platform == 'win32':
        python_path = template_dir / "builder" / "venv" / "Scripts" / "python.exe"
    else:
        python_path = template_dir / "builder" / "venv" / "bin" / "python"

    build_script = template_dir / "builder" / "build.py"

    exit_code = subprocess.run([str(python_path), str(build_script), str(project_dir)]).returncode

    print()
    if exit_code == 0:
        print_green("╔════════════════════════════════════════╗")
        print_green("║   OK: Build Complete                   ║")
        print_green("╚════════════════════════════════════════╝")
        print()
        print("Your application has been built and deployed!")
        print()
        print(f"Project location: {project_dir}")
        print()
        print_blue("Next steps:")
        print("  1. Review generated code")
        print("  2. Test the dev deployment")
        print("  3. Deploy to staging/prod if ready")
    else:
        print_red("╔════════════════════════════════════════╗")
        print_red("║   ERROR: Build Failed                  ║")
        print_red("╚════════════════════════════════════════╝")
        print()
        print(f"Build failed. Check logs in: {project_dir}/.exon/logs/")
        print()
        print("To resume:")
        print(f"  cd {template_dir}")
        print(f"  python resume.py {project_dir}")

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
