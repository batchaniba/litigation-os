# Canonical document store

R2 (`litigation-documents`) holds the bytes. D1 (`litigation-portfolio`) is
the index. Repo-root `documents/` mirrors `/documents/<matter>/...` paths for
everything that is **public**. The 14-path owner denylist lives only under
`internal/private/documents/` (and in R2, hash-addressed).

## Visibility (owner rule, 2026-10-14)

- **Public (no auth):** every D1-registered document except the denylist.
  `GET /doc/<sha256>` and `GET /documents/<path>` stay open for those files.
- **Private (bearer / OAuth `read` or `write`):** the 14 paths in
  `internal/src/data/documents/private-documents.json` — twelve
  `/documents/matter-05/hope-discovery/HOPE_000*.pdf` (D1 versions) and two
  matter-12 card-authorization PDFs. Same bytes under another path (the
  aug31 CC-auth duplicate) are blocked by SHA-256. Anonymous callers get
  `404 not_found` so the file is not confirmed to exist.
- **Writes:** still require OAuth/`API_KEYS` scope `write` (`rw`). New
  uploads default public unless the path or hash matches the denylist.
- Do **not** put denylist bytes in `documents/` or `internal/public/`.

## Connect any MCP-capable model

URL: `https://litigation-doc-api.ss8sxswwkt.workers.dev/mcp`

Reads work without a token (minus the 14). Writes need OAuth or a bearer
token with `write` scope.

**ChatGPT:** custom connector / MCP app → that `/mcp` URL → OAuth. Consent
defaults to **read only**; existing ChatGPT/Claude grants keep their current
scope. Do not request `write` unless the owner ticks it.

**Claude (claude.ai / Claude Desktop / Claude Code):** same URL. Claude Code:

```bash
claude mcp add --transport http litigation-portfolio \
  https://litigation-doc-api.ss8sxswwkt.workers.dev/mcp
```

Add `--header "Authorization: Bearer <token>"` only when you need the
private 14 or write tools.

**Cursor:** Settings → MCP → Streamable HTTP → the `/mcp` URL.

### Example prompts

- “List active matters and the next clock on each.”
- “List documents for matter 24, then read the FAC text.”
- “Search documents for ‘Rule 12(b)(6)’ and open the UPS opposition.”
- “Fetch the PDF link for sha256 \<64 hex\>.”

Tools: `listMatters` / `list_matters`, `listDocuments` / `list_documents`,
`readDocumentText` / `get_document_text`, `searchDocuments` /
`search_documents` (D1 FTS5 when `documents_fts` exists, otherwise path
LIKE — FTS5 is the right index for docket strings and statute numbers;
Vectorize would add a second product without helping exact tokens),
`fetchDocument` / `get_document_pdf` / `get_document_link`. Write tools
stay behind `write` scope.

## Sync (idempotent, not destructive)

```bash
npm run documents:sync              # dry-run
npm run documents:sync -- --apply   # needs R2_* from ~/.config/r2/env
```

Uploads repo-only **public** PDFs to R2 (HEAD-skip if present), refreshes
the path index (denylist omitted), and extracts text sidecars when
`pdftotext` is installed. Never DELETE/DROP. A D1 reseed is a different,
destructive operation — do not run it as part of this sync.

## Deploy steps (owner)

1. `cd workers/doc-api && wrangler deploy`
2. `wrangler d1 execute litigation-portfolio --remote --file=schema.sql`
   (adds `documents_fts`; idempotent)
3. Do **not** reseed unless you intend to wipe assistant-registered D1
   rows. To register new public files without a reseed, run
   `documents:sync -- --apply` on the laptop.
4. Existing ChatGPT/Claude OAuth clients keep working. New consents
   default to read-only.

## Git LFS

Not recommended. GitHub’s free LFS quota is 1 GB of bandwidth a month;
Vercel builds would exhaust it. R2 is the serving store. This branch
tracks previously-scattered public PDFs so they are no longer at repo
root or under `internal/docs/`.
