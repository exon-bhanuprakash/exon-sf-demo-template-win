# Exonpro Tech Stack Selection Standards - Salesforce Edition

## Core Principles (ALWAYS PRIORITIZE)

### 1. **Demo-First Approach**
- Build functional demos quickly
- Production best practices documented but not enforced
- Focus on core features, skip comprehensive testing for demos
- Keep complexity minimal

### 2. **Salesforce Platform Native**
- Full-stack Salesforce: Lightning Web Components + Apex + Custom Objects
- Leverage platform capabilities (built-in security, scalability, etc.)
- Use Salesforce CLI (sf commands) for all operations
- Deploy to Developer Orgs

### 3. **Easy to Enhance**
- Modular architecture for easy feature additions
- Well-documented code and clear separation of concerns
- Standard Salesforce patterns (Service layer, Trigger framework)
- Typed Apex and JavaScript for maintainability

### 4. **Target Scale: Demo to Production**
- Demo: Focus on functionality, minimal testing
- Production: Full test coverage, security hardening, governor limit optimization
- Document production requirements separately
- Easy transition from demo to production-ready

## Pre-Established Salesforce Stack Template

### Stack: salesforce-lwc-apex

**Name**: `salesforce-lwc-apex`

**Best for:**
- Full-stack Salesforce applications
- Custom CRM features
- Internal business applications
- Customer portals (with Experience Cloud)
- Mobile apps (via Salesforce Mobile)

**Components:**
- **Frontend**: Lightning Web Components (LWC) - JavaScript, HTML, CSS
- **Backend**: Apex - Business logic, triggers, integrations
- **Database**: Salesforce Objects - Custom and standard objects
- **API**: REST/SOAP APIs, Platform Events
- **Auth**: Salesforce Identity (built-in OAuth, SSO)
- **Storage**: Files/Attachments, Content
- **Deployment**: Salesforce CLI (sf commands)
- **Version Control**: SFDX source format in Git

**Why this stack:**
- Platform-native - everything runs on Salesforce
- Built-in security, scalability, and compliance
- No infrastructure management
- Rapid development with declarative + code
- Enterprise-grade by default

**Demo Mode:**
- Skip comprehensive unit tests
- Minimal error handling
- Focus on happy path
- Document production requirements

**Production Requirements (documented, not enforced in demo):**
- 75% Apex test coverage minimum
- LWC Jest tests for complex components
- Proper error handling and logging
- Governor limit optimization
- Field-level security
- Sharing rules
- Security review

## Decision Framework

### 1. Project Requirements Analysis
- **Complexity**: CRM extension vs standalone app
- **Integration**: Salesforce-only vs external systems
- **Timeline**: Demo speed vs production readiness
- **Team**: Salesforce experience level
- **Scale**: Users, data volume, API calls

### 2. Frontend Framework Selection

#### Lightning Web Components (LWC) - PRIMARY
**Use when:**
- Building on Salesforce platform
- Need access to Salesforce data/APIs
- Want mobile responsiveness (Salesforce Mobile)
- Need Lightning App Builder integration
- Building reusable components

**Characteristics:**
- Web standards based (ES6+, Web Components)
- Reactive data binding
- Component lifecycle
- Lightning Data Service (automatic data caching)
- Lightning Message Service (component communication)

**Avoid when:**
- Need full custom UI outside Salesforce (use Visualforce or external app)

### 3. Backend Framework Selection

#### Apex - PRIMARY
**Use when:**
- Building on Salesforce platform
- Need database operations (DML, SOQL)
- Trigger logic required
- Integration with external systems
- Custom business logic

**Characteristics:**
- Strongly typed, OOP language (Java-like)
- Automatic transaction management
- Built-in security (sharing rules, FLS)
- Governor limits (prevent resource abuse)
- Asynchronous processing (Future, Queueable, Batch, Scheduled)

**Patterns:**
- Service layer for business logic
- Trigger handler pattern (one trigger per object)
- Selector layer for SOQL queries
- Domain layer for record manipulation

### 4. Database Selection

#### Salesforce Objects - PRIMARY
**Use when:**
- Building on Salesforce platform
- Need ACID compliance
- Relational data model
- Need built-in features (record ownership, sharing, validation)

**Characteristics:**
- Custom Objects for business entities
- Standard Objects (Account, Contact, etc.)
- Relationships (Lookup, Master-Detail)
- Field types (Text, Number, Date, Picklist, Formula, etc.)
- Validation rules
- Workflow rules / Process Builder / Flow

**Best Practices:**
- Use External Objects for external data (via External Data Sources)
- Keep data model simple
- Use naming conventions (singular, descriptive)
- Document relationships

### 5. Deployment Strategy

#### Salesforce CLI (sf commands) - PRIMARY
**Use when:**
- Source-driven development
- Team collaboration with Git
- CI/CD pipelines
- Scratch org or sandbox development

**Commands:**
```bash
# Login to org
sf org login web --alias DevOrg

# Deploy source
sf project deploy start

# Run tests
sf apex run test --test-level RunLocalTests

# Retrieve metadata
sf project retrieve start

# Open org
sf org open
```

### 6. Authentication Strategy

**Salesforce Identity (Built-in):**
- OAuth 2.0 for external integrations
- Single Sign-On (SSO) with SAML
- Named Credentials for API callouts
- Permission Sets for access control
- Profiles for baseline access

**Never:**
- Roll your own auth on Salesforce platform
- Store credentials in code
- Hardcode integration credentials

### 7. Technology Version Requirements

**Always use:**
- Latest API version (currently v61.0)
- ES6+ for LWC (modern JavaScript)
- Actively maintained packages
- Security-patched dependencies

**Avoid:**
- Visualforce for new projects (legacy)
- Aura Components (replaced by LWC)
- Deprecated APIs
- Unmaintained AppExchange packages

## Demo vs Production Readiness

### Demo Mode (Current Focus)
- **Testing**: Minimal or none
- **Error Handling**: Basic
- **Security**: Platform defaults
- **Governor Limits**: Not optimized
- **Documentation**: Code comments only

### Production Mode (Future Enhancement)
- **Testing**: 75%+ coverage
- **Error Handling**: Comprehensive try-catch, logging
- **Security**: FLS, sharing rules, security review
- **Governor Limits**: Bulkified, optimized queries
- **Documentation**: User guides, admin guides, API docs

### Transition Checklist
- [ ] Add Apex unit tests (75%+ coverage)
- [ ] Add LWC Jest tests
- [ ] Implement proper error handling
- [ ] Add logging/monitoring
- [ ] Enable field-level security
- [ ] Configure sharing rules
- [ ] Optimize SOQL queries (bulkification)
- [ ] Review governor limits
- [ ] Security review compliance
- [ ] User documentation
- [ ] Deployment automation

## Salesforce Development Best Practices (Reference Only)

### Code Organization
- One trigger per object
- Trigger handlers for logic
- Service classes for business logic
- Selector classes for queries
- Test classes with @isTest annotation

### Security
- Respect field-level security (FLS)
- Use WITH SECURITY_ENFORCED in SOQL
- Implement sharing rules
- Validate user permissions

### Performance
- Bulkify Apex code (handle 200 records)
- Avoid SOQL in loops
- Use selective queries (indexes)
- Limit query results
- Use asynchronous processing for heavy operations

### Testing
- 75% minimum coverage for production
- Test bulk operations (200+ records)
- Test negative scenarios
- Use Test.startTest() / Test.stopTest()
- Create test data in tests (no @SeeAllData)
