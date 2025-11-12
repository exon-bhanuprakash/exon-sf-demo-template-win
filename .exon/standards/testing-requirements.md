# Exonpro Testing Requirements - Salesforce Edition

## Demo vs Production Testing

**IMPORTANT: For DEMO projects, comprehensive testing is OPTIONAL. This document is for REFERENCE when transitioning to production.**

### Demo Mode (Current Focus)
- **Testing**: Optional, skip for demos
- **Coverage**: Not required
- **Focus**: Functional demonstration
- **Validation**: Manual testing only

### Production Mode (Future Implementation)
- **Testing**: 75%+ Apex coverage REQUIRED
- **Coverage**: LWC Jest tests for complex components
- **Focus**: Quality assurance
- **Validation**: Automated test suites

---

## Production Testing Guidelines (Reference Only)

### 1. Apex Test Coverage Requirements

#### Minimum Coverage
- **Apex classes**: 75% minimum for production deployment
- **Triggers**: 75% coverage through trigger handler tests
- **Critical logic**: 90%+ coverage
- **Overall org**: 75% average required

#### What to Test
- Service layer methods
- Trigger handlers
- Selector classes
- Controller methods (@AuraEnabled)
- Batch/Queueable/Schedulable classes
- REST API endpoints

#### What NOT to Test (Demo)
- Simple getters/setters
- Standard Salesforce features
- Framework code
- Auto-generated code

### 2. Apex Test Class Structure

#### Basic Test Template
```apex
@isTest
private class AccountServiceTest {

    @TestSetup
    static void setup() {
        // Create test data once per test class
        List<Account> accounts = new List<Account>();
        for (Integer i = 0; i < 10; i++) {
            accounts.add(new Account(
                Name = 'Test Account ' + i,
                Industry = 'Technology'
            ));
        }
        insert accounts;
    }

    @isTest
    static void testGetAccountsByIndustry_WithValidIndustry_ReturnsAccounts() {
        // Given
        String industry = 'Technology';

        // When
        Test.startTest();
        List<Account> result = AccountService.getAccountsByIndustry(industry);
        Test.stopTest();

        // Then
        System.assertEquals(10, result.size(), 'Should return 10 accounts');
        for (Account acc : result) {
            System.assertEquals(industry, acc.Industry, 'Industry should match');
        }
    }

    @isTest
    static void testGetAccountsByIndustry_WithNoMatches_ReturnsEmpty() {
        // Given
        String industry = 'NonExistent';

        // When
        Test.startTest();
        List<Account> result = AccountService.getAccountsByIndustry(industry);
        Test.stopTest();

        // Then
        System.assertEquals(0, result.size(), 'Should return empty list');
    }

    @isTest
    static void testBulkOperations_With200Records_Succeeds() {
        // Given - create 200 accounts for bulk testing
        List<Account> accounts = new List<Account>();
        for (Integer i = 0; i < 200; i++) {
            accounts.add(new Account(
                Name = 'Bulk Account ' + i,
                Industry = 'Finance'
            ));
        }

        // When
        Test.startTest();
        insert accounts;
        Test.stopTest();

        // Then
        Integer count = [SELECT COUNT() FROM Account WHERE Industry = 'Finance'];
        System.assertEquals(200, count, 'Should insert all 200 records');
    }
}
```

#### Test Execution Context
```apex
// Test.startTest() and Test.stopTest() reset governor limits
Test.startTest();
// Code here gets fresh governor limits
// Asynchronous code executes here
Test.stopTest();
// Async operations complete before assertions
```

#### Test Data Creation
```apex
// Create test data - NO @SeeAllData=true
@TestSetup
static void setup() {
    // Setup runs once per test class
    // Data persists across test methods
    Account testAccount = new Account(Name = 'Test');
    insert testAccount;
}

// Use Test.loadData() for CSV test data (optional)
List<Account> accounts = Test.loadData(Account.sObjectType, 'test_accounts');
```

### 3. Testing Triggers

#### Trigger Handler Test
```apex
@isTest
private class AccountTriggerHandlerTest {

    @isTest
    static void testBeforeInsert_SetsDefaultValues() {
        // Given
        Account acc = new Account(Name = 'Test Account');
        // Don't set Industry - handler should set default

        // When
        Test.startTest();
        insert acc;
        Test.stopTest();

        // Then
        Account inserted = [SELECT Id, Industry FROM Account WHERE Id = :acc.Id];
        System.assertNotEquals(null, inserted.Industry, 'Industry should be set by trigger');
    }

    @isTest
    static void testAfterInsert_CreatesRelatedRecords() {
        // Given
        Account acc = new Account(Name = 'Test Account');

        // When
        Test.startTest();
        insert acc;
        Test.stopTest();

        // Then
        List<Contact> contacts = [SELECT Id FROM Contact WHERE AccountId = :acc.Id];
        System.assertEquals(1, contacts.size(), 'Trigger should create related contact');
    }

    @isTest
    static void testBulkInsert_Handles200Records() {
        // Given
        List<Account> accounts = new List<Account>();
        for (Integer i = 0; i < 200; i++) {
            accounts.add(new Account(Name = 'Bulk Account ' + i));
        }

        // When
        Test.startTest();
        insert accounts;
        Test.stopTest();

        // Then - verify trigger logic executed for all records
        System.assertEquals(200, [SELECT COUNT() FROM Account WHERE Name LIKE 'Bulk Account%']);
    }
}
```

### 4. Testing LWC Controllers (@AuraEnabled)

#### Controller Test
```apex
@isTest
private class AccountControllerTest {

    @isTest
    static void testGetAccounts_ReturnsAccountList() {
        // Given
        insert new Account(Name = 'Test Account', Industry = 'Technology');

        // When
        Test.startTest();
        List<Account> result = AccountController.getAccounts('Technology');
        Test.stopTest();

        // Then
        System.assertEquals(1, result.size());
        System.assertEquals('Test Account', result[0].Name);
    }

    @isTest
    static void testCreateAccount_WithValidData_CreatesAccount() {
        // Given
        String accountName = 'New Account';
        String industry = 'Technology';

        // When
        Test.startTest();
        Id accountId = AccountController.createAccount(accountName, industry);
        Test.stopTest();

        // Then
        Account acc = [SELECT Name, Industry FROM Account WHERE Id = :accountId];
        System.assertEquals(accountName, acc.Name);
        System.assertEquals(industry, acc.Industry);
    }

    @isTest
    static void testCreateAccount_WithInvalidData_ThrowsException() {
        // Given
        String accountName = null;  // Invalid

        // When/Then
        Test.startTest();
        try {
            AccountController.createAccount(accountName, 'Technology');
            System.assert(false, 'Should have thrown exception');
        } catch (AuraHandledException e) {
            System.assert(e.getMessage().contains('required'), 'Should mention required field');
        }
        Test.stopTest();
    }
}
```

### 5. LWC Testing (Jest) - Optional for Demo

#### Basic Jest Test
```javascript
// accountList.test.js
import { createElement } from 'lwc';
import AccountList from 'c/accountList';
import getAccounts from '@salesforce/apex/AccountController.getAccounts';

// Mock Apex method
jest.mock(
    '@salesforce/apex/AccountController.getAccounts',
    () => ({
        default: jest.fn()
    }),
    { virtual: true }
);

describe('c-account-list', () => {
    afterEach(() => {
        while (document.body.firstChild) {
            document.body.removeChild(document.body.firstChild);
        }
        jest.clearAllMocks();
    });

    it('renders account list when data is returned', async () => {
        // Given
        const mockAccounts = [
            { Id: '001000000000001', Name: 'Account 1' },
            { Id: '001000000000002', Name: 'Account 2' }
        ];
        getAccounts.mockResolvedValue(mockAccounts);

        // When
        const element = createElement('c-account-list', {
            is: AccountList
        });
        document.body.appendChild(element);

        // Wait for async operations
        await Promise.resolve();

        // Then
        const accountItems = element.shadowRoot.querySelectorAll('.account-item');
        expect(accountItems.length).toBe(2);
    });

    it('displays error message when fetch fails', async () => {
        // Given
        getAccounts.mockRejectedValue(new Error('Failed to fetch'));

        // When
        const element = createElement('c-account-list', {
            is: AccountList
        });
        document.body.appendChild(element);

        // Wait for async operations
        await Promise.resolve();

        // Then
        const errorMessage = element.shadowRoot.querySelector('.error-message');
        expect(errorMessage).not.toBeNull();
    });
});
```

### 6. Test Execution

#### Run Tests via sf CLI
```bash
# Run all tests
sf apex run test --test-level RunLocalTests --wait 10

# Run specific test class
sf apex run test --class-names AccountServiceTest --wait 5

# Run tests with code coverage
sf apex run test --code-coverage --result-format human

# Run tests in specific org
sf apex run test --test-level RunLocalTests --target-org DevOrg
```

#### Check Code Coverage
```bash
# Get org-wide coverage
sf apex get test --test-run-id 707xxx --code-coverage

# View coverage in VS Code
# Use Salesforce Extension Pack
# View > Command Palette > SFDX: Get Apex Test Code Coverage
```

### 7. Test Best Practices (Production)

#### DO:
- Test bulk operations (200 records minimum)
- Test positive and negative scenarios
- Test governor limits
- Use @TestSetup for data creation
- Use Test.startTest() / Test.stopTest()
- Create test data in tests (no @SeeAllData)
- Assert expected outcomes
- Test error handling

#### DON'T:
- Use @SeeAllData=true (queries production data)
- Make callouts without Test.setMock()
- Skip bulk testing
- Test framework code
- Rely on test execution order
- Leave System.debug() in test code
- Skip negative test cases

### 8. Testing Checklist (Production Only)

Before deployment:
- [ ] 75%+ Apex code coverage
- [ ] All test classes pass
- [ ] Bulk operations tested (200+ records)
- [ ] Negative scenarios tested
- [ ] Error handling tested
- [ ] No @SeeAllData=true
- [ ] No hardcoded IDs
- [ ] Test.startTest() / Test.stopTest() used correctly
- [ ] Governor limits checked
- [ ] Async operations tested

### 9. Common Testing Anti-Patterns

**Avoid:**
```apex
// Anti-pattern 1: Using @SeeAllData=true
@isTest(SeeAllData=true)  // Don't use in production

// Anti-pattern 2: No Test.startTest()
insert accounts;  // No fresh governor limits

// Anti-pattern 3: Testing only single records
Account acc = new Account(Name = 'Test');
insert acc;  // Doesn't test bulk

// Anti-pattern 4: Hardcoded IDs
Account acc = [SELECT Id FROM Account WHERE Id = '001000000000001'];
// Breaks in different orgs

// Anti-pattern 5: No assertions
AccountService.createAccount(acc);
// No verification that it worked
```

### 10. Test Utilities (Optional)

#### Test Data Factory
```apex
@isTest
public class TestDataFactory {

    public static Account createAccount(String name) {
        return new Account(
            Name = name,
            Industry = 'Technology',
            AnnualRevenue = 1000000
        );
    }

    public static List<Account> createAccounts(Integer count) {
        List<Account> accounts = new List<Account>();
        for (Integer i = 0; i < count; i++) {
            accounts.add(createAccount('Test Account ' + i));
        }
        return accounts;
    }

    public static Contact createContact(Id accountId) {
        return new Contact(
            FirstName = 'Test',
            LastName = 'Contact',
            AccountId = accountId,
            Email = 'test@example.com'
        );
    }
}
```

---

## Demo Testing Notes

For demo projects:
1. **Skip**: Apex test classes, Jest tests, code coverage
2. **Use**: Manual testing with System Administrator
3. **Document**: Test scenarios for production
4. **Focus**: Demonstrate functionality, not quality assurance

**To convert demo to production:**
1. Write test classes for all Apex code
2. Achieve 75%+ code coverage
3. Add Jest tests for complex LWC components
4. Run full test suite before each deployment
5. Set up CI/CD with automated testing

---

## Testing Resources

**Salesforce Documentation:**
- Apex Testing: https://developer.salesforce.com/docs/atlas.en-us.apexcode.meta/apexcode/apex_testing.htm
- LWC Testing: https://developer.salesforce.com/docs/component-library/documentation/en/lwc/lwc.testing

**Tools:**
- Apex Test Execution: Salesforce CLI (`sf apex run test`)
- LWC Testing: Jest framework
- Code Coverage: VS Code Salesforce Extension Pack
- CI/CD: GitHub Actions, Jenkins, CircleCI
