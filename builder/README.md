# Exonpro Builder

Automated application builder using Claude Agent SDK.

## Overview

This builder automates the complete application generation process using AI. It spawns Claude Code sessions with full tool access (Read, Write, Edit, Bash, etc.) to build production-ready applications autonomously.

The builder:
- Reads business requirements
- Selects the optimal tech stack based on cost/scale/requirements
- Generates complete, production-ready code following exonpro standards
- Creates infrastructure, backend, frontend, tests, and documentation
- Deploys to AWS dev environment

**Key Features:**
- **Autonomous Execution**: Uses `bypassPermissions` mode to run without prompts
- **Full Tool Access**: Claude can read files, write code, run commands
- **Context-Driven**: Loads all context from files, not in-memory conversation
- **Resumable**: Can resume from any checkpoint if interrupted
- **Multi-Phase**: Executes in structured phases (research, architecture, implementation, testing, deployment)

## Installation

```bash
cd builder
npm install
```

## Environment Variables

Create `.env` file in builder directory (or copy from `.env.example`):

```bash
ANTHROPIC_API_KEY=sk-ant-api03-...
VERBOSE=false
DRY_RUN=false
```

## Usage

### Build New Application

```bash
npm run build-app -- --requirements ../requirements.md
```

This will:
1. Validate configuration (aws-config.json, requirements.md)
2. Spawn a Claude Code session with full tool access
3. Execute all build phases autonomously
4. Generate complete application code
5. Deploy to AWS dev environment (if configured)

### Resume from Checkpoint

```bash
npm run build-app -- --resume
```

This will:
1. Load state from `.exon/phases/state.json`
2. Spawn a Claude session with context from completed phases
3. Continue from the last checkpoint

### Dry Run (No File Creation)

```bash
npm run build-app -- --requirements ../requirements.md --dry-run
```

Simulates the build process without actually creating files.

## How It Works

The builder uses the Claude Agent SDK's `query()` function to spawn Claude Code sessions with:
- **Full tool access**: Read, Write, Edit, Bash, Glob, Grep, WebSearch, WebFetch
- **Bypass permissions mode**: No manual prompts - fully automated
- **Context from files**: All standards, templates, and requirements loaded from disk

### Phase 0: Configuration Validation (5-10 min)
- Validates `aws-config.json` exists and is complete
- Validates `requirements.md` is filled in
- Checks AWS credentials
- Saves validated config to `.exon/config/`

### Phase 1: Research & Stack Selection (30-60 min)
- Analyzes business requirements deeply
- Researches domain best practices
- Evaluates all available stacks against requirements AND budget
- Calculates cost estimates for each stack
- Selects optimal stack (prioritizing cost-effectiveness)
- **Outputs** (using Write tool):
  - `research/domain_analysis.md`
  - `research/stack_justification.md`
  - `research/cost_analysis.md`
  - `research/best_practices.md`

### Phase 2: Architecture Design (45-90 min)
- Designs complete system architecture
- Creates detailed API specification
- Designs database schema (DynamoDB single-table design)
- Plans AWS infrastructure
- **Outputs** (using Write tool):
  - `architecture/system-architecture.md`
  - `architecture/api-specification.md`
  - `architecture/database-schema.md`
  - `architecture/infrastructure-plan.md`
  - `specs/api-contracts.json`
  - `specs/database-schema.json`

### Phase 3: Code Generation (2-4 hours)
- Generates COMPLETE, production-ready code
- Creates infrastructure code (AWS CDK)
- Builds backend services (Node.js + Python Lambda)
- Develops frontend (SvelteKit)
- Writes comprehensive tests
- Adds documentation
- **Outputs** (using Write tool):
  - `infrastructure/` - Complete CDK code
  - `shared/` - Types and utilities
  - `backend/nodejs/` - Node.js Lambda functions
  - `backend/python/` - Python Lambda functions (if hybrid)
  - `apps/web/` - Complete SvelteKit app
  - `tests/` - Unit and integration tests
  - Root config files, README, DEPLOYMENT.md

### Phase 4: Testing & Validation (30-60 min)
- Runs all tests using Bash tool
- Validates TypeScript compilation
- Checks code quality
- Verifies security compliance

### Phase 5: Deployment to AWS (45-90 min)
- Configures AWS credentials
- Bootstraps CDK (if needed)
- Deploys infrastructure stacks
- Runs deployment validation
- Creates deployment documentation

## Context Loading

The builder passes comprehensive context to each Claude session:

**System Prompt** (loaded from):
- All exonpro standards from `.exon/standards/`
- Selected stack template from `.exon/stacks/{stack}/`
- Builder configuration from `.exon/config/builder-config.json`

**User Prompt** (includes instructions to):
- Read requirements.md
- Read aws-config.json
- Read previous phase outputs (research/, architecture/, specs/)
- Use Write/Edit tools to create all necessary files
- Follow the folder structure from the stack template

## State Management

Progress is tracked in `.exon/phases/state.json`. If interrupted:
- State is saved automatically
- Resume with `--resume` flag
- Checkpoints saved after each phase

## Error Handling

Configured in `.exon/config/exceptions.json`:
- API errors: Retry 5 times with backoff
- Unclear requirements: Ask user for clarification
- Multiple valid stacks: Present options
- Critical decisions: Request approval

## Development

```bash
# Development mode with hot reload
npm run dev -- --requirements ../requirements.md

# Build TypeScript
npm run build

# Run compiled version
npm start -- --requirements ../requirements.md
```

## Architecture

```
builder/
├── src/
│   ├── index.ts              # CLI entry point
│   ├── core/
│   │   └── builder.ts        # Main builder logic
│   ├── phases/               # Phase implementations (TODO)
│   │   ├── phase1.ts
│   │   ├── phase2.ts
│   │   └── phase3.ts
│   ├── stacks/               # Stack-specific generators (TODO)
│   └── utils/
│       ├── context-loader.ts # Load framework context
│       └── state-manager.ts  # Track build state
├── package.json
└── tsconfig.json
```

## TODO

- [ ] Implement complete Phase 1-5 logic
- [ ] Add stack-specific code generators
- [ ] Implement file parser for Claude responses
- [ ] Add progress indicators and logging
- [ ] Error recovery and retry logic
- [ ] Testing suite
- [ ] Documentation generator
