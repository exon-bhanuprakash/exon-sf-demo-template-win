# Quick Start - Automated Build (Recommended)

Get from zero to deployed AWS application in 4-6 hours, fully automated.

## Prerequisites

- AWS Account with credentials configured
- Node.js 18+ installed
- Anthropic API key

## Step 1: Initialize Project (2 minutes)

```bash
cd /Users/kusaldipdas/Documents/00_All_Work/exon-template

./init-project.sh my-app /Users/kusaldipdas/Documents/00_All_Work/ExonProProjects
```

**Answer the prompts:**

1. **Select stack template:**
   ```
   1. aws-serverless-svelte-hybrid-dynamodb-nodejs-python (RECOMMENDED)
   ```
   Press `1` and Enter

2. **AWS Account ID:**
   ```
   Enter your AWS Account ID: 535563617782
   ```

3. **AWS Region:**
   ```
   Enter AWS region (default: us-east-1): ap-south-1
   ```

4. **AWS Profile:**
   ```
   Enter AWS CLI profile name (default: default): [press Enter]
   ```

5. **Contact Email:**
   ```
   Enter contact email: your-email@example.com
   ```

6. **Start automated build?**
   ```
   Start automated build now? [y/N]: N
   ```
   Press `N` for now (we'll do it manually next)

**Result:** Project initialized at `/Users/kusaldipdas/Documents/00_All_Work/ExonProProjects/my-app`

---

## Step 2: Navigate to Project

```bash
cd /Users/kusaldipdas/Documents/00_All_Work/ExonProProjects/my-app
```

---

## Step 3: Edit Requirements (5-10 minutes)

**CRITICAL**: Fill in your business requirements:

```bash
nano requirements.md
# or
code requirements.md
```

**Replace the placeholders with your actual requirements:**

```markdown
# Project Name: My App

## Business Problem
[Describe the problem your app solves]

## Solution
[Describe your solution]

## Target Users
- **User Type 1**: [Description]
- **User Type 2**: [Description]

## Key Features

### Phase 1 (MVP - Deploy First)
1. **Feature 1**: [Description]
2. **Feature 2**: [Description]
3. **Feature 3**: [Description]
4. **Feature 4**: [Description]
5. **Feature 5**: [Description]

### Phase 2 (Post-MVP)
[Future features...]

## Scale Requirements
- Expected users: 100-1,000 users in first year
- Traffic pattern: Variable during business hours
- Budget: $50-150/month for AWS infrastructure
- Growth potential: [High/Medium/Low]

## Technical Requirements
- Authentication: AWS Cognito with JWT (email/password)
- File uploads: [Yes/No] (max size)
- Real-time features: [Yes/No]
- AI/ML: [Yes/No] - describe
- Third-party integrations: [List integrations]
```

**Save the file!**

---

## Step 4: Configure Builder API Key

```bash
cd builder

# Copy example env file
cp .env.example .env

# Edit .env
nano .env
```

**Add your Anthropic API key:**

```bash
ANTHROPIC_API_KEY=sk-ant-api03-your-key-here
VERBOSE=false
DRY_RUN=false
```

Save and exit.

---

## Step 5: Start Automated Build (4-6 hours)

```bash
cd /Users/kusaldipdas/Documents/00_All_Work/ExonProProjects/my-app

./start-build.sh
```

**What happens:**

```
╔════════════════════════════════════════╗
║   Exonpro Automated Build              ║
╚════════════════════════════════════════╝

✓ Requirements configured
✓ Claude Agent SDK ready

Starting automated build...
This will spawn a NEW Claude session to build your application.

Phases to execute:
  0. Configuration validation (5-10 min)
  1. Research & stack selection (30-60 min)
  2. Architecture design (45-90 min)
  3. Code generation (2-4 hours)
  4. Testing & validation (30-60 min)
  5. Deployment to AWS dev (45-90 min)

Total estimated time: 4-6 hours

Press Enter to start, or Ctrl+C to cancel...
```

Press **Enter** to start!

---

## What Gets Built Automatically

The builder will:

### Phase 0: Configuration (5-10 min)
- ✅ Validate AWS credentials
- ✅ Check requirements.md is filled
- ✅ Validate aws-config.json

### Phase 1: Research (30-60 min)
- ✅ Analyze your business domain
- ✅ Research best practices
- ✅ Evaluate tech stacks vs budget
- ✅ Select optimal stack (considering cost!)
- ✅ Create research documents

**Files created:**
```
research/
├── domain_analysis.md
├── stack_justification.md
├── cost_analysis.md
└── best_practices.md
```

### Phase 2: Architecture (45-90 min)
- ✅ Design system architecture
- ✅ Create API specification
- ✅ Design database schema
- ✅ Plan AWS infrastructure

**Files created:**
```
architecture/
├── system-architecture.md
├── api-specification.md
├── database-schema.md
└── infrastructure-plan.md

specs/
├── api-contracts.json
└── database-schema.json
```

### Phase 3: Code Generation (2-4 hours)
- ✅ Generate complete infrastructure code (AWS CDK)
- ✅ Generate shared types
- ✅ Generate Node.js Lambda functions
- ✅ Generate Python Lambda functions (if hybrid)
- ✅ Generate SvelteKit frontend
- ✅ Generate tests
- ✅ Generate documentation

**Files created:**
```
infrastructure/          # Complete AWS CDK code
shared/                  # Shared TypeScript types
backend/nodejs/          # Node.js Lambdas
backend/python/          # Python Lambdas (if hybrid)
apps/web/                # Complete SvelteKit app
tests/                   # All tests
README.md                # Complete documentation
DEPLOYMENT.md            # Deployment guide
```

### Phase 4: Testing (30-60 min)
- ✅ Run TypeScript compilation
- ✅ Run all unit tests
- ✅ Validate code quality
- ✅ Check security compliance

### Phase 5: Deployment (45-90 min)
- ✅ Bootstrap CDK (if needed)
- ✅ Deploy DynamoDB table
- ✅ Deploy Cognito user pool
- ✅ Deploy Lambda functions
- ✅ Deploy API Gateway
- ✅ Configure CORS
- ✅ Output API URLs

---

## Step 6: Check Build Output

After 4-6 hours, check the results:

```bash
cd /Users/kusaldipdas/Documents/00_All_Work/ExonProProjects/my-app

# See what was created
tree -L 2 -I 'node_modules|dist|.cdk.out'

# Read the generated README
cat README.md

# Check deployment output
cat infrastructure/deployment-output.txt
```

---

## Step 7: Access Your Deployed App

### API Endpoints

The builder outputs your API URL. Test it:

```bash
# Get API URL from CDK output (shown at end of build)
export API_URL="https://abc123.execute-api.ap-south-1.amazonaws.com"

# Test health endpoint
curl $API_URL/health

# Test your endpoints (see API spec in architecture/api-specification.md)
curl $API_URL/api/v1/your-endpoint
```

### Frontend

```bash
cd apps/web

# Run locally
npm run dev

# Visit http://localhost:5173
```

---

## Step 8: Next Steps

### Review Generated Code

```bash
# Read architecture docs
cat architecture/system-architecture.md
cat architecture/database-schema.md

# Review API contracts
cat specs/api-contracts.json

# Understand the code
ls -la infrastructure/lib/
ls -la backend/nodejs/src/
ls -la apps/web/src/routes/
```

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

---

## Monitoring Build Progress

The builder runs autonomously, but you can check progress:

```bash
# Check state
cat .exon/phases/state.json

# See current phase
jq -r '.current_phase' .exon/phases/state.json

# See completed phases
jq -r '.completed_phases[]' .exon/phases/state.json
```

---

## If Build Gets Interrupted

The builder automatically saves checkpoints. To resume:

```bash
cd /Users/kusaldipdas/Documents/00_All_Work/ExonProProjects/my-app

./resume-project.sh
```

This will:
- Load the last checkpoint
- Spawn a new Claude session
- Continue from where it left off

---

## Cost Estimate

### Development Environment
- DynamoDB (on-demand): ~$5-10/month
- Lambda (pay-per-use): ~$5-15/month
- API Gateway: ~$3-5/month
- Cognito: Free tier (up to 50k users)
- **Total**: ~$15-30/month

### Production Environment
- DynamoDB (on-demand): ~$20-40/month
- Lambda (reserved): ~$20-50/month
- API Gateway: ~$10-20/month
- CloudFront (if frontend deployed): ~$10-20/month
- **Total**: ~$60-130/month

Actual costs depend on usage. Builder optimizes for cost-effectiveness!

---

## Troubleshooting

### Build fails with "requirements.md not filled"
```bash
# Make sure you replaced all placeholders in requirements.md
grep -i "what problem" requirements.md
# Should return nothing if properly filled
```

### Build fails with "ANTHROPIC_API_KEY not found"
```bash
# Check .env file exists
cat builder/.env

# Should show: ANTHROPIC_API_KEY=sk-ant-...
```

### Build fails with AWS credentials error
```bash
# Check AWS credentials
aws sts get-caller-identity

# Should show your account ID
```

### Want to see verbose output
```bash
# Edit builder/.env
VERBOSE=true

# Re-run
./start-build.sh
```

---

## Complete Example Session

```bash
# 1. Initialize
cd /Users/kusaldipdas/Documents/00_All_Work/exon-template
./init-project.sh my-saas-app /Users/kusaldipdas/Documents/00_All_Work/ExonProProjects

# 2. Configure
cd /Users/kusaldipdas/Documents/00_All_Work/ExonProProjects/my-saas-app
nano requirements.md  # Fill in your business details
cd builder && cp .env.example .env && nano .env  # Add API key
cd ..

# 3. Build
./start-build.sh  # Press Enter when prompted

# 4. Wait 4-6 hours... ☕️

# 5. Test
export API_URL=$(jq -r '.dev.apiUrl' infrastructure/deployment-output.json)
curl $API_URL/health

# 6. Run frontend
cd apps/web && npm run dev

# 7. Success! 🎉
```

---

## What Makes This "Automated"?

Unlike manual building where you tell Claude what to do step-by-step:

- ✅ **Zero manual intervention** - Builder runs for 4-6 hours autonomously
- ✅ **Full tool access** - Claude can read files, write code, run commands
- ✅ **Context from files** - Loads all standards, templates automatically
- ✅ **Bypass permissions** - No prompts, fully automated
- ✅ **Multi-phase execution** - Structured workflow from research to deployment
- ✅ **Auto-resume** - Can recover from interruptions
- ✅ **Production-ready output** - Complete, tested, deployed application

You just:
1. Fill requirements.md
2. Run ./start-build.sh
3. Come back to a deployed app!

---

## Support

If build fails or you need help:
- Check `.exon/logs/` for error logs
- Check `.exon/phases/state.json` for current state
- Read the generated `DEPLOYMENT.md` for deployment issues
- Ask Claude Code in a manual session to debug specific errors

---

**Ready to build your next application in one command? Let's go! 🚀**
