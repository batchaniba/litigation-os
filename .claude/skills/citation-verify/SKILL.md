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

2. **Lookup** — existence via CourtListener + CAP `static.case.law`  
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
| *In re Leman*, 66 Cal.App.5th 200 | Must **not** resolve (NOT_FOUND) |

## Source reachability (this cloud environment)

| Source | Status |
|---|---|
| CourtListener `/api/rest/v4/search/` | OK (unauthenticated) |
| CourtListener `/api/rest/v4/citation-lookup/` | Needs `COURTLISTENER_TOKEN` (alias: `COURTLISTENER_API_TOKEN`) |
| CAP `static.case.law` CasesMetadata + HTML | OK |
| `api.case.law` JSON | Need auth |
| Justia | Cloudflare 403 |
| Google Scholar | Unreliable (often 403) |
| govinfo Search Service | Opt-in `--probe-extra`. POST JSON + name-match. Not a Horn resolver. |
| `cdn.ca9.uscourts.gov` | Opt-in `--probe-extra`. Strip `No. `; opinions then memoranda. |

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
| `internal/docs/citation_verification_sources.json` | Case-law source catalog (wired / opt-in / gap) |

## Priority queues (from ledger)

- **P0** — plaintiff-only + `UNVERIFIED` → clear first (`verify-citations.py --queue`)
- **P1** — plaintiff-only + bad status → remediation lists for future drafts
- Existence ≠ holding — characterization still needs opinion text

## Known fabrications (hard NOT_FOUND)

*In re Leman*, *Friends of the Trinity River*, *Dunford v. Rovi*, *Collins v. Moore*, *Burrell v. Jackson* — see `KNOWN_FABRICATED` in `verify-citations.py`. New plaintiff-filing introductions fail CI unless listed in the debt file.
