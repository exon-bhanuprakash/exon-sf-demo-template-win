# CLAUDE.md - Salesforce LWC + Apex Stack

This file provides guidance to Claude Code when working with this Salesforce application.

## Tech Stack

- **Platform**: Salesforce (Developer Org for demos)
- **Frontend**: Lightning Web Components (LWC) - JavaScript ES6+, HTML, CSS
- **Backend**: Apex - Business logic, triggers, SOQL
- **Database**: Salesforce Objects (Custom objects only for demo - avoid standard objects)
- **API**: REST/SOAP, Platform Events
- **Auth**: Salesforce Identity (OAuth, SSO)
- **File Storage**: Files, Attachments, Content
- **Deployment**: Salesforce CLI (sf commands)
- **Version Control**: SFDX source format in Git
- **IDE**: VS Code with Salesforce Extension Pack

## DEMO MODE - Custom Objects Strategy

⚠️ **IMPORTANT for Demo Projects:**
- Always create custom objects to showcase Salesforce development capabilities
- Do NOT use standard objects (Account, Contact, Opportunity, Lead, Case, etc.)
- Design domain-specific custom objects with __c suffix
- Examples:
  - Instead of Account → Customer__c, Client__c, Vendor__c
  - Instead of Contact → Person__c, Member__c, Participant__c
  - Instead of Opportunity → Deal__c, Order__c, Sale__c
- Include relationships, validation rules, and formula fields to demonstrate platform features
- This makes the demo more impressive and shows custom object creation skills

## Project Structure

```
/
├── force-app/
│   └── main/
│       └── default/
│           ├── lwc/                      # Lightning Web Components
│           │   ├── accountList/         # Component folder
│           │   │   ├── accountList.js
│           │   │   ├── accountList.html
│           │   │   ├── accountList.css
│           │   │   ├── accountList.js-meta.xml
│           │   │   └── __tests__/       # Jest tests (optional)
│           │   └── contactForm/
│           │
│           ├── classes/                  # Apex classes
│           │   ├── AccountService.cls
│           │   ├── AccountService.cls-meta.xml
│           │   ├── AccountController.cls  # LWC controller
│           │   ├── AccountSelector.cls    # SOQL queries
│           │   ├── AccountTriggerHandler.cls
│           │   └── AccountServiceTest.cls # Test class
│           │
│           ├── triggers/                 # Apex triggers
│           │   ├── AccountTrigger.trigger
│           │   └── AccountTrigger.trigger-meta.xml
│           │
│           ├── objects/                  # Custom objects
│           │   ├── CustomObject__c/
│           │   │   ├── CustomObject__c.object-meta.xml
│           │   │   └── fields/
│           │   │       ├── CustomField__c.field-meta.xml
│           │   │       └── AnotherField__c.field-meta.xml
│           │   └── ...
│           │
│           ├── tabs/                     # Custom tabs
│           ├── flexipages/               # Lightning pages
│           ├── applications/             # Lightning apps
│           ├── permissionsets/           # Permission sets
│           ├── layouts/                  # Page layouts
│           ├── flows/                    # Flows
│           └── staticresources/          # Static resources
│
├── config/
│   └── project-scratch-def.json         # Scratch org config
│
├── scripts/
│   └── setup.apex                       # Setup scripts
│
├── .exon/                               # Exonpro automation
├── .gitignore
├── sfdx-project.json                    # SFDX config
├── package.json                         # For LWC testing (optional)
└── README.md
```

## Development Commands

### Setup (First Time)
```bash
# Install Salesforce CLI
npm install -g @salesforce/cli

# Verify installation
sf --version

# Login to Developer Org
sf org login web --alias DevOrg

# Set as default
sf config set target-org DevOrg

# Open org in browser
sf org open
```

### Development Workflow
```bash
# Deploy all source to org
sf project deploy start

# Deploy specific component
sf project deploy start --metadata ApexClass:AccountService
sf project deploy start --source-dir force-app/main/default/lwc/accountList

# Retrieve metadata from org
sf project retrieve start

# Open org
sf org open

# View logs
sf apex log list
sf apex log get --log-id 07L...
```

### Testing (Optional for Demo)
```bash
# Run all Apex tests
sf apex run test --test-level RunLocalTests --wait 10

# Run specific test class
sf apex run test --class-names AccountServiceTest --wait 5

# Get code coverage
sf apex get test --code-coverage
```

### Execute Anonymous Apex
```bash
# Run setup script
sf apex run --file scripts/setup.apex

# Interactive
sf apex run
# Then paste Apex code
```

## Architecture Patterns

### Lightning Web Component Structure

**Basic LWC Component:**
```javascript
// accountList.js
import { LightningElement, wire } from 'lwc';
import getAccounts from '@salesforce/apex/AccountController.getAccounts';

export default class AccountList extends LightningElement {
    accounts;
    error;

    @wire(getAccounts)
    wiredAccounts({ error, data }) {
        if (data) {
            this.accounts = data;
            this.error = undefined;
        } else if (error) {
            this.error = error;
            this.accounts = undefined;
        }
    }
}
```

```html
<!-- accountList.html -->
<template>
    <lightning-card title="Accounts" icon-name="standard:account">
        <div class="slds-p-around_medium">
            <template if:true={accounts}>
                <template for:each={accounts} for:item="account">
                    <div key={account.Id} class="slds-box slds-m-bottom_small">
                        <p>{account.Name}</p>
                        <p class="slds-text-color_weak">{account.Industry}</p>
                    </div>
                </template>
            </template>
            <template if:true={error}>
                <p class="slds-text-color_error">{error.body.message}</p>
            </template>
        </div>
    </lightning-card>
</template>
```

### Apex Service Layer Pattern

**Controller (for LWC):**
```apex
// AccountController.cls
public with sharing class AccountController {

    @AuraEnabled(cacheable=true)
    public static List<Account> getAccounts(String industry) {
        return AccountService.getAccountsByIndustry(industry);
    }

    @AuraEnabled
    public static Id createAccount(String name, String industry) {
        Account acc = new Account(Name = name, Industry = industry);
        return AccountService.createAccount(acc).Id;
    }
}
```

**Service Layer:**
```apex
// AccountService.cls
public with sharing class AccountService {

    public static List<Account> getAccountsByIndustry(String industry) {
        return AccountSelector.selectByIndustry(industry);
    }

    public static Account createAccount(Account acc) {
        // Validation
        if (String.isBlank(acc.Name)) {
            throw new IllegalArgumentException('Account name is required');
        }

        // Insert
        insert acc;
        return acc;
    }
}
```

**Selector Layer (SOQL):**
```apex
// AccountSelector.cls
public with sharing class AccountSelector {

    public static List<Account> selectByIndustry(String industry) {
        return [
            SELECT Id, Name, Industry, AnnualRevenue
            FROM Account
            WHERE Industry = :industry
            WITH SECURITY_ENFORCED
            ORDER BY Name
            LIMIT 200
        ];
    }
}
```

### Trigger Handler Pattern

**Trigger:**
```apex
// AccountTrigger.trigger
trigger AccountTrigger on Account (before insert, before update, after insert, after update) {
    new AccountTriggerHandler().run();
}
```

**Handler:**
```apex
// AccountTriggerHandler.cls
public with sharing class AccountTriggerHandler extends TriggerHandler {

    protected override void beforeInsert() {
        // Set defaults
        for (Account acc : (List<Account>)Trigger.new) {
            if (String.isBlank(acc.Industry)) {
                acc.Industry = 'Other';
            }
        }
    }

    protected override void afterInsert() {
        // Create related records
        List<Contact> contacts = new List<Contact>();
        for (Account acc : (List<Account>)Trigger.new) {
            contacts.add(new Contact(
                FirstName = 'Primary',
                LastName = 'Contact',
                AccountId = acc.Id
            ));
        }
        if (!contacts.isEmpty()) {
            insert contacts;
        }
    }
}
```

## Deployment to Salesforce

### Initial Setup
```bash
# 1. Create Developer Org (if don't have one)
# Go to: https://developer.salesforce.com/signup

# 2. Login
sf org login web --alias DevOrg

# 3. Deploy project
sf project deploy start

# 4. Open org
sf org open
```

### Development Workflow
```bash
# Make changes to code
# Deploy
sf project deploy start

# Test in org
sf org open

# Commit to Git
git add .
git commit -m "feat: Add account list component"
git push
```

### Deployment Script (Optional)
```bash
#!/bin/bash
# scripts/deploy.sh

set -e

echo "Deploying to Salesforce..."

# Deploy source
sf project deploy start --target-org DevOrg

# Run tests (optional for demo)
# sf apex run test --test-level RunLocalTests --wait 10

echo "Deployment complete!"

# Open org
sf org open --target-org DevOrg
```

## Environment Configuration

### sfdx-project.json
```json
{
    "packageDirectories": [
        {
            "path": "force-app",
            "default": true
        }
    ],
    "name": "{{PROJECT_NAME}}",
    "namespace": "",
    "sfdcLoginUrl": "https://login.salesforce.com",
    "sourceApiVersion": "61.0"
}
```

### .gitignore (for Salesforce)
```.gitignore
# Salesforce
.sfdx/
.sf/
*.dup

# Logs
*.log

# OS
.DS_Store
Thumbs.db

# IDE
.vscode/
.idea/
*.swp

# Dependencies (if using npm for LWC testing)
node_modules/
coverage/

# Environment
.env
.env.local
```

## Testing (Optional for Demo)

### Apex Test Class
```apex
// AccountServiceTest.cls
@isTest
private class AccountServiceTest {

    @TestSetup
    static void setup() {
        insert new Account(Name = 'Test Account', Industry = 'Technology');
    }

    @isTest
    static void testGetAccountsByIndustry() {
        Test.startTest();
        List<Account> accounts = AccountService.getAccountsByIndustry('Technology');
        Test.stopTest();

        System.assertEquals(1, accounts.size());
        System.assertEquals('Technology', accounts[0].Industry);
    }

    @isTest
    static void testCreateAccount() {
        Account acc = new Account(Name = 'New Account', Industry = 'Finance');

        Test.startTest();
        Account result = AccountService.createAccount(acc);
        Test.stopTest();

        System.assertNotEquals(null, result.Id);
        Account inserted = [SELECT Name FROM Account WHERE Id = :result.Id];
        System.assertEquals('New Account', inserted.Name);
    }
}
```

## Monitoring & Debugging

### Debug Logs
```bash
# Enable debug logs for your user
# Setup > Debug Logs > New > Select your user

# View logs
sf apex log list
sf apex log get --log-id 07L...

# Tail logs (real-time)
sf apex log tail
```

### Developer Console
- Open: `sf org open`, then Setup > Developer Console
- Execute Anonymous Apex
- Query data with SOQL
- View logs
- Run tests

### VS Code Debugging
- Set breakpoints in Apex code
- Use Apex Replay Debugger
- View variable values
- Step through code

## Common Commands Quick Reference

```bash
# Org Management
sf org login web --alias MyOrg
sf org list
sf org open
sf config set target-org MyOrg

# Deployment
sf project deploy start
sf project deploy start --metadata ApexClass:MyClass
sf project retrieve start

# Testing
sf apex run test --test-level RunLocalTests
sf apex run test --class-names MyTestClass

# Logs
sf apex log list
sf apex log get --log-id 07L...

# Execute Apex
sf apex run --file script.apex

# Create Metadata
# Use VS Code: Cmd/Ctrl + Shift + P → "SFDX: Create Apex Class"
# Use VS Code: Cmd/Ctrl + Shift + P → "SFDX: Create Lightning Web Component"
```

## Important Notes for Demo Projects

### DO (Demo):
- Use Developer Org (free)
- Deploy with `sf project deploy start`
- Manual testing only
- Skip comprehensive test classes
- Use platform defaults for security
- Commit frequently to Git

### DON'T (Demo):
- Don't implement full test coverage (save for production)
- Don't optimize for governor limits (unless testing bulk)
- Don't implement field-level security
- Don't configure sharing rules
- Don't set up CI/CD (unless specifically needed)

### Converting Demo to Production:
1. Write Apex test classes (75%+ coverage)
2. Add LWC Jest tests for complex components
3. Implement field-level security
4. Configure sharing rules
5. Optimize for governor limits (bulkify code)
6. Set up sandboxes
7. Configure CI/CD pipeline
8. Add monitoring and logging

## Resources

**Salesforce Documentation:**
- LWC: https://developer.salesforce.com/docs/component-library/documentation/en/lwc
- Apex: https://developer.salesforce.com/docs/atlas.en-us.apexcode.meta/apexcode/
- SOQL: https://developer.salesforce.com/docs/atlas.en-us.soql_sosl.meta/soql_sosl/
- Trailhead: https://trailhead.salesforce.com/

**Tools:**
- Salesforce CLI: https://developer.salesforce.com/tools/sfdxcli
- VS Code Extensions: Salesforce Extension Pack
- Developer Console: In Salesforce org
- Workbench: https://workbench.developerforce.com/

**Community:**
- Salesforce Stack Exchange: https://salesforce.stackexchange.com/
- Trailblazer Community: https://trailblazer.salesforce.com/
- Salesforce Developers: https://developer.salesforce.com/forums
