#!/usr/bin/env python3
"""Hard gate: fail if required extraction fields contain blanks."""
from __future__ import annotations
import csv
from pathlib import Path

DATA = Path(__file__).resolve().parents[1] / 'data' / 'extracted'
CHECKS = {
    'index_quarterly_metrics.csv': ['incoming_count','incoming_pct','outgoing_count','outgoing_pct','avg_outgoing_tenure_years'],
    'index_quarterly_splits.csv': ['count_value','pct_value'],
    'industry_quarterly_metrics.csv': ['incoming_count','incoming_pct','outgoing_count','outgoing_pct','avg_outgoing_tenure_years'],
    'industry_quarterly_splits.csv': ['count_value','pct_value'],
}

fails = []
for f, cols in CHECKS.items():
    with (DATA/f).open(newline='', encoding='utf-8') as fh:
        rows=list(csv.DictReader(fh))
    for c in cols:
        n=sum(1 for r in rows if str(r.get(c,''))=='')
        if n:
            fails.append((f,c,n))

if fails:
    print('FAIL: blank required fields remain')
    for f,c,n in fails:
        print(f'- {f}::{c} blank={n}')
    raise SystemExit(1)

print('PASS: no blanks in required fields')
