# Portfolio true-up — October 28, 2026

Draft PR only. Do not merge or deploy until Plaintiff reviews. This analysis file is not a live calendar (`clocks.json` is). It lists every data change in this pass, its source, and what remains unverified.

**As-of date:** SPA `DashboardTab` reads the latest `timeline.json` `verified_at`. A milestone event with `verified_at: "2026-10-28"` is the last verification stamp. Index `today` is `2026-10-28`.

**Live Pages/Vercel still show 2026-09-18** until this branch is deployed. This PR does not deploy.

## What this environment could not reach

| Source | Result |
| --- | --- |
| Cloudflare R2 admin (`R2_*`, `~/.config/r2/env`) | Not present. Worked from the repo + public Worker. |
| Worker `https://litigation-doc-api.ss8sxswwkt.workers.dev/health` | `ok: true`, bucket `litigation-documents`. D1 `seeded_at` **2026-10-16**, `stale: true`, source commit `fe7120f8`. Not reseeded (no admin keys; user asked not to deploy). |
| CourtListener (`COURTLISTENER_TOKEN`, `.env`) | Not present. API/HTML 401/403. Last ledger sync **2026-09-12**. No incremental docket pull. |
| Open PRs #1035 / #1036 / #1038 | Read via GitHub. Dkt. 22/23 PDFs live on #1035, not copied onto this branch. Accurate Oct. 28 reinvestigation letter lives in the #1036 private research room; not published. |

No Randstad settlement figure is in any public status label, README upcoming table, or index `next_clock`. Private M27 payment clocks stay `private: true`.

Damages/exposure table was **not** changed. Do not invent figures. The live moderate aggregate ($3,523,072) is unchanged.

## Code (leak stop)

Public surfaces were still able to surface `private: true` clocks (Matter 27 Randstad payment / outside date) as the index `next_clock` and in the README upcoming table.

| File | Change | Source |
| --- | --- | --- |
| `internal/scripts/lib/publish-matter.mjs` | `isCourtFacingClock` rejects `private: true`. | Settlement-guard / no public settlement amounts. |
| `internal/scripts/lib/upcoming-from-clocks.mjs` | `excludePrivate` on flatten; `nextFromClocks` always skips private. | Same. |
| `internal/scripts/sync-upcoming.mjs` | SPA upcoming snapshot uses `excludePrivate: true`. | Same. |
| `internal/scripts/generate-readme-tables.mjs` | README upcoming table uses `excludePrivate: true`. | Caught on regenerate: Oct. 9 payment row had leaked into README. |
| Tests in `upcomingFromClocks.test.js` and `publish-matter.test.mjs` | Assert private payment clocks stay off public index/SPA. | Unit coverage. |

Laptop `npm run next` can still see private clocks (desk view without `excludePrivate`).

## Matter-by-matter

Clock stored statuses remain `open \| set \| contingent \| vacated \| satisfied`. `overdue` is derived on the index, never stored.

### Matter 5 — Palacios (STK-CV-UF-2026-0001032)

| Change | Source |
| --- | --- |
| Status: dismissed Jul. 15 WOLA; Plaintiff requesting entry of judgment. | User report Oct. 28; Jul. 15 WOLA order already on disk. |
| New clock `05-judgment-request` (open, 2026-10-28). | User report. No filed request PDF. Do not invent a judgment date. |
| Sep. 21 register re-pull found no CCP § 581d judgment — left as narrative, not a new clock. | Prior repo fact. |

### Matter 19 — Macomber habeas (C2604791)

| Change | Source |
| --- | --- |
| Status label: HC-004 pending; Oct. 1 CRC 4.551(a)(6)(B) calendar passed. | Computed from Sep. 1 in-person HC-004. |
| Clock `19-deadline-1` **left open** (derived overdue). | No ruling PDF; CourtListener unavailable. **UNCERTAIN** whether the court has ruled. |

### Matter 20 — CHP writ (Alameda 26CV191136)

| Change | Source |
| --- | --- |
| CMC Nov. 4, 2026, 4:00 p.m., Dept. 25, Hon. Jenna M. Whitman. | User report. No continuance-order PDF. |
| Opening brief Nov. 13; opposition Dec. 11; reply Dec. 18; merits hearing Jan. 8, 2027. | User report. Replaces prior internal Nov. 2 / CCP § 1005(b) Dec. 11 computations. |
| Oct. 28 CMC, Oct. 13 CMS, Nov. 2 target, old Dec. 11 open-brief computation: vacated/superseded. | Follows the Nov. 4 / Nov. 13 user dates. |
| RFP Set One watch Oct. 20: satisfied. | CHP Production Set One served Oct. 23 (production-map / PR #1026). Completeness not stipulated. |

**Open:** ingest the CMC-continuance / briefing order when it exists.

### Matter 25 — FedEx (E.D. Cal. 2:26-cv-02881)

| Change | Source |
| --- | --- |
| Oct. 8 status conference: vacated (date passed). | Calendar. **UNCERTAIN** outcome — no minute/scheduling order ingested. |
| Discovery Set One responses watch Nov. 5 remains open. | Email service Oct. 6 already on clocks. |

### Matter 27 — Randstad (Alameda 26CV199902)

| Change | Source |
| --- | --- |
| Public `next_clock` is CMC Dec. 17 (`27-deadline-3`). | Private payment clocks excluded from index. |
| Stipulated response Oct. 26: vacated (date passed). Confirm Alameda docket. | Calendar. Do not publish agreement terms. |
| `27-deadline-5` payment and `27-outside-date` remain **open + private**. | No confirmation that checks cleared. **UNCERTAIN**. Not on public pages. |

No settlement number was added, moved, or published.

### Matter 28 — Smith / HOPE (N.D. Cal. 3:26-cv-07504-LJC)

| Change | Source |
| --- | --- |
| Oct. 27 combined CMC + Dkt. 15 MTD held; MTD deferred pending San Joaquin judgment; discovery stayed. | User report of the Oct. 27 order. **No order PDF ingested.** Clocks cite Dkt. 29 (Oct. 8 continuance) as the closest on-disk order. |
| Joint status reports Nov. 17, 2026 and the 17th monthly through May 17, 2027. | User report. |
| Joint CMC statement June 10, 2027; CMC June 17, 2027, 1:30 p.m. | User report. |
| Phase `stayed`. L.R. 7-3(d) objection window and Joint-CMS proposed Nov. 13 re-production: vacated. | Follows the stay. |

**Open:** ingest the Oct. 27 order when PACER/R2 has it; then point `source_dkt` at that docket number (do not invent one now).

### Matter 29 — Amazon / Accurate (N.D. Cal. 4:26-cv-09249-ASK)

| Change | Source |
| --- | --- |
| Rule 26(f) Nov. 6, 1:00 p.m. PT (already on clocks). ADR certification Nov. 10; Joint CMS Nov. 24; CMC Dec. 1; Dkt. 19 MTD Nov. 18. | Dkt. 9 + existing MTD clocks + user confirmation. |
| Accurate reinvestigation removed the "Newansorbi" alias. Clock `29-accurate-reinvestigation` satisfied. | User report Oct. 28. No result-letter PDF on this branch (PR #1036 private room). NSOR component completeness **not independently verified**. |
| § 1447(c) remand window Sep. 30: satisfied (closed, no motion). | Computed window + no remand filing on disk. |
| CRD right-to-sue watch: contingent, undated. | Internal gap, not a court deadline. Outer CRD limit remains 3 years from July 2026. |

Identity JSON is still ~11 KB (pre-existing over the 8 KB mutate cap). Not rewritten to shrink.

### Matter 32 — Meza / Melano (N.D. Cal. 4:26-cv-08271-ASK)

| Change | Source |
| --- | --- |
| Summons return being refiled. `32-deadline-1` stays **open** (derived overdue; dkt null). | User report. Do not invent a filing. |
| Computed Oct. 19 Rule 12(a) watch: vacated. | Service return is being refiled; PR #1035 catalogs a later MTD. |
| Melano-answer watch: satisfied as answered-by-motion. | Open PR #1035 catalogs **Dkt. 22** MTD/strike filed Oct. 26 and **Dkt. 23** magistrate declination. PDFs **not copied** onto this branch (no registry/docket rows here). |
| New computed opposition clock Nov. 9 (Civ. L.R. 7-3(a): 14 days after Oct. 26). | Computed. Confirm against the motion notice once the PDF is ingested. **No hearing date invented.** |

**Open:** merge or cherry-pick #1035 PDFs + docket rows; confirm PACER; do not treat Dkt. 23 as a reassignment until a clerk notice exists.

### Matter 33 — Candelaria (N.D. Cal. 3:26-cv-08272-RFL)

| Change | Source |
| --- | --- |
| Rule 26(f) / ADR certification title expanded; date remains Nov. 18. | User report + Dkt. 4 / Dkt. 23 (already on clocks). |
| Defendants' FAC response due Oct. 27 (`33-deadline-7`) **left open** (derived overdue). | Dkt. 24. Filing **not verified** on PACER. |
| CMC Dec. 9, 10:00 a.m., Hon. Rita F. Lin unchanged. | Existing clock. |

### Matter 35 — Ross (Santa Clara 26CV501995)

| Change | Source |
| --- | --- |
| Oct. 21 meet-and-confer task and Oct. 26 demurrer/extension task: vacated (dates passed; no paper ingested). | Calendar. Do not invent a Nov. 25 extension. |
| Discovery responses Nov. 17 remain open. | Existing clock. |

### Matter 38 — Swift (E.D. Cal. 2:26-cv-03312)

| Change | Source |
| --- | --- |
| CCP § 338(a) outer-bound filing clock: satisfied (federal action is on file). | Case number already assigned. |
| IFP-or-fee Oct. 26 (`38-order-ifp-renewal`) **left open** (derived overdue). | ECF No. 4. **UNCERTAIN** — no payment/renewed AO 239 ingested. This is **not** Matter 39. |

### Matter 39 — Best Buy (E.D. Cal. 2:26-cv-03315)

| Change | Source |
| --- | --- |
| $405 fee paid by money order Oct. 27; IFP withdrawn as moot. | User report. No receipt or withdrawal PDF. |
| Satisfied clocks `39-fee-paid` and `39-ifp-withdrawn`. | Same. No `next_clock` until the clerk dockets the fee / issues summons. |

### Matter 41 — Nuro (pre-filing)

| Change | Source |
| --- | --- |
| Sep. 25 Checkr watch: satisfied (date passed; no authorization/disclosure ingested). | Calendar + empty file. Still unripened. |

### Matter 42 — Staples / First Advantage (pre-filing)

| Change | Source |
| --- | --- |
| Oct. 14 file-request watch: contingent, undated. | Still watching for the FADV file / Fair Chance preliminary decision. No new PDF. |

### Matter 43 — Hertz (pre-filing)

| Change | Source |
| --- | --- |
| 16 Hertz/HireRight/ADP paths added to `registry.json`. | Pre-existing `documents.json` + `npm run sync:registry`. Unblocks validate-portfolio. No new facts invented. Status unchanged (HireRight screening active). |

## Timeline archive

`internal/src/data/timeline.json`:

- Appended Oct. 28 true-up milestone (`verified_at: 2026-10-28`) so the SPA badge reads that date.
- Set `upcoming: false` on past or vacated archive rows (27 from `retire:upcoming`, plus M20 Oct. 28 CMC, M27 CRC 3.110(h) default-judgment target, M33 Cisneros-era Nov. 5 / Nov. 12). Live calendar remains `clocks.json`.
- Formatting kept at HEAD's 1-space / UTF-8 so the diff is the flags + milestone, not a full rewrite.

`events.jsonl` is append-only. New Oct. 28 lines on matters 5, 20, 28, 29, 32, 39.

## Derived files regenerated

`npm run sync:derived` and `npm run generate:readme` (with `PORTFOLIO_SKIP_DISK_DOCS=1`):

- `internal/src/data/index/matters.json` — `today: 2026-10-28`
- README inventory / upcoming table (private clocks excluded)
- gitignored: `upcoming.json` (49 events), `summaries.json`, `publish/*.json`

Index derived-overdue `next_clock` rows after this pass (expected, flagged):

| Matter | Clock | Why it stays |
| --- | --- | --- |
| 19 | habeas ruling calendar Oct. 1 | No ruling ingested |
| 32 | summons-return FILE Sep. 17 | User: refiling in progress |
| 33 | FAC response Oct. 27 | Filing not verified |
| 38 | IFP-or-fee Oct. 26 | Payment/renewal not verified |

## What was not done (on purpose)

- No merge, no Vercel/Pages deploy, no Worker D1 reseed, no R2 push.
- No CourtListener sync.
- No damages/exposure edits.
- No Randstad settlement amount anywhere public.
- Did not copy PR #1035 PDFs or #1036 private research onto this branch.
- Did not invent Dkt. 22 hearing date, Palacios judgment date, FedEx scheduling order, Swift fee payment, or Candelaria answer filing.
- `sync-public-timeline.mjs` still fails on a missing `settlementLeakPatterns` export (pre-existing). Not used.

## Open questions for Plaintiff

1. Matter 28: please drop the Oct. 27 order PDF when PACER has it.
2. Matter 32: confirm Dkt. 22/23 on PACER and whether to ingest #1035 in a follow-up; confirm opposition date against the motion notice; summons-return refile still open.
3. Matter 33: did defendants file the FAC response on Oct. 27?
4. Matter 38: was the Swift IFP renewed or the fee paid? (Best Buy M39 is the fee that was paid.)
5. Matter 19: any Macomber ruling after Oct. 1?
6. Matter 25: any Oct. 8 minute order / schedule?
7. Matter 27: payment/outside-date clocks stay private and open until Plaintiff says otherwise.
8. Matter 29: ingest the Accurate Oct. 28 letter when it is safe to put on the public graph (not the #1036 private room).
9. Worker D1 is 12 days stale; reseed from laptop after merge if the public `/matters` API should match this graph.

## Addendum — ECF / Gmail pass, Oct. 28, 2026 (4:00 p.m. PT)

Follow-up to PR #1039. Sources are CM/ECF Notices of Electronic Filing received in Plaintiff's Gmail and Plaintiff's own sent mail. No PDFs ingested; no deploy, reseed, or R2 push. Answers open questions 1, 2, and 3 above.

| Matter | Change | Source |
| --- | --- | --- |
| 5 | `05-judgment-request` satisfied (filed Oct. 27). New contingent `05-judgment-entry-watch`. | Plaintiff's Oct. 27 courtesy-copy email: CCP § 581(f)(1) request, proposed judgment, POS; eFiling order no. 23338459. |
| 28 | Order-derived clocks now cite `source_dkt: 38`. Dkt. 37 = motion-hearing minute entry. | NEFs Oct. 27, 3:54 p.m. (Dkt. 37) and 3:58 p.m. (Dkt. 38). NEF emails carry no docket text; contents remain Plaintiff's report. |
| 32 | Opposition Nov. 9 and reply Nov. 16 now from Dkt. 22 docket text (no longer computed). New `32-mtd-reply` (open) and `32-mtd-hearing` Dec. 9 1:30 p.m. (vacated). New contingent `32-reassignment-watch`. | Dkt. 22 NEF (Oct. 26); Dkt. 25 Clerk's Notice of Impending Reassignment (Oct. 28) vacated all hearing dates before the magistrate judge. |
| 32 | Opposition **not on ECF**: emailed to DOJ Oct. 27, no NEF through Oct. 28 4:00 p.m. Clock stays open. | Gmail sent + NEF search. |
| 32 | `32-deadline-1` stays open. Dkt. 21 (Melano return) drew a filing-error notice; refiled as Dkt. 24 Oct. 28. Dkt. 24 is Melano, not the Meza-Gonzalez § 415.20(b) declaration this clock tracks. | NEFs Oct. 26 / Oct. 28. |
| 33 | `33-deadline-7` satisfied: Dkt. 26 Answer to FAC by Candelaria and Gordon, Oct. 27. | NEF Oct. 27, 3:48 p.m. |

Still open: Matter 19 (no Macomber ruling email found), Matter 25 (no E.D. Cal. NEF since Oct. 1), Matter 38 (an Oct. 20 "Notice of Payment of Filing Fee" PDF for Swift exists only as an email to self — not proof of payment), Matter 32 Meza-Gonzalez return, and the PDFs for Dkt. 37/38 (M28), Dkt. 22–26 (M32), Dkt. 26 (M33).

## Addendum — San Joaquin docket pass, Oct. 28, 2026 (evening PT)

Sources: San Joaquin eCourt public portal (checked Oct. 28, 2026) and Plaintiff's AppFile e-filing order status. No PDFs ingested; no deploy, reseed, or R2 push.

| Matter | Change | Source |
| --- | --- | --- |
| 5 | Status re-verified: Disposed 07/15/2026; no judgment entered; no new tentative (latest remains Jul. 10, 2026). `05-hearing-exparte-judgment` (Nov. 2, 9:15 a.m., Dept. 10A) verified on calendar. | eCourt portal, Oct. 28. |
| 5 | New `05-exparte-opposition` (satisfied Oct. 28): Response to ex parte and Objection to proposed judgment, relodged proposed judgment without "with prejudice", POS. `05-judgment-entry-watch` text updated. Two unfiled docket rows added (`filed: false`, no path) for the Oct. 27 and Oct. 28 submissions. | AppFile orders 23338459 (Oct. 27) and 14773399 (Oct. 28), both Awaiting Verification; neither on the public docket yet. |
| 12 | Lifecycle `active` → `dismissed` (phase `terminal`, badge DISMISSED, label "Dismissal filed Oct. 26 — pending closure"). Filed docket row for Request for Dismissal (entire action), no path. New contingent `12-dismissal-closure-watch`. | AppFile order 83349531 / case order 16776157, accepted and processed Oct. 26. |
| 12 | `12-hearing-1` Further CMC Dec. 11, 2026, 8:30 a.m., Dept. 11B stays **open**: portal still shows the case Open and the CMC on calendar (likely to be vacated). | eCourt portal, Oct. 28. |

Still open: conformed copies of the M12 dismissal and the M5 Oct. 27/28 submissions; whether the court vacates the M12 Dec. 11 CMC; which proposed judgment (if any) is signed in M5 after the Nov. 2 ex parte.
