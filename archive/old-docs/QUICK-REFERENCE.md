# Exonpro Template - Quick Reference Guide

**Version**: 1.0
**Last Updated**: November 2025

This guide provides quick access to common commands and workflows for the Exonpro Universal App Template.

---

## Table of Contents

1. [Getting Started](#getting-started)
2. [Local Development](#local-development)
3. [Building Your Application](#building-your-application)
4. [Deployment](#deployment)
5. [Monitoring & URLs](#monitoring--urls)
6. [Common Workflows](#common-workflows)
7. [Troubleshooting](#troubleshooting)

---

## Getting Started

### Initialize a New Project

```bash
# Basic initialization
./init-project.sh my-project-name

# Initialize in specific directory
./init-project.sh my-project-name /path/to/parent/directory

# Example
./init-project.sh todo-app ~/projects
```

**What happens:**
- Creates project directory
- Copies template files
- Sets up `.exon/` configuration structure
- Creates initial `requirements.md`

### First Steps After Initialization

1. **Navigate to your project:**
   ```bash
   cd my-project-name
   ```

2. **Update requirements.md** with your application requirements

3. **Configure AWS settings** (if deploying to AWS):
   ```bash
   # Edit AWS configuration
   nano .exon/config/aws-config.json
   ```

---

## Local Development

### ⚠️ IMPORTANT: When to Use Dev Scripts

**Dev scripts require the `apps/` directory to exist.**

The dev scripts (`npm run dev`, `npm run dev:frontend`, etc.) are designed to run **AFTER** the builder has generated your application code.

**Correct Order:**
```bash
# 1. First, install builder dependencies
cd builder && npm install && cd ..

# 2. Run builder to generate application code
npm run build -- --requirements requirements.md

# 3. THEN use dev scripts
npm run dev
```

**If you see "No apps directory found":**
- This means the builder hasn't generated your application yet
- Run the builder first (step 2 above)
- The builder creates `apps/web/` (frontend) and `apps/api/` (backend)
- Then dev scripts will work

---

### Quick Start - Interactive Menu

```bash
npm run dev
```

**Provides menu to:**
- Start frontend only
- Start backend only
- Start both (full stack)
- View deployment URLs
- Check deployment status

### Start Frontend Only

```bash
npm run dev:frontend
```

**Details:**
- Starts SvelteKit development server
- Available at: `http://localhost:5173`
- Auto-installs dependencies if needed
- Hot-reload enabled

### Start Backend Only

```bash
npm run dev:backend
```

**Details:**
- Auto-detects Python (FastAPI) or Node.js (Express)
- **Python**: Available at `http://localhost:8000`
  - API docs: `http://localhost:8000/docs`
  - Creates virtual environment automatically
  - Installs from `requirements.txt`
- **Node.js**: Available at `http://localhost:3000`
  - Installs from `package.json`

### Start Full Stack (Frontend + Backend)

```bash
npm run dev:full
```

**Details:**
- Runs both frontend and backend simultaneously
- Requires `concurrently` package (auto-suggested if missing)
- Color-coded output (cyan for frontend, yellow for backend)
- Kills both when one fails (--kill-others)

**Install concurrently:**
```bash
npm install --save-dev concurrently
```

---

## Building Your Application

### Phase 0: Configuration Setup

```bash
npm run build -- --requirements requirements.md
```

**What it does:**
- Validates AWS credentials
- Analyzes your requirements
- Generates stack-specific configuration
- Creates deployment scripts
- Sets up multi-environment structure (dev/stage/prod)

**Expected output:**
```
✅ Phase 0 completed successfully
📁 Configuration files created in .exon/config/
📁 Stack templates created in .exon/stacks/
```

### Phase 1-5: Full Application Build

```bash
npm run build -- --requirements requirements.md --full
```

**Phases:**
- **Phase 1**: AI-powered research and planning
- **Phase 2**: Architecture design
- **Phase 3**: Code generation and implementation
- **Phase 4**: Testing and validation
- **Phase 5**: Deployment preparation

**Check progress:**
```bash
cat .exon/phases/state.json
```

---

## Deployment

### Development Environment (Auto-Deploy)

```bash
# After Phase 0
cd deployment
./deploy-dev.sh
```

**Details:**
- Deploys to AWS automatically
- Uses CloudFormation/CDK (serverless) or Lightsail
- Captures deployment URLs automatically
- Updates `.exon/deployment/urls.json`

### Stage Environment (Manual)

```bash
cd deployment
./deploy-stage.sh
```

**Details:**
- Manual deployment for testing
- Approval required before execution
- Higher resource allocation than dev

### Production Environment (Manual with Approval)

```bash
cd deployment
./deploy-prod.sh
```

**Details:**
- Production-ready deployment
- Multiple approval checkpoints
- Rollback capability
- Enhanced monitoring

---

## Monitoring & URLs

### View All Deployment URLs

```bash
npm run urls
```

**Shows:**
- Local development URLs (if running)
- DEV environment URLs
- STAGE environment URLs
- PROD environment URLs
- API documentation links
- Health check endpoints

**Example output:**
```
🌐 Deployment URLs:

📍 Local Development:
   Frontend:  http://localhost:5173
   Backend:   http://localhost:8000
   API Docs:  http://localhost:8000/docs

📍 DEV Environment:
   Frontend:  https://d1a2b3c4.cloudfront.net
   API:       https://api123.execute-api.ap-south-1.amazonaws.com/dev
   Status:    https://api123.execute-api.ap-south-1.amazonaws.com/dev/health
   Deployed:  2025-11-01 10:30:45
```

### Check Deployment Status

```bash
npm run status
```

**Performs:**
- Health checks on all deployed environments
- Validates frontend accessibility
- Tests API endpoints (including /health)
- Shows AWS account information
- Displays cost estimates
- Reports HTTP status codes

**Example output:**
```
🔍 Checking DEV environment...
   Frontend: https://d1a2b3c4.cloudfront.net
   ✅ Online (200)
   Backend:  https://api123.execute-api.ap-south-1.amazonaws.com/dev
   ✅ Online (200)
```

---

## Common Workflows

### Workflow 1: Start New Project from Scratch

```bash
# 1. Initialize project
./init-project.sh my-app ~/projects
cd my-app

# 2. Edit requirements
nano requirements.md

# 3. Configure AWS (if needed)
nano .exon/config/aws-config.json

# 4. Run Phase 0 configuration
npm run build -- --requirements requirements.md

# 5. Start local development
npm run dev
# Choose "3. Start both (Full Stack)"

# 6. Test locally at http://localhost:5173

# 7. Deploy to AWS
cd deployment
./deploy-dev.sh

# 8. Check deployment status
npm run status

# 9. View deployment URLs
npm run urls
```

### Workflow 2: Local Development Only

```bash
# 1. Start interactive menu
npm run dev

# 2. Choose option 3 (Full Stack)
# OR run directly:
npm run dev:full

# 3. Open browser to http://localhost:5173

# 4. Make changes (auto-reload enabled)

# 5. Test API at http://localhost:8000/docs (Python)
#    or http://localhost:3000 (Node.js)
```

### Workflow 3: Deploy Updates to Production

```bash
# 1. Test locally first
npm run dev:full
# Verify everything works

# 2. Run full build
npm run build -- --requirements requirements.md --full

# 3. Deploy to stage first
cd deployment
./deploy-stage.sh

# 4. Verify stage deployment
npm run status

# 5. Test stage environment thoroughly
# Visit stage URLs from `npm run urls`

# 6. Deploy to production
./deploy-prod.sh
# Follow approval prompts

# 7. Verify production
npm run status
npm run urls
```

### Workflow 4: Switch Between Stack Templates

```bash
# 1. Check current stack
cat .exon/config/project.json | grep stack_template

# 2. To change stack, edit requirements.md
nano requirements.md

# Update to specify different stack:
# - "use AWS Lambda and DynamoDB" → Python Serverless
# - "use AWS Lambda with Node.js" → Node.js Serverless
# - "use AWS Lightsail" → Lightsail

# 3. Re-run Phase 0
npm run build -- --requirements requirements.md

# 4. Review changes
cat .exon/config/project.json

# 5. Rebuild apps (if needed)
npm run build -- --requirements requirements.md --full
```

---

## Troubleshooting

### Frontend Won't Start

**Problem**: `npm run dev:frontend` fails

**Solutions:**
```bash
# 1. Check if apps/web exists
ls apps/web

# 2. If missing, run builder first
npm run build -- --requirements requirements.md --full

# 3. If exists, clean and reinstall
cd apps/web
rm -rf node_modules package-lock.json
npm install
npm run dev
```

### Backend Won't Start

**Problem**: `npm run dev:backend` fails

**Solutions for Python:**
```bash
# 1. Check Python version (need 3.8+)
python3 --version

# 2. Recreate virtual environment
cd apps/api
rm -rf venv
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt

# 3. Start manually
uvicorn src.main:app --reload
```

**Solutions for Node.js:**
```bash
# 1. Check Node version (need 16+)
node --version

# 2. Clean install
cd apps/api
rm -rf node_modules package-lock.json
npm install
npm run dev
```

### Deployment URLs Not Showing

**Problem**: `npm run urls` shows "No deployments found"

**Solutions:**
```bash
# 1. Check if deployment file exists
cat .exon/deployment/urls.json

# 2. If missing, deploy first
cd deployment
./deploy-dev.sh

# 3. Manually check CloudFormation outputs
aws cloudformation describe-stacks --stack-name <your-stack-name>
```

### AWS Credentials Invalid

**Problem**: Deployment fails with authentication errors

**Solutions:**
```bash
# 1. Verify AWS CLI is configured
aws sts get-caller-identity

# 2. Check credentials
cat ~/.aws/credentials

# 3. Update aws-config.json
nano .exon/config/aws-config.json

# 4. Use environment variables instead
export AWS_ACCESS_KEY_ID=your_key
export AWS_SECRET_ACCESS_KEY=your_secret
export AWS_DEFAULT_REGION=us-east-1
```

### Port Already in Use

**Problem**: "Port 5173 already in use" or "Port 8000 already in use"

**Solutions:**
```bash
# Find process using port
lsof -i :5173  # or :8000, :3000

# Kill the process
kill -9 <PID>

# Or change port in vite.config.ts (frontend)
# Or in uvicorn/express config (backend)
```

### "No apps directory found" Error

**Problem**: `npm run dev` shows "This appears to be a template, not a generated project"

**Root Cause**: Dev scripts need the `apps/` directory which is created by the builder.

**Solution:**
```bash
# 1. Install builder dependencies first
cd builder
npm install
cd ..

# 2. Run the builder to generate application code
npm run build -- --requirements requirements.md

# This creates:
# - apps/web/ (frontend)
# - apps/api/ (backend)

# 3. Now dev scripts will work
npm run dev
```

**Understanding the Workflow:**
- **Template** = Starting point (no apps yet)
- **Builder** = Generates your application code
- **Dev Scripts** = Run the generated application locally

---

## Quick Command Reference

| Command | Description |
|---------|-------------|
| `./init-project.sh <name> [dir]` | Initialize new project |
| `npm run dev` | Interactive development menu |
| `npm run dev:frontend` | Start frontend only |
| `npm run dev:backend` | Start backend only |
| `npm run dev:full` | Start both frontend and backend |
| `npm run build -- --requirements requirements.md` | Run Phase 0 configuration |
| `npm run build -- --requirements requirements.md --full` | Run all phases |
| `npm run urls` | Show all deployment URLs |
| `npm run status` | Check deployment health |
| `cd deployment && ./deploy-dev.sh` | Deploy to development |
| `cd deployment && ./deploy-stage.sh` | Deploy to staging |
| `cd deployment && ./deploy-prod.sh` | Deploy to production |

---

## File Locations

| File | Purpose |
|------|---------|
| `requirements.md` | Application requirements and specifications |
| `.exon/config/project.json` | Project metadata and stack template |
| `.exon/config/aws-config.json` | AWS credentials and configuration |
| `.exon/deployment/urls.json` | Deployment URLs (auto-generated) |
| `.exon/deployment/DEPLOYMENT-URLS.md` | Human-readable URL documentation |
| `.exon/phases/state.json` | Build phase progress tracking |
| `apps/web/` | SvelteKit frontend application |
| `apps/api/` | Backend API (FastAPI or Express) |
| `deployment/` | Deployment scripts for all environments |

---

## Support

### Documentation Files
- `README.md` - Project overview
- `AWS-SETUP.md` - AWS configuration guide
- `QUICK-REFERENCE.md` - This document
- `WHATS-NEW.md` - Latest improvements and changes

### Getting Help
1. Check this Quick Reference first
2. Review the main README.md
3. Check AWS-SETUP.md for deployment issues
4. Review `.exon/phases/state.json` for build status
5. Check logs in `.exon/logs/` directory

### Common Resources
- **Exonpro Standards**: `.exon/standards/`
- **Stack Templates**: `.exon/stacks/`
- **Configuration**: `.exon/config/`
- **Build Logs**: `.exon/logs/`

---

**Happy Building!** 🚀
