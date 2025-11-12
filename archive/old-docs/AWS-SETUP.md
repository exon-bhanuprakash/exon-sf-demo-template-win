# AWS Multi-Environment Setup Guide

This guide explains how to prepare AWS configuration and use the Exonpro builder to create cost-effective, production-ready applications with dev/stage/prod environments.

## Overview

The Exonpro builder automatically:
1. ✅ Validates your AWS configuration
2. ✅ Selects the optimal tech stack based on requirements and budget
3. ✅ Generates complete application code
4. ✅ Deploys to **dev environment immediately**
5. ✅ Prepares stage/prod deployment scripts (manual deployment)

**Target**: Small to medium scale applications (100-10,000 users, $20-150/month budget)

---

## Prerequisites

### 1. AWS Account Setup

```bash
# Install AWS CLI
# macOS
brew install awscli

# Linux
curl "https://awscli.amazonaws.com/awscli-exe-linux-x86_64.zip" -o "awscliv2.zip"
unzip awscliv2.zip
sudo ./aws/install

# Windows
# Download installer from https://aws.amazon.com/cli/
```

### 2. Configure AWS Credentials

**Option A: Using AWS CLI (Recommended)**
```bash
aws configure

# Enter:
# AWS Access Key ID: [your-access-key]
# AWS Secret Access Key: [your-secret-key]
# Default region name: us-east-1
# Default output format: json
```

**Option B: Using Environment Variables**
```bash
export AWS_ACCESS_KEY_ID="your-access-key"
export AWS_SECRET_ACCESS_KEY="your-secret-key"
export AWS_DEFAULT_REGION="us-east-1"
```

### 3. Verify AWS Access

```bash
# Check credentials work
aws sts get-caller-identity

# Expected output:
# {
#     "UserId": "AIDAI...",
#     "Account": "123456789012",
#     "Arn": "arn:aws:iam::123456789012:user/yourname"
# }

# Get your AWS Account ID (needed for configuration)
aws sts get-caller-identity --query Account --output text
```

---

## Step 1: Initialize New Project

```bash
# From the exon-template directory
./init-project.sh /path/to/new-project "My Application Name"

# Example:
./init-project.sh ../projects/todo-app "TODO Application"

cd ../projects/todo-app
```

**What this does:**
- Copies template to new location
- Initializes git repository on `dev` branch
- Creates sample `requirements.md` and `aws-config.json`
- Resets state for new build

---

## Step 2: Configure AWS Settings

### Edit `aws-config.json`

This file tells the builder about your AWS setup and environment preferences.

```bash
# Copy template and edit
cp aws-config.template.json aws-config.json
nano aws-config.json  # or use your editor
```

### Minimal Required Configuration

```json
{
  "project": {
    "name": "todo-app",
    "description": "Task management application",
    "organization": "my-company",
    "contact_email": "admin@example.com"
  },

  "aws": {
    "account_id": "123456789012",  // ← Get from: aws sts get-caller-identity
    "region": "us-east-1",
    "profile": "default",
    "use_existing_profile": true
  },

  "environments": {
    "dev": {
      "enabled": true,
      "deploy_immediately": true,  // ← Builder will deploy dev automatically
      "domain": "dev.myapp.com",   // Optional: leave null if not using custom domain
      "branch": "dev",
      "budget_alert": {
        "enabled": true,
        "monthly_limit_usd": 20
      }
    },
    "stage": {
      "enabled": true,
      "deploy_immediately": false,  // ← Will create scripts, not deploy yet
      "domain": "stage.myapp.com",
      "branch": "stage"
    },
    "prod": {
      "enabled": true,
      "deploy_immediately": false,  // ← Manual deployment only
      "domain": "myapp.com",
      "branch": "main",
      "require_approval": true
    }
  },

  "cost_optimization": {
    "priority": "high",
    "target_scale": "small-medium",
    "expected_users": {
      "dev": 10,
      "stage": 50,
      "prod": 1000
    },
    "monthly_budget_usd": {
      "dev": 20,
      "stage": 30,
      "prod": 100
    }
  }
}
```

**Key Settings Explained:**

| Setting | Purpose | Recommendation |
|---------|---------|----------------|
| `aws.account_id` | Your AWS account | Get with `aws sts get-caller-identity` |
| `aws.region` | AWS region | `us-east-1` (cheapest, most services) |
| `environments.dev.deploy_immediately` | Auto-deploy dev | ✅ Always `true` - you want dev ready immediately |
| `environments.stage/prod.deploy_immediately` | Auto-deploy stage/prod | ❌ Always `false` - deploy manually after testing |
| `cost_optimization.monthly_budget_usd` | Cost alerts | Set realistic limits, alerts at 80% |

### Full Configuration Options

See `aws-config.template.json` for all available options including:
- Database sizing per environment
- Lambda memory/timeout settings
- Backup retention policies
- Monitoring and logging settings
- Security configurations (WAF, GuardDuty)
- CI/CD pipeline settings

---

## Step 3: Write Business Requirements

### Edit `requirements.md`

```markdown
# TODO Application Requirements

## Overview
A task management application for personal productivity.

## Features
1. User authentication (email/password)
2. Create, read, update, delete tasks
3. Mark tasks as complete/incomplete
4. Due dates and priority levels
5. Filter tasks (all, active, completed)
6. Search tasks by title

## Technical Requirements
- Expected users: 100 initially, scale to 1000
- Budget: $50/month for production
- Mobile-friendly UI
- Simple deployment (no dedicated DevOps team)

## Non-Functional Requirements
- Response time < 2 seconds
- 99% uptime target
- Data backed up daily
- GDPR compliance for EU users
```

**Tips for Good Requirements:**
- ✅ Be specific about expected scale (users, requests)
- ✅ Include budget constraints
- ✅ Mention team expertise if relevant
- ✅ List any special requirements (compliance, integrations)
- ❌ Don't specify technologies (let builder choose optimal stack)

---

## Step 4: Run the Builder

```bash
# Make sure you're in the project directory
cd /path/to/new-project

# Install builder dependencies (first time only)
cd builder && npm install && cd ..

# Run the build process
npm run build -- --requirements requirements.md
```

### What Happens During Build

The builder executes **6 phases**:

#### Phase 0: Configuration Validation (5-10 min)
```
📋 Validating AWS configuration...
✓ AWS credentials valid
✓ Account ID confirmed: 123456789012
✓ Region us-east-1 accessible
✓ Budget constraints realistic
✓ Dev environment configured
```

**What it checks:**
- AWS credentials work
- Account ID matches configuration
- Region is valid
- Budget limits are realistic for requirements
- Required environment settings present

#### Phase 1: Research & Stack Selection (30-60 min)
```
🔍 Analyzing business requirements...
🔍 Researching best practices for task management apps...
🔍 Evaluating AWS stacks against requirements...
✓ Selected: aws-serverless-svelte-fastapi-dynamodb-python

Justification:
- Budget: $50/month fits serverless perfectly ($15-25 actual cost)
- Scale: 1000 users easily handled by Lambda + DynamoDB
- Maintenance: Zero server management, fully managed services
- Cost-effectiveness: Pay-per-use pricing, no baseline costs
```

**Outputs generated:**
- `research/domain_analysis.md` - Deep dive into problem domain
- `research/stack_justification.md` - Why this stack was chosen
- `research/cost_analysis.md` - Detailed cost breakdown per environment
- `research/best_practices.md` - Industry best practices research
- `.exon/config/project.json` - Selected stack metadata

**Research Priorities (Always Applied):**
1. **Cost-effective** - Minimize monthly costs for small/medium scale
2. **Easy maintenance** - Prefer managed services, minimal ops
3. **Easy to enhance** - Modular, well-documented, testable
4. **AWS-native** - All infrastructure on AWS
5. **Serverless-first** - Use Lambda/DynamoDB when possible

#### Phase 2: Architecture Design (45-90 min)
```
🏗️  Designing system architecture...
✓ Created system architecture
✓ Designed API specification
✓ Designed database schema (DynamoDB single table)
✓ Planned AWS infrastructure
```

**Outputs generated:**
- `architecture/system_design.md` - Component architecture, data flow
- `architecture/database_schema.md` - DynamoDB table design
- `architecture/infrastructure.md` - AWS resources needed
- `specs/api_contracts.json` - All API endpoints with schemas
- `specs/database_schema.md` - Detailed access patterns

**Example API Spec:**
```json
{
  "POST /api/v1/tasks": {
    "description": "Create new task",
    "auth": "required",
    "request": {
      "title": "string",
      "priority": "low|medium|high",
      "due_date": "ISO 8601 date"
    },
    "response": {
      "task_id": "uuid",
      "title": "string",
      "completed": false,
      "created_at": "timestamp"
    }
  }
}
```

#### Phase 3: Implementation (2-4 hours)
```
💻 Generating application code...
✓ Generated infrastructure code (AWS CDK)
✓ Generated backend API (FastAPI)
✓ Generated frontend (SvelteKit)
✓ Generated tests (pytest, vitest)
✓ Generated deployment configurations
```

**Complete codebase generated:**
```
apps/
├── web/                    # SvelteKit frontend
│   ├── src/
│   │   ├── routes/        # Pages
│   │   ├── lib/
│   │   │   ├── components/ # UI components
│   │   │   ├── api/       # API client
│   │   │   └── stores/    # State management
│   │   └── app.html
│   ├── package.json
│   └── svelte.config.js
│
├── api/                    # FastAPI backend
│   ├── src/
│   │   ├── handlers/      # Lambda handlers
│   │   ├── api/v1/        # API routes
│   │   ├── services/      # Business logic
│   │   ├── repositories/  # DynamoDB access
│   │   └── models/        # Pydantic models
│   ├── tests/
│   └── requirements.txt
│
infrastructure/             # AWS CDK
├── lib/
│   ├── api-stack.ts      # Lambda + API Gateway + DynamoDB
│   ├── frontend-stack.ts # S3 + CloudFront
│   └── environments/
│       ├── dev.ts        # Dev environment config
│       ├── stage.ts      # Stage environment config
│       └── prod.ts       # Prod environment config
└── package.json
```

**Code Quality:**
- ✅ TypeScript strict mode
- ✅ Comprehensive comments
- ✅ Error handling
- ✅ Input validation
- ✅ Test coverage > 75%
- ✅ Follows all Exonpro standards

#### Phase 4: Testing & Validation (30-60 min)
```
🧪 Running tests...
✓ Backend tests: 42 passed
✓ Frontend tests: 28 passed
✓ Linting: No errors
✓ Type checking: Passed
```

#### Phase 5: Multi-Environment Deployment (45-90 min)
```
🚀 Setting up deployment pipeline...
✓ Created GitHub Actions workflows
✓ Created environment-specific configs
✓ Deploying to DEV environment...
  ✓ Infrastructure deployed (CloudFormation stacks)
  ✓ Backend deployed (Lambda function)
  ✓ Frontend deployed (S3 + CloudFront)
  ✓ Database tables created
✓ DEV environment ready!
✓ Prepared STAGE deployment scripts
✓ Prepared PROD deployment scripts
```

**DEV Environment URLs:**
```
Frontend: https://d1234abcd5678.cloudfront.net
API: https://abc123xyz.execute-api.us-east-1.amazonaws.com/dev
```

**What gets deployed to DEV immediately:**
- ✅ All AWS infrastructure (Lambda, DynamoDB, API Gateway, S3, CloudFront)
- ✅ Backend application code
- ✅ Frontend application code
- ✅ Database tables with indexes
- ✅ Environment variables and secrets
- ✅ CloudWatch logs and monitoring

**What gets prepared (not deployed) for STAGE/PROD:**
- 📄 Deployment scripts in `deployment/scripts/`
- 📄 GitHub Actions workflows in `.github/workflows/`
- 📄 Environment-specific configurations
- 📄 Deployment documentation in `deployment/DEPLOYMENT.md`

---

### Final Output

```
✅ Build completed successfully!

Generated application: TODO Application
Stack: aws-serverless-svelte-fastapi-dynamodb-python
Time: 4 hours 32 minutes

DEV Environment:
  Status: ✅ DEPLOYED AND READY
  Frontend: https://d1234abcd5678.cloudfront.net
  API: https://abc123xyz.execute-api.us-east-1.amazonaws.com/dev
  Costs: ~$5-10/month (mostly free tier)

STAGE Environment:
  Status: ⏸️  READY TO DEPLOY
  Command: cd deployment && ./deploy-stage.sh
  Estimated costs: ~$20-30/month

PROD Environment:
  Status: ⏸️  READY TO DEPLOY (requires approval)
  Command: cd deployment && ./deploy-prod.sh
  Estimated costs: ~$50-80/month (1000 users)

Next steps:
  1. Test dev environment: https://d1234abcd5678.cloudfront.net
  2. Review generated code in apps/
  3. Read deployment/DEPLOYMENT.md
  4. When ready, deploy to stage: ./deployment/deploy-stage.sh
```

---

## Step 5: Testing Dev Environment

```bash
# Frontend should be live
curl https://d1234abcd5678.cloudfront.net

# Test API
curl https://abc123xyz.execute-api.us-east-1.amazonaws.com/dev/health
# Expected: {"status": "healthy"}

# Check CloudWatch logs
aws logs tail /aws/lambda/todo-app-dev-api --follow

# Check DynamoDB table
aws dynamodb list-tables --region us-east-1
```

**Verify Everything Works:**
1. ✅ Open frontend URL in browser
2. ✅ Sign up / log in
3. ✅ Create a task
4. ✅ Update task
5. ✅ Delete task
6. ✅ Check CloudWatch logs for errors

---

## Step 6: Deploy to Stage (Manual)

### When to Deploy Stage
- ✅ Dev environment fully tested
- ✅ All features working
- ✅ No critical bugs
- ✅ Ready for pre-production testing

### Deployment Command

```bash
cd deployment

# Review stage configuration
cat ../infrastructure/environments/stage.ts

# Deploy stage infrastructure + application
./deploy-stage.sh

# This will:
# 1. Create CloudFormation stacks for stage
# 2. Deploy backend to Lambda
# 3. Deploy frontend to S3 + CloudFront
# 4. Run database migrations
# 5. Output stage URLs
```

### Verify Stage Deployment

```bash
# Check CloudFormation stacks
aws cloudformation list-stacks --region us-east-1 | grep todo-app-stage

# Test stage API
curl https://stage-api-url/health

# View logs
aws logs tail /aws/lambda/todo-app-stage-api --follow
```

---

## Step 7: Deploy to Production (Manual + Approval)

### Pre-Production Checklist

- [ ] Stage environment fully tested
- [ ] Load testing completed
- [ ] Security audit passed
- [ ] Backup strategy verified
- [ ] Monitoring and alerts configured
- [ ] Rollback plan documented
- [ ] Budget alerts configured
- [ ] Team approval obtained

### Production Deployment

```bash
cd deployment

# Review prod configuration (IMPORTANT!)
cat ../infrastructure/environments/prod.ts

# Check estimated costs
cat ../research/cost_analysis.md

# Deploy to production
./deploy-prod.sh

# This will:
# 1. Prompt for confirmation (double-check)
# 2. Create prod CloudFormation stacks
# 3. Deploy with deletion protection enabled
# 4. Enable backups and monitoring
# 5. Configure CloudWatch alarms
# 6. Output prod URLs
```

### Post-Production Verification

```bash
# Monitor deployment
aws cloudformation describe-stacks --stack-name todo-app-prod --region us-east-1

# Check all services healthy
curl https://api.myapp.com/health

# Monitor CloudWatch dashboards
# AWS Console → CloudWatch → Dashboards → todo-app-prod

# Verify alarms configured
aws cloudwatch describe-alarms --region us-east-1 | grep todo-app-prod
```

---

## Multi-Environment Workflow

### Git Branch Strategy

```
main (prod)
  ↑
stage
  ↑
dev ← active development
```

**Workflow:**
1. Develop on `dev` branch → auto-deploys to dev environment
2. When ready, merge `dev` → `stage` → manually deploy stage
3. When stage tested, merge `stage` → `main` → manually deploy prod

### CI/CD Pipeline (Auto-Generated)

**`.github/workflows/deploy-dev.yml`** - Auto-deploys on push to `dev`
```yaml
on:
  push:
    branches: [dev]

jobs:
  deploy:
    runs-on: ubuntu-latest
    steps:
      - Run tests
      - Deploy to dev environment
```

**`.github/workflows/deploy-stage.yml`** - Triggered manually or on merge to `stage`
```yaml
on:
  push:
    branches: [stage]
  workflow_dispatch:  # Manual trigger

jobs:
  deploy:
    # ... deploy to stage
```

**`.github/workflows/deploy-prod.yml`** - Requires approval
```yaml
on:
  push:
    branches: [main]

jobs:
  deploy:
    environment:
      name: production
      url: https://myapp.com
    steps:
      # ... deploy to prod (requires GitHub approval)
```

---

## Cost Monitoring

### Set Up Budget Alerts (Auto-Configured)

The builder automatically creates AWS Budget alerts per environment:

```bash
# View budgets
aws budgets describe-budgets --account-id YOUR_ACCOUNT_ID

# Expected budgets:
# - todo-app-dev-budget: $20/month, alert at 80% ($16)
# - todo-app-stage-budget: $30/month, alert at 80% ($24)
# - todo-app-prod-budget: $100/month, alert at 80% ($80)
```

### Monthly Cost Tracking

**Typical costs for TODO app (1000 users, 10k requests/day):**

| Service | Dev | Stage | Prod | Notes |
|---------|-----|-------|------|-------|
| Lambda | $2 | $5 | $15 | Free tier: 1M requests |
| DynamoDB | $1 | $3 | $10 | On-demand billing |
| API Gateway | $1 | $3 | $8 | $3.50 per million requests |
| CloudFront | Free | $2 | $5 | 1TB transfer free |
| S3 | Free | $1 | $3 | Storage + requests |
| CloudWatch | Free | $2 | $5 | Logs + metrics |
| **Total** | **~$10** | **~$25** | **~$60** | |

**AWS Free Tier Benefits (First 12 months):**
- Lambda: 1M requests/month free
- DynamoDB: 25 GB storage free
- CloudFront: 50 GB transfer free
- S3: 5 GB storage free

### View Actual Costs

```bash
# Current month costs
aws ce get-cost-and-usage \
  --time-period Start=2025-11-01,End=2025-11-30 \
  --granularity MONTHLY \
  --metrics BlendedCost \
  --group-by Type=TAG,Key=Environment

# Costs by service
aws ce get-cost-and-usage \
  --time-period Start=2025-11-01,End=2025-11-30 \
  --granularity MONTHLY \
  --metrics BlendedCost \
  --group-by Type=SERVICE
```

---

## Troubleshooting

### Build Phase Fails

```bash
# Check state file
cat .exon/phases/state.json

# Resume from last checkpoint
npm run build -- --resume

# View detailed logs
cat .exon/logs/builder_*.log
```

### AWS Credentials Invalid

```bash
# Verify credentials
aws sts get-caller-identity

# Reconfigure
aws configure

# Check IAM permissions (need Admin or PowerUser)
aws iam get-user
```

### Deployment Fails

```bash
# Check CloudFormation events
aws cloudformation describe-stack-events --stack-name todo-app-dev

# View error logs
aws logs tail /aws/lambda/todo-app-dev-api --follow

# Check CDK diff
cd infrastructure
cdk diff --context environment=dev
```

### Lambda Cold Starts Too Slow

**Options:**
1. Increase Lambda memory (faster CPU)
2. Enable provisioned concurrency ($$$)
3. Switch to Lightsail stack (always warm)

```typescript
// infrastructure/lib/api-stack.ts
const apiFunction = new lambda.Function(this, 'ApiFunction', {
  memorySize: 1024,  // Increase from 512
  // OR enable provisioned concurrency:
  reservedConcurrentExecutions: 2,  // Always 2 warm instances
});
```

### Cost Higher Than Expected

```bash
# Identify expensive services
aws ce get-cost-and-usage \
  --time-period Start=2025-11-01,End=2025-11-30 \
  --granularity DAILY \
  --metrics BlendedCost \
  --group-by Type=SERVICE

# Common issues:
# - CloudWatch logs retention too long
# - DynamoDB provisioned instead of on-demand
# - Large S3 storage or requests
# - API Gateway throttling not set
```

---

## Advanced Configuration

### Custom Domains

**Update `aws-config.json`:**
```json
{
  "domains": {
    "use_custom_domains": true,
    "zone_id": "Z1234567890ABC",  // Route53 hosted zone
    "create_route53_zone": false,
    "certificate_arn": "arn:aws:acm:us-east-1:123456789012:certificate/abcd-1234"
  },
  "environments": {
    "dev": {
      "domain": "dev.myapp.com"
    },
    "prod": {
      "domain": "myapp.com"
    }
  }
}
```

**Builder will:**
1. Use existing Route53 zone and ACM certificate
2. Create CloudFront distributions with custom domains
3. Configure DNS records automatically

### Enable WAF (Production Security)

```json
{
  "security": {
    "enable_waf": {
      "dev": false,
      "stage": false,
      "prod": true  // ← Enable for prod
    }
  }
}
```

**Adds:**
- Rate limiting (100 requests/5min per IP)
- SQL injection protection
- XSS protection
- Geographic blocking (optional)

**Cost:** ~$5-10/month

### Multi-Region Deployment

```json
{
  "aws": {
    "regions": {
      "primary": "us-east-1",
      "secondary": "eu-west-1"
    }
  }
}
```

**Builder will:**
- Deploy to both regions
- Set up Route53 latency-based routing
- Configure DynamoDB global tables

**Cost:** ~2x single region

---

## Best Practices

### ✅ DO

- ✅ Start with dev environment, test thoroughly
- ✅ Use budget alerts (avoid surprises)
- ✅ Enable backups for prod
- ✅ Review CloudWatch logs regularly
- ✅ Use secrets manager for sensitive data
- ✅ Enable deletion protection for prod
- ✅ Test stage before deploying prod
- ✅ Document any manual changes

### ❌ DON'T

- ❌ Manually modify AWS resources (use CDK)
- ❌ Skip testing dev/stage before prod
- ❌ Ignore budget alerts
- ❌ Disable backups to save costs
- ❌ Use provisioned DynamoDB for unpredictable traffic
- ❌ Store secrets in code or environment files
- ❌ Deploy directly to prod without stage testing

---

## Next Steps

After successful deployment:

1. **Monitor Costs**: Check AWS Billing Dashboard daily first week
2. **Set Up Monitoring**: Configure CloudWatch dashboards and alarms
3. **Load Testing**: Use tools like Artillery or k6 to test scale
4. **Security Audit**: Review IAM policies, enable GuardDuty
5. **Documentation**: Document any custom configurations
6. **Backup Testing**: Verify backup/restore procedures work
7. **Team Training**: Share access, document deployment process

---

## Support

### Documentation
- **Exonpro Standards**: `.exon/standards/`
- **Stack Documentation**: `.exon/stacks/{stack-name}/CLAUDE.md`
- **Deployment Guide**: `deployment/DEPLOYMENT.md`

### AWS Resources
- [AWS Cost Calculator](https://calculator.aws/)
- [AWS Well-Architected Framework](https://aws.amazon.com/architecture/well-architected/)
- [AWS Free Tier](https://aws.amazon.com/free/)

### Estimated Response Times
- Dev environment: 5-10 minutes
- Full build: 4-6 hours
- Stage/Prod deployment: 10-15 minutes each
