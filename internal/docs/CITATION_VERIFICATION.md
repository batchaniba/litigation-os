# Citation Verification Ledger

Generated 2026-09-09 by `verify-citations.py`. Joins the PR #490 citation index to the July / Matter-28 citation audit, then overlays Round 4+ verification results (WebSearch + CourtListener/CAP multisource confirmation).

## Why this exists

The campaign is entering a phase where claims are cognizable and motions to dismiss are more likely to be denied. Opposing counsel and the court will scrutinize authority. Locating cites (the index) is not enough — each load-bearing authority must exist and support the proposition claimed.

## Status totals (paired authorities)

| Status | Count |
|---|---|
| UNVERIFIED | 485 |
| VERIFIED | 460 |
| MISCITED | 30 |
| MISCHARACTERIZED | 6 |
| NOT_FOUND | 6 |

**Plaintiff-only + still UNVERIFIED (P0 queue): 8**  
**Plaintiff-only + bad status (P1): 30**

## Method controls

- Positive: Richardson v. McKnight, 521 U.S. 399 (1997) — must be findable
- Negative: In re Leman, 66 Cal.App.5th 200 — must NOT be findable
- Multi-source reachability (this environment):
  - `courtlistener_search`: ok (unauthenticated /api/rest/v4/search/)
  - `case_law_api`: html docs only — JSON API not usable without auth/migration
  - `case_law_static`: ok (CasesMetadata.json + html/{file_name}.html)
  - `justia`: blocked (Cloudflare 403) in this environment
  - `google_scholar`: unreliable (often 403)
  - `courtlistener_citation_lookup`: requires API token (401)
- Confirmation artifact: `citation_lookup_multisource.json` (1 probes on 2026-08-16).
- Matter 28 funnel: `citation_lookup_matter28.json` (54 probes on 2026-08-09).

## Known fabricated / hard NOT_FOUND — live locations

### In re Leman, 66 Cal.App.5th 200 — 18 hits (14 in plaintiff filings)

_July audit: likely fabricated. Negative control for verification method._

- M19 `/documents/matter-19/HC-004 Notice and Request for Ruling Packet (with Exhibit A — Unstamped Petition) (Ready to File Aug 17 2026).pdf` p.11 — plaintiff_filing
- M19 `/documents/matter-19/HC-004 Notice and Request for Ruling Packet (with Exhibit A — Unstamped Petition) (Ready to File Aug 7 2026).pdf` p.11 — plaintiff_filing
- M19 `/documents/matter-19/Petition for Writ of Habeas Corpus (filed Apr. 3, 2026).pdf` p.9 — plaintiff_filing
- M9 `/documents/matter-09/31626-43188-NTCHNG_69ce9f1e7ab52 2.pdf` p.52 — other
- M9 `/documents/matter-09/31626-43188-NTCHNG_69ce9f1e7ab52 2.pdf` p.61 — other
- M9 `/documents/matter-09/Amended Notice of Hearing on Petition for Writ of Mandate.pdf` p.53 — plaintiff_filing
- M9 `/documents/matter-09/Amended Notice of Hearing on Petition for Writ of Mandate.pdf` p.62 — plaintiff_filing
- M9 `/documents/matter-09/WOM_Opening Brief.pdf` p.10 — plaintiff_filing
- M9 `/documents/matter-09/WOM_Opening Brief.pdf` p.19 — plaintiff_filing
- M19 `/documents/matter-19/HC-004 Notice and Request for Ruling Packet (with Exhibit A — Unstamped Petition) (Ready to File Aug 17 2026).pdf` p.11 — plaintiff_filing
- M19 `/documents/matter-19/HC-004 Notice and Request for Ruling Packet (with Exhibit A — Unstamped Petition) (Ready to File Aug 7 2026).pdf` p.11 — plaintiff_filing
- M19 `/documents/matter-19/Petition for Writ of Habeas Corpus (filed Apr. 3, 2026).pdf` p.9 — plaintiff_filing
- …and 6 more

### Friends of the Trinity River, 184 Cal.App.4th 1466 — 2 hits (0 in plaintiff filings)

_July audit: likely fabricated (Matter 14)._

- M14 `/documents/matter-14/Newanforbi v Urrea.pdf` p.14 — other
- M14 `/documents/matter-14/Newanforbi v Urrea.pdf` p.14 — other

### Dunford v. Rovi Corp., 2015 WL 13752958 — 9 hits (0 in plaintiff filings)

_Matter 28 Round 3: no such decision; Netflix v. Rovi is the real N.D. Cal. 2015 Rovi case._

- M28 `/documents/matter-28/Motion Protective Order NDCA.pdf` p.5 — court_order
- M28 `/documents/matter-28/Motion Protective Order NDCA.pdf` p.6 — court_order
- M28 `/documents/matter-28/Proposed Protective Order NDCA.pdf` p.2 — court_order
- M28 `/documents/matter-28/Motion Protective Order NDCA.pdf` p.5 — court_order
- M28 `/documents/matter-28/Proposed Protective Order NDCA.pdf` p.2 — court_order
- M28 `/documents/matter-28/Motion Protective Order NDCA.pdf` p.5 — court_order
- M28 `/documents/matter-28/Proposed Protective Order NDCA.pdf` p.2 — court_order
- M28 `/documents/matter-28/Motion Protective Order NDCA.pdf` p.6 — court_order
- M28 `/documents/matter-28/Motion Protective Order NDCA.pdf` p.6 — court_order

### Collins v. Moore, 81 F.3d 167 — 2 hits (0 in plaintiff filings)

_Matter 28 Round 3: table page hosts unrelated dispositions._

- M28 `/documents/matter-28/research/Research Note - Strongest Clearly Established Right to Invoke.pdf` p.16 — other
- M28 `/documents/matter-28/research/Research Note - Strongest Clearly Established Right to Invoke.pdf` p.16 — other

### Burrell v. Jackson, 2003 WL 23545858 — 18 hits (14 in plaintiff filings)

_Round 4: no matching absolute-immunity hearing-officer decision at that WL number._

- M7 `/documents/matter-33/from-07/Objections to FR Newanforbi v Candelaria BOLSTERED 3.pdf` p.4 — plaintiff_filing
- M7 `/documents/matter-33/from-07/Objections to FR Newanforbi v Candelaria BOLSTERED 3.pdf` p.15 — plaintiff_filing
- M33 `/documents/matter-33/ndcal/Complaint Ngwa Nforbi v Candelaria and Gordon NDCal 3 Operative.pdf` p.43 — plaintiff_filing
- M33 `/documents/matter-33/ndcal/Complaint Ngwa Nforbi v Candelaria and Gordon NDCal.pdf` p.43 — plaintiff_filing
- M33 `/documents/matter-33/ndcal/Dkt 01 - Complaint (CONFORMED, Filed Aug 10 2026).pdf` p.43 — plaintiff_filing
- M7 `/documents/matter-33/opinions/Newanforbi v Candelaria - USDC EDCal - FR Recommending Dismissal Jun 15 2026.pdf` p.6 — court_order
- M7 `/documents/matter-33/opinions/Newanforbi v Candelaria - USDC EDCal - FR Recommending Dismissal Jun 15 2026.pdf` p.10 — court_order
- M7 `/documents/matter-33/from-07/Objections to FR Newanforbi v Candelaria BOLSTERED 3.pdf` p.4 — plaintiff_filing
- M33 `/documents/matter-33/ndcal/Complaint Ngwa Nforbi v Candelaria and Gordon NDCal 3 Operative.pdf` p.43 — plaintiff_filing
- M33 `/documents/matter-33/ndcal/Complaint Ngwa Nforbi v Candelaria and Gordon NDCal.pdf` p.43 — plaintiff_filing
- M33 `/documents/matter-33/ndcal/Dkt 01 - Complaint (CONFORMED, Filed Aug 10 2026).pdf` p.43 — plaintiff_filing
- M33 `/documents/matter-33/ndcal/Notice Identifying Operative First Amended Complaint (Candelaria) (Aug 24 2026).pdf` p.1 — plaintiff_filing
- …and 6 more

## P1 — Plaintiff-only authorities with bad audit/round status

| Uses | Status | Authority | Matters |
|---|---|---|---|
| 12 | MISCHARACTERIZED | California Highway Patrol v. Superior Court, 158 Cal.App. 4th 726 (200 | 9, 19 |
| 12 | MISCHARACTERIZED | People v. Rizo, 22 Cal. 4th 681 (2000) | 9, 19 |
| 9 | NOT_FOUND | In re Leman, 66 Cal.App. 5th 200 (2021) | 9, 19 |
| 9 | MISCHARACTERIZED | Pomona Police Officers' Ass'n v. City of Pomona, 58 Cal.App. 4th 578 ( | 9 |
| 9 | MISCITED | Rodriguez v. United States, 575 U.S. 348 (2015) | 1, 32 |
| 7 | MISCITED | In re Hudson, 1 Cal.App. 4th 1 (2006) | 5, 15, 19 |
| 6 | MISCITED | Home v. Dep't of Health Care Services, 204 Cal.App. 4th 676 (2012) | 9 |
| 6 | MISCITED | People v. Superior Court, 25 Cal. 4th 703 (2001) | 9 |
| 6 | MISCHARACTERIZED | Pomona Police Officers’ Ass’n v. City of Pomona, 58 Cal.App. 4th 578 ( | 9 |
| 5 | MISCITED | Caldwell v. Montoya, 10 Cal. 4th 972 (1995) | 14, 15, 16 |
| 5 | MISCITED | Devenpeck v. Alford, 543 U.S. 11 (2004) | 32 |
| 4 | NOT_FOUND | Burrell v. Jackson, 2003 WL 23545858 | 7, 32, 33 |
| 3 | MISCITED | County of Contra Costa v. State of California, 177 Cal.App. 3d 62 (198 | 9 |
| 3 | MISCITED | Home v. Dep’t of Health Care Services, 204 Cal.App. 4th 676 (2012) | 9 |
| 3 | MISCHARACTERIZED | See California Highway Patrol v. Superior Court, 158 Cal.App. 4th 726  | 9 |
| 3 | MISCITED | See Rodriguez v. United States, 575 U.S. 348 (2015) | 32 |
| 2 | MISCITED | California, Ltd. v. Dry Creek Joint Elementary Sch. Dist, 50 Cal.App.  | 20, 32 |
| 2 | MISCITED | Devenpeck v. Alford, 3 U.S. 146 (2004) | 32 |
| 2 | MISCITED | Soranno's Gasco, Inc. v. Morgan Hill Unified, 874 F. 2d 1310 | 24, 32 |
| 2 | MISCITED | Swift v. Christian, 384 F. 3d 1184 | 30 |
| 2 | MISCITED | Unicorn Glob., Inc. v. Hillo Am., Inc, 2021 WL 1034838 | 29 |
| 1 | MISCITED | Accurate and Amazon. Los Angeles Cath. Worker v. Los Angeles Downtown  | 29 |
| 1 | MISCITED | Ashcroft v. Iqbals, 556 U.S. 662 (2009) | 33 |
| 1 | MISCITED | Cases Ashcroft v. Iqbal, 556 U.S. 662 | 29 |
| 1 | MISCITED | Chubb v. Sullivan, 2014 WL 2807986 | 28 |
| 1 | MISCITED | Jessie v. United States, 79 M.J. 437 | 28 |
| 1 | MISCITED | Lockley v. Law Office, 91 Cal.App. 4th 401 (2001) | 20, 32 |
| 1 | MISCITED | Los Angeles Cath. Worker v. Los Angeles Downtown Indus. Dist. Bus, 201 | 29 |
| 1 | MISCITED | See Johnson v. City of Grants Pass, 50 F. 4th 787 | 28 |
| 1 | MISCITED | Soranno’s Gasco, Inc. v. Morgan Hill Uniifed Sch. Dist, 874 F. 2d 1310 | 24 |

## P0 — Plaintiff-only UNVERIFIED queue (work this next)

Asserted only in Plaintiff's filings; no court order or opposing brief in the corpus cites them back; not yet joined to an audit/round status.

| Uses | Authority | Matters | Sample page |
|---|---|---|---|
| 5 | Benavidez v. County of San Diego, 993 F. 3d 9 | 32 | p.13 |
| 3 | Dart Cherokee Basin Operating Co., LLC v. Owens, 574 U.S. 81 | 26 | p.3 |
| 3 | Ruelaz v. Leprino Foods Co, 2025 WL 25549 | 26 | p.4 |
| 1 | Davenport v. Mutual Ben. Health, 325 F. 3d 785 | 25 | p.8 |
| 1 | Hernandez v. Regents of, 2009 WL 6045700 (2009) | 25 | p.10 |
| 1 | In Aucina v. Amoco Oil Co, 871 F. Supp. 332 | 25 | p.13 |
| 1 | Villa v. Maricopa County, 865 F. 3d 8 | 33 | p.38 |
| 1 | Weyhe v. Wal-Mart Stores, Inc, 2010 WL 3411462 | 25 | p.10 |

_8 total in JSON `priorityQueue`._

## Round overlay

Loaded round: **2026-08-09 Round 4 — portfolio P0 (batches A–D; LACW WL correction); Round 5 multisource (CourtListener + CAP); Round 5b Matter 28 full funnel; Round 6 spot-check of the Matter 33 conformed complaint (3:26-cv-08272-LJC, Dkt. 1) page-43 immunity sentence; Round 7 authorities cited in the Serrato IFP screening order (Matter 24, Dkt. 5) after OCR made that scan searchable; Round 8 — OCR tranche (16 plaintiff filings + court orders: Matters 5/12/15/25/26/33, Barocio opinion); Round 9 — Matter 24 Serrato Opp v4 final citation/quotation verification pass (2026-08-27); Round 10 — Matter 26 hybrid UPS MTD opposition (Claude structure + Cursor caution), 2026-08-28; Round 11 — P0 plaintiff-only queue after OCR-alias index rebuild (Matters 25/26/32/33 plus remaining portfolio P0), 2026-09-06** — 366 results

Method note: Round 4: WebSearch after Richardson(+) / Leman(−) controls. Round 5: CourtListener /api/rest/v4/search/ + CAP static.case.law for controls/high-risk. Round 5b: all Matter 28 indexed authorities through lookup-citations.py --matter 28 (→ citation_lookup_matter28.json). Justia Cloudflare-blocked; Scholar unreliable; api.case.law JSON and CL citation-lookup need auth. Existence FOUND does not clear prior MISCHARACTERIZED/MISCITED proposition problems. Table-page F.3d pins can host multiple dispositions — do not treat first CL hit as unique. Round 7: the June 29, 2026 Serrato IFP/screening order was an image-only scan contributing nothing to the index until internal/scripts/ocr-text-layer.py added a text layer; its authorities were then probed through lookup-citations.py (→ citation_lookup_serrato_order.json) behind the same Richardson(+) / Leman(−) controls. These are a court's own citations, so they carry role court_order and never enter the plaintiff-only P0/P1 queues. Round 8: after ocr-text-layer.py on the 16-document plaintiff_filing/court_order tranche, probed new P0 Matter 12/15 authorities (citation_lookup_matter12_p0.json) and Barocio screening-order authorities (citation_lookup_barocio_order.json). McCorkle manually confirmed on CourtListener when CAP lacked cal2d/70. Round 9: Matter 24 Opposition v4 — npm citations:index + citations:lookup:matter --matter 24 (→ citation_lookup_matter24.json); quote needles checked against CAP static.case.law HTML (Whittlestone/Lopez/Noll/Perry/Twombly/Iqbal/Wade/Knievel/Erickson/Ford) and CA9 PDF (Capp); fixed Garity miscitation, Whittlestone non-opinion paraphrase, Perry/Twombly wording, and removed unused Lewis/Shanks TOA entries; Bureerong manually FOUND on CL+CAP. Round 10: Matter 26 hybrid opposition — npm citations:index + citations:lookup:matter --matter 26 (→ citation_lookup_matter26.json); Cal. App. 5th pins for Williams (40 Cal. App. 5th 280) and Quinn (121 Cal. App. 5th 1124) confirmed by direct CourtListener search when the reporter probe missed (CAP static lacks those volumes). Mendoza quotes checked against the published opinion (anti-SLAPP; 1658-59). Cel-Tech 183 quote is UPS's own. Round 11: build-citation-index.py OCR_PAGE_FIXES (Califomia/DUl/MedinOy/TorreSy/Knudsen/Devenpeck 3 U.S.→543 U.S. etc.) dropped P0 70→54; lookup-citations.py → citation_lookup_p0.json (FOUND 28, CAPTION_MISMATCH 14, PARTIAL 3, NOT_FOUND 7, UNKNOWN 2); overlay-citation-lookups.py folded FOUND + same-case OCR mismatches + Gonzalez/Hertz PARTIAL into VERIFIED (existence only) and marked both Devenpeck mispins MISCITED (real case is 543 U.S. 146). NOT_FOUND/UNKNOWN left UNVERIFIED (a miss is not a fabrication). Controls were not re-probed this pass.

## Regenerating
```

python3 internal/scripts/verify-citations.py
python3 internal/scripts/verify-citations.py --check
python3 internal/scripts/verify-citations.py --queue
python3 internal/scripts/lookup-citations.py --batch all
python3 internal/scripts/lookup-citations.py --matter 28
```

## Known-bad debt gate

`--check` fails if a known-fabricated pattern appears in a `plaintiff_filing` location that is **not** listed in `citation_known_bad_debt.json`. Existing filed-document hits are tracked as debt so CI stays green while corrected drafts are prepared; **new** introductions fail the gate.

