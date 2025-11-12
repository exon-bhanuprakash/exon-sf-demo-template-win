#!/bin/bash

# Exonpro Template - Cleanup Project
# Completely removes a project directory

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
echo -e "${BLUE}║   Exonpro - Cleanup Project            ║${NC}"
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

echo -e "${RED}⚠ WARNING: This will COMPLETELY DELETE the entire project!${NC}"
echo ""
echo "Project directory: $PROJECT_DIR"
echo ""
echo -e "${YELLOW}This will delete:${NC}"
echo "  - ALL files and folders in this directory"
echo "  - Generated code (infrastructure, backend, frontend)"
echo "  - Configuration files (requirements.md, aws-config.json)"
echo "  - Build state and logs"
echo "  - EVERYTHING!"
echo ""
echo -e "${RED}This action CANNOT be undone!${NC}"
echo ""
read -p "Type 'DELETE' to confirm: " CONFIRM

if [ "$CONFIRM" != "DELETE" ]; then
    echo ""
    echo "Cleanup cancelled."
    exit 0
fi

echo ""
echo -e "${BLUE}Deleting project...${NC}"
echo ""

# Remove the entire directory
rm -rf "$PROJECT_DIR"

echo -e "${GREEN}✓ Project deleted${NC}"
echo ""
echo "Deleted: $PROJECT_DIR"
echo ""
echo "To create a new project:"
echo "  ./start.sh"
echo ""
