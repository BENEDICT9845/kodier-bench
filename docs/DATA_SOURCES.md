# Data sources — provenance, access & vintage

Every number in KodierBench is a **derived aggregate** of official, published data.
No patient-level data is used. Raw source files are **not** committed (licence + size);
this document is how you obtain them and `pipeline/` rebuilds the tracked `data/*.json`.

| # | Source | What we derive | Access | Vintage | Licence |
|---|---|---|---|---|---|
| 1 | **InEK DatenBrowser** (§21 KHEntgG) — `datenbrowser.inek.org` | national cases per DRG (tier split), secondary-dx (CC) & procedure frequencies, cohort mix | **Free account** → export the default dataset (xlsx with sheets DRG-Verteilung, Nebendiagnosen, Prozeduren, Krankenhausverteilung) | §21 data Jan–Dec 2025 | ⚠️ reuse terms **unconfirmed** — see NOTICE.md before public/commercial use |
| 2 | **InEK Fallpauschalen-Katalog** — `g-drg.de` | per-DRG cost weight (Bewertungsrelation) + mean LOS | file download (aG-DRG-Katalog for the system year) | aG-DRG 2026 | official price annex; confirm terms |
| 3 | **G-BA structured Quality Reports** — `qb-datenportal.g-ba.de` | per-hospital ICD/OPS case volumes (Teil B) → peer distribution | **Order form → credentials → bulk XML** (declare publication; free) | Berichtsjahr 2024 | ANB — free, **derived only, no raw re-host**, attribution required (§136b) |
| 4 | **BfArM** — ICD-10-GM & OPS | code labels / version reference | file download | 2024/2026 | reuse permitted |
| (5) | **Destatis** GENESIS 23141 (DL-DE-2.0) | permissive fallback / cross-check for CC & procedure frequencies | GENESIS API (free account) | ~2023 | Datenlizenz Deutschland 2.0 (commercial OK) |

## Key facts baked into the pipeline
- **DRG-Statistik = EVAS 23141** (not 23131 — that's the main-diagnosis statistic).
- Free GENESIS 23141 exposes **only** Nebendiagnosen (ICD) + Prozeduren (OPS) — **no DRG-code table**; hence per-DRG case counts come from InEK (source #1), cost weights from #2.
- G-BA per-hospital data: main reports are the `*-xml.xml` files (root `<Qualitaetsbericht>`); `*-das.xml` / `*-IQTIG_*.xml` are supplements. **~66% of per-hospital counts are suppressed** (`<4` cases masked) — fine for high-volume conditions, so peer benchmarking targets those.
- Per-hospital data gives **volumes + structure**, not per-hospital CMI/tier-split (those stay the hospital's own input vs the national reference).

## Rebuild the tracked aggregates
See `pipeline/README.md`. In short: put #1 and #2 in `pipeline/raw/inek/` → `build_national.py`;
run `aggregate_qb.py` where the #3 XML lives → `build_peer.py`.
