# Global CEO Turnover Index (Q4 2025 Rebuild Workspace)

This folder is a **new, separate project workspace** for rebuilding the dashboard from the Q4 2025 report-table images (pages 1–39).

## What this contains
- A normalized data schema for Tableau-ready extracts.
- A page inventory so every source table is tracked.
- QA scripts/checklist for validating extracted counts and percentages.
- A dashboard design blueprint for a cleaner executive-ready Tableau experience.

## What this does **not** contain
- Any edits to the legacy Tableau workbook in the repository root.
- Any assumption of write access to your GitHub account or your local machine.

## Intended output datasets
1. `index_quarterly_metrics.csv`
2. `index_quarterly_splits.csv`
3. `industry_quarterly_metrics.csv`
4. `industry_quarterly_splits.csv`
5. `denominators_companies.csv`

These files should be joined in Tableau by `year`, `quarter`, `scope`, and `segment` fields.

## Current extraction status
- ✅ Global-level quarterly metrics/splits (2019 Q1–2025 Q4) are populated.
- ✅ Denominator counts are populated for all index + industry segments.
- ✅ 2025 Q4 non-global **metrics** are populated for all index + industry segments.
- ⚠️ Non-global split values and earlier non-global metrics remain pending transcription.
- See `docs/data_coverage_and_limitations.md` for details.


## Utility scripts
- `scripts/populate_global_from_report.py`: regenerates extracted CSVs.
- `scripts/qa_checks.py`: validates split percentage integrity.
- `scripts/coverage_report.py`: prints extraction population percentages.

- `scripts/fill_non_global_from_legacy_raw.py`: backfills non-global 2019–2023 metrics + gender/appointment splits from legacy row-level CSVs.
