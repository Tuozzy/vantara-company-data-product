# Vantara Company Data Product — Pipeline Lineage

## End-to-End Data Flow

```mermaid
flowchart TD
    A["🏛️ Companies House\nBulk Data Register\n5.7M company records\nUpdated monthly"]
    
    B["📁 Raw Landing Zone\ndata/raw/\nBasicCompanyDataAsOneFile.csv\nNo transformations applied"]
    
    C["⚙️ dbt Staging Model\nstg_companies_house\n• Field selection and renaming\n• Data type casting\n• Whitespace trimming\n• SIC code promotion logic"]
    
    D["✅ Great Expectations\nQuality Gate\n• 10 CDE threshold checks\n• HARD STOP on critical failures\n• WARNING flags on soft failures\n• JSON report generated"]
    
    E["🏆 dbt Mart Model\ngolden_company_record\n• Vantara status mapping\n• Name normalisation flags\n• Derived field computation\n• Quality indicator flags"]
    
    F["📊 Relationship Management\nClient verification\nOnboarding enrichment"]
    
    G["📈 Credit Risk\nOrigination assessment\nPortfolio monitoring\nCredit scoring model features"]
    
    H["🔍 Compliance and KYC\nKYC verification\nAddress currency\nRefresh programme"]
    
    I["💰 Finance and Treasury\nPortfolio segmentation\nHalcyon investor reporting"]
    
    J["🤖 AI Credit Scoring Model\nFeature store input\nGoverned training data"]

    A -->|"Weekly refresh\nMonday 06:00 UTC"| B
    B -->|"read_csv_auto\nignore_errors=true"| C
    C -->|"Quality validation\n10 CDE checks"| D
    D -->|"PASS — publish\nFAIL — stop pipeline"| E
    E --> F
    E --> G
    E --> H
    E --> I
    E -->|"Planned — v2"| J

    style A fill:#E1F5EE,stroke:#0F6E56
    style B fill:#F5F5F0,stroke:#999
    style C fill:#FFF8EC,stroke:#D48A00
    style D fill:#FDECEA,stroke:#C0392B
    style E fill:#EEF0FF,stroke:#4A52C2
    style F fill:#E8F4FD,stroke:#1A6FA3
    style G fill:#E8F4FD,stroke:#1A6FA3
    style H fill:#E8F4FD,stroke:#1A6FA3
    style I fill:#E8F4FD,stroke:#1A6FA3
    style J fill:#F0FAF4,stroke:#1A7A4A
```

## Quality Scorecard — Latest Run (2026-10-01)

| CDE | Check | Threshold | Actual | Status |
|---|---|---|---|---|
| CDE 1 | Company Number — Completeness | 100% | 100% | 🟢 PASS |
| CDE 1 | Company Number — Uniqueness | 100% | 100% | 🟢 PASS |
| CDE 2 | Registered Name — Completeness | 100% | 100% | 🟢 PASS |
| CDE 3 | Company Status — No Unmapped Values | 100% | 99.95% | 🔴 FAIL |
| CDE 4 | Registered Address — PostCode | 95% | 98.4% | 🟢 PASS |
| CDE 4 | Registered Address — AddressLine1 | 98% | 98.9% | 🟢 PASS |
| CDE 5 | SIC Code — Completeness | 90% | 100% | 🟢 PASS |
| CDE 6 | Incorporation Date — Completeness | 100% | 100% | 🟢 PASS |
| CDE 7 | Last Accounts Date — Completeness | 85% | 91.8% | 🟢 PASS |
| CDE 8 | Confirmation Statement Date | 85% | 81.7% | 🟡 WARN |

## Key Findings

**2,612 UNMAPPED status values** — Companies House 
returned status codes not in the agreed Vantara 
mapping table. Steward review required to extend 
the mapping before these records can be published.

**18.3% of active companies have no confirmation 
statement date** — meaning they cannot be classified 
as ACTIVELY MAINTAINED under the agreed Vantara 
definition. This is a known Companies House data 
characteristic for certain company types.

**SIC promotion logic worked perfectly** — zero 
UNKNOWN SIC codes despite Companies House having 
gaps in SicText_1. The fallback to SicText_2, 3, 
and 4 resolved every gap.

## Technology Stack

| Layer | Tool |
|---|---|
| Source | Companies House Bulk Data (free, public) |
| Database | DuckDB |
| Transformation | dbt Core 1.12.5 |
| Quality | Custom Python quality suite |
| Version Control | Git + GitHub |