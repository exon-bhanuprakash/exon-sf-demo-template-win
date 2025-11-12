# Exonpro Universal App Template

**Automated application generation with Claude Agent SDK**

Generate production-ready applications from business requirements using AI-powered automation. This template supports multiple AWS-focused tech stacks and follows exonpro's established development standards.

## Overview

The Exonpro Template is a comprehensive framework that:
- ✅ Analyzes business requirements
- ✅ Selects optimal tech stack automatically
- ✅ Generates complete application code
- ✅ Follows security and testing best practices
- ✅ Sets up CI/CD and deployment
- ✅ Creates comprehensive documentation

## Supported Tech Stacks

### 1. AWS Serverless + Svelte + FastAPI + DynamoDB + Python
**Best for:** AI/ML integrated apps, data-intensive applications, Python teams

- **Frontend**: SvelteKit (static deployment)
- **Backend**: FastAPI on AWS Lambda
- **Database**: DynamoDB (serverless NoSQL)
- **Hosting**: AWS Lambda + API Gateway + S3 + CloudFront
- **Cost**: Pay-per-use (variable)
- **Scaling**: Automatic, unlimited

### 2. AWS Serverless + Svelte + DynamoDB + Node.js
**Best for:** Real-time applications, JavaScript full-stack, microservices

- **Frontend**: SvelteKit
- **Backend**: Express.js on AWS Lambda
- **Database**: DynamoDB
- **Hosting**: AWS Lambda + API Gateway + S3 + CloudFront
- **Cost**: Pay-per-use (variable)
- **Scaling**: Automatic, unlimited

### 3. AWS Lightsail + Svelte + FastAPI + PostgreSQL
**Best for:** Predictable traffic, need relational database, fixed budget

- **Frontend**: SvelteKit (Nginx static)
- **Backend**: FastAPI on Lightsail VPS
- **Database**: PostgreSQL (managed)
- **Hosting**: AWS Lightsail (Docker containers)
- **Cost**: Fixed ~$25/month
- **Scaling**: Vertical (upgrade instance)

## Quick Start

### For Exonpro Employees

**1. Initialize new project from template:**

**macOS/Linux:**
```bash
./init-project.sh my-client-project ~/projects
```

**Windows (PowerShell):**
```powershell
.\init-project.ps1 -ProjectName "my-client-project" -TargetDir "C:\Projects"
```

**Or default to current directory:**
```bash
./init-project.sh my-client-project
```

The script will:
- Copy template to specified location
- Clean up template-specific files
- Initialize git repository on `dev` branch
- Create sample `requirements.md`
- Set up project structure

**2. Create requirements document** (`requirements.md`):
```markdown
# Project: My SaaS App

## Business Problem
What problem does this solve?

## Solution
How does the app solve it?

## Target Users
- User type 1: Description
- User type 2: Description

## Key Features
- Feature 1
- Feature 2
- Feature 3

## Scale Requirements
- Expected users: 1,000-10,000
- Traffic pattern: Predictable/Variable
- Budget: $50/month

## Technical Requirements
- Authentication: Yes
- File uploads: Yes
- Real-time features: No
- AI/ML: No
```

**3. Run builder** (once implemented):
```bash
npm run build -- --requirements=requirements.md
```

**4. Review and deliver:**
- Test generated application
- Review code quality
- Verify deployment configuration
- Hand off to client

## What Gets Generated

A complete, production-ready application with:

```
generated-project/
├── research/             # Phase 1: Research outputs
├── architecture/         # Phase 2: Architecture design
├── specs/                # Project specifications
├── apps/
│   ├── web/              # SvelteKit frontend
│   └── api/              # Backend (FastAPI or Node.js)
├── infrastructure/       # AWS CDK or deployment scripts
├── tests/                # Unit, integration, E2E tests
├── .github/workflows/    # CI/CD pipelines
├── docker-compose.yml    # Local development
├── README.md             # Project documentation
└── CLAUDE.md             # Development guidance for client
```

### Included Features:
- ✅ User authentication (JWT or AWS Cognito)
- ✅ Database models and migrations
- ✅ API endpoints with full CRUD
- ✅ Frontend components and routing
- ✅ Form validation
- ✅ Error handling
- ✅ Logging and monitoring
- ✅ Tests (75%+ coverage)
- ✅ CI/CD pipeline
- ✅ Deployment configuration
- ✅ Documentation

## Architecture

### Exonpro Standards
All generated code follows comprehensive standards:
- **Tech Stack Selection**: Framework, database, hosting choices
- **Code Structure**: Project organization, naming conventions
- **Security**: Authentication, authorization, data protection
- **Testing**: Unit, integration, E2E strategies
- **Deployment**: CI/CD, monitoring, backups

See `.exon/standards/` for details.

### Build Phases

#### Phase 1: Research & Analysis (30-60 min)
- Analyze business domain
- Research competitive solutions
- Evaluate requirements
- Select optimal tech stack
- Document decision rationale

#### Phase 2: Architecture Design (45-90 min)
- Design system architecture
- Create database schema
- Define API contracts
- Plan component structure

#### Phase 3: Implementation (2-4 hours)
- Infrastructure setup
- Database models
- API endpoints
- Frontend components
- Tests
- Deployment configuration

#### Phase 4: Testing & Validation (30-60 min)
- Run all tests
- Code quality checks
- Security validation
- Deployment readiness

#### Phase 5: Deployment Setup (30-45 min)
- CI/CD pipeline configuration
- Deployment scripts
- Documentation

**Total Time:** ~4-7 hours for complete application

## Configuration

### Builder Configuration
`.exon/config/builder-config.json` controls:
- Available tech stacks
- Build phase behavior
- Git workflow
- Error handling
- When to ask for user input

### Exception Handling
The builder asks for input when:
- Requirements are unclear or incomplete
- Multiple tech stacks are equally suitable
- Critical security decisions needed
- Working more than 4 hours (checkpoint)
- API errors after max retries
- Deployment credentials required

## Customization

### Adding a New Tech Stack

1. Create stack directory:
```bash
mkdir -p .exon/stacks/new-stack-name/{.claude,scripts}
```

2. Name format: `{hosting}-{frontend}-{backend}-{database}-{language}`

Example: `vercel-react-nestjs-mongodb-typescript`

3. Create required files:
- `CLAUDE.md` - Development guidance
- `constitution.md` - Architecture patterns
- `.claude/settings.json` - Claude Code config
- `folder-structure.json` - Project structure

4. Add to `builder-config.json`:
```json
{
  "available_stacks": [
    "new-stack-name"
  ]
}
```

5. Test with sample requirements

### Modifying Standards

Edit files in `.exon/standards/`:
- `tech-stack-selection.md`
- `hosting-deployment.md`
- `code-structure.md`
- `naming-conventions.md`
- `testing-requirements.md`
- `security-best-practices.md`

**Warning:** Changes affect all future generated projects.

## Project Structure

```
exon-template/
├── .exon/
│   ├── standards/          # Universal exonpro standards
│   ├── stacks/             # Tech stack templates
│   ├── config/             # Builder configuration
│   └── phases/             # Build state tracking
├── research/               # Generated: Phase 1 research
├── architecture/           # Generated: Phase 2 architecture
├── specs/                  # Generated: Project specifications
├── builder/                # Claude SDK builder (TODO)
├── CLAUDE.md               # Claude Code guidance
├── .claude/                # Claude Code settings
├── README.md               # This file
└── START_HERE.md           # Quick start guide
```

## Technology Choices

### Why AWS?
- **Reliability**: 99.99% uptime SLA
- **Scalability**: From startup to enterprise
- **Cost-effective**: Pay only for what you use (serverless) or fixed pricing (Lightsail)
- **Comprehensive**: All services in one platform

### Why Svelte?
- **Performance**: Fastest frontend framework
- **Simplicity**: Easier to learn than React/Vue
- **Bundle size**: Smaller than alternatives
- **Developer experience**: Excellent tooling

### Why FastAPI (Python)?
- **Speed**: One of the fastest Python frameworks
- **Modern**: Async/await, type hints
- **Auto-docs**: OpenAPI/Swagger built-in
- **Developer experience**: Great IDE support

### Why DynamoDB?
- **Serverless**: No server management
- **Scalability**: Unlimited automatic scaling
- **Performance**: Single-digit millisecond latency
- **Cost**: Pay per request

### Why PostgreSQL (for Lightsail)?
- **Relational**: Complex queries, joins
- **ACID**: Strong consistency guarantees
- **Mature**: Battle-tested, reliable
- **Feature-rich**: JSON, full-text search, etc.

## Cost Estimates

### AWS Serverless (Python or Node.js)
- Lambda: $0.20 per 1M requests + compute
- DynamoDB: $0.25 per 1M read requests (on-demand)
- API Gateway: $1.00 per 1M requests (HTTP API)
- S3 + CloudFront: ~$1-5/month

**Estimated:** $0-10/month (low traffic) to $50-200/month (medium traffic)

### AWS Lightsail
- Instance (2 GB): $10/month
- Managed PostgreSQL (1 GB): $15/month
- Data transfer: Included (2 TB)

**Estimated:** ~$25/month (fixed, predictable)

## Development Workflow

### Local Development
1. Clone generated project
2. Install dependencies
3. Run database (Docker or cloud)
4. Start backend dev server
5. Start frontend dev server
6. Open browser at localhost

### Deployment
1. Push to `dev` branch
2. GitHub Actions runs automatically
3. Tests execute
4. Deploy to AWS
5. Smoke tests run
6. Notify team

### Monitoring
- CloudWatch logs and metrics
- Error tracking (Sentry)
- Uptime monitoring
- Performance metrics

## Security

All generated applications include:
- ✅ Password hashing (bcrypt)
- ✅ JWT authentication
- ✅ Input validation
- ✅ SQL injection prevention
- ✅ XSS protection
- ✅ CORS configuration
- ✅ Rate limiting
- ✅ HTTPS enforcement
- ✅ Environment variable management

## Testing

Every generated project includes:
- **Unit tests**: Business logic, utilities
- **Integration tests**: API endpoints, database
- **E2E tests**: Critical user flows
- **Coverage target**: 75%+ minimum

## Support

- **Documentation**: See `CLAUDE.md` for detailed guidance
- **Standards**: See `.exon/standards/` for coding standards
- **Stack Templates**: See `.exon/stacks/` for implementation patterns
- **Issues**: Report to exonpro internal repository

## License

Proprietary - Exonpro Internal Use Only

## Version

1.0.0

---

**Built with ❤️ by Exonpro**
