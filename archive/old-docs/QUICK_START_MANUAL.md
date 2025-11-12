# Quick Start Guide - Manual Build (Optional Approach)

This guide shows you how to use the Exonpro Template **manually** in your current Claude Code session, instead of using the automated builder.

## When to Use Manual vs Automated

### Use Automated Builder (Recommended)
- You want a complete app generated automatically
- You're okay with 4-6 hours of automated build time
- You want to follow best practices without thinking
- **Command**: `./start-build.sh`

### Use Manual Approach (This Guide)
- You want full control over each step
- You want to learn the architecture as you build
- You're experimenting or prototyping
- You want to customize heavily from the start
- **Method**: Tell Claude Code what to build step-by-step

---

## Step 1: Initialize New Project

```bash
cd /Users/kusaldipdas/Documents/00_All_Work/exon-template

./init-project.sh my-project /Users/kusaldipdas/Documents/00_All_Work/ExonProProjects
```

**When prompted:**
1. **Select stack**: Choose option 1-4 (hybrid is recommended for most projects)
2. **AWS Account ID**: Enter your AWS account ID
3. **AWS Region**: Choose your preferred region (e.g., ap-south-1)
4. **AWS Profile**: Enter your AWS CLI profile name (default: default)
5. **Email**: Your contact email
6. **Start automated build?**: Press **N** (No) for manual approach

**Result**: Fresh project initialized at `/Users/kusaldipdas/Documents/00_All_Work/ExonProProjects/my-project`

---

## Step 2: Navigate to Your Project

```bash
cd /Users/kusaldipdas/Documents/00_All_Work/ExonProProjects/my-project
```

---

## Step 3: Fill Requirements

**CRITICAL**: Edit `requirements.md` with your actual business requirements:

```bash
# Edit with your preferred editor
nano requirements.md
# or
code requirements.md
```

Fill in:
- **Business Problem**: What problem does this solve?
- **Solution**: Your application's value proposition
- **Target Users**: Who will use this?
- **Key Features**: What features do you need? (Phase 1 MVP)
- **Scale Requirements**: Expected users, traffic, budget
- **Technical Requirements**: Auth, file uploads, real-time, AI/ML, integrations

See the template inside the file for guidance.

---

## Step 4: Review Your Selected Stack

Check what stack was selected:

```bash
cat .exon/config/project.json
```

View the stack template details:

```bash
# See architecture principles
cat .exon/stacks/aws-serverless-svelte-hybrid-dynamodb-nodejs-python/constitution.md

# See folder structure
cat .exon/stacks/aws-serverless-svelte-hybrid-dynamodb-nodejs-python/folder-structure.json

# See development guidance
cat .exon/stacks/aws-serverless-svelte-hybrid-dynamodb-nodejs-python/CLAUDE.md
```

---

## Step 5: Tell Claude Code What to Build

Now, in this Claude Code session, give me clear instructions. You can use this template:

### Option A: Build Everything in One Go

```
Build the complete application following these steps:

1. Analyze requirements.md and aws-config.json
2. Create the folder structure from the selected stack template
3. Generate shared types and utilities
4. Create DynamoDB repositories (Node.js and Python)
5. Generate Node.js Lambda functions for CRUD operations
6. Generate Python Lambda functions for analytics/AI features (if hybrid stack)
7. Create AWS CDK infrastructure code
8. Generate SvelteKit frontend with all pages and components
9. Create all package.json files and configuration
10. Create tests
11. Create documentation (README, DEPLOYMENT.md)

Work systematically through each step. Show me progress as you go.
```

### Option B: Build Step-by-Step (More Control)

Start with Phase 1:

```
I want to build this manually with your help. Let's start with Phase 1:

1. First, analyze my requirements.md and tell me:
   - What entities/models we need
   - What API endpoints we need
   - What database schema to use
   - What pages/components for frontend

Then wait for my approval before generating code.
```

Then proceed incrementally:

```
Great! Now create the folder structure.
```

```
Now generate shared types based on the entities we discussed.
```

```
Now create the DynamoDB repositories for [entity name].
```

And so on...

---

## Step 6: What Gets Built

Here's what will be created (for hybrid stack):

```
my-project/
├── apps/
│   ├── api-node/              # Node.js Lambda functions
│   │   ├── src/
│   │   │   ├── functions/     # Lambda handlers (users, leads, products, etc.)
│   │   │   ├── repositories/  # DynamoDB access layer
│   │   │   ├── services/      # Business logic
│   │   │   └── utils/         # Helpers, middleware
│   │   ├── tests/
│   │   ├── package.json
│   │   └── tsconfig.json
│   │
│   ├── api-python/            # Python Lambda functions
│   │   ├── src/
│   │   │   ├── functions/     # Lambda handlers (analytics, ML)
│   │   │   ├── repositories/  # DynamoDB access
│   │   │   └── utils/
│   │   ├── tests/
│   │   └── requirements.txt
│   │
│   ├── web/                   # SvelteKit frontend
│   │   ├── src/
│   │   │   ├── routes/        # Pages (+page.svelte files)
│   │   │   └── lib/
│   │   │       ├── components/
│   │   │       ├── stores/
│   │   │       ├── api/       # API client
│   │   │       └── types/
│   │   ├── static/
│   │   ├── tests/
│   │   ├── package.json
│   │   ├── svelte.config.js
│   │   └── vite.config.ts
│   │
│   └── shared/                # Shared types and utilities
│       ├── types/
│       │   ├── entities.ts
│       │   └── api.ts
│       └── utils/
│
├── infrastructure/            # AWS CDK
│   ├── lib/
│   │   ├── database-stack.ts       # DynamoDB table
│   │   ├── auth-stack.ts           # Cognito
│   │   ├── api-node-stack.ts       # Node.js Lambdas
│   │   ├── api-python-stack.ts     # Python Lambdas
│   │   ├── api-gateway-stack.ts    # API Gateway
│   │   └── frontend-stack.ts       # S3 + CloudFront (optional)
│   ├── bin/
│   │   └── app.ts
│   ├── package.json
│   ├── cdk.json
│   └── tsconfig.json
│
├── .exon/                     # Framework configuration
│   ├── config/
│   │   ├── project.json
│   │   └── aws-config.json
│   ├── stacks/                # Stack templates
│   └── standards/             # Coding standards
│
├── requirements.md            # Your business requirements
├── aws-config.json           # AWS configuration
├── package.json              # Root workspace
├── .gitignore
└── README.md
```

---

## Step 7: Install Dependencies

After code is generated:

```bash
# Install all dependencies (uses npm workspaces)
npm install
```

This will install dependencies for:
- Root workspace
- infrastructure/
- apps/api-node/
- apps/api-python/ (pip packages)
- apps/web/

---

## Step 8: Deploy to AWS

### Deploy Infrastructure

```bash
cd infrastructure

# First time only: Bootstrap CDK in your AWS account
npx cdk bootstrap aws://<ACCOUNT-ID>/<REGION>

# Deploy all stacks to dev environment
npx cdk deploy --all --context env=dev

# Or deploy specific stack
npx cdk deploy DatabaseStack --context env=dev
```

**Expected Output:**
- DynamoDB table ARN
- API Gateway URL
- Cognito User Pool ID
- Lambda function ARNs

### Deploy Frontend (Optional)

If frontend stack is included:

```bash
cd apps/web
npm run build

# Frontend will be deployed via CDK to S3 + CloudFront
cd ../../infrastructure
npx cdk deploy FrontendStack --context env=dev
```

Or run locally:

```bash
cd apps/web
npm run dev
# Visit http://localhost:5173
```

---

## Step 9: Test Your Application

### Test API Endpoints

```bash
# Get API URL from CDK output
export API_URL="https://abc123.execute-api.ap-south-1.amazonaws.com"

# Test health check
curl $API_URL/health

# Create a user (if you have user management)
curl -X POST $API_URL/api/v1/users \
  -H "Content-Type: application/json" \
  -d '{
    "email": "test@example.com",
    "name": "Test User",
    "role": "USER"
  }'

# Get all users
curl $API_URL/api/v1/users
```

### Test Frontend

```bash
# Run locally
cd apps/web
npm run dev

# Open browser to http://localhost:5173
# Test user flows, forms, dashboards
```

---

## Important Architecture Principles

Read these files to understand the architecture:

### 1. Constitution (Architecture Rules)
```bash
cat .exon/stacks/aws-serverless-svelte-hybrid-dynamodb-nodejs-python/constitution.md
```

**Key principles:**
- **Single-table DynamoDB design** (MANDATORY)
- Repository pattern for data access
- Service layer for business logic
- Comprehensive error handling
- Type safety with TypeScript

### 2. Exonpro Standards
```bash
ls .exon/standards/

# Read each:
cat .exon/standards/code-structure.md
cat .exon/standards/naming-conventions.md
cat .exon/standards/security-best-practices.md
cat .exon/standards/testing-requirements.md
```

---

## Common Manual Build Commands

### Ask Claude Code for Help

- **"Create DynamoDB repository for [entity]"**
- **"Generate Lambda function to create a [entity]"**
- **"Create API endpoint for [operation]"**
- **"Build Svelte component for [feature]"**
- **"Add authentication to [endpoint]"**
- **"Create tests for [module]"**

### Development Workflow

```bash
# Check structure
tree -L 3 -I 'node_modules|dist|.cdk.out'

# Install dependencies
npm install

# Build TypeScript
npm run build

# Run tests
npm test

# Deploy
cd infrastructure
npx cdk deploy --all --context env=dev

# Run frontend locally
cd apps/web
npm run dev
```

### Git Workflow

```bash
git status
git add .
git commit -m "feat: Add user management module"
git push origin dev
```

---

## Deployment to Other Environments

### Deploy to Staging

```bash
cd infrastructure
npx cdk deploy --all --context env=stage
```

### Deploy to Production

```bash
cd infrastructure
npx cdk deploy --all --context env=prod
```

**Note**: Production deployments may require approval if configured in `aws-config.json`.

---

## Troubleshooting

### CDK Errors

```bash
# Check CDK version
npx cdk --version

# Synthesize to check for errors
npx cdk synth

# Check diff before deploy
npx cdk diff --context env=dev
```

### Lambda Errors

```bash
# View logs in CloudWatch
aws logs tail /aws/lambda/<function-name> --follow

# Or use CDK output
aws logs tail <log-group-from-cdk-output> --follow
```

### DynamoDB Issues

```bash
# Check table exists
aws dynamodb describe-table --table-name <table-name>

# Scan table (dev only!)
aws dynamodb scan --table-name <table-name>
```

---

## Next Steps

1. **Test all features** in dev environment
2. **Add Phase 2 features** (if needed)
3. **Set up CI/CD pipeline** (GitHub Actions)
4. **Deploy to staging** for QA testing
5. **Deploy to production** when ready

---

## Comparison: Manual vs Automated

| Aspect | Manual (This Guide) | Automated (`./start-build.sh`) |
|--------|---------------------|-------------------------------|
| **Control** | Full control over every decision | Follows best practices automatically |
| **Time** | Depends on your pace | 4-6 hours unattended |
| **Learning** | Learn architecture as you build | Review generated code after |
| **Customization** | Customize from the start | Customize after generation |
| **Best for** | Prototyping, learning, heavy customization | Production apps, standard patterns |

---

## Need Help?

In this Claude Code session, ask me:
- "Explain the single-table DynamoDB design"
- "Show me how to add a new entity"
- "Help me create authentication flow"
- "Debug this deployment error: [paste error]"
- "Add feature: [describe feature]"

---

**Remember**: This is YOUR build process. You control the pace and decisions!
