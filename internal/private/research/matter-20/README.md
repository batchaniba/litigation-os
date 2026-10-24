# Matter 20 Research Branch

This private research room collects the source record and working materials for Newanforbi v. California Highway Patrol, Alameda Superior Court case 26CV191136. It preserves original documents, exact-byte aliases and source commits without changing the portfolio's live docket, calendar, public registry or R2 objects.

The initial collection contains 92 unique PDFs and 268 source/derivative assets representing 386 source occurrences. Counts exclude this README and administrative audit files; the manifest distinguishes originals, historical analysis, graph snapshots and generated text.

## Start here

- **Record-to-argument map**: `09-evidence-map/Matter-20-Record-to-Argument-Evidence-Map.md` connects the surviving writ theory to primary-record pinpoints, contrary evidence, proof gaps and conditional remedies. It is newly authored analysis, separate from the baseline collection's 268 indexed assets.
- **Federal screening-order supplement**: The June 29, 2026 federal order is preserved in `00-user-inputs/` and added to the map as R15/A19–A20, with assumed-true limits, page-specific quotations and a proposed limited-use paragraph. Its two source/derived assets are separately hash-indexed in `08-audit/supplemental-manifest-federal-screening-order-2026-10-24.json`; the original 268-asset/92-PDF baseline is unchanged.
- **Requested packets**: `00-user-inputs/Newanforbi_26CV191136_Writ_Motion_Packet.pdf` and `00-user-inputs/Matter20_Merged_v3.pdf` are preserved under their original filenames. Inclusion does not independently establish that a packet was filed, served or admitted.
- **Human-readable inventory**: `08-audit/inventory.md` lists each unique research file, PDF page count, size, hash and source count. Its retrieval-gap section identifies known material not yet imported as original bytes.
- **Provenance manifest**: `08-audit/manifest.json` records source paths, branches, immutable commits, duplicate aliases, historical inventory filing labels, retrieval method and targeted R2 object locations. `08-audit/SHA256SUMS` permits byte-level verification from this folder.

## Collection structure

- **`01-portfolio-records/`**: Matter 20 portfolio records, the original petition and demurrer record recovered from the legacy Matter 32 `from-20` home, orders, correspondence and related lodging materials. Proposed orders, service proofs and historical filing labels are not automatically adopted as operative judicial facts.
- **`02-incident-evidence/`**: Relevant Matter 33 incident records, including the arrest report, DS-367 material, discovery records, DMV-related documents and transcript. Transcript text is not a substitute for reviewing the native recording.
- **`03-discovery-production/`**: Production Set One, the incident log, beat sheet, CHP-202/DS-367/warrant material, CHP-415 reports, privilege log, service material, dashcam coversheet and preserved production analysis. Exact-byte duplicates are stored once; their aliases remain in the manifest.
- **`04-drafts-and-working-papers/`**: User-supplied versions and the prior assistant-generated package, explicitly separated from the evidentiary record. No draft is certified as filed, current, legally sufficient or guaranteed to succeed.
- **`05-prior-analysis/`**: Historical research rooms and selected source-branch materials. Their legal assertions, quotations, calendar statements and recommendations are preserved for comparison, not adopted or independently reverified.
- **`06-source-snapshots/`**: Read-only copies of relevant Matter 20 graph siblings and selected historical manifest data. Consult the actual live `clocks.json` and `docket.json` for current calendar and pleading information.
- **`07-source-text/`**: Existing sidecars, recovered R2 text and generated `pdftotext -layout` output. The original PDF controls; text extraction is not an OCR-accuracy or transcription certification.
- **`08-audit/`**: Inventory, hashes, source provenance, R2 key audits, exclusions and remaining retrieval gaps.
- **`09-merits-analysis/`**: Added October 24 as a separate research-only layer: the full remedy-focused writ research memorandum with citations to the two original uploaded packets, plus a use/verification guide. Not counted among the 268 preserved source assets.

## Important discoveries and limits

The core case record is distributed across Matter 20, Matter 32's `from-20` folder and related Matter 33 incident materials. Some files absent from current branch tips were recovered from repository history and accepted only when their bytes matched the registered SHA-256.

The R2 review paged all 6,004 object keys in `litigation-documents` and filtered the 1,726-entry path index for relevant records. It did not exhaustively read or OCR-search every unindexed object's contents; the four objects in `ilp-backups` were inventoried as D1 SQL/FTS backups, not fully unpacked.

Several older staged PDFs exist in R2 under bare-hash keys but were not retrievable through the public document Worker. Their known keys remain in the gap list; six associated text objects were separately retrieved and byte-hash verified, without pretending that text is the missing original PDF.

The remaining retrieval gaps are seven original PDFs and one indexed text sidecar. The uploaded beat-sheet PDF has too little extractable text for reliable text search and is flagged for OCR; its original bytes remain intact.

The preserved production-description document records four native MP4s with historical hashes, sizes and private Drive locators. Those videos were not downloaded, independently hash-verified or committed to this branch; retaining their locator record is not a representation that the native video evidence is present.

## Research controls

Keep Count 1 writ research separate from dismissed claims, damages theories and related federal litigation. The separate Centerline wage-reference document was excluded from this narrow certification-writ collection.

Do not infer a live hearing from a draft reservation, valid service from a rejected proof, admission from lodging, or an established fact from an analyst's description. Preserve the distinction between the April agency record, later production, proposed findings and actual court rulings.

This directory stays under `internal/private/`. Do not register its contents in the public SPA, Worker/D1 publication, public document manifest or calendar merely because they were collected here.
