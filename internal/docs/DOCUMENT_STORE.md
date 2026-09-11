# Document store

Filed PDFs live on the `documents` branch. `main` keeps the catalogs
(`registry.json`, `manifest.json`) and gitignores the bytes. Local
`internal/public/documents/` is filled with `npm run documents:pull`.
`/documents/...` URLs do not change.

Git LFS does not fix this. GitHub's free LFS quota is 1 GB of bandwidth a
month; one Vercel build plus a couple of CI runs would exhaust it.

## What stays on main

| File | Role |
|---|---|
| `internal/src/data/documents/registry.json` | Editorial catalog: path → label + owning matter |
| `internal/src/data/documents/manifest.json` | Physical inventory: path → size + sha256 |
| `internal/public/documents/README.md` | How to pull / push the store |

## Day to day — adding a filing

Same desk. The PDF still goes in the matter folder. Git ignores the bytes
on `main`; the hook pushes them to `origin/documents` when the inventory
changes.

```bash
# 1. Drop the PDF next to the others
#    internal/public/documents/matter-NN/Your Filing (Date).pdf

# 2. Point the matter record at it (path + optional filed / label override)
#    internal/src/data/matters/NN.json → documents[]

# 3. Commit the matter JSON (do not git add -f the PDF).
git add internal/src/data/matters/NN.json
git commit -m "Add Matter NN filing"
```

The pre-commit hook runs `npm run sync:all` (hashes *only the new/resized
file*), and if `manifest.json` changed it runs `npm run documents:push`.
Data CI never sees the bytes. GitHub Pages checks out `documents` before
`vite build`. Vercel rewrites `/documents/:path*` to
https://newanforbi.github.io/interactive-litigation-portfolio/documents/:path*
so the live site keeps the same paths without copying 660 MB on every
Vercel build.

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

## Two CI paths

Those workflows are currently **dispatch-only** (GitHub billing is blocking
runners). Restore `push` / `pull_request` in `.github/workflows/*.yml` when
Actions can start again. The jobs below stay as written.

**Data job** (`.github/workflows/ci.yml` → `build-and-validate`):

- Sparse-checkout excludes `internal/public/documents/` (and `main` no
  longer tracks those files).
- `PORTFOLIO_SKIP_DISK_DOCS=1` — `validate-portfolio` treats a path as real
  when it is in the committed manifest (and the registry).
- `VITE_COPY_DOCUMENTS=0` — Vite copies `internal/public/` *except*
  `documents/`.
- Still runs lint, typecheck, the JS bundle, citations gate, and tests.

**Documents job** (`.github/workflows/documents.yml`):

- Checks out this ref for scripts, then `ref: documents` for the PDF tree.
- Hashes every file, checks `%PDF` magic, rejects byte-identical duplicates
  inside one matter folder, warns on orphans.

**GitHub Pages** checks out `documents` into `internal/public/documents`
before `npm run build`, so `dist/documents/` is still the full library.

## After clone

```bash
npm install
npm run documents:pull
npm run dev
```

`prepare` / `npm ci` do **not** pull. Data CI must stay off the 660 MB tree.

## History

Removing the files from the `main` tree makes **shallow** clones and Vercel
checkouts small. A full clone of `main` still contains the historical blobs
until a coordinated `git filter-repo`. Do not rewrite history until every
clone has switched to `documents:pull`.

A cheaper follow-up: the ~47 MB of short-link slug copies under
`internal/public/*.pdf` can become redirects to the `/documents/...`
sources.

## Why not the other options

| Option | Why it loses |
|---|---|
| Git LFS | Bandwidth quota; every deploy still downloads every blob |
| `fetch-depth: 1` alone | Helps history, not the current tree |
| Leaving PDFs in `publicDir` and deleting after copy | Still copies 660 MB |
| Serving from a random CDN with new URLs | Breaks matter links, short-links, and the registry id |
