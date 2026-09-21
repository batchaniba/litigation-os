---
name: citation-verify
description: Verify legal citations in the litigation portfolio — existence, caption match, and known fabrications. Use when the user asks to check cites, run the citation funnel, look up authorities on CourtListener/case.law, clear UNVERIFIED queues, audit a matter's authorities, or asks whether a case exists / is miscited. Covers citation_index, lookup-citations, verify-citations, and the known-bad CI gate.
---

# Citation verification funnel

Do not mark a citation VERIFIED from memory. Run the funnel and record evidence.

## Pipeline (always this order)

1. **Index** — every cite keyed to page + role  
   `npm run citations:index`  
   → `internal/docs/citation_index.json` / `CITATION_INDEX.md`

2. **Lookup** — existence via offline bulk oracle + CourtListener + CAP `static.case.law`  
   ```bash
   npm run citations:lookup                         # controls + high-risk batch
   npm run citations:lookup:matter -- --matter N    # one matter's authorities
   ```  
   → `citation_lookup_multisource.json` or `citation_lookup_matterNN.json`

3. **Overlay** — fold lookup consensus into `citation_verification_rounds.json`  
   - `FOUND` + prior `UNVERIFIED` → `VERIFIED` (existence only)  
   - `CAPTION_MISMATCH` with wrong case at pin → `MISCITED`  
   - Prior `MISCHARACTERIZED` / proposition-`MISCITED` **stays** even if the pin exists  
   - Never downgrade a table-page `VERIFIED` solely because CL’s first hit differs  
   - `UNRESOLVED` and `NOT_FOUND` are left alone (a miss is not a fabrication; a skipped probe is not a miss)

4. **Ledger + gate**  
   ```bash
   npm run citations:verify    # rebuild citation_verification.json + .md
   npm run citations:check     # fails on new known-fabricated plaintiff_filing hits
   npm run generate:readme     # refreshes README citation scoreboard
   ```

`npm run validate` already runs `citations:check`.

## Method controls (reconfirm when batching)

| Control | Expectation |
|---|---|
| *Richardson v. McKnight*, 521 U.S. 399 | Must resolve (FOUND) |
| *In re Leman*, 66 Cal.App.5th 200 | Must **not** resolve as FOUND. `NOT_FOUND` when citation-lookup 404s; `UNRESOLVED` if pin sources were skipped |

## Consensus vocabulary

- **FOUND** — a live pin source hit with a compatible caption  
- **NOT_FOUND** — citation-lookup returned 404 and the other live pin sources actually ran and missed  
- **UNRESOLVED** — probes were skipped (no token, no bulk DB, volume metadata unavailable) or incomplete. Absence of evidence is not evidence of absence  
- **PARTIAL** — single-source hit, or name-only search with no reporter/WL pin behind it  
- **CAPTION_MISMATCH** — pin resolves to a different case  

Pin confidence is separate: only CAP `*page-label` anchors or official prelim/bound PDFs are PRIMARY.

## Source reachability (this cloud environment)

Live source survey (controls, star pagination, cliffs, traps): `internal/docs/CITATION_SOURCE_SURVEY.md` (2026-09-19). Wired/opt-in/gap catalog: `internal/docs/citation_verification_sources.json`.

| Source | Status |
|---|---|
| CourtListener `/api/rest/v4/search/` | OK (unauthenticated). Use fielded `citation:"…"` plus caption — bare `q=` returns citing cases. |
| CourtListener `/api/rest/v4/citation-lookup/` | Needs `COURTLISTENER_TOKEN` (alias: `COURTLISTENER_API_TOKEN`) |
| CAP `static.case.law` CasesMetadata + HTML | OK inside the scan window (U.S. through 2014; no F.4th; Cal.App.5th only vols 1–11). Star pagination lives here. |
| `api.case.law` JSON | Retired 2024-09-05 (HTML docs redirect, not a lookup) |
| Justia | Cloudflare 403 |
| Google Scholar | Unreliable (often 403) |
| Casetext | 410 Gone (shuttered 2025-04-01) |
| govinfo Search Service | Opt-in `--probe-extra`. POST JSON + name-match. Not a Horn resolver. |
| `cdn.ca9.uscourts.gov` | Opt-in `--probe-extra`. Strip `No. `; opinions then memoranda. |
| `cl_bulk_offline` | Step 0 if the local SQLite index exists (`build-bulk-citation-index.py`). Existence only. A miss is not NOT_FOUND. |
| Westlaw Patron Access for Pro Se | Plaintiff has it (2026-09-19). MANUAL ONLY — KeyCite / bare WL / post-cliff pins. Never wire; never put OnePass in chat. |

`--probe-extra` is evidence only. It does **not** vote in `consensus_for()`. Do not mark VERIFIED from a govinfo first hit.

## Artifacts

| File | Role |
|---|---|
| `internal/docs/citation_verification.json` | Portfolio ledger |
| `internal/docs/CITATION_VERIFICATION.md` | Human report |
| `internal/docs/citation_verification_rounds.json` | Round overlays |
| `internal/docs/citation_known_bad_debt.json` | Allowed pre-existing fabrications |
| `internal/docs/citation_audit.json` | July + Matter 28 hand audit |
| `internal/docs/MATTER_28_SAFE_CITE_LIST.md` | Matter 28 page-keyed safe/do-not-use |
| `internal/docs/WESTLAW_PORTFOLIO_QUEUE.md` | Unique KeyCite queue (20-view sessions). `python3 internal/scripts/build-westlaw-queue.py` |
| `internal/docs/citation_verification_sources.json` | Case-law source catalog (wired / opt-in / gap) |
| `internal/docs/CITATION_SOURCE_SURVEY.md` | Live free-source survey (2026-09-19) |
| `internal/docs/WESTLAW_PATRON_ACCESS.md` | Library remote door + session hygiene |
| `internal/docs/legal-intel/recon/2026-09-19-matter-28-keycite-westlaw.md` | Matter 28 UNIFIED KeyCite (27/27) |

## Priority queues (from ledger)

- **P0** — plaintiff-only + `UNVERIFIED` → clear first (`verify-citations.py --queue`)
- **P1** — plaintiff-only + bad status → remediation lists for future drafts
- Existence ≠ holding — characterization still needs opinion text

## Known fabrications (hard NOT_FOUND)

*In re Leman*, *Friends of the Trinity River*, *Dunford v. Rovi*, *Collins v. Moore*, *Burrell v. Jackson* — see `KNOWN_FABRICATED` in `verify-citations.py`. New plaintiff-filing introductions fail CI unless listed in the debt file.
