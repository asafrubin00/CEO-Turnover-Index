#!/usr/bin/env python3
"""Fill non-global 2019-2023 metrics and selected splits from legacy processed row-level CSVs.

This uses repository files `incoming_ceos_processed.csv` and `outgoing_ceos_processed.csv`.
It populates:
- metrics: incoming/outgoing counts, percentages, and outgoing avg tenure (where derivable)
- splits: gender + appointment (count/%), for non-global rows up to 2023

It does not infer first-timer non-global splits.
"""
from __future__ import annotations
import csv
from collections import defaultdict
from pathlib import Path

BASE = Path(__file__).resolve().parents[1] / "data" / "extracted"

INDEX_MAP = {
    "S&P 500": "SP500",
    "FTSE100": "FTSE100",
    "ASX200": "ASX200",
    "CAC40": "CAC40",
    "DAX40": "DAX40",
    "EuroNext100": "EuroNext100",
    "FTSE250": "FTSE250",
    "HANG SENG": "HANGSENG",
    "Nikkei 225": "Nikkei225",
    "NSE Nifty": "NSENifty50",
    "S&P/TSX Composite": "SPTSX Composite",
    "STI": "STI",
    "SMI": "SMI",
}
INDUSTRIES = {"Consumer", "Financial Services", "Healthcare", "Industrial", "Technology"}


def load_denominators():
    out = {}
    with (BASE / "denominators_companies.csv").open(newline="", encoding="utf-8") as f:
        for r in csv.DictReader(f):
            out[(r["scope"], int(r["year"]), int(r["quarter"]), r["segment"])] = float(r["company_count"])
    return out


def aggregate_incoming():
    tot_idx = defaultdict(int)
    g_idx = defaultdict(lambda: defaultdict(int))
    a_idx = defaultdict(lambda: defaultdict(int))
    tot_ind = defaultdict(int)
    g_ind = defaultdict(lambda: defaultdict(int))
    a_ind = defaultdict(lambda: defaultdict(int))
    with open("incoming_ceos_processed.csv", newline="", encoding="utf-8") as f:
        for r in csv.DictReader(f):
            y = int(float(r["start_year"])); q = int(float(r["start_quarter"]))
            if y < 2019 or y > 2023:
                continue
            idx = INDEX_MAP.get(r["index"])
            gender = "Men" if r["gender"].strip().lower().startswith("m") else "Women"
            appt = "Internal" if r["appointment"].strip().lower().startswith("int") else "External"
            if idx:
                k = (y, q, idx)
                tot_idx[k] += 1; g_idx[k][gender] += 1; a_idx[k][appt] += 1
            ind = r["industry"].strip()
            if ind in INDUSTRIES:
                k = (y, q, ind)
                tot_ind[k] += 1; g_ind[k][gender] += 1; a_ind[k][appt] += 1
    return tot_idx, g_idx, a_idx, tot_ind, g_ind, a_ind


def aggregate_outgoing():
    tot_idx = defaultdict(int)
    g_idx = defaultdict(lambda: defaultdict(int))
    a_idx = defaultdict(lambda: defaultdict(int))
    ten_idx = defaultdict(list)
    tot_ind = defaultdict(int)
    g_ind = defaultdict(lambda: defaultdict(int))
    a_ind = defaultdict(lambda: defaultdict(int))
    ten_ind = defaultdict(list)
    with open("outgoing_ceos_processed.csv", newline="", encoding="utf-8") as f:
        for r in csv.DictReader(f):
            y = int(float(r["end_year"])); q = int(float(r["end_quarter"]))
            if y < 2019 or y > 2023:
                continue
            idx = INDEX_MAP.get(r["index"])
            gender = "Men" if r["gender"].strip().lower().startswith("m") else "Women"
            appt = "Internal" if r["appointment"].strip().lower().startswith("int") else "External"
            tenure = float(r["tenure_year"]) if r.get("tenure_year") else None
            if idx:
                k = (y, q, idx)
                tot_idx[k] += 1; g_idx[k][gender] += 1; a_idx[k][appt] += 1
                if tenure is not None: ten_idx[k].append(tenure)
            ind = r["industry"].strip()
            if ind in INDUSTRIES:
                k = (y, q, ind)
                tot_ind[k] += 1; g_ind[k][gender] += 1; a_ind[k][appt] += 1
                if tenure is not None: ten_ind[k].append(tenure)
    return tot_idx, g_idx, a_idx, ten_idx, tot_ind, g_ind, a_ind, ten_ind


def write_rows(path, rows):
    with path.open("w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=list(rows[0].keys()))
        w.writeheader(); w.writerows(rows)


def fill_metrics(path, scope, inc_tot, out_tot, out_ten, denom):
    with path.open(newline="", encoding="utf-8") as f:
        rows = list(csv.DictReader(f))
    for r in rows:
        y = int(r["year"]); q = int(r["quarter"]); seg = r["segment"]
        if seg == "Global" or y > 2023:
            continue
        key = (y, q, seg)
        den = denom.get((scope, y, q, seg))
        if key in inc_tot:
            r["incoming_count"] = str(inc_tot[key])
            if den: r["incoming_pct"] = f"{inc_tot[key] / den * 100:.1f}"
        if key in out_tot:
            r["outgoing_count"] = str(out_tot[key])
            if den: r["outgoing_pct"] = f"{out_tot[key] / den * 100:.1f}"
        if key in out_ten and out_ten[key]:
            r["avg_outgoing_tenure_years"] = f"{sum(out_ten[key]) / len(out_ten[key]):.1f}"
    write_rows(path, rows)


def fill_splits(path, inc_g, inc_a, out_g, out_a):
    with path.open(newline="", encoding="utf-8") as f:
        rows = list(csv.DictReader(f))
    for r in rows:
        y = int(r["year"]); q = int(r["quarter"]); seg = r["segment"]
        if seg == "Global" or y > 2023:
            continue
        if r["split_type"] == "first_timer":
            continue
        key = (y, q, seg)
        src = None
        if r["flow"] == "incoming" and r["split_type"] == "gender": src = inc_g.get(key, {})
        if r["flow"] == "incoming" and r["split_type"] == "appointment": src = inc_a.get(key, {})
        if r["flow"] == "outgoing" and r["split_type"] == "gender": src = out_g.get(key, {})
        if r["flow"] == "outgoing" and r["split_type"] == "appointment": src = out_a.get(key, {})
        if src is None:
            continue
        total = sum(src.values())
        val = src.get(r["split_value"], 0)
        if total > 0:
            r["count_value"] = str(val)
            r["pct_value"] = f"{val / total * 100:.1f}"
    write_rows(path, rows)


def main():
    denom = load_denominators()
    inc_tot_i, inc_g_i, inc_a_i, inc_tot_d, inc_g_d, inc_a_d = aggregate_incoming()
    out_tot_i, out_g_i, out_a_i, out_t_i, out_tot_d, out_g_d, out_a_d, out_t_d = aggregate_outgoing()

    fill_metrics(BASE / "index_quarterly_metrics.csv", "index", inc_tot_i, out_tot_i, out_t_i, denom)
    fill_metrics(BASE / "industry_quarterly_metrics.csv", "industry", inc_tot_d, out_tot_d, out_t_d, denom)
    fill_splits(BASE / "index_quarterly_splits.csv", inc_g_i, inc_a_i, out_g_i, out_a_i)
    fill_splits(BASE / "industry_quarterly_splits.csv", inc_g_d, inc_a_d, out_g_d, out_a_d)


if __name__ == "__main__":
    main()
