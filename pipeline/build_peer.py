#!/usr/bin/env python3
"""Rebuild data/peer.json from the aggregated per-hospital CSV produced by aggregate_qb.py.

INPUT:  _agg_focus.csv  (ik, standort, code_type, code, count)
OUTPUT: data/peer.json  (per condition/procedure: the across-hospital volume distribution)

Usage:  python pipeline/build_peer.py --focus _agg_focus.csv --out data/peer.json
"""
from __future__ import annotations
import argparse, json
from pathlib import Path
import polars as pl
import numpy as np

GROUPS = [("Heart failure", "ICD", "I50"), ("Atrial fibrillation", "ICD", "I48"),
          ("Acute myocardial infarction", "ICD", "I21"), ("Chronic ischaemic heart disease", "ICD", "I25"),
          ("Stroke", "ICD", "I63"), ("Coronary angiography", "OPS", "1-275"), ("PCI (stent)", "OPS", "8-837")]


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--focus", default="_agg_focus.csv")
    ap.add_argument("--out", default="data/peer.json")
    a = ap.parse_args()
    f = pl.read_csv(a.focus)
    out = []
    for label, ct, pfx in GROUPS:
        per = (f.filter((pl.col("code_type") == ct) & pl.col("code").str.starts_with(pfx))
               .group_by(["ik", "standort"]).agg(pl.col("count").sum().alias("vol")))
        vols = sorted(int(v) for v in per["vol"].to_list())
        if not vols:
            continue
        arr = np.array(vols)
        out.append({"label": label, "code": pfx, "type": ct, "n": len(vols),
                    "median": int(np.median(arr)), "p90": int(np.percentile(arr, 90)),
                    "max": int(arr.max()), "vols": vols})
    data = {"vintage": "G-BA Quality Reports · Berichtsjahr 2024 · 2,220 hospital reports",
            "note": "Per-hospital case volumes; small counts (<4) suppressed by the source, so hospitals below threshold aren't shown.",
            "groups": out}
    Path(a.out).parent.mkdir(parents=True, exist_ok=True)
    json.dump(data, open(a.out, "w"), separators=(",", ":"))
    print(f"wrote {a.out}: {len(out)} condition/procedure groups")


if __name__ == "__main__":
    main()
