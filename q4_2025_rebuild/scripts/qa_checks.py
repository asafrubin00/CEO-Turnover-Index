#!/usr/bin/env python3
"""Basic QA checks for extracted CEO turnover CSVs."""

from __future__ import annotations
import csv
from collections import defaultdict
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1] / "data" / "extracted"


def read_rows(path: Path):
    with path.open(newline="", encoding="utf-8") as f:
        return list(csv.DictReader(f))


def to_float(value: str):
    if value is None or value == "":
        return None
    v = value.strip().replace("%", "")
    try:
        return float(v)
    except ValueError:
        return None


def check_split_pairs(rows):
    errs = []
    bucket = defaultdict(lambda: {"count": 0.0, "pct": 0.0, "n": 0})
    for r in rows:
        k = (r["year"], r["quarter"], r["segment"], r["flow"], r["split_type"])
        c = to_float(r.get("count_value", ""))
        p = to_float(r.get("pct_value", ""))
        if c is not None:
            bucket[k]["count"] += c
        if p is not None:
            bucket[k]["pct"] += p
        bucket[k]["n"] += 1

    for key, agg in bucket.items():
        if agg["n"] == 2 and agg["pct"]:
            if abs(agg["pct"] - 100.0) > 1.0:
                errs.append(f"pct split != 100 for {key}: {agg['pct']:.2f}")
    return errs


def main():
    split_files = [ROOT / "index_quarterly_splits.csv", ROOT / "industry_quarterly_splits.csv"]
    all_errs = []
    for f in split_files:
        if not f.exists():
            print(f"WARN missing {f}")
            continue
        rows = read_rows(f)
        if not rows:
            print(f"WARN empty {f.name}")
            continue
        errs = check_split_pairs(rows)
        if errs:
            print(f"FAIL {f.name}")
            for e in errs[:50]:
                print(" -", e)
        else:
            print(f"PASS {f.name}")
        all_errs.extend(errs)

    if all_errs:
        raise SystemExit(1)


if __name__ == "__main__":
    main()
