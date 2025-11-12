# Exonpro Hosting & Deployment Standards - Salesforce Edition

## Deployment Principles

### 1. Salesforce Org Types

#### Developer Org (FREE - For Demos)
**Use for:**
- Personal development
- Learning and experimentation
- Demo projects
- POCs and prototypes

**Characteristics:**
- Free forever
- Full Salesforce functionality
- Limited data storage (5MB)
- No production use
- Never expires (with regular login)

**Get one:** https://developer.salesforce.com/signup

#### Sandbox (PAID - For Production Development)
**Use for:**
- Development for production orgs
- Testing before production deployment
- UAT (User Acceptance Testing)
- Training environments

**Types:**
- Developer Sandbox: Development and testing
- Developer Pro Sandbox: More storage, longer refresh
- Partial Copy Sandbox: Sample of production data
- Full Sandbox: Complete copy of production

#### Production Org (PAID)
**Use for:**
- Live business operations
- Real user data
- Customer-facing applications

**Editions:**
- Essentials: Small businesses (up to 10 users)
- Professional: Growing businesses
- Enterprise: Large organizations
- Unlimited: Maximum features and support

---

## 2. Deployment Tools & Commands

### Salesforce CLI (sf) - PRIMARY TOOL

#### Installation
```bash
# Install via npm (cross-platform)
npm install -g @salesforce/cli

# Verify installation
sf --version

# Update CLI
sf update
```

#### Common Commands
```bash
# Login to org
sf org login web --alias DevOrg
sf org login web --instance-url https://test.salesforce.com --alias Sandbox  # Sandbox

# View connected orgs
sf org list

# Set default org
sf config set target-org DevOrg

# Open org in browser
sf org open

# Deploy source to org
sf project deploy start

# Deploy specific metadata
sf project deploy start --metadata ApexClass:AccountService
sf project deploy start --source-dir force-app/main/default/lwc/accountList

# Deploy and run tests
sf project deploy start --test-level RunLocalTests

# Retrieve metadata from org
sf project retrieve start

# Retrieve specific metadata
sf project retrieve start --metadata ApexClass:AccountService

# Run Apex tests
sf apex run test --test-level RunLocalTests --wait 10

# Run specific test class
sf apex run test --class-names AccountServiceTest --wait 5

# Execute anonymous Apex
sf apex run --file scripts/setup.apex

# View logs
sf apex log list
sf apex log get --log-id 07L...

# Create scratch org (for enterprise orgs with Dev Hub)
sf org create scratch --definition-file config/project-scratch-def.json --alias MyScratchOrg
```

### VS Code with Salesforce Extension Pack

**Extensions to install:**
- Salesforce Extension Pack
- Salesforce CLI Integration
- Apex PMD (code quality)
- Prettier Apex (code formatting)

**Common Operations:**
- `Cmd/Ctrl + Shift + P` → "SFDX: Deploy Source to Org"
- `Cmd/Ctrl + Shift + P` → "SFDX: Retrieve Source from Org"
- `Cmd/Ctrl + Shift + P` → "SFDX: Create Apex Class"
- `Cmd/Ctrl + Shift + P` → "SFDX: Create Lightning Web Component"

---

## 3. Deployment Workflow

### For Demo Projects (Developer Org)

#### Initial Setup
```bash
# 1. Login to developer org
sf org login web --alias DevOrg

# 2. Initialize SFDX project (if not already done)
sf project generate --name my-project

# 3. Set default org
sf config set target-org DevOrg

# 4. Open org to verify connection
sf org open
```

#### Development Workflow
```bash
# 1. Create components (Apex, LWC, etc.)
#    - Use VS Code or CLI to create files
#    - Write code in force-app/main/default/

# 2. Deploy to org
sf project deploy start

# 3. Test manually in org
sf org open

# 4. Make changes, redeploy
sf project deploy start

# 5. Commit to Git
git add .
git commit -m "feat: Add account list component"
git push
```

#### Quick Deploy (Single Component)
```bash
# Deploy single Apex class
sf project deploy start --metadata ApexClass:AccountService

# Deploy single LWC component
sf project deploy start --source-dir force-app/main/default/lwc/accountList

# Deploy custom object
sf project deploy start --metadata CustomObject:MyObject__c
```

### For Production Projects (Sandbox → Production)

#### Development in Sandbox
```bash
# 1. Login to sandbox
sf org login web --instance-url https://test.salesforce.com --alias DevSandbox

# 2. Develop and test in sandbox
sf project deploy start
sf apex run test --test-level RunLocalTests

# 3. Retrieve changes from sandbox
sf project retrieve start

# 4. Commit to Git
git add .
git commit -m "feat: Add feature"
git push
```

#### Deploy to Production
```bash
# 1. Login to production
sf org login web --alias Production

# 2. Validate deployment (don't deploy, just check)
sf project deploy start --dry-run --test-level RunLocalTests

# 3. Deploy to production (requires 75% test coverage)
sf project deploy start --test-level RunLocalTests

# 4. Monitor deployment
sf project deploy report

# 5. Cancel deployment if needed
sf project deploy cancel
```

---

## 4. Metadata Types to Deploy

### Core Metadata
```
force-app/main/default/
├── lwc/                      # Lightning Web Components
├── classes/                  # Apex classes
├── triggers/                 # Apex triggers
├── objects/                  # Custom objects and fields
├── tabs/                     # Custom tabs
├── flexipages/               # Lightning pages
├── applications/             # Lightning apps
├── permissionsets/           # Permission sets
├── flows/                    # Flows
├── staticresources/          # Static resources
└── aura/                     # Aura components (legacy)
```

### Deployment Order (if manual)
1. Custom Objects and Fields
2. Apex Classes (non-dependent)
3. Apex Triggers
4. LWC Components
5. Lightning Pages
6. Permission Sets
7. Flows

**Note:** `sf project deploy start` handles dependencies automatically.

---

## 5. Environment Management

### Environment Variables

**sfdx-project.json:**
```json
{
    "packageDirectories": [
        {
            "path": "force-app",
            "default": true
        }
    ],
    "name": "my-project",
    "namespace": "",
    "sfdcLoginUrl": "https://login.salesforce.com",
    "sourceApiVersion": "61.0"
}
```

**config/project-scratch-def.json** (for scratch orgs):
```json
{
    "orgName": "My Demo Org",
    "edition": "Developer",
    "features": ["EnableSetPasswordInApi"],
    "settings": {
        "lightningExperienceSettings": {
            "enableS1DesktopEnabled": true
        },
        "securitySettings": {
            "passwordPolicies": {
                "enableSetPasswordInApi": true
            }
        }
    }
}
```

### Org Aliases
```bash
# Set aliases for easy switching
sf org login web --alias DevOrg
sf org login web --alias UAT --instance-url https://test.salesforce.com
sf org login web --alias Production

# Switch between orgs
sf config set target-org DevOrg
sf config set target-org Production

# View all orgs
sf org list
```

---

## 6. CI/CD Pipeline (Production)

### GitHub Actions Example
```yaml
# .github/workflows/deploy.yml
name: Deploy to Salesforce

on:
  push:
    branches: [dev]

jobs:
  deploy:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3

      - name: Install Salesforce CLI
        run: npm install -g @salesforce/cli

      - name: Authorize Salesforce Org
        run: |
          echo "${{ secrets.SFDX_AUTH_URL }}" > auth.txt
          sf org login sfdx-url --sfdx-url-file auth.txt --alias CICDOrg

      - name: Deploy Source
        run: sf project deploy start --test-level RunLocalTests

      - name: Run Tests
        run: sf apex run test --test-level RunLocalTests --wait 10
```

### Get SFDX Auth URL (for CI/CD)
```bash
# Login to org
sf org login web --alias DevOrg

# Get auth URL (for CI/CD secrets)
sf org display --target-org DevOrg --verbose

# Copy the "Sfdx Auth Url" value to GitHub secrets as SFDX_AUTH_URL
```

---

## 7. Deployment Checklist

### Before Deployment
- [ ] All components created in source format
- [ ] Code committed to Git
- [ ] Org connected via `sf org login`
- [ ] Default org set (`sf config set target-org`)
- [ ] No syntax errors in code
- [ ] Manual testing completed

### For Production Deployment (Additional)
- [ ] 75%+ Apex test coverage achieved
- [ ] All tests passing (`sf apex run test`)
- [ ] Deployment validated (`--dry-run`)
- [ ] Backup of production metadata
- [ ] Change set documented
- [ ] Rollback plan prepared
- [ ] Stakeholders notified

### After Deployment
- [ ] Verify deployment success
- [ ] Test critical functionality in org
- [ ] Check logs for errors
- [ ] Update documentation
- [ ] Notify users (for production)

---

## 8. Rollback Procedures

### Quick Rollback (Developer Org)
```bash
# 1. Checkout previous Git commit
git log  # Find previous commit
git checkout <previous-commit-hash>

# 2. Redeploy previous version
sf project deploy start

# 3. Return to current branch
git checkout dev
```

### Production Rollback
```bash
# Option 1: Deploy previous version from Git
git checkout <previous-release-tag>
sf project deploy start --target-org Production

# Option 2: Delete problematic metadata
sf project delete source --metadata ApexClass:ProblematicClass

# Option 3: Use change sets (manual in UI)
# Setup > Deployment > Inbound Change Sets
```

---

## 9. Deployment Best Practices

### DO:
- Use source format (SFDX) for all projects
- Commit frequently to Git
- Deploy small, incremental changes
- Test in sandbox before production
- Use meaningful commit messages
- Keep org aliases consistent
- Document deployment steps

### DON'T:
- Deploy untested code to production
- Skip test execution in production deployments
- Use destructive changes without backup
- Deploy during business hours (production)
- Commit secrets or credentials to Git
- Deploy without version control

---

## 10. Common Deployment Errors

### Insufficient Test Coverage
**Error:** "Average test coverage across all Apex Classes and Triggers is 74%, at least 75% test coverage is required"

**Solution:**
```bash
# Check current coverage
sf apex get test --target-org DevOrg --code-coverage

# Write more test classes
# Redeploy with tests
sf project deploy start --test-level RunLocalTests
```

### Metadata API Error
**Error:** "Component <X> is not available for this organization"

**Solution:**
- Check that metadata type is supported in org edition
- Verify API version compatibility
- Check feature licensing

### Deployment Lock
**Error:** "Another deployment is in progress"

**Solution:**
```bash
# Wait for other deployment to finish, or
# Cancel if you initiated it
sf project deploy cancel --target-org Production
```

---

## 11. Demo Deployment Notes

For demo projects:
1. **Use**: Developer Org (free)
2. **Deploy**: Via `sf project deploy start`
3. **Test**: Manual testing only
4. **Version Control**: Git (dev branch)
5. **CI/CD**: Skip for demos

**To convert to production:**
1. Set up sandboxes
2. Implement automated testing
3. Configure CI/CD pipeline
4. Add deployment validation
5. Document rollback procedures
6. Plan production deployment schedule

---

## 12. Resources

**Salesforce CLI:**
- Documentation: https://developer.salesforce.com/docs/atlas.en-us.sfdx_cli_reference.meta/sfdx_cli_reference/cli_reference_top.htm
- sf commands: https://developer.salesforce.com/docs/atlas.en-us.sfdx_cli_reference.meta/sfdx_cli_reference/cli_reference_unified.htm

**Deployment:**
- Metadata API: https://developer.salesforce.com/docs/atlas.en-us.api_meta.meta/api_meta/
- DevOps Center: https://help.salesforce.com/s/articleView?id=sf.devops_center_overview.htm

**Tools:**
- VS Code Salesforce Extension Pack
- Salesforce CLI
- Git for version control
