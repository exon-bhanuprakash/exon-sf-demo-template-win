# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Repository Overview

**exon-template-sfdc-demo** - Project generation framework that creates Salesforce applications with automated builds.

Location: `/Users/kusaldipdas/Documents/00_All_Work/exon-template-sfdc-demo`

**CRITICAL: This is the TEMPLATE repository, NOT a generated project.**
- Work on THIS repository: Modify builder code, standards, stack templates → commit to `dev` branch
- Work on GENERATED projects: Located at `~/Documents/00_All_Work/ExonProProjects/{project-name}/` → use their own CLAUDE.md

Check your location: `pwd` (if you see `/exon-template-sfdc-demo`, you're in the template)

## System Architecture

### Three-Layer Design

**1. Project Generation Layer** (`start.sh`, `resume.sh`, `cleanup.sh`)
- `start.sh`: Interactive wizard → creates project structure → copies templates → optionally launches builder
- `resume.sh`: Resumes builds from `.exon/phases/state.json` checkpoint
- `cleanup.sh`: Safe project deletion with confirmation

**2. Automated Builder Layer** (Python + Claude Agent SDK)

Two builder implementations:

**Phase-Based Builder (`builder/build.py`)** - Full automated builds
- Executes 6 phases: Configuration → Research → Architecture → Implementation → Testing → Deployment
- Uses Claude Agent SDK with `permission_mode='bypassPermissions'` (no manual approvals)
- Each phase = separate Claude Code session with custom prompts (see `build_phase0_prompt()` through `build_phase5_prompt()`)
- State tracking: `.exon/phases/state.json` enables resume capability
- Dual logging: detailed conversation log + summary log in `.exon/logs/`

**TODO-Driven Builders** - Resume work on existing projects:
- `simple-todo-builder.py` (RECOMMENDED): Loops Claude sessions with "continue next task" prompt. Claude uses project's `todo-helper.sh` to manage TODO.md status. Simpler, more reliable.
- `todo-builder.py`: Builder parses TODO.md, builds custom prompts per task. Has issues with IN_PROGRESS state tracking.
- Both use `shared/todo_manager.py` for TODO.md parsing/validation

**3. Template Framework Layer** (`.exon/`)

**Standards** (`.exon/standards/`) - Copied to ALL generated projects:
- `CLAUDE.md.template`: Template for generated project's CLAUDE.md (variables replaced by `start.sh` via sed)
- Coding standards: `code-structure.md`, `naming-conventions.md`, `security-best-practices.md`, `testing-requirements.md`
- Deployment: `hosting-deployment.md`, `tech-stack-selection.md`

**Stacks** (`.exon/stacks/{stack-name}/`):
- `CLAUDE.md`: Stack-specific guidance for generated projects
- `constitution.md`: Architectural patterns and design principles
- `folder-structure.json`: Project structure blueprint
- Primary stack: Salesforce LWC + Apex (Lightning Web Components + Apex + Salesforce Objects)

## Common Commands

### Setup (First Time Only)
```bash
# Create Python virtual environment
cd builder && python3 -m venv venv
./venv/bin/pip install -r requirements.txt
cd ..
```

### Create New Project
```bash
./start.sh
# Interactive wizard: name → stack → Salesforce config → requirements → auto-build
```

### Resume Build
```bash
./resume.sh ~/Documents/00_All_Work/ExonProProjects/my-project
# Resumes from last completed phase in .exon/phases/state.json
```

### Continue Existing Project (TODO-driven)
```bash
# Simple builder (recommended)
./run-simple-builder.sh /path/to/project           # Interactive
./run-simple-builder.sh /path/to/project --batch 5  # Auto-run 5 tasks

# Complex builder (has state issues)
./run-todo-builder.sh /path/to/project --max-tasks 5
```

### Clean Up Test Project
```bash
./cleanup.sh ~/Documents/00_All_Work/ExonProProjects/test-project
# Requires typing 'DELETE' to confirm
```

### Test Template Changes
```bash
# 1. Modify standards or stack templates
vim .exon/standards/some-file.md

# 2. Generate test project
./start.sh  # Name: test-xyz, skip auto-build

# 3. Verify changes copied correctly
cd ~/Documents/00_All_Work/ExonProProjects/test-xyz
cat .exon/standards/some-file.md

# 4. Clean up
cd /Users/kusaldipdas/Documents/00_All_Work/exon-template-sfdc-demo
./cleanup.sh ~/Documents/00_All_Work/ExonProProjects/test-xyz
```

## Key Implementation Details

### How Phase-Based Builder Works (build.py:33-1099)

**Phase Execution Pipeline:**
1. Load requirements from `requirements.md`
2. Load Salesforce config from `salesforce-config.json`
3. Load framework context (standards + stack templates)
4. For each phase:
   - Build custom prompt via `build_phase{N}_prompt()` functions
   - Call `query(prompt, options)` from Claude Agent SDK
   - Stream Claude's responses (async iterator)
   - Log to both detailed and summary logs
   - Update `.exon/phases/state.json` on completion

**Phase 1 Improvements (Critical for MVP):**
- Module & feature breakdown with priorities (Critical/Medium/Low)
- Deep research ONLY on Critical features (MVP scope)
- Component architecture planning (atoms/molecules/organisms)
- Implementation plan separates MVP (Critical) from Post-MVP (Medium/Low)
- NO timelines, just priorities

**Claude Agent SDK Configuration:**
```python
options = ClaudeAgentOptions(
    permission_mode='bypassPermissions',  # No manual approvals
    cwd=str(project_root),
    setting_sources=["project"]  # Use Claude Pro subscription
)
```

### How TODO-Driven Builder Works (todo-builder.py:1-448)

**Task Selection Algorithm (shared/todo_manager.py:186-207):**
1. Parse TODO.md into Task objects
2. Check for IN_PROGRESS tasks → resume first if found
3. Filter TODO tasks (status 🔴)
4. Sort by priority (P0 > P1 > P2) then task ID
5. Return highest priority task

**Simple vs Complex Builder:**
- **simple-todo-builder.py**: Minimal wrapper. Just calls Claude with "continue next task" prompt. Claude reads TODO.md and calls `./scripts/todo-helper.sh start/complete` itself. More reliable.
- **todo-builder.py**: Parses TODO.md, extracts metadata, builds custom prompts. Known issue: status transitions sometimes incorrect. Use simple builder instead.

### Template Variable Replacement (start.sh:262-285)

`start.sh` uses `sed` to replace template variables in `CLAUDE.md.template`:
```bash
sed -e "s/{{PROJECT_NAME}}/$PROJECT_NAME/g" \
    -e "s/{{STACK_NAME}}/$STACK_NAME/g" \
    -e "s/{{ORG_USERNAME}}/$ORG_USERNAME/g" \
    -e "s/{{ORG_ALIAS}}/$ORG_ALIAS/g" \
    # ... 15+ variable replacements
```
This generates project-specific CLAUDE.md from template.

## Modifying the Template

### Change Standards (affects all future projects)
```bash
vim .exon/standards/security-best-practices.md
./start.sh  # Test: create project, verify file copied
git add .exon/standards/ && git commit -m "feat: Update security standards"
```

### Change Stack Template (affects projects using that stack)
```bash
vim .exon/stacks/salesforce-lwc-apex/constitution.md
./start.sh  # Test: select Salesforce stack, verify changes
git add .exon/stacks/ && git commit -m "feat: Update Salesforce patterns"
```

### Change Builder Logic
```bash
vim builder/build.py  # Edit phase prompts or execution logic
# Test changes (see "Test Template Changes" section above)
git add builder/ && git commit -m "fix: Improve Phase 1 research prompt"
```

### Change Generated Project's CLAUDE.md Template
```bash
vim .exon/standards/CLAUDE.md.template
# IMPORTANT: Uses sed variable replacement ({{PROJECT_NAME}}, {{STACK_NAME}}, etc.)
# See start.sh:262-285 for full list of variables
./start.sh  # Test: verify generated CLAUDE.md has correct values
git add .exon/standards/CLAUDE.md.template && git commit -m "feat: Improve project CLAUDE template"
```

## Git Workflow

Always work on `dev` branch:
```bash
git checkout dev
git add .
git commit -m "feat: description

🤖 Generated with Claude Code

Co-Authored-By: Claude <noreply@anthropic.com>"
git push origin dev
```

## Project Structure

```
exon-template-sfdc-demo/
├── start.sh, resume.sh, cleanup.sh      # Main entry points
├── run-simple-builder.sh                # TODO-driven builder (recommended)
├── run-todo-builder.sh                  # TODO-driven builder (has state issues)
│
├── builder/                             # Python automation
│   ├── build.py                         # Phase-based builder (6 phases)
│   ├── simple-todo-builder.py           # Simple TODO executor
│   ├── todo-builder.py                  # Complex TODO executor
│   ├── shared/todo_manager.py           # TODO.md parser
│   └── venv/                            # Python virtual environment
│
└── .exon/                               # Template framework
    ├── standards/                       # Copied to ALL projects
    │   ├── CLAUDE.md.template           # Uses {{VARIABLES}}
    │   └── *.md                         # Coding standards
    │
    └── stacks/                          # Stack-specific templates
        └── salesforce-lwc-apex/         # Salesforce stack
            ├── CLAUDE.md                # Stack guidance
            ├── constitution.md          # Patterns
            ├── folder-structure.json    # Structure
            └── .claude/settings.json    # Claude Code settings
```

**Generated Project Structure** (created by `start.sh`):
```
~/Documents/00_All_Work/ExonProProjects/{project-name}/
├── CLAUDE.md                            # Generated from template
├── TODO.md                              # Created by Phase 1
├── requirements.md                      # User-provided
├── salesforce-config.json               # Salesforce org settings
├── sfdx-project.json                    # SFDX project configuration
├── force-app/                           # Salesforce source
│   └── main/default/                    # Created by Phase 3
│       ├── lwc/                         # Lightning Web Components
│       ├── classes/                     # Apex classes
│       ├── triggers/                    # Apex triggers
│       └── objects/                     # Custom objects
├── .exon/
│   ├── standards/                       # Copied from template
│   ├── stacks/salesforce-lwc-apex/      # Copied from template
│   ├── phases/state.json                # Build state
│   └── logs/                            # Builder logs
└── scripts/                             # Setup and deployment scripts
```

## Important Notes

**Dependencies:**
- Python 3.x with `claude-agent-sdk` (`pip install claude-agent-sdk`)
- Claude Pro subscription (for `setting_sources=["project"]`)
- Salesforce CLI installed (`npm install -g @salesforce/cli`)
- Salesforce Developer Org (free at https://developer.salesforce.com/signup)

**MVP Philosophy:**
- Phase 1 creates module/feature breakdown with priorities (Critical/Medium/Low)
- Phase 3 implements ONLY Critical features (MVP scope)
- Medium/Low features documented but not implemented
- No timelines, just priorities

**Builder Autonomy:**
- Uses `permission_mode='bypassPermissions'` → no manual approvals
- Dual logging (detailed + summary) in `.exon/logs/`
- Resumable from any phase via `.exon/phases/state.json`
- Simple TODO builder more reliable than complex version
