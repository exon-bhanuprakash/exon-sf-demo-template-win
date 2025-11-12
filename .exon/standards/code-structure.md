# Exonpro Code Structure Standards - Salesforce Edition

## Project Organization Principles

### 1. SFDX Project Structure (Standard)

```
project-root/
├── force-app/
│   └── main/
│       └── default/
│           ├── lwc/                      # Lightning Web Components
│           │   ├── componentName/
│           │   │   ├── componentName.js
│           │   │   ├── componentName.html
│           │   │   ├── componentName.css
│           │   │   ├── componentName.js-meta.xml
│           │   │   └── __tests__/        # Jest tests (optional)
│           │   │       └── componentName.test.js
│           │   └── ... (more components)
│           │
│           ├── classes/                  # Apex classes
│           │   ├── AccountService.cls
│           │   ├── AccountService.cls-meta.xml
│           │   ├── AccountServiceTest.cls
│           │   ├── AccountServiceTest.cls-meta.xml
│           │   └── ... (more classes)
│           │
│           ├── triggers/                 # Apex triggers
│           │   ├── AccountTrigger.trigger
│           │   ├── AccountTrigger.trigger-meta.xml
│           │   └── ... (more triggers)
│           │
│           ├── objects/                  # Custom objects
│           │   ├── CustomObject__c/
│           │   │   ├── CustomObject__c.object-meta.xml
│           │   │   ├── fields/
│           │   │   │   ├── CustomField__c.field-meta.xml
│           │   │   │   └── ... (more fields)
│           │   │   ├── listViews/
│           │   │   ├── validationRules/
│           │   │   └── compactLayouts/
│           │   └── ... (more objects)
│           │
│           ├── tabs/                     # Custom tabs
│           ├── flexipages/               # Lightning pages
│           ├── applications/             # Lightning apps
│           ├── permissionsets/           # Permission sets
│           ├── profiles/                 # Profiles (limited use)
│           ├── flows/                    # Flows
│           ├── staticresources/          # Static resources
│           └── aura/                     # Aura components (legacy)
│
├── .exon/                               # Exonpro automation artifacts
├── config/                              # Scratch org configs
│   └── project-scratch-def.json
├── scripts/                             # Deployment/utility scripts
│   └── deploy.sh
├── .gitignore
├── sfdx-project.json                    # SFDX project config
├── package.json                         # For LWC dev/testing
├── jest.config.js                       # Jest config (optional)
└── README.md
```

### 2. Lightning Web Components Structure

#### Component Organization
```
lwc/
├── atoms/                               # Simple, reusable components
│   ├── button/
│   ├── input/
│   └── card/
│
├── molecules/                           # Composed components
│   ├── formGroup/
│   ├── searchBar/
│   └── dataTable/
│
├── organisms/                           # Feature components
│   ├── accountList/
│   ├── contactForm/
│   └── dashboard/
│
└── pages/                               # Full-page components
    ├── accountListPage/
    └── accountDetailPage/
```

#### LWC Component Files
```javascript
// componentName/componentName.js
import { LightningElement, api, track, wire } from 'lwc';
import { getRecord } from 'lightning/uiRecordApi';

export default class ComponentName extends LightningElement {
    // Public properties (decorated with @api)
    @api recordId;
    @api objectApiName;

    // Tracked properties (reactive)
    @track data = [];

    // Wire service (automatic data fetching)
    @wire(getRecord, { recordId: '$recordId', fields: FIELDS })
    wiredRecord({ error, data }) {
        if (data) {
            this.handleData(data);
        } else if (error) {
            this.handleError(error);
        }
    }

    // Lifecycle hooks
    connectedCallback() {
        // Component connected to DOM
    }

    disconnectedCallback() {
        // Component removed from DOM
    }

    // Event handlers
    handleClick(event) {
        // Handle user interaction
    }

    // Helper methods
    handleData(data) {
        // Process data
    }

    handleError(error) {
        // Handle error
    }
}
```

```html
<!-- componentName/componentName.html -->
<template>
    <lightning-card title="Component Title">
        <div class="slds-p-around_medium">
            <!-- Component content -->
            <lightning-button
                label="Click Me"
                onclick={handleClick}>
            </lightning-button>
        </div>
    </lightning-card>
</template>
```

```css
/* componentName/componentName.css */
.container {
    padding: 1rem;
}

.title {
    font-size: 1.5rem;
    font-weight: bold;
}
```

```xml
<!-- componentName/componentName.js-meta.xml -->
<?xml version="1.0" encoding="UTF-8"?>
<LightningComponentBundle xmlns="http://soap.sforce.com/2006/04/metadata">
    <apiVersion>61.0</apiVersion>
    <isExposed>true</isExposed>
    <targets>
        <target>lightning__AppPage</target>
        <target>lightning__RecordPage</target>
        <target>lightning__HomePage</target>
    </targets>
</LightningComponentBundle>
```

### 3. Apex Class Structure

#### Service Layer Pattern
```apex
// AccountService.cls
public with sharing class AccountService {

    /**
     * Get accounts by industry
     * @param industry The industry to filter by
     * @return List of accounts
     */
    public static List<Account> getAccountsByIndustry(String industry) {
        return AccountSelector.selectByIndustry(industry);
    }

    /**
     * Create new account
     * @param accountData Account data
     * @return Created account
     */
    public static Account createAccount(Account accountData) {
        // Validate
        validateAccount(accountData);

        // Insert
        insert accountData;

        return accountData;
    }

    /**
     * Validate account data
     */
    private static void validateAccount(Account acc) {
        if (String.isBlank(acc.Name)) {
            throw new IllegalArgumentException('Account name is required');
        }
    }
}
```

#### Selector Layer Pattern
```apex
// AccountSelector.cls
public with sharing class AccountSelector {

    /**
     * Select accounts by industry
     */
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

    /**
     * Select account by Id
     */
    public static Account selectById(Id accountId) {
        List<Account> accounts = [
            SELECT Id, Name, Industry, AnnualRevenue
            FROM Account
            WHERE Id = :accountId
            WITH SECURITY_ENFORCED
            LIMIT 1
        ];
        return accounts.isEmpty() ? null : accounts[0];
    }
}
```

#### Trigger Handler Pattern
```apex
// AccountTrigger.trigger
trigger AccountTrigger on Account (before insert, before update, after insert, after update) {
    AccountTriggerHandler handler = new AccountTriggerHandler();
    handler.run();
}
```

```apex
// AccountTriggerHandler.cls
public with sharing class AccountTriggerHandler extends TriggerHandler {

    protected override void beforeInsert() {
        AccountDomain.setDefaults((List<Account>)Trigger.new);
    }

    protected override void beforeUpdate() {
        AccountDomain.validateUpdates((List<Account>)Trigger.new, (Map<Id, Account>)Trigger.oldMap);
    }

    protected override void afterInsert() {
        AccountDomain.createRelatedRecords((List<Account>)Trigger.new);
    }

    protected override void afterUpdate() {
        AccountDomain.syncRelatedRecords((List<Account>)Trigger.new, (Map<Id, Account>)Trigger.oldMap);
    }
}
```

#### Test Class Pattern
```apex
// AccountServiceTest.cls
@isTest
private class AccountServiceTest {

    @TestSetup
    static void setup() {
        // Create test data
        Account testAccount = new Account(
            Name = 'Test Account',
            Industry = 'Technology'
        );
        insert testAccount;
    }

    @isTest
    static void testGetAccountsByIndustry() {
        // Given
        String industry = 'Technology';

        // When
        Test.startTest();
        List<Account> result = AccountService.getAccountsByIndustry(industry);
        Test.stopTest();

        // Then
        System.assertEquals(1, result.size(), 'Should return 1 account');
        System.assertEquals(industry, result[0].Industry, 'Industry should match');
    }

    @isTest
    static void testCreateAccount() {
        // Given
        Account newAccount = new Account(
            Name = 'New Test Account',
            Industry = 'Finance'
        );

        // When
        Test.startTest();
        Account result = AccountService.createAccount(newAccount);
        Test.stopTest();

        // Then
        System.assertNotEquals(null, result.Id, 'Account should be created');

        // Verify in database
        Account inserted = [SELECT Id, Name, Industry FROM Account WHERE Id = :result.Id];
        System.assertEquals('New Test Account', inserted.Name);
    }

    @isTest
    static void testBulkInsert() {
        // Given - create 200 accounts for bulk testing
        List<Account> accounts = new List<Account>();
        for (Integer i = 0; i < 200; i++) {
            accounts.add(new Account(
                Name = 'Bulk Test Account ' + i,
                Industry = 'Technology'
            ));
        }

        // When
        Test.startTest();
        insert accounts;
        Test.stopTest();

        // Then
        System.assertEquals(200, [SELECT COUNT() FROM Account WHERE Name LIKE 'Bulk Test Account%']);
    }
}
```

### 4. File Naming Conventions

#### Apex Classes
- **Classes**: PascalCase - `AccountService.cls`, `ContactTriggerHandler.cls`
- **Test Classes**: PascalCase + Test suffix - `AccountServiceTest.cls`
- **Naming patterns**:
  - Services: `{Object}Service.cls`
  - Selectors: `{Object}Selector.cls`
  - Trigger Handlers: `{Object}TriggerHandler.cls`
  - Domain classes: `{Object}Domain.cls`
  - Controllers (LWC): `{Object}Controller.cls`

#### LWC Components
- **Component folders**: camelCase - `accountList/`, `contactForm/`
- **Files**: Match folder name
  - `accountList.js`
  - `accountList.html`
  - `accountList.css`
  - `accountList.js-meta.xml`

#### Custom Objects & Fields
- **Objects**: PascalCase + `__c` suffix - `CustomObject__c`
- **Fields**: PascalCase + `__c` suffix - `CustomField__c`
- **Relationships**: Descriptive + `__c` - `ParentAccount__c`

### 5. API Route Organization (Apex REST)

```apex
// AccountRestService.cls
@RestResource(urlMapping='/accounts/*')
global with sharing class AccountRestService {

    @HttpGet
    global static List<Account> getAccounts() {
        RestRequest req = RestContext.request;
        String industry = req.params.get('industry');
        return AccountService.getAccountsByIndustry(industry);
    }

    @HttpPost
    global static Account createAccount(Account accountData) {
        return AccountService.createAccount(accountData);
    }

    @HttpPut
    global static Account updateAccount(Account accountData) {
        return AccountService.updateAccount(accountData);
    }

    @HttpDelete
    global static void deleteAccount() {
        RestRequest req = RestContext.request;
        String accountId = req.requestURI.substring(req.requestURI.lastIndexOf('/')+1);
        AccountService.deleteAccount(accountId);
    }
}
```

### 6. Custom Object Structure

#### Field Naming
- **Text fields**: PascalCase - `FirstName__c`, `EmailAddress__c`
- **Lookup fields**: Object name + `__c` - `Account__c`, `ParentContact__c`
- **Checkbox fields**: `Is` or `Has` prefix - `IsActive__c`, `HasAccess__c`
- **Date fields**: Past tense or noun - `CreatedDate__c`, `ExpirationDate__c`

#### Standard Fields (Auto-created)
Every custom object has:
- `Id` - Unique identifier
- `Name` - Auto-number or text
- `CreatedById`, `CreatedDate` - Audit fields
- `LastModifiedById`, `LastModifiedDate` - Audit fields
- `OwnerId` - Record owner

### 7. Testing Structure (Optional for Demo)

```
tests/                                   # Optional testing directory
├── apex/
│   ├── AccountServiceTest.cls
│   ├── AccountSelectorTest.cls
│   └── AccountTriggerHandlerTest.cls
│
└── lwc/
    └── accountList/
        └── __tests__/
            └── accountList.test.js
```

### 8. Configuration Files Location

```
project-root/
├── .exon/                               # Exonpro automation (DO NOT modify manually)
│
├── .vscode/                             # VS Code settings (optional)
│   └── settings.json
│
├── config/                              # Org configurations
│   └── project-scratch-def.json
│
├── .gitignore
├── .prettierrc                          # Code formatting
├── .eslintrc.json                       # Linting (LWC)
├── sfdx-project.json                    # SFDX config
├── package.json                         # npm packages (for LWC testing)
└── README.md
```

### 9. Import Organization

#### LWC Imports
```javascript
// 1. Lightning platform modules
import { LightningElement, api, track, wire } from 'lwc';
import { getRecord, updateRecord } from 'lightning/uiRecordApi';
import { ShowToastEvent } from 'lightning/platformShowToastEvent';

// 2. Apex methods
import getAccounts from '@salesforce/apex/AccountController.getAccounts';
import createAccount from '@salesforce/apex/AccountController.createAccount';

// 3. Schema references
import ACCOUNT_OBJECT from '@salesforce/schema/Account';
import NAME_FIELD from '@salesforce/schema/Account.Name';

// 4. Labels
import LABEL_SAVE from '@salesforce/label/c.Save';
import LABEL_CANCEL from '@salesforce/label/c.Cancel';

// 5. Static resources
import LOGO from '@salesforce/resourceUrl/CompanyLogo';

// 6. User/org info
import userId from '@salesforce/user/Id';
import isGuest from '@salesforce/user/isGuest';
```

#### Apex Imports
```apex
// No explicit imports in Apex
// All classes in same namespace are automatically available
```

### 10. Environment-Specific Code

**Always:**
```apex
// Use Custom Settings or Custom Metadata for config
Integration_Config__c config = Integration_Config__c.getInstance();
String apiUrl = config.API_URL__c;

// Or Custom Metadata
List<API_Config__mdt> configs = [SELECT API_URL__c FROM API_Config__mdt WHERE DeveloperName = 'Production'];
```

**Never:**
```apex
// DON'T hardcode environment checks
String apiUrl = URL.getSalesforceBaseUrl().toExternalForm().contains('sandbox') ?
    'https://test-api.com' : 'https://api.com';
```

### 11. sfdx-project.json Configuration

```json
{
    "packageDirectories": [
        {
            "path": "force-app",
            "default": true
        }
    ],
    "name": "project-name",
    "namespace": "",
    "sfdcLoginUrl": "https://login.salesforce.com",
    "sourceApiVersion": "61.0"
}
```

### 12. Folder Structure Rules

**DO:**
- Keep related components together (e.g., service + selector + trigger handler)
- Use naming conventions consistently
- Separate test classes clearly
- Use sub-folders in `objects/` for field definitions

**DON'T:**
- Mix Apex classes and LWC in same conceptual folder (they're separate by SFDX structure)
- Use Aura components for new development
- Overuse triggers (one per object max)

**DEMO PROJECTS - Custom Objects Strategy:**
- Always create custom objects to showcase Salesforce development capabilities
- Design domain-specific data models (e.g., for CRM: Customer__c, Order__c, Product__c instead of Account, Opportunity, PricebookEntry)
- Include relationships, validation rules, and formula fields to demonstrate platform features
- Even if standard objects could work, create custom ones for better demo visibility

### 13. Metadata Type Organization

```
force-app/main/default/
├── classes/              # Apex classes
├── triggers/             # Apex triggers
├── lwc/                  # Lightning Web Components
├── aura/                 # Aura components (avoid for new dev)
├── objects/              # Custom objects and fields
├── tabs/                 # Custom tabs
├── flexipages/           # Lightning pages
├── applications/         # Lightning apps
├── permissionsets/       # Permission sets
├── profiles/             # Profiles (use sparingly)
├── layouts/              # Page layouts
├── flows/                # Flows
├── email/                # Email templates
├── reports/              # Reports
├── dashboards/           # Dashboards
└── staticresources/      # Static resources
```

## Demo vs Production Structure

### Demo Mode
- Flat class structure (no deep packages)
- Minimal separation of concerns
- Test classes optional
- Basic error handling

### Production Mode
- Layered architecture (Service, Selector, Domain, Trigger Handler)
- Full test coverage
- Comprehensive error handling
- Governor limit optimization

### Transition Checklist
- [ ] Refactor into service/selector/domain layers
- [ ] Add trigger handler framework
- [ ] Create test classes for all Apex
- [ ] Add LWC Jest tests
- [ ] Implement error handling
- [ ] Add logging
- [ ] Optimize SOQL queries
- [ ] Bulkify trigger logic
