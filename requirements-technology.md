# Project Name: saas-subscription-platform

## Business Problem

SaaS companies struggle to manage the entire customer lifecycle from trial to renewal. Sales teams lack visibility into product usage data when prioritizing upsell opportunities, support teams manually track SLAs across multiple tools, and finance teams spend days calculating MRR/ARR metrics. Subscription renewals are managed in spreadsheets, leading to churn due to missed outreach. Technical support cases lack context about customer usage patterns and billing status.

## Solution

A comprehensive Sales Cloud + Service Cloud implementation tailored for SaaS businesses, with CPQ for subscription management and Revenue Cloud for usage-based billing. The platform centralizes subscription lifecycle management, automates renewal workflows, tracks product usage for data-driven upsells, and provides technical support teams with 360° customer context including billing status, feature adoption, and health scores.

## Target Users

- **Sales Reps**: Manage new business and upsell opportunities
- **Customer Success Managers**: Monitor usage, health scores, and renewal risk
- **Support Engineers**: Resolve technical issues with SLA tracking
- **Product Managers**: Analyze feature adoption and usage trends
- **Finance Team**: Track MRR/ARR, manage billing and invoices
- **Customers**: Self-service portal for subscriptions, billing, and support

## Key Features

### Phase 1 (MVP - Deploy First)
1. **Subscription Management**
   - Multi-product subscription tracking (Starter/Pro/Enterprise tiers)
   - Auto-renewal with expiration alerts (30/60/90 days)
   - Mid-term upgrades/downgrades (proration logic)
   - Subscription pause/resume workflows
   - Contract amendment tracking

2. **MRR/ARR Tracking & Reporting**
   - Automated MRR calculation (monthly recurring revenue)
   - ARR dashboards (annual recurring revenue)
   - Expansion, contraction, churn metrics
   - Cohort analysis (retention by signup month)
   - Revenue forecasting by renewal date

3. **Technical Support Ticketing**
   - Multi-channel case creation (email, chat, portal, API)
   - SLA management (response time, resolution time)
   - Priority-based routing (P0: 1hr, P1: 4hr, P2: 24hr)
   - Escalation workflows (breached SLA auto-escalates)
   - Knowledge base integration

4. **Customer Health Scoring**
   - Usage-based health calculation (login frequency, feature adoption)
   - Support ticket volume tracking (high ticket count = risk)
   - NPS score integration
   - Automated at-risk alerts (health score <50)
   - CSM assignment rules (enterprise accounts get dedicated CSM)

5. **Self-Service Customer Portal**
   - Subscription management (view plan, billing history)
   - Support ticket submission and tracking
   - Knowledge base search
   - Billing and invoice downloads
   - User management (add/remove seats)

### Phase 2 (Post-MVP)
1. **Usage-Based Billing**
   - API call metering (track usage via API)
   - Overage billing (charge for usage above plan limits)
   - Custom pricing models (per user, per GB, per API call)
   - Usage dashboards for customers

2. **Advanced Renewal Management**
   - Renewal forecasting with probability scores
   - Automated renewal playbooks (email sequences)
   - Contract negotiation tracking
   - Renewal vs. churn cohort analysis

3. **Integration Marketplace Tracking**
   - Track 3rd-party integrations per customer
   - Integration health monitoring (API errors, sync failures)
   - Partner referral tracking

4. **Developer/API User Management**
   - API key management (creation, rotation, revocation)
   - Rate limit tracking per customer
   - Webhook configuration management
   - Developer portal with API docs

## Scale Requirements

- Expected users: 20-100 internal users, 5,000-50,000 customer portal users
- Peak load: Month-end (renewals, billing), product launches
- Deployment: Salesforce Developer Org (demo), Sales + Service Cloud in production
- Growth potential: Very high (SaaS growth trajectory, international expansion)

## Technical Requirements

### Salesforce Products
- **Sales Cloud**: Opportunity and account management
- **Service Cloud**: Technical support and case management
- **Revenue Cloud (CPQ + Billing)**: Subscription management and billing
- **Experience Cloud**: Customer self-service portal
- **Slack Integration**: Internal team collaboration

### Custom Objects
- Subscription__c (link to CPQ)
- HealthScore__c (calculated daily)
- UsageMetric__c (API calls, logins, feature usage)
- RenewalOpportunity__c (auto-created 120 days before expiry)
- IntegrationConfig__c (3rd-party integrations)
- APIKey__c (developer API keys)
- BillingEvent__c (usage-based billing events)

### Apex Components
- SubscriptionService: Handle upgrades, downgrades, pauses
- HealthScoreService: Calculate customer health scores
- RenewalService: Auto-create renewal opportunities
- BillingService: Calculate MRR, ARR, usage overage
- SupportService: SLA calculation and escalation logic
- UsageTrackingService: Ingest usage data from product APIs
- IntegrationService: External API connectivity

### Lightning Web Components
- subscriptionDashboard (customer view of their plan)
- healthScoreCard (CSM view of account health)
- ticketList (support case dashboard)
- renewalPipeline (sales view of upcoming renewals)
- usageChart (graphical usage trends)
- billingHistory (invoice list with download)
- apiKeyManager (developer portal)

### Integrations
- **Product Usage API**: Real-time usage data ingestion (Segment, Mixpanel)
- **Payment Gateway**: Stripe/PayPal for subscription billing
- **Accounting System**: QuickBooks/Xero for invoice sync
- **Data Warehouse**: Snowflake/BigQuery for analytics
- **Communication Tools**: Intercom/Zendesk for support chat
- **Email Provider**: SendGrid for transactional emails (renewal reminders)

### Automation Needs
- Trigger: SubscriptionTrigger (renewal opportunity creation, health score update)
- Trigger: CaseTrigger (SLA breach escalation, priority routing)
- Flow: Renewal Reminder Workflow (automated email 90/60/30 days before expiry)
- Flow: Upsell Alert (high usage triggers upgrade recommendation)
- Scheduled Batch: Daily health score calculation (runs at midnight)
- Scheduled Batch: Weekly MRR/ARR rollup for dashboards

## Compliance & Security

- **Data Privacy**: GDPR/CCPA compliance (customer data deletion, export)
- **Payment Security**: PCI-DSS compliance (never store credit cards in Salesforce)
- **SLA Compliance**: Contractual SLA tracking and reporting
- **Audit Trail**: Track all subscription changes and billing adjustments

### Security Requirements (Demo Mode)
- Use Salesforce platform defaults
- Sharing rules: Private by default, share via account teams
- Portal user profiles: Customers see only their own data

### Production Requirements
- SSO integration with corporate Active Directory
- Multi-factor authentication for all users
- API authentication with OAuth 2.0
- Data encryption at rest and in transit
- GDPR data deletion automation (Right to be Forgotten)

## Testing Requirements

- **Demo Mode**: Testing optional, focus on happy path
- **Production Mode**:
  - 75%+ Apex code coverage
  - Integration tests for payment gateway and usage API
  - Load testing for renewal season (1000+ renewals/day)
  - UAT with sales, support, and CSM teams

## Timeline

- MVP deadline: 3 months (before next major renewal cycle)
- Phase 2: 6 months (usage-based billing launch)
- Full production: 9 months (enterprise features, international expansion)

## ExonPro Implementation Notes

**Why Sales Cloud + Service Cloud:**
- Sales Cloud: Native opportunity and forecasting for SaaS sales cycles
- Service Cloud: Purpose-built case management with SLA tracking
- Revenue Cloud (CPQ): Subscription lifecycle automation (renewals, amendments)
- No "Tech Cloud" product, but these three combined cover SaaS needs

**Demo Approach:**
- Focus on 3 customer tiers (Starter: $49/mo, Pro: $199/mo, Enterprise: $999/mo)
- Mock usage data (API calls, logins) for health score calculation
- Pre-populate support cases with realistic SLA scenarios
- Show renewal pipeline with auto-created opportunities

**Production Conversion:**
- Implement real-time usage data ingestion (Segment/Mixpanel webhook)
- Connect to Stripe for actual subscription billing
- Add Einstein Analytics for churn prediction models
- Enable Slack integration for support case notifications
- Deploy mobile app for support team (offline case updates)

**Common Use Case Example:**
A SaaS company with 5,000 customers across 3 pricing tiers ($49/mo, $199/mo, $999/mo) needs to:
- Track MRR/ARR and forecast revenue
- Monitor product usage (API calls, feature adoption) to identify upsell opportunities
- Automate renewal outreach (email 90/60/30 days before expiry)
- Provide technical support with SLA tracking (Enterprise gets 1hr response time)
- Enable customers to self-serve (upgrade plan, download invoices, submit tickets)

This platform centralizes all of that in Salesforce, replacing spreadsheets, multiple tools, and manual processes.
