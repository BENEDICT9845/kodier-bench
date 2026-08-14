# Deployment

The site is the static folder **`public/`** (just `public/index.html`). Any static host works.

## Option A — Netlify, connected to this repo (recommended: auto-deploy on push)
1. Netlify → **Add new site → Import an existing project** → GitHub → pick `kodier-bench`.
2. Build settings:
   - **Build command:** *(leave empty)* — `public/index.html` is committed, no build needed.
     *(Optional: `python3 build.py` to rebuild from `data/` on deploy.)*
   - **Publish directory:** `public`
3. Deploy. Every `git push` to the default branch now auto-deploys.
4. Rename the site (Site settings → Change site name) → e.g. `kodierbench.netlify.app`.

## Option A′ — Netlify Drop (fastest, no repo needed)
Drag the **`public/`** folder onto `app.netlify.com/drop`. Instant URL. (Manual — re-drag to update.)

## Option B — Render (Blueprint)
`render.yaml` is included. Render → **New → Blueprint** → connect `kodier-bench` → it reads
`render.yaml` (static site, publish `./public`). Auto-deploys on push.

## Updating a live site
```bash
# after changing data or the app template:
python3 build.py                 # regenerates public/index.html
git add data public && git commit -m "data: refresh" && git push   # auto-deploys
```

## Access control (optional, for the licence-caution phase)
- **Cloudflare Access** (free) or Netlify password protection to gate by email while the
  InEK reuse terms are unconfirmed (see NOTICE.md). Open/public is fine once those are cleared.

## Notes
- No server, DB, or secrets — nothing to configure beyond the publish directory.
- Everything runs client-side; user inputs never leave the browser.
