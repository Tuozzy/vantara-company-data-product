# Data Catalogue Entry — Vantara Company Data Product

## Product Overview

| Field | Value |
|---|---|
| Product Name | Vantara Company Data Product |
| Product ID | DP-001 |
| Domain | Company Master Data |
| Version | 1.0 |
| Status | Active |
| Created | October 2026 |
| Last Updated | October 2026 |
| Next Review | April 2027 |

---

## What This Product Is

The Vantara Company Data Product is the single, 
authoritative, governed source of company data 
for all teams at Vantara Finance.

It is built on the Companies House public bulk 
data register — the UK's official record of all 
registered companies — and processed through a 
documented pipeline that applies agreed business 
rules, quality checks, and governance standards 
before any data reaches a consumer.

Every team at Vantara that needs company data 
consumes this product. No team maintains their 
own extract, their own copy, or their own 
definition of what a company record contains.

**One product. One source of truth. One owner.**

---

## The Problem This Product Solves

Before this product existed, Vantara had three 
teams consuming company data from three different 
sources with three different definitions of 
what "active" means.

The consequences:

- Two high-risk loan approvals reversed in Q3 
  because dissolved companies appeared active 
  in the relationship manager view
- Monthly portfolio review required 2 days of 
  manual reconciliation between Credit Risk 
  and Compliance outputs
- 18% of the active portfolio — 2,160 companies — 
  had an unverifiable registered address
- SIC codes missing for 22% of the portfolio, 
  making investor reporting unreliable
- Credit scoring model blocked from production 
  because training data could not be trusted

This product resolves all five problems 
from a single governed foundation.

---

## Ownership

| Role | Name | Responsibility |
|---|---|---|
| Data Product Owner | James Whitfield, CRO | Accountable for product quality and fitness for purpose. Quality metrics included in annual objectives. |
| Data Steward | Portfolio Role | Day-to-day quality monitoring, breach investigation, catalogue maintenance, consumer support |
| Authoritative Source Owner | Companies House | Maintains the underlying public register |

---

## Who This Product Is For

This product is designed for consumption by 
all six departments at Vantara Finance.

| Department | Primary Use Case | Key Fields Used |
|---|---|---|
| Relationship Management | Client record verification, onboarding, client communications | Registered Name, Company Status, Registered Address |
| Credit Risk | Origination assessment, portfolio monitoring, credit scoring model features | Company Status, Incorporation Date, SIC Code, is_actively_maintained |
| Compliance and KYC | KYC verification, address currency, refresh programme | Registered Address, Confirmation Statement Date, is_actively_maintained |
| Finance and Treasury | Portfolio segmentation, investor reporting, sector exposure | SIC Code, Company Status, Incorporation Date |
| Operations and Technology | Automated onboarding, CRM enrichment, data quality reporting | All CDEs |
| Executive and Strategy | Pre-exit data governance evidence, Halcyon board pack | All CDEs — aggregate quality scorecard |

---

## What This Product Contains

### The Eight Critical Data Elements

| CDE | Business Definition | Quality Threshold |
|---|---|---|
| Company Number | Unique CH identifier — the golden key linking a company across all Vantara systems. Never changes. | 100% complete, 100% unique |
| Registered Name | Full legal name as filed at Companies House. Not the trading name. The exact registered legal entity name. | 100% complete, Title Case normalised |
| Company Status | Current trading status mapped to Vantara's agreed classification: ACTIVE, RESTRICTED, or INACTIVE. | 100% complete, 0% unmapped |
| Registered Address | Current registered office address as on the CH register — not the last filed address. | 95% PostCode, 98% AddressLine1 |
| SIC Code (Primary) | Primary Standard Industrial Classification code representing the company's main business activity. | 90% for active companies |
| Incorporation Date | Date the company was registered at Companies House. Used to calculate company age. | 100% complete, valid date |
| Last Accounts Date | Date to which most recent annual accounts were prepared. Flags overdue filers. | 85% for active companies 18m+ |
| Confirmation Statement Date | Date of most recent confirmation statement. Basis for is_actively_maintained flag. | 85% for active companies |

### Derived Fields

| Field | Definition | Source CDEs |
|---|---|---|
| is_actively_maintained | True if Company Status = ACTIVE and Confirmation Statement Date is within 12 months | CDE 3 + CDE 8 |
| company_age_years | Years since incorporation at the point of the most recent refresh | CDE 6 |
| address_incomplete | True if PostCode or AddressLine1 is null for an ACTIVE company | CDE 4 |
| sic_requires_review | True if SIC Code = UNKNOWN | CDE 5 |
| accounts_overdue_review | True if Last Accounts Date is null and company is 18+ months old | CDE 6 + CDE 7 |

---

## What This Product Guarantees

By consuming this product you are guaranteed:

**Accuracy** — every field reflects the current 
Companies House register, not a stale extract 
or a third-party enrichment approximation.

**Consistency** — the same company record 
produces the same values regardless of which 
team queries it. There is one definition 
of active. One registered name. One status.

**Timeliness** — the golden record is refreshed 
weekly from the Companies House bulk data file. 
Company Status is confirmed within 7 days. 
Registered Address within 14 days.

**Traceability** — every field has documented 
lineage back to its source. If a regulator 
asks where a value came from, the answer 
is in the catalogue and in the pipeline logs.

**Quality assurance** — every weekly refresh 
passes an automated quality gate before 
data is published. A breach stops the pipeline. 
Bad data does not reach you silently.

---

## What This Product Does Not Guarantee

**It does not cover trading names** — the 
Registered Name is the legal entity name 
only. Trading names are not in scope for v1.

**It does not cover financial data** — 
accounts figures, turnover, or credit 
scores are not included. This is a company 
identity and status product.

**It does not cover directors or PSCs** — 
People with Significant Control and 
director information are planned for v2.

**SIC codes are self-reported** — Companies 
House does not verify SIC codes. A company 
may have filed an inaccurate code. 
The product reflects what was filed.

---

## How to Access This Product

### For analysts and reporting (SQL access)

Connect to the Vantara DuckDB instance and 
query the `mart.golden_company_record` table.

```sql
-- All active companies
SELECT *
FROM mart.golden_company_record
WHERE company_status_vantara = 'ACTIVE';

-- Active and maintained companies only
SELECT *
FROM mart.golden_company_record
WHERE is_actively_maintained = true;

-- Companies with overdue accounts
SELECT
    company_number,
    registered_name,
    incorporation_date,
    last_accounts_date
FROM mart.golden_company_record
WHERE accounts_overdue_review = true
AND company_status_vantara = 'ACTIVE';

-- Portfolio segment by SIC code
SELECT
    sic_code_primary,
    COUNT(*) as company_count
FROM mart.golden_company_record
WHERE company_status_vantara = 'ACTIVE'
GROUP BY sic_code_primary
ORDER BY company_count DESC;
```

### For operational systems (API access)

The golden record is available via the 
internal data API. Authenticate with your 
Vantara service account and query by 
Company Number:
GET /api/v1/companies/{company_number}

Contact the Data Steward to request 
API access credentials.

### For new consumers

Before consuming this product, contact 
the Data Steward to:

1. Register your team as a consumer
2. Confirm your use case and required fields
3. Receive access credentials appropriate 
   to your role and data sensitivity requirements
4. Be added to the consumer notification 
   list for change communications

---

## Data Lineage Summary

Companies House Bulk Data (weekly refresh)
↓
Raw landing zone (DuckDB — data/raw/)
↓
dbt staging model (stg_companies_house)
— field selection and renaming
— data type casting
— whitespace and format cleaning
↓
Great Expectations quality gate
— CDE threshold validation
— HARD STOP on critical failures
— WARNING flags on soft failures
↓
dbt mart model (golden_company_record)
— status mapping to Vantara classification
— SIC code promotion logic
— derived field computation
— name normalisation
↓
Published golden record
— mart.golden_company_record
— Consumed by all Vantara departments

Full lineage documentation with field-level 
detail is available via the dbt docs site.

---

## Change Management

### How to request a change to this product

If your team needs a field added, a definition 
changed, or a threshold adjusted, contact 
the Data Steward with:

- The field or CDE affected
- The change requested
- The business reason
- The consuming systems or reports affected

Changes are assessed by the Data Steward 
and escalated to the Data Product Owner 
for approval where they affect quality 
thresholds or CDE definitions.

### How consumers are notified of changes

All registered consumers receive advance 
notice of:

- Changes to CDE definitions (minimum 10 working days notice)
- Changes to field names or data types (minimum 10 working days notice)
- Changes to quality thresholds (minimum 5 working days notice)
- Unplanned pipeline failures (same day notification)

Notice is sent to the consumer contact 
registered at the point of access setup.

---

## Quality Scorecard — Current Status

Full quality specification is documented 
in `governance/quality_spec.md`.

| CDE | Overall Status | Last Reviewed |
|---|---|---|
| Company Number | 🟢 Green | TBC — populated after first pipeline run |
| Registered Name | 🟢 Green | TBC |
| Company Status | 🟢 Green | TBC |
| Registered Address | 🟡 Amber | TBC |
| SIC Code | 🟡 Amber | TBC |
| Incorporation Date | 🟢 Green | TBC |
| Last Accounts Date | 🟢 Green | TBC |
| Confirmation Statement Date | 🟢 Green | TBC |

Registered Address and SIC Code are pre-flagged 
Amber based on known Companies House data 
characteristics — address gaps for some 
company types, and SIC exemptions for others. 
These are expected and documented, not failures.

Scores will be updated after the first 
Great Expectations pipeline run.

---

## Known Limitations

| Limitation | Impact | Mitigation |
|---|---|---|
| Companies House data is self-reported | SIC codes and some address fields may be inaccurate at source | Flagged in quality spec — consumers advised not to rely on SIC as definitive |
| Weekly refresh cadence | Status changes between Monday refreshes will not be reflected immediately | Timeliness threshold documented — consumers aware of 7-day window |
| Directors and PSC data not included | KYC beneficial ownership checks cannot be performed from this product alone | Planned for v2 — consumers should continue using existing PSC process for now |
| Companies House bulk file occasionally has formatting anomalies | May affect name normalisation for a small number of records | Steward review process in place — anomalies flagged and resolved within 5 working days |

---

## Version History

| Version | Date | Changes | Approved By |
|---|---|---|---|
| 1.0 | October 2026 | Initial release — 8 CDEs, weekly refresh, Great Expectations quality suite | James Whitfield, CRO |

---

## Contact

**Data Steward:** Contact via the data governance 
channel in the internal communications platform

**Data Product Owner:** James Whitfield, CRO — 
for escalations and threshold change approvals

**For access requests:** Contact the Data Steward 
with your name, department, use case, and 
line manager approval