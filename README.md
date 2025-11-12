# Exonpro Salesforce Template

Automated project generation framework that creates complete Salesforce applications with Lightning Web Components (LWC), Apex classes, Custom Objects, and deployment scripts.

## 🚀 Quick Start

### For Linux/Mac Users

```bash
# 1. Make scripts executable (first time only)
chmod +x start.sh resume.sh cleanup.sh

# 2. Create new project
./start.sh

# 3. Resume interrupted build
./resume.sh ~/Documents/00_All_Work/ExonProProjects/my-project

# 4. Delete test project
./cleanup.sh ~/Documents/00_All_Work/ExonProProjects/test-project
```

### For Windows Users

```powershell
# 1. Open PowerShell as Administrator (first time only)
# Run: Set-ExecutionPolicy RemoteSigned

# 2. Create new project
.\start.ps1

# 3. Resume interrupted build
.\resume.ps1 C:\Users\YourName\Documents\00_All_Work\ExonProProjects\my-project

# 4. Delete test project
.\cleanup.ps1 C:\Users\YourName\Documents\00_All_Work\ExonProProjects\test-project
```

## 📋 Prerequisites

### Required (All Platforms)

1. **Python 3.8+**
   ```bash
   python --version  # Should show 3.8 or higher
   ```

2. **Salesforce CLI**
   ```bash
   # Install
   npm install -g @salesforce/cli

   # Verify
   sf --version
   ```

3. **Salesforce Developer Org** (Free)
   - Sign up: https://developer.salesforce.com/signup
   - Login to org: `sf org login web --alias DevOrg`

4. **Claude Agent SDK**
   ```bash
   # Installed automatically by scripts
   pip install claude-agent-sdk
   ```

5. **Git**
   ```bash
   git --version
   ```

### Optional

- **VS Code** with Salesforce Extension Pack (recommended)
- **Node.js** (for LWC local development)

## 📁 Project Structure

```
exon-template-sfdc-demo/
├── start.sh / start.ps1           # Create new project (Linux/Windows)
├── resume.sh / resume.ps1         # Resume build (Linux/Windows)
├── cleanup.sh / cleanup.ps1       # Delete project (Linux/Windows)
│
├── requirements-education.md      # Education Cloud template
├── requirements-manufacturing.md  # Manufacturing Cloud template
├── requirements-technology.md     # SaaS/Tech template
├── requirements-fintech.md        # Financial Services Cloud template
├── INDUSTRY-REQUIREMENTS.md       # Usage guide for templates
│
├── builder/
│   ├── build.py                   # Automated builder (Python)
│   ├── simple-todo-builder.py     # Resume incomplete projects
│   ├── requirements.txt           # Python dependencies
│   └── venv/                      # Python virtual env (auto-created)
│
└── .exon/
    ├── standards/                 # Coding standards (copied to projects)
    │   ├── CLAUDE.md.template
    │   ├── code-structure.md
    │   ├── naming-conventions.md
    │   ├── security-best-practices.md
    │   └── testing-requirements.md
    │
    └── stacks/
        └── salesforce-lwc-apex/   # Salesforce stack template
            ├── CLAUDE.md
            ├── constitution.md
            ├── folder-structure.json
            └── .claude/settings.json
```

## 🎯 Usage Examples

### Example 1: Create University Admissions Platform

**Linux/Mac:**
```bash
./start.sh

# Project name: university-admissions
# Org username: your@email.com
# Org alias: DevOrg
#
# When asked for requirements:
# Choose option 2: Copy from existing file
# Enter: ./requirements-education.md
#
# Start build: Y
```

**Windows:**
```powershell
.\start.ps1

# Same prompts as above
```

### Example 2: Create SaaS Subscription Platform

**Linux/Mac:**
```bash
./start.sh

# Project name: saas-subscription-platform
# Choose option 2 for requirements
# Enter: ./requirements-technology.md
```

**Windows:**
```powershell
.\start.ps1
# Same as above
```

### Example 3: Resume Interrupted Build

**Linux/Mac:**
```bash
./resume.sh ~/Documents/00_All_Work/ExonProProjects/university-admissions
```

**Windows:**
```powershell
.\resume.ps1 C:\Users\YourName\Documents\00_All_Work\ExonProProjects\university-admissions
```

## 📚 Industry-Specific Templates

### 1. Education Cloud (`requirements-education.md`)
- Student recruitment and admissions
- Enrollment management
- Student success tracking
- Alumni engagement

**Use Case:** Universities, K-12 schools, training institutes

### 2. Manufacturing Cloud (`requirements-manufacturing.md`)
- Sales agreement management
- Rebate program automation
- Account-based forecasting
- Dealer network management

**Use Case:** B2B manufacturers with distributor networks

### 3. Technology & SaaS (`requirements-technology.md`)
- Subscription lifecycle management
- MRR/ARR tracking
- Technical support with SLA
- Customer health scoring

**Use Case:** SaaS companies, software vendors

### 4. Financial Services Cloud (`requirements-fintech.md`)
- Loan application workflow
- KYC/AML compliance
- Customer 360 with households
- Loan servicing and collections

**Use Case:** Banks, NBFCs, FinTech lenders

See [INDUSTRY-REQUIREMENTS.md](./INDUSTRY-REQUIREMENTS.md) for detailed guide.

## 🔧 What Gets Generated

The automated builder creates:

### Phase 0 (5-10 min): Configuration
- Validates Salesforce CLI
- Checks org authentication
- Sets up project structure

### Phase 1 (30-60 min): Research
- Breaks down features into modules
- Assigns priorities (Critical/Medium/Low)
- Researches LWC and Apex patterns
- Creates implementation plan

### Phase 2 (45-90 min): Architecture
- Designs Custom Objects and Fields
- Plans Apex class structure
- Designs LWC component hierarchy
- Creates data model

### Phase 3 (2-4 hours): Code Generation
- Creates SFDX project (`sfdx-project.json`)
- Generates Custom Objects (`.object-meta.xml`)
- Writes Apex classes (`.cls` + `.cls-meta.xml`)
- Builds LWC components (`.js`, `.html`, `.css`, `.js-meta.xml`)
- Creates Lightning Pages (`.flexipage-meta.xml`)
- Generates deployment scripts

### Phase 4 (30-60 min): Validation
- Validates SFDX structure
- Checks Apex/LWC syntax
- Generates validation report

### Phase 5 (45-90 min): Deployment
- Deploys to Salesforce: `sf project deploy start`
- Runs demo data setup script
- Opens org for testing

**Total Time:** 4-6 hours (fully automated)

## Generated Project Structure

```
~/Documents/00_All_Work/ExonProProjects/my-project/
├── force-app/main/default/
│   ├── lwc/                    # Lightning Web Components
│   │   ├── componentName/
│   │   │   ├── componentName.js
│   │   │   ├── componentName.html
│   │   │   ├── componentName.css
│   │   │   └── componentName.js-meta.xml
│   │
│   ├── classes/                # Apex classes
│   │   ├── AccountController.cls
│   │   ├── AccountService.cls
│   │   ├── AccountSelector.cls
│   │   └── *.cls-meta.xml
│   │
│   ├── triggers/               # Apex triggers
│   │   ├── AccountTrigger.trigger
│   │   └── AccountTrigger.trigger-meta.xml
│   │
│   ├── objects/                # Custom Objects
│   │   ├── CustomObject__c/
│   │   │   ├── CustomObject__c.object-meta.xml
│   │   │   └── fields/*.field-meta.xml
│   │
│   ├── tabs/                   # Custom tabs
│   ├── flexipages/             # Lightning pages
│   └── applications/           # Lightning apps
│
├── scripts/
│   ├── setup.apex              # Demo data creation
│   └── deploy.sh / deploy.ps1  # Deployment automation
│
├── sfdx-project.json           # SFDX configuration
├── salesforce-config.json      # Org settings
├── requirements.md             # Your requirements
├── CLAUDE.md                   # Project brain (progress tracking)
├── TODO.md                     # Task list (created in Phase 1)
│
└── .exon/
    ├── logs/                   # Build logs
    ├── phases/state.json       # Resume checkpoint
    ├── standards/              # Coding standards
    └── stacks/                 # Stack templates
```

## 🛠️ Common Commands

### Salesforce CLI Commands (Generated Projects)

```bash
# Deploy to org
cd ~/Documents/00_All_Work/ExonProProjects/my-project
sf project deploy start

# Open org
sf org open

# Run demo data script
sf apex run --file scripts/setup.apex

# Retrieve changes from org
sf project retrieve start

# View logs
sf apex log tail
```

### Builder Commands

**Linux/Mac:**
```bash
# Create new project
./start.sh

# Resume build
./resume.sh /path/to/project

# Clean up
./cleanup.sh /path/to/project
```

**Windows:**
```powershell
# Create new project
.\start.ps1

# Resume build
.\resume.ps1 C:\path\to\project

# Clean up
.\cleanup.ps1 C:\path\to\project
```

## 🔒 Demo Mode vs Production Mode

### Demo Mode (Default)
- **Testing:** Optional (skip Apex tests)
- **Security:** Use Salesforce platform defaults
- **Validation:** Minimal (syntax checks only)
- **Focus:** Happy path implementation
- **Timeline:** Faster (3-4 hours for Phase 3)

### Production Mode
To convert demo to production:

1. **Enable Testing:**
   ```json
   // salesforce-config.json
   "demo_mode": {
     "enabled": false,
     "skip_tests": false
   }
   ```

2. **Add Apex Tests:**
   - 75%+ code coverage required
   - Test bulk operations (200+ records)
   - Add negative test cases

3. **Implement Security:**
   - Configure sharing rules
   - Set field-level security (FLS)
   - Add object-level security (OLS)
   - Use `WITH SECURITY_ENFORCED` in SOQL

4. **Add Error Handling:**
   - Comprehensive try-catch blocks
   - User-friendly error messages
   - Logging and monitoring

5. **Optimize for Governor Limits:**
   - Bulkify all Apex code
   - Avoid SOQL in loops
   - Use batch Apex for large datasets

## 🐛 Troubleshooting

### Windows: "Cannot run scripts"
```powershell
# Run as Administrator
Set-ExecutionPolicy RemoteSigned

# Or run with bypass
powershell -ExecutionPolicy Bypass -File .\start.ps1
```

### "Salesforce CLI not found"
```bash
# Install globally
npm install -g @salesforce/cli

# Verify
sf --version

# If still not found, add to PATH
# Mac: ~/.zshrc or ~/.bash_profile
# Windows: System Environment Variables
```

### "Claude Agent SDK import error"
```bash
# Reinstall in virtual environment
cd builder
rm -rf venv  # or Remove-Item venv -Recurse (Windows)
python -m venv venv
./venv/bin/pip install -r requirements.txt  # Linux/Mac
.\venv\Scripts\pip.exe install -r requirements.txt  # Windows
```

### "Deployment failed"
```bash
# Check if logged into org
sf org list

# Login if needed
sf org login web --alias DevOrg

# Set default org
sf config set target-org DevOrg

# Try deployment again
cd /path/to/project
sf project deploy start
```

### Build interrupted / Want to resume
```bash
# Linux/Mac
./resume.sh /path/to/project

# Windows
.\resume.ps1 C:\path\to\project

# Check state
cat .exon/phases/state.json  # Linux/Mac
Get-Content .exon\phases\state.json  # Windows
```

## 📖 Additional Resources

- **Salesforce Developer Docs:** https://developer.salesforce.com/docs
- **LWC Documentation:** https://developer.salesforce.com/docs/component-library/documentation/en/lwc
- **Apex Developer Guide:** https://developer.salesforce.com/docs/atlas.en-us.apexcode.meta/apexcode/
- **Trailhead (Free Learning):** https://trailhead.salesforce.com/
- **Claude Code Docs:** https://docs.claude.com/claude-code

## 🤝 Support

For issues or questions:
- GitHub Issues: https://github.com/anthropics/claude-code/issues
- Documentation: https://docs.claude.com/claude-code

## 📝 License

Built with Claude Code by Exonpro

---

## Quick Reference Card

### Create New Project

| Platform | Command |
|----------|---------|
| Linux/Mac | `./start.sh` |
| Windows | `.\start.ps1` |

### Resume Build

| Platform | Command |
|----------|---------|
| Linux/Mac | `./resume.sh /path/to/project` |
| Windows | `.\resume.ps1 C:\path\to\project` |

### Delete Project

| Platform | Command |
|----------|---------|
| Linux/Mac | `./cleanup.sh /path/to/project` |
| Windows | `.\cleanup.ps1 C:\path\to\project` |

### Deploy to Salesforce

```bash
cd /path/to/project
sf project deploy start
sf org open
```

**Estimated Time:** 4-6 hours for complete application generation
