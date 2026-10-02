# Vantara Finance — Company Data Product

A governed, reusable company data product built on 
publicly available Companies House data — demonstrating 
end-to-end data product design including business 
problem framing, CDE definition, survivorship rules, 
quality specification, dbt transformations, and 
Great Expectations quality monitoring.

---

## The Business Problem

Vantara Finance is a UK-based SME lender with 12,000 
corporate borrowers and a £1.1 billion active loan book. 
Three departments consume company data from three 
different sources — each with different definitions, 
different refresh frequencies, and different quality 
standards.

The consequences are real and costly:

- Dissolved companies still shown as active in the 
  relationship manager view — two high-risk loan 
  approvals reversed in Q3 at significant operational cost
- Credit risk and compliance teams disagree on whether 
  a company is "active" because they use different 
  source definitions
- 18% of the active portfolio has an unverifiable 
  registered address — a KYC compliance gap
- SIC codes missing for 22% of the portfolio — 
  making investor segmentation reporting unreliable

The root cause is not bad technology. It is the absence 
of a single, trusted, governed source of company data 
that every team agrees on and consumes consistently.

---

## The Solution

A governed **Company data product** — built on the 
Companies House public bulk data register — with:

- Eight defined Critical Data Elements (CDEs) with 
  business definitions, quality thresholds, and named ownership
- Documented survivorship rules resolving conflicts 
  between source system interpretations
- dbt transformation pipeline producing a golden 
  company record with automatic lineage capture
- Great Expectations quality suite enforcing CDE 
  thresholds in the pipeline before data reaches consumers
- A data catalogue entry consumable by any team at 
  Vantara without requiring tribal knowledge

---

## Repository Structure

| Folder / File | Purpose |
|---|---|
| `problem_statement.md` | Business context, stakeholder pain, and the case for a data product |
| `governance/cde_definitions.md` | Eight CDEs with business definitions, thresholds, and ownership |
| `governance/survivorship_rules.md` | Business decisions for resolving data conflicts |
| `governance/quality_spec.md` | Full quality specification per CDE |
| `governance/data_catalogue_entry.md` | Consumer-facing product documentation |
| `data/raw/` | Companies House source data (not committed — see data README) |
| `models/` | dbt staging and mart models |
| `tests/` | Great Expectations quality suite |
| `docs/` | Lineage diagrams and architectural documentation |

---

## Technology Stack

| Layer | Tool | Why |
|---|---|---|
| Source data | Companies House Bulk Data | Free, public, updated monthly, real quality issues |
| Database | DuckDB | Serverless, handles 5M+ rows locally, zero infrastructure cost |
| Transformation | dbt Core | Version-controlled SQL, automatic lineage, documented models |
| Quality monitoring | Great Expectations | Quality rules as code, pipeline gates, HTML reports |
| Catalogue | dbt docs + Markdown | Auto-generated lineage graph, browsable documentation |
| Version control | Git + GitHub | Full change history, public portfolio visibility |

---

## Governance Design Principles

This artefact is built on the same principles as a 
production data product:

**Governance before technology** — CDE definitions, 
survivorship rules, and quality thresholds were 
documented before any pipeline code was written.

**Quality as code** — quality rules live in the pipeline 
as executable tests, not in a policy document. 
A threshold breach stops the pipeline.

**Lineage by default** — every transformation is 
documented automatically by dbt. No manual lineage 
reconstruction required.

**Owned, not just published** — every CDE has a named 
owner. Every quality score has someone accountable for it.

---

## Status

- [x] Business problem statement
- [x] Stakeholder and department analysis  
- [x] CDE definitions (8 CDEs)
- [x] Survivorship rules
- [x] Quality specification
- [x] Data catalogue entry
- [x] dbt staging models
- [x] dbt golden record mart
- [x] Great Expectations quality suite
- [x] dbt docs published via GitHub Pages

---

## About This Project

Built by Tolu — Senior Data Governance and MDM 
professional specialising in data products, MDM, 
and data strategy for financial services and 
government organisations.

This portfolio artefact demonstrates end-to-end 
data product design and build capability, from 
business problem through to a governed, 
quality-assured, documented data asset.

[LinkedIn Profile](https://linkedin.com/in/tolu-olaosebikan-0aa38488)
