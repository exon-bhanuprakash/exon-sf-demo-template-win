# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with the Exonpro Template Repository.

## Overview

This is the **Exonpro Universal App Template** - a comprehensive framework for generating production-ready applications using Claude Agent SDK. The template supports multiple AWS-focused tech stacks and automates the entire development process from requirements to deployment.

## Repository Purpose

**This is a template repository**, not an application. Exonpro employees use this template to:
1. Copy it for each new client project
2. Run the builder with client requirements
3. Generate a complete, production-ready application
4. Deliver to client with full documentation

## Directory Structure

```
exon-template/
├── .exon/                              # Template configuration & standards
│   ├── standards/                      # Exonpro universal standards
│   │   ├── tech-stack-selection.md
│   │   ├── hosting-deployment.md
│   │   ├── code-structure.md
│   │   ├── naming-conventions.md
│   │   ├── testing-requirements.md
│   │   └── security-best-practices.md
│   │
│   ├── stacks/                         # Pre-established tech stack templates
│   │   ├── aws-serverless-svelte-fastapi-dynamodb-python/
│   │   │   ├── CLAUDE.md              # Stack-specific guidance
│   │   │   ├── constitution.md        # Architecture patterns
│   │   │   ├── .claude/settings.json
│   │   │   └── folder-structure.json
│   │   ├── aws-serverless-svelte-dynamodb-nodejs/
│   │   └── aws-lightsail-svelte-fastapi-postgres/
│   │
│   ├── config/                         # Builder configuration
│   │   ├── project.json               # Populated during build
│   │   ├── builder-config.json        # Builder behavior
│   │   └── exceptions.json            # When to ask for help
│   │
│   └── phases/                         # Build phase tracking
│       └── state.json                 # Current build state
│
├── research/                           # Phase 1 outputs (generated)
│   ├── domain_analysis.md
│   ├── stack_justification.md
│   ├── competitive_analysis.md
│   └── best_practices.md
│
├── architecture/                       # Phase 2 outputs (generated)
│   ├── system_design.md
│   ├── database_schema.md
│   └── infrastructure.md
│
├── specs/                              # Project specifications (generated)
│   ├── requirements.json
│   ├── features.csv
│   ├── user_stories.md
│   ├── api_contracts.json
│   ├── database_schema.md
│   └── phases/
│       ├── phase_1_core.json
│       ├── phase_2_extended.json
│       └── phase_3_advanced.json
│
├── builder/                            # TypeScript Claude SDK builder (TODO)
│   └── src/
│
├── CLAUDE.md                           # This file
├── .claude/settings.json               # Claude Code settings
├── README.md                           # Template usage guide
└── START_HERE.md                       # Quick start guide
```

## Working with This Template

### For Exonpro Employees

**Starting a New Project:**
1. Initialize from template:
   ```bash
   # From the template directory
   ./init-project.sh client-project-name /path/to/projects

   # Or Windows
   .\init-project.ps1 -ProjectName "client-project-name" -TargetDir "C:\Projects"
   ```

2. Navigate to new project and edit requirements.md:
   ```bash
   cd /path/to/projects/client-project-name
   # Edit requirements.md with client's business needs
   ```

3. Run the builder:
   ```bash
   # TODO: Once builder is implemented
   npm run build -- --requirements=path/to/requirements.md
   ```

4. The builder will:
   - Analyze requirements
   - Select optimal tech stack from `.exon/stacks/`
   - Generate complete application code
   - Set up deployment configuration
   - Create documentation

5. Review generated code, test, and deliver to client

### Stack Selection Logic

The builder automatically selects the best stack based on:

**AWS Serverless (Python + DynamoDB)**:
- Use when: AI/ML integration, data-heavy, Python team expertise
- Stack: Svelte + FastAPI on Lambda + DynamoDB
- Cost: Variable, pay-per-use
- Scaling: Automatic, unlimited

**AWS Serverless (Node.js + DynamoDB)**:
- Use when: Real-time features, JavaScript full-stack, microservices
- Stack: Svelte + Express on Lambda + DynamoDB
- Cost: Variable, pay-per-use
- Scaling: Automatic, unlimited

**AWS Lightsail (Python + PostgreSQL)**:
- Use when: Predictable traffic, need PostgreSQL, fixed budget preferred
- Stack: Svelte + FastAPI + PostgreSQL on Lightsail VPS
- Cost: Fixed ~$25/month
- Scaling: Vertical only

### Custom Stack Creation

If client requirements don't fit pre-established stacks:
1. Create new directory in `.exon/stacks/`
2. Name it: `{hosting}-{frontend}-{backend}-{database}-{language}`
3. Include:
   - `CLAUDE.md` - Development guidance
   - `constitution.md` - Architecture patterns
   - `.claude/settings.json` - Claude Code config
   - `folder-structure.json` - Project structure
4. Test with sample requirements
5. Add to `builder-config.json` available_stacks

## Configuration Files

### `.exon/config/project.json`
Populated during build with project metadata:
- Project name, description
- Selected tech stack
- Business domain info
- Target scale

### `.exon/config/builder-config.json`
Controls builder behavior:
- Available stacks
- Build phases
- Git workflow settings
- Error handling rules
- Exception scenarios

### `.exon/config/exceptions.json`
Defines when builder should ask for user input:
- API errors after retries
- Working > 4 hours
- Unclear requirements
- Multiple valid stack options
- Critical security decisions
- Deployment credentials needed

## Exonpro Standards

All generated code must follow standards in `.exon/standards/`:

1. **Tech Stack Selection** - How to choose hosting, frameworks, databases
2. **Hosting & Deployment** - Platform setup, CI/CD, monitoring
3. **Code Structure** - Project organization, file naming, folder patterns
4. **Naming Conventions** - Variables, functions, files, commits
5. **Testing Requirements** - Coverage targets, testing strategies
6. **Security Best Practices** - Authentication, authorization, data protection

**Important**: These standards are applied to generated projects. When client context requires deviations, the builder may modify standards during Phase 1 (Research).

## Build Phases

The builder executes in phases (see `builder-config.json`):

### Phase 1: Deep Research & Stack Selection
- Analyze business domain
- Research competitive solutions
- Evaluate technical requirements
- Select optimal tech stack
- Output: `research/` directory with analysis documents
- Update: `.exon/config/project.json`

### Phase 2: Architecture Design
- Design system architecture
- Create database schema
- Define API contracts
- Plan component structure
- Output: `architecture/` and `specs/` directories

### Phase 3: Implementation
- Generate infrastructure code
- Create database models
- Build API endpoints
- Implement frontend components
- Write tests
- Configure deployment

### Phase 4: Testing & Validation
- Run all tests
- Validate code quality
- Check security compliance
- Verify deployment readiness

### Phase 5: Deployment Setup
- Configure CI/CD pipelines
- Prepare deployment scripts
- Document deployment process

## Git Workflow

The builder automatically:
- Initializes git repository (if not exists)
- Commits to `dev` branch after each sub-phase
- Uses descriptive commit messages
- Includes 🤖 attribution in commits

**Commit message format:**
```
{phase}: {description}

🤖 Generated with Exonpro Template Builder

Phase: {phase_name}
Stack: {stack_template}
```

## Error Handling & Resumability

The builder is resilient to interruptions:
- **State tracking**: `.exon/phases/state.json` tracks progress
- **Checkpoints**: Saved after each phase
- **Auto-retry**: API errors retry 5 times with backoff
- **Resume**: Can resume from last checkpoint

To resume after interruption:
```bash
# Check state
cat .exon/phases/state.json

# Resume
npm run build -- --resume
```

## Important Notes for Claude Code

When working in this repository:

1. **Don't modify `.exon/` manually** - These files are template configuration
2. **Generated directories** - `research/`, `architecture/`, `specs/` are created during build
3. **Update standards carefully** - Changes affect all future projects
4. **Test new stacks thoroughly** - Use sample requirements before production
5. **Follow naming conventions** - Stack names must match format: `{hosting}-{frontend}-{backend}-{database}-{language}`
6. **Document stack decisions** - Update `tech-stack-selection.md` with new patterns

## Builder Development (TODO)

The TypeScript Claude SDK builder will be implemented in `builder/`:
- Uses `@anthropic-ai/claude-agent-sdk`
- Reads configuration from `.exon/config/`
- Applies standards from `.exon/standards/`
- Uses stack templates from `.exon/stacks/`
- Tracks state in `.exon/phases/`
- Handles exceptions per `.exon/config/exceptions.json`

## Common Tasks

### Adding a New Exonpro Standard
1. Create new file in `.exon/standards/`
2. Document the standard comprehensively
3. Update this CLAUDE.md to reference it
4. Test with sample project generation

### Adding a New Tech Stack
1. Create directory in `.exon/stacks/` with proper naming
2. Add CLAUDE.md, constitution.md, .claude/settings.json, folder-structure.json
3. Add to `builder-config.json` available_stacks
4. Test generation with sample requirements

### Updating Existing Stack
1. Modify files in `.exon/stacks/{stack-name}/`
2. Test with existing requirements to ensure compatibility
3. Update version in stack's constitution.md

### Testing the Builder
1. Create sample requirements.md
2. Run builder with `--dry-run` flag (when implemented)
3. Review generated code structure
4. Verify all files match stack template
5. Check that exonpro standards are followed

## Support & Documentation

- **Standards**: See `.exon/standards/` for comprehensive guides
- **Stack Templates**: See `.exon/stacks/` for implementation patterns
- **Builder Config**: See `.exon/config/` for configuration options
- **Issues**: Report template issues to exonpro internal repo

## Version Control

This template uses semantic versioning:
- **Major**: Breaking changes to structure or standards
- **Minor**: New stacks or features
- **Patch**: Bug fixes, documentation updates

Current version: 1.0.0
