# Exonpro Template - Start New Project (Windows PowerShell)
# Collects inputs, creates project, and starts automated build

$ErrorActionPreference = "Stop"

$TEMPLATE_DIR = Split-Path -Parent $MyInvocation.MyCommand.Path
Set-Location $TEMPLATE_DIR

# Colors
function Write-Blue { Write-Host $args -ForegroundColor Blue }
function Write-Green { Write-Host $args -ForegroundColor Green }
function Write-Yellow { Write-Host $args -ForegroundColor Yellow }
function Write-Red { Write-Host $args -ForegroundColor Red }

Write-Blue "╔════════════════════════════════════════╗"
Write-Blue "║   Exonpro - New Project Setup         ║"
Write-Blue "╚════════════════════════════════════════╝"
Write-Host ""

# Step 1: Project Name
Write-Blue "Step 1: Project Information"
Write-Host ""
$PROJECT_NAME = Read-Host "Enter project name (lowercase, hyphens allowed)"

# Validate project name
if ($PROJECT_NAME -notmatch '^[a-z0-9-]+$') {
    Write-Red "❌ Invalid project name. Use lowercase letters, numbers, and hyphens only."
    exit 1
}

# Step 2: Target Directory
Write-Host ""
$defaultPath = Join-Path $env:USERPROFILE "Documents\00_All_Work\ExonProProjects"
$targetInput = Read-Host "Enter parent directory path [$defaultPath]"
$TARGET_BASE_DIR = if ($targetInput) { $targetInput } else { $defaultPath }

# Expand environment variables if present
$TARGET_BASE_DIR = [Environment]::ExpandEnvironmentVariables($TARGET_BASE_DIR)

$PROJECT_DIR = Join-Path $TARGET_BASE_DIR $PROJECT_NAME

# Check if project already exists
if (Test-Path $PROJECT_DIR) {
    Write-Red "❌ Error: Project directory already exists: $PROJECT_DIR"
    Write-Host ""
    $reply = Read-Host "Delete it and start fresh? [y/N]"
    if ($reply -match "^[Yy]$") {
        Remove-Item -Path $PROJECT_DIR -Recurse -Force
        Write-Green "✓ Removed existing directory"
    } else {
        exit 1
    }
}

# Step 3: Tech Stack Selection
Write-Host ""
Write-Blue "Step 2: Tech Stack Selection"
Write-Host ""
Write-Host "Available stack:"
Write-Host ""
Write-Host "1. salesforce-lwc-apex (Salesforce Platform)"
Write-Host "   Frontend: Lightning Web Components (LWC)"
Write-Host "   Backend: Apex"
Write-Host "   Database: Salesforce Objects"
Write-Host "   Best for: Salesforce demos and applications"
Write-Host "   Deployment: Developer Org (free)"
Write-Host ""

$STACK_NAME = "salesforce-lwc-apex"
Write-Green "✓ Selected: $STACK_NAME"

# Step 4: Salesforce Configuration
Write-Host ""
Write-Blue "Step 3: Salesforce Configuration"
Write-Host ""
Write-Host "Get your Salesforce org info by running: sf org list"
Write-Host ""

$orgUsernameInput = Read-Host "Salesforce Org Username [your@email.com]"
$ORG_USERNAME = if ($orgUsernameInput) { $orgUsernameInput } else { "your@email.com" }

$orgAliasInput = Read-Host "Salesforce Org Alias [DevOrg]"
$ORG_ALIAS = if ($orgAliasInput) { $orgAliasInput } else { "DevOrg" }

$contactEmailInput = Read-Host "Your email for project contact [kusaldip.das@exonpro.com]"
$CONTACT_EMAIL = if ($contactEmailInput) { $contactEmailInput } else { "kusaldip.das@exonpro.com" }

# Step 5: Create Project Structure
Write-Host ""
Write-Blue "Step 4: Creating Project"
Write-Host ""

New-Item -Path $PROJECT_DIR -ItemType Directory -Force | Out-Null
Set-Location $PROJECT_DIR

# Create necessary directories
Write-Host "Creating directory structure..."
New-Item -Path ".exon\config" -ItemType Directory -Force | Out-Null
New-Item -Path ".exon\phases" -ItemType Directory -Force | Out-Null
New-Item -Path ".exon\logs" -ItemType Directory -Force | Out-Null
New-Item -Path ".exon\standards" -ItemType Directory -Force | Out-Null
New-Item -Path ".exon\stacks\$STACK_NAME" -ItemType Directory -Force | Out-Null

# Copy standards and stacks from template
Write-Host "Copying framework files..."
if (Test-Path "$TEMPLATE_DIR\.exon\standards") {
    Copy-Item -Path "$TEMPLATE_DIR\.exon\standards\*" -Destination ".exon\standards\" -Recurse -Force -ErrorAction SilentlyContinue
}
if (Test-Path "$TEMPLATE_DIR\.exon\stacks") {
    Copy-Item -Path "$TEMPLATE_DIR\.exon\stacks\*" -Destination ".exon\stacks\" -Recurse -Force -ErrorAction SilentlyContinue
}

# Create requirements.md template
Write-Host "Creating requirements.md template..."
@"
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
1. User authentication (Salesforce platform)
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
"@ | Out-File -FilePath "requirements.md" -Encoding UTF8

# Create salesforce-config.json
Write-Host "Creating salesforce-config.json..."
@"
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
"@ | Out-File -FilePath "salesforce-config.json" -Encoding UTF8

# Create state.json
@"
{
  "current_phase": null,
  "completed_phases": [],
  "phase_status": {},
  "started_at": null,
  "last_updated": null
}
"@ | Out-File -FilePath ".exon\phases\state.json" -Encoding UTF8

# Create project.json
$BUILD_TIMESTAMP = Get-Date -Format "yyyy-MM-ddTHH:mm:ssZ" -AsUTC
@"
{
  "project_name": "$PROJECT_NAME",
  "stack_template": "$STACK_NAME",
  "created_at": "$BUILD_TIMESTAMP",
  "exonpro_version": "1.0.0"
}
"@ | Out-File -FilePath ".exon\config\project.json" -Encoding UTF8

# Create CLAUDE.md from template
Write-Host "Creating CLAUDE.md project brain..."
if (Test-Path "$TEMPLATE_DIR\.exon\standards\CLAUDE.md.template") {
    $claudeContent = Get-Content "$TEMPLATE_DIR\.exon\standards\CLAUDE.md.template" -Raw
    $claudeContent = $claudeContent -replace '{{PROJECT_NAME}}', $PROJECT_NAME
    $claudeContent = $claudeContent -replace '{{LAST_UPDATED}}', $BUILD_TIMESTAMP
    $claudeContent = $claudeContent -replace '{{CURRENT_PHASE}}', 'Not Started'
    $claudeContent = $claudeContent -replace '{{BUILD_STARTED}}', $BUILD_TIMESTAMP
    $claudeContent = $claudeContent -replace '{{NEXT_ACTION}}', 'Start Phase 0: Configuration validation'
    $claudeContent = $claudeContent -replace '{{PHASE0_STATUS}}', 'PENDING'
    $claudeContent = $claudeContent -replace '{{PHASE1_STATUS}}', 'PENDING'
    $claudeContent = $claudeContent -replace '{{PHASE2_STATUS}}', 'PENDING'
    $claudeContent = $claudeContent -replace '{{PHASE3_STATUS}}', 'PENDING'
    $claudeContent = $claudeContent -replace '{{PHASE4_STATUS}}', 'PENDING'
    $claudeContent = $claudeContent -replace '{{PHASE5_STATUS}}', 'PENDING'
    $claudeContent = $claudeContent -replace '{{STACK_NAME}}', $STACK_NAME
    $claudeContent = $claudeContent -replace '{{ORG_USERNAME}}', $ORG_USERNAME
    $claudeContent = $claudeContent -replace '{{ORG_ALIAS}}', $ORG_ALIAS
    $claudeContent = $claudeContent -replace '{{CONTACT_EMAIL}}', $CONTACT_EMAIL
    $claudeContent | Out-File -FilePath "CLAUDE.md" -Encoding UTF8
}

# Initialize git
Write-Host "Initializing git repository..."
git init -q
git checkout -b dev -q 2>$null
git add .
$commitTimestamp = Get-Date -Format "yyyy-MM-ddTHH:mm:ssZ" -AsUTC
git commit -q -m @"
Initial commit - $PROJECT_NAME

Stack: $STACK_NAME
Created: $commitTimestamp

🤖 Initialized with Exonpro Template
"@

Write-Green "✓ Project created successfully"
Write-Host ""
Write-Host "Project location: $PROJECT_DIR"
Write-Host ""

# Step 6: Edit Requirements
Write-Blue "Step 5: Configure Requirements"
Write-Host ""
Write-Host "Options:"
Write-Host "  1. Edit requirements.md now (opens editor)"
Write-Host "  2. Copy from existing requirements file"
Write-Host "  3. Skip editing (edit manually later)"
Write-Host ""
$reqOption = Read-Host "Choose option [1-3] (default: 1)"
if (-not $reqOption) { $reqOption = "1" }

switch ($reqOption) {
    "1" {
        Write-Host ""
        Write-Host "Opening requirements.md for editing..."
        Write-Host "Fill in your business requirements, then save and close."
        Write-Host ""
        Read-Host "Press Enter to open editor..."

        # Try to find a suitable editor
        if (Get-Command "code" -ErrorAction SilentlyContinue) {
            code "requirements.md" -w
        } elseif (Get-Command "notepad++" -ErrorAction SilentlyContinue) {
            & "notepad++" "requirements.md"
        } else {
            notepad "requirements.md"
        }
        Write-Green "✓ Requirements saved"
    }
    "2" {
        Write-Host ""
        $existingReqPath = Read-Host "Enter path to existing requirements file"
        $existingReqPath = [Environment]::ExpandEnvironmentVariables($existingReqPath)

        if (Test-Path $existingReqPath) {
            Copy-Item -Path $existingReqPath -Destination "requirements.md" -Force
            Write-Green "✓ Requirements copied from $existingReqPath"
        } else {
            Write-Red "❌ File not found: $existingReqPath"
            Write-Host "Keeping template requirements.md - please edit it manually"
        }
        Write-Host ""
        Read-Host "Press Enter to continue..."
    }
    "3" {
        Write-Yellow "⚠ Skipping requirements edit"
        Write-Host ""
        Write-Host "IMPORTANT: Edit requirements.md before starting the build!"
        Write-Host ""
        Read-Host "Press Enter to continue..."
    }
}

# Step 7: Check Python venv
Write-Host ""
Write-Blue "Step 6: Preparing Builder"
Write-Host ""

Set-Location $TEMPLATE_DIR

if (-not (Test-Path "builder\venv")) {
    Write-Host "Creating Python virtual environment..."
    Set-Location "builder"
    python -m venv venv
    & ".\venv\Scripts\pip.exe" install -q -r requirements.txt
    Set-Location ".."
    Write-Green "✓ Python venv created"
}

# Step 8: Confirm and Start Build
Write-Host ""
Write-Blue "╔════════════════════════════════════════╗"
Write-Blue "║   Ready to Build                       ║"
Write-Blue "╚════════════════════════════════════════╝"
Write-Host ""
Write-Green "Project Configuration:"
Write-Host "  Name: $PROJECT_NAME"
Write-Host "  Location: $PROJECT_DIR"
Write-Host "  Stack: $STACK_NAME"
Write-Host "  Salesforce Org: $ORG_USERNAME"
Write-Host "  Org Alias: $ORG_ALIAS"
Write-Host ""
Write-Yellow "Build Process:"
Write-Host "  Phase 0: Configuration validation (5-10 min)"
Write-Host "  Phase 1: Research & feature planning (30-60 min)"
Write-Host "  Phase 2: Architecture design (45-90 min)"
Write-Host "  Phase 3: Code generation (2-4 hours)"
Write-Host "  Phase 4: Testing & validation (30-60 min)"
Write-Host "  Phase 5: Deployment to Salesforce (45-90 min)"
Write-Host ""
Write-Yellow "Total estimated time: 4-6 hours"
Write-Host ""
$startBuild = Read-Host "Start automated build now? [Y/n]"
if (-not $startBuild) { $startBuild = "Y" }

if ($startBuild -notmatch "^[Yy]$") {
    Write-Host ""
    Write-Yellow "Build cancelled."
    Write-Host ""
    Write-Host "To start the build later:"
    Write-Host "  cd $TEMPLATE_DIR"
    Write-Host "  .\start.ps1 $PROJECT_DIR"
    Write-Host ""
    exit 0
}

Write-Host ""
Write-Green "Starting automated build..."
Write-Host ""

# Run the Python builder
& ".\builder\venv\Scripts\python.exe" "builder\build.py" "$PROJECT_DIR"

$EXIT_CODE = $LASTEXITCODE

Write-Host ""
if ($EXIT_CODE -eq 0) {
    Write-Green "╔════════════════════════════════════════╗"
    Write-Green "║   ✓ Build Complete                     ║"
    Write-Green "╚════════════════════════════════════════╝"
    Write-Host ""
    Write-Host "Your application has been built and deployed!"
    Write-Host ""
    Write-Host "Project location: $PROJECT_DIR"
    Write-Host ""
    Write-Blue "Next steps:"
    Write-Host "  1. Review generated code"
    Write-Host "  2. Test the dev deployment"
    Write-Host "  3. Deploy to staging/prod if ready"
} else {
    Write-Red "╔════════════════════════════════════════╗"
    Write-Red "║   ✗ Build Failed                       ║"
    Write-Red "╚════════════════════════════════════════╝"
    Write-Host ""
    Write-Host "Build failed. Check logs in: $PROJECT_DIR\.exon\logs\"
    Write-Host ""
    Write-Host "To resume:"
    Write-Host "  cd $TEMPLATE_DIR"
    Write-Host "  .\resume.ps1 $PROJECT_DIR"
}

Write-Host ""
