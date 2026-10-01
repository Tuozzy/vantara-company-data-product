# quality_checks.py
# Great Expectations quality suite for the Vantara Company Data Product
# Enforces CDE thresholds defined in governance/quality_spec.md
# Run this after every dbt pipeline run to validate the golden record

import duckdb
import json
from datetime import datetime

# Connect to the DuckDB database
conn = duckdb.connect("vantara_dbt/dev.duckdb")

# Results store
results = []
passed = 0
failed = 0
warnings = 0


def check(name, cde, dimension, threshold, actual, gate_type="HARD"):
    """
    Evaluate a single quality check and record the result.
    gate_type: HARD = pipeline stops on failure, WARN = logged but continues
    """
    global passed, failed, warnings

    status = "PASS" if actual >= threshold else "FAIL"
    rag = "GREEN" if actual >= threshold else (
        "AMBER" if actual >= threshold * 0.95 else "RED"
    )

    if status == "FAIL":
        if gate_type == "HARD":
            failed += 1
        else:
            warnings += 1
    else:
        passed += 1

    result = {
        "cde": cde,
        "check": name,
        "dimension": dimension,
        "threshold": f"{threshold:.1%}",
        "actual": f"{actual:.1%}",
        "status": status,
        "rag": rag,
        "gate": gate_type
    }
    results.append(result)
    return result


print("=" * 60)
print("VANTARA COMPANY DATA PRODUCT — QUALITY SCORECARD")
print(f"Run date: {datetime.now().strftime('%Y-%m-%d %H:%M')}")
print("=" * 60)

# ── Fetch base counts ──────────────────────────────────────────

total = conn.execute(
    "SELECT COUNT(*) FROM main.golden_company_record"
).fetchone()[0]

active = conn.execute(
    "SELECT COUNT(*) FROM main.golden_company_record "
    "WHERE company_status_vantara = 'ACTIVE'"
).fetchone()[0]

active_18m = conn.execute(
    "SELECT COUNT(*) FROM main.golden_company_record "
    "WHERE company_status_vantara = 'ACTIVE' "
    "AND incorporation_date <= current_date - interval '18 months'"
).fetchone()[0]

# ── CDE 1 — Company Number ─────────────────────────────────────

null_company_number = conn.execute(
    "SELECT COUNT(*) FROM main.golden_company_record "
    "WHERE company_number IS NULL OR trim(company_number) = ''"
).fetchone()[0]

duplicate_company_number = conn.execute(
    "SELECT COUNT(*) - COUNT(DISTINCT company_number) "
    "FROM main.golden_company_record"
).fetchone()[0]

check("Company Number — Completeness", "CDE 1", "Completeness",
      1.0, (total - null_company_number) / total, "HARD")

check("Company Number — Uniqueness", "CDE 1", "Uniqueness",
      1.0, (total - duplicate_company_number) / total, "HARD")

# ── CDE 2 — Registered Name ────────────────────────────────────

null_name = conn.execute(
    "SELECT COUNT(*) FROM main.golden_company_record "
    "WHERE company_status_vantara = 'ACTIVE' "
    "AND (registered_name IS NULL OR trim(registered_name) = '')"
).fetchone()[0]

check("Registered Name — Completeness", "CDE 2", "Completeness",
      1.0, (active - null_name) / active, "HARD")

# ── CDE 3 — Company Status ─────────────────────────────────────

unmapped = conn.execute(
    "SELECT COUNT(*) FROM main.golden_company_record "
    "WHERE company_status_vantara = 'UNMAPPED'"
).fetchone()[0]

check("Company Status — No Unmapped Values", "CDE 3", "Validity",
      1.0, (total - unmapped) / total, "HARD")

# ── CDE 4 — Registered Address ────────────────────────────────

null_postcode = conn.execute(
    "SELECT COUNT(*) FROM main.golden_company_record "
    "WHERE company_status_vantara = 'ACTIVE' "
    "AND (post_code IS NULL OR trim(post_code) = '')"
).fetchone()[0]

null_address1 = conn.execute(
    "SELECT COUNT(*) FROM main.golden_company_record "
    "WHERE company_status_vantara = 'ACTIVE' "
    "AND (address_line_1 IS NULL OR trim(address_line_1) = '')"
).fetchone()[0]

check("Registered Address — PostCode Completeness", "CDE 4",
      "Completeness", 0.95,
      (active - null_postcode) / active, "WARN")

check("Registered Address — AddressLine1 Completeness", "CDE 4",
      "Completeness", 0.98,
      (active - null_address1) / active, "WARN")

# ── CDE 5 — SIC Code ──────────────────────────────────────────

unknown_sic = conn.execute(
    "SELECT COUNT(*) FROM main.golden_company_record "
    "WHERE company_status_vantara = 'ACTIVE' "
    "AND sic_code_primary = 'UNKNOWN'"
).fetchone()[0]

check("SIC Code — Completeness", "CDE 5", "Completeness",
      0.90, (active - unknown_sic) / active, "WARN")

# ── CDE 6 — Incorporation Date ────────────────────────────────

null_inc_date = conn.execute(
    "SELECT COUNT(*) FROM main.golden_company_record "
    "WHERE incorporation_date IS NULL"
).fetchone()[0]

check("Incorporation Date — Completeness", "CDE 6", "Completeness",
      1.0, (total - null_inc_date) / total, "HARD")

# ── CDE 7 — Last Accounts Date ───────────────────────────────

null_accounts = conn.execute(
    "SELECT COUNT(*) FROM main.golden_company_record "
    "WHERE company_status_vantara = 'ACTIVE' "
    "AND last_accounts_date IS NULL "
    "AND incorporation_date <= current_date - interval '18 months'"
).fetchone()[0]

check("Last Accounts Date — Completeness", "CDE 7", "Completeness",
      0.85, (active_18m - null_accounts) / active_18m, "WARN")

# ── CDE 8 — Confirmation Statement Date ──────────────────────

null_conf = conn.execute(
    "SELECT COUNT(*) FROM main.golden_company_record "
    "WHERE company_status_vantara = 'ACTIVE' "
    "AND confirmation_statement_date IS NULL"
).fetchone()[0]

check("Confirmation Statement Date — Completeness", "CDE 8",
      "Completeness", 0.85,
      (active - null_conf) / active, "WARN")

# ── Print Scorecard ───────────────────────────────────────────

print(f"\n{'CDE':<8} {'Check':<45} {'Threshold':>10} {'Actual':>10} {'Status':>6} {'RAG':>7} {'Gate':>5}")
print("-" * 100)

for r in results:
    rag_symbol = "🟢" if r["rag"] == "GREEN" else "🟡" if r["rag"] == "AMBER" else "🔴"
    print(
        f"{r['cde']:<8} {r['check']:<45} {r['threshold']:>10} "
        f"{r['actual']:>10} {r['status']:>6} {rag_symbol:>4}  {r['gate']:>5}"
    )

print("-" * 100)
print(f"\nSUMMARY: {passed} PASSED | {warnings} WARNINGS | {failed} HARD FAILURES")

if failed > 0:
    print("\n🔴 PIPELINE GATE: HARD STOP — fix failures before publishing golden record")
elif warnings > 0:
    print("\n🟡 PIPELINE GATE: WARNINGS PRESENT — golden record published with quality flags")
else:
    print("\n🟢 PIPELINE GATE: ALL CHECKS PASSED — golden record published")

# ── Save results to JSON ──────────────────────────────────────

output = {
    "run_date": datetime.now().isoformat(),
    "total_companies": total,
    "active_companies": active,
    "summary": {
        "passed": passed,
        "warnings": warnings,
        "hard_failures": failed
    },
    "checks": results
}

with open("tests/quality_report.json", "w") as f:
    json.dump(output, f, indent=2)

print(f"\nFull report saved to tests/quality_report.json")
conn.close()