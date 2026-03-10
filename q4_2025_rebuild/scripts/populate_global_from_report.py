#!/usr/bin/env python3
"""Populate extracted CSVs with GLOBAL values + full denominator tables from report pages 3-39."""
from __future__ import annotations
import csv
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1] / "data" / "extracted"
years = list(range(2019, 2026))
quarters = [1, 2, 3, 4]
index_segments = ["Global","SP500","FTSE100","ASX200","CAC40","DAX40","EuroNext100","FTSE250","HANGSENG","Nikkei225","NSENifty50","SPTSX Composite","STI","SMI"]
industry_segments = ["Global","Consumer","Financial Services","Healthcare","Industrial","Technology"]

# Ordered 2019Q1..2025Q4
incoming_count = [53,81,41,38,59,63,46,37,69,59,33,26,59,63,39,33,56,74,27,24,73,67,48,31,54,72,50,37]
incoming_pct   = [2.9,4.0,2.2,2.1,3.2,3.4,2.5,2.0,3.7,3.2,1.8,1.4,3.2,3.4,2.1,1.8,3.0,4.0,1.5,1.3,4.0,3.6,2.6,1.7,2.9,3.9,2.7,2.0]
outgoing_count = [41,63,34,44,66,52,30,39,53,56,25,32,46,65,40,50,41,70,39,36,58,65,42,37,55,64,56,59]
outgoing_pct   = [2.2,3.4,1.8,2.4,3.6,2.8,1.6,2.1,2.9,3.0,1.4,1.7,2.5,3.5,2.2,2.7,2.2,3.8,2.1,2.0,3.1,3.5,2.3,2.0,3.0,3.5,3.0,3.2]
avg_tenure     = [7.7,7.2,6.2,6.9,8.5,7.7,6.6,9.4,9.8,6.6,9.7,7.8,7.7,7.7,6.7,7.3,9.1,9.2,6.2,7.8,8.1,7.3,6.4,7.9,6.6,6.7,8.7,6.7]

in_gender_c=[(49,4),(74,7),(37,4),(35,3),(55,4),(58,5),(43,3),(34,3),(59,10),(55,4),(30,3),(26,0),(51,8),(53,10),(34,5),(31,2),(48,8),(66,8),(23,4),(22,2),(68,5),(60,7),(41,7),(26,5),(48,6),(67,5),(46,4),(33,4)]
in_gender_p=[(92.5,7.5),(91.4,8.6),(90.2,9.8),(92.1,7.9),(93.2,6.8),(92.1,7.9),(93.5,6.5),(91.9,8.1),(85.5,14.5),(93.2,6.8),(90.9,9.1),(100,0),(86.4,13.6),(84.1,15.9),(87.2,12.8),(93.9,6.1),(85.7,14.3),(89.2,10.8),(85.2,14.8),(91.7,8.3),(93.2,6.8),(89.6,10.4),(85.4,14.6),(83.9,16.1),(88.9,11.1),(93.1,6.9),(92.0,8.0),(89.2,10.9)]
in_appt_c=[(40,13),(67,14),(20,21),(27,11),(37,22),(50,13),(22,24),(20,17),(47,22),(44,15),(21,12),(16,10),(42,17),(49,14),(27,12),(21,12),(39,17),(57,17),(20,7),(15,9),(53,20),(54,13),(33,15),(20,11),(39,15),(59,13),(28,22),(19,18)]
in_appt_p=[(75.5,24.5),(82.7,17.3),(48.8,51.2),(71.1,28.9),(62.7,37.3),(79.4,20.6),(47.8,52.2),(54.1,45.9),(68.1,31.9),(74.6,25.4),(63.6,36.4),(61.5,38.5),(71.2,28.8),(77.8,22.2),(69.2,30.8),(63.6,36.4),(69.6,30.4),(77.0,23.0),(74.1,25.9),(62.5,37.5),(72.6,27.4),(80.6,19.4),(68.8,31.2),(64.5,35.5),(72.2,27.8),(81.9,18.1),(56.0,44.0),(51.4,48.6)]
in_ft_c=[(45,8),(72,9),(37,4),(33,5),(49,10),(57,6),(33,13),(33,4),(58,11),(51,8),(27,6),(20,6),(53,6),(59,4),(35,4),(24,9),(48,8),(66,8),(24,3),(20,4),(67,6),(59,8),(34,14),(26,5),(45,9),(67,5),(42,8),(30,7)]
in_ft_p=[(84.9,15.1),(88.9,11.1),(90.2,9.8),(86.8,13.2),(83.1,16.9),(90.5,9.5),(71.7,28.3),(89.2,10.8),(84.1,15.9),(86.4,13.6),(81.8,18.2),(76.9,23.1),(89.8,10.2),(93.7,6.3),(89.7,10.3),(72.7,27.3),(85.7,14.3),(89.2,10.8),(88.9,11.1),(83.3,16.7),(91.8,8.2),(88.1,11.9),(70.8,29.2),(83.9,16.1),(83.3,16.7),(93.1,6.9),(84.0,16.0),(81.1,18.9)]
out_gender_c=[(39,2),(62,1),(32,2),(41,3),(63,3),(47,5),(30,0),(38,1),(51,2),(54,2),(25,0),(31,1),(45,1),(63,2),(39,1),(49,1),(37,4),(68,2),(33,6),(31,5),(56,2),(62,3),(37,5),(35,2),(54,1),(60,4),(52,4),(51,8)]
out_gender_p=[(95.1,4.9),(98.4,1.6),(94.1,5.9),(93.2,6.8),(95.5,4.5),(90.4,9.6),(100,0),(97.4,2.6),(96.2,3.8),(96.4,3.6),(100,0),(96.9,3.1),(97.8,2.2),(96.9,3.1),(97.5,2.5),(98.0,2.0),(90.2,9.8),(97.1,2.9),(84.6,15.4),(86.1,13.9),(96.6,3.4),(95.4,4.6),(88.1,11.9),(94.6,5.4),(98.2,1.8),(93.8,6.2),(92.9,7.1),(86.4,13.6)]
out_appt_c=[(32,9),(53,10),(25,9),(31,13),(50,16),(38,14),(17,13),(30,9),(42,11),(39,17),(21,4),(25,7),(36,10),(45,20),(26,14),(28,22),(31,10),(52,18),(24,15),(26,10),(40,18),(47,18),(30,12),(28,9),(31,24),(46,18),(38,18),(44,15)]
out_appt_p=[(78.0,22.0),(84.1,15.9),(73.5,26.5),(70.5,29.5),(75.8,24.2),(73.1,26.9),(56.7,43.3),(76.9,23.1),(79.2,20.8),(69.6,30.4),(84.0,16.0),(78.1,21.9),(78.3,21.7),(69.2,30.8),(65.0,35.0),(56.0,44.0),(75.6,24.4),(74.3,25.7),(61.5,38.5),(72.2,27.8),(69.0,31.0),(72.3,27.7),(71.4,28.6),(75.7,24.3),(56.4,43.6),(71.9,28.1),(67.9,32.1),(74.6,25.4)]
out_ft_c=[(34,7),(52,11),(27,7),(38,6),(58,8),(47,5),(26,4),(34,5),(45,8),(54,2),(24,1),(31,1),(39,7),(58,7),(33,7),(43,7),(37,4),(62,8),(33,6),(29,7),(49,9),(54,11),(37,5),(32,5),(44,11),(58,6),(47,9),(52,7)]
out_ft_p=[(82.9,17.1),(82.5,17.5),(79.4,20.6),(86.4,13.6),(87.9,12.1),(90.4,9.6),(86.7,13.3),(87.2,12.8),(84.9,15.1),(96.4,3.6),(96.0,4.0),(96.9,3.1),(84.8,15.2),(89.2,10.8),(82.5,17.5),(86.0,14.0),(90.2,9.8),(88.6,11.4),(84.6,15.4),(80.6,19.4),(84.5,15.5),(83.1,16.9),(88.1,11.9),(86.5,13.5),(80.0,20.0),(90.6,9.4),(83.9,16.1),(88.1,11.9)]

# Full denominator tables (page 38 and 39)

index_2025q4_metrics = {
"Global": (37,2.0,59,3.2,6.7),
"SP500": (9,1.8,9,1.8,10.9),
"FTSE100": (3,3.0,7,7.0,6.5),
"ASX200": (12,6.0,12,6.0,7.1),
"CAC40": (0,0.0,1,2.5,5.0),
"DAX40": (1,2.5,2,5.0,8.9),
"EuroNext100": (1,1.0,1,1.0,5.0),
"FTSE250": (2,0.8,9,3.6,4.9),
"HANGSENG": (3,3.4,7,7.9,5.2),
"Nikkei225": (0,0.0,1,0.4,5.2),
"NSENifty50": (2,4.0,2,4.0,1.4),
"SPTSX Composite": (3,1.3,6,2.6,6.2),
"STI": (1,3.3,2,6.7,5.1),
"SMI": (0,0.0,0,0.0,0.0),
}

industry_2025q4_metrics = {
"Global": (37,2.0,59,3.2,6.7),
"Consumer": (12,3.8,15,4.7,4.4),
"Financial Services": (6,1.3,12,2.6,11.1),
"Healthcare": (3,2.7,5,4.5,10.7),
"Industrial": (12,1.6,22,3.0,5.3),
"Technology": (4,1.9,5,2.3,4.7),
}

index_company_table = {
"Global":[1855,1855,1855,1855,1855,1855,1855,1855,1855,1855,1855,1855,1855,1855,1855,1855,1855,1842,1842,1857,1859,1860,1869,1862,1857,1853,1855,1855],
"SP500":[500,500,500,500,500,500,500,500,500,500,500,500,500,500,500,500,500,500,500,500,501,500,503,500,500,500,500,500],
"FTSE100":[100,100,100,100,100,100,100,100,100,100,100,100,100,100,100,100,100,100,100,100,100,100,102,100,100,100,99,99],
"ASX200":[200,200,200,200,200,200,200,200,200,200,200,200,200,200,200,200,200,200,200,197,199,199,202,199,200,201,201,201],
"CAC40":[40,40,40,40,40,40,40,40,40,40,40,40,40,40,40,40,40,40,40,40,40,40,40,40,40,40,41,41],
"DAX40":[40,40,40,40,40,40,40,40,40,40,40,40,40,40,40,40,40,40,40,40,39,40,40,41,40,40,39,39],
"EuroNext100":[100,100,100,100,100,100,100,100,100,100,100,100,100,100,100,100,100,83,83,100,100,100,99,101,101,100,100,100],
"FTSE250":[250,250,250,250,250,250,250,250,250,250,250,250,250,250,250,250,250,250,250,250,250,249,251,250,250,250,249,249],
"HANGSENG":[75,75,75,75,75,75,75,75,75,75,75,75,75,75,75,75,75,78,78,82,82,82,82,83,83,85,88,88],
"Nikkei225":[225,225,225,225,225,225,225,225,225,225,225,225,225,225,225,225,225,225,225,225,225,225,225,225,225,225,224,224],
"NSENifty50":[50,50,50,50,50,50,50,50,50,50,50,50,50,50,50,50,50,50,50,50,50,50,50,50,50,50,50,50],
"SPTSX Composite":[226,226,226,226,226,226,226,226,226,226,226,226,226,226,226,226,226,226,226,223,223,225,225,223,218,212,213,213],
"STI":[29,29,29,29,29,29,29,29,29,29,29,29,29,29,29,29,29,30,30,30,30,30,30,30,30,30,30,30],
"SMI":[20,20,20,20,20,20,20,20,20,20,20,20,20,20,20,20,20,20,20,20,20,20,20,20,20,20,21,21],
}

industry_company_table = {
"Global":[1855,1855,1855,1855,1855,1855,1855,1855,1855,1855,1855,1855,1855,1855,1855,1855,1855,1842,1842,1857,1859,1860,1869,1862,1857,1853,1855,1855],
"Consumer":[321,321,321,321,321,321,321,321,321,321,321,321,321,321,321,321,321,319,319,324,326,325,327,318,319,323,322,322],
"Financial Services":[465,465,465,465,465,465,465,465,465,465,465,465,465,465,465,465,465,462,462,458,457,460,467,466,466,472,470,470],
"Healthcare":[111,111,111,111,111,111,111,111,111,111,111,111,111,111,111,111,111,110,110,113,112,110,112,111,113,110,113,113],
"Industrial":[743,743,743,743,743,743,743,743,743,743,743,743,743,743,743,743,743,738,738,747,746,744,741,739,733,724,727,727],
"Technology":[215,215,215,215,215,215,215,215,215,215,215,215,215,215,215,215,215,213,213,215,218,221,222,228,226,224,223,223],
}


def write_csv(path: Path, fieldnames, rows):
    with path.open("w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=fieldnames)
        w.writeheader()
        w.writerows(rows)


def make_metrics_rows(segments, company_table, q4_overrides):
    rows=[]
    i=0
    for y in years:
        for q in quarters:
            for seg in segments:
                company_count = company_table[seg][i]
                if seg == "Global":
                    rows.append({"year":y,"quarter":q,"segment":seg,"incoming_count":incoming_count[i],"incoming_pct":incoming_pct[i],"outgoing_count":outgoing_count[i],"outgoing_pct":outgoing_pct[i],"avg_outgoing_tenure_years":avg_tenure[i],"company_count":company_count})
                elif y == 2025 and q == 4 and seg in q4_overrides:
                    inc_c, inc_p, out_c, out_p, ten = q4_overrides[seg]
                    rows.append({"year":y,"quarter":q,"segment":seg,"incoming_count":inc_c,"incoming_pct":inc_p,"outgoing_count":out_c,"outgoing_pct":out_p,"avg_outgoing_tenure_years":ten,"company_count":company_count})
                else:
                    rows.append({"year":y,"quarter":q,"segment":seg,"incoming_count":"","incoming_pct":"","outgoing_count":"","outgoing_pct":"","avg_outgoing_tenure_years":"","company_count":company_count})
            i += 1
    return rows


def make_split_rows(segments):
    rows=[]
    i=0
    split_defs=[("incoming","gender",("Men","Women")),("incoming","appointment",("Internal","External")),("incoming","first_timer",("Yes","No")),("outgoing","gender",("Men","Women")),("outgoing","appointment",("Internal","External")),("outgoing","first_timer",("Yes","No"))]
    for y in years:
        for q in quarters:
            for seg in segments:
                if seg == "Global":
                    values={
                        ("incoming","gender"):(in_gender_c[i],in_gender_p[i]),
                        ("incoming","appointment"):(in_appt_c[i],in_appt_p[i]),
                        ("incoming","first_timer"):(in_ft_c[i],in_ft_p[i]),
                        ("outgoing","gender"):(out_gender_c[i],out_gender_p[i]),
                        ("outgoing","appointment"):(out_appt_c[i],out_appt_p[i]),
                        ("outgoing","first_timer"):(out_ft_c[i],out_ft_p[i]),
                    }
                    for flow,stype,svals in split_defs:
                        cvals,pvals = values[(flow,stype)]
                        for j, sval in enumerate(svals):
                            rows.append({"year":y,"quarter":q,"segment":seg,"flow":flow,"split_type":stype,"split_value":sval,"count_value":cvals[j],"pct_value":pvals[j]})
                else:
                    for flow,stype,svals in split_defs:
                        for sval in svals:
                            rows.append({"year":y,"quarter":q,"segment":seg,"flow":flow,"split_type":stype,"split_value":sval,"count_value":"","pct_value":""})
            i += 1
    return rows


def make_denominator_rows(scope, table):
    rows=[]
    idx=0
    for y in years:
        for q in quarters:
            for seg, values in table.items():
                rows.append({"year":y,"quarter":q,"scope":scope,"segment":seg,"company_count":values[idx]})
            idx += 1
    return rows


def main():
    index_metrics = make_metrics_rows(index_segments, index_company_table, index_2025q4_metrics)
    industry_metrics = make_metrics_rows(industry_segments, industry_company_table, industry_2025q4_metrics)
    index_splits = make_split_rows(index_segments)
    industry_splits = make_split_rows(industry_segments)
    den = make_denominator_rows("index", index_company_table) + make_denominator_rows("industry", industry_company_table)

    write_csv(ROOT / "index_quarterly_metrics.csv", ["year","quarter","segment","incoming_count","incoming_pct","outgoing_count","outgoing_pct","avg_outgoing_tenure_years","company_count"], index_metrics)
    write_csv(ROOT / "index_quarterly_splits.csv", ["year","quarter","segment","flow","split_type","split_value","count_value","pct_value"], index_splits)
    write_csv(ROOT / "industry_quarterly_metrics.csv", ["year","quarter","segment","incoming_count","incoming_pct","outgoing_count","outgoing_pct","avg_outgoing_tenure_years","company_count"], industry_metrics)
    write_csv(ROOT / "industry_quarterly_splits.csv", ["year","quarter","segment","flow","split_type","split_value","count_value","pct_value"], industry_splits)
    write_csv(ROOT / "denominators_companies.csv", ["year","quarter","scope","segment","company_count"], den)


if __name__ == "__main__":
    main()
