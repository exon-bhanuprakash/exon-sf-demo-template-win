#!/bin/bash

# Simple script to run TODO builder on exon-hr-hubv3.0

set -e

TEMPLATE_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cd "$TEMPLATE_DIR"

# Default project path
DEFAULT_PROJECT="/Users/kusaldipdas/Documents/00_All_Work/exon-hr-hubv3.0"

# Colors
BLUE='\033[0;34m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m'

echo -e "${BLUE}╔════════════════════════════════════════╗${NC}"
echo -e "${BLUE}║   TODO-Driven Builder Launcher         ║${NC}"
echo -e "${BLUE}╚════════════════════════════════════════╝${NC}"
echo ""

# Get project path
if [ -z "$1" ]; then
    echo -e "${YELLOW}Using default project: ${DEFAULT_PROJECT}${NC}"
    PROJECT_DIR="$DEFAULT_PROJECT"
else
    PROJECT_DIR="$1"
fi

# Expand ~
PROJECT_DIR="${PROJECT_DIR/#\~/$HOME}"

# Check project exists
if [ ! -d "$PROJECT_DIR" ]; then
    echo -e "${RED}❌ Error: Project not found: $PROJECT_DIR${NC}"
    exit 1
fi

# Check for Python venv
if [ ! -d "builder/venv" ]; then
    echo -e "${YELLOW}⚠️  Creating Python virtual environment...${NC}"
    cd builder
    python3 -m venv venv
    ./venv/bin/pip install -q -r requirements.txt
    cd ..
    echo -e "${GREEN}✓ Virtual environment ready${NC}"
fi

echo ""
echo -e "${GREEN}Starting TODO-Driven Builder...${NC}"
echo -e "${GREEN}Project: ${PROJECT_DIR}${NC}"
echo ""

# Run the builder
./builder/venv/bin/python3 builder/todo-builder.py "$PROJECT_DIR" "$@"

EXIT_CODE=$?

echo ""
if [ $EXIT_CODE -eq 0 ]; then
    echo -e "${GREEN}✓ Builder completed successfully${NC}"
else
    echo -e "${YELLOW}⚠️  Builder stopped${NC}"
fi
echo ""
