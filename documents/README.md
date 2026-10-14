# Public document library

Canonical on-disk copies of **public** litigation PDFs. Paths here mirror
D1/R2 `/documents/<matter>/...`. Bytes are served from Cloudflare R2;
this folder is the git-tracked working set for files that used to sit at
repo root, under `internal/docs/`, and similar.

Private denylist PDFs (HOPE_000 discovery + two matter-12 card forms) do
**not** belong here. See `internal/private/documents/` and
`internal/docs/CANONICAL_DOCUMENT_STORE.md`.

```bash
npm run documents:pull              # fill / refresh from R2 or origin/documents
npm run documents:sync              # dry-run R2/D1 register
npm run documents:sync -- --apply   # CI (cloudflare-deploy.yml) or laptop, needs R2_*
```

Phone-only deploys: [CI_CLOUDFLARE_DEPLOY.md](../internal/docs/CI_CLOUDFLARE_DEPLOY.md).
