# Citation Verification Ledger

Generated 2026-08-09 by `verify-citations.py`. Joins the PR #490 citation index to the July / Matter-28 citation audit, then overlays Round 4+ WebSearch results.

## Why this exists

The campaign is entering a phase where claims are cognizable and motions to dismiss are more likely to be denied. Opposing counsel and the court will scrutinize authority. Locating cites (the index) is not enough — each load-bearing authority must exist and support the proposition claimed.

## Status totals (paired authorities)

| Status | Count |
|---|---|
| UNVERIFIED | 423 |
| VERIFIED | 278 |
| MISCITED | 28 |
| MISCHARACTERIZED | 6 |
| NOT_FOUND | 6 |

**Plaintiff-only + still UNVERIFIED (P0 queue): 0**  
**Plaintiff-only + bad status (P1): 27**

## Method controls

- Positive: Richardson v. McKnight, 521 U.S. 399 (1997) — must be findable
- Negative: In re Leman, 66 Cal.App.5th 200 — must NOT be findable
- Direct CourtListener / case.law / Justia fetches are egress-blocked; statuses rest on WebSearch summaries + primary-source URLs.

## Known fabricated / hard NOT_FOUND — live locations

### In re Leman, 66 Cal.App.5th 200 — 16 hits (12 in plaintiff filings)

_July audit: likely fabricated. Negative control for verification method._

- M9 `/documents/matter-09/31626-43188-NTCHNG_69ce9f1e7ab52 2.pdf` p.52 — other
- M9 `/documents/matter-09/31626-43188-NTCHNG_69ce9f1e7ab52 2.pdf` p.61 — other
- M9 `/documents/matter-09/Amended Notice of Hearing on Petition for Writ of Mandate.pdf` p.53 — plaintiff_filing
- M9 `/documents/matter-09/Amended Notice of Hearing on Petition for Writ of Mandate.pdf` p.62 — plaintiff_filing
- M9 `/documents/matter-09/WOM_Opening Brief.pdf` p.10 — plaintiff_filing
- M9 `/documents/matter-09/WOM_Opening Brief.pdf` p.19 — plaintiff_filing
- M19 `/documents/matter-19/HC-004 Notice and Request for Ruling Packet (with Exhibit A — Unstamped Petition) (Ready to File Aug 7 2026).pdf` p.11 — plaintiff_filing
- M19 `/documents/matter-19/Petition for Writ of Habeas Corpus (filed Apr. 3, 2026).pdf` p.9 — plaintiff_filing
- M9 `/documents/matter-09/31626-43188-NTCHNG_69ce9f1e7ab52 2.pdf` p.52 — other
- M9 `/documents/matter-09/31626-43188-NTCHNG_69ce9f1e7ab52 2.pdf` p.61 — other
- M9 `/documents/matter-09/Amended Notice of Hearing on Petition for Writ of Mandate.pdf` p.53 — plaintiff_filing
- M9 `/documents/matter-09/Amended Notice of Hearing on Petition for Writ of Mandate.pdf` p.62 — plaintiff_filing
- …and 4 more

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

### Burrell v. Jackson, 2003 WL 23545858 — 14 hits (10 in plaintiff filings)

_Round 4: no matching absolute-immunity hearing-officer decision at that WL number._

- M7 `/documents/matter-33/from-07/Objections to FR Newanforbi v Candelaria BOLSTERED 3.pdf` p.4 — plaintiff_filing
- M7 `/documents/matter-33/from-07/Objections to FR Newanforbi v Candelaria BOLSTERED 3.pdf` p.15 — plaintiff_filing
- M33 `/documents/matter-33/ndcal/Complaint Ngwa Nforbi v Candelaria and Gordon NDCal 3 Operative.pdf` p.43 — plaintiff_filing
- M33 `/documents/matter-33/ndcal/Complaint Ngwa Nforbi v Candelaria and Gordon NDCal.pdf` p.43 — plaintiff_filing
- M7 `/documents/matter-33/opinions/Newanforbi v Candelaria - USDC EDCal - FR Recommending Dismissal Jun 15 2026.pdf` p.6 — court_order
- M7 `/documents/matter-33/opinions/Newanforbi v Candelaria - USDC EDCal - FR Recommending Dismissal Jun 15 2026.pdf` p.10 — court_order
- M7 `/documents/matter-33/from-07/Objections to FR Newanforbi v Candelaria BOLSTERED 3.pdf` p.4 — plaintiff_filing
- M33 `/documents/matter-33/ndcal/Complaint Ngwa Nforbi v Candelaria and Gordon NDCal 3 Operative.pdf` p.43 — plaintiff_filing
- M33 `/documents/matter-33/ndcal/Complaint Ngwa Nforbi v Candelaria and Gordon NDCal.pdf` p.43 — plaintiff_filing
- M7 `/documents/matter-33/from-07/Objections to FR Newanforbi v Candelaria BOLSTERED 3.pdf` p.4 — plaintiff_filing
- M33 `/documents/matter-33/ndcal/Complaint Ngwa Nforbi v Candelaria and Gordon NDCal 3 Operative.pdf` p.43 — plaintiff_filing
- M33 `/documents/matter-33/ndcal/Complaint Ngwa Nforbi v Candelaria and Gordon NDCal.pdf` p.43 — plaintiff_filing
- …and 2 more

## P1 — Plaintiff-only authorities with bad audit/round status

| Uses | Status | Authority | Matters |
|---|---|---|---|
| 11 | MISCHARACTERIZED | California Highway Patrol v. Superior Court, 158 Cal.App. 4th 726 (200 | 9, 19 |
| 11 | MISCHARACTERIZED | People v. Rizo, 22 Cal. 4th 681 (2000) | 9, 19 |
| 9 | MISCHARACTERIZED | Pomona Police Officers' Ass'n v. City of Pomona, 58 Cal.App. 4th 578 ( | 9 |
| 8 | NOT_FOUND | In re Leman, 66 Cal.App. 5th 200 (2021) | 9, 19 |
| 6 | MISCITED | Home v. Dep't of Health Care Services, 204 Cal.App. 4th 676 (2012) | 9 |
| 6 | MISCITED | In re Hudson, 1 Cal.App. 4th 1 (2006) | 5, 15, 19 |
| 6 | MISCITED | People v. Superior Court, 25 Cal. 4th 703 (2001) | 9 |
| 6 | MISCHARACTERIZED | Pomona Police Officers’ Ass’n v. City of Pomona, 58 Cal.App. 4th 578 ( | 9 |
| 5 | MISCITED | Rodriguez v. United States, 575 U.S. 348 (2015) | 1, 32 |
| 3 | NOT_FOUND | Burrell v. Jackson, 2003 WL 23545858 | 7, 32, 33 |
| 3 | MISCITED | County of Contra Costa v. State of California, 177 Cal.App. 3d 62 (198 | 9 |
| 3 | MISCITED | Home v. Dep’t of Health Care Services, 204 Cal.App. 4th 676 (2012) | 9 |
| 3 | MISCHARACTERIZED | See California Highway Patrol v. Superior Court, 158 Cal.App. 4th 726  | 9 |
| 2 | MISCITED | California, Ltd. v. Dry Creek Joint Elementary Sch. Dist, 50 Cal.App.  | 20, 32 |
| 2 | MISCITED | Soranno's Gasco, Inc. v. Morgan Hill Unified, 874 F. 2d 1310 | 24, 32 |
| 2 | MISCITED | Swift v. Christian, 384 F. 3d 1184 | 30 |
| 2 | MISCITED | Unicorn Glob., Inc. v. Hillo Am., Inc, 2021 WL 1034838 | 29 |
| 1 | MISCITED | Accurate and Amazon. Los Angeles Cath. Worker v. Los Angeles Downtown  | 29 |
| 1 | MISCITED | Ashcroft v. Iqbal, 556 U.S. 662 | 29 |
| 1 | MISCITED | Cases Ashcroft v. Iqbal, 556 U.S. 662 | 29 |
| 1 | MISCITED | Chubb v. Sullivan, 2014 WL 2807986 | 28 |
| 1 | MISCITED | Jessie v. United States, 79 M.J. 437 | 28 |
| 1 | MISCITED | Lockley v. Law Office, 91 Cal.App. 4th 401 (2001) | 20, 32 |
| 1 | MISCITED | Los Angeles Cath. Worker v. Los Angeles Downtown Indus. Dist. Bus, 201 | 29 |
| 1 | MISCITED | See Johnson v. City of Grants Pass, 50 F. 4th 787 | 28 |
| 1 | MISCITED | See Rodriguez v. United States, 575 U.S. 348 (2015) | 32 |
| 1 | MISCITED | Soranno’s Gasco, Inc. v. Morgan Hill Uniifed Sch. Dist, 874 F. 2d 1310 | 24 |

## P0 — Plaintiff-only UNVERIFIED queue (work this next)

Asserted only in Plaintiff's filings; no court order or opposing brief in the corpus cites them back; not yet joined to an audit/round status.

| Uses | Authority | Matters | Sample page |
|---|---|---|---|

_0 total in JSON `priorityQueue`._

## Round overlay

Loaded round: **2026-08-09 Round 4 — portfolio P0 (batches A–D; LACW WL correction)** — 177 results

Method note: WebSearch against primary-source URLs after positive control (Richardson v. McKnight, 521 U.S. 399 — hit govinfo.gov U.S. Reports PDF) and negative control (In re Leman, 66 Cal.App.5th 200 — no matching decision; only Lemanuel C. / Marriage of Lemen noise). CourtListener/case.law/Justia direct fetches remain egress-blocked. Statuses rest on search-returned summaries plus primary URLs. Characterization flags applied when index sample context attributes a proposition the opinion does not support. Batch D closed the remaining plaintiff-only UNVERIFIED queue.

## Regenerating
```

python3 internal/scripts/verify-citations.py
python3 internal/scripts/verify-citations.py --check
python3 internal/scripts/verify-citations.py --queue
```

## Known-bad debt gate

`--check` fails if a known-fabricated pattern appears in a `plaintiff_filing` location that is **not** listed in `citation_known_bad_debt.json`. Existing filed-document hits are tracked as debt so CI stays green while corrected drafts are prepared; **new** introductions fail the gate.

