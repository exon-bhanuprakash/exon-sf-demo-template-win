# Exonpro Security Best Practices - Salesforce Edition

## Demo vs Production Security

**IMPORTANT: This document provides production-ready security guidelines. For DEMO projects, these are REFERENCE ONLY - not enforced.**

### Demo Mode (Current Focus)
- Use Salesforce platform defaults
- Skip custom security implementation
- Minimal validation
- Focus on functionality

### Production Mode (Future Implementation)
- Full field-level security (FLS)
- Sharing rules implementation
- Input validation
- Governor limit protection
- Security review compliance

---

## Production Security Guidelines (Reference Only)

### 1. Salesforce Platform Security

#### Sharing Model
```apex
// Use 'with sharing' for all classes (enforces sharing rules)
public with sharing class AccountService {
    // Respects org-wide defaults, sharing rules, role hierarchy
}

// Use 'without sharing' ONLY when explicitly needed
public without sharing class SystemProcessService {
    // Bypasses sharing rules - use carefully
}

// Inherited sharing (new)
public inherited sharing class HelperClass {
    // Inherits sharing from caller
}
```

#### Field-Level Security (FLS)
```apex
// Method 1: WITH SECURITY_ENFORCED (recommended)
List<Account> accounts = [
    SELECT Id, Name, Industry
    FROM Account
    WHERE Industry = :industry
    WITH SECURITY_ENFORCED
];

// Method 2: Security.stripInaccessible()
SObjectAccessDecision decision = Security.stripInaccessible(
    AccessType.READABLE,
    [SELECT Id, Name, Industry FROM Account]
);
List<Account> accounts = decision.getRecords();

// Method 3: Schema methods (manual check)
if (Schema.sObjectType.Account.fields.Industry.isAccessible()) {
    // Query Industry field
}
```

#### Object-Level Security (CRUD)
```apex
// Check CRUD permissions before DML
if (Schema.sObjectType.Account.isCreateable()) {
    insert accounts;
}

if (Schema.sObjectType.Account.isUpdateable()) {
    update accounts;
}

if (Schema.sObjectType.Account.isDeletable()) {
    delete accounts;
}
```

### 2. Input Validation & Sanitization

#### SOQL Injection Prevention
```apex
// CORRECT - Use bind variables
String industry = 'Technology';
List<Account> accounts = [
    SELECT Id, Name
    FROM Account
    WHERE Industry = :industry
];

// NEVER - String concatenation
String query = 'SELECT Id FROM Account WHERE Industry = \'' + industry + '\'';
// SOQL injection vulnerability!
```

#### Apex Input Validation
```apex
public class AccountService {
    public static void createAccount(String name, String industry) {
        // Validate inputs
        if (String.isBlank(name)) {
            throw new IllegalArgumentException('Account name is required');
        }

        if (name.length() > 255) {
            throw new IllegalArgumentException('Account name too long');
        }

        // Sanitize
        name = name.trim();

        // Create account
        Account acc = new Account(
            Name = name,
            Industry = industry
        );
        insert acc;
    }
}
```

#### LWC Input Validation
```javascript
// validateForm in LWC
validateForm() {
    const nameField = this.template.querySelector('.name-field');
    const emailField = this.template.querySelector('.email-field');

    // Validate name
    if (!nameField.value || nameField.value.trim() === '') {
        nameField.setCustomValidity('Name is required');
        nameField.reportValidity();
        return false;
    }

    // Validate email
    const emailPattern = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
    if (!emailPattern.test(emailField.value)) {
        emailField.setCustomValidity('Invalid email format');
        emailField.reportValidity();
        return false;
    }

    return true;
}
```

### 3. Authentication & Authorization

#### Profile & Permission Sets
```
// Profiles - Baseline access (use sparingly)
- Standard User
- System Administrator

// Permission Sets - Additive permissions (recommended)
- Account_Manager
- Contact_Editor
- Report_Viewer
- Admin_Functions
```

#### Custom Permissions
```apex
// Check custom permissions
if (FeatureManagement.checkPermission('Access_Admin_Features')) {
    // User has custom permission
}
```

#### Named Credentials (API Integration)
```apex
// Use Named Credentials for external API calls (stores credentials securely)
HttpRequest req = new HttpRequest();
req.setEndpoint('callout:My_Named_Credential/api/endpoint');
req.setMethod('GET');
Http http = new Http();
HttpResponse res = http.send(req);
```

### 4. Governor Limits Protection

#### SOQL Best Practices
```apex
// GOOD - Query outside loop
List<Contact> contacts = [SELECT Id, AccountId FROM Contact WHERE AccountId IN :accountIds];
Map<Id, List<Contact>> contactsByAccount = new Map<Id, List<Contact>>();
for (Contact c : contacts) {
    if (!contactsByAccount.containsKey(c.AccountId)) {
        contactsByAccount.put(c.AccountId, new List<Contact>());
    }
    contactsByAccount.get(c.AccountId).add(c);
}

// BAD - SOQL in loop
for (Account acc : accounts) {
    List<Contact> contacts = [SELECT Id FROM Contact WHERE AccountId = :acc.Id];
    // SOQL query inside loop - hits governor limits!
}
```

#### DML Best Practices
```apex
// GOOD - Bulk DML
List<Account> accounts = new List<Account>();
for (Integer i = 0; i < 200; i++) {
    accounts.add(new Account(Name = 'Account ' + i));
}
insert accounts;  // Single DML for all records

// BAD - DML in loop
for (Integer i = 0; i < 200; i++) {
    Account acc = new Account(Name = 'Account ' + i);
    insert acc;  // DML inside loop - hits governor limits!
}
```

#### Limit Tracking
```apex
// Check governor limits
System.debug('SOQL Queries: ' + Limits.getQueries() + '/' + Limits.getLimitQueries());
System.debug('DML Statements: ' + Limits.getDmlStatements() + '/' + Limits.getLimitDmlStatements());
System.debug('Heap Size: ' + Limits.getHeapSize() + '/' + Limits.getLimitHeapSize());
```

### 5. Error Handling & Logging

#### Try-Catch Blocks
```apex
public class AccountService {
    public static void createAccount(Account acc) {
        try {
            insert acc;
        } catch (DmlException e) {
            // Log error (don't expose to user)
            System.debug(LoggingLevel.ERROR, 'DML Error: ' + e.getMessage());

            // Return user-friendly error
            throw new AuraHandledException('Unable to create account. Please try again.');
        }
    }
}
```

#### LWC Error Handling
```javascript
// handleSave in LWC
handleSave() {
    createAccount({ name: this.accountName })
        .then(result => {
            this.showToast('Success', 'Account created', 'success');
        })
        .catch(error => {
            // Don't expose internal errors to users
            const errorMessage = error.body?.message || 'An error occurred';
            this.showToast('Error', errorMessage, 'error');
        });
}
```

### 6. Data Protection

#### Sensitive Data Handling
```apex
// NEVER log sensitive data
// BAD
System.debug('Password: ' + password);
System.debug('SSN: ' + ssn);
System.debug('Credit Card: ' + ccNumber);

// GOOD - Mask or omit sensitive fields
System.debug('Processing user: ' + userId);
System.debug('Record count: ' + records.size());
```

#### Encryption
```apex
// Use Crypto class for encryption
Blob key = Crypto.generateAesKey(256);
Blob data = Blob.valueOf('Sensitive data');
Blob encrypted = Crypto.encryptWithManagedIV('AES256', key, data);

// Decrypt
Blob decrypted = Crypto.decryptWithManagedIV('AES256', key, encrypted);
String originalData = decrypted.toString();
```

### 7. Lightning Security (LWC)

#### Lightning Locker Service
- Automatic XSS protection
- DOM access restrictions
- Strict CSP enforcement
- Secure component isolation

#### LWC Security Best Practices
```javascript
// SAFE - Lightning Data Service (automatic security)
import { getRecord } from 'lightning/uiRecordApi';

@wire(getRecord, { recordId: '$recordId', fields })
wiredRecord;

// SAFE - Apex method with @AuraEnabled
import getAccounts from '@salesforce/apex/AccountController.getAccounts';

// DANGEROUS - Bypassing security (avoid)
// Don't use dynamic SOQL in Apex methods exposed to LWC
```

#### Content Security Policy
- Lightning Locker enforces strict CSP
- No inline scripts allowed
- Limited external resource loading
- Use Lightning Base Components (pre-secured)

### 8. API Security

#### Apex REST API
```apex
@RestResource(urlMapping='/accounts/*')
global with sharing class AccountRestAPI {

    @HttpGet
    global static List<Account> getAccounts() {
        // Enforces sharing rules (with sharing)
        // Enforces FLS (WITH SECURITY_ENFORCED)
        return [
            SELECT Id, Name
            FROM Account
            WITH SECURITY_ENFORCED
            LIMIT 200
        ];
    }

    @HttpPost
    global static Account createAccount(String name, String industry) {
        // Validate input
        if (String.isBlank(name)) {
            RestContext.response.statusCode = 400;
            return null;
        }

        // Check CRUD
        if (!Schema.sObjectType.Account.isCreateable()) {
            RestContext.response.statusCode = 403;
            return null;
        }

        Account acc = new Account(Name = name, Industry = industry);
        insert acc;
        return acc;
    }
}
```

### 9. Security Checklist (Production Only)

Before deployment:
- [ ] All classes use 'with sharing' (unless explicitly needed)
- [ ] SOQL queries use WITH SECURITY_ENFORCED or stripInaccessible()
- [ ] No SOQL in loops
- [ ] No DML in loops
- [ ] Input validation on all user inputs
- [ ] No sensitive data in logs/debug statements
- [ ] Error messages don't expose internal details
- [ ] Named Credentials for external APIs
- [ ] Custom permissions for sensitive operations
- [ ] Field-level security configured
- [ ] Sharing rules configured
- [ ] Governor limits tested with bulk data
- [ ] Security review compliance (for AppExchange)

### 10. Common Security Anti-Patterns

**Avoid:**
```apex
// Anti-pattern 1: SOQL injection
String query = 'SELECT Id FROM Account WHERE Name = \'' + userInput + '\'';

// Anti-pattern 2: No sharing enforcement
public without sharing class AccountService { }  // Use sparingly

// Anti-pattern 3: Ignoring FLS
List<Account> accounts = [SELECT Id, Sensitive_Field__c FROM Account];
// Access sensitive field without checking permissions

// Anti-pattern 4: DML without CRUD check
insert accounts;  // No check if user can create accounts

// Anti-pattern 5: Exposing internal errors
catch (Exception e) {
    throw new AuraHandledException(e.getMessage());  // Exposes internal details
}
```

### 11. Security Resources

**Salesforce Documentation:**
- Security Guide: https://developer.salesforce.com/docs/atlas.en-us.securityImplGuide.meta/securityImplGuide/
- Apex Security: https://developer.salesforce.com/docs/atlas.en-us.apexcode.meta/apexcode/apex_security.htm
- LWC Security: https://developer.salesforce.com/docs/component-library/documentation/en/lwc/lwc.security

**Tools:**
- PMD (Static code analysis)
- Checkmarx for Salesforce
- Security Health Check (in Setup)

---

## Demo Implementation Notes

For demo projects:
1. **Skip**: Custom security implementation, FLS checks, sharing rules
2. **Use**: Platform defaults, with sharing classes
3. **Document**: Security requirements for production
4. **Test**: With System Administrator profile only

**To convert demo to production:**
See production checklist above and implement all security measures.
