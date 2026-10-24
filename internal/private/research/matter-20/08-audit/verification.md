# Matter 20 Research Collection Verification

The collection was assembled on October 24, 2026 in a separate worktree on `research/matter-20-2026-10-24`. Its application/data baseline is the immutable `origin/main` commit recorded in `manifest.json`.

## Integrity checks

- **Requested uploads**: Both requested PDFs are copied under their original filenames and are included in the SHA-256 manifest.
- **Independent byte verification**: A separate verification pass re-read all 268 indexed research assets and matched every recorded size and SHA-256, with zero failures.
- **PDF parsing**: All 92 unique PDFs returned page counts from `pdfinfo`; no PDF failed the parser check. Poppler emitted reconstruction/shared-object warnings on some source files; no repair or alteration of source bytes was performed.
- **Text search**: `pdftotext -layout` output is explicitly derivative. The uploaded beat sheet is flagged as needing OCR; extracted text is not certified complete or accurate.
- **Deduplication**: Exact-byte aliases share one research copy while source occurrences and commits remain in the manifest. Distinct document versions are not collapsed merely because their titles resemble one another.
- **R2 text retrieval**: Six original text objects were recovered through the Cloudflare connector and accepted only after their UTF-8 byte hashes matched their indexed SHA-256 values.
- **Binary retrieval restraint**: Lossy connector-decoded PDF strings were not saved as original PDFs. Seven known older PDF objects and one text sidecar remain explicit retrieval gaps.

## Repository checks

The portfolio gate passed under Node 22.22.2: lint, typecheck, portfolio validation, document-kind validation, golden damages tests, 61 test files containing 609 tests, and the known-bad citation gate. Existing lint/data warnings and the existing citation-verification debt remain; gate success does not independently verify legal authorities preserved in historical research.

Only the new private research directory is intended for this commit. No live docket, clock, event log, public document manifest, Worker configuration, R2 object or main-branch file is changed by the research collection.

## Verify locally

From this research directory, run `sha256sum -c 08-audit/SHA256SUMS`. The integrity manifest covers research assets, while README and audit metadata are administrative files outside its asset count.
