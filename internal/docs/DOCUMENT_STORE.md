# Document store

Filed PDFs live in Cloudflare R2. `main` keeps the catalogs
(`registry.json`, `manifest.json`) and gitignores the bytes. Local
`internal/public/documents/` is filled with `npm run documents:pull`.
`/documents/...` URLs do not change: a redraft at the same path gets a
new sha256 object and the path index moves to it. Old objects stay
(upload-only, never deletes).

The `documents` git branch is a cold backup. Do not retire it until a
public Worker `GET /documents/...` returns HTTP 200 for the Serrato FAC
**and** a current mailing packet.

Git LFS does not fix this. GitHub's free LFS quota is 1 GB of bandwidth a
month; a handful of Vercel builds would exhaust it.

## What stays on main

| File | Role |
|---|---|
| `internal/src/data/documents/registry.json` | Editorial catalog: path → label + owning matter |
| `internal/src/data/documents/manifest.json` | Physical inventory: path → size + sha256 |
| `internal/public/documents/README.md` | How to pull / push the store |
| `internal/public/short-links.json` | Phone-tap slugs |
| `internal/public/{slug}.pdf` | Vercel-hosted tap copies — keep until R2 returns 200 |

## Working set — do not pull the whole room

A Cloud Agent or a laptop answering one matter should not extract ~660 MB.

```bash
npm run documents:pull -- --matter 24          # Serrato folder only
npm run documents:pull -- --matter 20,24       # two matters
npm run documents:pull -- --matter 24 --forms  # plus _form-library
npm run documents:pull -- --list               # folders on origin/documents
npm run documents:pull                         # whole tree (rare)
```

Sparse pulls **merge** into whatever is already on disk. They do not delete
other matter folders. `PORTFOLIO_SKIP_DISK_DOCS=1` (set automatically by
pre-push when no `matter-*` folders exist) treats the committed manifest as
the inventory, so validate does not need bytes.

Thin clone (history on the remote, current `main` tree only):

```bash
git clone --filter=blob:none <url>
```

Two worktrees, one repo — desk vs file room, never `checkout documents`
on the desk:

```bash
git worktree add ../portfolio-documents documents
```

## Day to day — adding or replacing a filing

Same desk as before. Drop the PDF in the matter folder, or overwrite the
file at the same path if you need to change it. `main` never takes the
library bytes. With `R2_*` in the environment, the hook publishes to
Cloudflare (new object + path-index update) so `/documents/matter-NN/...`
keeps working after a redraft.

```bash
# 1. Drop the PDF next to the others — or replace the existing file
#    internal/public/documents/matter-NN/Your Filing (Date).pdf

# 2. Point the matter record at it (path + optional filed / label override)
#    internal/src/data/matters/NN/documents.json  (split) or NN.json

# 3. Commit the matter JSON (do not git add -f the PDF).
git add internal/src/data/matters/NN/
git commit -m "Add Matter NN filing"
```

The pre-commit hook hashes *only the new/resized file* and, if
`manifest.json` changed, runs `npm run documents:push`. That command:

1. Updates `origin/documents` (cold backup).
2. PUTs each local PDF to R2 at `sha256/<first2>/<rest>.pdf` (HEAD-skip if present).
3. PUTs `index/path-to-sha256.json` so the Worker path still names the court file.

A same-path replacement is a new sha256. The index overwrites that path.
The previous object stays in the bucket.

If `R2_*` is missing (typical cloud agent), the git branch still updates
and the `r2-upload.yml` job on a `manifest.json` push to `main` does the
PUT + index. The hook prints a warning when it skips R2.

Vercel rewrites `/documents/:path*` to
`https://litigation-doc-api.ss8sxswwkt.workers.dev/documents/:path*`.
That returns PDF bytes only after the Worker is deployed with this path
route **and** the path index is in R2. Phone taps stay as
`internal/public/{slug}.pdf` copies until that origin returns HTTP 200
for the Serrato FAC and a current mailing packet. Do not point them at
GitHub Pages (404).

If the hook is skipped (`git commit --no-verify`):

```bash
npm run sync:manifest
npm run documents:push
git add internal/src/data/documents/manifest.json internal/src/data/documents/registry.json
```

In-place rewrite of an existing PDF that happens to keep the same byte size
is the one case the incremental write will not notice. `npm run sync:manifest -- --full` rehashes everything.

Do **not** put new PDFs anywhere else, and do not `git add -f` them onto
`main`.

## Where the checks run now

There is no GitHub Actions CI. The checks the old data job ran live in the
git hooks:

- **pre-commit** syncs registry + manifest when PDFs or the catalog are
  staged, hashes only new/resized files, checks `%PDF` magic, and pushes
  `origin/documents` when the inventory changes.
- **pre-push** runs `validate-portfolio`, which treats a document path as
  real when it is in the committed manifest and registry
  (`PORTFOLIO_SKIP_DISK_DOCS=1` is set automatically when the tree is not on
  disk). Vercel builds set the same flag plus `VITE_COPY_DOCUMENTS=0`.

## Publishing the library — R2 migration (2026-09-17)

Cloudflare R2 bucket `litigation-documents` now holds the store: **1,198 PDFs
from the `documents` branch → 1,139 unique objects / 793.6 MB** after
content-hash dedup. Every object was ETag-verified against source bytes at
migration time. GitHub Actions secrets for the bucket are live.

Key scheme (deterministic from `manifest.json` `sha256`):
`sha256/<first two hex chars>/<remaining hex>.pdf`.

Fetch one file without cloning the branch:

```bash
npm run docs:fetch <sha256>            # needs R2_ACCOUNT_ID / R2_ACCESS_KEY_ID /
                                       # R2_SECRET_ACCESS_KEY / R2_BUCKET
npm run docs:fetch <sha256> -- --out /tmp/doc.pdf
```

On the laptop those variables are exported from `~/.config/r2/env` (mode 600).
Shells on that machine source it. Cloud agents do not have that file unless
the environment image does — they read `R2_*` from the process environment
or they cannot fetch. GitHub Actions secrets hold the same values for
`r2-upload.yml` and are workflow-only; an agent cannot read them back.
Never paste keys into chat, files, or memory.

The helper re-hashes the bytes client-side and refuses to write on mismatch.
`origin/documents` is a cold backup. Incremental upload is
`.github/workflows/r2-upload.yml` (`workflow_dispatch`, a `documents`
branch push, or a `manifest.json` push to `main`) plus `documents:push`
when `R2_*` is set. Upload-only; never deletes. Do not retire the branch
until a public `GET /documents/...` has returned 200 for the Serrato FAC
and a current mailing packet.

GitHub Pages was the public origin for `/documents/*`. The Actions workflow
is gone and the Pages host now 404s. **Phone taps do not use it.** They stay
as slug copies on Vercel until the Worker path origin returns HTTP 200.
Then `/{slug}` can rewrite to encoded `/documents/...` and the copies leave
`main`.

## After clone

```bash
npm install
npm run documents:pull -- --matter 24   # or omit flags for the whole tree
npm run dev
```

`prepare` / `npm ci` do **not** pull. Vercel builds must stay off the 660 MB tree.

## History

Removing the files from the `main` tree makes **shallow** clones and Vercel
checkouts small. A full clone of `main` still contains the historical blobs
until a coordinated `git filter-repo`. Do not rewrite history until every
clone has switched to `documents:pull`.

## Why not the other options

| Option | Why it loses |
|---|---|
| Git LFS | Bandwidth quota; every deploy still downloads every blob |
| `fetch-depth: 1` alone | Helps history, not the current tree |
| Leaving PDFs in `publicDir` and deleting after copy | Still copies 660 MB |
| Serving from a random CDN with new URLs | Breaks matter links, short-links, and the registry id |
