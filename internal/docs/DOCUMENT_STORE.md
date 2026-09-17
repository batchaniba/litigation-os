# Document store

Filed PDFs live on the `documents` branch. `main` keeps the catalogs
(`registry.json`, `manifest.json`) and gitignores the bytes. Local
`internal/public/documents/` is filled with `npm run documents:pull`.
`/documents/...` URLs do not change.

Git LFS does not fix this. GitHub's free LFS quota is 1 GB of bandwidth a
month; a handful of Vercel builds would exhaust it.

## What stays on main

| File | Role |
|---|---|
| `internal/src/data/documents/registry.json` | Editorial catalog: path → label + owning matter |
| `internal/src/data/documents/manifest.json` | Physical inventory: path → size + sha256 |
| `internal/public/documents/README.md` | How to pull / push the store |
| `internal/public/short-links.json` | Phone-tap slugs → `/documents/...` sources |
| `internal/public/hope-name-stip.pdf` / `hope-name-motion.pdf` | Desk leftovers not yet on `documents` |

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
Nothing on `main` ever sees the bytes. Vercel rewrites `/documents/:path*` to
https://newanforbi.github.io/interactive-litigation-portfolio/documents/:path*
so the live site keeps the same paths without copying 660 MB on every
Vercel build.

Short-link taps (`/serrato-opp`, `/habeas-discharge`) **rewrite** to that
same origin, with each path segment encoded so court-style parentheses
never appear in a Vercel destination. Do not copy a second PDF to
`internal/public/{slug}.pdf`. Add the catalog row and run
`npm run sync:short-links`. Old `/{slug}.pdf` bookmarks follow the rewrite.

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

## Publishing the library

GitHub Pages was the public origin for `/documents/*` and was deployed by an
Actions workflow that no longer exists. The Pages site still serves whatever
was last deployed, and the Vercel rewrite still points at it, so every
existing link works. **New PDFs are not published** until a replacement
origin is in place. Short-link taps follow the same origin, so a packet that
is only on `documents` is on the desk immediately and on the public tap
when Pages/R2 catches up.

The intended replacement is a Cloudflare R2 bucket (free egress, no Actions)
fed by `documents:push` and fronted by the same Vercel rewrite; see the note
in `internal/docs/VERCEL_DEPLOYS.md`.

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
