# Architecture

Deliberately simple: an **annual batch pipeline** produces small derived-aggregate JSON,
and a **single static HTML app** renders it entirely in the browser. No backend, no DB,
no PHI.

```
 SOURCES (raw, not committed)              PIPELINE (python)                 TRACKED            APP
 ─────────────────────────────            ──────────────────               ─────────          ─────
 InEK DatenBrowser export  ┐
                           ├─ build_national.py ───────────────────────▶  data/national.json ┐
 InEK Fallpauschalen-Katalog┘                                                                 │
                                                                                              ├─ build.py ─▶ public/index.html
 G-BA Quality-Report XML ── aggregate_qb.py ─▶ _agg_focus.csv ─ build_peer.py ─▶ data/peer.json┘         (single self-contained file)
   (~1.7 GB, run in place)                                                                                        │
                                                                                                                 ▼
                                                                                                    static host (Netlify/Render)
                                                                                                    → runs in the user's browser
```

## Why this shape
- **Data changes ~yearly**, so we pre-bake aggregates instead of running a live service.
- **Aggregates are tiny** (~200 KB total) → the whole app is one file → trivial to host,
  impossible to leak patient data (there isn't any), scales for free.
- **Reproducible**: `data/*.json` is regenerated from documented sources by `pipeline/`.
  The app is regenerated from `src/index.template.html` + `data/*.json` by `build.py`.

## The two data layers
| Layer | Built by | Granularity |
|---|---|---|
| National reference (complexity, tiers, CMI, CC/OPS frequencies) | `build_national.py` | national aggregates + the user's own entered number |
| Per-hospital peer distribution (volumes) | `aggregate_qb.py` + `build_peer.py` | true across-hospital distribution (high-volume codes) |

## App internals
`src/index.template.html` is the source; two tabs, each an isolated IIFE reading its own
embedded JSON (`__NATIONAL__`, `__PEER__` placeholders filled by `build.py`). Charts are
hand-rendered SVG on a fixed, accessibility-checked palette. No runtime dependencies.
