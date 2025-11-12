# .exon/ - Automation Framework Directory

This directory contains the 100% automated implementation framework for building production-ready applications from business requirements.

## Directory Structure

```
.exon/
├── automation/
│   ├── config.json         # Automation configuration
│   ├── state.json          # Current progress state
│   └── checkpoints/        # Resume points
├── research/               # Phase 1: Deep Research outputs
│   ├── domain_analysis.md
│   ├── best_practices.md
│   └── competitive_analysis.md
├── specs/                  # Phase 2-3: Requirements & MVP outputs
│   ├── requirements.json
│   ├── features.csv
│   ├── user_stories.md
│   ├── mvp_roadmap.md
│   └── phases/
│       ├── phase_1_core.json
│       ├── phase_2_extended.json
│       └── phase_3_advanced.json
├── implementation/         # Phase 4+: Implementation tracking
│   ├── completed.json
│   └── current_phase.json
├── logs/                   # All automation logs
│   ├── automation_*.log
│   ├── conversation_*.log
│   └── summary_*.log
└── constitution.md         # Architecture principles (updated during research)
```

## Automation Phases

### Phase 1: Deep Research
- Analyze the business domain
- Research best practices for the industry
- Identify competitive solutions
- Recommend technology stack
- Update constitution.md with chosen stack

### Phase 2: Requirements & Feature Breakdown
- Extract features from app_details document
- Create detailed requirements
- Write user stories
- Generate features.csv for prioritization

### Phase 3: MVP Phasing
- Break features into implementation phases
- Define Phase 1 (Core MVP)
- Define Phase 2 (Extended features)
- Define Phase 3 (Advanced features)
- Create roadmap

### Phase 4+: Implementation
For each phase:
1. **Models**: Database models
2. **Schemas**: Request/Response schemas
3. **Routers**: API endpoints
4. **Frontend**: UI components
5. **Tests**: Unit + Integration tests

Each sub-phase gets its own git branch and is auto-committed.

## State Management

The automation tracks progress in `automation/state.json`:
```json
{
  "current_phase": "1_deep_research",
  "current_sub_phase": null,
  "completed_phases": [],
  "last_checkpoint": "2025-01-15T10:30:00Z",
  "can_resume": true
}
```

## Checkpoints

Checkpoints are saved after each major milestone:
- `checkpoint_phase1_complete.json`
- `checkpoint_phase2_complete.json`
- etc.

Use checkpoints to resume if interrupted.

## Configuration

Edit `automation/config.json` before starting:
- Set `project_name`
- Set `project_type`
- Point `app_details` to your requirements document
- Adjust `working_directory`

## Error Handling

The automation retries API calls 5 times with 10-second intervals. If all retries fail, it:
1. Saves current state to checkpoint
2. Logs the error
3. Waits for manual resume

Resume with: `python .exon/automation_script.py --mode=resume`

## Logs

Three types of logs:
1. **automation_*.log**: Detailed technical logs
2. **conversation_*.log**: Full Claude conversation
3. **summary_*.log**: High-level progress summary

## Clean Root Directory

All automation artifacts stay in `.exon/`. The root directory only contains actual project code.

Add `.exon/` to `.gitignore` if you don't want to version automation artifacts.
