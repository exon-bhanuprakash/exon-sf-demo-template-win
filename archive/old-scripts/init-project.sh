#!/bin/bash

# Exonpro Template - New Project Initialization Script
# Usage: ./init-project.sh <project-name> <target-directory>

set -e

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Function to print colored output
print_info() {
    echo -e "${BLUE}ℹ${NC} $1"
}

print_success() {
    echo -e "${GREEN}✓${NC} $1"
}

print_warning() {
    echo -e "${YELLOW}⚠${NC} $1"
}

print_error() {
    echo -e "${RED}✗${NC} $1"
}

# Function to print banner
print_banner() {
    echo ""
    echo -e "${BLUE}╔════════════════════════════════════════╗${NC}"
    echo -e "${BLUE}║   Exonpro Template Initialization     ║${NC}"
    echo -e "${BLUE}╚════════════════════════════════════════╝${NC}"
    echo ""
}

# Check arguments
if [ "$#" -lt 1 ]; then
    print_error "Usage: ./init-project.sh <project-name> [target-directory]"
    echo ""
    echo "Examples:"
    echo "  ./init-project.sh my-saas-app"
    echo "  ./init-project.sh my-saas-app ~/projects"
    echo "  ./init-project.sh my-saas-app /Users/john/Documents/clients"
    exit 1
fi

PROJECT_NAME=$1
TARGET_BASE_DIR=${2:-.}  # Default to current directory if not specified

# Validate project name (alphanumeric, hyphens, underscores only)
if ! [[ "$PROJECT_NAME" =~ ^[a-zA-Z0-9_-]+$ ]]; then
    print_error "Invalid project name. Use only letters, numbers, hyphens, and underscores."
    exit 1
fi

# Get absolute path of template directory (where this script lives)
TEMPLATE_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"

# Create target directory path
TARGET_DIR="$TARGET_BASE_DIR/$PROJECT_NAME"

print_banner

print_info "Template location: $TEMPLATE_DIR"
print_info "Project name: $PROJECT_NAME"
print_info "Target location: $TARGET_DIR"
echo ""

# Check if target already exists
if [ -d "$TARGET_DIR" ]; then
    print_error "Directory $TARGET_DIR already exists!"
    read -p "Do you want to remove it and continue? (y/N): " -n 1 -r
    echo
    if [[ $REPLY =~ ^[Yy]$ ]]; then
        print_warning "Removing existing directory..."
        rm -rf "$TARGET_DIR"
    else
        print_error "Aborted."
        exit 1
    fi
fi

# Create target base directory if it doesn't exist
mkdir -p "$TARGET_BASE_DIR"

print_info "Copying template to $TARGET_DIR..."

# Copy template to target location, excluding certain files/directories
rsync -av \
    --exclude='.git' \
    --exclude='node_modules' \
    --exclude='.DS_Store' \
    --exclude='*.log' \
    --exclude='.env*' \
    --exclude='__pycache__' \
    --exclude='*.pyc' \
    --exclude='.exon/logs' \
    --exclude='.exon/phases/checkpoints' \
    --exclude='builder/node_modules' \
    --exclude='builder/dist' \
    --exclude='init-project.sh' \
    "$TEMPLATE_DIR/" "$TARGET_DIR/"

print_success "Template copied successfully"

# Navigate to new project
cd "$TARGET_DIR"

# Clean up template-specific content
print_info "Cleaning up template-specific files..."

# Remove any existing research/architecture/specs content (keep only README.md)
find research -type f ! -name 'README.md' -delete 2>/dev/null || true
find architecture -type f ! -name 'README.md' -delete 2>/dev/null || true
find specs -type f ! -name 'README.md' -delete 2>/dev/null || true
find specs/phases -type f -delete 2>/dev/null || true

# Reset state.json
cat > .exon/phases/state.json <<EOF
{
  "current_phase": null,
  "current_sub_phase": null,
  "completed_phases": [],
  "phase_status": {
    "0_configuration": "pending",
    "1_research": "pending",
    "2_architecture": "pending",
    "3_implementation": "pending",
    "4_testing": "pending",
    "5_deployment": "pending"
  },
  "start_time": null,
  "last_update": null,
  "total_duration_minutes": 0,
  "can_resume": false,
  "last_checkpoint": null,
  "errors": [],
  "warnings": [],
  "metadata": {
    "builder_version": "1.0.0",
    "claude_sdk_version": null,
    "stack_template": null
  }
}
EOF

# Reset project.json with project name and selected stack
cat > .exon/config/project.json <<EOF
{
  "project_name": "$PROJECT_NAME",
  "project_type": "web_application",
  "description": "Exonpro project",
  "tech_stack": {
    "hosting": "aws_serverless",
    "frontend": "sveltekit",
    "backend": "$(echo $STACK_NAME | grep -o 'nodejs\|python\|hybrid\|fastapi' | head -1)",
    "database": "$(echo $STACK_NAME | grep -o 'dynamodb\|postgres' | head -1)",
    "language": "typescript_python"
  },
  "stack_template": "$STACK_NAME",
  "created_at": "$(date -u +"%Y-%m-%dT%H:%M:%SZ")",
  "exonpro_version": "1.0.0",
  "metadata": {
    "business_domain": "to_be_determined",
    "target_users": "to_be_determined",
    "expected_scale": "small_to_medium"
  }
}
EOF

print_success "Template files cleaned"

# Initialize git repository
print_info "Initializing git repository..."
git init
git checkout -b dev

# Create .gitignore if it doesn't exist
if [ ! -f .gitignore ]; then
    print_warning ".gitignore not found, creating one..."
    # .gitignore should already be copied, but just in case
fi

# Initial commit
print_info "Creating initial commit..."
git add .
git commit -m "Initial commit - Exonpro template initialized

Project: $PROJECT_NAME
Template version: 1.0.0
Created: $(date -u +"%Y-%m-%dT%H:%M:%SZ")

🤖 Initialized with Exonpro Template"

print_success "Git repository initialized on 'dev' branch"

# Create logs directory
mkdir -p .exon/logs
mkdir -p .exon/phases/checkpoints

print_success "Project structure initialized"

# Create a sample requirements template if it doesn't exist
if [ ! -f requirements.md ]; then
    print_info "Creating sample requirements.md template..."
    cat > requirements.md <<'EOF'
# Project Name: PROJECT_NAME

## Business Problem
[What problem does this solve? 2-3 sentences]

## Solution
[How does your app solve it? 2-3 sentences]

## Target Users
- [User type 1]: [Description]
- [User type 2]: [Description]

## Key Features
1. User authentication (email/password)
2. [Feature 2]
3. [Feature 3]
4. [Feature 4]
5. [Feature 5]

## Scale Requirements
- Expected users: [Number, e.g., 100-1,000 in first year]
- Traffic pattern: [Predictable/Variable/Spiky]
- Budget: [$X/month, e.g., $25-50/month]
- Growth potential: [Low/Medium/High]

## Technical Requirements
- Authentication: Yes
- File uploads: [Yes/No] [Max size if yes]
- Real-time features: [Yes/No]
- AI/ML: [Yes/No] [What kind if yes]
- Third-party integrations: [List any, e.g., Stripe for payments]
- Payment processing: [Yes/No]

## Compliance & Security
- Data compliance: [GDPR/HIPAA/None]
- Special security needs: [List any]

## Timeline
- MVP deadline: [Date]
- Full launch: [Date]
EOF

    # Replace PROJECT_NAME placeholder
    if [[ "$OSTYPE" == "darwin"* ]]; then
        # macOS
        sed -i '' "s/PROJECT_NAME/$PROJECT_NAME/g" requirements.md
    else
        # Linux
        sed -i "s/PROJECT_NAME/$PROJECT_NAME/g" requirements.md
    fi

    print_success "Created requirements.md template"
fi

# Select tech stack
print_info "Tech Stack Selection"
echo ""
echo "Available stacks:"
echo ""
echo "1. aws-serverless-svelte-hybrid-dynamodb-nodejs-python (RECOMMENDED)"
echo "   - Best for: Apps needing both CRUD APIs and data processing"
echo "   - Backend: Node.js (APIs) + Python (analytics, ML, reports)"
echo "   - Cost: ~$20-50/month for small-medium scale"
echo ""
echo "2. aws-serverless-svelte-dynamodb-nodejs"
echo "   - Best for: Pure Node.js teams, real-time apps"
echo "   - Backend: Node.js only"
echo "   - Cost: ~$15-40/month"
echo ""
echo "3. aws-serverless-svelte-fastapi-dynamodb-python"
echo "   - Best for: Python teams, data-heavy apps, ML integration"
echo "   - Backend: Python FastAPI"
echo "   - Cost: ~$25-60/month"
echo ""
echo "4. aws-lightsail-svelte-fastapi-postgres"
echo "   - Best for: Need PostgreSQL, predictable costs, fixed budget"
echo "   - Backend: Python FastAPI + PostgreSQL"
echo "   - Cost: Fixed ~$25/month"
echo ""

read -p "Select stack [1-4] (default: 1): " STACK_CHOICE
STACK_CHOICE=${STACK_CHOICE:-1}

case $STACK_CHOICE in
    1)
        STACK_NAME="aws-serverless-svelte-hybrid-dynamodb-nodejs-python"
        ;;
    2)
        STACK_NAME="aws-serverless-svelte-dynamodb-nodejs"
        ;;
    3)
        STACK_NAME="aws-serverless-svelte-fastapi-dynamodb-python"
        ;;
    4)
        STACK_NAME="aws-lightsail-svelte-fastapi-postgres"
        ;;
    *)
        print_error "Invalid choice. Using default: hybrid stack"
        STACK_NAME="aws-serverless-svelte-hybrid-dynamodb-nodejs-python"
        ;;
esac

print_success "Selected stack: $STACK_NAME"
echo ""

# Create and configure aws-config.json
print_info "AWS Configuration Setup"
echo ""

# Get AWS credentials
echo "Please provide your AWS details (or press Enter to skip and configure manually later):"
echo ""

read -p "AWS Account ID (from 'aws sts get-caller-identity'): " AWS_ACCOUNT_ID
read -p "AWS Region [us-east-1]: " AWS_REGION
AWS_REGION=${AWS_REGION:-us-east-1}

read -p "AWS Profile name [default]: " AWS_PROFILE
AWS_PROFILE=${AWS_PROFILE:-default}

read -p "Your email for notifications: " CONTACT_EMAIL
CONTACT_EMAIL=${CONTACT_EMAIL:-admin@example.com}

echo ""

if [ ! -f aws-config.json ]; then
    print_info "Creating aws-config.json from template..."
    cp aws-config.template.json aws-config.json
fi

# Update aws-config.json with provided values
if [ -n "$AWS_ACCOUNT_ID" ]; then
    print_info "Updating AWS configuration..."

    if [[ "$OSTYPE" == "darwin"* ]]; then
        # macOS
        sed -i '' "s/\"name\": \".*\"/\"name\": \"$PROJECT_NAME\"/g" aws-config.json
        sed -i '' "s/\"account_id\": \".*\"/\"account_id\": \"$AWS_ACCOUNT_ID\"/g" aws-config.json
        sed -i '' "s/\"region\": \".*\"/\"region\": \"$AWS_REGION\"/g" aws-config.json
        sed -i '' "s/\"profile\": \".*\"/\"profile\": \"$AWS_PROFILE\"/g" aws-config.json
        sed -i '' "s/admin@example.com/$CONTACT_EMAIL/g" aws-config.json
    else
        # Linux
        sed -i "s/\"name\": \".*\"/\"name\": \"$PROJECT_NAME\"/g" aws-config.json
        sed -i "s/\"account_id\": \".*\"/\"account_id\": \"$AWS_ACCOUNT_ID\"/g" aws-config.json
        sed -i "s/\"region\": \".*\"/\"region\": \"$AWS_REGION\"/g" aws-config.json
        sed -i "s/\"profile\": \".*\"/\"profile\": \"$AWS_PROFILE\"/g" aws-config.json
        sed -i "s/admin@example.com/$CONTACT_EMAIL/g" aws-config.json
    fi

    print_success "AWS configuration updated"
    print_info "Account: $AWS_ACCOUNT_ID"
    print_info "Region: $AWS_REGION"
    print_info "Profile: $AWS_PROFILE"
else
    print_warning "AWS configuration skipped - you can edit aws-config.json manually"
fi

echo ""

# Personalize documentation files with project name
print_info "Personalizing documentation files..."

# Convert project-name to Title Case for display
PROJECT_TITLE=$(echo "$PROJECT_NAME" | sed 's/-/ /g' | awk '{for(i=1;i<=NF;i++) $i=toupper(substr($i,1,1)) tolower(substr($i,2));}1')

# Update README.md
if [ -f README.md ]; then
    if [[ "$OSTYPE" == "darwin"* ]]; then
        sed -i '' "1s/.*/# $PROJECT_TITLE/" README.md
        sed -i '' "s/Exonpro Universal App Template/$PROJECT_TITLE - Exonpro Project/g" README.md
        sed -i '' "s/exon-template/$PROJECT_NAME/g" README.md
    else
        sed -i "1s/.*/# $PROJECT_TITLE/" README.md
        sed -i "s/Exonpro Universal App Template/$PROJECT_TITLE - Exonpro Project/g" README.md
        sed -i "s/exon-template/$PROJECT_NAME/g" README.md
    fi
fi

# Update CLAUDE.md
if [ -f CLAUDE.md ]; then
    if [[ "$OSTYPE" == "darwin"* ]]; then
        sed -i '' "s/Exonpro Universal App Template/$PROJECT_TITLE/g" CLAUDE.md
        sed -i '' "s/exon-template/$PROJECT_NAME/g" CLAUDE.md
        sed -i '' "s/\[Project Name\]/$PROJECT_TITLE/g" CLAUDE.md
    else
        sed -i "s/Exonpro Universal App Template/$PROJECT_TITLE/g" CLAUDE.md
        sed -i "s/exon-template/$PROJECT_NAME/g" CLAUDE.md
        sed -i "s/\[Project Name\]/$PROJECT_TITLE/g" CLAUDE.md
    fi
fi

# Update START_HERE.md
if [ -f START_HERE.md ]; then
    if [[ "$OSTYPE" == "darwin"* ]]; then
        sed -i '' "s/Exonpro Template/$PROJECT_TITLE/g" START_HERE.md
        sed -i '' "s/exon-template/$PROJECT_NAME/g" START_HERE.md
    else
        sed -i "s/Exonpro Template/$PROJECT_TITLE/g" START_HERE.md
        sed -i "s/exon-template/$PROJECT_NAME/g" START_HERE.md
    fi
fi

# Update .exon/constitution.md
if [ -f .exon/constitution.md ]; then
    if [[ "$OSTYPE" == "darwin"* ]]; then
        sed -i '' "s/Exonpro Universal App Template/$PROJECT_TITLE/g" .exon/constitution.md
        sed -i '' "s/exon-template/$PROJECT_NAME/g" .exon/constitution.md
    else
        sed -i "s/Exonpro Universal App Template/$PROJECT_TITLE/g" .exon/constitution.md
        sed -i "s/exon-template/$PROJECT_NAME/g" .exon/constitution.md
    fi
fi

# Update WHATS-NEW.md and QUICK-REFERENCE.md (make them project-specific)
if [ -f WHATS-NEW.md ]; then
    if [[ "$OSTYPE" == "darwin"* ]]; then
        sed -i '' "1i\\
# $PROJECT_TITLE - What's New\\
\\
**Project**: $PROJECT_NAME  \\
**Initialized**: $(date '+%B %d, %Y')  \\
\\
---\\
\\
" WHATS-NEW.md
    else
        sed -i "1i # $PROJECT_TITLE - What's New\n\n**Project**: $PROJECT_NAME  \n**Initialized**: $(date '+%B %d, %Y')  \n\n---\n\n" WHATS-NEW.md
    fi
fi

if [ -f QUICK-REFERENCE.md ]; then
    if [[ "$OSTYPE" == "darwin"* ]]; then
        sed -i '' "1s/.*/#  $PROJECT_TITLE - Quick Reference/" QUICK-REFERENCE.md
        sed -i '' "s/Exonpro Template/$PROJECT_TITLE/g" QUICK-REFERENCE.md
    else
        sed -i "1s/.*/#  $PROJECT_TITLE - Quick Reference/" QUICK-REFERENCE.md
        sed -i "s/Exonpro Template/$PROJECT_TITLE/g" QUICK-REFERENCE.md
    fi
fi

print_success "Documentation personalized with project name"

# Copy automation scripts
print_info "Setting up automation scripts..."

# Copy start-build.sh
if [ -f "$TEMPLATE_DIR/start-build.sh" ]; then
    cp "$TEMPLATE_DIR/start-build.sh" ./
    chmod +x start-build.sh
    print_success "Copied start-build.sh"
fi

# Copy resume-project.sh
if [ -f "$TEMPLATE_DIR/resume-project.sh" ]; then
    cp "$TEMPLATE_DIR/resume-project.sh" ./
    chmod +x resume-project.sh
    print_success "Copied resume-project.sh"
fi

# Copy update-resume-context.sh
if [ -f "$TEMPLATE_DIR/update-resume-context.sh" ]; then
    cp "$TEMPLATE_DIR/update-resume-context.sh" ./
    chmod +x update-resume-context.sh
    print_success "Copied update-resume-context.sh"
fi

# Ask if user wants to build now
echo ""
echo -e "${BLUE}╔════════════════════════════════════════╗${NC}"
echo -e "${BLUE}║   Automated Build Setup                ║${NC}"
echo -e "${BLUE}╚════════════════════════════════════════╝${NC}"
echo ""

if [ -n "$AWS_ACCOUNT_ID" ]; then
    echo "Would you like to start the automated build now?"
    echo ""
    echo "This will:"
    echo "  1. Prepare requirements.md"
    echo "  2. Spawn a NEW Claude session (via SDK)"
    echo "  3. Build complete application automatically"
    echo "  4. Deploy to AWS dev environment"
    echo ""
    echo "Estimated time: 4-6 hours"
    echo ""
    read -p "Start automated build? [y/N]: " START_BUILD

    if [[ $START_BUILD =~ ^[Yy]$ ]]; then
        echo ""
        echo "Requirements file options:"
        echo "  1. Edit requirements.md now (interactive)"
        echo "  2. Use existing requirements file (provide path)"
        echo "  3. Skip editing (edit manually later)"
        echo ""
        read -p "Choose option [1-3] (default: 1): " REQ_OPTION
        REQ_OPTION=${REQ_OPTION:-1}

        case $REQ_OPTION in
            1)
                print_info "Opening requirements.md for editing..."
                echo "Fill in your business requirements, then save and close."
                echo ""
                read -p "Press Enter to open editor..."
                ${EDITOR:-nano} requirements.md
                print_success "Requirements saved"
                ;;
            2)
                echo ""
                read -p "Enter path to your requirements.md file: " EXISTING_REQ_PATH
                if [ -f "$EXISTING_REQ_PATH" ]; then
                    cp "$EXISTING_REQ_PATH" requirements.md
                    print_success "Requirements copied from $EXISTING_REQ_PATH"
                else
                    print_error "File not found: $EXISTING_REQ_PATH"
                    print_warning "Using template requirements.md - please edit it manually before build"
                fi
                ;;
            3)
                print_warning "Skipping requirements edit"
                print_info "Make sure to edit requirements.md before starting build!"
                ;;
            *)
                print_warning "Invalid option, skipping edit"
                ;;
        esac

        echo ""
        print_info "Starting automated build..."
        print_warning "This spawns a NEW Claude session. Do not close this terminal!"
        echo ""

        # Start the automated build (spawns new Claude session)
        ./start-build.sh
    else
        print_info "Skipping automated build"
    fi
fi

# Print next steps
echo ""
echo -e "${GREEN}╔════════════════════════════════════════╗${NC}"
echo -e "${GREEN}║   ✓ Project Initialized Successfully  ║${NC}"
echo -e "${GREEN}╚════════════════════════════════════════╝${NC}"
echo ""
print_info "Project location: $TARGET_DIR"
echo ""

if [ -n "$AWS_ACCOUNT_ID" ]; then
    echo -e "${GREEN}✓ AWS Configured:${NC}"
    echo "  Account: $AWS_ACCOUNT_ID"
    echo "  Region: $AWS_REGION"
    echo ""
fi

echo -e "${BLUE}Next Steps:${NC}"
echo ""
echo "1. Navigate to project:"
echo -e "   ${YELLOW}cd $TARGET_DIR${NC}"
echo ""
echo "2. Edit requirements.md with your business details"
echo ""
echo "3. Start automated build (spawns NEW Claude session):"
echo -e "   ${YELLOW}./start-build.sh${NC}"
echo ""
echo "   This will:"
echo "   - Spawn a fresh Claude session via SDK"
echo "   - Execute all 5 build phases automatically"
echo "   - Deploy complete app to AWS dev"
echo "   - Takes 4-6 hours total"
echo ""
echo -e "${BLUE}💾 Resume Support:${NC}"
echo "   If build crashes, resume automatically:"
echo -e "   ${YELLOW}./resume-project.sh${NC}"
echo "   (Also spawns NEW Claude session, continues from checkpoint)"
echo ""
echo -e "${BLUE}🚀 After Dev Deployment:${NC}"
echo "   Deploy to staging:"
echo -e "   ${YELLOW}npm run deploy:stage${NC}"
echo ""
echo "   Deploy to production:"
echo -e "   ${YELLOW}npm run deploy:prod${NC}"
echo ""
echo -e "${BLUE}📖 Documentation:${NC}"
echo "   - START_HERE.md - Quick start guide"
echo "   - AUTOMATION-SUMMARY.md - How automation works"
echo "   - RESUME-GUIDE.md - Resume flow details"
echo "   - QUICK_START_MANUAL.md - Manual build (no automation)"
echo ""
