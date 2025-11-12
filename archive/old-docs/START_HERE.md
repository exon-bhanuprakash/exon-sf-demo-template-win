# 🚀 Exonpro Template - Start Here

Welcome to the Exonpro Universal App Template! Build production-ready AWS applications in hours, not weeks.

## Choose Your Approach

### 🤖 Automated Build (Recommended)
**⏱ Time**: 4-6 hours unattended | **🎯 Difficulty**: Easy | **📦 Output**: Complete production app

Build everything automatically with one command. The builder spawns a Claude Code session that writes all code, runs tests, and deploys to AWS.

**Best for:**
- Production applications
- Standard business apps (CRM, SaaS, dashboards, e-commerce)
- When you want best practices without manual work
- When you have clear requirements

**📖 Full Guide**: [QUICK_START_AUTO.md](./QUICK_START_AUTO.md)

```bash
# Quick preview:
./init-project.sh my-app /path/to/projects
cd /path/to/projects/my-app
# 1. Fill requirements.md
# 2. Add API key to builder/.env
./start-build.sh  # ← Done! Come back in 4-6 hours
```

---

### 👨‍💻 Manual Build (Step-by-Step)
**⏱ Time**: Your pace | **🎯 Difficulty**: Medium | **📦 Output**: Custom application

Build with Claude Code's help in this session, controlling every decision and learning as you go.

**Best for:**
- Learning the architecture
- Prototyping and experimentation
- Heavy customization from the start
- Evolving requirements

**📖 Full Guide**: [QUICK_START_MANUAL.md](./QUICK_START_MANUAL.md)

```bash
# Quick preview:
./init-project.sh my-app /path/to/projects
cd /path/to/projects/my-app
# 1. Fill requirements.md
# 2. Tell Claude Code what to build: "Create X feature"
```

---

## Quick Comparison

| Feature | 🤖 Automated | 👨‍💻 Manual |
|---------|--------------|-------------|
| **Time** | 4-6 hours (unattended) | Days to weeks (your pace) |
| **Effort** | Fill requirements.md only | Continuous interaction |
| **Code quality** | Best practices enforced | You decide |
| **Learning** | Review after | Learn as you build |
| **Customization** | Modify after generation | Customize during build |
| **Best for** | Production apps | Prototypes, learning |

---

## What Gets Built

Both approaches create a complete AWS application:

```
your-app/
├── infrastructure/          # AWS CDK code
│   ├── lib/
│   │   ├── database-stack.ts      # DynamoDB table
│   │   ├── auth-stack.ts          # AWS Cognito
│   │   ├── api-node-stack.ts      # Node.js Lambdas
│   │   ├── api-python-stack.ts    # Python Lambdas (if hybrid)
│   │   ├── api-gateway-stack.ts   # API Gateway
│   │   └── frontend-stack.ts      # S3 + CloudFront (optional)
│   └── bin/app.ts
│
├── backend/
│   ├── nodejs/              # Node.js Lambda functions
│   │   ├── src/
│   │   │   ├── functions/   # Lambda handlers (CRUD operations)
│   │   │   ├── repositories/ # DynamoDB access layer
│   │   │   ├── services/    # Business logic
│   │   │   └── utils/       # Helpers, middleware
│   │   └── tests/
│   │
│   └── python/              # Python Lambda functions (if hybrid stack)
│       ├── src/
│       │   ├── functions/   # Lambda handlers (analytics, ML)
│       │   └── repositories/
│       └── tests/
│
├── apps/web/                # SvelteKit frontend
│   ├── src/
│   │   ├── routes/          # Pages (+page.svelte)
│   │   └── lib/
│   │       ├── components/  # Reusable components
│   │       ├── stores/      # State management
│   │       ├── api/         # API client
│   │       └── types/       # TypeScript types
│   └── tests/
│
├── shared/                  # Shared types and utilities
│   ├── types/               # TypeScript interfaces
│   └── utils/               # Common utilities
│
├── research/                # Research outputs (automated only)
│   ├── domain_analysis.md
│   ├── stack_justification.md
│   └── cost_analysis.md
│
├── architecture/            # Architecture docs (automated only)
│   ├── system-architecture.md
│   ├── api-specification.md
│   └── database-schema.md
│
├── README.md                # Complete documentation
├── DEPLOYMENT.md            # Deployment guide
└── requirements.md          # Your business requirements
```

**Deployed to AWS:**
- ✅ DynamoDB (serverless NoSQL database)
- ✅ AWS Lambda (serverless backend functions)
- ✅ API Gateway (RESTful API with CORS)
- ✅ AWS Cognito (user authentication)
- ✅ CloudWatch (logs and monitoring)
- ✅ S3 + CloudFront (frontend hosting - optional)

---

## Available Tech Stacks

### 1. 🔀 Hybrid: Node.js + Python (Recommended)
- **Frontend**: SvelteKit (TypeScript)
- **Backend**: Node.js (CRUD) + Python (AI/ML, analytics)
- **Database**: DynamoDB (single-table design)
- **Hosting**: AWS Serverless (Lambda + API Gateway)
- **Best for**: Business apps with analytics, ML, or data processing
- **Cost**: $15-30/month (dev), $60-130/month (prod)

### 2. 📘 Node.js Only
- **Frontend**: SvelteKit (TypeScript)
- **Backend**: Node.js + Express
- **Database**: DynamoDB
- **Hosting**: AWS Serverless
- **Best for**: Standard web apps, real-time features
- **Cost**: $10-25/month (dev), $50-100/month (prod)

### 3. 🐍 Python Only
- **Frontend**: SvelteKit (TypeScript)
- **Backend**: Python FastAPI
- **Database**: DynamoDB
- **Hosting**: AWS Serverless
- **Best for**: Data-heavy apps, ML-focused, Python teams
- **Cost**: $10-25/month (dev), $50-100/month (prod)

### 4. 🐘 PostgreSQL Stack
- **Frontend**: SvelteKit (TypeScript)
- **Backend**: Python FastAPI
- **Database**: PostgreSQL
- **Hosting**: AWS Lightsail (VPS)
- **Best for**: Relational data, predictable traffic, fixed budget
- **Cost**: $25/month (fixed) for dev+prod

---

## Prerequisites

### Required for All
- ✅ **AWS Account** ([Create one](https://aws.amazon.com/))
- ✅ **AWS CLI** configured ([Installation guide](https://docs.aws.amazon.com/cli/latest/userguide/getting-started-install.html))
- ✅ **Node.js 18+** ([Download](https://nodejs.org/))
- ✅ **Git** installed

### Additional for Automated Build
- ✅ **Anthropic API Key** ([Get one](https://console.anthropic.com/settings/keys))

### Verify Setup

```bash
# Check AWS credentials
aws sts get-caller-identity
# Should show your account ID

# Check Node.js version
node --version
# Should be v18 or higher

# Check Git
git --version
```

---

## Getting Started (Choose Your Path)

### 🤖 Path 1: Automated Build (Recommended)

```bash
# 1. Initialize project
cd /Users/kusaldipdas/Documents/00_All_Work/exon-template
./init-project.sh my-app /path/to/projects

# 2. Navigate to project
cd /path/to/projects/my-app

# 3. Fill requirements.md
nano requirements.md
# Replace all placeholders with your business details

# 4. Configure builder
cd builder && cp .env.example .env && nano .env
# Add: ANTHROPIC_API_KEY=sk-ant-api03-...
cd ..

# 5. Start automated build
./start-build.sh
# Press Enter when prompted
# Come back in 4-6 hours!
```

**📖 Complete guide**: [QUICK_START_AUTO.md](./QUICK_START_AUTO.md)

---

### 👨‍💻 Path 2: Manual Build

```bash
# 1. Initialize project
cd /Users/kusaldipdas/Documents/00_All_Work/exon-template
./init-project.sh my-app /path/to/projects

# 2. Navigate to project
cd /path/to/projects/my-app

# 3. Fill requirements.md
nano requirements.md

# 4. Tell Claude Code what to build
# Example: "Build the complete application following these steps:
#   1. Create folder structure
#   2. Generate shared types
#   3. Create DynamoDB repositories
#   4. Generate Lambda functions
#   5. Create CDK infrastructure
#   6. Generate SvelteKit frontend
#   7. Create tests"
```

**📖 Complete guide**: [QUICK_START_MANUAL.md](./QUICK_START_MANUAL.md)

---

## Cost Estimates

### Development Environment
| Service | Cost/Month |
|---------|------------|
| DynamoDB (on-demand) | ~$5-10 |
| Lambda (1M requests/month) | ~$5-15 |
| API Gateway | ~$3-5 |
| Cognito (free tier) | $0 |
| **Total Dev** | **~$15-30/month** |

### Production Environment
| Service | Cost/Month |
|---------|------------|
| DynamoDB (on-demand) | ~$20-40 |
| Lambda (reserved concurrency) | ~$20-50 |
| API Gateway | ~$10-20 |
| CloudFront (frontend) | ~$10-20 |
| **Total Prod** | **~$60-130/month** |

*Costs vary by usage. The template optimizes for cost-effectiveness!*

---

## Example Use Cases

### SaaS Application
```
Features: User management, subscriptions, analytics dashboard
Stack: Hybrid (Node.js + Python)
Time: 4-6 hours automated
Cost: $60-100/month production
```

### CRM System
```
Features: Contacts, deals, pipeline, activities, reports
Stack: Node.js only
Time: 4-6 hours automated
Cost: $50-80/month production
```

### E-commerce Platform
```
Features: Products, cart, checkout, recommendations (ML)
Stack: Hybrid (Node.js + Python)
Time: 4-6 hours automated
Cost: $80-150/month production
```

### Internal Dashboard
```
Features: Data visualization, reports, user management
Stack: Python only
Time: 4-6 hours automated
Cost: $40-70/month production
```

---

## Documentation

### 🚀 Quick Start Guides
- **[QUICK_START_AUTO.md](./QUICK_START_AUTO.md)** - Automated build (recommended)
- **[QUICK_START_MANUAL.md](./QUICK_START_MANUAL.md)** - Manual build guide

### 📚 Reference Documentation
- **[CLAUDE.md](./CLAUDE.md)** - Complete framework documentation
- **[README.md](./README.md)** - Comprehensive overview
- **[builder/README.md](./builder/README.md)** - Builder implementation details

### 🏗 Architecture & Standards
- **[.exon/standards/](./exon/standards/)** - Coding standards and best practices
- **[.exon/stacks/](./exon/stacks/)** - Available tech stack templates

### 🔧 Advanced Guides
- **[AUTOMATION-SUMMARY.md](./AUTOMATION-SUMMARY.md)** - How automation works
- **[RESUME-GUIDE.md](./RESUME-GUIDE.md)** - Resume interrupted builds
- **[AWS-SETUP.md](./AWS-SETUP.md)** - AWS account configuration

---

## Troubleshooting

### "requirements.md not filled"
```bash
# Make sure you replaced ALL placeholders
grep "\[What problem" requirements.md
# Should return nothing if properly filled
```

### "ANTHROPIC_API_KEY not found"
```bash
# Check .env exists in builder directory
cat builder/.env
# Should show: ANTHROPIC_API_KEY=sk-ant-...
```

### AWS Credentials Error
```bash
# Verify AWS credentials
aws sts get-caller-identity
# Should show your account details
```

### Builder Not Starting
```bash
# Check Node.js version
node --version  # Should be 18+

# Reinstall dependencies
cd builder
rm -rf node_modules
npm install
```

---

## Next Steps

1. **Choose your approach** (automated or manual)
2. **Read the appropriate quick start guide**
3. **Initialize your project** with `./init-project.sh`
4. **Fill requirements.md** with your business requirements
5. **Build!** (automated: `./start-build.sh`, manual: ask Claude Code)

---

## Support

- **Issues**: Report on GitHub or internal Exonpro repo
- **Questions**: Check documentation in this repository
- **Builder Help**: See [builder/README.md](./builder/README.md)

---

## Version

**Current Version**: 1.0.0

**Last Updated**: November 2025

---

**Ready to build your next AWS application? Choose your path above and get started! 🚀**

🤖 Powered by Claude Agent SDK | 🏗 Built by Exonpro
