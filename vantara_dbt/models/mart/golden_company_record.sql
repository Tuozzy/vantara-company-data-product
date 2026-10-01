-- golden_company_record.sql
-- Mart model — the golden company record for Vantara Finance
-- Implements survivorship rules from governance/survivorship_rules.md
-- Applies Vantara status mapping, derived fields, and quality flags

with staged as (

    select * from {{ ref('stg_companies_house') }}

),

-- Apply Vantara status mapping (Survivorship Rule 3)
status_mapped as (

    select
        *,
        case company_status_raw
            when 'Active'                                       then 'ACTIVE'
            when 'Active - Proposal to Strike off'              then 'ACTIVE'
            when 'Voluntary Arrangement'                        then 'RESTRICTED'
            when 'In Administration'                            then 'RESTRICTED'
            when 'Administration Order'                         then 'RESTRICTED'
            when 'In Administration/Administrative Receiver'    then 'RESTRICTED'
            when 'Liquidation'                                  then 'INACTIVE'
            when 'Dissolved'                                    then 'INACTIVE'
            when 'Converted / Closed'                           then 'INACTIVE'
            when 'Receivership'                                 then 'INACTIVE'
            else                                                     'UNMAPPED'
        end                                     as company_status_vantara

    from staged

),

-- Apply name normalisation (Survivorship Rule 2)
-- Trim is already done in staging
-- Flag all-caps names for review
name_normalised as (

    select
        *,
        case
            when registered_name = upper(registered_name)
            and length(registered_name) > 4
            then true
            else false
        end                                     as name_requires_normalisation

    from status_mapped

),

-- Compute derived fields and quality flags
final as (

    select

        -- Core CDEs
        company_number,
        registered_name,
        registered_name_raw,
        company_status_raw,
        company_status_vantara,
        address_line_1,
        address_line_2,
        post_town,
        county,
        country,
        post_code,
        sic_code_primary,
        incorporation_date,
        last_accounts_date,
        confirmation_statement_date,

        -- Derived field 1 — is_actively_maintained (Survivorship Rule 4)
        -- True if ACTIVE and confirmation statement within last 12 months
        case
            when company_status_vantara = 'ACTIVE'
            and confirmation_statement_date >= current_date - interval '12 months'
            then true
            else false
        end                                     as is_actively_maintained,

        -- Derived field 2 — company_age_years
        case
            when incorporation_date is not null
            then datediff('year', incorporation_date, current_date)
            else null
        end                                     as company_age_years,

        -- Quality flag 1 — address_incomplete (CDE 4)
        case
            when company_status_vantara = 'ACTIVE'
            and (post_code is null or trim(post_code) = '')
            then true
            else false
        end                                     as address_incomplete,

        -- Quality flag 2 — sic_requires_review (CDE 5)
        case
            when sic_code_primary = 'UNKNOWN'
            then true
            else false
        end                                     as sic_requires_review,

        -- Quality flag 3 — accounts_overdue_review (CDEs 6 and 7)
        case
            when company_status_vantara = 'ACTIVE'
            and last_accounts_date is null
            and incorporation_date <= current_date - interval '18 months'
            then true
            else false
        end                                     as accounts_overdue_review,

        -- Quality flag 4 — status_unmapped
        case
            when company_status_vantara = 'UNMAPPED'
            then true
            else false
        end                                     as status_unmapped,

        -- Quality flag 5 — name requires normalisation
        name_requires_normalisation,

        -- Metadata
        dbt_loaded_date,
        current_timestamp                       as dbt_updated_at

    from name_normalised

)

select * from final