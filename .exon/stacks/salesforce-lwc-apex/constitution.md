# Salesforce LWC + Apex Constitution

## Architectural Principles

### 1. Platform-Native Design
- Leverage Salesforce platform capabilities (built-in security, scalability, etc.)
- Use Lightning Data Service where possible (automatic caching, offline support)
- Prefer declarative before programmatic (Flows before Apex when appropriate)
- Use platform events for asynchronous communication
- **DEMO PROJECTS**: Always create custom objects to showcase development capabilities (even if standard objects exist)

### 2. Component-Based Architecture (LWC)
- **Atomic Design**: Atoms (buttons, inputs) → Molecules (form groups) → Organisms (feature components)
- **Single Responsibility**: Each component does one thing well
- **Reusability**: Build generic components, make specific through properties
- **Communication**: Use events for parent-child and Lightning Message Service for siblings
- **Composition**: Prefer composition over inheritance

### 3. Service Layer Pattern (Apex)
- **Controller**: Thin layer for LWC, only @AuraEnabled methods
- **Service**: Business logic, validation, orchestration
- **Selector**: SOQL queries, data access
- **Domain**: Record manipulation, defaults, calculations
- **Trigger Handler**: Centralized trigger logic

### 4. Data Access Patterns
- **SOQL Optimization**: Query outside loops, selective queries, limit results
- **Bulkification**: Handle 200+ records in all operations
- **Security**: Use WITH SECURITY_ENFORCED, `with sharing` classes
- **Caching**: Lightning Data Service for automatic caching
- **Lazy Loading**: Load data on-demand, not upfront

### 5. Governor Limit Awareness
- **SOQL**: Max 100 queries per transaction
- **DML**: Max 150 statements per transaction
- **Heap Size**: 6 MB synchronous, 12 MB asynchronous
- **CPU Time**: 10,000 ms synchronous, 60,000 ms asynchronous
- **Bulkify**: Design for 200 records minimum
- **Async**: Use Future, Queueable, Batch for heavy operations

## Code Organization Patterns

### Lightning Web Component Patterns

#### 1. Wire Service Pattern (Preferred)
```javascript
import { LightningElement, wire } from 'lwc';
import { getRecord } from 'lightning/uiRecordApi';

export default class MyComponent extends LightningElement {
    @wire(getRecord, { recordId: '$recordId', fields })
    record;
}
```

#### 2. Imperative Apex Call Pattern
```javascript
import { LightningElement } from 'lwc';
import getAccounts from '@salesforce/apex/AccountController.getAccounts';

export default class MyComponent extends LightningElement {
    async loadAccounts() {
        try {
            this.accounts = await getAccounts({ industry: 'Technology' });
        } catch (error) {
            this.handleError(error);
        }
    }
}
```

#### 3. Event Communication Pattern
```javascript
// Child component - dispatch event
this.dispatchEvent(new CustomEvent('accountselect', {
    detail: { accountId: this.accountId }
}));

// Parent component - handle event
<template>
    <c-account-list onaccountselect={handleAccountSelect}></c-account-list>
</template>
```

### Apex Patterns

#### 1. Service Layer Pattern
```apex
// Controller - thin layer
public with sharing class AccountController {
    @AuraEnabled(cacheable=true)
    public static List<Account> getAccounts(String industry) {
        return AccountService.getAccountsByIndustry(industry);
    }
}

// Service - business logic
public with sharing class AccountService {
    public static List<Account> getAccountsByIndustry(String industry) {
        return AccountSelector.selectByIndustry(industry);
    }

    public static Account createAccount(Account acc) {
        validateAccount(acc);
        insert acc;
        return acc;
    }

    private static void validateAccount(Account acc) {
        if (String.isBlank(acc.Name)) {
            throw new IllegalArgumentException('Name required');
        }
    }
}

// Selector - data access
public with sharing class AccountSelector {
    public static List<Account> selectByIndustry(String industry) {
        return [
            SELECT Id, Name, Industry
            FROM Account
            WHERE Industry = :industry
            WITH SECURITY_ENFORCED
            LIMIT 200
        ];
    }
}
```

#### 2. Trigger Handler Pattern
```apex
// Trigger - one per object
trigger AccountTrigger on Account (before insert, after insert) {
    new AccountTriggerHandler().run();
}

// Handler - extends base
public with sharing class AccountTriggerHandler extends TriggerHandler {
    protected override void beforeInsert() {
        AccountDomain.setDefaults((List<Account>)Trigger.new);
    }

    protected override void afterInsert() {
        AccountDomain.createRelatedRecords((List<Account>)Trigger.new);
    }
}

// Domain - record manipulation
public with sharing class AccountDomain {
    public static void setDefaults(List<Account> accounts) {
        for (Account acc : accounts) {
            if (String.isBlank(acc.Industry)) {
                acc.Industry = 'Other';
            }
        }
    }

    public static void createRelatedRecords(List<Account> accounts) {
        List<Contact> contacts = new List<Contact>();
        for (Account acc : accounts) {
            contacts.add(new Contact(
                FirstName = 'Primary',
                LastName = 'Contact',
                AccountId = acc.Id
            ));
        }
        insert contacts;
    }
}
```

## Design Patterns by Use Case

### 1. List View (Accounts, Contacts, etc.)
- Use Lightning Datatable component
- Wire service for data loading
- Pagination for large datasets
- Inline editing where appropriate
- Filter and search capabilities

### 2. Record Detail View
- Use Lightning Record Form (simplest)
- Or Lightning Record View Form + Edit Form (custom layout)
- Or build custom with field-level control
- Display related lists
- Quick actions

### 3. Create/Edit Forms
- Lightning Record Edit Form (fastest)
- Custom forms with lightning-input components
- Client-side validation
- Server-side validation in Apex
- Success/error toast messages

### 4. Search Functionality
- SOSL for cross-object search
- SOQL for single-object search
- Typeahead/autocomplete with debouncing
- Result highlighting
- Recent items

### 5. Bulk Operations
- Process in batches of 200
- Use Queueable or Batch Apex for large datasets
- Progress indicators
- Error handling per record
- Rollback on failure (transaction management)

## Security Patterns

### 1. Sharing Rules
```apex
// Enforce sharing rules
public with sharing class AccountService { }

// Bypass sharing (use carefully)
public without sharing class SystemProcessService { }

// Inherit from caller
public inherited sharing class HelperClass { }
```

### 2. Field-Level Security
```apex
// WITH SECURITY_ENFORCED (recommended)
List<Account> accounts = [
    SELECT Id, Name
    FROM Account
    WITH SECURITY_ENFORCED
];

// Security.stripInaccessible()
SObjectAccessDecision decision = Security.stripInaccessible(
    AccessType.READABLE,
    [SELECT Id, Name FROM Account]
);
```

### 3. Object-Level Security
```apex
if (Schema.sObjectType.Account.isCreateable()) {
    insert accounts;
}

if (Schema.sObjectType.Account.isUpdateable()) {
    update accounts;
}
```

## Error Handling Patterns

### LWC Error Handling
```javascript
import { LightningElement } from 'lwc';
import { ShowToastEvent } from 'lightning/platformShowToastEvent';
import saveAccount from '@salesforce/apex/AccountController.saveAccount';

export default class MyComponent extends LightningElement {
    async handleSave() {
        try {
            await saveAccount({ account: this.account });
            this.showToast('Success', 'Account saved', 'success');
        } catch (error) {
            this.showToast('Error', this.getErrorMessage(error), 'error');
        }
    }

    getErrorMessage(error) {
        if (error.body?.message) {
            return error.body.message;
        }
        return 'An unknown error occurred';
    }

    showToast(title, message, variant) {
        this.dispatchEvent(new ShowToastEvent({ title, message, variant }));
    }
}
```

### Apex Error Handling
```apex
public with sharing class AccountService {
    public static void createAccount(Account acc) {
        try {
            validateAccount(acc);
            insert acc;
        } catch (DmlException e) {
            System.debug(LoggingLevel.ERROR, 'DML Error: ' + e.getMessage());
            throw new AuraHandledException('Unable to create account');
        }
    }

    private static void validateAccount(Account acc) {
        if (String.isBlank(acc.Name)) {
            throw new IllegalArgumentException('Account name is required');
        }
    }
}
```

## Performance Optimization Patterns

### 1. Avoid SOQL in Loops
```apex
// BAD
for (Account acc : accounts) {
    List<Contact> contacts = [SELECT Id FROM Contact WHERE AccountId = :acc.Id];
}

// GOOD
Set<Id> accountIds = new Set<Id>();
for (Account acc : accounts) {
    accountIds.add(acc.Id);
}
List<Contact> contacts = [SELECT Id, AccountId FROM Contact WHERE AccountId IN :accountIds];
```

### 2. Bulkify DML
```apex
// BAD
for (Account acc : accounts) {
    insert acc;
}

// GOOD
insert accounts;
```

### 3. Use Collections Efficiently
```apex
// Build maps for lookups
Map<Id, Account> accountMap = new Map<Id, Account>(accounts);

// Group related data
Map<Id, List<Contact>> contactsByAccount = new Map<Id, List<Contact>>();
for (Contact c : contacts) {
    if (!contactsByAccount.containsKey(c.AccountId)) {
        contactsByAccount.put(c.AccountId, new List<Contact>());
    }
    contactsByAccount.get(c.AccountId).add(c);
}
```

## Testing Patterns (Production)

### Apex Test Pattern
```apex
@isTest
private class AccountServiceTest {
    @TestSetup
    static void setup() {
        // Create test data
    }

    @isTest
    static void testCreateAccount_ValidData_Success() {
        // Given
        Account acc = new Account(Name = 'Test');

        // When
        Test.startTest();
        Account result = AccountService.createAccount(acc);
        Test.stopTest();

        // Then
        System.assertNotEquals(null, result.Id);
    }

    @isTest
    static void testBulkInsert_200Records_Success() {
        // Given
        List<Account> accounts = new List<Account>();
        for (Integer i = 0; i < 200; i++) {
            accounts.add(new Account(Name = 'Bulk ' + i));
        }

        // When
        Test.startTest();
        insert accounts;
        Test.stopTest();

        // Then
        System.assertEquals(200, [SELECT COUNT() FROM Account]);
    }
}
```

## Anti-Patterns to Avoid

### NEVER DO:
1. **SOQL in loops** - Hits governor limits
2. **DML in loops** - Hits governor limits
3. **Hard-coded IDs** - Breaks in different orgs
4. **SOQL injection** - Security vulnerability (always use bind variables)
5. **Without sharing** everywhere - Security risk
6. **@SeeAllData=true** in tests - Unreliable, breaks isolation
7. **Ignore governor limits** - App will fail at scale

### DO INSTEAD:
1. Query once, loop through results
2. Collect records, DML once
3. Query by name or external ID
4. Use bind variables: `WHERE Name = :name`
5. Use `with sharing` by default
6. Create test data in tests
7. Always design for 200+ records

## Deployment Patterns

### 1. Metadata Structure
- Apex classes together
- LWC components together
- Custom objects with fields
- Triggers with handlers
- Permission sets for access

### 2. Deployment Order (if manual)
1. Custom Objects & Fields
2. Apex Classes (non-dependent)
3. Apex Triggers & Handlers
4. LWC Components
5. Lightning Pages
6. Permission Sets

### 3. Version Control
- Use SFDX source format
- Commit frequently
- Meaningful commit messages
- Feature branches
- PR reviews before merge

## Naming Conventions

### Apex
- Classes: PascalCase - `AccountService`, `ContactTriggerHandler`
- Methods: camelCase - `getAccounts`, `createAccount`
- Variables: camelCase - `accountList`, `isActive`
- Constants: UPPER_SNAKE_CASE - `MAX_RECORDS`, `DEFAULT_INDUSTRY`

### LWC
- Components: camelCase - `accountList`, `contactForm`
- JS Classes: PascalCase - `export default class AccountList`
- Properties: camelCase - `@api recordId`, `@track accounts`
- Methods: camelCase - `handleClick`, `loadAccounts`

### Salesforce Metadata
- Objects: PascalCase + `__c` - `CustomObject__c`
- Fields: PascalCase + `__c` - `CustomField__c`
- Triggers: `{Object}Trigger` - `AccountTrigger`

## Summary

**Key Principles:**
1. Platform-native design
2. Component-based architecture
3. Service layer separation
4. Governor limit awareness
5. Security by default
6. Bulk operations always
7. Test comprehensively (production)
8. Deploy incrementally
