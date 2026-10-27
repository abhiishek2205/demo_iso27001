# Organisation Profile: SecurePay Technologies Pvt. Ltd.

> **Fictional organisation.** SecurePay Technologies is invented for a self-directed ISO/IEC 27001:2022 gap
> assessment. Its people, systems, incidents and metrics are realistic assumptions for an early-stage Indian
> fintech. They do not describe any real company, and this is not a real client engagement.

---

## 1. Business overview

| Attribute | Detail |
|---|---|
| Legal name | SecurePay Technologies Private Limited |
| Founded | 2021, Bengaluru, Karnataka |
| Funding | Series A (venture-backed) |
| Business model | Online **Payment Aggregator (PA)** for small and medium merchants: hosted checkout, payment links, card and UPI acceptance, T+1 settlement to merchant bank accounts, merchant dashboard and REST API |
| Regulatory status | **In-principle authorisation** from the Reserve Bank of India as an online PA; final authorisation pending |
| Customers | About 1,200 active merchants (D2C brands, education, SaaS, local services), plus their payers (end customers) |
| Volume | About 0.9 million transactions/month; gross transaction value about INR 180 crore/month |
| Revenue | Merchant discount rate on transactions, plus subscription fees for premium dashboard features |
| Headcount | 50 employees, plus 12 outsourced customer support agents |

### Strategy and drivers for security

- **Partner banks** (acquiring and sponsor bank) send annual security questionnaires and increasingly ask for
  ISO/IEC 27001 certification.
- **Final RBI PA authorisation** depends partly on showing sound IT governance and security controls.
- **PCI DSS v4.0.1**: a QSA pre-assessment is done, and a formal assessment is targeted within 9 months.
- **DPDP Act, 2023**: obligations are being phased in through the DPDP Rules, 2025, and leadership wants to be
  ready.
- **Growth**: the plan is to reach 5,000 merchants in 24 months, which will attract more attackers and
  regulatory attention.

### Organisation structure (50 employees)

| Function | Headcount | Security-relevant notes |
|---|---|---|
| Leadership (CEO, CTO, CFO, COO) | 4 | CTO is the de facto security owner; there is no CISO or Information Security Manager |
| Engineering (backend, frontend, mobile SDK, QA, 2 Cloud & DevOps) | 20 | Builds and runs the platform; production access is broad |
| Operations & Risk (onboarding/KYC, settlement, fraud & risk, merchant support L2) | 10 | Use the internal Ops Console; can initiate refunds |
| Sales & Partnerships | 6 | Handle merchant contracts and pricing |
| Product & Design | 5 | Have access to analytics data |
| Finance, Legal & Compliance | 3 | Head of Legal & Compliance also acts as Grievance Officer |
| HR & Admin | 2 | Own HR records, the laptop register and office facilities |

**Outsourced:** SupportCo (fictional), a Pune-based BPO, runs L1 customer and merchant support with 12 agents
working from the vendor's premises.

---

## 2. Key information assets

| Asset | Description | Location | Classification | Owner (proposed) |
|---|---|---|---|---|
| Transaction data | Payment records, card tokens, last-4 digits, UPI IDs, amounts, merchant IDs, status | RDS PostgreSQL (Mumbai) | Restricted | CTO |
| Merchant KYC data | PAN, GST, bank account proof, masked Aadhaar, director details | S3 (encrypted) | Restricted | Head of Operations |
| Customer personal data | Payer names, phone numbers, email addresses | RDS, helpdesk | Confidential | Head of Legal & Compliance |
| Settlement and payout data | Daily settlement files, merchant bank accounts, payout instructions | S3, bank SFTP, finance mailboxes | Restricted | CFO |
| Source code and IaC | Payment platform code, Terraform, CI/CD workflows | GitHub | Restricted | Engineering Lead |
| Secrets and keys | Bank and partner API credentials, KMS keys, webhook signing secrets | AWS Secrets Manager, KMS (some hard-coded in code history) | Restricted | CTO |
| Security and audit logs | CloudTrail, application, load balancer and WAF logs | CloudWatch Logs | Confidential | Cloud & DevOps Lead |
| Corporate information | Contracts, board papers, HR records, financials | Google Workspace, HRMS | Confidential | CEO / CFO / HR |
| Endpoints | 54 company laptops (macOS and Windows) | Staff, office, home | Internal | HR & Admin Manager |

> SecurePay **never stores full card numbers (PAN)**. Card data is entered in the partner processor's hosted
> fields (a PCI DSS Level 1 service provider) and exchanged for a token. SecurePay is still in PCI DSS scope as a
> service provider because its checkout pages and APIs affect the security of the card data flow.

---

## 3. Systems and technology

| Layer | Components |
|---|---|
| Customer-facing | Hosted checkout page and JS SDK, payment links, merchant dashboard (React), public REST Payment API, merchant webhooks |
| Internal | **Ops Console** (KYC review, refunds, merchant management), support console (read-only), reconciliation service |
| Cloud (AWS) | AWS Organizations with separate production and non-production accounts; ap-south-1 (Mumbai) primary, Multi-AZ; ALB + AWS WAF; ECS Fargate; RDS PostgreSQL Multi-AZ; ElastiCache Redis; S3; KMS; Secrets Manager (partly adopted); CloudTrail; CloudWatch; backups copied to ap-south-2 (Hyderabad) |
| Engineering | GitHub (code, branch protection, Dependabot), GitHub Actions CI/CD to Amazon ECR and ECS, Terraform (~70% of infra) |
| Corporate IT | Google Workspace (SSO with enforced 2-step verification, email, Drive), Slack, Jira, HRMS, password manager, SaaS helpdesk (used by SupportCo) |
| Endpoints | Company laptops managed by MDM: full-disk encryption, screen lock, OS updates, anti-malware |
| Office | Single floor in a managed building in Bengaluru: Wi-Fi and ISP router in a locked cabinet; no servers |
| Third parties | Acquiring bank, UPI sponsor bank (PSP) and NPCI, partner card processor (tokenisation), KYC verification API, SMS and email gateways, SupportCo, CERT-In empanelled VAPT firm, PCI QSA |

---

## 4. Principal data flows

```
1. Card checkout
   Payer browser -> SecurePay hosted checkout -> partner processor hosted fields (PCI L1)
   -> card token -> SecurePay Payment API -> acquiring bank -> card network -> result
   -> SecurePay -> signed webhook to merchant

2. UPI payment
   Payer UPI app -> sponsor bank PSP -> NPCI -> sponsor bank -> SecurePay callback (signed)

3. Merchant onboarding (KYC)
   Merchant uploads documents -> S3 (KMS-encrypted) -> KYC verification API
   -> Operations review in Ops Console -> merchant activated

4. Settlement and payout
   Acquiring bank settlement file (SFTP) -> reconciliation service -> payout file
   -> bank payout API (single finance approver)

5. Customer support
   Payer/merchant -> SaaS helpdesk -> SupportCo agents (shared logins) -> support console
   -> escalation to SecurePay Operations

6. Software delivery
   Developer -> GitHub pull request (1 reviewer) -> GitHub Actions -> Amazon ECR -> ECS (production)
   (production database snapshots are periodically copied to staging for debugging)
```

Trust boundaries that matter most: the public internet to checkout/API, SecurePay to banks and partners,
SecurePay to SupportCo, and engineers' laptops to the AWS production account.

---

## 5. Regulatory and contractual obligations

| Obligation | Key requirements for SecurePay |
|---|---|
| **Digital Personal Data Protection Act, 2023** and **DPDP Rules, 2025** | SecurePay is a **Data Fiduciary**. It must take reasonable security safeguards, give notice and obtain consent, honour Data Principal rights, limit retention, notify the Data Protection Board and affected individuals of breaches, and hold processors (e.g. SupportCo) to its standards. Penalties reach up to INR 250 crore for failing to take reasonable security safeguards. |
| **RBI Guidelines on Regulation of Payment Aggregators and Payment Gateways** (2020, as amended) | Authorisation and net-worth conditions, merchant due diligence, no storage of card data, baseline technology and security recommendations, incident reporting to RBI. |
| **RBI directive on storage of payment system data** (2018) | All payment data must be stored only in India; this drives the choice of AWS Mumbai and Hyderabad regions. |
| **CERT-In Directions** under section 70B of the IT Act (April 2022) | Report specified cyber incidents to CERT-In within **6 hours**; keep ICT system logs for **180 days** within India; synchronise clocks to NIC/NPL NTP or traceable sources; nominate a point of contact. |
| **PCI DSS v4.0.1** | Required by card networks through the acquirer. SecurePay is a service provider whose systems affect cardholder data security. |
| **Information Technology Act, 2000** | Section 43A (compensation for failing to protect data), offences relating to computer systems. |
| **PMLA / KYC requirements** | Merchant KYC and transaction record-keeping for the statutory periods. |
| **Contracts** | Partner bank agreements (security questionnaires, audit rights, breach notification), merchant terms of service, SupportCo master services agreement. |

---

## 6. Stakeholders and interested parties

| Stakeholder | Interest / expectation |
|---|---|
| CEO and Board | Business continuity, regulatory standing, investor confidence, certification for sales |
| CTO (interim security owner) | Practical, prioritised controls that do not slow delivery |
| Head of Legal & Compliance | DPDP, RBI and contractual compliance; incident notification |
| Head of Customer Operations | Secure, efficient vendor-supported operations |
| Employees | Clear rules, usable tools, privacy of their own data |
| Merchants | Availability, settlement accuracy, protection of their and their customers' data |
| Payers (Data Principals) | Safe payments, privacy, grievance redress |
| RBI | Sound governance, security and continuity of payment services |
| CERT-In | Timely incident reporting, log retention |
| Data Protection Board of India | DPDP compliance, breach notification |
| Acquiring and sponsor banks, card networks, NPCI | PCI DSS compliance, secure integration, incident notification |
| Investors | Risk management, valuation protection |
| SupportCo, AWS and other suppliers | Clear contractual requirements |
| PCI QSA, VAPT firm, future ISO certification body | Access to evidence and systems for assurance |

---

## 7. Current security posture (summary)

**In place:** cloud-native architecture in India-only regions, encryption in transit and at rest, card
tokenisation, cross-region tested backups, Google Workspace SSO with MFA, managed and encrypted laptops,
pre-employment background verification, annual VAPT, GitHub branch protection and Dependabot, 70%
infrastructure-as-code, managed office access control.

**Missing or weak:** formal ISMS (no approved policy, roles, risk assessment, internal audit or management
review); privileged access management; security monitoring and incident response; supplier security; DPDP
compliance programme; threat intelligence; secure coding standard and SAST; equipment disposal.

**Recent incident (assumed):** In March 2026 a credential-stuffing attack against merchant dashboard logins
compromised 14 merchant accounts. It was detected about 19 hours later through a merchant complaint and handled
ad hoc in Slack. No CERT-In report was assessed or filed and no post-incident review was recorded.

---

## 8. Key assumptions

The full list is in [`data/assumptions.csv`](data/assumptions.csv) and Appendix C of the report. Key points:

1. All facts about SecurePay are fictional and assumed as at October 2026.
2. No interviews, system access or evidence sampling were performed; "evidence requested" lists what a real
   assessor would ask for.
3. AWS data centre physical controls are inherited and verified through AWS assurance reports.
4. Card data never touches SecurePay storage (partner tokenisation), but PCI DSS still applies.
