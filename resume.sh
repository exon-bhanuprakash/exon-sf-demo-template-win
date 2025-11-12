#!/bin/bash

# Exonpro Template - Resume Build
# Resumes an interrupted build from last checkpoint

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
echo -e "${BLUE}║   Exonpro - Resume Build               ║${NC}"
echo -e "${BLUE}╚════════════════════════════════════════╝${NC}"
echo ""

# Ask for project directory
if [ -z "$1" ]; then
    read -p "Enter project directory path: " PROJECT_DIR
else
    PROJECT_DIR="$1"
fi

# Expand ~ to home directory
PROJECT_DIR="${PROJECT_DIR/#\~/$HOME}"

# Check if project directory exists
if [ ! -d "$PROJECT_DIR" ]; then
    echo -e "${RED}❌ Error: Project directory not found: $PROJECT_DIR${NC}"
    exit 1
fi

# Check if state file exists
if [ ! -f "$PROJECT_DIR/.exon/phases/state.json" ]; then
    echo -e "${RED}❌ Error: No build state found${NC}"
    echo ""
    echo "Cannot resume - no previous build found in $PROJECT_DIR"
    echo "Use ./start.sh to start a new build."
    exit 1
fi

# Show current state
echo -e "${BLUE}Build State:${NC}"
echo ""

# More reliable JSON parsing for Windows Git Bash
STATE_FILE="$PROJECT_DIR/.exon/phases/state.json"
python -c "
import json
import sys
import os

state_file = sys.argv[1]

# Convert Git Bash path to Windows path if needed
if state_file.startswith('/c/'):
    state_file = 'C:/' + state_file[3:]
elif state_file.startswith('/'):
    # Try to handle other drive letters
    parts = state_file[1:].split('/', 1)
    if len(parts[0]) == 1 and parts[0].isalpha():
        state_file = parts[0].upper() + ':/' + (parts[1] if len(parts) > 1 else '')

try:
    with open(state_file, 'r') as f:
        data = json.load(f)

    current_phase = data.get('current_phase', 'unknown')
    completed = ', '.join(data.get('completed_phases', [])) or 'none'
    phase_status = data.get('phase_status', {})

    print(f'  Current phase: {current_phase}')
    print(f'  Completed: {completed}')

    # Show phase status if current phase has failed
    if current_phase in phase_status and phase_status[current_phase] == 'failed':
        print(f'  [!] Last phase failed - will retry from phase {current_phase}')
except Exception as e:
    print(f'  Error reading state: {e}')
    sys.exit(1)
" "$STATE_FILE"

echo ""

# Show incomplete TODOs from CLAUDE.md
if [ -f "$PROJECT_DIR/CLAUDE.md" ]; then
    echo -e "${YELLOW}Incomplete TODOs (first 10):${NC}"
    echo ""
    grep -n "^- \[ \]" "$PROJECT_DIR/CLAUDE.md" | head -10 | while read -r line; do
        echo "  $line"
    done
    echo ""

    TOTAL_INCOMPLETE=$(grep -c "^- \[ \]" "$PROJECT_DIR/CLAUDE.md" || echo "0")
    TOTAL_COMPLETE=$(grep -c "^- \[x\]" "$PROJECT_DIR/CLAUDE.md" || echo "0")
    echo "  Total: $TOTAL_COMPLETE completed, $TOTAL_INCOMPLETE remaining"
    echo ""
fi

# Check for Python venv
if [ ! -d "builder/venv" ]; then
    echo -e "${YELLOW}⚠${NC} Creating Python virtual environment..."
    cd builder
    python -m venv venv
    ./venv/Scripts/pip install -q -r requirements.txt
    cd ..
fi

echo -e "${GREEN}✓${NC} Claude Agent SDK ready"
echo -e "${GREEN}✓${NC} Project directory: $PROJECT_DIR"
echo ""
echo -e "${YELLOW}Resuming build from last checkpoint...${NC}"
echo ""
read -p "Press Enter to resume, or Ctrl+C to cancel..."
echo ""

# Run the Python builder with --resume flag
export PYTHONIOENCODING=utf-8
./builder/venv/Scripts/python builder/build.py "$PROJECT_DIR" --resume

EXIT_CODE=$?

echo ""
if [ $EXIT_CODE -eq 0 ]; then
    echo -e "${GREEN}╔════════════════════════════════════════╗${NC}"
    echo -e "${GREEN}║   ✓ Build Complete                     ║${NC}"
    echo -e "${GREEN}╚════════════════════════════════════════╝${NC}"
    echo ""
    echo "Build resumed and completed successfully!"
else
    echo -e "${RED}╔════════════════════════════════════════╗${NC}"
    echo -e "${RED}║   ✗ Build Failed                       ║${NC}"
    echo -e "${RED}╚════════════════════════════════════════╝${NC}"
    echo ""
    echo "Build failed. Check logs in: $PROJECT_DIR/.exon/logs/"
fi

echo ""
