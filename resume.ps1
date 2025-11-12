# Exonpro Template - Resume Build (Windows PowerShell)
# Resumes an interrupted build from last checkpoint

param(
    [Parameter(Position=0)]
    [string]$ProjectPath
)

$ErrorActionPreference = "Stop"

$TEMPLATE_DIR = Split-Path -Parent $MyInvocation.MyCommand.Path

# Colors
function Write-Blue { Write-Host $args -ForegroundColor Blue }
function Write-Green { Write-Host $args -ForegroundColor Green }
function Write-Yellow { Write-Host $args -ForegroundColor Yellow }
function Write-Red { Write-Host $args -ForegroundColor Red }

Write-Blue "╔════════════════════════════════════════╗"
Write-Blue "║   Exonpro - Resume Build               ║"
Write-Blue "╚════════════════════════════════════════╝"
Write-Host ""

# Get project path
if (-not $ProjectPath) {
    $ProjectPath = Read-Host "Enter project directory path"
}

# Expand environment variables
$ProjectPath = [Environment]::ExpandEnvironmentVariables($ProjectPath)

# Validate project directory
if (-not (Test-Path $ProjectPath)) {
    Write-Red "❌ Error: Project directory not found: $ProjectPath"
    exit 1
}

# Check for state file
$stateFile = Join-Path $ProjectPath ".exon\phases\state.json"
if (-not (Test-Path $stateFile)) {
    Write-Red "❌ Error: No build state found in project."
    Write-Host "This project may not have been created with the automated builder."
    exit 1
}

# Load state
$state = Get-Content $stateFile -Raw | ConvertFrom-Json

Write-Host "Project: $ProjectPath"
Write-Host ""
Write-Green "Build State:"
Write-Host "  Current Phase: $($state.current_phase)"
Write-Host "  Completed Phases: $($state.completed_phases -join ', ')"
Write-Host "  Last Updated: $($state.last_updated)"
Write-Host ""

# Check if already complete
if ($state.completed_phases.Count -eq 6) {
    Write-Green "✓ Build already complete!"
    Write-Host ""
    Write-Host "All 6 phases have been completed."
    Write-Host "Check the project at: $ProjectPath"
    exit 0
}

# Confirm resume
$confirm = Read-Host "Resume build from last checkpoint? [Y/n]"
if (-not $confirm) { $confirm = "Y" }

if ($confirm -notmatch "^[Yy]$") {
    Write-Yellow "Resume cancelled."
    exit 0
}

Write-Host ""
Write-Green "Resuming automated build..."
Write-Host ""

# Check for Python venv
if (-not (Test-Path "$TEMPLATE_DIR\builder\venv")) {
    Write-Host "Creating Python virtual environment..."
    Set-Location "$TEMPLATE_DIR\builder"
    python -m venv venv
    & ".\venv\Scripts\pip.exe" install -q -r requirements.txt
    Set-Location $TEMPLATE_DIR
    Write-Green "✓ Python venv created"
}

# Run the Python builder with --resume flag
Set-Location $TEMPLATE_DIR
& ".\builder\venv\Scripts\python.exe" "builder\build.py" "$ProjectPath" --resume

$EXIT_CODE = $LASTEXITCODE

Write-Host ""
if ($EXIT_CODE -eq 0) {
    Write-Green "╔════════════════════════════════════════╗"
    Write-Green "║   ✓ Build Complete                     ║"
    Write-Green "╚════════════════════════════════════════╝"
    Write-Host ""
    Write-Host "Your application has been built and deployed!"
    Write-Host ""
    Write-Host "Project location: $ProjectPath"
} else {
    Write-Red "╔════════════════════════════════════════╗"
    Write-Red "║   ✗ Build Failed                       ║"
    Write-Red "╚════════════════════════════════════════╝"
    Write-Host ""
    Write-Host "Build failed. Check logs in: $ProjectPath\.exon\logs\"
    Write-Host ""
    Write-Host "To retry:"
    Write-Host "  .\resume.ps1 $ProjectPath"
}

Write-Host ""
