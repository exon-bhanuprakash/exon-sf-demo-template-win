# Windows Setup Guide

Quick start guide for Windows users to run the Exonpro Salesforce Template.

## ⚠️ First Time Setup (One Time Only)

### Step 1: Enable PowerShell Script Execution

1. **Open PowerShell as Administrator**
   - Press `Win + X`
   - Select "Windows PowerShell (Admin)" or "Terminal (Admin)"

2. **Run this command:**
   ```powershell
   Set-ExecutionPolicy RemoteSigned
   ```

3. **Type `Y` when prompted**

4. **Close PowerShell**

### Step 2: Install Prerequisites

#### Install Python 3.8+

1. Download from: https://www.python.org/downloads/
2. **Important:** Check "Add Python to PATH" during installation
3. Verify:
   ```powershell
   python --version
   ```

#### Install Node.js (for Salesforce CLI)

1. Download from: https://nodejs.org/
2. Install the LTS version
3. Verify:
   ```powershell
   node --version
   npm --version
   ```

#### Install Salesforce CLI

1. Open PowerShell (regular, not Admin)
2. Run:
   ```powershell
   npm install -g @salesforce/cli
   ```
3. Verify:
   ```powershell
   sf --version
   ```

#### Install Git

1. Download from: https://git-scm.com/download/win
2. Install with default options
3. Verify:
   ```powershell
   git --version
   ```

### Step 3: Get a Salesforce Developer Org (Free)

1. Sign up: https://developer.salesforce.com/signup
2. Fill in the form (use your email)
3. Check email for verification
4. Login to your new org

### Step 4: Login to Salesforce from CLI

```powershell
sf org login web --alias DevOrg
```

- Browser will open
- Login with your Developer Org credentials
- Authorize the CLI
- You should see "Successfully authorized..."

Verify:
```powershell
sf org list
```

## 🚀 Usage (Every Time)

### Create New Project

1. **Open PowerShell**
   - Press `Win + X`
   - Select "Windows PowerShell" (regular, not Admin)

2. **Navigate to template directory**
   ```powershell
   cd C:\path\to\exon-template-sfdc-demo
   ```

3. **Run start script**
   ```powershell
   .\start.ps1
   ```

4. **Follow prompts:**
   - Project name: `my-salesforce-app`
   - Parent directory: (press Enter for default)
   - Org username: (the email you used for Developer Org)
   - Org alias: `DevOrg`
   - Contact email: (your email)

5. **Choose requirements option:**
   - Option 1: Edit now (opens Notepad)
   - Option 2: Copy from template (e.g., `.\requirements-education.md`)
   - Option 3: Skip (edit later)

6. **Start build: `Y`**

7. **Wait 4-6 hours** (script runs automatically)

### Resume Interrupted Build

If build was interrupted (closed PowerShell, error, etc.):

```powershell
.\resume.ps1 C:\Users\YourName\Documents\00_All_Work\ExonProProjects\my-project
```

### Delete Test Project

```powershell
.\cleanup.ps1 C:\Users\YourName\Documents\00_All_Work\ExonProProjects\test-project
```

Type `DELETE` to confirm.

## 📂 Default Project Location

Projects are created in:
```
C:\Users\YourName\Documents\00_All_Work\ExonProProjects\
```

## 🛠️ Common Commands

### Navigate to Project

```powershell
cd C:\Users\YourName\Documents\00_All_Work\ExonProProjects\my-project
```

### Deploy to Salesforce

```powershell
sf project deploy start
```

### Open Salesforce Org

```powershell
sf org open
```

### Run Demo Data Script

```powershell
sf apex run --file scripts\setup.apex
```

### View Generated Files

```powershell
# List all LWC components
dir force-app\main\default\lwc

# List all Apex classes
dir force-app\main\default\classes

# View specific file
code force-app\main\default\lwc\myComponent\myComponent.js
# or
notepad force-app\main\default\lwc\myComponent\myComponent.js
```

## 🐛 Troubleshooting

### Issue: "Cannot run scripts"

**Error:**
```
.\start.ps1 : File cannot be loaded because running scripts is disabled on this system.
```

**Fix:**
```powershell
# Run as Administrator
Set-ExecutionPolicy RemoteSigned

# Or run with bypass
powershell -ExecutionPolicy Bypass -File .\start.ps1
```

### Issue: "Python not found"

**Error:**
```
python : The term 'python' is not recognized...
```

**Fix:**
1. Reinstall Python from https://www.python.org/downloads/
2. **Check "Add Python to PATH"** during installation
3. Restart PowerShell
4. Verify: `python --version`

### Issue: "sf not found"

**Error:**
```
sf : The term 'sf' is not recognized...
```

**Fix:**
```powershell
# Install Salesforce CLI
npm install -g @salesforce/cli

# If npm not found, install Node.js first
# https://nodejs.org/

# Restart PowerShell after installation
```

### Issue: "Not logged into Salesforce"

**Error:**
```
No org found. Please login...
```

**Fix:**
```powershell
sf org login web --alias DevOrg
```

Browser opens → Login → Authorize → Done

### Issue: Build failed during deployment

**Check if logged in:**
```powershell
sf org list
```

**Re-login if needed:**
```powershell
sf org login web --alias DevOrg
```

**Set default org:**
```powershell
sf config set target-org DevOrg
```

**Try deployment manually:**
```powershell
cd C:\Users\YourName\Documents\00_All_Work\ExonProProjects\my-project
sf project deploy start
```

### Issue: Python virtual environment errors

**Fix:**
```powershell
cd C:\path\to\exon-template-sfdc-demo\builder

# Delete old venv
Remove-Item venv -Recurse -Force

# Create new venv
python -m venv venv

# Install dependencies
.\venv\Scripts\pip.exe install -r requirements.txt

# Go back to template directory
cd ..

# Try start.ps1 again
.\start.ps1
```

## 📋 Pre-Flight Checklist

Before running `.\start.ps1`, verify:

- [ ] PowerShell script execution enabled (`Set-ExecutionPolicy RemoteSigned`)
- [ ] Python installed and in PATH (`python --version`)
- [ ] Node.js installed (`node --version`)
- [ ] Salesforce CLI installed (`sf --version`)
- [ ] Git installed (`git --version`)
- [ ] Logged into Salesforce Developer Org (`sf org list`)
- [ ] In template directory (`cd C:\path\to\exon-template-sfdc-demo`)

## 🎯 Quick Start Example (Full Workflow)

```powershell
# 1. Navigate to template
cd C:\exon-template-sfdc-demo

# 2. Start new project
.\start.ps1

# Project name: university-admissions
# Org username: your@email.com
# Org alias: DevOrg
# Requirements: Option 2 → .\requirements-education.md
# Start build: Y

# 3. Wait for build to complete (4-6 hours)

# 4. Navigate to generated project
cd C:\Users\YourName\Documents\00_All_Work\ExonProProjects\university-admissions

# 5. Deploy to Salesforce (if not auto-deployed)
sf project deploy start

# 6. Open Salesforce org
sf org open

# 7. Run demo data script
sf apex run --file scripts\setup.apex

# 8. Navigate in Salesforce to see your app
# App Launcher → [Your App Name]
```

## 💡 Tips for Windows Users

### Use Tab Completion

PowerShell supports tab completion:
```powershell
cd .\req[TAB]  # Completes to .\requirements-education.md
```

### Copy File Paths Easily

1. Hold `Shift` and right-click file in Explorer
2. Select "Copy as path"
3. Paste in PowerShell

### Use PowerShell ISE (Alternative)

If regular PowerShell doesn't work well:
1. Press `Win + R`
2. Type `powershell_ise`
3. Open the `.ps1` file
4. Press `F5` to run

### Set Default Directory

Create a profile to start in template directory:

```powershell
# Check if profile exists
Test-Path $PROFILE

# Create if doesn't exist
New-Item -Path $PROFILE -Type File -Force

# Edit profile
notepad $PROFILE

# Add this line:
Set-Location C:\path\to\exon-template-sfdc-demo

# Save and close
# Restart PowerShell
```

## 🔗 Useful Resources

- **Salesforce CLI Commands:** https://developer.salesforce.com/docs/atlas.en-us.sfdx_cli_reference.meta/sfdx_cli_reference/
- **PowerShell Basics:** https://learn.microsoft.com/en-us/powershell/scripting/overview
- **Salesforce Developer Org:** https://developer.salesforce.com/signup
- **Python for Windows:** https://www.python.org/downloads/windows/

## ❓ FAQ

**Q: Do I need Visual Studio?**
A: No, but VS Code with Salesforce Extension Pack is recommended.

**Q: Can I use Command Prompt instead of PowerShell?**
A: No, the scripts are PowerShell-specific. Use PowerShell.

**Q: Can I use WSL (Windows Subsystem for Linux)?**
A: Yes! In WSL, use the `.sh` scripts instead of `.ps1` scripts.

**Q: How much disk space needed?**
A: ~500MB for template, ~100-200MB per generated project.

**Q: Can I run multiple projects simultaneously?**
A: Yes, but each build takes 4-6 hours. Run them sequentially.

**Q: What if I close PowerShell during build?**
A: Use `.\resume.ps1 <path>` to continue from last checkpoint.

## 📞 Getting Help

If stuck:
1. Check this guide
2. Review error message carefully
3. Try troubleshooting steps above
4. Search error message on Google
5. Ask on Salesforce Stack Exchange: https://salesforce.stackexchange.com/

---

**Ready to start?** Run `.\start.ps1` and follow the prompts! 🚀
