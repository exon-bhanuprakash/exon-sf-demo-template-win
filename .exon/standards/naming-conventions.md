# Exonpro Naming & Copywriting Standards - Salesforce Edition

## Code Naming Conventions

### 1. Apex Naming

#### Classes & Interfaces
```apex
// Classes - PascalCase
public class AccountService { }
public class ContactTriggerHandler { }
public class OpportunitySelector { }

// Interfaces - PascalCase with 'I' prefix (optional) or descriptive name
public interface IAccountService { }
public interface Queueable { }  // Salesforce standard

// Test classes - PascalCase + Test suffix
@isTest
private class AccountServiceTest { }
```

#### Variables & Methods
```apex
// Variables - camelCase
String accountName = 'Acme Corp';
Integer recordCount = 0;
Boolean isActive = true;
List<Account> accounts = new List<Account>();
Map<Id, Contact> contactMap = new Map<Id, Contact>();

// Boolean variables - is/has/should prefix
Boolean isActive = true;
Boolean hasPermission = false;
Boolean shouldProcess = true;

// Methods - camelCase, verb + noun
public List<Account> getActiveAccounts() { }
public void createAccount(Account acc) { }
public Boolean validateEmail(String email) { }
public void handleBeforeInsert(List<Account> newRecords) { }

// Private methods - camelCase (no underscore prefix needed)
private void processRecords(List<Account> records) { }

// Constants - UPPER_SNAKE_CASE
public static final String DEFAULT_INDUSTRY = 'Technology';
public static final Integer MAX_RECORDS = 200;
public static final Decimal TAX_RATE = 0.08;
```

#### Naming Patterns by Type
```apex
// Service classes - {Object}Service
AccountService, ContactService, OpportunityService

// Selector classes - {Object}Selector
AccountSelector, ContactSelector, OpportunitySelector

// Trigger handlers - {Object}TriggerHandler
AccountTriggerHandler, ContactTriggerHandler

// Domain classes - {Object}Domain
AccountDomain, ContactDomain

// Controllers (for LWC) - {Object}Controller
AccountController, ContactFormController

// Utility classes - descriptive + Utils/Helper
EmailUtils, DateHelper, ValidationUtils

// Exception classes - descriptive + Exception
ValidationException, DataNotFoundException
```

### 2. Lightning Web Component Naming

#### Component Names
```javascript
// Component folder - camelCase
accountList/
contactForm/
opportunityDashboard/

// Component files - match folder name
accountList.js
accountList.html
accountList.css
accountList.js-meta.xml

// Class name in JS - PascalCase
export default class AccountList extends LightningElement { }
```

#### JavaScript Variables & Methods
```javascript
// Variables - camelCase
let accountName = 'Acme';
const maxRecords = 100;
let isLoading = false;

// Arrays - plural
let accounts = [];
let contacts = [];

// Objects - singular
let account = { Name: 'Acme' };
let config = { apiVersion: '61.0' };

// Methods - camelCase, verb + noun
handleClick(event) { }
loadAccounts() { }
validateForm() { }
handleAccountSelect(event) { }

// Private methods - underscore prefix (optional)
_processData() { }

// Event handlers - handle + EventName
handleClick(event) { }
handleChange(event) { }
handleSave(event) { }
handleAccountSelect(event) { }

// Constants - UPPER_SNAKE_CASE
const API_URL = '/services/data/v61.0';
const MAX_FILE_SIZE = 5000000;
```

#### Property Decorators
```javascript
// Public API properties - @api
@api recordId;
@api objectApiName;

// Tracked properties - @track (rarely needed now)
@track formData = {};

// Wire properties
@wire(getRecord, { recordId: '$recordId', fields })
wiredRecord;
```

### 3. Custom Metadata Naming

#### Custom Objects
```
// Objects - PascalCase + __c suffix
Account__c
CustomProduct__c
OrderLineItem__c

// Junction objects - Object1_Object2__c (alphabetical)
Account_Contact__c
Project_Resource__c

// Avoid abbreviations
CustomerOrder__c  // Good
CustOrd__c       // Bad
```

#### Custom Fields
```
// Fields - PascalCase + __c suffix
FirstName__c
EmailAddress__c
TotalAmount__c

// Lookup/Relationship fields - RelatedObject__c
Account__c
ParentContact__c
PrimaryOwner__c

// Checkbox fields - Is/Has prefix
IsActive__c
HasAccess__c
IsVerified__c

// Date fields - past tense or descriptive
ExpirationDate__c
LastLoginDate__c
CompletedDate__c

// Formula/Rollup fields - descriptive
TotalRevenue__c
FullName__c (formula: FirstName + LastName)
NumberOfContacts__c (rollup)
```

#### Triggers
```
// Triggers - {Object}Trigger (singular, no plural)
AccountTrigger
ContactTrigger
OpportunityTrigger

// NOT: AccountsTrigger, AccountTriggers
```

### 4. Salesforce Metadata Naming

#### Permission Sets
```
// Permission sets - descriptive, no __c suffix
Sales_User
Marketing_Manager
Admin_Full_Access
Read_Only_User
```

#### Custom Tabs
```
// Tabs - PascalCase, descriptive
Accounts_Tab
CustomDashboard_Tab
Reports_Tab
```

#### Lightning Pages
```
// Flexipages - PascalCase
Account_Record_Page
Home_Page
Custom_Dashboard
```

#### Flows
```
// Flows - descriptive with underscores
Account_Creation_Flow
Approval_Process_Flow
Email_Notification_Flow
```

### 5. SOQL Query Variables

```apex
// Query strings - descriptive + Query suffix
String accountQuery = 'SELECT Id, Name FROM Account';
String contactQuery = 'SELECT Id, FirstName FROM Contact';

// Query results - plural noun
List<Account> accounts = [SELECT Id, Name FROM Account];
List<Contact> contacts = [SELECT Id FROM Contact WHERE AccountId = :accountId];

// Single record - singular
Account account = [SELECT Id, Name FROM Account WHERE Id = :accountId LIMIT 1];

// Query maps
Map<Id, Account> accountMap = new Map<Id, Account>([SELECT Id, Name FROM Account]);
```

### 6. Test Data Naming

```apex
@isTest
private class AccountServiceTest {
    // Test data variables - test + Description
    static Account testAccount;
    static Contact testContact;
    static List<Opportunity> testOpportunities;

    // Test methods - test + MethodName + Scenario
    @isTest
    static void testGetAccountsByIndustry_WithValidIndustry_ReturnsAccounts() { }

    @isTest
    static void testCreateAccount_WithNullName_ThrowsException() { }

    @isTest
    static void testBulkInsert_With200Records_Succeeds() { }
}
```

### 7. REST API Naming

```apex
// REST Resources - plural, lowercase in URL
@RestResource(urlMapping='/accounts/*')
@RestResource(urlMapping='/contacts/*')
@RestResource(urlMapping='/custom-objects/*')

// HTTP methods follow standard naming
@HttpGet
@HttpPost
@HttpPut
@HttpPatch
@HttpDelete
```

### 8. Git Branch Naming

```bash
# Feature branches
dev                           # Main development branch
feature/account-integration
feature/contact-form-lwc

# Bug fixes
fix/account-trigger-error
fix/lwc-validation-bug

# Hotfixes
hotfix/critical-soql-query-fix

# Format: type/brief-description-kebab-case
```

### 9. Git Commit Messages

```bash
# Format: <type>: <subject>

# Types for Salesforce
feat: Add Account creation LWC component
fix: Resolve SOQL query in loop in AccountTrigger
docs: Update API documentation for ContactController
style: Format Apex code with prettier
refactor: Extract SOQL queries to selector class
test: Add test class for OpportunityService
chore: Update sfdx-project.json API version

# Good examples
feat: Add bulk account import functionality
fix: Resolve governor limit issue in batch class
refactor: Move trigger logic to handler class
test: Add test coverage for ContactTriggerHandler
docs: Add JSDoc comments to LWC components

# Bad examples
fixed stuff                   # Too vague
WIP                          # Work in progress
apex changes                 # Not descriptive
```

### 10. Environment Variables & Custom Settings

```apex
// Custom Settings - PascalCase + __c
Integration_Settings__c
Email_Configuration__c
API_Credentials__c

// Custom Metadata Types - PascalCase + __mdt
API_Config__mdt
Feature_Flag__mdt
Integration_Endpoint__mdt

// Fields in custom settings/metadata - PascalCase + __c
API_Endpoint__c
API_Key__c
Is_Enabled__c
Timeout_Seconds__c
```

## Copywriting Standards

### 11. User-Facing Text (LWC/Visualforce)

#### Buttons
```javascript
// Action buttons - imperative verbs
label="Save"
label="Create Account"
label="Send Email"
label="Download Report"

// NOT
label="Saving..."  // Use for loading state
label="Click Here"
label="Submit"     // Too generic
```

#### Error Messages
```javascript
// Be specific and helpful
"Account name is required"
"Email address is invalid"
"Unable to save record. Please check required fields."

// Provide next steps
"Record locked. Please contact your administrator."
"Insufficient privileges. You need Edit access to this record."

// NOT
"Error"
"Invalid input"
"Something went wrong"  // Too vague
```

#### Success Messages
```javascript
// Confirm the action
"Account created successfully"
"Record saved"
"Email sent to contact@example.com"

// NOT
"Success!"
"Done"
"OK"
```

#### Loading States
```javascript
// Present continuous tense
"Loading accounts..."
"Saving record..."
"Sending email..."
"Processing request..."
```

### 12. Custom Labels

```
// Custom labels - descriptive, underscores
Account_List_Header
Save_Button_Label
Error_Required_Field
Success_Record_Created
```

### 13. Code Comments

#### When to Comment
```apex
// GOOD - Explain WHY, not WHAT
// Limit to 200 records to stay within governor limits
List<Account> accounts = [SELECT Id FROM Account LIMIT 200];

// GOOD - Document complex logic
// Calculate discount: 10% for orders > $1000, 5% for orders > $500
Decimal discount = orderAmount > 1000 ? 0.10 : (orderAmount > 500 ? 0.05 : 0);

// GOOD - Warn about governor limits
// Note: Bulkify this method to handle 200+ records
public void updateAccounts(List<Account> accounts) { }

// BAD - Obvious comments
// Set account name
account.Name = 'Acme';

// BAD - Commented-out code
// String oldQuery = 'SELECT Id FROM Account';  // Remove instead
```

#### JavaDoc / ApexDoc Comments
```apex
/**
 * Get accounts by industry
 *
 * @param industry The industry to filter by
 * @param limitCount Maximum number of records to return
 * @return List of accounts matching the industry
 * @throws QueryException if query fails
 */
public static List<Account> getAccountsByIndustry(String industry, Integer limitCount) {
    // Implementation
}
```

#### JSDoc Comments (LWC)
```javascript
/**
 * Load accounts from Apex
 * @param {string} industry - Industry filter
 * @returns {Promise<Account[]>} Array of accounts
 */
loadAccounts(industry) {
    // Implementation
}
```

### 14. Naming Checklist

Before finalizing names:
- [ ] Is it descriptive and clear?
- [ ] Does it follow Salesforce conventions?
- [ ] Is it consistent with existing code?
- [ ] Can a new developer understand it?
- [ ] Is it not too long (< 40 characters for Apex, < 30 for fields)?
- [ ] Does it avoid abbreviations (except Id, API, URL)?
- [ ] Is it searchable (avoid single letters)?
- [ ] Does it follow __c or __mdt suffix rules?

### 15. Abbreviations

#### Acceptable
- `Id` (identifier) - Salesforce standard
- `API` (application programming interface)
- `URL` (uniform resource locator)
- `SOQL` (Salesforce Object Query Language)
- `DML` (Data Manipulation Language)
- `FLS` (Field Level Security)
- `CRUD` (Create, Read, Update, Delete)
- `LWC` (Lightning Web Components)
- `Aura` (Aura Components)

#### Avoid
- `acc` (use `account`)
- `cont` (use `contact`)
- `opp` (use `opportunity`)
- `rec` (use `record`)
- `val` (use `value`)
- `msg` (use `message`)

### 16. Tone & Voice

**Exonpro Standard Tone:**
- **Professional** but approachable
- **Clear** over clever
- **Helpful** not condescending
- **Concise** but complete
- **Consistent** throughout application

**Examples:**
```
GOOD: "Enter email address to continue"
BAD:  "Pop your email in here!"

GOOD: "Record saved successfully"
BAD:  "Woohoo! All done!"

GOOD: "Unable to delete record. Remove related contacts first."
BAD:  "Oops! Can't delete that!"
```

### 17. Salesforce-Specific Naming Rules

#### Standard Objects
- Use standard object names: `Account`, `Contact`, `Opportunity`, `Lead`, `Case`
- NOT custom names for standard objects

#### Naming Length Limits
- Custom object names: 40 characters (including __c)
- Custom field names: 40 characters (including __c)
- Apex class names: 40 characters
- LWC component names: 40 characters

#### Reserved Words
Avoid Salesforce reserved words:
- `abstract`, `after`, `before`, `break`, `catch`, `class`, `continue`
- `delete`, `do`, `else`, `enum`, `extends`, `false`, `final`, `finally`
- `for`, `from`, `global`, `if`, `implements`, `insert`, `instanceof`
- `interface`, `merge`, `new`, `null`, `on`, `override`, `private`
- `protected`, `public`, `return`, `select`, `static`, `super`, `switch`
- `this`, `throw`, `true`, `try`, `undelete`, `update`, `upsert`
- `virtual`, `void`, `webservice`, `while`, `with`, `without`

Full list: https://developer.salesforce.com/docs/atlas.en-us.apexcode.meta/apexcode/apex_reserved_words.htm
