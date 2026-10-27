# Study Guide: ISO/IEC 27001:2022 Gap Assessment of SecurePay Technologies

A guide for interview preparation. It explains the standard in plain English, the risk model used, the
reasoning behind every rating in this project, how a real engagement would differ, and 25 likely interview
questions with model answers.

> Reminder: SecurePay is fictional and the current state is assumed. Say so up front in interviews; it shows
> integrity, and interviewers respect a clearly scoped self-directed project.

---

## Contents

1. [ISO/IEC 27001 in plain English](#1-isoiec-27001-in-plain-english)
2. [The risk model and how it was applied](#2-the-risk-model-and-how-it-was-applied)
3. [Control-by-control notes (all 20 assessed controls)](#3-control-by-control-notes)
4. [How a real engagement would differ](#4-how-a-real-engagement-would-differ)
5. [25 likely interview questions with model answers](#5-25-likely-interview-questions)
6. [One-page cheat sheet](#6-one-page-cheat-sheet)

---

## 1. ISO/IEC 27001 in plain English

### What it is

ISO/IEC 27001 is the international standard for an **Information Security Management System (ISMS)**: a
structured, risk-based way for an organisation to manage information security, keep improving it, and prove it
to others. An organisation can be **certified** against ISO/IEC 27001 by an accredited certification body.

- **ISO/IEC 27001:2022** contains the requirements (what you must do). You are certified against this one.
- **ISO/IEC 27002:2022** is guidance on implementing each Annex A control (how you might do it). You cannot be
  certified against 27002.
- Related standards: 27005 (information security risk management), 27017 (cloud), 27018 (PII in public
  clouds), 27701 (privacy information management extension).

### Clauses vs Annex A vs SoA

| Part | What it is | Mandatory? |
|---|---|---|
| **Clauses 4–10** | Requirements for the *management system*: context, leadership, planning (risk), support, operation, performance evaluation, improvement | **Yes, all of them.** No exclusions are allowed. |
| **Annex A** | A reference list of 93 information security *controls* | You must compare your risk treatment with Annex A, but you implement only the controls your risk assessment shows you need |
| **Statement of Applicability (SoA)** | A document (required by Clause 6.1.3 d) listing every Annex A control, whether it is applicable, why it is included or excluded, and whether it is implemented | **Yes.** It is one of the key documents an auditor reviews |

A simple way to say it: *the clauses are the engine (how you manage security); Annex A is the toolbox (what
controls you can use); the SoA is the inventory of which tools you chose and why.*

Clauses 1–3 (scope, normative references, terms) are introductory and contain no requirements.

### The PDCA cycle

ISO management system standards follow **Plan–Do–Check–Act**:

| PDCA | Clauses | In practice |
|---|---|---|
| **Plan** | 4 Context, 5 Leadership, 6 Planning | Define scope and interested parties; get leadership commitment and a policy; assess risks; pick controls; set objectives |
| **Do** | 7 Support, 8 Operation | Provide resources, competence, awareness, communication and documented information; run the risk treatment plan and controls |
| **Check** | 9 Performance evaluation | Monitor and measure; internal audit; management review |
| **Act** | 10 Improvement | Fix nonconformities, find root causes, continually improve |

In this project SecurePay has parts of Plan and Do (controls exist because partner banks and PCI DSS demand
them) but almost nothing in Check and Act. That is why Clauses 9 and 10 are non-conformant.

### The four 2022 themes

| Theme | Annex A section | Number of controls | Examples |
|---|---|---|---|
| Organizational | A.5 | 37 | Policies, supplier security, incident management, cloud services, privacy |
| People | A.6 | 8 | Screening, awareness training, remote working |
| Physical | A.7 | 14 | Physical entry, clear desk, equipment disposal |
| Technological | A.8 | 34 | Privileged access, authentication, vulnerability management, logging, secure coding |
| **Total** | | **93** | |

ISO/IEC 27002:2022 also gives each control **attributes** so you can filter controls in different ways:
control type (preventive, detective, corrective), security properties (confidentiality, integrity,
availability), cybersecurity concepts (Identify, Protect, Detect, Respond, Recover), operational capabilities
and security domains.

### What changed from 2013 to 2022

- **Controls:** 114 controls in 14 domains (A.5–A.18) were restructured into **93 controls in 4 themes**.
  Roughly: **11 new**, **24 merged** from older controls, and **58 updated**. No security topic was really
  removed; many were consolidated.
- **The 11 new controls:** A.5.7 Threat intelligence, A.5.23 Information security for use of cloud services,
  A.5.30 ICT readiness for business continuity, A.7.4 Physical security monitoring, A.8.9 Configuration
  management, A.8.10 Information deletion, A.8.11 Data masking, A.8.12 Data leakage prevention, A.8.16
  Monitoring activities, A.8.23 Web filtering, A.8.28 Secure coding.
  *This project assessed five of them: A.5.7, A.5.23, A.8.9, A.8.16 and A.8.28.*
- **Clause changes (small but testable):** 4.2 now asks which interested-party requirements will be addressed
  through the ISMS; 4.4 refers explicitly to the processes needed; a new **6.3 Planning of changes**; 6.2
  objectives must be monitored; 8.1 covers criteria for processes and control of externally provided
  processes; 9.2 and 9.3 were split into sub-clauses (9.3 adds changes in interested parties' needs as a
  management review input).
- **Transition:** certified organisations had until **31 October 2025** to move to the 2022 version.
- **Amendment 1 (2024)** added climate change considerations to Clauses 4.1 and 4.2.

---

## 2. The risk model and how it was applied

### Core idea

Risk is about **uncertainty that affects objectives**. In information security, a risk scenario is usually
written as:

> **Asset** (what we protect) + **Threat** (who or what could cause harm) + **Vulnerability** (the weakness the
> threat exploits) leads to an **Impact**.

Example (R01): *the AWS production environment* (asset) could be taken over by *an external attacker using a
stolen engineer credential* (threat) because of *standing admin rights and shared root/DB credentials*
(vulnerability). The result would be full compromise of payment and customer data (impact).

### Likelihood × Impact

| Score | Likelihood | Impact |
|---|---|---|
| 1 | Rare: not expected in 3 years | Negligible: < INR 5 lakh, no personal data, < 15 min disruption |
| 2 | Unlikely: could occur in 3 years | Minor: INR 5–25 lakh, < 1,000 records, < 1 h outage |
| 3 | Possible: could occur this year | Moderate: INR 25 lakh–1 crore, regulatory inquiry, 1–10k records |
| 4 | Likely: expected this year | Major: INR 1–5 crore, formal regulatory action, 10–100k records, 4–24 h outage |
| 5 | Almost certain: expected within months | Severe: > INR 5 crore, DPDP penalty or RBI suspension, > 100k records, > 24 h outage |

**Risk score = Likelihood × Impact (1–25).** Bands: **Low 1–5, Medium 6–10, High 12–16, Critical 20–25**.
(Scores 11, 13, 14 and 17–19 cannot occur with a 5 × 5 product, so the bands have no gaps.)

Impact is judged on the **worst credible** of financial, regulatory, customer/data and operational effects.

### Risk appetite

Risk appetite is the amount and type of risk an organisation is willing to accept to achieve its objectives.
The assumed appetite for SecurePay:

- **Low appetite** for risks to payment data, personal data and regulatory standing (its licence to operate).
- Scores of **12 or more** (High and Critical) are above appetite and **must be treated**.
- **Medium** risks may be accepted with documented CEO sign-off; **Low** risks are accepted and monitored.

### The four treatment options

| Option | Meaning | Example in this project |
|---|---|---|
| **Mitigate (modify)** | Add or improve controls to reduce likelihood and/or impact | R01: JIT admin access, MFA, root lockdown (20 → 10) |
| **Transfer (share)** | Shift the financial impact to a third party, e.g. insurance or contract | R06: cyber insurance with social-engineering fraud cover for BEC payout fraud (12 → 6) |
| **Avoid** | Stop the activity that creates the risk | R07: stop copying production data into staging (9 → 3) |
| **Accept (retain)** | Knowingly keep the risk, with management approval | R08: AWS regional outage. Multi-AZ and cross-region backups exist; multi-region active-active costs too much at this scale (8, within appetite) |

Points to make in interviews:

- **Transfer never transfers accountability.** SecurePay is still the Data Fiduciary under DPDP even if
  SupportCo causes the breach, and insurance does not pay regulatory penalties in many cases. That is why R06
  also includes supporting controls (dual approval, call-back verification).
- **Accepting a risk is a decision, not neglect.** It needs an owner, a rationale, a review date and sign-off.

### Inherent vs target (residual) risk

- **Inherent** (current) risk is scored on today's controls.
- **Target** risk is the expected score once the treatment plan is delivered. It is what the owner signs up
  to. After treatment, every risk in the register is Medium or Low (within appetite).
- Clause 6.1.3 requires risk owners to approve the risk treatment plan and accept the residual risk.

### How the register links to controls and the SoA

Each risk lists the related Annex A controls. The control gaps are the vulnerabilities, and the
recommendations are the treatment. In a real ISMS: risk assessment (6.1.2) → risk treatment and control
selection (6.1.3) → compare with Annex A → SoA → risk treatment plan → operate (8.2, 8.3) → monitor (9).

| Risk | Inherent | Treatment | Target |
|---|---|---|---|
| R01 Privileged account compromise | 4×5 = **20 Critical** | Mitigate | 2×5 = 10 Medium |
| R02 PII exposure via support vendor | 4×4 = **16 High** | Mitigate | 2×4 = 8 Medium |
| R03 Unpatched vulnerabilities exploited | 4×4 = **16 High** | Mitigate | 2×4 = 8 Medium |
| R04 Undetected intrusion / missed CERT-In 6 h | 3×5 = **15 High** | Mitigate | 2×4 = 8 Medium |
| R05 DPDP Act penalty | 3×5 = **15 High** | Mitigate | 2×5 = 10 Medium |
| R06 BEC payout fraud | 3×4 = **12 High** | Transfer | 2×3 = 6 Medium |
| R07 Production PII in staging | 3×3 = **9 Medium** | Avoid | 1×3 = 3 Low |
| R08 AWS region outage | 2×4 = **8 Medium** | Accept | 2×4 = 8 Medium |

Why R01's impact stays at 5 after treatment: controls make compromise much **less likely**, but if it did
happen, full admin access to production is still catastrophic. Mitigation usually reduces likelihood more than
impact.

---

## 3. Control-by-control notes

For each control: **what it requires** (paraphrased), **why it matters for a fintech**, **why it got this
rating**, **evidence that would prove conformance**, and **the fix**.

Rating key: 🟢 Conformant · 🟡 Partially conformant · 🔴 Non-conformant. Maturity is current / target on 0–5.

### Organizational controls (A.5)

#### A.5.1 Policies for information security: 🟡 Partial · Medium · maturity 1/3
- **Requires:** a top-level security policy approved by management, supported by topic-specific policies,
  communicated, acknowledged and reviewed regularly.
- **Why it matters:** policy is how leadership sets direction. RBI, partner banks and auditors ask for it
  first, and without it no other rule is enforceable.
- **Rating reasoning:** a draft exists (so not 🔴), but it is unapproved, uncommunicated, has no review cycle
  and no topic-specific policies. The key test is *management approval*, which fails.
- **Evidence:** signed policy with version history; policy index; acknowledgement records from the HRMS; review
  minutes.
- **Fix:** CEO-approved policy, about eight topic-specific policies, annual e-acknowledgement and annual review.

#### A.5.7 Threat intelligence (new in 2022): 🔴 Non-conformant · Medium · 0/3
- **Requires:** collect information about relevant threats, analyse it, and use it to improve controls and
  decisions (strategic, tactical and operational levels).
- **Why it matters:** payment companies face targeted threats such as card-testing, credential stuffing,
  malicious npm packages and BEC on settlement teams. CERT-In publishes sector advisories.
- **Rating reasoning:** no owner, no sources, no process, and a relevant CERT-In advisory was missed. Nothing
  exists to rate as partial.
- **Why only Medium risk:** the gap makes other risks worse (R03, R04) rather than causing harm by itself.
- **Evidence:** procedure; list of sources; triage log showing advisories and actions; quarterly threat briefing.
- **Fix:** ISM owns it; subscribe to CERT-In, AWS and GitHub advisories and a fintech sharing community;
  fortnightly triage; quarterly briefing; later feed IOCs into WAF and GuardDuty. Planned for 6–12 months
  because monitoring (A.8.16) must exist first to make intelligence actionable.

#### A.5.9 Inventory of information and other associated assets: 🟡 Partial · Medium · 2/3
- **Requires:** an up-to-date inventory of information and associated assets, each with an owner.
- **Why it matters:** you cannot protect, classify, review access to, or map personal data (DPDP) for assets
  you do not know about. It is also the starting point for risk assessment.
- **Rating reasoning:** AWS tagging (~80%) and a laptop register exist, so there is a repeatable practice
  (maturity 2). But there are no information assets, no SaaS catalogue (~25 apps), no owners and stale data.
- **Evidence:** register with owner, classification and location; AWS Config export; SaaS discovery;
  reconciliation to MDM; review records.
- **Fix:** single register covering information, SaaS, cloud and endpoints; owners and classification;
  mandatory AWS tag policies; monthly reconciliation; quarterly review.

#### A.5.19 Information security in supplier relationships: 🔴 Non-conformant · High · 1/3
- **Requires:** processes to manage security risks from suppliers, including due diligence before onboarding
  and agreed rules for their access to your information.
- **Why it matters:** fintechs depend on suppliers (cloud, BPOs, KYC APIs). Under the DPDP Act, SupportCo is a
  **Data Processor**; SecurePay as **Data Fiduciary** stays accountable for its failures. RBI also expects
  outsourcing risk to be managed.
- **Rating reasoning:** the vendor with the most customer PII access was chosen on cost, never assessed,
  shares logins and has no security clauses. A generic confidentiality clause does not meet the requirement
  (maturity 1, but still 🔴).
- **Evidence:** supplier policy; tiered supplier inventory; questionnaires and SOC 2 / ISO certificates; DPA
  with security schedule; supplier account lists and access reviews.
- **Fix:** policy and tiering; immediate SupportCo assessment; DPA (minimum controls, 6-hour breach
  notification, audit rights, data return and deletion, sub-processor approval); named MFA accounts; field
  masking; quarterly access review.

#### A.5.23 Information security for use of cloud services (new): 🟡 Partial · Medium · 2/3
- **Requires:** processes for acquiring, using, managing and exiting cloud services, including a clear split of
  security responsibilities with the provider.
- **Why it matters:** SecurePay is 100% on AWS. Most cloud breaches come from the *customer's* side of the
  shared responsibility model (misconfiguration, identity).
- **Rating reasoning:** strong technical basics (India regions for RBI localisation, account separation,
  encryption, S3 Block Public Access), but no governance: no policy, no responsibility matrix, no posture
  monitoring, uncontrolled SaaS, no exit plan.
- **Evidence:** cloud standard; shared-responsibility matrix; review of AWS SOC 2 / PCI AOC from AWS Artifact;
  Security Hub findings; SaaS approvals; exit plan.
- **Fix:** cloud standard and matrix; Security Hub with CIS and PCI DSS standards; annual review of AWS
  assurance reports; SaaS approval workflow; exit and portability plan.

#### A.5.24 Incident management planning and preparation: 🔴 Non-conformant · High · 1/3
- **Requires:** plan and prepare for incidents with defined processes, roles and responsibilities, communicated
  in advance.
- **Why it matters:** **CERT-In requires reporting within 6 hours**; DPDP requires breach intimation to the
  Data Protection Board and affected individuals; RBI and partner banks expect notification. Payment fraud
  incidents escalate quickly.
- **Rating reasoning:** no plan, roles, severity matrix, contact list or reporting channel. The March 2026
  incident proves it: handled ad hoc, no regulatory reporting decision, no lessons learned.
- **Evidence:** IR plan; RACI; severity matrix; regulatory notification matrix; incident log; tabletop reports;
  on-call rota.
- **Fix:** approve an IR plan (prepare, detect, triage, contain, eradicate, recover, review); IR team with
  deputies; notification templates; single reporting channel; tabletop within 90 days; consider an IR retainer.

#### A.5.34 Privacy and protection of PII: 🟡 Partial · High · 1/3
- **Requires:** identify and meet the privacy and PII protection requirements of applicable law, regulation and
  contracts.
- **Why it matters:** the **DPDP Act 2023** applies (penalties up to INR 250 crore for failing to take
  reasonable security safeguards). Payment data is sensitive and customers expect privacy.
- **Rating reasoning:** some measures exist (privacy notice, consent capture, no card storage, Aadhaar
  masking), so it is not 🔴. But there is no data inventory, retention schedule, rights process, breach
  procedure or accountable owner, and production PII is copied to staging. High risk because of the
  regulatory exposure.
- **Evidence:** personal data inventory and records of processing; DPDP gap assessment; notices and consent
  logs; retention schedule and deletion logs; rights-request log; privacy owner appointment; DPAs.
- **Fix:** DPDP gap assessment; data inventory and flow maps; retention schedule respecting RBI/PMLA minimums,
  automated with S3 lifecycle rules; rights and grievance process; accountable owner; no production PII in
  non-production; DPDP breach steps in the IR plan.

### People controls (A.6)

#### A.6.1 Screening: 🟢 Conformant · Low · 3/3
- **Requires:** background checks before joining (and later where appropriate), proportionate to the role and
  lawful.
- **Why it matters:** insiders at payment firms can commit fraud or leak data. Background verification is
  standard Indian HR practice and expected by banks.
- **Rating reasoning:** all hires are verified by an accredited agency, with extra checks for privileged and
  finance roles, and access is granted only after clearance. This meets the requirement in design and
  operation. Observations (no written role-based standard; vendor staff not covered) are minor.
- **Evidence:** HR checklist; a sample of BGV reports for recent joiners; consent forms; proof that checks were
  completed before access.
- **Fix (improvement):** written role-based standard; contractual screening requirement for suppliers;
  periodic re-screening for privileged roles.

#### A.6.3 Awareness, education and training: 🟡 Partial · Medium · 1/3
- **Requires:** suitable awareness, education and training for staff and relevant parties, with regular updates.
- **Why it matters:** phishing and BEC are the most common entry points in financial services. Developers need
  secure coding skills and finance staff need fraud awareness.
- **Rating reasoning:** one 20-minute induction slide exists, so not 🔴. But there is no refresher, no
  role-based training, no phishing simulation, no tracking and no vendor coverage.
- **Evidence:** training plan; LMS completion data; phishing simulation results; role-based records; vendor
  training records.
- **Fix:** annual programme with ≥95% completion; quarterly phishing simulations; role-based modules
  (engineers, finance, support); vendor agents included; metrics to management.

#### A.6.7 Remote working: 🟢 Conformant · Low · 3/3
- **Requires:** security measures for information accessed, processed or stored outside the premises.
- **Why it matters:** hybrid working means engineers reach production from home networks.
- **Rating reasoning:** company laptops under MDM with full-disk encryption, screen lock, updates and
  anti-malware; SSO with MFA; handbook rules acknowledged. Minor observations: 3 of 54 laptops have overdue
  updates, and personal phones are unmanaged.
- **Evidence:** remote working policy and acknowledgements; MDM compliance report; device configuration sample;
  SSO/MFA settings.
- **Fix (improvement):** device compliance as a condition of SSO; app protection for mobiles; monthly MDM vs
  asset register reconciliation.

### Physical controls (A.7)

#### A.7.2 Physical entry: 🟢 Conformant · Low · 3/3
- **Requires:** entry controls so only authorised people reach secure areas.
- **Why it matters:** the office holds laptops with production access. There is no server room, which limits
  physical risk.
- **Rating reasoning:** managed building with reception, visitor ID checks, RFID cards, logged card doors and
  card deactivation on exit. Minor observations: visitors are not escorted and cards are not reviewed.
- **Evidence:** facility procedure; card issuance and revocation records reconciled to leavers; visitor logs;
  door logs; CCTV coverage.
- **Fix (improvement):** visitor badges and escort rule; quarterly card review against the HR roster.

#### A.7.14 Secure disposal or re-use of equipment: 🔴 Non-conformant · Medium · 0/3
- **Requires:** before disposal or re-use, verify that sensitive data and licensed software are removed or
  securely overwritten.
- **Why it matters:** laptops hold source code, cached credentials and data exports.
- **Rating reasoning:** laptops are reissued after a manual profile deletion only, six were sold informally
  without sanitisation, and there is no procedure or log. Full-disk encryption reduces the risk (hence Medium,
  not High), but the control is still absent.
- **Evidence:** procedure; disposal log; certificates of data destruction from an authorised e-waste
  recycler; MDM wipe records.
- **Fix:** MDM wipe or cryptographic erase before reissue; authorised recycler only (also needed for the
  E-Waste Rules 2022); disposal log linked to the asset register.

### Technological controls (A.8)

#### A.8.2 Privileged access rights: 🔴 Non-conformant · **Critical** · 1/3
- **Requires:** restrict and manage privileged access so only authorised people have it, only for as long as
  needed, and its use is controlled and monitored.
- **Why it matters:** admin access to AWS and the production database is the "keys to the kingdom" for a
  payment platform. Most serious cloud breaches involve compromised privileged identities.
- **Rating reasoning:** five permanent AWS admins (two no longer need it), shared root credentials, a shared DB
  superuser known to seven people, and no reviews or monitoring. It fails every element of the requirement.
  Critical because likelihood is high (4: phishing and laptop malware are common) and impact is severe (5).
- **Evidence:** PAM procedure; list of privileged accounts across AWS, DB, GitHub owners and Workspace super
  admins; approvals; review records; CloudTrail root usage; break-glass procedure.
- **Fix:** AWS IAM Identity Center with MFA and just-in-time elevation; remove admin IAM users; root locked with
  hardware MFA and alerting; individual IAM-authenticated DB roles with session logging; monthly then
  quarterly reviews; at most two GitHub owners and two Workspace super admins.

#### A.8.5 Secure authentication: 🟡 Partial · High · 2/3
- **Requires:** secure authentication suited to the sensitivity of the information, e.g. MFA for high-risk
  access.
- **Why it matters:** the Ops Console can view PII and **initiate refunds**, so it moves money. Merchant
  accounts were already attacked by credential stuffing in March 2026.
- **Rating reasoning:** strong for corporate identity (Workspace SSO + MFA, AWS MFA), so partial rather than
  🔴. But the money-moving and PII applications lack MFA, lockout and brute-force protection, and vendors share
  credentials.
- **Evidence:** authentication standard; MFA enforcement reports; Ops Console and dashboard auth configuration;
  rate-limit test results; list of accounts without MFA.
- **Fix:** Ops Console behind SSO with MFA; named vendor accounts; mandatory 2FA for merchant users with
  refund or payout rights; rate limiting, lockout and bot protection; breached-password checks; FIDO2 keys for
  admins.

#### A.8.8 Management of technical vulnerabilities: 🟡 Partial · High · 2/3
- **Requires:** get timely information about vulnerabilities, assess exposure, and act within defined
  timeframes.
- **Why it matters:** internet-facing payment APIs are scanned by attackers constantly. PCI DSS requires
  quarterly ASV scans and timely patching.
- **Rating reasoning:** identification works (Dependabot, annual CERT-In empanelled VAPT), but remediation does
  not: 4 High VAPT findings open after 9 months (including an IDOR), 17 Critical/High dependency alerts, no
  SLAs, no container or ASV scanning. Finding a problem and not fixing it is the classic "partial".
- **Evidence:** procedure with SLAs; VAPT reports and tracker; Dependabot/SCA dashboards; ECR/Inspector
  scans; ASV reports; risk acceptances.
- **Fix:** SLAs (Critical 7, High 30, Medium 90 days); close and retest the 4 Highs within 30 days; ECR
  enhanced scanning in CI; weekly Dependabot triage; quarterly ASV; twice-yearly VAPT; monthly ageing report.

#### A.8.9 Configuration management (new): 🟡 Partial · Medium · 2/3
- **Requires:** define, document, implement, monitor and review secure configurations (baselines) for
  hardware, software, services and networks.
- **Why it matters:** misconfiguration is a leading cause of cloud breaches. Infrastructure-as-code makes
  configuration reviewable and repeatable.
- **Rating reasoning:** 70% Terraform with peer review is good practice (maturity 2). But there are no
  baselines, no drift detection, manual "snowflake" resources and AWS Config without rules.
- **Evidence:** configuration standard and baselines; Terraform repo and PR history; AWS Config conformance
  results; drift reports; exception register.
- **Fix:** CIS baselines; import manual resources into Terraform; policy-as-code (Checkov/tfsec) in CI; AWS
  Config conformance packs with drift alerts; replace the bastion with SSM Session Manager.

#### A.8.13 Information backup: 🟢 Conformant · Low · 3/3
- **Requires:** keep backups of information, software and systems and test them regularly per an agreed
  policy.
- **Why it matters:** transaction and settlement data must be recoverable for merchants, banks and regulators.
  Ransomware targets backups.
- **Rating reasoning:** RDS PITR with 35-day retention, encrypted cross-region copies (still in India), S3
  versioning and replication, a documented RPO/RTO, and a documented restore test (2h40m, within the 4h RTO).
  Design and operation are both evidenced. Observations: no recurring test schedule, no immutability, and no
  backup of GitHub or Workspace.
- **Evidence:** backup policy; backup configuration; cross-region copies; restore test reports; failure alerts.
- **Fix (improvement):** quarterly restore tests; AWS Backup Vault Lock; third-party GitHub/Workspace backup;
  failure alerting.

#### A.8.16 Monitoring activities (new): 🔴 Non-conformant · High · 1/3
- **Requires:** monitor networks, systems and applications for anomalous behaviour and evaluate possible
  incidents.
- **Why it matters:** you cannot meet CERT-In's 6-hour reporting rule if you do not know you have been
  attacked. Fraud patterns (unusual refunds) also need detection.
- **Rating reasoning:** logs exist but **nobody watches them**; GuardDuty is off; alerts are only for
  performance; the March 2026 attack was found by a customer 19 hours later. Collecting logs is A.8.15
  (logging); A.8.16 is about *monitoring*, which is absent. Retention (30 days) also misses CERT-In (180 days)
  and PCI DSS (12 months).
- **Evidence:** monitoring standard; log source inventory; use-case catalogue; alert triage records; GuardDuty
  history; review evidence; escalation procedure.
- **Fix:** enable GuardDuty, VPC Flow Logs, S3 data events and Security Hub now; one-year write-protected log
  archive; 10–15 priority alerts to on-call; SIEM or MDR for 24x7 coverage within 6–12 months.

#### A.8.24 Use of cryptography: 🟢 Conformant · Low · 3/3
- **Requires:** rules for effective use of cryptography, including key management across the key lifecycle.
- **Why it matters:** payment and personal data must be protected in transit and at rest. PCI DSS and the RBI
  guidelines require strong encryption, and card data must not be stored.
- **Rating reasoning:** TLS 1.2+ (grade A) with HSTS; KMS customer-managed keys with rotation and restrictive
  policies; tokenisation means no PAN storage; HMAC-signed webhooks; Secrets Manager for bank credentials. The
  missing written policy is an observation, not enough to make it partial, because practice is consistent and
  verifiable.
  *(An interviewer may push back that a missing policy should mean "partial". A fair answer: ISO 27002 does
  expect a topic-specific crypto policy, so a stricter assessor could rate it partial. I judged operating
  effectiveness to be strong and the policy gap minor, and recorded it as an observation with a remediation
  item. Showing you know where the judgement line is matters more than which side you pick.)*
- **Evidence:** crypto and key management policy; TLS scans; KMS inventory and rotation; encryption
  configuration; tokenisation architecture and partner AOC; webhook signing review.
- **Fix (improvement):** write the policy (algorithms, key lengths, rotation, crypto-periods); certificate and
  key inventory with expiry alerts; crypto-agility review.

#### A.8.28 Secure coding (new): 🟡 Partial · High · 2/3
- **Requires:** apply secure coding principles throughout development to reduce vulnerabilities.
- **Why it matters:** SecurePay writes its own payment code. Authorisation flaws such as IDOR in payment APIs
  can expose other merchants' data or allow fraud.
- **Rating reasoning:** peer review and an ORM help (maturity 2), but there is no standard, SAST, secret
  scanning or training. Nine hard-coded secrets (one live) and an IDOR show the gap is real.
- **Evidence:** secure coding standard (OWASP ASVS/Top 10); review checklist; SAST/SCA/secret-scanning results;
  sample PRs with security review; training records; threat models.
- **Fix:** rotate secrets now and move them to Secrets Manager; GitHub push protection; ASVS L2 standard and PR
  checklist; SAST/SCA in CI blocking Highs; annual training; threat modelling; security champions.

---

## 4. How a real engagement would differ

This project is a **desk-based assessment against an assumed current state**. A real consulting engagement
would gather and test evidence. Key differences:

| Area | This project | Real engagement |
|---|---|---|
| Kick-off and scoping | Self-defined | Engagement letter or SOW, kick-off meeting, agreed scope, timelines, points of contact, information request list (IRL) |
| Information gathering | Assumptions | **Document review** of policies, procedures, contracts, architecture diagrams, previous audit, VAPT and PCI reports |
| Interviews | None | **Interviews and walkthroughs** with control owners: CTO, DevOps, Engineering Lead, HR, Legal, Finance, Customer Ops and the vendor. Ask "show me", not just "tell me" |
| Testing | Not performed | **Test of design** (would the control work as designed?) and **test of operating effectiveness** (did it work over the period?) |
| Evidence sampling | Not performed | Select samples from populations, e.g. 10–25 joiners from the year to test screening before access; all leavers in the quarter to test timely access removal; a sample of PRs for peer review; a sample of changes, incidents and VAPT findings for timely closure |
| Technical validation | Not performed | Read-only review of AWS IAM, Security Hub/Config output, GitHub settings, MDM reports; possibly a configuration review or cloud security posture scan with consent |
| Rating | Assessor judgement on assumed facts | Judgement supported by evidence, with working papers and a reviewer (manager or partner) quality-checking ratings |
| Validation | None | **Draft findings validated with the client** to correct factual errors; management responses, owners and target dates added to each finding |
| Reporting | Single author | Executive presentation to leadership or the audit committee; detailed report; finding tracker handed over |
| Limitations | Fictional | Point-in-time; sample-based (not every transaction tested); reliance on client-provided information; not an audit opinion unless contracted as one |

Other things to mention:

- **Professional scepticism:** a policy existing is not the same as a control operating. Always look for
  evidence of operation (logs, tickets, sign-offs, dates).
- **Independence:** the assessor should not audit their own work. If the same firm later implements the
  remediation, the certification audit must be done by an independent accredited body.
- **Confidentiality:** client evidence is handled under NDA. Findings are sensitive (they are a roadmap for an
  attacker).
- **Gap assessment vs internal audit vs certification audit:** a gap assessment advises on readiness; an
  internal audit (Clause 9.2) checks the ISMS for the organisation; a certification audit (Stage 1 document
  review, Stage 2 implementation) is performed by an accredited certification body and leads to a 3-year
  certificate with annual surveillance audits.

---

## 5. 25 likely interview questions

**1. Walk me through this project in two minutes.**
> I did a self-directed ISO 27001:2022 gap assessment of a fictional 50-person Indian payment aggregator,
> SecurePay. I wrote an organisation profile covering assets, data flows, and DPDP, RBI, CERT-In and PCI DSS
> obligations, then assessed 20 Annex A controls across all four themes, including five of the new 2022
> controls. For each control I recorded the requirement in my own words, the assumed current state, the
> evidence I'd request, a conformance status, maturity, the gap, a risk rating and a recommendation. The result
> was 5 conformant, 9 partial and 6 non-conformant, average maturity 1.7 out of 5. I reviewed Clauses 4–10,
> built a risk register of the top eight risks with likelihood × impact scoring and treatments, drafted an SoA
> for all 93 controls, and produced a 0–3, 3–6 and 6–12 month roadmap. The PDF report is generated from CSV
> data with a Python script. The top priorities were privileged access, detection and incident response, and
> third-party and privacy risk.

**2. Why did you choose those 20 controls?**
> Relevance to a cloud-hosted payments business and coverage of all four themes. I covered governance
> foundations (policy, inventory), the business's biggest dependencies (cloud, the support vendor), the
> regulatory drivers (privacy, incident reporting) and the technical controls that most directly protect
> payment data: privileged access, authentication, vulnerabilities, configuration, monitoring, cryptography,
> backup and secure coding. I deliberately included new 2022 controls because they reflect modern threats and
> are often where organisations moving from 2013 have gaps.

**3. What is the difference between ISO 27001 and ISO 27002?**
> 27001 contains the certifiable requirements: Clauses 4–10 for the management system and Annex A as the
> control reference list. 27002 is implementation guidance for each control, with purpose, guidance and
> attributes. You certify against 27001 and use 27002 to decide how to implement.

**4. What is a Statement of Applicability, and can you exclude controls?**
> The SoA is required by Clause 6.1.3. It lists all 93 Annex A controls, whether each is applicable, the
> justification for including or excluding it, and its implementation status. You can exclude controls if
> your risk assessment and context justify it. I excluded three: A.7.6 working in secure areas (no server rooms
> or data centres), A.7.12 cabling security (cabling owned by the building and AWS), and A.8.30 outsourced
> development (all development is in-house). Data centre physical controls I kept as applicable but inherited
> from AWS, verified through AWS's SOC 2 and PCI AOC. You cannot exclude any Clause 4–10 requirement.

**5. Can an organisation be certified if it implements all Annex A controls but ignores Clauses 4–10?**
> No. Certification is against the management system. Without context, leadership, risk assessment, internal
> audit, management review and corrective action, there is no ISMS, just a set of controls. In my assessment,
> SecurePay has several decent controls but Clauses 6, 9 and 10 are non-conformant. Those would be major
> nonconformities at a certification audit.

**6. How did you decide between "partially conformant" and "non-conformant"?**
> Non-conformant means the control is absent or so ineffective that the requirement's intent isn't met.
> Partial means a meaningful part exists or operates informally, but key elements are missing. For example,
> vulnerability management is partial because Dependabot and annual VAPT identify issues, but there are no SLAs
> and findings stay open. Supplier security is non-conformant even though there's a confidentiality clause,
> because there's no due diligence, no security requirements and shared logins. That clause doesn't meet the
> intent. I also used a separate maturity score so the rating isn't just binary.

**7. Explain your risk methodology. What are its weaknesses?**
> Qualitative 5 × 5: likelihood and impact are each scored 1–5 against defined descriptors (impact covers
> financial, regulatory, customer/data and operational), multiplied to 1–25, and banded Low, Medium, High,
> Critical. Each risk is an asset–threat–vulnerability scenario tied to control gaps. Weaknesses: it is
> subjective, ordinal numbers aren't truly multiplicative, and similar scores can hide different profiles (a
> 4×4 and a 2×5 behave differently). Mitigations: clear descriptors, calibration with stakeholders, and for
> key risks, a quantitative approach such as FAIR to express loss in rupees.

**8. What is risk appetite, and how did you use it?**
> It's how much risk the organisation is willing to accept in pursuit of its objectives. For SecurePay I
> assumed a low appetite for risks to payment and personal data and to regulatory standing. Anything scored 12
> or more must be treated; Medium risks can be accepted with CEO sign-off. That's why the regional outage risk
> (8, Medium) was accepted, while every High and Critical risk got a treatment plan bringing it within
> appetite.

**9. Give an example of each treatment option from your register.**
> Mitigate: R01 privileged access. JIT admin, MFA and root lockdown take it from 20 to 10. Transfer: R06 BEC
> payout fraud. Cyber insurance with social-engineering cover transfers the financial loss, backed by dual
> approval. Avoid: R07. Stop copying production data to staging. Accept: R08 AWS regional outage. Multi-AZ and
> cross-region backups exist, active-active multi-region isn't cost-justified yet, so the CEO accepts it with a
> review in 12 months.

**10. Why did you rate privileged access Critical?**
> Five engineers have permanent AWS admin, root and the database superuser are shared, and there's no review or
> monitoring. Likelihood is 4 because phishing and info-stealer malware against engineers are common and one
> credential is enough. Impact is 5 because it means full control of the payment platform and all customer
> data, with DPDP penalties, RBI action and loss of bank partners. It's also the risk that makes other risks
> worse, since an attacker with admin can disable logging and delete backups.

**11. How would you test A.8.5 Secure authentication in a real engagement?**
> Review the authentication standard. Get the MFA enforcement reports from Google Workspace and AWS and the
> list of users without MFA. Inspect the Ops Console and merchant dashboard configuration for MFA, lockout and
> rate limiting, and with permission, observe a login and test lockout in a non-production environment. Sample
> vendor accounts to confirm they're named, not shared. Compare against the policy, for example whether every
> account that can issue refunds has MFA.

**12. What's the difference between test of design and test of operating effectiveness?**
> Design asks whether the control, as described, would address the risk if it worked. Operating effectiveness
> asks whether it actually worked consistently over a period, tested by sampling evidence. A quarterly access
> review procedure might be well designed, but if two of four quarters have no sign-off, it isn't operating
> effectively.

**13. Name the new controls in 2022 and explain one you assessed.**
> Threat intelligence, cloud services security, ICT readiness for business continuity, physical security
> monitoring, configuration management, information deletion, data masking, data leakage prevention,
> monitoring activities, web filtering, and secure coding. I assessed five. A.8.16 Monitoring activities is
> about actively watching for anomalous behaviour, which is different from A.8.15 Logging. SecurePay collects
> logs but nobody reviews them and GuardDuty is off, so a real credential-stuffing attack took 19 hours to
> spot. I rated it non-conformant with High risk.

**14. How does the DPDP Act affect SecurePay?**
> SecurePay is a Data Fiduciary for payers' and merchants' personal data. It must process data lawfully with
> notice and consent (or a legitimate use), take reasonable security safeguards, limit retention, honour Data
> Principal rights, notify the Data Protection Board and affected people of breaches, and ensure processors
> like the support BPO protect the data. Penalties go up to INR 250 crore for failing to take reasonable
> safeguards. That's why A.5.34 and A.5.19 were rated High risk and DPDP non-compliance is R05.

**15. What is the CERT-In 6-hour rule and why does it matter here?**
> CERT-In's April 2022 Directions require specified cyber incidents to be reported within 6 hours of noticing
> them, ICT logs to be kept for 180 days in India, and clocks to be synchronised. SecurePay has no monitoring
> (so it may not notice in time), no IR plan or contact list (so it may not report), and keeps only 30 days of
> logs. That linked A.8.16, A.5.24 and A.8.15 to R04.

**16. How do PCI DSS and ISO 27001 relate?**
> PCI DSS is prescriptive and scoped to cardholder data. ISO 27001 is risk-based and covers the whole
> organisation's information security. They overlap heavily (access control, logging, vulnerability management,
> encryption, incident response), so one set of controls and evidence can serve both. For SecurePay, partner
> tokenisation reduces PCI scope, and an ISMS gives the governance PCI assumes but doesn't build, such as risk
> assessment, management review and improvement.

**17. Explain the shared responsibility model and A.5.23.**
> The cloud provider secures the cloud: data centres, hardware, the hypervisor and managed service
> infrastructure. The customer secures what it puts in the cloud: identities, configuration, data, network
> rules and application code. A.5.23 asks organisations to manage cloud use deliberately: requirements,
> responsibility split, monitoring, and exit. SecurePay's technical setup is good but it hasn't documented the
> split, doesn't monitor posture and has no exit plan, so I rated it partial.

**18. With a limited budget, how did you prioritise the roadmap?**
> By risk reduction per unit of effort, plus dependencies. The 0–3 month quick wins target the Critical and High
> risks with mostly configuration and governance changes that cost little: SSO-based admin roles, MFA, enabling
> GuardDuty, rotating secrets, an IR plan. Appointing an Information Security Manager comes first because that
> role owns later work. Expensive items like MDR or SIEM come in 6–12 months, once alert use cases are proven.

**19. What would you do differently in a real engagement?**
> Collect evidence instead of assuming it: interviews and walkthroughs with control owners, document review,
> sampling for operating effectiveness, read-only technical checks, and validation of draft findings with
> management so each finding has an agreed owner and date. I'd also involve stakeholders in calibrating risk
> scores, and I'd assess more controls, at least all those linked to the top risks such as A.8.15 Logging and
> A.5.30 ICT readiness.

**20. The CTO says engineers need permanent admin rights to move fast. How do you respond?**
> Acknowledge the concern; delivery speed matters. Then show that just-in-time access through SSO keeps speed:
> engineers request elevation for a few hours and get it in seconds, with approval and logging. Most daily
> work needs only scoped roles. Explain the business risk in their terms: one stolen laptop credential today
> equals full platform compromise, a CERT-In report, a DPDP penalty and partner bank concerns. Offer a
> break-glass path for emergencies. If they still decline, document a formal risk acceptance by the CEO, since
> it's above appetite.

**21. How do you assess a third-party supplier like SupportCo?**
> Tier the supplier by data access and criticality; SupportCo is high because it sees customer PII. Send a
> security questionnaire, request evidence (ISO 27001 certificate with scope, SOC 2 report, policies, BGV
> process), and do a site or virtual visit. Agree contractual controls in a DPA: minimum security, breach
> notification within hours, audit rights, sub-processor approval, data return and deletion. Then monitor
> through periodic reviews, access reviews and incident reporting. Offboarding should include access removal
> and confirmation of data deletion.

**22. What's the difference between inherent and residual risk in your register?**
> Inherent (current) risk is scored on today's controls; in my register it's the "current" score. Target or
> residual risk is what's expected after the treatment plan is delivered. For R01, current is 4×5=20; after JIT
> access and monitoring, likelihood falls to 2 but impact stays 5, giving 10. The risk owner approves the plan
> and accepts that residual risk, as Clause 6.1.3 requires.

**23. Why did you use both a conformance status and a maturity score?**
> Status answers "does it meet the requirement?", which is what an auditor cares about. Maturity (0–5,
> CMMI-inspired) shows how far along the control is and lets us set a target, here 3 "Defined" in 12 months. Two
> partial controls can be very different: A.5.34 is at 1 (ad hoc), A.8.8 is at 2 (repeatable but not
> managed). It also makes progress measurable for leadership.

**24. What are the steps from here to certification?**
> Define the ISMS scope, approve the policy and roles, run the formal risk assessment and treatment plan, approve
> the SoA, implement the priority controls, operate them long enough to create evidence (typically at least
> 2–3 months), run an internal audit and a management review, close corrective actions, then go to an
> accredited certification body. Stage 1 reviews documentation and readiness; Stage 2 tests implementation.
> The certificate lasts three years with annual surveillance audits and recertification in year three.

**25. Why did you automate the report with Python, and what would you improve?**
> Keeping data in CSVs and generating the PDF, charts and tables from them means the numbers in the executive
> summary, charts, SoA and README can't drift apart. Changing a rating updates everything. The script also
> checks the data, for example that every risk score equals L × I and that the SoA has 93 rows. Improvements: a
> finding tracker with owners and dates, a quantitative view of the top risks, more controls in scope, and
> mapping each control to PCI DSS and DPDP requirements so one piece of evidence serves several frameworks.

---

## 6. One-page cheat sheet

| Item | Value |
|---|---|
| Standard | ISO/IEC 27001:2022 (+ Amd 1:2024); guidance ISO/IEC 27002:2022 |
| Annex A | 93 controls: Organizational 37, People 8, Physical 14, Technological 34; 11 new |
| 2013 → 2022 | 114 controls / 14 domains → 93 / 4 themes; transition ended 31 Oct 2025 |
| Mandatory | Clauses 4–10 (no exclusions); SoA (6.1.3 d) |
| Assessed | 20 controls: Org 7, People 3, Physical 2, Tech 8; new: A.5.7, A.5.23, A.8.9, A.8.16, A.8.28 |
| Results | 5 conformant (25%), 9 partial (45%), 6 non-conformant (30%); score 47.5%; maturity 1.7/5 |
| Non-conformant | A.5.7, A.5.19, A.5.24, A.7.14, A.8.2, A.8.16 |
| Conformant | A.6.1, A.6.7, A.7.2, A.8.13, A.8.24 |
| Clauses | 4, 5, 7, 8 partial; 6, 9, 10 non-conformant |
| Risks | R01 20 Critical; R02, R03 16; R04, R05 15; R06 12 (High); R07 9, R08 8 (Medium) |
| Treatments | Mitigate R01–R05 · Transfer R06 · Avoid R07 · Accept R08 |
| SoA | 90 applicable, 3 excluded (A.7.6, A.7.12, A.8.30); 21 implemented, 47 partial, 22 not implemented |
| Regulations | DPDP Act 2023 (up to INR 250 cr) · RBI PA/PG guidelines · RBI data localisation · CERT-In 6 h / 180-day logs · PCI DSS v4.0.1 |
| Top 3 priorities | Privileged access and MFA · detection and incident response · governance plus app security (VAPT, secrets) |
