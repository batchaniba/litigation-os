# Document library

PDF bytes live in Cloudflare R2. This folder is gitignored on `main`
(historical prefix). The git-tracked public working set is repo-root
`documents/`. `origin/documents` is a cold backup that still uses this
prefix. A replacement at the same path is a new object; the Worker path
index moves `/documents/...` to it. Private denylist PDFs must never
land here.

```bash
npm run documents:pull   # after clone (R2 if R2_* is set, else the git branch)
npm run documents:push   # after adding or replacing a filing
```

The pre-commit hook runs `documents:push` when `manifest.json` changes.
Matter JSON still lists paths under `/documents/...`. Vercel rewrites those
URLs to the Worker (`litigation-doc-api`). Phone-tap slugs stay as copies
on `main` until that origin returns HTTP 200.
