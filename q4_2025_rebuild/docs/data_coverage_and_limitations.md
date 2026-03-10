# Data Coverage and Limitations (Current Extract)

## Included now
- Global segment values are populated for all quarterly metric families from 2019 Q1 to 2025 Q4:
  - Incoming/outgoing counts and percentages
  - Outgoing average tenure
  - Gender, appointment, and first-timer splits (count + %)
- Full denominator coverage is populated for **all index and industry segments** from pages 38 and 39.
- Non-global segment rows are pre-created in metrics/splits for consistent Tableau filtering.
- Non-global **2025 Q4 metrics** (incoming/outgoing counts, rates, and tenure) are now populated for index and industry tables.

## Not yet included
- Non-global split values remain pending transcription for all quarters.
- Non-global metric values for quarters prior to 2025 Q4 remain pending transcription.

## Why
- Runtime environment lacks OCR tooling and package installs are blocked by proxy restrictions.
- Current pass prioritizes correctness and reproducibility with explicit coverage boundaries.

## QA status
- Split percentages pass integrity checks for populated rows.
- Denominator table is fully populated across both scopes.

- Non-global 2019–2023 metrics and gender/appointment splits are partially backfilled from legacy row-level datasets in this repository.
