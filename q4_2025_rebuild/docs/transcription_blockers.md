# Transcription Blockers (Direct Report-Table Extraction)

## Requested scope
Complete all remaining blank values in:
- `index_quarterly_metrics.csv`
- `index_quarterly_splits.csv`
- `industry_quarterly_metrics.csv`
- `industry_quarterly_splits.csv`

using **direct transcription from report JPEG tables** only.

## Blocking constraint in this runtime
- The uploaded report JPEGs are available in chat context, but not exposed as local files in the workspace filesystem.
- OCR tooling is unavailable in this environment, and prior attempts to install dependencies were blocked by network/proxy restrictions.
- Without file-level access to the JPEGs (or OCR), high-volume cell-by-cell direct transcription cannot be completed reliably via automation.

## What remains missing right now (from completion report)
- Metrics blank rows: 273 (index), 64 (industry)
- Splits blank rows: 3788 (index), 1116 (industry)
- Non-global first-timer split rows missing:
  - index: 1456/1456
  - industry: 560/560

## Required to finish exactly as requested
One of the following:
1. Provide the JPEGs as downloadable files in the workspace (or a mounted folder path), OR
2. Provide source tables as CSV/XLSX/PDF with selectable text, OR
3. Allow external OCR tooling/network install in this runtime.

With any of the above, the remaining rows can be transcribed directly and QA rerun to target zero blanks.
