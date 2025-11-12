# Industry-Specific Requirements Templates

This directory contains pre-built requirements files for 4 Salesforce Industry Clouds, ready to use with the exon-template automated builder.

## Available Industry Templates

### 1. 📚 Education Cloud (`requirements-education.md`)
**For:** Universities, K-12 schools, training institutes, EdTech companies

**Sample Project:** University Admissions & Student Success Platform
- Student recruitment and application management
- Enrollment and course registration
- Student success tracking with early warning system
- Alumni engagement and fundraising

**Key Features:**
- Application workflow automation
- GPA and attendance monitoring
- Advisor case management
- Alumni directory and donation tracking

**Use with:**
```bash
./start.sh
# When prompted for requirements, use:
# Option 2: Copy from existing file
# Enter path: ./requirements-education.md
```

---

### 2. 🏭 Manufacturing Cloud (`requirements-manufacturing.md`)
**For:** B2B manufacturers with distributor/dealer networks

**Sample Project:** Dealer Network & Rebate Management Platform
- Sales agreements with volume commitments
- Account-based revenue forecasting
- Automated rebate calculations
- Field visit planning and optimization

**Key Features:**
- Multi-year contract tracking
- Rebate program automation
- Dealer performance dashboards
- Route-optimized visit scheduling

**Use with:**
```bash
./start.sh
# When prompted for requirements, use:
# Option 2: Copy from existing file
# Enter path: ./requirements-manufacturing.md
```

---

### 3. 💻 Technology & Software (`requirements-technology.md`)
**For:** SaaS companies, software vendors, tech startups

**Sample Project:** SaaS Subscription & Support Platform
- Subscription lifecycle management (trials, renewals, upgrades)
- MRR/ARR tracking and forecasting
- Technical support with SLA management
- Customer health scoring based on usage

**Key Features:**
- Auto-renewal workflows
- Usage-based health scores
- Support ticket routing with SLA tracking
- Self-service customer portal

**Use with:**
```bash
./start.sh
# When prompted for requirements, use:
# Option 2: Copy from existing file
# Enter path: ./requirements-technology.md
```

---

### 4. 💰 Financial Services Cloud (`requirements-fintech.md`)
**For:** Banks, NBFCs, FinTech lending platforms, insurance companies

**Sample Project:** Digital Lending & KYC Platform
- Loan application and origination
- KYC/AML compliance automation
- Underwriting and approval workflows
- Loan servicing and EMI tracking

**Key Features:**
- Customer 360 with household relationships
- Credit score integration (CIBIL/Experian)
- Automated KYC verification
- Collections and delinquency management

**Use with:**
```bash
./start.sh
# When prompted for requirements, use:
# Option 2: Copy from existing file
# Enter path: ./requirements-fintech.md
```

---

## How to Use These Templates

### Option A: Use Template As-Is (Quickest)
```bash
# Start new project
./start.sh

# Enter project name (e.g., "university-admissions")
# Select Salesforce stack (only option)
# Enter Salesforce org details

# When prompted for requirements:
# Choose option 2: "Copy from existing requirements file"
# Enter path: ./requirements-education.md (or other template)

# Start automated build
```

### Option B: Customize Template First
```bash
# 1. Copy template to new file
cp requirements-education.md my-custom-requirements.md

# 2. Edit to match your specific needs
nano my-custom-requirements.md
# - Change project name
# - Add/remove features
# - Adjust timeline and scale

# 3. Use in start.sh
./start.sh
# Choose option 2: Copy from existing file
# Enter path: ./my-custom-requirements.md
```

### Option C: Use as Reference (Most Customization)
```bash
# 1. Start project with generated template
./start.sh
# Choose option 1: Edit requirements.md now

# 2. Manually copy sections from industry template
# - Open requirements-education.md in another window
# - Copy relevant features into generated requirements.md
# - Adjust for your specific use case

# 3. Save and continue with build
```

---

## What Gets Generated

When you use these templates with `./start.sh`, the automated builder will:

### Phase 0 (5-10 min): Configuration
- Verify Salesforce CLI installed
- Check org authentication
- Validate project structure

### Phase 1 (30-60 min): Research & Planning
- Break down features into modules (with priorities)
- Research LWC component architecture
- Design Custom Objects and fields
- Plan Apex class structure
- Create implementation plan (MVP vs Post-MVP)

### Phase 2 (45-90 min): Architecture Design
- Define complete data model (objects, fields, relationships)
- Design Apex class hierarchy (Services, Selectors, Controllers)
- Plan LWC component structure
- Create API specifications

### Phase 3 (2-4 hours): Code Generation
- Generate SFDX project structure
- Create Custom Objects and Fields
- Write Apex classes (Controllers, Services, Selectors, Triggers)
- Build LWC components (.js, .html, .css)
- Create Lightning Pages and navigation
- Generate deployment scripts

### Phase 4 (30-60 min): Validation
- Validate SFDX structure
- Check syntax (Apex and LWC)
- Generate validation report

### Phase 5 (45-90 min): Deployment
- Deploy to Salesforce org: `sf project deploy start`
- Run demo data setup script
- Verify deployment
- Open org for testing

**Total Time:** 4-6 hours (fully automated)

---

## Template Structure

Each industry template follows this structure:

```markdown
# Project Name: [kebab-case-name]

## Business Problem
[2-3 sentences describing the pain points]

## Solution
[2-3 sentences describing how Salesforce solves it]

## Target Users
[5-7 user personas with their needs]

## Key Features

### Phase 1 (MVP)
[5-7 critical features to implement NOW]

### Phase 2 (Post-MVP)
[3-5 future enhancements]

## Scale Requirements
[User counts, peak loads, growth potential]

## Technical Requirements
- Salesforce Products needed
- Custom Objects to create
- Apex Components needed
- LWC Components needed
- Integrations required
- Automation needs (Triggers, Flows)

## Compliance & Security
[Industry-specific regulations and security needs]

## Testing Requirements
[Demo vs Production testing approach]

## Timeline
[Milestone dates]
```

---

## Tips for BTS 2025 Demos

### For Education Sector Visitors:
```bash
# Use Education template
./start.sh
# Project name: university-admissions-demo
# Copy from: ./requirements-education.md

# Key selling point:
"We can implement Education Cloud to manage your entire student lifecycle
from inquiry to alumni, with automated admissions workflows and student
success tracking built in."
```

### For Manufacturing Companies:
```bash
# Use Manufacturing template
./start.sh
# Project name: dealer-network-demo
# Copy from: ./requirements-manufacturing.md

# Key selling point:
"Manufacturing Cloud gives you account-based forecasting and automated
rebate calculations, so you can manage 300+ dealers without spreadsheets."
```

### For SaaS Startups:
```bash
# Use Technology template
./start.sh
# Project name: saas-platform-demo
# Copy from: ./requirements-technology.md

# Key selling point:
"We implement Sales Cloud with CPQ to track MRR/ARR, automate renewals,
and monitor customer health scores based on product usage."
```

### For FinTech/NBFCs:
```bash
# Use FinTech template
./start.sh
# Project name: lending-platform-demo
# Copy from: ./requirements-fintech.md

# Key selling point:
"Financial Services Cloud gives you 360° customer view with built-in
compliance. We can implement KYC automation, credit score integration,
and loan lifecycle management in 4 months."
```

---

## Customization Guide

### Quick Edits (5 minutes):
1. Change project name (line 1)
2. Update business problem to match specific company (lines 3-7)
3. Adjust timeline (bottom of file)

### Medium Edits (30 minutes):
1. Add/remove features from Phase 1 based on actual needs
2. Adjust scale requirements (user counts, peak loads)
3. Modify integrations based on existing systems
4. Update compliance requirements

### Full Customization (2-3 hours):
1. Rewrite business problem and solution
2. Create custom user personas
3. Design completely different feature set
4. Add new Custom Objects not in template
5. Specify additional Apex services
6. Design custom LWC components

---

## Generated Project Structure

After using any template, your generated project will have:

```
~/Documents/00_All_Work/ExonProProjects/[project-name]/
├── force-app/main/default/
│   ├── lwc/                    # Generated LWC components
│   ├── classes/                # Generated Apex classes
│   ├── triggers/               # Generated Apex triggers
│   ├── objects/                # Generated Custom Objects
│   ├── tabs/                   # Generated custom tabs
│   └── flexipages/             # Generated Lightning pages
├── scripts/
│   ├── setup.apex              # Demo data creation script
│   └── deploy.sh               # Deployment automation
├── sfdx-project.json           # SFDX configuration
├── salesforce-config.json      # Org settings
├── requirements.md             # Your requirements (copied from template)
├── CLAUDE.md                   # Project brain (progress tracking)
└── .exon/
    ├── logs/                   # Build logs
    ├── phases/                 # Phase tracking
    └── stacks/                 # Stack templates
```

---

## FAQ

**Q: Can I mix features from multiple templates?**
A: Yes! Copy a base template, then manually add sections from other templates.

**Q: Do I need to deploy to an actual Salesforce org?**
A: For Phase 5 deployment, yes. But you can run Phases 0-4 without an org (generates code only).

**Q: How do I pause the build?**
A: Press Ctrl+C to stop. Run `./resume.sh ~/Documents/.../[project]` to continue.

**Q: Can I use these for non-demo (production) projects?**
A: Absolutely! The templates include production requirements. Set `demo_mode: false` in salesforce-config.json and enable testing in Phase 4.

**Q: What if my industry isn't listed?**
A: Use the closest template as a starting point and customize. Or use the generic template in `start.sh` (created automatically).

---

## Support

For issues or questions:
- GitHub: https://github.com/anthropics/claude-code/issues
- Documentation: https://docs.claude.com/claude-code

Built with ❤️ by Exonpro using Claude Code
