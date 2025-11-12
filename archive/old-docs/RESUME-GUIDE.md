# Exonpro Template - Resume Guide

## Overview

The Exonpro Template Builder is designed to be **fully resumable**. If your build session crashes, is interrupted, or you need to stop work, you can resume from the exact checkpoint.

## How Resume Works

### 1. State Tracking

Every phase and sub-phase updates `.exon/phases/state.json`:

```json
{
  "current_phase": "3_implementation",
  "current_sub_phase": "api_endpoints",
  "completed_phases": ["0_configuration", "1_research", "2_architecture"],
  "phase_status": {
    "0_configuration": "completed",
    "1_research": "completed",
    "2_architecture": "completed",
    "3_implementation": "in_progress",
    "4_testing": "pending",
    "5_deployment": "pending"
  },
  "start_time": "2025-11-02T03:00:00Z",
  "last_update": "2025-11-02T05:30:00Z",
  "can_resume": true,
  "last_checkpoint": "phase_3_database_models_complete"
}
```

### 2. Resume Context

When you run `./resume-project.sh`, it:

1. **Reads state.json** to determine where build stopped
2. **Generates `.claude/resume-context.md`** with:
   - Current phase and sub-phase
   - Completed work
   - Files to load
   - Exact next steps
3. **Lists all context** Claude needs to load

### 3. Claude Auto-Resume

When Claude Code starts in the project directory:

1. **Detects** `.claude/resume-context.md` exists
2. **Loads** all context:
   - requirements.md
   - .exon/standards/
   - .exon/stacks/{selected-stack}/
   - Completed phase outputs (research/, architecture/)
   - Current code in apps/, infrastructure/
3. **Continues** from exact checkpoint
4. **Updates** state.json as progress continues

## Usage

### Resume After Crash

```bash
cd /path/to/your-project

# Run resume script
./resume-project.sh

# Output shows:
# 📍 Resuming from:
#   Phase: 3_implementation
#   Sub-phase: api_endpoints
# ✓ Resume context created: .claude/resume-context.md
```

### Start Claude Code

```bash
# Claude automatically reads .claude/resume-context.md
# and continues building from the checkpoint
```

## What Gets Saved

### Checkpoints

After each sub-phase completion:
- **state.json** updated
- **Git commit** created
- **Checkpoint file** saved in `.exon/phases/checkpoints/`

### Example Checkpoint Flow

```
Phase 3: Implementation
├── Sub-phase: database_models ✓ (checkpoint saved)
├── Sub-phase: api_endpoints ✓ (checkpoint saved)
├── Sub-phase: frontend_components ⏸ (CRASHED HERE)
├── Sub-phase: tests (pending)
└── Sub-phase: deployment_config (pending)
```

Resume picks up at `frontend_components`.

## State Management

### state.json Fields

| Field | Purpose | Example |
|-------|---------|---------|
| `current_phase` | Active phase | `"3_implementation"` |
| `current_sub_phase` | Active sub-phase | `"api_endpoints"` |
| `completed_phases` | Finished phases | `["0_configuration", "1_research"]` |
| `phase_status` | Status per phase | `"3_implementation": "in_progress"` |
| `can_resume` | Can resume build | `true` |
| `last_checkpoint` | Last save point | `"phase_3_database_models_complete"` |
| `last_update` | Last activity | `"2025-11-02T05:30:00Z"` |

### Updating State During Build

Claude calls `./update-resume-context.sh` after completing each sub-phase:

```bash
# In Claude's workflow
# After completing sub-phase:
./update-resume-context.sh

# This updates:
# - state.json with new progress
# - .claude/resume-context.md with new checkpoint
```

## Context Loading

### What Claude Loads on Resume

```
1. Configuration
   └── .exon/config/project.json
   └── aws-config.json

2. Requirements
   └── requirements.md

3. Standards (Apply to ALL code)
   └── .exon/standards/code-structure.md
   └── .exon/standards/naming-conventions.md
   └── .exon/standards/security-best-practices.md
   └── .exon/standards/testing-requirements.md

4. Selected Stack Template
   └── .exon/stacks/{stack}/CLAUDE.md
   └── .exon/stacks/{stack}/constitution.md
   └── .exon/stacks/{stack}/folder-structure.json

5. Completed Phase Outputs
   └── research/ (if Phase 1 complete)
   └── architecture/ (if Phase 2 complete)
   └── specs/ (if Phase 2 complete)

6. Generated Code (if Phase 3 started)
   └── apps/
   └── infrastructure/
   └── package.json, etc.

7. Build State
   └── .exon/phases/state.json
```

## Git Integration

### Automatic Commits

After each sub-phase:

```bash
git add .
git commit -m "phase_3: Completed API endpoints generation

🤖 Generated with Exonpro Template Builder

Phase: 3_implementation
Sub-phase: api_endpoints
Stack: aws-serverless-svelte-hybrid-dynamodb-nodejs-python
Checkpoint: phase_3_api_endpoints_complete"
```

### Resume from Git History

You can also check git history to see exactly what was done:

```bash
git log --oneline

# Shows:
# abc1234 phase_3: Completed API endpoints generation
# def5678 phase_3: Completed database models generation
# ghi9012 phase_2: Architecture design complete
# jkl3456 phase_1: Research and stack selection complete
```

## Troubleshooting

### Resume Script Fails

```bash
# Check state
cat .exon/phases/state.json

# If can_resume is false:
# - Build may have completed
# - Build may have encountered error
# - Check .exon/logs/ for details
```

### Claude Doesn't Auto-Resume

1. Ensure `.claude/resume-context.md` exists
2. Run `./resume-project.sh` again
3. Manually tell Claude: "Resume building this project from the checkpoint in .claude/resume-context.md"

### Lost Progress

Check git history:

```bash
git log --all --oneline
git checkout <commit-hash>
```

Checkpoints are also saved:

```bash
ls -la .exon/phases/checkpoints/
```

## Best Practices

1. **Commit often**: State is saved after each sub-phase
2. **Monitor progress**: Check state.json periodically
3. **Keep context**: Don't delete .exon/ directory
4. **Save checkpoints**: Checkpoints are your backup
5. **Git is source of truth**: Can always revert to last commit

## Advanced: Manual Resume

If automation fails, you can manually resume:

```bash
# 1. Check state
cat .exon/phases/state.json

# 2. See what was completed
ls -R apps/ infrastructure/ research/ architecture/

# 3. Tell Claude exactly:
"Resume building business-hub project.
Last phase: 3_implementation
Last sub-phase: api_endpoints
Stack: aws-serverless-svelte-hybrid-dynamodb-nodejs-python

Load context from:
- requirements.md
- .exon/stacks/aws-serverless-svelte-hybrid-dynamodb-nodejs-python/
- research/ and architecture/ directories
- Current code in apps/ and infrastructure/

Continue generating remaining files for Phase 3."
```

## Summary

The Exonpro Template is **crash-resistant**:

- ✅ State tracked in `.exon/phases/state.json`
- ✅ Resume via `./resume-project.sh`
- ✅ Claude auto-loads context from `.claude/resume-context.md`
- ✅ Git commits after each sub-phase
- ✅ Checkpoints saved in `.exon/phases/checkpoints/`
- ✅ Can resume from any point

**You never lose progress!**
