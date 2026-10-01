# Survivorship Rules — Vantara Company Data Product

## What Are Survivorship Rules?

Survivorship rules determine which value wins 
when data from multiple sources conflicts, 
or when a business decision must be made about 
how to handle ambiguous or edge-case data.

These are **business decisions, not technical ones.**  
They were agreed between the Data Steward, 
the Head of Credit Risk (James Whitfield), 
and the Head of Compliance (Priya Sharma) 
before any pipeline code was written.

Documenting them here means:
- Every transformation in the pipeline has 
  a traceable business justification
- When a regulator asks why a field contains 
  a particular value, the answer is documented
- When business rules change, the change is 
  made here first, then reflected in the pipeline

---

## Rule 1 — Company Number Is the Golden Key

The Company Number is the sole identifier used 
for deduplication, matching, and record linkage.

Company Name is **never** used as a matching key. 
Names change. Numbers do not.

If two records share the same Company Number, 
they represent the same company. The record 
with the most recent data refresh timestamp 
is retained as the authoritative version.

---

## Rule 2 — Name Normalisation

Companies House registered names occasionally 
contain formatting inconsistencies that must 
be resolved before the name enters the golden record.

**Normalisation steps applied in order:**

1. Remove leading and trailing whitespace
2. Convert all-uppercase names to Title Case  
   Example: `ACME TRADING LIMITED` → `Acme Trading Limited`
3. Retain standard legal suffix abbreviations 
   in uppercase regardless of source format:  
   LTD, PLC, LLP, LTD., CIC, CIO, CBP
4. Preserve all special characters exactly 
   as filed — do not remove ampersands, 
   hyphens, or apostrophes
5. Store the original CH value in a 
   `registered_name_raw` field alongside 
   the normalised value — for audit purposes

**Previous names:**  
Where a company has changed its registered name, 
the most recent name is the active value. 
Previous names are written to a separate 
`company_name_history` table with effective 
dates. They are never overwritten or deleted.

---

## Rule 3 — Company Status Mapping

Companies House uses specific status values 
that must be mapped to Vantara's internal 
classification before entering the golden record.

**Mapping table:**

| CH Raw Value | Vantara Classification |
|---|---|
| Active | ACTIVE |
| Active - Proposal to Strike off | ACTIVE |
| Voluntary Arrangement | RESTRICTED |
| In Administration | RESTRICTED |
| Administration Order | RESTRICTED |
| In Administration/Administrative Receiver | RESTRICTED |
| Liquidation | INACTIVE |
| Dissolved | INACTIVE |
| Converted / Closed | INACTIVE |
| Receivership | INACTIVE |

**Unmapped values:**  
If Companies House returns a status value not 
in this table, the record is assigned 
`UNMAPPED` status and flagged for 
Data Steward review within 5 working days. 
The record is excluded from the active 
golden record until resolved.

The mapping table is maintained in 
`governance/status_mapping.csv` and 
referenced by the dbt model — it is not 
hardcoded into the SQL. Changes to the 
mapping require a documented update 
to this file and a new dbt run.

---

## Rule 4 — The Agreed Active Definition

**This rule directly resolves Problem 2 
from the problem statement.**

Before this product, Credit Risk and Compliance 
used different definitions of "active." 
This rule replaces both with one agreed standard.

**Vantara's single agreed definition:**

A company is **ACTIVELY MAINTAINED** if 
ALL of the following are true:

1. `company_status_vantara` = `ACTIVE`
2. `confirmation_statement_date` is within 
   the last 12 months from the report date

A company is **ACTIVE BUT NOT MAINTAINED** if:

1. `company_status_vantara` = `ACTIVE`
2. `confirmation_statement_date` is more than 
   12 months ago, OR is null

This produces a derived boolean field on 
every golden record: `is_actively_maintained`

**Usage by department:**
- Credit Risk uses `company_status_vantara` 
  for lending eligibility decisions
- Compliance uses `is_actively_maintained` 
  for KYC refresh triggers
- Both now derive from the same governed source

The 12-month threshold was agreed by James Whitfield 
and Priya Sharma in the CDE definition workshop. 
Any change to this threshold requires sign-off 
from both and a documented update to this file.

---

## Rule 5 — SIC Code Promotion

Companies House allows up to 4 SIC codes per company. 
Vantara uses a single primary SIC code.

**Selection logic applied in order:**

1. Use `SICCode.SicText_1` if populated
2. If SicText_1 is null, promote `SICCode.SicText_2`
3. If SicText_2 is also null, promote `SICCode.SicText_3`
4. If SicText_3 is also null, promote `SICCode.SicText_4`
5. If all four are null, assign `SIC_PRIMARY` = `UNKNOWN` 
   and set `sic_requires_review` = true

Records with `UNKNOWN` SIC are included in the 
golden record but flagged. The Data Steward 
reviews these monthly and updates the mapping 
where a manual lookup resolves the code.

---

## Rule 6 — Address Currency

**This rule directly addresses the 18% 
KYC address discrepancy.**

The registered address in the golden record 
always reflects the current address on the 
Companies House register at the time of the 
most recent data refresh — not the address 
from the last filed document.

Companies House bulk data provides the 
current registered office address directly. 
This is different from what Vantara's 
third-party enrichment service was providing 
(last filed address, which can lag by 
18+ months after an address change).

A derived field `address_last_verified_date` 
records the date of the most recent refresh 
in which the address was confirmed present 
and valid. Compliance uses this field to 
evidence KYC address currency to regulators.

---

## Rule 7 — Dissolved Company Retention

Dissolved and inactive companies are **never 
deleted** from the golden record.

They are retained with `company_status_vantara` 
= `INACTIVE` and excluded from active portfolio 
reporting by default. They remain accessible 
via filter for:

- Historical lending record queries
- Regulatory audit trail requirements
- Bad debt and write-off reporting

This prevents the data product from losing 
the historical record that credit agreements 
were made against a company that subsequently dissolved.

---

## Rule 8 — Stale Record Handling

The Companies House bulk file is downloaded 
and processed weekly — every Monday at 06:00 UTC.

A record in the golden record is considered 
**STALE** if it has not been refreshed 
within 10 calendar days.

If a weekly refresh fails:
1. The Data Steward is alerted automatically
2. The previous week's data remains in place 
   and is not deleted
3. A `data_refresh_status` field on the 
   golden record is updated to `STALE` 
   with the last successful refresh date
4. Consuming teams are notified via 
   a documented alert process

No data is ever silently replaced without 
a refresh timestamp update.