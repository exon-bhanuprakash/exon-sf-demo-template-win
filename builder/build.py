#!/usr/bin/env python3
"""
Exonpro Automated Builder - Python Implementation

Spawns Claude Code sessions to build complete Salesforce applications from requirements.
Uses the claude-agent-sdk with project settings (Claude Pro subscription).
"""

import sys
import json
import asyncio
import argparse
from pathlib import Path
from datetime import datetime
import logging

try:
    from claude_agent_sdk import query, ClaudeAgentOptions
except ImportError:
    print("Error: claude-agent-sdk not installed.")
    print("Please install it with: pip install claude-agent-sdk")
    sys.exit(1)

# Configure logging with UTF-8 encoding for Windows
import io

# Create a UTF-8 stream handler for Windows compatibility
if sys.platform == 'win32':
    # Wrap stdout with UTF-8 encoding
    utf8_stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')
    stream_handler = logging.StreamHandler(utf8_stdout)
else:
    stream_handler = logging.StreamHandler(sys.stdout)

logging.basicConfig(
    level=logging.INFO,
    format='%(message)s',
    handlers=[stream_handler]
)
logger = logging.getLogger(__name__)


class ExonproBuilder:
    """Automated application builder using Claude Agent SDK."""

    PHASES = [
        ('0_configuration', 'Configuration & Setup', '5-10 min'),
        ('1_research', 'Deep Research & Stack Selection', '30-60 min'),
        ('2_architecture', 'Architecture Design', '45-90 min'),
        ('3_implementation', 'Code Generation', '2-4 hours'),
        ('4_testing', 'Testing & Validation', '30-60 min'),
        ('5_deployment', 'Deployment Setup', '45-90 min'),
    ]

    def __init__(self, project_root: Path, requirements_path: Path, verbose: bool = False, dry_run: bool = False, resume: bool = False):
        """
        Initialize the builder.

        Args:
            project_root: Root directory of the project
            requirements_path: Path to requirements.md file
            verbose: Enable verbose logging
            dry_run: If True, only print what would be executed
            resume: If True, resume from last checkpoint
        """
        self.project_root = project_root
        self.requirements_path = requirements_path
        self.verbose = verbose
        self.dry_run = dry_run
        self.resume = resume
        self.state_file = project_root / '.exon/phases/state.json'
        self.log_dir = project_root / '.exon/logs'
        self.log_dir.mkdir(parents=True, exist_ok=True)

        # Initialize dual log files
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        self.detailed_log = self.log_dir / f'build_detailed_{timestamp}.log'
        self.summary_log = self.log_dir / f'build_summary_{timestamp}.log'

        # Progress tracking
        self.progress_messages = []

    def log_detailed(self, message: str):
        """Write message to detailed log (full conversation history)."""
        try:
            with open(self.detailed_log, 'a', encoding='utf-8') as f:
                f.write(f"{message}\n")
        except Exception as e:
            logger.warning(f"Failed to write to detailed log: {e}")

    def log_summary(self, message: str, display: bool = True):
        """Write message to summary log and optionally display in terminal."""
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        log_line = f"[{timestamp}] {message}"

        # Write to summary log
        try:
            with open(self.summary_log, 'a', encoding='utf-8') as f:
                f.write(f"{log_line}\n")
        except Exception as e:
            logger.warning(f"Failed to write to summary log: {e}")

        # Display in terminal
        if display:
            print(f"  {message}")

        # Store for progress tracking
        self.progress_messages.append(message)

    def display_progress(self, phase_name: str, action: str):
        """Display real-time progress in terminal."""
        progress_msg = f"[{phase_name}] {action}"
        logger.info(progress_msg)
        self.log_summary(progress_msg, display=True)

    def _get_claude_cli_path(self) -> str:
        """
        Get the path to Claude CLI executable.

        On Windows, returns path to .bat wrapper that handles .cmd execution.
        On Unix, returns the claude binary path.

        Returns:
            String path to executable
        """
        import shutil
        import os

        if os.name == 'nt':  # Windows
            # Use .bat wrapper which calls Python wrapper to execute claude.cmd
            # .bat files ARE executable by Windows subprocess without shell=True
            wrapper_bat = Path(__file__).parent / "claude-wrapper.bat"
            if wrapper_bat.exists():
                return str(wrapper_bat.absolute())

            # Fallback: try to find claude directly
            claude_path = shutil.which('claude')
            if claude_path:
                return claude_path

        # On Unix-like systems, find claude binary
        claude_path = shutil.which('claude')
        if claude_path:
            return claude_path

        # Last resort fallback
        return 'claude'

    def load_state(self) -> dict:
        """Load build state from state.json."""
        if self.state_file.exists():
            try:
                with open(self.state_file, 'r') as f:
                    return json.load(f)
            except Exception as e:
                logger.warning(f"Could not load state: {e}")

        return {
            'current_phase': '0_configuration',
            'completed_phases': [],
            'phase_status': {},
            'started_at': datetime.now().isoformat(),
            'last_updated': datetime.now().isoformat()
        }

    def save_state(self, state: dict):
        """Save build state to state.json."""
        state['last_updated'] = datetime.now().isoformat()
        self.state_file.parent.mkdir(parents=True, exist_ok=True)

        try:
            with open(self.state_file, 'w') as f:
                json.dump(state, f, indent=2)
        except Exception as e:
            logger.error(f"Failed to save state: {e}")

    def load_requirements(self) -> str:
        """Load requirements from file."""
        if not self.requirements_path.exists():
            raise FileNotFoundError(f"Requirements file not found: {self.requirements_path}")

        with open(self.requirements_path, 'r', encoding='utf-8') as f:
            return f.read()

    def load_salesforce_config(self) -> dict:
        """Load Salesforce configuration."""
        config_path = self.project_root / 'salesforce-config.json'
        if not config_path.exists():
            raise FileNotFoundError(
                "Salesforce configuration file not found. "
                "Please copy salesforce-config.template.json to salesforce-config.json and fill it out."
            )

        with open(config_path, 'r') as f:
            config = json.load(f)

        # Validate required fields
        required = ['project.name', 'salesforce.org_username', 'salesforce.instance_url']
        for field in required:
            parts = field.split('.')
            value = config
            for part in parts:
                value = value.get(part)
                if value is None:
                    raise ValueError(f"Required field missing in salesforce-config.json: {field}")

        return config

    def load_context(self) -> dict:
        """Load exonpro framework context (standards, stacks, etc.)."""
        context = {
            'standards': {},
            'stacks': [],
            'selected_stack': None
        }

        # Load standards
        standards_dir = self.project_root / '.exon/standards'
        if standards_dir.exists():
            for standard_file in standards_dir.glob('*.md'):
                with open(standard_file, 'r', encoding='utf-8') as f:
                    context['standards'][standard_file.stem] = f.read()

        # Load available stacks
        stacks_dir = self.project_root / '.exon/stacks'
        if stacks_dir.exists():
            for stack_dir in stacks_dir.iterdir():
                if stack_dir.is_dir():
                    context['stacks'].append({
                        'name': stack_dir.name,
                        'path': str(stack_dir)
                    })

        # Load selected stack template (if exists)
        project_config = self.project_root / '.exon/config/project.json'
        if project_config.exists():
            with open(project_config, 'r') as f:
                proj_data = json.load(f)
                context['selected_stack'] = proj_data.get('stack_template')

        return context

    def build_system_prompt(self, context: dict) -> str:
        """Build system prompt with exonpro standards."""
        standards_text = "\n\n".join([
            f"## {name}\n{content}"
            for name, content in context['standards'].items()
        ])

        return f"""You are an expert full-stack developer building production-ready applications following Exonpro standards.

EXONPRO STANDARDS:
{standards_text}

Your task is to build a complete, production-ready application following these standards exactly.
Generate clean, well-documented, tested code.
Follow the folder structure from the template precisely.
"""

    def build_phase_prompt(self, phase: str, requirements: str, salesforce_config: dict, context: dict) -> str:
        """Build prompt for specific phase."""

        if phase == '0_configuration':
            return self.build_phase0_prompt(salesforce_config)
        elif phase == '1_research':
            return self.build_phase1_prompt(requirements, salesforce_config, context)
        elif phase == '2_architecture':
            return self.build_phase2_prompt()
        elif phase == '3_implementation':
            return self.build_phase3_prompt()
        elif phase == '4_testing':
            return self.build_phase4_prompt()
        elif phase == '5_deployment':
            return self.build_phase5_prompt()

        return ""

    def build_phase0_prompt(self, salesforce_config: dict) -> str:
        """Phase 0: Configuration validation."""
        return f"""
PHASE 0: Configuration & Setup

⚠️ CRITICAL: First, read CLAUDE.md in the project root to see your TODO list for this phase.

Validate the Salesforce configuration and set up the project.

Salesforce Config loaded:
- Org Username: {salesforce_config['salesforce']['org_username']}
- Instance URL: {salesforce_config['salesforce']['instance_url']}
- Org Type: {salesforce_config['salesforce']['org_type']}
- API Version: {salesforce_config['salesforce']['api_version']}
- Demo Mode: {'Enabled' if salesforce_config.get('demo_mode', {}).get('enabled', True) else 'Disabled'}

Tasks (also listed in CLAUDE.md):
1. Verify Salesforce CLI is installed (run: sf --version)
2. Check if logged into org (run: sf org list)
3. Create .exon/config/salesforce-config.json with validated config
4. Create .exon/config/org-info.json with org details
5. Create .exon/logs/preflight-check.log with validation results

IMPORTANT - Update CLAUDE.md as you work:
1. Use Edit tool to mark each TODO as [x] when completed
2. Update "Last Updated" timestamp in CLAUDE.md
3. Update "Next Action" to guide future sessions
4. Add notes under "Phase 0 Notes" section about decisions made

Example CLAUDE.md update:
- Old: - [ ] Verify Salesforce CLI
- New: - [x] Verify Salesforce CLI (version: 2.x.x)

Work through each TODO systematically. Keep CLAUDE.md updated so future sessions know progress.
"""

    def build_phase1_prompt(self, requirements: str, salesforce_config: dict, context: dict) -> str:
        """Phase 1: Module breakdown, deep research, and implementation planning."""
        selected_stack = context.get('selected_stack', 'salesforce-lwc-apex')

        return f"""
PHASE 1: Module Breakdown, Deep Research & Implementation Planning

⚠️ CRITICAL: First, read CLAUDE.md in the project root to see your TODO list for this phase.

STACK ALREADY SELECTED: {selected_stack}
You do NOT need to compare stacks. Focus on researching HOW to build with this stack.

USER PROVIDED OVERVIEW:
{requirements}

SALESFORCE CONFIGURATION:
- Org Type: {salesforce_config.get('salesforce', {}).get('org_type', 'developer')}
- API Version: {salesforce_config.get('salesforce', {}).get('api_version', '61.0')}
- Demo Mode: {salesforce_config.get('demo_mode', {}).get('enabled', True)}
- Skip Tests: {salesforce_config.get('demo_mode', {}).get('skip_tests', True)}

PHASE 1 WORKFLOW:

STEP 1: MODULE & FEATURE BREAKDOWN
From the high-level overview, intelligently break down the application into:
- **Modules**: Logical groupings (e.g., Lead Management, Bug Tracking, User Management)
- **Features per Module**: Specific capabilities within each module
- **Priority Assignment**: Critical (MVP), Medium (post-MVP phase 1), Low (post-MVP phase 2)

For example, if requirements mention "lead management, bug tracking, customer feedback":
- Module: Lead Management
  * Feature: Create/view leads (Critical)
  * Feature: Lead status workflow (Critical)
  * Feature: Lead assignment (Medium)
  * Feature: Lead scoring (Low)
  * Feature: Email integration (Low)

STEP 2: DEEP RESEARCH FOCUS AREAS:

1. BUSINESS DOMAIN ANALYSIS:
   - Analyze target users and their workflows
   - Research competitors and best practices
   - Document user journeys for critical features only

2. MODULE & FEATURE BREAKDOWN:
   From the overview, create comprehensive breakdown:
   - Identify all logical modules (8-15 modules typical)
   - List features per module (5-20 features per module)
   - Assign priorities: Critical (MVP), Medium (Phase 2), Low (Phase 3)
   - Critical = Must-have for MVP to be functional
   - Medium = Important but not blocking
   - Low = Nice-to-have, future enhancement

3. FRONTEND ARCHITECTURE RESEARCH:
   - Lightning Web Components (LWC) best practices
   - Reusable component architecture (atoms, molecules, organisms)
   - Lightning Data Service vs Apex imperative calls
   - Mobile-first responsive design with SLDS
   - State management (@wire, @track, @api)
   - UI/UX best practices with Lightning Design System

4. CRITICAL FEATURE DEEP RESEARCH:
   For EACH Critical priority feature only:
   - Research best implementation approaches
   - Break down into detailed implementation TODOs (5-15 per feature)
   - Identify required LWC components and Apex classes
   - Document data flow and security model
   - Estimate complexity and time

5. BACKEND ARCHITECTURE:
   - Custom Objects and Fields design
   - ⚠️ DEMO MODE: Always create custom objects (do NOT use standard objects like Account, Contact, Opportunity)
   - Design domain-specific objects (e.g., Customer__c, Order__c, Product__c)
   - Include relationships, validation rules, and formula fields to showcase platform features
   - Apex class organization (Service, Selector, Domain, Trigger Handler)
   - SOQL queries and governor limits
   - Salesforce security model (sharing rules, FLS, OLS)
   - Minimal but sufficient error handling

6. IMPLEMENTATION PLAN:
   Create priority-based implementation plan:
   - MVP: Only Critical features from each module
   - Post-MVP: Medium priority features (NOT implemented now)
   - Future: Low priority features (NOT implemented now)

   NO TIMELINES - Just priorities. Implementation order is flexible.

7. DEMO MODE CONSIDERATIONS:
   - Skip comprehensive unit tests (optional for demo)
   - Use platform security defaults
   - Focus on happy path implementations

OUTPUT DELIVERABLES - Use Write tool to create these files:

1. research/module_breakdown.md
   - Complete list of all modules
   - Features per module with priorities (Critical/Medium/Low)
   - Rationale for priority assignments

2. research/domain_analysis.md
   - Business domain analysis
   - Target user workflows (critical flows only)
   - Competitor analysis

3. research/frontend_architecture.md
   - LWC component architecture
   - Lightning Design System (SLDS) usage
   - Mobile-first design patterns
   - State management approach (@wire, @track)

4. research/mvp_features.md
   - Deep research on CRITICAL features only
   - For each Critical feature:
     * Best practices research
     * Component breakdown (LWC + Apex)
     * Implementation TODOs (5-15 actionable items)
     * Data flow diagram
     * Complexity estimate

5. research/backend_architecture.md
   - Custom Objects and Fields schema
   - Apex class structure (Service, Selector, Domain)
   - SOQL queries and access patterns
   - Salesforce security model

6. research/implementation_plan.md
   - MVP (Critical Priority): Features to implement NOW
   - Post-MVP (Medium Priority): Features documented but NOT implemented
   - Future (Low Priority): Features documented but NOT implemented
   - Complexity estimates (NOT timelines)

7. research/deployment_plan.md
   - Developer Org deployment strategy
   - Demo data generation approach

CRITICAL STRUCTURE for research/mvp_features.md:

```markdown
# MVP Features - Deep Research

## Module: [Module Name]

### Feature: [Feature Name] (Priority: Critical)

#### Why Critical
- [Explain why this is must-have for MVP]

#### Best Practices Research
- [Research findings]

#### Component Breakdown
Frontend:
- componentName/ (LWC folder with .js, .html, .css, .js-meta.xml)
- anotherComponent/ (LWC folder)

Backend:
- Apex class: ClassName (Service/Controller/Selector)
- Custom Objects: ObjectName__c
- SOQL queries needed

#### Implementation TODOs
- [ ] Specific TODO 1
- [ ] Specific TODO 2
...
- [ ] Specific TODO 10

#### Data Flow
[User action] → [Frontend] → [API] → [Lambda] → [DynamoDB] → Response flow

#### Complexity Estimate
Medium, 6-8 hours

---
[Repeat for each Critical feature]
```

CRITICAL STRUCTURE for research/implementation_plan.md:

```markdown
# Implementation Plan

## MVP: Critical Priority Features (Implement NOW)

### Module: Lead Management
- ✅ F01.1: Create/view leads (Complexity: Medium, 6-8 hours)
- ✅ F01.2: Lead status workflow (Complexity: Simple, 3-4 hours)

### Module: Bug Tracking
- ✅ F02.1: Create/view bugs (Complexity: Medium, 6-8 hours)
- ✅ F02.2: Bug status workflow (Complexity: Simple, 3-4 hours)

### Module: User Management
- ✅ F03.1: User registration (Complexity: Medium, 5-7 hours)
- ✅ F03.2: User login (Complexity: Simple, 3-4 hours)

**Total MVP Features**: 25 Critical features across 12 modules

---

## Post-MVP: Medium Priority (Document, DON'T Implement)

### Module: Lead Management
- ⏸️ F01.3: Lead assignment (Complexity: Medium, 4-5 hours)
- ⏸️ F01.4: Lead filtering/search (Complexity: Medium, 5-6 hours)

### Module: Bug Tracking
- ⏸️ F02.3: Bug assignment (Complexity: Medium, 4-5 hours)
- ⏸️ F02.4: Bug attachments (Complexity: Medium, 6-8 hours)

**Total Post-MVP Features**: 35 Medium features

---

## Future: Low Priority (Document, DON'T Implement)

### Module: Lead Management
- 🔮 F01.5: Lead scoring (Complexity: Complex, 10-12 hours)
- 🔮 F01.6: Email integration (Complexity: Complex, 12-15 hours)

### Module: Bug Tracking
- 🔮 F02.5: Auto-tagging (Complexity: Complex, 8-10 hours)
- 🔮 F02.6: Analytics dashboard (Complexity: Complex, 15-20 hours)

**Total Future Features**: 27 Low features

---

NO TIMELINES. NO "Week 2" OR "Day 6-7". Just priorities.
Implementation order is flexible based on dependencies.
```

IMPORTANT - Update CLAUDE.md as you work:
1. Mark each TODO as [x] when completed using Edit tool
2. Update "Last Updated" timestamp
3. Update "Next Action" field
4. Add notes under "Phase 1 Notes" about:
   - Key LWC architecture decisions
   - Custom Object design approach
   - Feature complexity analysis
   - Any risks or concerns identified

Work through each TODO in CLAUDE.md systematically. Focus on PRACTICAL research that will guide implementation.
"""

    def build_phase2_prompt(self) -> str:
        """Phase 2: Architecture design."""
        return """
PHASE 2: Architecture Design

⚠️ CRITICAL: First, read CLAUDE.md in the project root to see your TODO list for this phase.

Design the complete system architecture based on the research from Phase 1.

Review these files (already available):
- research/domain_analysis.md
- research/module_breakdown.md
- research/frontend_architecture.md
- research/backend_architecture.md
- requirements.md
- salesforce-config.json

Tasks (detailed in CLAUDE.md):
1. Design system architecture (LWC components, Apex classes, data flow, security model)
2. Define Custom Objects and Fields schema
   ⚠️ DEMO MODE: Create ALL custom objects (do NOT use Account, Contact, Opportunity, etc.)
   - Design domain-specific objects (e.g., Customer__c, Order__c, Product__c)
   - Include master-detail and lookup relationships
   - Add validation rules and formula fields
   - Define all required fields with proper data types
3. Plan Apex class structure (Controllers, Services, Selectors, Domains, Trigger Handlers)
4. Design SOQL queries and access patterns
5. Plan Lightning Pages and navigation

OUTPUT DELIVERABLES - Use Write tool to create these files:
- architecture/system-architecture.md (complete system design with component diagrams)
- architecture/data-model.md (Custom Objects, Fields, Relationships, Validation Rules)
- architecture/apex-structure.md (Apex class organization and responsibilities)
- architecture/lwc-components.md (LWC component hierarchy and communication)
- specs/objects-schema.json (JSON representation of Custom Objects)
- specs/apex-interfaces.json (Apex method signatures and contracts)

IMPORTANT - Update CLAUDE.md as you work:
1. Mark each TODO as [x] when completed using Edit tool
2. Update "Last Updated" timestamp
3. Update "Next Action" field
4. Add notes under "Phase 2 Notes" about:
   - Key architectural patterns chosen
   - Data model design decisions
   - Apex class organization strategy
   - LWC component architecture
   - Security model decisions (sharing, FLS, OLS)

Follow the Salesforce stack template patterns precisely.
Design for demo mode (skip complex security for now).
Work through CLAUDE.md TODOs systematically.
"""

    def build_phase3_prompt(self) -> str:
        """Phase 3: MVP code generation (Critical features only)."""
        return """
PHASE 3: MVP Code Generation (Critical Features Only)

⚠️ CRITICAL: First, read CLAUDE.md in the project root to see your TODO list for this phase.

IMPORTANT: Only implement CRITICAL priority features from research/implementation_plan.md
- Medium and Low priority features should NOT be implemented
- Focus on creating a working MVP, not a complete product

Generate MVP application code following the architecture from Phase 2.

Review all context files:
- research/module_breakdown.md (all modules and features with priorities)
- research/implementation_plan.md (MVP = Critical features only)
- research/mvp_features.md (deep research on Critical features)
- research/frontend_architecture.md (LWC component architecture)
- research/backend_architecture.md (Custom Objects, Apex classes)
- All architecture/ documents (system architecture, data model, Apex structure)
- requirements.md (original business overview)
- salesforce-config.json (Salesforce configuration)

Your task is to generate a WORKING MVP with CRITICAL FEATURES ONLY.

CODE GENERATION TASKS (detailed in CLAUDE.md):

1. SFDX Project Structure:
   - sfdx-project.json (SFDX project configuration)
   - .gitignore (Salesforce-specific)
   - README.md (setup and usage guide)

2. Custom Objects and Fields:
   ⚠️ DEMO MODE: Create ALL custom objects (do NOT use standard objects)
   - force-app/main/default/objects/[ObjectName]__c/[ObjectName]__c.object-meta.xml
   - force-app/main/default/objects/[ObjectName]__c/fields/[FieldName]__c.field-meta.xml
   - Create all Custom Objects needed for Critical features
   - Example: Instead of Account, create Customer__c or Client__c
   - Include relationships, validation rules, formula fields

3. Apex Classes:
   - force-app/main/default/classes/*Controller.cls (LWC controllers with @AuraEnabled methods)
   - force-app/main/default/classes/*Service.cls (business logic services)
   - force-app/main/default/classes/*Selector.cls (SOQL query classes)
   - force-app/main/default/classes/*Domain.cls (record manipulation logic)
   - force-app/main/default/classes/*TriggerHandler.cls (trigger logic)
   - force-app/main/default/classes/*.cls-meta.xml (metadata for each class)

4. Apex Triggers:
   - force-app/main/default/triggers/[ObjectName]Trigger.trigger
   - force-app/main/default/triggers/[ObjectName]Trigger.trigger-meta.xml
   - One trigger per Custom Object

5. Lightning Web Components:
   - force-app/main/default/lwc/[componentName]/[componentName].js
   - force-app/main/default/lwc/[componentName]/[componentName].html
   - force-app/main/default/lwc/[componentName]/[componentName].css
   - force-app/main/default/lwc/[componentName]/[componentName].js-meta.xml
   - Create all LWC components needed for Critical features

6. Lightning Pages & Tabs:
   - force-app/main/default/flexipages/*.flexipage-meta.xml (Lightning pages)
   - force-app/main/default/tabs/*.tab-meta.xml (custom tabs)
   - force-app/main/default/applications/*.app-meta.xml (Lightning apps)

7. Tests (Optional for Demo):
   - force-app/main/default/classes/*Test.cls (Apex test classes - optional)
   - Note: Tests are optional for demo mode but recommended for production

8. Scripts & Documentation:
   - scripts/setup.apex (demo data creation script)
   - scripts/deploy.sh (deployment automation)
   - DEPLOYMENT.md (deployment instructions)

CRITICAL REQUIREMENTS:
- Use Write tool to create files for MVP (Critical features only)
- Follow the SFDX folder structure EXACTLY
- Implement ONLY Critical priority features from research/implementation_plan.md
- DO NOT implement Medium or Low priority features
- Use proper Apex patterns (Service, Selector, Domain, Trigger Handler)
- Include minimal error handling (sufficient for demo)
- Use `with sharing` for all Apex classes by default
- Use WITH SECURITY_ENFORCED in SOQL queries
- Follow all exonpro coding standards
- Add minimal documentation (inline comments)
- Use platform security defaults (demo mode)
- Create placeholder components/classes for Medium/Low features (just structure, no logic)
- Tests are OPTIONAL for demo mode (skip if short on time)

IMPORTANT - Update CLAUDE.md as you work:
1. Mark each TODO as [x] when completed (there are 50+ TODOs for this phase)
2. Update "Last Updated" timestamp every 10-15 files created
3. Update "Next Action" field regularly
4. Add notes under "Phase 3 Notes" about:
   - Folder structure choices
   - Key implementation patterns used
   - Custom Objects design decisions
   - Apex class organization
   - Any deviations from standard patterns and why

WORKFLOW:
1. Start with SFDX project structure (sfdx-project.json, .gitignore, README) - mark as [x]
2. Then Custom Objects and Fields - mark each as [x]
3. Then Apex classes (Controllers, Services, Selectors) - mark as [x]
4. Then Apex triggers and handlers - mark as [x]
5. Then LWC components - mark as [x]
6. Then Lightning Pages and navigation - mark as [x]
7. Finally scripts and documentation - mark as [x]

Use Write tool to create each file. After every 5-10 files, update CLAUDE.md to track progress.
Work systematically through CLAUDE.md TODOs.
"""

    def build_phase4_prompt(self) -> str:
        """Phase 4: Minimal testing & validation."""
        return """
PHASE 4: Minimal Testing & Validation

⚠️ CRITICAL: First, read CLAUDE.md in the project root to see your TODO list for this phase.

GOAL: Minimal validation to ensure code is syntactically correct. Not comprehensive testing.

Tasks (detailed in CLAUDE.md):
1. Validate SFDX project structure (run: sf project retrieve preview)
2. Check Apex syntax (no actual compilation until deployment)
3. Validate LWC components structure
4. Create brief validation report

KEEP TESTING MINIMAL (DEMO MODE):
- Skip comprehensive Apex unit tests (optional for demo)
- Skip LWC Jest tests (optional for demo)
- Skip integration tests (not needed for demo)
- Skip code coverage requirements (not needed for demo)
- Focus on: "Is the structure correct? Is syntax valid?"

Note: Salesforce validates and compiles code during deployment (Phase 5).
If you find critical syntax errors, fix them. Otherwise, move to deployment.

IMPORTANT - Update CLAUDE.md as you work:
1. Mark each TODO as [x] when completed
2. Update "Last Updated" timestamp
3. Update "Next Action" field
4. Add notes under "Phase 4 Notes" about:
   - Structure validation success/failure
   - Any critical syntax errors fixed
   - What was skipped (comprehensive tests - demo mode)

Work through CLAUDE.md TODOs systematically.
"""

    def build_phase5_prompt(self) -> str:
        """Phase 5: Deployment setup."""
        return """
PHASE 5: MVP Deployment to Salesforce

⚠️ CRITICAL: First, read CLAUDE.md in the project root to see your TODO list for this phase.

GOAL: Deploy a working MVP to Salesforce Developer Org.

Set up deployment to Salesforce org.

Tasks (detailed in CLAUDE.md):
1. Verify Salesforce CLI authentication (run: sf org list)
2. Deploy source code: sf project deploy start
3. Capture deployment results
4. Run scripts/setup.apex to create demo data
5. Open org and verify deployment
6. Create deployment-output.json with org info
7. Update README.md with org access information
8. Create MVP_STATUS.md with completion report

DEPLOYMENT COMMANDS:
```bash
# Deploy all source
sf project deploy start

# Run setup script to create demo data
sf apex run --file scripts/setup.apex

# Open org
sf org open
```

DEPLOYMENT OUTPUT CAPTURE:
After deployment completes, save these details:
- Org Username
- Org ID
- Instance URL
- Deployed Components (Objects, Classes, LWC)
- Any deployment warnings or errors

CRITICAL - Create MVP_STATUS.md:
Calculate completion percentage by counting TODOs in CLAUDE.md:
- Total TODOs: grep "^- \[ \]" CLAUDE.md | wc -l
- Completed TODOs: grep "^- \[x\]" CLAUDE.md | wc -l
- Completion %: (completed / total) * 100

Create MVP_STATUS.md with:
```markdown
# MVP Status Report

## Completion: XX%

### What's Working
- [List deployed features]
- [Salesforce org details]

### What's Not Complete
- [List incomplete TODOs from CLAUDE.md]

### Salesforce Org Access
- Username: [org username]
- Org ID: [org id]
- Access: sf org open
- Instance URL: [instance URL]

### Deployed Components
- Custom Objects: [count]
- Apex Classes: [count]
- LWC Components: [count]
- Lightning Pages: [count]

### Next Actions
1. [Priority 1 incomplete TODO]
2. [Priority 2 incomplete TODO]
3. [Priority 3 incomplete TODO]

### Estimated Time to 100%
X hours (based on remaining TODOs)
```

IMPORTANT - Update CLAUDE.md as you work:
1. Mark each TODO as [x] when completed
2. Update "Last Updated" timestamp
3. Update "Current Phase" based on completion:
   - If 100% complete: "COMPLETED"
   - If 80-99% complete: "MVP DEPLOYED - Refinements remaining"
   - If <80% complete: "MVP DEPLOYED - Core features remaining"
4. Update "Next Action" with priority incomplete TODOs
5. Add notes under "Phase 5 Notes" about:
   - Deployment success/warnings/errors
   - Org access details
   - Deployed components
   - What works vs what's incomplete
   - Demo data created

Even if not 100% complete, deploy what exists. A working 70% MVP is better than a non-deployed 100% plan.
Work through CLAUDE.md TODOs systematically.
"""

    async def execute_phase(self, phase_id: str, phase_name: str, requirements: str, salesforce_config: dict, context: dict) -> bool:
        """
        Execute a single build phase using Claude SDK.

        Args:
            phase_id: Phase identifier (e.g., '0_configuration')
            phase_name: Human-readable phase name
            requirements: Requirements text
            salesforce_config: Salesforce configuration
            context: Exonpro framework context

        Returns:
            True if successful, False otherwise
        """
        logger.info(f"\n{'='*60}")
        logger.info(f"Starting Phase: {phase_name}")
        logger.info(f"{'='*60}\n")

        self.log_summary(f"━━━ Starting: {phase_name} ━━━", display=True)

        if self.dry_run:
            logger.info(f"[DRY RUN] Would execute phase: {phase_id}")
            return True

        try:
            # Build prompts
            self.display_progress(phase_name, "Building prompts...")
            system_prompt = self.build_system_prompt(context)
            user_prompt = self.build_phase_prompt(phase_id, requirements, salesforce_config, context)

            full_prompt = f"{system_prompt}\n\n---\n\n{user_prompt}"

            # Get Claude CLI path (.bat wrapper on Windows, binary on Unix)
            claude_cli_path = self._get_claude_cli_path()
            logger.info(f"Using Claude CLI: {claude_cli_path}")

            # Create options
            options = ClaudeAgentOptions(
                permission_mode='bypassPermissions',
                cwd=str(self.project_root),
                setting_sources=["project"],  # Use Claude Pro subscription
                cli_path=claude_cli_path
            )

            # Execute query and process messages
            message_count = 0
            response_text = ""

            self.display_progress(phase_name, "Starting Claude Code session...")
            self.log_detailed(f"\n{'='*70}")
            self.log_detailed(f"Phase: {phase_name}")
            self.log_detailed(f"Started: {datetime.now().isoformat()}")
            self.log_detailed(f"{'='*70}\n")

            async for message in query(prompt=full_prompt, options=options):
                message_count += 1

                # Show progress every 10 messages
                if message_count % 10 == 0:
                    self.display_progress(phase_name, f"Processing... ({message_count} messages received)")

                # Handle different message types
                if isinstance(message, str):
                    # Text content from Claude
                    if self.verbose:
                        logger.debug(f"[Message {message_count}] Received {len(message)} chars")
                    self.log_detailed(message)
                    response_text += message
                elif isinstance(message, dict):
                    # Structured message
                    text = message.get('text') or message.get('content') or message.get('message', '')
                    if text:
                        if not isinstance(text, str):
                            text = str(text)
                        self.log_detailed(text)
                        response_text += text
                elif hasattr(message, 'text'):
                    # Object with text attribute
                    text = str(message.text) if not isinstance(message.text, str) else message.text
                    self.log_detailed(text)
                    response_text += text
                elif hasattr(message, 'content'):
                    # Object with content attribute
                    content = message.content
                    if isinstance(content, list):
                        text = ""
                        for block in content:
                            if isinstance(block, dict):
                                text += block.get('text', '') or block.get('content', '') or ''
                            elif hasattr(block, 'text'):
                                text += str(block.text)
                            elif isinstance(block, str):
                                text += block
                            else:
                                text += str(block)
                        content = text
                    elif not isinstance(content, str):
                        content = str(content)

                    self.log_detailed(content)
                    response_text += content
                else:
                    # Unknown message type
                    if self.verbose:
                        logger.debug(f"[Message {message_count}] Unknown type: {type(message)}")

            self.log_detailed(f"\n{'='*70}")
            self.log_detailed(f"Phase completed: {phase_name}")
            self.log_detailed(f"Messages: {message_count}, Chars: {len(response_text)}")
            self.log_detailed(f"Ended: {datetime.now().isoformat()}")
            self.log_detailed(f"{'='*70}\n")

            self.log_summary(f"✅ Completed: {phase_name} ({message_count} messages, {len(response_text)} chars)", display=True)

            logger.info(f"\n✅ Phase completed: {phase_name}")
            logger.info(f"   Messages: {message_count}, Response: {len(response_text)} chars\n")

            if message_count == 0:
                raise Exception("No messages received from Claude SDK")

            return True

        except Exception as e:
            logger.error(f"\n❌ Phase failed: {phase_name}")
            logger.error(f"   Error: {str(e)}\n")
            self.log_summary(f"❌ Failed: {phase_name} - Error: {str(e)}", display=True)
            self.log_detailed(f"\n{'='*70}")
            self.log_detailed(f"Phase FAILED: {phase_name}")
            self.log_detailed(f"Error: {str(e)}")
            self.log_detailed(f"{'='*70}\n")
            return False

    async def run(self) -> bool:
        """
        Run the complete build process through all phases.

        Returns:
            True if successful, False otherwise
        """
        logger.info(f"\n╔════════════════════════════════════════╗")
        logger.info(f"║   Exonpro Automated Builder v1.0.0    ║")
        logger.info(f"╚════════════════════════════════════════╝\n")

        self.log_summary("╔════════════════════════════════════════╗", display=True)
        self.log_summary("║   Exonpro Automated Builder v1.0.0    ║", display=True)
        self.log_summary("╚════════════════════════════════════════╝", display=True)
        self.log_summary("", display=True)

        try:
            # Load requirements
            logger.info("📋 Loading requirements...")
            self.log_summary("📋 Loading requirements...", display=True)
            requirements = self.load_requirements()

            # Load Salesforce config
            logger.info("⚙️  Loading Salesforce configuration...")
            self.log_summary("⚙️  Loading Salesforce configuration...", display=True)
            salesforce_config = self.load_salesforce_config()

            # Load exonpro context
            logger.info("⚙️  Loading exonpro framework context...")
            self.log_summary("⚙️  Loading exonpro framework context...", display=True)
            context = self.load_context()

            # Load state
            state = self.load_state()

            # Handle resume
            if self.resume:
                logger.info("🔄 Resuming from last checkpoint...\n")
                logger.info(f"Current phase: {state['current_phase']}")
                logger.info(f"Completed phases: {', '.join(state['completed_phases']) if state['completed_phases'] else 'None'}\n")
                self.log_summary("🔄 Resuming from last checkpoint...", display=True)
                self.log_summary(f"Current phase: {state['current_phase']}", display=True)
                self.log_summary(f"Completed phases: {', '.join(state['completed_phases']) if state['completed_phases'] else 'None'}", display=True)
            else:
                logger.info("🚀 Starting automated build process...\n")
                self.log_summary("🚀 Starting automated build process...", display=True)
                self.log_summary("", display=True)

            # Determine which phases to execute
            phases_to_execute = []
            if self.resume and state['completed_phases']:
                # Skip completed phases
                for phase_id, phase_name, estimated_time in self.PHASES:
                    if phase_id not in state['completed_phases']:
                        phases_to_execute.append((phase_id, phase_name, estimated_time))
            else:
                # Execute all phases
                phases_to_execute = self.PHASES

            if not phases_to_execute:
                logger.info("✓ All phases already completed!")
                return True

            # Execute each phase
            total_phases = len(phases_to_execute)
            for idx, (phase_id, phase_name, estimated_time) in enumerate(phases_to_execute, 1):
                logger.info(f"Phase {idx}/{total_phases}: {phase_name} (estimated: {estimated_time})")
                self.log_summary(f"", display=True)
                self.log_summary(f"Phase {idx}/{total_phases}: {phase_name} (estimated: {estimated_time})", display=True)

                # Mark phase as in progress
                state['current_phase'] = phase_id
                state['phase_status'][phase_id] = 'in_progress'
                self.save_state(state)

                # Execute the phase
                success = await self.execute_phase(phase_id, phase_name, requirements, salesforce_config, context)

                if not success:
                    logger.error(f"\n❌ Build failed at phase: {phase_name}")
                    self.log_summary(f"❌ Build failed at phase: {phase_name}", display=True)
                    state['phase_status'][phase_id] = 'failed'
                    self.save_state(state)
                    return False

                # Mark phase as completed
                state['completed_phases'].append(phase_id)
                state['phase_status'][phase_id] = 'completed'
                self.save_state(state)

                logger.info(f"✓ Phase {phase_name} completed\n")

            logger.info(f"\n✓ Build completed successfully!")
            logger.info(f"\nGenerated files are ready for review and deployment.")
            logger.info(f"Detailed log: {self.detailed_log}")
            logger.info(f"Summary log: {self.summary_log}\n")

            self.log_summary("", display=True)
            self.log_summary("✓ Build completed successfully!", display=True)
            self.log_summary("", display=True)
            self.log_summary(f"Detailed log: {self.detailed_log}", display=True)
            self.log_summary(f"Summary log: {self.summary_log}", display=True)

            return True

        except Exception as e:
            logger.error(f"\n❌ Build failed: {str(e)}")
            self.log_summary(f"❌ Build failed: {str(e)}", display=True)
            import traceback
            traceback.print_exc()
            return False


async def async_main(args):
    """Async main entry point."""
    project_root = args.project_dir
    requirements_path = args.requirements

    if not project_root.exists():
        logger.error(f"Project directory not found: {project_root}")
        sys.exit(1)

    if not requirements_path.exists():
        logger.error(f"Requirements file not found: {requirements_path}")
        logger.error(f"Please create requirements.md in {project_root}")
        sys.exit(1)

    builder = ExonproBuilder(
        project_root=project_root,
        requirements_path=requirements_path,
        verbose=args.verbose,
        dry_run=args.dry_run,
        resume=args.resume
    )

    try:
        success = await builder.run()
        sys.exit(0 if success else 1)
    except KeyboardInterrupt:
        logger.info("\n\nBuild interrupted by user")
        sys.exit(1)
    except Exception as e:
        logger.error(f"\nUnexpected error: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)


def main():
    """Main entry point."""
    parser = argparse.ArgumentParser(
        description='Exonpro Automated Builder - Build complete Salesforce applications from requirements',
        formatter_class=argparse.RawDescriptionHelpFormatter
    )

    parser.add_argument(
        'project_dir',
        type=str,
        help='Path to project directory to build'
    )

    parser.add_argument(
        '--verbose',
        action='store_true',
        help='Enable verbose logging for debugging'
    )

    parser.add_argument(
        '--dry-run',
        action='store_true',
        help='Run in dry-run mode (do not execute commands)'
    )

    parser.add_argument(
        '--resume',
        action='store_true',
        help='Resume from last checkpoint'
    )

    args = parser.parse_args()

    # Convert project_dir to absolute path
    args.project_dir = Path(args.project_dir).resolve()

    # Requirements file is in project directory
    args.requirements = args.project_dir / 'requirements.md'

    # Run the async main function
    asyncio.run(async_main(args))


if __name__ == '__main__':
    main()
