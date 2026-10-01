# Critical Data Elements — Vantara Company Data Product

## What Is a CDE?

A Critical Data Element is a data field so important 
that its accuracy, completeness, or timeliness 
directly affects a business outcome or 
regulatory obligation at Vantara Finance.

Not every field in a company record is a CDE. 
The eight fields below are CDEs because their 
quality directly affects credit decisions, 
KYC compliance, regulatory reporting, 
or investor reporting.

---

## CDE 1 — Company Number

**Business definition**  
The unique identifier assigned by Companies House 
at incorporation. This is the golden key linking 
a company record across all of Vantara's systems. 
It never changes, even if the company name changes. 
Leading zeros must be preserved — 00445790 
and 445790 are the same company, but systems 
that strip leading zeros create phantom duplicates.

**Authoritative source:** Companies House bulk data — 
`CompanyNumber` field

**Quality threshold:**  
- Completeness: 100% — zero nulls permitted  
- Uniqueness: 100% — zero duplicate company 
  numbers in the golden record  
- Format: 8 characters, leading zeros preserved

**Owner:** Data Steward (Tolu — portfolio role)

**Why it matters:**  
Without a consistent company number as the golden key, 
the same company appears as multiple records across 
Vantara's systems. This is the root cause of the 
reconciliation failures between credit risk 
and compliance.

---

## CDE 2 — Registered Name

**Business definition**  
The full legal name of the company exactly as it 
appears on the Companies House register. This is 
the name used in all legal documents, credit 
agreements, and regulatory submissions. It is 
not the trading name. It is not an abbreviated 
version. It is the exact registered legal name.

**Authoritative source:** Companies House bulk data — 
`CompanyName` field

**Survivorship rule:** Where a company has changed 
its name, the most recent registered name is the 
authoritative value. Previous names are stored 
in a separate name history record, not overwritten.

**Quality threshold:**  
- Completeness: 100% — zero nulls  
- No leading or trailing whitespace  
- No all-uppercase entries (require normalisation 
  to Title Case with standard abbreviations 
  LTD, PLC, LLP retained in uppercase)

**Owner:** Data Steward

**Why it matters:**  
Vantara's credit agreements must reference the 
correct legal entity name. A mismatch between 
the agreement and the CH register is a legal risk. 
This is also the field causing the wrong-name 
problem in RM client calls.

---

## CDE 3 — Company Status

**Business definition**  
The current trading and legal status of the company 
as recorded at Companies House, mapped to Vantara's 
agreed internal classification.

**Agreed Vantara status mapping:**

| Companies House Value | Vantara Classification | Credit Eligible |
|---|---|---|
| Active | ACTIVE | Yes |
| Active - Proposal to Strike off | ACTIVE | Yes — review required |
| Voluntary Arrangement | RESTRICTED | Case by case |
| In Administration | RESTRICTED | No new lending |
| Liquidation | INACTIVE | No |
| Dissolved | INACTIVE | No |
| Converted / Closed | INACTIVE | No |
| Any unmapped value | UNMAPPED | Blocked — steward review |

**Authoritative source:** Companies House bulk data — 
`CompanyStatus` field

**Quality threshold:**  
- Completeness: 100% — zero nulls  
- All values must map to an agreed 
  Vantara classification — zero UNMAPPED 
  permitted in the published golden record  
- Timeliness: refreshed within 7 days 
  of any status change at Companies House

**Owner:** Data Steward

**Why it matters:**  
This is the field directly responsible for 
Vantara's Q3 dissolved-company loan approvals. 
A stale or unmapped status creates direct 
credit and regulatory risk.

---

## CDE 4 — Registered Address

**Business definition**  
The current registered office address of the company 
as recorded at Companies House. This is the legally 
recognised address used in Vantara's KYC process 
to verify the company's registered UK presence.

Components: AddressLine1, AddressLine2 (where present), 
PostTown, County (where present), PostCode, Country

**Authoritative source:** Companies House bulk data — 
address fields

**Quality threshold:**  
- PostCode: 95% populated for ACTIVE companies  
- AddressLine1: 98% populated for ACTIVE companies  
- PostCode must conform to valid UK postcode format  
- Timeliness: refreshed within 14 days 
  of any address change filing

**Owner:** Data Steward

**Why it matters:**  
KYC regulation requires Vantara to hold a current 
verified registered address for all corporate borrowers. 
This is the field behind the 18% address discrepancy — 
2,160 companies where the address on file cannot 
be confirmed as current.

---

## CDE 5 — SIC Code (Primary)

**Business definition**  
The Standard Industrial Classification code 
representing the company's primary business activity, 
as self-reported to Companies House. Where a company 
has filed multiple SIC codes, the first code in the 
filing is taken as primary.

**Authoritative source:** Companies House bulk data — 
`SICCode.SicText_1` field

**Survivorship rule:** Where SicText_1 is null, 
SicText_2 is promoted to primary. Where all four 
SIC code fields are null, SIC = UNKNOWN is assigned 
and the record is flagged for manual review.

**Quality threshold:**  
- 90% populated for ACTIVE companies  
  (Companies House does not mandate SIC codes 
  for all company types — some legitimate exemptions apply)

**Owner:** Data Steward

**Why it matters:**  
SIC codes drive Vantara's portfolio segmentation 
for investor reporting, sector exposure analysis, 
and credit policy application. Currently missing 
for 22% of the active portfolio — making the 
Halcyon board pack sector analysis unreliable.

---

## CDE 6 — Incorporation Date

**Business definition**  
The date on which the company was incorporated 
and registered at Companies House. Used by 
Vantara's credit risk team to calculate 
company age as a credit assessment factor. 
Company age is a significant input to the 
credit scoring model currently in development.

**Authoritative source:** Companies House bulk data — 
`IncorporationDate` field

**Quality threshold:**  
- Completeness: 100% — zero nulls  
- Date must be a valid calendar date  
- Date must fall between 01/01/1844 
  (earliest Companies House record) and today  
- No dates in the future permitted

**Owner:** Data Steward

**Why it matters:**  
An erroneous incorporation date produces a wrong 
company age, which produces a wrong risk score 
in the credit model. This feeds directly into 
James Whitfield's decision to block the model 
from production until data quality is resolved.

---

## CDE 7 — Last Accounts Date

**Business definition**  
The date to which the most recently filed annual 
accounts were prepared. Used by Vantara's compliance 
team to identify companies with overdue financial 
disclosures — a flag for enhanced due diligence. 
A company that has not filed accounts in over 
24 months triggers an enhanced KYC review 
under Vantara's risk-based monitoring policy.

**Authoritative source:** Companies House bulk data — 
`Accounts.LastMadeUpDate` field

**Quality threshold:**  
- 85% populated for ACTIVE companies 
  that have been incorporated for more than 18 months  
  (newly incorporated companies may not yet 
  have a filing obligation)

**Owner:** Data Steward

**Why it matters:**  
Late or absent accounts filing is an early 
warning indicator of company distress. 
Systematic monitoring of this field supports 
Vantara's portfolio risk monitoring programme 
and reduces the lag between company deterioration 
and Vantara's awareness of it.

---

## CDE 8 — Confirmation Statement Date

**Business definition**  
The date to which the most recent confirmation 
statement (formerly annual return) was made up. 
The confirmation statement confirms that the 
company's registered details at Companies House 
are current and accurate.

This CDE directly resolves Problem 2 from the 
problem statement. It is the agreed, single 
definition of whether a company is 
"actively maintained" at Vantara — adopted 
by both Credit Risk and Compliance.

**Agreed definition of ACTIVELY MAINTAINED:**  
A company is classified as ACTIVELY MAINTAINED 
if its confirmation statement date is within 
the last 12 months AND its Company Status is ACTIVE.

This flag — `is_actively_maintained` — is a derived 
boolean on the golden record, computed from this 
CDE and CDE 3 combined.

**Authoritative source:** Companies House bulk data — 
`ConfStmtLastMadeUpDate` field

**Quality threshold:**  
- 85% populated for ACTIVE companies

**Owner:** Data Steward

**Why it matters:**  
This is the field that reconciles the 
credit risk and compliance definitions 
of "active." Before this product existed, 
the two teams ran their own calculations 
from their own sources. Now there is one 
definition, one source, one flag. The monthly 
2-day reconciliation exercise disappears.