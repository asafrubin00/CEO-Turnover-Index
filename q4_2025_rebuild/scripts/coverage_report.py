#!/usr/bin/env python3
from __future__ import annotations
import csv
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1] / 'data' / 'extracted'


def pct_populated(path: Path, value_cols):
    with path.open(newline='', encoding='utf-8') as f:
        rows=list(csv.DictReader(f))
    total=len(rows)*len(value_cols)
    filled=sum(1 for r in rows for c in value_cols if r.get(c,'')!='')
    return len(rows), filled, total, (filled/total*100 if total else 0)


def main():
    configs=[
        ('index_quarterly_metrics.csv',['incoming_count','incoming_pct','outgoing_count','outgoing_pct','avg_outgoing_tenure_years']),
        ('index_quarterly_splits.csv',['count_value','pct_value']),
        ('industry_quarterly_metrics.csv',['incoming_count','incoming_pct','outgoing_count','outgoing_pct','avg_outgoing_tenure_years']),
        ('industry_quarterly_splits.csv',['count_value','pct_value']),
        ('denominators_companies.csv',['company_count']),
    ]
    for name, cols in configs:
        rows,filled,total,p=pct_populated(ROOT/name, cols)
        print(f"{name}: rows={rows}, populated={filled}/{total} ({p:.1f}%)")

if __name__=='__main__':
    main()
