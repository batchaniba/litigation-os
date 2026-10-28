# Verification report

## What was opened

- Live Matter 29 graph: `matter.json`, `clocks.json`, `docket.json`, `claims.json`, `counsel.json`, `damages.json`, `evidence.json`, `parties.json`, `documents.json`, `events.jsonl`.
- `internal/docs/matter-29/` accuracy audit, 60-day calendar, dispute draft.
- `internal/docs/counsel/frederick-stanzick/README.md` and PLAYBOOK.md (start).
- User PDF `accurate-reinvestigation-2026-10-28.pdf` (25 pages); SHA-256 hashed; text extracted with pypdf (not poppler `-layout`).
- Matter 20 / 28 / 32 research-room trees on origin (structure only).
- `origin/matter-29/discovery-set-one-amazon-accurate-2026-10-17` README and ESI proposal (snapshots).

## What was not done

- No PACER refresh.
- No CourtListener citation run (`citation-verify` skill not executed).
- Krishnan standing-order PDF not re-read in this room.
- Oct. 14 consumer-report PDF not byte-compared page-by-page in this room; comparison uses the Oct. 14 **audit** plus the Oct. 28 extract. Flag: **UNVERIFIED** pixels for any cell that the audit did not quote.
- Discovery-set-one generated PDFs not copied.
- No email sent; no clock edited; no R2 upload; no public manifest change.
- No settlement-guard run (no figure proposed).

## Extraction limit

`pdftotext` was not available. `pypdf` extracted 25 pages / 49,777 characters. Letter page 1 extract is whitespace-heavy (address block). Substance of the letter and report was also read from the PDF via the environment's PDF reader. **The PDF bytes control.**

## Hash

See `SHA256SUMS`. Independent re-hash before any court use.
