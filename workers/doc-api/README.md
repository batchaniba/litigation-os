# doc-api — Cloudflare Worker + D1 for the litigation portfolio

Live at `https://litigation-doc-api.ss8sxswwkt.workers.dev`.
Reads R2 through the `DOCS` binding. No keys in this directory.

## Laptop apply (this branch does not push bytes)

Git cannot mint R2 objects or reseed production D1. After merge, on the machine that already has wrangler + `~/.config/r2/env`:

```bash
cd workers/doc-api
wrangler deploy
wrangler d1 execute litigation-portfolio --remote --command "ALTER TABLE clocks ADD COLUMN status TEXT"   # ignore duplicate-column
wrangler d1 execute litigation-portfolio --remote --file=schema.sql
node seed.mjs > seed.sql
wrangler d1 execute litigation-portfolio --remote --file=seed.sql
# then the existing documents:push so Sep 17 Meza objects + path index land in R2
```

Then fire the Vercel Deploy Hook so `/documents/:path*` rewrite is on the live SPA.

Do not paste R2 tokens into chat. Do not POST `/admin/reseed` without `RESEED_SECRET`.

## Who gets what

| Audience | What they get |
|---|---|
| ChatGPT / Grok / any third-party chat | This Worker URL. Zero credentials. |
| Cursor on the laptop | The Worker for reads. `~/.config/r2/env` only for writes (`documents:push`). |

## What this branch fixes in code

- `/documents/<path>` looks up `documents_by_path` (path is the identity). The old `documents.sha256` primary key collapsed slug + court-path aliases onto one row and made court paths 404 even when the hash object existed.
- `/upcoming` and folded `next_clock_*` ignore `satisfied` / `retired` / `cancelled` / `vacated` clocks. Git already marked Matter 30 Sep 16 and Matter 26 Rule 15 satisfied; D1 was still serving them.
- Missing path is `404 {error:not_found, path}` — not a bare `{error:not_found}` that is indistinguishable from an unknown route.

## Not done in git

- Uploading Meza Sep 17 PDFs to R2
- Writing `index/path-to-sha256.json` into the bucket
- The Vercel Deploy Hook
- Physical Sep 17 mailing in Matter 32
