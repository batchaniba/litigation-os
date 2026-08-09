# Citation Verification Ledger

Generated 2026-08-09 by `verify-citations.py`. Joins the PR #490 citation index to the July / Matter-28 citation audit, then overlays Round 4+ WebSearch results.

## Why this exists

The campaign is entering a phase where claims are cognizable and motions to dismiss are more likely to be denied. Opposing counsel and the court will scrutinize authority. Locating cites (the index) is not enough — each load-bearing authority must exist and support the proposition claimed.

## Status totals (paired authorities)

| Status | Count |
|---|---|
| UNVERIFIED | 460 |
| VERIFIED | 244 |
| MISCITED | 25 |
| MISCHARACTERIZED | 6 |
| NOT_FOUND | 6 |

**Plaintiff-only + still UNVERIFIED (P0 queue): 37**  
**Plaintiff-only + bad status (P1): 24**

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
| 1 | MISCITED | Ashcroft v. Iqbal, 556 U.S. 662 | 29 |
| 1 | MISCITED | Cases Ashcroft v. Iqbal, 556 U.S. 662 | 29 |
| 1 | MISCITED | Chubb v. Sullivan, 2014 WL 2807986 | 28 |
| 1 | MISCITED | Jessie v. United States, 79 M.J. 437 | 28 |
| 1 | MISCITED | Lockley v. Law Office, 91 Cal.App. 4th 401 (2001) | 20, 32 |
| 1 | MISCITED | See Johnson v. City of Grants Pass, 50 F. 4th 787 | 28 |
| 1 | MISCITED | See Rodriguez v. United States, 575 U.S. 348 (2015) | 32 |
| 1 | MISCITED | Soranno’s Gasco, Inc. v. Morgan Hill Uniifed Sch. Dist, 874 F. 2d 1310 | 24 |

## P0 — Plaintiff-only UNVERIFIED queue (work this next)

Asserted only in Plaintiff's filings; no court order or opposing brief in the corpus cites them back; not yet joined to an audit/round status.

| Uses | Authority | Matters | Sample page |
|---|---|---|---|
| 2 | Pearson v. Callahan, 555 U.S. 223 (2009) | 1, 32 | p.3 |
| 2 | People v. Woodell, 17 Cal. 4th 448 (1998) | 5 | p.3 |
| 2 | Ross v. Creel Printing, 100 Cal.App. 4th 736 (2002) | 5 | p.5 |
| 2 | SN Sands Corp. v. City and County, 167 Cal.App. 4th 185 (2008) | 20, 32 | p.8 |
| 2 | See Saleeby v. State Bar, 39 Cal. 3d 547 (1985) | 20, 32 | p.8 |
| 2 | Sonner v. Premier Nutrition Corporation, 49 F. 4th 1300 (2022) | 29 | p.3 |
| 2 | Sugar Co-op v. Archer-Daniels-Midland Co, 2012 WL 3101659 | 29 | p.3 |
| 2 | Under United States v. Knights, 534 U.S. 112 (2001) | 19 | p.15 |
| 2 | Unicorn Glob., Inc. v. Hillo Am., Inc, 2021 WL 1034838 | 29 | p.3 |
| 1 | Accurate and Amazon. Los Angeles Cath. Worker v. Los Angeles Downtown  | 29 | p.18 |
| 1 | Bd. of Educ. v. Doyle, 429 U.S. 274 (1977) | 30 | p.11 |
| 1 | Bill Johnson's Restaurants, Inc. v. NLRB, 461 U.S. 731 (1983) | 30 | p.15 |
| 1 | Bolkiah v. Superior Ct, 74 Cal. App. 4th 984 (1999) | 3 | p.2 |
| 1 | California DUI Lawyers Ass'n v. Department of Motor Vehicles, 77 Cal.  | 7, 32, 33 | p.4 |
| 1 | California Motor Transport Co. v. Trucking Unlimited, 404 U.S. 508 (19 | 30 | p.16 |
| 1 | California v. Acevedo, 500 U.S. 565 (1991) | 32 | p.20 |
| 1 | California v. Carney, 471 U.S. 386 (1985) | 32 | p.19 |
| 1 | E. & J. Gallo Winery v. Encana Energy Servs., Inc, 2005 WL 2435900 | 29 | p.4 |
| 1 | Griffin v. Green Tree Servicing, LLC, 166 F. Supp. 3d 1030 | 29 | p.5 |
| 1 | Helm v. Alderwoods Group, Inc, 696 F. Supp. 2d 1057 | 29 | p.4 |
| 1 | Herr v. Nestle U.S.A., Inc, 109 Cal.App. 4th 779 | 29 | p.23 |
| 1 | Jones v. Sutter Health, 499 F. Supp. 3d 704 | 29 | p.2 |
| 1 | L'Garde, Inc. v. Raytheon Space, 805 F. Supp. 2d 932 | 29 | p.11 |
| 1 | Los Angeles Cath. Worker v. Los Angeles Downtown Indus. Dist. Bus, 201 | 29 | p.3 |
| 1 | MGIC Indem. Corp. v. Weisman, 803 F. 2d 500 | 29 | p.4 |
| 1 | Mack v. South Bay Beer Distribs, 798 F. 2d 1279 | 29 | p.2 |
| 1 | Milhouse v. Carlson, 652 F. 2d 371 | 30 | p.6 |
| 1 | Mir v. Little Co, 844 F. 2d 646 | 29 | p.4 |
| 1 | Moser v. Benefytt, Inc, 8 F. 4th 872 | 3 | p.3 |
| 1 | Neilson v. Union Bank, 290 F. Supp. 2d 1101 | 29 | p.4 |
| 1 | Taylor v. Sturgell, 553 U.S. 880 (2008) | 7, 32, 33 | p.14 |
| 1 | United States Small Bus. Admin. v. Bensal, 853 F. 3d 992 | 29 | p.4 |
| 1 | United States v. Reyna-Tapia, 328 F. 3d 1114 | 7, 32, 33 | p.1 |
| 1 | United States v. Wilson, 631 F. 2d 118 | 29 | p.4 |
| 1 | Villiarimo v. Aloha Island Air, Inc, 281 F. 3d 1054 | 30 | p.11 |
| 1 | Weston v. Motiu, 2025 WL 2916303 | 3 | p.3 |
| 1 | Zahrey v. Coffey, 221 F. 3d 342 | 30 | p.18 |

_37 total in JSON `priorityQueue`._

## Round overlay

Loaded round: **2026-08-09 Round 4 — portfolio P0 (batches A–C; continuing)** — 140 results

Method note: WebSearch against primary-source URLs after positive control (Richardson v. McKnight, 521 U.S. 399 — hit govinfo.gov U.S. Reports PDF) and negative control (In re Leman, 66 Cal.App.5th 200 — no matching decision; only Lemanuel C. / Marriage of Lemen noise). CourtListener/case.law/Justia direct fetches remain egress-blocked. Statuses rest on search-returned summaries plus primary URLs. Characterization flags applied when index sample context attributes a proposition the opinion does not support.

## Regenerating
```

python3 internal/scripts/verify-citations.py
python3 internal/scripts/verify-citations.py --check
python3 internal/scripts/verify-citations.py --queue
```

## Known-bad debt gate

`--check` fails if a known-fabricated pattern appears in a `plaintiff_filing` location that is **not** listed in `citation_known_bad_debt.json`. Existing filed-document hits are tracked as debt so CI stays green while corrected drafts are prepared; **new** introductions fail the gate.

