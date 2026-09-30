# Quality Specification — Vantara Company Data Product

## Purpose

This document defines the measurable quality 
thresholds for each Critical Data Element in the 
Vantara Company data product. These thresholds 
form the quality contract between the data product 
and its consumers.

They are enforced in two ways:

1. As automated pipeline gates in Great Expectations 
   — a threshold breach stops the pipeline before 
   bad data reaches any consumer
2. As a monthly scorecard reviewed by the 
   Data Product Owner (James Whitfield, CRO)

A threshold is not an aspiration. It is a commitment.

---

## Quality Dimensions

Each CDE is measured against one or more of 
the following six dimensions:

| Dimension | Definition |
|---|---|
| Completeness | Is the field populated where required? |
| Accuracy | Does the value reflect reality? |
| Timeliness | Is the data current enough for its intended use? |
| Consistency | Does the value mean the same thing everywhere? |
| Uniqueness | Is each entity represented exactly once? |
| Validity | Does the value conform to its expected format? |

---

## CDE Quality Thresholds

### CDE 1 — Company Number

| Dimension | Threshold | Measurement Method |
|---|---|---|
| Completeness | 100% | Zero nulls in golden record |
| Uniqueness | 100% | Zero duplicate company numbers |
| Validity | 100% | 8-character format, leading zeros preserved |

**Pipeline gate:** HARD STOP — any breach blocks 
the pipeline entirely. Company Number is the 
golden key. A null or duplicate here invalidates 
the entire record.

**Scorecard RAG:**
- Green: All three dimensions at 100%
- Red: Any dimension below 100%

---

### CDE 2 — Registered Name

| Dimension | Threshold | Measurement Method |
|---|---|---|
| Completeness | 100% | Zero nulls for ACTIVE companies |
| Validity | 100% | No leading/trailing whitespace, no all-caps entries |

**Pipeline gate:** HARD STOP for completeness. 
Validity failures trigger a WARNING and a 
steward review task — they do not stop the pipeline 
but are logged and reported.

**Scorecard RAG:**
- Green: Completeness 100%, Validity 98%+
- Amber: Validity between 95% and 98%
- Red: Completeness below 100%, or Validity below 95%

---

### CDE 3 — Company Status

| Dimension | Threshold | Measurement Method |
|---|---|---|
| Completeness | 100% | Zero nulls |
| Validity | 100% | All values map to agreed Vantara classification |
| Timeliness | 95% of records | Refreshed within 7 days of last CH update |

**Pipeline gate:** HARD STOP if any record carries 
an UNMAPPED status value. The pipeline does not 
publish a record with an unresolved status.

**Scorecard RAG:**
- Green: Completeness 100%, Validity 100%, Timeliness 95%+
- Amber: Timeliness between 90% and 95%
- Red: Any completeness or validity breach, 
  or timeliness below 90%

**Note:** Timeliness is measured as the proportion 
of ACTIVE company records whose status was 
confirmed or updated within the last 7 days 
in the Companies House bulk file.

---

### CDE 4 — Registered Address

| Dimension | Threshold | Measurement Method |
|---|---|---|
| Completeness — PostCode | 95% | For ACTIVE companies |
| Completeness — AddressLine1 | 98% | For ACTIVE companies |
| Validity — PostCode format | 98% | Matches UK postcode regex pattern |
| Timeliness | 90% of records | Address confirmed within 14 days |

**Pipeline gate:** WARNING only — address gaps 
do not stop the pipeline but are flagged 
for steward review. Records with null PostCode 
are tagged `address_incomplete = true`.

**Scorecard RAG:**
- Green: PostCode 95%+, AddressLine1 98%+, 
  Validity 98%+, Timeliness 90%+
- Amber: PostCode between 90% and 95%, 
  or Timeliness between 85% and 90%
- Red: PostCode below 90%, AddressLine1 
  below 95%, or Validity below 95%

---

### CDE 5 — SIC Code (Primary)

| Dimension | Threshold | Measurement Method |
|---|---|---|
| Completeness | 90% | For ACTIVE companies incorporated 18+ months |
| Validity | 100% | Value must be a valid SIC 2007 code or UNKNOWN |

**Pipeline gate:** WARNING only — SIC gaps 
are flagged but do not stop the pipeline. 
Records with SIC = UNKNOWN are tagged 
`sic_requires_review = true`.

**Scorecard RAG:**
- Green: Completeness 90%+
- Amber: Completeness between 85% and 90%
- Red: Completeness below 85%

**Note:** The 90% threshold reflects the known 
Companies House data characteristic that 
some company types are not required to 
file a SIC code.

---

### CDE 6 — Incorporation Date

| Dimension | Threshold | Measurement Method |
|---|---|---|
| Completeness | 100% | Zero nulls |
| Validity | 100% | Valid date between 01/01/1844 and today |

**Pipeline gate:** HARD STOP — an invalid or 
missing incorporation date produces a wrong 
company age, which corrupts the credit 
scoring model feature. No exceptions.

**Scorecard RAG:**
- Green: Both dimensions at 100%
- Red: Any breach

---

### CDE 7 — Last Accounts Date

| Dimension | Threshold | Measurement Method |
|---|---|---|
| Completeness | 85% | For ACTIVE companies incorporated 18+ months |
| Validity | 100% | Valid date, not in the future |

**Pipeline gate:** WARNING only — gaps are 
expected for newer companies. Records with 
null Last Accounts Date and incorporation 
date over 18 months ago are tagged 
`accounts_overdue_review = true`.

**Scorecard RAG:**
- Green: Completeness 85%+
- Amber: Completeness between 80% and 85%
- Red: Completeness below 80%

---

### CDE 8 — Confirmation Statement Date

| Dimension | Threshold | Measurement Method |
|---|---|---|
| Completeness | 85% | For ACTIVE companies |
| Validity | 100% | Valid date, not in the future |
| Derived field accuracy | 100% | is_actively_maintained computed correctly |

**Pipeline gate:** WARNING for completeness gaps. 
HARD STOP if the is_actively_maintained 
derived field cannot be computed due to 
a null in both Company Status and 
Confirmation Statement Date simultaneously.

**Scorecard RAG:**
- Green: Completeness 85%+, derived field 100%
- Amber: Completeness between 80% and 85%
- Red: Completeness below 80%, or derived 
  field accuracy below 100%

---

## Scorecard Summary Table

This table is produced monthly from the 
Great Expectations quality run and reviewed 
by James Whitfield (Data Product Owner) 
in the monthly governance review.

| CDE | Dimension | Threshold | Current Score | Status | Trend |
|---|---|---|---|---|---|
| Company Number | Completeness | 100% | TBC | TBC | TBC |
| Company Number | Uniqueness | 100% | TBC | TBC | TBC |
| Registered Name | Completeness | 100% | TBC | TBC | TBC |
| Company Status | Completeness | 100% | TBC | TBC | TBC |
| Company Status | Timeliness | 95% | TBC | TBC | TBC |
| Registered Address | PostCode Completeness | 95% | TBC | TBC | TBC |
| SIC Code | Completeness | 90% | TBC | TBC | TBC |
| Incorporation Date | Completeness | 100% | TBC | TBC | TBC |
| Last Accounts Date | Completeness | 85% | TBC | TBC | TBC |
| Confirmation Statement | Completeness | 85% | TBC | TBC | TBC |

TBC fields will be populated once the 
Great Expectations quality suite runs 
against the Companies House bulk data.

---

## Breach Response Process

When a pipeline gate triggers a HARD STOP:

1. Pipeline halts — no data published to consumers
2. Data Steward receives automatic alert
3. Steward investigates root cause within 
   1 working day
4. Root cause documented in breach log
5. Fix applied in source or transformation layer
6. Pipeline re-run and validated
7. Data Product Owner notified of resolution

When a quality check triggers a WARNING:

1. Pipeline continues — data published with 
   quality flags attached
2. Flagged records tagged with relevant 
   review indicator field
3. Steward reviews flagged records weekly
4. Patterns escalated to Data Product Owner 
   if warning persists across two consecutive runs

---

## Review Cadence

| Review Type | Frequency | Owner | Forum |
|---|---|---|---|
| Automated quality run | Weekly — Monday 06:00 UTC | Data Steward | Automated |
| Scorecard review | Monthly | Data Product Owner | Governance review meeting |
| Threshold review | Six-monthly | Data Product Owner + Steward | Product review |
| Threshold change approval | As needed | Data Product Owner | Documented sign-off |