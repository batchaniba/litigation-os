# Verification Results

Checks run October 26, 2026. The room is a research work product, not a filing-ready opposition or complete docket certification.

## Source preservation

- **Preserved assets:** 224 manifest records, including 153 original PDF assets, supporting snapshots, external text/audit records, and collection-script records.
- **Cloudflare recovery:** 114 unique manifest assets were obtained through the existing R2-backed document Worker and verified against the portfolio manifest's expected SHA-256. The Cloudflare connector also read the bucket/index and confirmed the old FAC object exists despite the Worker returning 404.
- **Selected unrecovered assets:** 11 original selected-manifest PDFs remain explicitly listed in `manifest.json`. Some have useful alternate records, but an alternate is not certified as the missing exact original.
- **Integrity:** All 224 entries in `SHA256SUMS` passed. Room validator passed source existence, hashes, sizes, PDF signatures, extraction-path presence, duplicate IDs/paths, provenance, and workshop source-ID existence.
- **Central visual checks:** Produced CHP 202 p. 2, DS 367 pp. 1–2, actual warrant/affidavit pp. 20–21, and supplied ECF 23 checkbox were visually reviewed.

## Code and scope

- **Scope:** All staged changes are inside `internal/private/research/matter-32/`. No tracked live graph, clocks, public assets, Worker code, or deployment configuration changed.
- **Golden test:** `npm run test:golden` passed, with 20 damages rows and totals matching.
- **Authored-text check:** `git diff --cached --check` passed for README, workshop, and audit files. Original PDFs and machine-extracted text are preserved as opaque source/derivative artifacts rather than reformatted to satisfy whitespace rules.
- **Private repository:** GitHub repository visibility was checked as private. Existing Vercel configuration disables Git deployments; no deployment action was requested or invoked.

## Whole-portfolio validator is not green

The existing whole-portfolio validator initially required generating ignored derived summary files. After generation, it reported 96 warnings and 2,010 errors, principally unresolved local document paths in the offloaded document architecture; it was not silently treated as a pass.

The same validator was run in a separate detached worktree at the unchanged base commit `0cc3acd62ca01459db0b3dff8b2b96684727de16`, with the same generated summaries. Baseline and workshop validator outputs were byte-identical, including the warning and error counts; this branch introduced no observed validator regression. No unrelated mass document/path repair was attempted.

## Not verified

Original audiovisual evidence, the stamped original Kim recommendation PDF, the earlier amended complaint original PDF, comprehensive prior disposition orders, live PACER posture, actual current assigned judge, and a final opposition deadline remain gates. The November 9 backstop is a conditional rule-based calculation, not a live-docket certification.

Comprehensive negative-treatment review, all claim-specific qualified-immunity authorities, independent due-process fabrication analysis, and a completed corrected-affidavit materiality conclusion remain unfinished. The working brief clearly marks those limits.
