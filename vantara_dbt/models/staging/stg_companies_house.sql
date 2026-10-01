-- stg_companies_house.sql
-- Staging model for Companies House bulk data
-- Selects and cleans the eight CDEs defined in governance/cde_definitions.md
-- Source: Companies House BasicCompanyDataAsOneFile (weekly refresh)

with source as (

    select *
    from read_csv_auto(
        '../data/raw/BasicCompanyDataAsOneFile-2026-09-01.csv',
        ignore_errors=true
    )

),

staged as (

    select

        -- CDE 1 — Company Number (golden key)
        -- Trimmed and padded to 8 characters to preserve leading zeros
        lpad(trim("CompanyNumber"), 8, '0')     as company_number,

        -- CDE 2 — Registered Name
        -- Trimmed of whitespace, raw value preserved separately
        trim("CompanyName")                     as registered_name,
        "CompanyName"                           as registered_name_raw,

        -- CDE 3 — Company Status
        trim("CompanyStatus")                   as company_status_raw,

        -- CDE 4 — Registered Address
        trim("RegAddress.AddressLine1")         as address_line_1,
        trim("RegAddress.AddressLine2")         as address_line_2,
        trim("RegAddress.PostTown")             as post_town,
        trim("RegAddress.County")               as county,
        trim("RegAddress.Country")              as country,
        trim("RegAddress.PostCode")             as post_code,

        -- CDE 5 — SIC Code (primary with fallback logic)
        -- Promotion rule: use first non-null SIC across four fields
        coalesce(
            nullif(trim("SICCode.SicText_1"), ''),
            nullif(trim("SICCode.SicText_2"), ''),
            nullif(trim("SICCode.SicText_3"), ''),
            nullif(trim("SICCode.SicText_4"), ''),
            'UNKNOWN'
        )                                       as sic_code_primary,

        -- CDE 6 — Incorporation Date
        "IncorporationDate"                     as incorporation_date,

        -- CDE 7 — Last Accounts Date
        "Accounts.LastMadeUpDate"               as last_accounts_date,

        -- CDE 8 — Confirmation Statement Date
        "ConfStmtLastMadeUpDate"                as confirmation_statement_date,

        -- Metadata
        current_date                            as dbt_loaded_date

    from source

)

select * from staged