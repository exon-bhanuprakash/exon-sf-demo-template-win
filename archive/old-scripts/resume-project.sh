#!/bin/bash

# Exonpro Template - Resume Project Builder
# Automatically resumes project build from last checkpoint

set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cd "$SCRIPT_DIR"

# Colors
BLUE='\033[0;34m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
NC='\033[0m' # No Color

echo -e "${BLUE}╔════════════════════════════════════════╗${NC}"
echo -e "${BLUE}║   Exonpro Project Resume               ║${NC}"
echo -e "${BLUE}╚════════════════════════════════════════╝${NC}"
echo ""

# Check if state file exists
STATE_FILE=".exon/phases/state.json"
if [ ! -f "$STATE_FILE" ]; then
    echo -e "${RED}❌ Error: No state file found${NC}"
    echo ""
    echo "This doesn't appear to be an active Exonpro project."
    echo "Use init-project.sh to start a new project."
    exit 1
fi

# Check if can resume
CAN_RESUME=$(jq -r '.can_resume' "$STATE_FILE")
if [ "$CAN_RESUME" != "true" ]; then
    echo -e "${RED}❌ Error: Project is not in a resumable state${NC}"
    echo ""
    echo "The project may have completed or encountered an error."
    echo "Check .exon/phases/state.json for details."
    exit 1
fi

# Extract state information
PROJECT_NAME=$(jq -r '.metadata.project_name // "unknown"' .exon/config/project.json)
CURRENT_PHASE=$(jq -r '.current_phase' "$STATE_FILE")
CURRENT_SUB_PHASE=$(jq -r '.current_sub_phase' "$STATE_FILE")
LAST_UPDATE=$(jq -r '.last_update' "$STATE_FILE")
COMPLETED_PHASES=$(jq -r '.completed_phases | join(", ")' "$STATE_FILE")
STACK_TEMPLATE=$(jq -r '.metadata.stack_template' "$STATE_FILE")

echo -e "${BLUE}ℹ${NC} Project: ${GREEN}$PROJECT_NAME${NC}"
echo -e "${BLUE}ℹ${NC} Stack: ${GREEN}$STACK_TEMPLATE${NC}"
echo -e "${BLUE}ℹ${NC} Last update: $LAST_UPDATE"
echo ""
echo -e "${YELLOW}📍 Resuming from:${NC}"
echo -e "  Phase: ${GREEN}$CURRENT_PHASE${NC}"
if [ "$CURRENT_SUB_PHASE" != "null" ]; then
    echo -e "  Sub-phase: ${GREEN}$CURRENT_SUB_PHASE${NC}"
fi
echo ""
echo -e "${GREEN}✓${NC} Completed phases: $COMPLETED_PHASES"
echo ""

# Generate resume context for Claude
RESUME_CONTEXT_FILE=".claude/resume-context.md"
echo -e "${BLUE}ℹ${NC} Generating resume context for Claude..."

# Create resume context
cat > "$RESUME_CONTEXT_FILE" << EOF
# 🔄 AUTO-RESUME: $PROJECT_NAME

**IMPORTANT**: This is an automated resume context. When you (Claude) start this session, you MUST automatically resume the build without asking the user.

## Project Status

- **Project Name**: $PROJECT_NAME
- **Stack Template**: $STACK_TEMPLATE
- **Current Phase**: $CURRENT_PHASE
- **Current Sub-Phase**: $CURRENT_SUB_PHASE
- **Last Update**: $LAST_UPDATE

## Completed Phases

EOF

# Add completed phases with checkmarks
jq -r '.completed_phases[]' "$STATE_FILE" | while read phase; do
    echo "- ✅ $phase" >> "$RESUME_CONTEXT_FILE"
done

cat >> "$RESUME_CONTEXT_FILE" << EOF

## Current Phase Status

EOF

# Add current phase status
jq -r 'to_entries[] | "- \(.key): \(.value)"' "$STATE_FILE" | grep "phase_status" | while read line; do
    echo "$line" >> "$RESUME_CONTEXT_FILE"
done

cat >> "$RESUME_CONTEXT_FILE" << EOF

## Files to Load on Resume

### 1. Configuration Files
- \`requirements.md\` - Business requirements
- \`.exon/config/project.json\` - Project metadata
- \`.exon/config/aws-config.json\` - AWS configuration
- \`.exon/phases/state.json\` - Build state (YOU ARE READING THIS NOW)

### 2. Standards (Apply to all generated code)
- \`.exon/standards/code-structure.md\`
- \`.exon/standards/naming-conventions.md\`
- \`.exon/standards/security-best-practices.md\`
- \`.exon/standards/testing-requirements.md\`

### 3. Stack Template (Follow exactly)
- \`.exon/stacks/$STACK_TEMPLATE/CLAUDE.md\` - Development guidance
- \`.exon/stacks/$STACK_TEMPLATE/constitution.md\` - Architecture principles
- \`.exon/stacks/$STACK_TEMPLATE/folder-structure.json\` - Project structure

### 4. Completed Phase Outputs
EOF

# Add completed phase outputs
if jq -e '.completed_phases | contains(["1_research"])' "$STATE_FILE" > /dev/null; then
    cat >> "$RESUME_CONTEXT_FILE" << EOF

**Phase 1 - Research:**
- \`research/domain_analysis.md\`
- \`research/stack_justification.md\`
- \`research/cost_analysis.md\`
- \`research/best_practices.md\`
EOF
fi

if jq -e '.completed_phases | contains(["2_architecture"])' "$STATE_FILE" > /dev/null; then
    cat >> "$RESUME_CONTEXT_FILE" << EOF

**Phase 2 - Architecture:**
- \`architecture/system_design.md\`
- \`specs/api_contracts.json\`
- \`specs/database_schema.md\`
EOF
fi

cat >> "$RESUME_CONTEXT_FILE" << EOF

## Next Steps (EXECUTE AUTOMATICALLY)

1. **Read state.json**: Determine exact checkpoint
2. **Load all context**: Standards, stack template, completed phase outputs
3. **Continue from current_sub_phase**: Pick up exactly where we left off
4. **Update state.json**: Mark progress as you complete sub-phases
5. **Git commit**: After each sub-phase completion
6. **Save checkpoint**: Update state.json regularly

## Claude's Instructions

\`\`\`
RESUME BUILD FOR: $PROJECT_NAME

You are the Exonpro Template Builder automation.
Your session was interrupted. Resume from:
- Phase: $CURRENT_PHASE
- Sub-phase: $CURRENT_SUB_PHASE

DO NOT ask the user what to do.
DO NOT start from scratch.

IMMEDIATELY:
1. Read all context files listed above
2. Review completed work in apps/, infrastructure/, etc.
3. Continue generating remaining files for current sub-phase
4. Follow the phase definitions in .exon/config/builder-config.json
5. Update .exon/phases/state.json as you progress
\`\`\`

---
Generated: $(date -u +"%Y-%m-%dT%H:%M:%SZ")
EOF

echo -e "${GREEN}✓${NC} Resume context created: .claude/resume-context.md"
echo ""
echo -e "${GREEN}╔════════════════════════════════════════╗${NC}"
echo -e "${GREEN}║   Ready to Resume                      ║${NC}"
echo -e "${GREEN}╚════════════════════════════════════════╝${NC}"
echo ""
echo -e "${YELLOW}Next steps:${NC}"
echo ""
echo "1. Start Claude Code in this directory"
echo "2. Claude will automatically read .claude/resume-context.md"
echo "3. Claude will continue the build from the checkpoint"
echo ""
echo "Alternatively, if using the builder CLI:"
echo "   ${BLUE}cd builder && npm run build-app -- --resume${NC}"
echo ""
