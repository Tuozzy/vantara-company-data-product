# Problem Statement — Vantara Finance Company Data Product

## About Vantara Finance

Vantara Finance is an independent UK-based specialist 
lender focused exclusively on small and medium-sized 
enterprises. Founded in 2009, Vantara fills the SME 
lending gap left by high street banks following the 
financial crisis.

**Key facts:**
- 600 employees across Leeds (HQ), London, and Edinburgh
- Active loan book: £1.1 billion
- Active borrowers: 12,000 corporate clients
- Annual lending volume: approximately £380 million
- Majority owned by Halcyon Capital Partners (PE) 
  since 2018 — exit anticipated within 2-3 years

Vantara is FCA-regulated (not PRA) as it does not 
take retail deposits. It funds its lending through 
institutional debt facilities, securitisation, and 
Halcyon co-investment. BCBS 239 principles are 
increasingly applied as Halcyon prepares for exit 
and pushes for institutional-grade data governance.

---

## The Four Lending Products

| Product | Range | Security | Risk Profile |
|---|---|---|---|
| Working Capital Loans | £10K–£250K | Unsecured / light | Highest volume, highest default risk |
| Asset Finance | £25K–£500K | Asset-secured | Lower risk, higher complexity |
| Invoice Finance | Up to 80% of debtor book | Invoice-backed | Operationally intensive |
| Property-Backed Business Loans | £200K–£2M | Commercial property | Lowest volume, highest average size |

All four products require accurate company data at 
origination, underwriting, monitoring, and regulatory 
reporting stages.

---

## The Six Departments and Their Data Pain

### Relationship Management
**Head:** Sarah Okafor, Director of Relationship Management  
**Team:** 120 people across Leeds and London

RMs originate new business and manage existing client 
relationships. They currently use a manual Companies 
House export maintained by the operations team — 
refreshed irregularly, typically 4–8 weeks stale.

RMs have lost trust in it and maintain personal 
spreadsheet copies "just in case," compounding 
the duplication problem.

**Sarah's exact words at the last QBR:**
*"My team is spending time they should spend with 
clients checking whether a company still exists. 
That is not why we hired them."*

**Pain:** Stale status data. Dissolved companies 
shown as active. Wrong names in client-facing 
communications.

---

### Credit Risk
**Head:** James Whitfield, Chief Risk Officer  
**Team:** 45 people, primarily Edinburgh

The credit risk team assesses every loan application 
above £25,000. They also run portfolio monitoring 
reports and are building a credit scoring model 
to partially automate Working Capital Loan origination.

James has **blocked the credit scoring model from 
going to production** until data quality issues 
are resolved — because a model trained on seven 
inconsistent sources learns the inconsistencies 
and automates them.

**Pain:** No agreed active/inactive definition 
with compliance. Missing SIC codes for 22% of 
the portfolio. Model blocked from production.

---

### Compliance and KYC
**Head:** Priya Sharma, Head of Compliance  
**Team:** 35 people across Leeds and Edinburgh

Compliance manages FCA regulatory obligations, 
AML requirements, and the KYC programme — 
verifying and refreshing the identity of 
all 12,000 corporate borrowers on a risk-based schedule.

The third-party enrichment service they use 
for KYC pulls address data from the last 
filed document rather than the current 
Companies House register.

**Pain:** 18% of the active portfolio — 
2,160 companies — have an unverifiable 
registered address. KYC refresh is manual 
and unsustainable at scale.

---

### Finance and Treasury
**Head:** Marcus Webb, Chief Financial Officer  
**Team:** 28 people, Leeds

Finance manages financial reporting, 
management accounts, and quarterly 
investor reporting to Halcyon. Portfolio 
segmentation by sector, geography, and 
company status feeds directly into the 
Halcyon board pack.

**Pain:** SIC codes missing for 22% of 
the active portfolio in the finance extract. 
Board pack segmentation is unreliable. 
Sector exposure reporting has gaps Halcyon 
has started to question.

---

### Operations and Technology
**Head:** David Chen, Chief Operating Officer  
**Team:** 85 people across all offices

Operations runs loan administration, systems, 
and the small data and analytics function. 
Currently maintains the manual Companies House 
export that the RM team uses. One data engineer 
employed. No data catalogue. No MDM platform.

**Pain:** 45-minute manual verification step 
per new client at onboarding. Half a day per 
month producing and distributing the RM extract. 
Neither should exist.

---

### Executive and Strategy
**CEO:** Rachel Thornton  
**PE Sponsor:** Halcyon Capital Partners

Rachel approved the data quality programme 
because Marcus framed it correctly: 
a credit scoring model an acquirer cannot audit, 
built on data three teams consume differently, 
is an exit risk. Halcyon is pushing BCBS 239 
principles as the quality benchmark for 
pre-exit data governance readiness.

---

## The Three Specific Problems This Product Solves

**Problem 1 — Dissolved company risk**

Credit applications processed for dissolved or 
liquidated companies because the RM export is stale. 
Two cases in Q3 required reversal at significant 
operational and reputational cost.

**Problem 2 — Inconsistent active definition**

Credit risk defines active as: CompanyStatus = Active.  
Compliance defines active as: Active AND confirmation 
statement filed within 12 months.

The same company can be active in one report and 
inactive in another. Monthly portfolio reviews 
require 2 days of manual reconciliation between 
the two teams' outputs.

**Problem 3 — KYC address discrepancy**

18% of the active portfolio — 2,160 companies — 
have a registered address on file that cannot be 
confirmed as current. The third-party enrichment 
service uses the last filed address, not the 
current register. Priya's team is working 
through these manually.

---

## Why a Data Product — Not a Better Report

A new report built on the same inconsistent sources 
solves nothing. A data cleansing exercise fixes 
records today and watches them get dirty again 
in six months because the underlying processes 
have not changed.

What Vantara needs is a **governed, reusable, 
documented data product** — the single authoritative 
version of company data that every team is 
required to consume, with agreed definitions, 
quality guarantees, and a named owner accountable 
for its accuracy.

The Companies House bulk data register is the 
authoritative source. This product builds on it 
properly — for the first time.