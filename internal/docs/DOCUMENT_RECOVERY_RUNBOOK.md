# Document-store recovery runbook

Use this when `manifest.json` knows a document path and SHA-256 but the R2
object may be absent. The recovery utility treats the committed manifest as
the expected inventory and the laptop working tree as a possible byte source.
It never deletes objects.

## 1. Load the laptop-only R2 environment

```bash
source ~/.config/r2/env
```

Do not copy these credentials into chat, issues, commits, or reports.

## 2. Audit before writing

```bash
npm run documents:recover
```

The command HEAD-checks every unique manifest SHA-256 in R2, then checks local
files only for hashes R2 lacks. A local candidate is usable only when its byte
size and SHA-256 both match the committed manifest. The checkpoint is written
to `.document-recovery/latest.json`, which is gitignored.

Key statuses:

- `present_r2`: the content-addressed object already exists; no upload needed.
- `recoverable_local`: R2 lacks the object and verified laptop bytes exist.
- `missing_local`: neither R2 nor the exact manifest paths supply bytes.
- `local_mismatch`: a path exists locally but its size or hash differs.
- `zero_byte`: deliberately not uploaded; the Worker refuses empty documents.

## 3. Recover in verified batches

One 25-object batch:

```bash
npm run documents:recover -- --apply
```

All currently recoverable objects, still checkpointed and verified in batches
of 25:

```bash
npm run documents:recover -- --apply --max-batches all
```

Useful controls:

```bash
npm run documents:recover -- --apply --batch-size 25 --max-batches 4
npm run documents:recover -- --concurrency 4
```

Every upload is re-HEADed and its R2 ETag must equal the local MD5. PDF text
sidecars are generated best-effort. After a successful apply run, the complete
`index/path-to-sha256.json` is refreshed from the committed manifest so every
alias path resolves to its content hash.

Interrupted runs are safe: rerun the same command. Already-present hashes are
detected and skipped.

## 4. Preserve the cold backup and verify catalogs

Do not run `documents:push` or `sync:manifest -- --full` from a sparse or
partial document tree: either operation can make an incomplete laptop folder
look authoritative. First finish recovery and restore the complete working
tree. Only when the report has no positive-byte `recoverable_local`,
`missing_local`, `local_mismatch`, or `upload_failed` objects:

```bash
npm run documents:pull
npm run sync:manifest -- --full
npm run documents:push
npm run validate
```

Review `.document-recovery/latest.json`. Any remaining `missing_local` hashes
must come from another archive. Resolve `local_mismatch` manually; never weaken
hash verification or upload renamed bytes as a substitute.
