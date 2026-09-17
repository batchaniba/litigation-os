# Document library

PDF bytes live on the `documents` branch so clones and Vercel checkouts of
`main` stay small. This folder is gitignored on `main`.

```bash
npm run documents:pull   # after clone
npm run documents:push   # after adding or replacing a filing
```

The pre-commit hook runs `documents:push` when `manifest.json` changes.
Matter JSON still lists paths under `/documents/...`; Vercel rewrites those
URLs to the Cloudflare Worker path map. Phone-tap slugs stay as copies on
`main` until that origin returns HTTP 200.
