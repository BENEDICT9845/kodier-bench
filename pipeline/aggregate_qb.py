#!/usr/bin/env python3
"""Aggregate the G-BA per-hospital Quality-Report XML into a compact per-hospital
focus-code table. RUN THIS WHERE THE XML LIVES (it's ~1.7 GB, thousands of files).

INPUT:  a folder of Quality-Report XML (the main reports are the *-xml.xml files,
        root <Qualitaetsbericht>; the *-das.xml / *-IQTIG_*.xml are supplements, skipped).
        Source: qb-datenportal.g-ba.de  (order form -> credentials -> bulk XML download).

OUTPUT: _agg_focus.csv  (ik, standort, code_type, code, count) — cardiology focus codes,
                          non-suppressed only (source masks counts < 4 as *_Datenschutz)
        _agg_hosp.csv   (ik, standort, name)

These two small CSVs are the input to build_peer.py. Raw XML is NOT committed.

Usage:  python pipeline/aggregate_qb.py --xml /path/to/xml_2024 --out .
"""
from __future__ import annotations
import argparse, csv, glob
from pathlib import Path
from lxml import etree

ICD_PREFIX = ("I",)                                   # cardiovascular chapter
OPS_PREFIX = ("1-27", "8-83", "8-84", "5-37", "8-64")  # cardiac procedures


def rf(el, t):
    c = el.find(".//{*}" + t)
    return c.text.strip() if c is not None and c.text else None


def ch(el, t):
    c = el.find("{*}" + t)
    return c.text.strip() if c is not None and c.text else None


def cnt(el, t):
    c = el.find("{*}" + t)
    if c is not None and c.text and c.text.strip():
        try:
            return int(c.text.strip().replace(".", ""))
        except ValueError:
            return None
    return None  # suppressed (*_Datenschutz) or absent


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--xml", required=True, help="folder of Quality-Report XML")
    ap.add_argument("--out", default=".", help="output folder for the two CSVs")
    a = ap.parse_args()
    out = Path(a.out)
    files = sorted(glob.glob(str(Path(a.xml) / "*-xml.xml")))
    print(f"{len(files)} candidate main reports")

    fr = open(out / "_agg_focus.csv", "w", newline="", encoding="utf-8")
    wr = csv.writer(fr); wr.writerow(["ik", "standort", "code_type", "code", "count"])
    fh = open(out / "_agg_hosp.csv", "w", newline="", encoding="utf-8")
    wh = csv.writer(fh); wh.writerow(["ik", "standort", "name"])
    nh = nr = 0
    for f in files:
        try:
            r = etree.parse(f).getroot()
        except Exception:
            continue
        if etree.QName(r).localname != "Qualitaetsbericht":
            continue
        ik, st, name = rf(r, "IK"), rf(r, "Standortnummer"), rf(r, "Name")
        wh.writerow([ik, st, name]); nh += 1
        for dept in r.iter("{*}Organisationseinheit_Fachabteilung"):
            for dx in dept.iter("{*}Hauptdiagnose"):
                code = ch(dx, "ICD_10")
                if code and code.startswith(ICD_PREFIX):
                    c = cnt(dx, "Fallzahl")
                    if c:
                        wr.writerow([ik, st, "ICD", code, c]); nr += 1
            for pr in dept.iter("{*}Prozedur"):
                code = ch(pr, "OPS_301")
                if code and code.startswith(OPS_PREFIX):
                    c = cnt(pr, "Anzahl")
                    if c:
                        wr.writerow([ik, st, "OPS", code, c]); nr += 1
    fr.close(); fh.close()
    print(f"wrote _agg_hosp.csv ({nh} hospitals) and _agg_focus.csv ({nr} rows)")


if __name__ == "__main__":
    main()
