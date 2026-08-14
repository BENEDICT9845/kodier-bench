# Pipeline — how to recreate the data

Regenerates the tracked `data/national.json` and `data/peer.json` from the original
sources. Raw files are never committed; see `../docs/DATA_SOURCES.md` for exactly where
to get each one.

```bash
pip install -r requirements.txt
```

## 1. National reference → `data/national.json`
Put these two files in `pipeline/raw/inek/`:
- the **InEK DatenBrowser** export (xlsx with a `DRG-Verteilung` sheet) — `datenbrowser.inek.org`, free account, export the default §21 dataset.
- the **InEK Fallpauschalen-Katalog** (xlsx with a `Hauptabteilungen` sheet) — `g-drg.de`.

```bash
python build_national.py --raw pipeline/raw/inek --out data/national.json
```

## 2. Per-hospital peer distribution → `data/peer.json`
The G-BA XML is ~1.7 GB, so **run the aggregation where the XML lives** (your machine),
then only the small CSV travels.

```bash
# get the XML: qb-datenportal.g-ba.de → order form → credentials → download & unzip
python aggregate_qb.py --xml /path/to/xml_2024 --out .     # -> _agg_focus.csv, _agg_hosp.csv
python build_peer.py --focus _agg_focus.csv --out data/peer.json
```
`aggregate_qb.py` keeps a cardiology focus set (ICD chapter I + cardiac OPS prefixes) and
drops source-suppressed (`<4`) counts. Widen the focus list at the top of that file to add
specialties.

## 3. Build the app
```bash
python ../build.py        # data/*.json + template -> public/index.html
```

## Notes
- Deterministic: same inputs → same JSON.
- To move to a new data year, swap the source files and re-run; update the `vintage`
  strings in the two build scripts.
