# KodierBench

A free, no-PHI benchmarking tool for German hospital DRG coding. It turns official
national data into an instant reference: for any DRG, how does our coded complexity
compare to the national norm — and how do our case volumes rank against every other
hospital?

**Status:** evaluation prototype (v1). Real German data, derived aggregates only,
runs entirely in the browser. Not affiliated with any of the data-source institutions.

---

## What's in the box

| Tab | What it shows | Data |
|---|---|---|
| **DRG Complexity** | All ~577 DRG groups: national severity-tier split, per-tier cost weights, average coded complexity (mean cost weight) vs the national CMI, LOS, top comorbidities/procedures | InEK §21 (Datenjahr 2025) + aG-DRG-Katalog 2026 |
| **Peer Volume** | 7 cardiology conditions/procedures: your annual volume → percentile among all German hospitals, with the real distribution | G-BA Quality Reports (Berichtsjahr 2024, 2,220 hospitals) |

The app is **one self-contained static HTML file** (`public/index.html`). No backend,
no database, no patient data. Everything a user types stays in their browser.

---

## Repo layout

```
kodierbench/
├── public/index.html          # ← the deployable (built; this is what you host)
├── src/index.template.html     # app source (data replaced by __NATIONAL__ / __PEER__ placeholders)
├── data/
│   ├── national.json           # derived national reference (tracked source of truth)
│   └── peer.json               # derived per-hospital peer distribution (tracked)
├── build.py                    # data/*.json + template  ->  public/index.html
├── pipeline/                   # reproduce data/*.json from the original sources
│   ├── build_national.py       # InEK export + Katalog        -> data/national.json
│   ├── aggregate_qb.py         # G-BA Quality-Report XML       -> _agg_*.csv  (run where the XML is)
│   ├── build_peer.py           # _agg_focus.csv                -> data/peer.json
│   └── requirements.txt
├── docs/
│   ├── DATA_SOURCES.md         # every source: URL, access, licence, vintage
│   ├── DEPLOYMENT.md           # Netlify / Render, and how to update
│   └── ARCHITECTURE.md         # how it fits together
├── netlify.toml / render.yaml  # deploy-from-repo config
├── NOTICE.md                   # attribution + data-use terms
└── .gitignore                  # raw data is never committed (licence + size)
```

**What is and isn't tracked:** the *derived aggregates* (`data/*.json`) and the built app
are tracked. The **raw source files** (InEK xlsx exports, the 1.7 GB of G-BA XML) are **not**
committed — both for licence reasons and size. `docs/DATA_SOURCES.md` says exactly where to
get them and `pipeline/` rebuilds the aggregates from them.

---

## Quick start

```bash
# 1. build the app from the tracked data (no source files needed)
python3 build.py            # -> public/index.html

# 2. preview locally
python3 -m http.server -d public 8000   # open http://localhost:8000
```

Deploy: see **docs/DEPLOYMENT.md** (drag `public/` to Netlify, or connect this repo to
Netlify/Render for auto-deploy on every push).

## Updating the data (new year / more conditions)

1. Get the source files (see **docs/DATA_SOURCES.md**).
2. Regenerate the aggregates:
   ```bash
   pip install -r pipeline/requirements.txt
   python3 pipeline/build_national.py --raw pipeline/raw/inek
   python3 pipeline/aggregate_qb.py --xml /path/to/xml_YYYY --out .
   python3 pipeline/build_peer.py --focus _agg_focus.csv
   ```
3. `python3 build.py` → commit `data/*.json` + `public/index.html` → push. Auto-deploys.

---

## Data & privacy

No patient-level data is used or stored anywhere. All figures are aggregated statistics
published by official bodies; the tool only ever shows *derived aggregates*. See
**NOTICE.md** for attribution and the data-use terms that apply before public/commercial use.
