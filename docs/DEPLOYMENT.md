# Deployment

The deployable site is the static folder **`public/`**. It contains the built
`public/index.html`, so any static host can serve it.

## Option A - Render Static Site (recommended)

Use this when you want the service managed directly in the Render dashboard instead of via a
Blueprint.

1. Render -> **New -> Static Site**.
2. Connect `BENEDICT9845/kodier-bench`.
3. Settings:
   - **Branch:** `main`
   - **Build command:** `python3 build.py`
   - **Publish directory:** `public`
4. Deploy. Every push to `main` now auto-deploys.

`render.yaml` is included only as an optional Blueprint convenience. Static sites are free on
Render, but the Blueprint should not include a `plan: free` field.

If Render ever has trouble with Python in the static build environment, leave the build command
empty or use a no-op command and rely on the committed `public/index.html`.

## Option B - Netlify, connected to this repo

1. Netlify -> **Add new site -> Import an existing project** -> GitHub -> pick `kodier-bench`.
2. Build settings:
   - **Build command:** leave empty because `public/index.html` is committed.
     Optional: use `python3 build.py` to rebuild from `data/` on deploy.
   - **Publish directory:** `public`
3. Deploy. Every push to the default branch now auto-deploys.
4. Rename the site, for example `kodierbench.netlify.app`.

## Option C - Netlify Drop

Drag the **`public/`** folder onto `app.netlify.com/drop`. This gives an instant URL, but updates
are manual.

## Option D - Render Blueprint

`render.yaml` is included. Render -> **New -> Blueprint** -> connect `kodier-bench` -> it reads
`render.yaml` as a static site and publishes `./public`.

## Updating a live site

```bash
# after changing data or the app template:
python3 build.py
git add data public
git commit -m "data: refresh"
git push
```

## Access control

- Cloudflare Access or Render/Netlify account-level controls can gate access during the
  licence-caution phase.
- Keep the deployment internal until the InEK reuse terms in `NOTICE.md` are confirmed.

## Notes

- No server, database, or secrets are required.
- Everything runs client-side; user inputs never leave the browser.
