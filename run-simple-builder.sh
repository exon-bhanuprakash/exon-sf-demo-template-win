#!/bin/bash

# Simple TODO Builder Launcher
# Just loops Claude sessions to work through TODO.md

set -e

TEMPLATE_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cd "$TEMPLATE_DIR"

# Default project
DEFAULT_PROJECT="/Users/kusaldipdas/Documents/00_All_Work/exon-hr-hubv3.0"

# Colors
BLUE='\033[0;34m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
NC='\033[0m'

echo -e "${BLUE}╔════════════════════════════════════════╗${NC}"
echo -e "${BLUE}║   Simple TODO Builder                  ║${NC}"
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

# Check project
if [ ! -d "$PROJECT_DIR" ]; then
    echo -e "${RED}❌ Project not found: $PROJECT_DIR${NC}"
    exit 1
fi

# Check for venv
if [ ! -d "builder/venv" ]; then
    echo -e "${YELLOW}⚠️  Creating Python virtual environment...${NC}"
    cd builder
    python3 -m venv venv
    ./venv/bin/pip install -q -r requirements.txt
    cd ..
    echo -e "${GREEN}✓ Virtual environment ready${NC}"
fi

echo ""
echo -e "${GREEN}Starting Simple TODO Builder...${NC}"
echo -e "${GREEN}Project: ${PROJECT_DIR}${NC}"
echo ""

# Get max iterations (optional)
MAX_ITERATIONS=""
if [ "$2" = "--batch" ]; then
    MAX_ITERATIONS="--max-iterations ${3:-10}"
fi

# Run the builder
./builder/venv/bin/python3 builder/simple-todo-builder.py "$PROJECT_DIR" $MAX_ITERATIONS

EXIT_CODE=$?

echo ""
if [ $EXIT_CODE -eq 0 ]; then
    echo -e "${GREEN}✓ Builder completed${NC}"
else
    echo -e "${YELLOW}⚠️  Builder stopped${NC}"
fi
echo ""
