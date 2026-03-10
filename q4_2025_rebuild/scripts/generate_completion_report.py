#!/usr/bin/env python3
from __future__ import annotations
import csv
from pathlib import Path
from datetime import datetime

BASE = Path(__file__).resolve().parents[1]
DATA = BASE / 'data' / 'extracted'
OUT = BASE / 'docs' / 'final_completion_report.md'

FILES = {
    'index_quarterly_metrics.csv': ['incoming_count','incoming_pct','outgoing_count','outgoing_pct','avg_outgoing_tenure_years','company_count'],
    'index_quarterly_splits.csv': ['count_value','pct_value'],
    'industry_quarterly_metrics.csv': ['incoming_count','incoming_pct','outgoing_count','outgoing_pct','avg_outgoing_tenure_years','company_count'],
    'industry_quarterly_splits.csv': ['count_value','pct_value'],
    'denominators_companies.csv': ['company_count'],
}

def read_rows(p: Path):
    with p.open(newline='', encoding='utf-8') as f:
        return list(csv.DictReader(f))

lines = []
lines.append('# Final Completion Report (Data Extraction)')
lines.append('')
lines.append(f'_Generated: {datetime.utcnow().isoformat()}Z_')
lines.append('')

lines.append('## 1) Row counts')
lines.append('')
for name in FILES:
    rows = read_rows(DATA/name)
    lines.append(f'- `{name}`: **{len(rows)}** rows')
lines.append('')

lines.append('## 2) Field completion status')
lines.append('')

for name, cols in FILES.items():
    rows = read_rows(DATA/name)
    lines.append(f'### {name}')
    for c in cols:
        total = len(rows)
        filled = sum(1 for r in rows if str(r.get(c,'')) != '')
        pct = (filled/total*100) if total else 0
        status = '100% complete' if filled == total else 'incomplete'
        lines.append(f'- `{c}`: {filled}/{total} ({pct:.1f}%) — {status}')
    lines.append('')

# blank segment row check for four target files
lines.append('## 3) Segment-row blank audit')
lines.append('')

def blank_metric_row(r):
    return all(str(r.get(c,''))=='' for c in ['incoming_count','incoming_pct','outgoing_count','outgoing_pct','avg_outgoing_tenure_years'])

def blank_split_row(r):
    return all(str(r.get(c,''))=='' for c in ['count_value','pct_value'])

for name in ['index_quarterly_metrics.csv','industry_quarterly_metrics.csv']:
    rows = read_rows(DATA/name)
    blank = sum(1 for r in rows if blank_metric_row(r))
    lines.append(f'- `{name}` blank segment rows (all metric values empty): **{blank}**')
for name in ['index_quarterly_splits.csv','industry_quarterly_splits.csv']:
    rows = read_rows(DATA/name)
    blank = sum(1 for r in rows if blank_split_row(r))
    lines.append(f'- `{name}` blank segment rows (both split values empty): **{blank}**')
lines.append('')

# focused remaining gaps
idxs = read_rows(DATA/'index_quarterly_splits.csv')
inds = read_rows(DATA/'industry_quarterly_splits.csv')

def missing_first_timer(rows):
    filt=[r for r in rows if r['split_type']=='first_timer' and r['segment']!='Global']
    miss=sum(1 for r in filt if r.get('count_value','')=='' or r.get('pct_value','')=='')
    return len(filt), miss

a,b = missing_first_timer(idxs)
c,d = missing_first_timer(inds)
lines.append('## 4) Remaining known gaps')
lines.append('')
lines.append(f'- Index non-global first-timer split rows missing value(s): **{b}/{a}**')
lines.append(f'- Industry non-global first-timer split rows missing value(s): **{d}/{c}**')
lines.append('')
lines.append('## 5) Notes')
lines.append('')
lines.append('- This report reflects current files only. It does not perform OCR or attempt new inference.')
lines.append('- Any remaining blank rows need direct transcription from report-table images.')

OUT.write_text('\n'.join(lines), encoding='utf-8')
print(f'wrote {OUT}')
