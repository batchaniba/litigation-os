# Document store

`internal/public/documents/` is ~660 MB of filed PDFs (and growing). Nothing
is pruned. Vite's `publicDir` copies that tree wholesale into `dist/`, so
every clone, every default CI checkout, and every production build used to
move the whole library — even on the ~4 commits/day that only touch matter
JSON.

Git LFS does not fix this. GitHub's free LFS quota is 1 GB of bandwidth a
month; one Vercel build plus a couple of CI runs would exhaust it, and the
blobs would still download whenever a job needed a working tree.

## What stays in git

| File | Role |
|---|---|
| `internal/src/data/documents/registry.json` | Editorial catalog: path → label + owning matter |
| `internal/src/data/documents/manifest.json` | Physical inventory: path → size + sha256 |

The PDFs themselves stay in git **for now** so local `npm run dev`, Vercel,
and GitHub Pages keep serving `/documents/...` with no extra account. What
changed is that **most CI no longer checks them out or copies them**.

## Two CI paths

**Data job** (`.github/workflows/ci.yml` → `build-and-validate`):

- Sparse-checkout excludes `internal/public/documents/`.
- `PORTFOLIO_SKIP_DISK_DOCS=1` — `validate-portfolio` treats a path as real
  when it is in the committed manifest (and the registry).
- `VITE_COPY_DOCUMENTS=0` — Vite copies `internal/public/` *except*
  `documents/` (logos, short-link slugs, `robots.txt`).
- Still runs lint, typecheck, the JS bundle, citations gate, and tests.

**Documents job** (`.github/workflows/documents.yml`):

- Full checkout, path-filtered. Runs when the PDF tree, the manifest, or
  the inventory scripts change — not on ordinary matter-data commits.
- Hashes every file, checks `%PDF` magic, rejects byte-identical duplicates
  inside one matter folder, warns on orphans.
- No `npm ci`; `validate-portfolio.mjs` is Node builtins + local modules.

Production deploy (Vercel and `.github/workflows/deploy-gh-pages.yml`) still
checks out the tree and copies it into `dist/`. That cost is paid once per
`main` push, not on every branch push.

## Local workflow

Default `npm run validate` still reads the files on disk. After you drop or
replace a PDF:

```bash
npm run sync:registry    # path → label
npm run sync:manifest    # path → size + sha256
npm run validate
```

`npm run sync:all` now includes the manifest. `npm run build` locally is
unchanged (documents still land in `dist/`).

To exercise the CI data path:

```bash
PORTFOLIO_SKIP_DISK_DOCS=1 VITE_COPY_DOCUMENTS=0 npm run validate
VITE_COPY_DOCUMENTS=0 npm run build
```

## Phase 2 — get the binaries out of the default clone

CI is no longer the growth curve. **Vercel and a full `git clone` still pay
660 MB**, and that number only goes up. The remaining move:

1. Host the tree outside this repo — a sibling repository, or one GitHub
   Release tarball (`tar -C internal/public -cf documents.tar documents`).
2. Gitignore `internal/public/documents/**` except folder READMEs / `.gitkeep`.
3. Add `npm run documents:pull` that unpacks the archive into the same path
   so `/documents/...` URLs do not change.
4. Point Vercel and GH Pages build commands at pull-then-`vite build`.
5. Keep the manifest in this repo. Data CI stays sparse. The documents job
   checks out the store, not this tree.

Do **not** rewrite history until every clone has switched. `git filter-repo`
to drop the PDFs is a coordinated cutover, not a first step.

A cheaper follow-up inside this repo: stop committing the ~47 MB of
short-link slug copies under `internal/public/*.pdf`. Point Vercel redirects
at the `/documents/...` source and delete the duplicates.

## Why not the other options

| Option | Why it loses |
|---|---|
| Git LFS | Bandwidth quota; every deploy still downloads every blob |
| `fetch-depth: 1` alone | Helps history, not the current tree (already in use) |
| Leaving PDFs in `publicDir` and deleting after copy | Still copies 660 MB |
| Serving from a random CDN with new URLs | Breaks matter links, short-links, and the registry id |
