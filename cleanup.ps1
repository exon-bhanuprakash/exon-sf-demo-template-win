# Exonpro Template - Cleanup Project (Windows PowerShell)
# Safely delete a generated project with confirmation

param(
    [Parameter(Position=0)]
    [string]$ProjectPath
)

$ErrorActionPreference = "Stop"

# Colors
function Write-Blue { Write-Host $args -ForegroundColor Blue }
function Write-Green { Write-Host $args -ForegroundColor Green }
function Write-Yellow { Write-Host $args -ForegroundColor Yellow }
function Write-Red { Write-Host $args -ForegroundColor Red }

Write-Blue "╔════════════════════════════════════════╗"
Write-Blue "║   Exonpro - Cleanup Project            ║"
Write-Blue "╚════════════════════════════════════════╝"
Write-Host ""

# Get project path
if (-not $ProjectPath) {
    $ProjectPath = Read-Host "Enter project directory path to delete"
}

# Expand environment variables
$ProjectPath = [Environment]::ExpandEnvironmentVariables($ProjectPath)

# Validate project directory exists
if (-not (Test-Path $ProjectPath)) {
    Write-Red "❌ Error: Project directory not found: $ProjectPath"
    exit 1
}

# Display project info
Write-Host "Project to delete: $ProjectPath"
Write-Host ""

# Check if it's an Exonpro project
$configFile = Join-Path $ProjectPath ".exon\config\project.json"
if (Test-Path $configFile) {
    $config = Get-Content $configFile -Raw | ConvertFrom-Json
    Write-Yellow "Project Details:"
    Write-Host "  Name: $($config.project_name)"
    Write-Host "  Stack: $($config.stack_template)"
    Write-Host "  Created: $($config.created_at)"
    Write-Host ""
} else {
    Write-Yellow "⚠ Warning: This doesn't appear to be an Exonpro project."
    Write-Host ""
}

# Calculate size
$size = (Get-ChildItem -Path $ProjectPath -Recurse -Force | Measure-Object -Property Length -Sum).Sum
$sizeMB = [math]::Round($size / 1MB, 2)
Write-Host "Directory size: $sizeMB MB"
Write-Host ""

# Safety confirmation
Write-Red "⚠ WARNING: This will permanently delete all files in this directory!"
Write-Host ""
Write-Host "To confirm deletion, type: DELETE"
$confirmation = Read-Host "Confirmation"

if ($confirmation -ne "DELETE") {
    Write-Yellow "Deletion cancelled. Project preserved."
    exit 0
}

Write-Host ""
Write-Host "Deleting project..."

try {
    Remove-Item -Path $ProjectPath -Recurse -Force
    Write-Green "✓ Project deleted successfully"
    Write-Host ""
    Write-Host "Deleted: $ProjectPath"
} catch {
    Write-Red "❌ Error deleting project: $_"
    Write-Host ""
    Write-Host "You may need to close any applications using files in this directory."
    exit 1
}

Write-Host ""
