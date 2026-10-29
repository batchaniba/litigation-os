# Cloudflare Pages host — Phase 1

Phase 1 puts the **in-repo scaffolding** next to the existing Vercel host.
It does **not** cut over DNS, delete Vercel config, retarget
`vercel-deploy-cron`, or drop static `/{slug}.pdf` copies.

**Production stays on Vercel** until Phase 3. The Pages project is a
parallel `*.pages.dev` smoke host.

## Locked project name

Keep the Vercel project slug on Cloudflare’s analogue of `*.vercel.app`:

| | |
|---|---|
| Pages **project name** | `interactive-litigation-portfolio` |
| Target host | `https://interactive-litigation-portfolio.pages.dev` |
| Preview (per deploy) | `https://<hash>.interactive-litigation-portfolio.pages.dev` |

Create the dashboard project with **exactly** that name. A different slug
produces a different `*.pages.dev` host. Wrangler’s `name` in the repo-root
`wrangler.toml` matches it.

Cloud-agent runs typically cannot create the Cloudflare dashboard project.
That step is operator-side; everything else in this file is already in the
repo.

## Build contract

Verified in-repo (not assumed):

| Setting | Value | Evidence |
|---|---|---|
| Node | **22** (`22.23.4`) | `package.json` `engines.node` is `>=22.23.4`. Pages v3 default is 22.16.0, which is below that floor. `.nvmrc` pins `22.23.4` to match engines. Pages also reads `NODE_VERSION` ([language support](https://developers.cloudflare.com/pages/configuration/language-support-and-tools/)). |
| Install | `npm ci` | Set dashboard env `SKIP_DEPENDENCY_INSTALL=1` so Pages does **not** also run `npm install` ([same page](https://developers.cloudflare.com/pages/configuration/language-support-and-tools/)). |
| Build command | `npm ci && npm run build` | `package.json` `build` is `vite build`. `prebuild` runs `sync:derived` (includes `sync:short-links`). |
| Output directory | `dist` | Vite default. `vite.config.js` has **no** `build.outDir`. Matches the Pages “React (Vite)” preset ([build configuration](https://developers.cloudflare.com/pages/configuration/build-configuration/)). |
| Root directory | `/` (repository root) | SPA lives at the repo root, not a monorepo subfolder. |
| Framework preset | React (Vite) | Build command `npm run build`, output `dist`. |
| `base` | `/` | Leave `GITHUB_PAGES` unset. Vercel and Pages both serve from the domain root. |
| Do not copy the PDF library | `VITE_COPY_DOCUMENTS=0` and `PORTFOLIO_SKIP_DISK_DOCS=1` | Same as Vercel. Bytes come from the Worker via `/documents/*`. Phone-tap slugs stay as `internal/public/{slug}.pdf` in the artifact. `sync:short-links` also treats `CF_PAGES=1` as skip-disk so a forgotten dashboard flag does not fail `prebuild`. |

`wrangler.toml` at the repo root records `name`,
`pages_build_output_dir = "./dist"`, and the top-level `[vars]` table.
Git-integration **build command** is a dashboard field; Pages does not take
it from Wrangler
([Wrangler configuration](https://developers.cloudflare.com/pages/functions/wrangler-configuration/)).
**Env vars are NOT dashboard fields while `wrangler.toml` exists** — the
dashboard refuses plain variables ("managed through wrangler.toml"), so the
four contract vars live in `[vars]`, which applies to both Production and
Preview.

System env Pages injects (do not set by hand): `CI`, `CF_PAGES=1`,
`CF_PAGES_COMMIT_SHA`, `CF_PAGES_BRANCH`, `CF_PAGES_URL`. `vite.config.js`
writes `dist/version.json` from `CF_PAGES_COMMIT_SHA` / `CF_PAGES_BRANCH`
when those are present. `postinstall` skips `sync:derived` when `CF_PAGES`
is set because `prebuild` runs it.

## Operator: create and connect the project

1. Cloudflare dashboard → **Workers & Pages** → **Create** → **Pages** →
   **Import an existing Git repository** (or **Direct Upload** for a one-shot
   smoke — see below).
2. Project name: **`interactive-litigation-portfolio`**.
3. Production branch: `main`.
4. Build settings:

   | Field | Value |
   |---|---|
   | Framework preset | React (Vite) — or None, with the values below |
   | Build command | `npm ci && npm run build` |
   | Build output directory | `dist` |
   | Root directory | *(empty / repository root)* |
   | Build system | v3 |

5. **Environment variables** (Production **and** Preview — via `wrangler.toml` `[vars]`, not the dashboard):

   | Name | Value |
   |---|---|
   | `SKIP_DEPENDENCY_INSTALL` | `1` |
   | `VITE_COPY_DOCUMENTS` | `0` |
   | `PORTFOLIO_SKIP_DISK_DOCS` | `1` *(same as Vercel — `prebuild` / `sync:short-links` checks catalog sources against the committed manifest. `CF_PAGES=1` also triggers this.)* |
   | `NODE_VERSION` | `22.23.4` *(belt and suspenders with `.nvmrc`)* |

6. **Throttle builds before the first flood.** Git integration deploys on
   every push by default ([git integration](https://developers.cloudflare.com/pages/configuration/git-integration/)).
   That is the Vercel every-push cost regression. Phase 1 must **not**
   recreate it:
   - Project → **Build** → **Branch control** → turn **off**
     **Enable automatic production branch deployments**.
   - Set **Preview branch** to **None** (disable automatic branch
     deployments).
   - Trigger **one** deployment by hand for smoke (dashboard **Retry
     deployment**, or Direct Upload).
7. Do **not** attach a custom domain. Do **not** change DNS. Do **not**
   retarget `internal/workers/vercel-deploy-cron/` — it still POSTs the
   Vercel Deploy Hook.

### Direct Upload alternative (no Git auto-builds)

If the dashboard Git connector cannot be used from this environment:

```bash
npm ci
VITE_COPY_DOCUMENTS=0 npm run build
npx wrangler pages deploy dist --project-name=interactive-litigation-portfolio
```

Requires Wrangler authenticated to the same account. Direct Upload cannot
later switch to Git integration on the same project ([git
integration](https://developers.cloudflare.com/pages/configuration/git-integration/)
— “You cannot switch to Direct Upload later” is the other direction; pick
Git **or** Direct Upload at creation). Prefer Git + branch control off so
a later Phase 3 cron can `wrangler pages deploy` without fighting
push-triggered builds.

## What the repo already generates

`npm run sync:short-links` (catalog: `internal/public/short-links.json`)
writes **both** hosts. Do not hand-edit either output.

| File | Host | Role |
|---|---|---|
| `vercel.json` | Vercel (production) | Short-link 302s, `Content-Disposition`, `/documents/:path*` rewrite to the Worker, SPA rewrite, `git.deploymentEnabled: false` |
| `internal/public/_redirects` | Pages | Short-link 302s + SPA fallback `/* /index.html 200`. Copied into `dist/` by Vite. |
| `internal/public/_headers` | Pages | `Content-Disposition` on `/{slug}.pdf`; `X-Robots-Tag: noindex` on `*.pages.dev` |
| `internal/public/_routes.json` | Pages | Functions run only on `/documents/*` |
| `internal/public/{slug}.pdf` | both | Static phone-tap copies (unchanged) |
| `functions/documents/[[path]].js` | Pages | Reverse-proxy `/documents/*` → doc-api Worker |

`npm run sync:short-links -- --check` covers Vercel **and** the Pages
files. `npm run validate` runs that check.

### Short-links (`_redirects`)

[Pages redirects](https://developers.cloudflare.com/pages/configuration/redirects/):
plain-text `_redirects` in the static asset directory; static rules before
dynamic; default 302. Generated rules look like:

```
/fedex-consent /fedex-consent.pdf 302
/fedex-consent/ /fedex-consent.pdf 302
…
/* /index.html 200
```

The splat is the analogue of Vercel’s `{ source: "/(.*)", destination: "/index.html" }`.
Pages **also** treats a missing top-level `404.html` as SPA routing to `/`
([Serving Pages](https://developers.cloudflare.com/pages/configuration/serving-pages/)).
Do **not** add a `404.html`.

### `/documents/:path*` — Function, not `_redirects`

Same docs page: **“Proxying will only support relative URLs on your site.
You cannot proxy external domains.”** A `_redirects` line of the form

```
/documents/* https://litigation-doc-api.ss8sxswwkt.workers.dev/documents/:splat 200
```

is **not valid** on Pages (it would 302-redirect, which would change the
browser URL — not today’s Vercel rewrite).

The analogue is a Pages Function
([file-based routing](https://developers.cloudflare.com/pages/functions/routing/)):

- `functions/documents/[[path]].js` — `onRequest` `fetch()`es
  `https://litigation-doc-api.ss8sxswwkt.workers.dev` with the incoming path
  and query (encoding preserved).
- `internal/public/_routes.json` — `{ "version": 1, "include": ["/documents/*"] }`
  so only those URLs invoke Functions (unlimited static requests otherwise).

`_redirects` are **not** applied to Function-handled requests (redirects
docs, caution). That keeps `/documents/*` off the SPA splat.

Do not add a Worker route on `pages.dev` for this; `pages.dev` is not a
zone we attach Worker routes to. The Function is the documented Pages
mechanism.

### Static slug PDFs

Unchanged. `internal/public/{slug}.pdf` is part of the Vite public tree and
lands in `dist/{slug}.pdf`, same as Vercel. `_headers` sets
`Content-Disposition` so Save As keeps the long portfolio filename.
R2-only short-links (dropping these copies) is a later phase.

## `*.pages.dev` smoke checklist

After the first deploy, against
`https://interactive-litigation-portfolio.pages.dev` (or the hashed preview
URL):

1. **Home** — `GET /` returns `200` and the SPA shell (`index.html`).
2. **Matter route** — `GET /` plus a client route such as a matter hash/path
   the SPA actually uses (hard-refresh a matter URL). Must not 404; SPA
   fallback should serve `index.html`.
3. **Short-link PDF** — `GET /fedex-consent` 302s to `/fedex-consent.pdf`;
   `GET /fedex-consent.pdf` is `application/pdf` (not HTML) with
   `Content-Disposition` containing the long filename.
4. **`/documents/...`** — pick a Worker path that already 200s on
   `https://litigation-doc-api.ss8sxswwkt.workers.dev/documents/...` (Serrato
   FAC or a current mailing packet). Same path on the Pages host must 200
   as a PDF **without** changing the browser origin to `workers.dev`.
5. **`/version.json`** — `200`, JSON with `sha` matching the deployed
   commit (`CF_PAGES_COMMIT_SHA`) and a `builtAt` timestamp.

If a short-link PDF comes back as HTML, the `/* /index.html 200` splat is
winning over the static asset — file that as a Pages behavior bug against
the smoke host; built-in SPA routing (no `404.html`) still covers matter
routes. Do not “fix” it by adding `404.html`.

## Deploy cadence (Phase 1 vs later)

| Phase | Production | Pages `*.pages.dev` | `vercel-deploy-cron` |
|---|---|---|---|
| **1 (this)** | Vercel | Manual / throttled smoke only | Unchanged (Vercel Deploy Hook) |
| 2 | Vercel | Still smoke; drop `@vercel/analytics` / Speed Insights from the bundle | Unchanged |
| 3 | Pages + custom domain | Same project | Retarget to Pages (`wrangler pages deploy` or a Deploy Hook analogue) |
| later | Pages | — | Delete Vercel project; optional R2-only short-links |

Phase 1 explicitly does **not** retarget the cron. Do not enable
build-on-every-push on Pages.

Later (when Pages *is* production): keep automatic production deployments
**off** and drive releases from a scheduled job, the same way
`git.deploymentEnabled: false` plus the cron does on Vercel today.
Commit-message skip (`[skip ci]` / Pages skip) is a backup, not the
control plane.

## Out of scope (do not do in this phase)

- DNS / custom domain
- Removing `@vercel/analytics` / `@vercel/speed-insights` (Phase 2)
- Pointing `vercel-deploy-cron` at Pages
- Deleting `vercel.json` or the Vercel project
- Dropping static slug PDFs in favor of R2-only short-links
- Adding `.github/workflows/`

## Docs fetched for this phase (2026-09-21)

- [Redirects](https://developers.cloudflare.com/pages/configuration/redirects/)
- [Headers](https://developers.cloudflare.com/pages/configuration/headers/)
- [Functions routing / `_routes.json`](https://developers.cloudflare.com/pages/functions/routing/)
- [Serving Pages (SPA default)](https://developers.cloudflare.com/pages/configuration/serving-pages/)
- [Build configuration](https://developers.cloudflare.com/pages/configuration/build-configuration/)
- [Language support (Node / `SKIP_DEPENDENCY_INSTALL`)](https://developers.cloudflare.com/pages/configuration/language-support-and-tools/)
- [Git integration (disable automatic deployments)](https://developers.cloudflare.com/pages/configuration/git-integration/)
- [Wrangler configuration for Pages](https://developers.cloudflare.com/pages/functions/wrangler-configuration/)
- [Deploy a React site](https://developers.cloudflare.com/pages/framework-guides/deploy-a-react-site/)
