# 🚀 100% Automated Project Builder - START HERE

## What This Template Does

This is a **fully automated framework** that takes a business requirements document and builds a complete, production-ready application with **zero manual coding**.

The automation:
1. ✅ Researches your business domain deeply
2. ✅ Recommends the best technology stack
3. ✅ Breaks requirements into phased MVP
4. ✅ Implements models, APIs, frontend, and tests
5. ✅ Handles errors, retries, and resumption
6. ✅ Creates git branches and commits automatically

---

## Quick Start

### Step 1: Create Your App Details Document

Create a file (anywhere) with your business requirements. Example format:

```markdown
# App Name:
YourAppName

# Business Context (200 words)
## Problem:
What problem does this solve?

## Solution:
How does your app solve it?

## Target Market:
Who are the users?

## Key Users:
Different user types and their roles

## Value Proposition:
Key metrics and benefits
```

### Step 2: Copy This Prompt

**COPY THE ENTIRE SECTION BELOW AND PASTE INTO A NEW CLAUDE CODE SESSION FROM THE `/Users/kusaldipdas/Documents/00_All_Work/exon-template` DIRECTORY:**

---

## 🎯 FINAL PROMPT (Copy this entire section)

```
I want you to build a complete production-ready application using the 100% automated framework in this directory.

**Framework Location:** `/Users/kusaldipdas/Documents/00_All_Work/exon-template/.exon/`

**My Business Requirements:** `/path/to/your/app_details.md`

**Instructions:**

1. Read and understand the framework structure in `.exon/README.md`

2. Read my business requirements from the path I provided above

3. Execute all phases automatically:
   - **Phase 1: Deep Research**
     - Analyze the business domain
     - Research best practices and competitive solutions
     - Recommend optimal technology stack (frontend, backend, database, deployment)
     - Update `.exon/constitution.md` with chosen stack and patterns
     - Output: `.exon/research/domain_analysis.md`, `.exon/research/best_practices.md`

   - **Phase 2: Requirements & Feature Breakdown**
     - Extract all features from requirements
     - Create detailed user stories
     - Generate prioritized features.csv
     - Output: `.exon/specs/requirements.json`, `.exon/specs/features.csv`

   - **Phase 3: MVP Phasing**
     - Break features into implementation phases
     - Define Phase 1 (Core MVP), Phase 2 (Extended), Phase 3 (Advanced)
     - Create roadmap
     - Output: `.exon/specs/phases/*.json`, `.exon/specs/mvp_roadmap.md`

   - **Phase 4+: Implementation**
     For each phase, create a git branch and implement:
     - Database models
     - Request/Response schemas
     - API routers with full CRUD
     - Frontend components
     - Tests (unit + integration)
     Auto-commit after each sub-phase completes.

4. **Error Handling:**
   - Retry API calls 5 times with 10-second intervals
   - If all retries fail: save checkpoint, log error, wait for manual resume
   - Track all progress in `.exon/automation/state.json`

5. **Progress Tracking:**
   - Update state.json after each milestone
   - Create checkpoints in `.exon/automation/checkpoints/`
   - Log everything to `.exon/logs/`

6. **Git Operations:**
   - Create branch for each phase: `phase-1-research`, `phase-2-requirements`, etc.
   - Auto-commit with descriptive messages
   - Keep main branch clean

**Configuration:**
- Follow `.exon/constitution.md` for architecture patterns (update during research)
- All automation artifacts stay in `.exon/` directory
- Keep root directory clean with only actual project code

**Expected Outcome:**
A fully functional, production-ready application with:
- Complete backend API
- Responsive frontend
- Database migrations
- Authentication & authorization
- Comprehensive tests
- Documentation
- Deployment-ready

**Start now and run through all phases automatically. Ask me questions only if the requirements document is unclear or missing critical information.**
```

---

## Step 3: Watch It Build

Claude Code will:
- ✅ Analyze your business
- ✅ Choose the best tech stack
- ✅ Build everything automatically
- ✅ Save progress continuously
- ✅ Resume if interrupted

## Step 4: Resume If Needed

If interrupted, resume with:
```
Continue from where we left off. Check `.exon/automation/state.json` for current progress and resume the automation.
```

---

## Directory Structure After Completion

```
exon-template/
├── .exon/                  # Automation artifacts (gitignored)
│   ├── research/           # Phase 1 outputs
│   ├── specs/              # Phase 2-3 outputs
│   ├── logs/               # All logs
│   └── automation/         # State tracking
├── backend/                # Generated backend code
├── frontend/               # Generated frontend code
├── docker-compose.yml      # Generated deployment config
└── README.md               # Generated project README
```

---

## Tips

1. **Be specific** in your app_details.md document
2. **Let it run** - the automation handles everything
3. **Check logs** if you want to see detailed progress
4. **Trust the process** - it will ask if something is unclear

---

**Ready? Copy the FINAL PROMPT section above and start a new Claude Code session in this directory!**
