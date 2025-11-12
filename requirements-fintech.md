# Project Name: digital-lending-platform

## Business Problem

FinTech lending platforms and NBFCs struggle with fragmented customer data across loan origination, underwriting, and servicing systems. Loan officers manually chase documents from applicants, compliance teams lack audit trails for KYC/AML checks, and customers have no visibility into application status. Relationship managers at banks can't see household financial positions across accounts, and insurance companies track policies in legacy systems disconnected from customer service.

## Solution

A Financial Services Cloud implementation that provides a 360° view of customers with household relationships, automates loan application workflows with KYC/AML compliance tracking, and enables relationship-based financial planning. The platform centralizes loan lifecycle management (application → approval → disbursement → repayment), tracks referrals and commissions, and ensures full audit trails for regulatory compliance.

## Target Users

- **Loan Officers**: Process loan applications and underwrite decisions
- **Compliance Officers**: Perform KYC/AML checks and manage audit trails
- **Relationship Managers**: Manage client relationships and financial goals
- **Collections Team**: Track repayments and manage delinquencies
- **Customers**: Apply for loans, track status, make payments
- **Referral Partners**: Submit loan applications on behalf of customers

## Key Features

### Phase 1 (MVP - Deploy First)
1. **Customer 360 & Household View**
   - Individual and business customer profiles
   - Household relationship mapping (primary account holder, dependents)
   - Financial accounts dashboard (loans, savings, investments)
   - Asset tracking (owned properties, vehicles)
   - Communication history and document repository

2. **Loan Application & Origination**
   - Multi-channel application capture (web, mobile, branch)
   - Document upload and verification (Aadhaar, PAN, bank statements)
   - Credit score integration (CIBIL/Experian API)
   - Application status tracking (submitted → in-review → approved/rejected)
   - Automated eligibility checks (income, credit score, debt-to-income ratio)

3. **KYC/AML Compliance**
   - Automated KYC workflow (document verification, address proof)
   - AML screening (watchlist checks, PEP screening)
   - Risk scoring (low/medium/high risk categorization)
   - Audit trail for all compliance actions
   - Regulatory reporting (suspicious activity alerts)

4. **Loan Underwriting & Approval**
   - Risk-based pricing (interest rate based on credit score)
   - Multi-level approval workflow (auto-approve <₹50K, manual >₹50K)
   - Underwriter workbench (all applicant data in one view)
   - Rejection reason tracking
   - Conditional approval with pending documents

5. **Loan Servicing & Repayment**
   - EMI schedule tracking (monthly payment due dates)
   - Payment history and outstanding balance
   - Late payment alerts and penalties
   - Prepayment/foreclosure calculations
   - Automated payment reminders (email/SMS)

### Phase 2 (Post-MVP)
1. **Financial Goals & Planning**
   - Goal tracking (retirement, education, home purchase)
   - Investment portfolio management
   - Insurance policy recommendations
   - Financial health score

2. **Referral Management**
   - Partner/agent referral tracking
   - Commission calculation and payment
   - Performance dashboards for partners
   - Lead distribution rules

3. **Collections & Recovery**
   - Delinquency tracking (30/60/90 day buckets)
   - Automated collection workflows (dunning sequences)
   - Field agent assignment for physical visits
   - Restructuring and settlement tracking

4. **Insurance Policy Management** (if applicable)
   - Policy lifecycle (quote → bind → renewal → claims)
   - Premium tracking and payment collection
   - Claims processing workflow
   - Policy renewal automation

## Scale Requirements

- Expected users: 50-300 internal users, 10,000-100,000 customer portal users
- Peak load: Festival seasons (Diwali, year-end), salary credit dates (5th, 10th of month)
- Deployment: Salesforce Developer Org (demo), Financial Services Cloud in production
- Growth potential: Very high (digital lending growth, geographic expansion)

## Technical Requirements

### Salesforce Products
- **Financial Services Cloud**: Core platform (Client 360, Household, Financial Accounts)
- **Experience Cloud**: Customer self-service portal
- **OmniStudio (optional)**: Complex loan application forms with conditional logic
- **Einstein Analytics**: Predictive risk modeling and portfolio analytics

### Custom Objects
- LoanApplication__c (extend standard Application)
- LoanAccount__c (extend Financial Account)
- KYCVerification__c
- AMLScreening__c
- EMISchedule__c
- Repayment__c
- Collateral__c (for secured loans)
- ReferralLead__c
- CommissionPayout__c

### Apex Components
- LoanApplicationService: Handle application workflows
- UnderwritingService: Risk scoring and eligibility checks
- KYCService: Automate document verification
- AMLService: Watchlist screening integration
- RepaymentService: EMI calculations and payment processing
- CollectionService: Delinquency tracking and recovery workflows
- ReferralService: Commission calculations
- IntegrationService: External API connectivity (credit bureaus, banks)

### Lightning Web Components
- loanApplicationForm (customer portal)
- kycVerificationWizard (document upload)
- underwriterWorkbench (loan officer dashboard)
- customerFinancial360 (relationship manager view)
- emiCalculator (loan calculator with amortization)
- paymentPortal (customer repayment interface)
- referralDashboard (partner performance)
- complianceAuditTrail (compliance officer view)

### Integrations
- **Credit Bureau**: CIBIL/Experian API for credit score checks
- **E-KYC**: Aadhaar/DigiLocker API for document verification
- **Bank Account Verification**: Penny drop API, bank statement parsing
- **Payment Gateway**: Razorpay/PayU for EMI collection
- **SMS Provider**: Twilio/MSG91 for payment reminders
- **Core Banking System**: Loan disbursement and repayment sync
- **Accounting System**: Journal entry posting for disbursements/repayments

### Automation Needs
- Trigger: LoanApplicationTrigger (status change notifications, auto-routing)
- Trigger: RepaymentTrigger (outstanding balance update, late fee calculation)
- Flow: Loan Approval Workflow (multi-level approval based on amount)
- Flow: KYC Verification Process (sequential document checks)
- Flow: Collections Escalation (30 days overdue → soft reminder, 60 days → call, 90 days → legal)
- Scheduled Batch: Daily EMI due reminder (runs at 8 AM)
- Scheduled Batch: Weekly delinquency report generation

## Compliance & Security

- **Regulatory Compliance**:
  - RBI Guidelines (for NBFCs in India)
  - KYC/AML regulations (PMLA Act)
  - Data localization (store customer data in India)
  - GDPR/CCPA (for international customers)

- **Data Privacy**:
  - Consent management (explicit consent for credit checks)
  - Data retention policy (7 years for loan records)
  - Right to erasure (customer data deletion requests)

- **Audit & Compliance**:
  - Full audit trail for all loan decisions
  - Track who accessed customer financial data
  - Generate compliance reports (KYC completion, AML screening)
  - Suspicious activity reporting (SAR) to regulators

### Security Requirements (Demo Mode)
- Use Salesforce platform defaults
- Sharing rules: Private by default, share via account teams
- Portal user profiles: Customers see only their own loans

### Production Requirements
- SSO integration with corporate Active Directory
- Multi-factor authentication for all internal users
- Data encryption at rest and in transit (AES-256)
- Mask sensitive data (PAN, bank account numbers) in UI
- IP whitelisting for API access
- Role-based access control (loan officers can't see others' portfolios)
- Regular security audits and penetration testing

## Testing Requirements

- **Demo Mode**: Testing optional, focus on happy path
- **Production Mode**:
  - 75%+ Apex code coverage
  - Integration tests for credit bureau and KYC APIs
  - Load testing for peak seasons (10,000+ applications/day)
  - UAT with loan officers, compliance team, and customers
  - Security testing (penetration testing, vulnerability scanning)

## Timeline

- MVP deadline: 4 months (before next festival season)
- Phase 2: 8 months (collections, referral management)
- Full production: 12 months (multi-product lending, insurance integration)

## ExonPro Implementation Notes

**Why Financial Services Cloud:**
- Pre-built Client 360 with household relationships
- Native Financial Account objects (loans, savings, investments)
- Compliance-focused features (audit trails, regulatory reporting)
- Purpose-built for banks, NBFCs, wealth managers, insurance

**Demo Approach:**
- Focus on personal loan product (unsecured, 12-month tenure)
- Mock credit bureau responses (good/average/poor scores)
- Pre-populate sample customers with household data
- Show loan journey: application → KYC → approval → disbursement → repayment

**Production Conversion:**
- Implement real credit bureau integration (CIBIL API)
- Add e-KYC integration (Aadhaar OTP verification)
- Connect to core banking system for disbursement
- Add payment gateway for EMI collection
- Enable Einstein Analytics for default prediction models
- Deploy mobile app for field agents (offline loan applications)

**Common Use Case Examples:**

1. **NBFC Personal Loan**: Customer applies for ₹2 lakh personal loan via website. System checks credit score, runs KYC, auto-approves if score >750, disburses to bank account, tracks 12 EMI payments, sends reminders before due date.

2. **Bank Relationship Management**: Relationship manager sees household view of HNI family (primary account holder + spouse + 2 children). Dashboard shows total assets (₹5 crore), existing loans (home loan ₹80 lakh), investments (mutual funds ₹1.5 crore), and recommends insurance policies.

3. **FinTech Lending Platform**: Digital lender processes 10,000 applications/month. Salesforce automates KYC (Aadhaar verification), credit checks (CIBIL), risk scoring, and approval workflows. Loan officers focus on edge cases, system auto-approves 80% of applications.

4. **Insurance Company**: Track life insurance policies with premium payment schedules, claims processing, policy renewals, and customer service cases in single platform.

**Industry-Specific Benefits:**
- Household view: See family's complete financial picture
- Compliance built-in: KYC/AML workflows with audit trails
- Financial goals: Track customer life goals (retirement, education)
- Referral tracking: Manage agent/broker commissions
- Regulatory reporting: Generate reports for RBI/SEBI/IRDAI
