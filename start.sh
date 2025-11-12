#!/bin/bash

# Exonpro Template - Start New Project
# Collects inputs, creates project, and starts automated build

set -e

TEMPLATE_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cd "$TEMPLATE_DIR"

# Colors
BLUE='\033[0;34m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
NC='\033[0m'

echo -e "${BLUE}╔════════════════════════════════════════╗${NC}"
echo -e "${BLUE}║   Exonpro - New Project Setup         ║${NC}"
echo -e "${BLUE}╚════════════════════════════════════════╝${NC}"
echo ""

# Step 1: Project Name
echo -e "${BLUE}Step 1: Project Information${NC}"
echo ""
read -p "Enter project name (lowercase, hyphens allowed): " PROJECT_NAME

# Validate project name
if ! [[ "$PROJECT_NAME" =~ ^[a-z0-9-]+$ ]]; then
    echo -e "${RED}❌ Invalid project name. Use lowercase letters, numbers, and hyphens only.${NC}"
    exit 1
fi

# Step 2: Target Directory
echo ""
read -p "Enter parent directory path [~/Documents/00_All_Work/ExonProProjects]: " TARGET_BASE_DIR
TARGET_BASE_DIR="${TARGET_BASE_DIR:-$HOME/Documents/00_All_Work/ExonProProjects}"
TARGET_BASE_DIR="${TARGET_BASE_DIR/#\~/$HOME}"

PROJECT_DIR="$TARGET_BASE_DIR/$PROJECT_NAME"

# Check if project already exists
if [ -d "$PROJECT_DIR" ]; then
    echo -e "${RED}❌ Error: Project directory already exists: $PROJECT_DIR${NC}"
    echo ""
    read -p "Delete it and start fresh? [y/N]: " -n 1 -r
    echo ""
    if [[ $REPLY =~ ^[Yy]$ ]]; then
        rm -rf "$PROJECT_DIR"
        echo -e "${GREEN}✓ Removed existing directory${NC}"
    else
        exit 1
    fi
fi

# Step 3: Tech Stack Selection
echo ""
echo -e "${BLUE}Step 2: Tech Stack Selection${NC}"
echo ""
echo "Available stack:"
echo ""
echo "1. salesforce-lwc-apex (Salesforce Platform)"
echo "   Frontend: Lightning Web Components (LWC)"
echo "   Backend: Apex"
echo "   Database: Salesforce Objects"
echo "   Best for: Salesforce demos and applications"
echo "   Deployment: Developer Org (free)"
echo ""

STACK_NAME="salesforce-lwc-apex"
echo -e "${GREEN}✓ Selected: $STACK_NAME${NC}"

# Step 4: Salesforce Configuration
echo ""
echo -e "${BLUE}Step 3: Salesforce Configuration${NC}"
echo ""
echo "Get your Salesforce org info by running: sf org list"
echo ""

read -p "Salesforce Org Username [your@email.com]: " ORG_USERNAME
ORG_USERNAME=${ORG_USERNAME:-your@email.com}

read -p "Salesforce Org Alias [DevOrg]: " ORG_ALIAS
ORG_ALIAS=${ORG_ALIAS:-DevOrg}

read -p "Your email for project contact [kusaldip.das@exonpro.com]: " CONTACT_EMAIL
CONTACT_EMAIL=${CONTACT_EMAIL:-kusaldip.das@exonpro.com}

# Step 5: Create Project Structure
echo ""
echo -e "${BLUE}Step 4: Creating Project${NC}"
echo ""

mkdir -p "$PROJECT_DIR"
cd "$PROJECT_DIR"

# Create necessary directories
echo "Creating directory structure..."
mkdir -p .exon/config
mkdir -p .exon/phases
mkdir -p .exon/logs
mkdir -p .exon/standards
mkdir -p .exon/stacks/$STACK_NAME

# Copy standards and stacks from template
echo "Copying framework files..."
cp -r "$TEMPLATE_DIR/.exon/standards/"* .exon/standards/ 2>/dev/null || true
cp -r "$TEMPLATE_DIR/.exon/stacks/"* .exon/stacks/ 2>/dev/null || true

# Create requirements.md template
echo "Creating requirements.md template..."
cat > requirements.md <<EOF
# Project Name: $PROJECT_NAME

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
EOF

# Create salesforce-config.json
echo "Creating salesforce-config.json..."
cat > salesforce-config.json <<EOF
{
  "project": {
    "name": "$PROJECT_NAME",
    "description": "Salesforce application built with Exonpro",
    "version": "1.0.0"
  },
  "salesforce": {
    "org_username": "$ORG_USERNAME",
    "instance_url": "https://login.salesforce.com",
    "org_type": "developer",
    "api_version": "61.0",
    "org_alias": "$ORG_ALIAS"
  },
  "deployment": {
    "auto_deploy": false,
    "test_level": "NoTestRun",
    "deploy_on_save": true
  },
  "project_settings": {
    "source_api_version": "61.0",
    "namespace": "",
    "sfdx_login_url": "https://login.salesforce.com"
  },
  "feature_flags": {
    "generate_tests": false,
    "use_security_enforced": true,
    "bulkify_code": true,
    "pwa_support": false
  },
  "notifications": {
    "email": "$CONTACT_EMAIL",
    "slack_webhook": null
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
    "exclude": [
      "Profile"
    ]
  },
  "demo_mode": {
    "enabled": true,
    "skip_tests": true,
    "minimal_validation": true,
    "generate_sample_data": true
  }
}
EOF

# Create state.json
cat > .exon/phases/state.json <<EOF
{
  "current_phase": null,
  "completed_phases": [],
  "phase_status": {},
  "started_at": null,
  "last_updated": null
}
EOF

# Create project.json
cat > .exon/config/project.json <<EOF
{
  "project_name": "$PROJECT_NAME",
  "stack_template": "$STACK_NAME",
  "created_at": "$(date -u +"%Y-%m-%dT%H:%M:%SZ")",
  "exonpro_version": "1.0.0"
}
EOF

# Create CLAUDE.md from template
echo "Creating CLAUDE.md project brain..."
BUILD_TIMESTAMP=$(date -u +"%Y-%m-%dT%H:%M:%SZ")
sed -e "s/{{PROJECT_NAME}}/$PROJECT_NAME/g" \
    -e "s/{{LAST_UPDATED}}/$BUILD_TIMESTAMP/g" \
    -e "s/{{CURRENT_PHASE}}/Not Started/g" \
    -e "s/{{BUILD_STARTED}}/$BUILD_TIMESTAMP/g" \
    -e "s/{{NEXT_ACTION}}/Start Phase 0: Configuration validation/g" \
    -e "s/{{PHASE0_STATUS}}/PENDING/g" \
    -e "s/{{PHASE1_STATUS}}/PENDING/g" \
    -e "s/{{PHASE2_STATUS}}/PENDING/g" \
    -e "s/{{PHASE3_STATUS}}/PENDING/g" \
    -e "s/{{PHASE4_STATUS}}/PENDING/g" \
    -e "s/{{PHASE5_STATUS}}/PENDING/g" \
    -e "s/{{STACK_NAME}}/$STACK_NAME/g" \
    -e "s/{{ORG_USERNAME}}/$ORG_USERNAME/g" \
    -e "s/{{ORG_ALIAS}}/$ORG_ALIAS/g" \
    -e "s/{{CONTACT_EMAIL}}/$CONTACT_EMAIL/g" \
    "$TEMPLATE_DIR/.exon/standards/CLAUDE.md.template" > CLAUDE.md

# Initialize git
echo "Initializing git repository..."
git init -q
git checkout -b dev -q
git add .
git commit -q -m "Initial commit - $PROJECT_NAME

Stack: $STACK_NAME
Created: $(date -u +"%Y-%m-%dT%H:%M:%SZ")

🤖 Initialized with Exonpro Template"

echo -e "${GREEN}✓ Project created successfully${NC}"
echo ""
echo "Project location: $PROJECT_DIR"
echo ""

# Step 6: Edit Requirements
echo -e "${BLUE}Step 5: Configure Requirements${NC}"
echo ""
echo "Options:"
echo "  1. Edit requirements.md now (opens editor)"
echo "  2. Copy from existing requirements file"
echo "  3. Skip editing (edit manually later)"
echo ""
read -p "Choose option [1-3] (default: 1): " REQ_OPTION
REQ_OPTION=${REQ_OPTION:-1}

case $REQ_OPTION in
    1)
        echo ""
        echo "Opening requirements.md for editing..."
        echo "Fill in your business requirements, then save and close."
        echo ""
        read -p "Press Enter to open editor..."
        ${EDITOR:-nano} requirements.md
        echo -e "${GREEN}✓ Requirements saved${NC}"
        ;;
    2)
        echo ""
        read -p "Enter path to existing requirements file: " EXISTING_REQ_PATH
        EXISTING_REQ_PATH="${EXISTING_REQ_PATH/#\~/$HOME}"

        if [ -f "$EXISTING_REQ_PATH" ]; then
            cp "$EXISTING_REQ_PATH" requirements.md
            echo -e "${GREEN}✓ Requirements copied from $EXISTING_REQ_PATH${NC}"
        else
            echo -e "${RED}❌ File not found: $EXISTING_REQ_PATH${NC}"
            echo "Keeping template requirements.md - please edit it manually"
        fi
        echo ""
        read -p "Press Enter to continue..."
        ;;
    3)
        echo -e "${YELLOW}⚠ Skipping requirements edit${NC}"
        echo ""
        echo "IMPORTANT: Edit requirements.md before starting the build!"
        echo ""
        read -p "Press Enter to continue..."
        ;;
esac

# Step 7: Check Python venv
echo ""
echo -e "${BLUE}Step 6: Preparing Builder${NC}"
echo ""

cd "$TEMPLATE_DIR"

if [ ! -d "builder/venv" ]; then
    echo "Creating Python virtual environment..."
    cd builder
    python3 -m venv venv
    ./venv/bin/pip install -q -r requirements.txt
    cd ..
    echo -e "${GREEN}✓ Python venv created${NC}"
fi

# Step 8: Confirm and Start Build
echo ""
echo -e "${BLUE}╔════════════════════════════════════════╗${NC}"
echo -e "${BLUE}║   Ready to Build                       ║${NC}"
echo -e "${BLUE}╚════════════════════════════════════════╝${NC}"
echo ""
echo -e "${GREEN}Project Configuration:${NC}"
echo "  Name: $PROJECT_NAME"
echo "  Location: $PROJECT_DIR"
echo "  Stack: $STACK_NAME"
echo "  Salesforce Org: $ORG_USERNAME"
echo "  Org Alias: $ORG_ALIAS"
echo ""
echo -e "${YELLOW}Build Process:${NC}"
echo "  Phase 0: Configuration validation (5-10 min)"
echo "  Phase 1: Research & feature planning (30-60 min)"
echo "  Phase 2: Architecture design (45-90 min)"
echo "  Phase 3: Code generation (2-4 hours)"
echo "  Phase 4: Testing & validation (30-60 min)"
echo "  Phase 5: Deployment to Salesforce (45-90 min)"
echo ""
echo -e "${YELLOW}Total estimated time: 4-6 hours${NC}"
echo ""
read -p "Start automated build now? [Y/n]: " START_BUILD
START_BUILD=${START_BUILD:-Y}

if [[ ! $START_BUILD =~ ^[Yy]$ ]]; then
    echo ""
    echo -e "${YELLOW}Build cancelled.${NC}"
    echo ""
    echo "To start the build later:"
    echo "  cd $TEMPLATE_DIR"
    echo "  ./start.sh $PROJECT_DIR"
    echo ""
    exit 0
fi

echo ""
echo -e "${GREEN}Starting automated build...${NC}"
echo ""

# Run the Python builder
./builder/venv/bin/python3 builder/build.py "$PROJECT_DIR"

EXIT_CODE=$?

echo ""
if [ $EXIT_CODE -eq 0 ]; then
    echo -e "${GREEN}╔════════════════════════════════════════╗${NC}"
    echo -e "${GREEN}║   ✓ Build Complete                     ║${NC}"
    echo -e "${GREEN}╚════════════════════════════════════════╝${NC}"
    echo ""
    echo "Your application has been built and deployed!"
    echo ""
    echo "Project location: $PROJECT_DIR"
    echo ""
    echo -e "${BLUE}Next steps:${NC}"
    echo "  1. Review generated code"
    echo "  2. Test the dev deployment"
    echo "  3. Deploy to staging/prod if ready"
else
    echo -e "${RED}╔════════════════════════════════════════╗${NC}"
    echo -e "${RED}║   ✗ Build Failed                       ║${NC}"
    echo -e "${RED}╚════════════════════════════════════════╝${NC}"
    echo ""
    echo "Build failed. Check logs in: $PROJECT_DIR/.exon/logs/"
    echo ""
    echo "To resume:"
    echo "  cd $TEMPLATE_DIR"
    echo "  ./resume.sh $PROJECT_DIR"
fi

echo ""
