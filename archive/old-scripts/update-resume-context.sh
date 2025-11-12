#!/bin/bash

# Exonpro Template - Update Resume Context
# Called by Claude during build to update resume context

set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cd "$SCRIPT_DIR"

# This script is called by Claude to update the resume context
# after completing each sub-phase

STATE_FILE=".exon/phases/state.json"
RESUME_CONTEXT_FILE=".claude/resume-context.md"

if [ ! -f "$STATE_FILE" ]; then
    echo "Error: state.json not found"
    exit 1
fi

# Update timestamp in state.json
TIMESTAMP=$(date -u +"%Y-%m-%dT%H:%M:%SZ")
jq --arg timestamp "$TIMESTAMP" '.last_update = $timestamp' "$STATE_FILE" > "$STATE_FILE.tmp"
mv "$STATE_FILE.tmp" "$STATE_FILE"

# Regenerate resume context
bash resume-project.sh > /dev/null 2>&1 || true

echo "Resume context updated at $TIMESTAMP"
