# Verification report

## Source review

- Main baseline: eaacea3e448e8296ca7747b5765b4ccb5d15cb4b. Base tree: a8a272994696ac428eb302af432cb4f6de3ed3be.
- The complaint was recovered at historical commit 893e4169fc91c973731bd7a0b91c59f5f632f994; 97,212 bytes and SHA-256 match the registered manifest.
- Downloaded/rehashed ECF 15, the signed state order, and ECF 30-1. State-order operative page and the two state-docket screenshot pages were rendered and visually reviewed.
- Read full available opposition/reply text, ECF 28/29 extracted text, and relevant PO/historical-analysis material. ECF 15 source text was generated from the original PDF. The manifest does not label all 18 preserved PDFs independently substantively reviewed.
- Retained source copies by existing Git blob SHA. The source inventory records original paths/ref and distinguishes registered document hashes from independently recomputed hashes.
- The opposition's registered native PDF returned HTTP 404 from the document Worker; its existing complete text sidecar is preserved. This gap is not hidden by creating a replacement PDF. ECF 30 identifies the opposition as ECF 23; acceptance/exact filed bytes still need current docket confirmation.
- Selected official procedures/primary opinions were checked; the authority ledger states limits. The current standing order is February 17, 2026.

## Repository validation

`npm run gate` was attempted using the unchanged main-branch package/gate and direct dependencies in a connector-materialized local workspace. It exited 1 at its fail-closed prerequisite check:

> portfolio-gate: node_modules missing — run npm install, then npm run gate.

This is **not a passing gate**. A complete authenticated local clone and installed repository dependencies were unavailable; no emergency bypass was used. The local files fetched only to attempt the gate are not included among this branch's changes. Run the full gate in a normal checkout before merging.

Targeted document verification checks new paths remain under this private room, generated JSON parses, links between newly authored documents resolve, source alias paths are unique and reuse valid retrieved Git blob identities, and the expected court/party/count/date labels appear. A post-commit GitHub compare and read-back verify the actual changed-file scope.

Historical copies in `05-prior-analysis/` are preserved byte for byte, including their original relative links and stale statements. Read them in the context of their recorded original path; the new room's README/map/gap report governs the new preparation. They are not silently rewritten or endorsed.

## Review status

Completed first hearing-preparation draft. Current-docket, objection-filing, finality, PO-entry/cross-use, defense-disclosure, current-injunction facts and consent-status questions remain explicit. No filing-ready representation is made. No court, counsel, or other recipient was contacted. No merge, deployment, public registry, calendar, or R2 write was made.
