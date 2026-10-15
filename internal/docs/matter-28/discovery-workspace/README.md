# Matter 28 — Discovery Workspace (Newanforbi v. Smith / HOPE)

Entry point for models and agents doing discovery planning and service in Matter 28.
Built 2026-10-14 (PT). Live calendar truth stays in
[`internal/src/data/matters/28/clocks.json`](../../../src/data/matters/28/clocks.json);
this file is a projection (do not treat dates here as clocks).

**Confidentiality:** the 12 HOPE discovery documents (Bates HOPE_000001–542) are
CONFIDENTIAL under the San Joaquin protective order and are on the owner denylist
(`internal/src/data/documents/private-documents.json`). Their originals and OCR text live
only under `internal/private/documents/matter-05/hope-discovery/`. Never copy them, their
text, or quotations from them into `documents/`, `internal/public/`, the SPA, D1/R2 public
paths, or anything filed/sent without checking the protective order. This workspace
indexes them by Bates range and title only.

Files here:

| File | What |
|---|---|
| `README.md` | This index: caption, parties, posture, dates, document table |
| [`DISCOVERY_PLAN.md`](DISCOVERY_PLAN.md) | Claims → facts → evidence held/needed → candidate RFP/ROG/RFA/subpoena scaffold; timing gates |
| [`ANALYSIS.md`](ANALYSIS.md) | Verified analysis of the production, the broader record, governing law, and unfinished Matter 5 discovery |
| [`NEXT_MOVES.md`](NEXT_MOVES.md) | Ranked actions, first-wave scope, CMC asks, sequencing, and guardrails |
| [`manifest.json`](manifest.json) | Machine-readable list of every file referenced, with metadata and sha256 |
| `incoming-2026-10-14/` | Oct 14 courtesy copies from Sims Lawrence (Dkt 30 reply set; proposed stipulated PO + COS), PDF + `.txt` |

## Case identity

| Field | Value | Source |
|---|---|---|
| Caption | *Brendan Ngehsi Newanforbi v. Shannon Smith, LCSW, et al.* | Dkt 29; `matter.json` |
| Court | U.S. District Court, N.D. Cal. (San Francisco Division) | Proposed PO caption |
| Case No. | 3:26-cv-07504-LJC | `matter.json` |
| Judge | Hon. Lisa J. Cisneros (Magistrate Judge; Courtroom G) | `matter.json`; Dkt 29 |
| Filed | July 20, 2026 (complaint docketed July 21) | `matter.json` |
| Plaintiff | Brendan Ngehsi Newanforbi, self-represented | caption |
| Defendants | Shannon Smith, LCSW (CEO/founder, individually); HOPE Program, a Licensed Clinical Social Worker Professional Corporation (sued as HOPE Psychotherapy, Inc., d/b/a HOPE Program), 1245 B Street, Hayward, CA 94541 | `parties.json`; PO caption |
| Defense counsel | Sims, Lawrence & Broghammer, 1478 Stone Point Dr. #450, Roseville, CA 95661 — Cynthia G. Lawrence, Blaze Van Dine, Eric T. Martinez; staff Kim Schmitt, Amber Krausse, June Meinecke | PO caption; `parties.json` serviceList |
| Service address | Must include `slb-eservice@sims-law.net`. `SLB@sims-law.net` bounced 550 on Oct 14, 2026 — do not use | SLB signature; `parties.json` |
| Insurance | Philadelphia Indemnity Policy No. 067968 ($1M / $5M) | `matter.json` |

## Claims (all live per `claims.json`)

1. 42 U.S.C. § 1983 — Monell (HOPE)
2. 42 U.S.C. § 1983 — individual capacity (Shannon Smith)
3. Bane Act, Cal. Civ. Code § 52.1
4. Fraud / negligent misrepresentation
5. RICO, 18 U.S.C. § 1962(c)–(d)

## Procedural posture (as of Oct 14, 2026)

- Dkt 15 Rule 12(b)(6) motion to dismiss (with 15-1 RFJN, 15-2 proposed order) filed Sep 21, 2026.
- Plaintiff's opposition served by email Sep 22, 2026 (unstamped copy in repo; no ECF no. ingested).
- **Dkt 30 Reply, 30-1 RFJN, 30-2 COS filed Oct 13, 2026**; courtesy copies emailed Oct 14 (in `incoming-2026-10-14/`). Satisfies the `28-deadline-mtd-reply` clock (still `open` in clocks.json — needs updating; not changed here).
- Dkt 28 Joint CMS filed Oct 5, 2026. Rule 26(f) conference held Sep 29, 2026 (Dkt 28 p.4).
- Dkt 29 (Oct 8) continued the initial CMC to **Oct 27, 2026, 10:30 a.m. PT, Courtroom G**, with the MTD hearing.
- **[Proposed] Stipulated Protective Order** (N.D. Cal. model + pro se "Receiving Party" language in § 2.14, § 13 revision, "IT IS SO STIPULATED", court signature block) signed by Plaintiff Oct 13 (5:38 p.m. PT) and **filed by SLB the morning of Oct 14, 2026**; Word version sent to `ljcpo@cand.uscourts.gov`. **Not yet entered** as of this build. ECF number not known.
- Plaintiff's Rule 26(a)(1) initial disclosures signed and served Oct 14, 2026. Defendants said they would serve theirs by Oct 15 but **withhold confidential material until a protective order is entered** (Martinez email, Oct 13, 2026).

## Key dates (projection — clocks.json controls)

| Date | Event | Status / source |
|---|---|---|
| 2026-09-29 | Rule 26(f) conference held | Dkt 28 |
| 2026-10-13 | Defendants' MTD reply due | Filed (Dkt 30); clock still `open` in repo |
| 2026-10-14 | Plaintiff's initial disclosures served; proposed stip. PO filed | Gmail; repo PDF |
| 2026-10-15 | Defendants' initial disclosures due | Dkt 28; Martinez email |
| **2026-10-27 10:30 PT** | **Initial CMC + Dkt 15 MTD hearing**, Courtroom G | clock `28-hearing-mtd` (open) |
| 2026-11-13 | "Prior Discovery Re-Production or Authorization: Completed by" | **Plaintiff's *proposed* schedule in Dkt 28 (p.6) only. Not a court-ordered date and NOT in clocks.json.** |
| 2027-01-29 / 2027-06-14 | Plaintiff-proposed fact-discovery cutoff / trial | Dkt 28 (proposal) |
| 2027-05-01 / 2028-07-10 | Defendant-proposed fact-discovery cutoff / trial | Dkt 28 (proposal) |

## The 12 discovery documents (HOPE Bates production, HOPE_000001–542)

Produced by HOPE in the San Joaquin case *Newanforbi v. Palacios et al.*, STK-CV-UF-2026-0001032
(Matter 5, demurrer sustained July 15, 2026), stamped CONFIDENTIAL. Plaintiff's Oct 14 initial
disclosures list them as the set he will produce in this action after a protective order
authorizes it. Originals: `internal/private/documents/matter-05/hope-discovery/`; OCR text
(tesseract; scans have no text layer): `.../hope-discovery/text/`.

| # | Bates | Pages | Title | Type |
|---|---|---|---|---|
| 1 | HOPE_000001–031 | 31 | Professional Liability Policy (PHCP067968-15, redacted) | insurance policy |
| 2 | HOPE_000032–104 | 73 | D&O / EPL Policy (PHSD1838240-007, redacted) | insurance policy |
| 3 | HOPE_000105–138 | 34 | Block 1 Homework | client treatment record (Plaintiff) |
| 4 | HOPE_000139–199 | 61 | Collateral Notes and Communications | client record / communications |
| 5 | HOPE_000200–223 | 24 | Homework and Preparatory Tickets | client treatment record (Plaintiff) |
| 6 | HOPE_000224 | 1 | Curriculum Tracking Audit (homework audit) | internal audit |
| 7 | HOPE_000225–314 | 90 | Clinical Operational Manual (9.24.24), Part 1 | policy manual |
| 8 | HOPE_000315–349 | 35 | Clinical Operational Manual, Part 2 | policy manual |
| 9 | HOPE_000350–434 | 85 | Maintenance Curriculum | curriculum |
| 10 | HOPE_000435–485 | 51 | Program Employee Handbook 2023 | HR policy |
| 11 | HOPE_000486–537 | 52 | Proprietary/Preparatory Treatment Manual (2.18.2019) | treatment manual |
| 12 | HOPE_000538–542 | 5 | Clinical Director Job Description | HR document |

Duplicates kept by repo policy (do not collapse; see `internal/private/documents/README.md`):
a second Maintenance Curriculum byte copy (`.root-ffcab3eb`) and a second Clinical Director
copy (`.upload-8ae28190`). The Matter 28 `documents.json` also lists the same 12 under
`/documents/matter-28/HOPE Discovery (Matter 5)/` (denylisted prefix, R2-only).

## Pleadings, motions, orders, disclosures, correspondence (pointers)

Paths are repo-relative. `R2` = bytes only in the R2 store (fetch by `/documents/...` path or `npm run docs:fetch`); not in git.

| Date | Document | Path | Type | Author |
|---|---|---|---|---|
| 2026-07-20 | Complaint (as filed, served on SLB Jul 22) | `/documents/matter-28/Complaint_Newanforbi_v_Smith_NDCA (as filed, served on SLB Jul 22 2026).pdf` (R2) | pleading (operative) | Plaintiff |
| 2026-07-20 | Motion for Protective Order + Decl. + Ex. A + Proposed PO | `/documents/matter-28/Motion Protective Order NDCA.pdf`; `Declaration ISO Motion PO NDCA and Exhibit A (combined, as filed).pdf`; `Proposed Protective Order NDCA.pdf` (R2) | motion | Plaintiff |
| 2026-07-23 | IFP / PO order | `/documents/opinions/Newanforbi v Smith - USDC NDCal - IFP PO Order Jul 23 2026.pdf` (R2) | order | Court |
| 2026-08-26 | Dkt 11 Order re Filing Fee/IFP, Directing Service | [`documents/matter-28/Dkt 11 - ...`](../../../../documents/matter-28/) | order | Court |
| 2026-09-03 | Dkt 13 POS of Rule 4 packet on SLB | `documents/matter-28/Dkt 13 - Proof of Service of Rule 4 Packet on SLB (Filed Sep 3 2026).pdf` | proof of service | Plaintiff |
| 2026-09-21 | Dkt 15 MTD; 15-1 RFJN; 15-2 proposed order | `documents/matter-28/Dkt 15*.pdf` | motion | Defendants |
| 2026-09-22 | Plaintiff's Opposition to MTD (served) | `/documents/matter-28/Plaintiff's Opposition ... (Served Sep 22 2026).pdf`; text: `internal/public/documents/matter-28/Plaintiff's Opposition ... .txt` | opposition | Plaintiff |
| 2026-10-05 | Dkt 28 Joint Case Management Statement | `documents/matter-28/Dkt 28 - Joint Case Management Statement (Filed Oct 5 2026).pdf` | CMS | Joint |
| 2026-10-08 | Dkt 29 Order Continuing CMC | `documents/matter-28/Dkt 29 - Order Continuing Case Management Conference (Filed Oct 8 2026).pdf` | order | Court |
| 2026-10-13 | Dkt 30 Reply ISO MTD; 30-1 RFJN; 30-2 COS | [`incoming-2026-10-14/`](incoming-2026-10-14/) | reply | Defendants |
| 2026-10-14 | [Proposed] Stipulated Protective Order (as filed) + COS | [`incoming-2026-10-14/`](incoming-2026-10-14/) | proposed order | Joint (SLB filed) |
| 2026-10-14 | Plaintiff's Rule 26(a)(1) Initial Disclosures (signed, served) | `documents/matter-28/Plaintiff's Rule 26(a)(1) Initial Disclosures - Nforbi v Smith 3-26-cv-07504-LJC (Signed, Served Oct 14 2026).pdf` | disclosures | Plaintiff |
| 2026-10-14 | Initial disclosures review draft (unsigned) | `internal/docs/matter-28/Plaintiff's Initial Disclosures ... (REVIEW DRAFT, unsigned).pdf` | draft | Plaintiff |
| 2026-06 | Palacios-case stipulated PO correspondence | `/documents/matter-28/Gmail - Re Contains JavaScript Re Newanforbi v Palacios re Stipulated Protective Order (Jun 2026).pdf` (R2) | correspondence | SLB / Plaintiff |
| 2026-09 | Meet-and-confer re MTD (Van Dine) | `/documents/matter-28/Gmail - Newanforbi v HOPE re Meet and Confer 3-26-cv-07504 (Sep 3-6 2026).pdf` (R2) | correspondence | SLB / Plaintiff |

Full inventory: [`internal/src/data/matters/28/documents.json`](../../../src/data/matters/28/documents.json) (86 rows).
Research memos (QI, CASOMB, Title 15 § 3574): `/documents/matter-28/research/`.

## Related matters (only those the repo links to Shannon)

- **Matter 5** — *Newanforbi v. Palacios et al.*, San Joaquin STK-CV-UF-2026-0001032 (disposed on demurrer July 15, 2026). Source of the HOPE_000001–542 production and the RFA/SROG responses relied on in `matter.json` (HOPE RFA 4, 18; Palacios RFA 6, 8; SROG 11, 14). Discovery responses: `internal/public/documents/matter-05/HOPE_resp_plntf_{RFP1,FROGS1,SROGS1}_*.pdf`.

## Gaps found while building this

- No clock in `clocks.json` for Nov 13, 2026; it exists only as Plaintiff's proposed date in Dkt 28.
- `28-deadline-mtd-reply` still `open`; Dkt 30 shows the reply was filed Oct 13.
- Proposed stip. PO filing has no ECF number in the repo; entry status unknown.
- Defendants' initial disclosures (due Oct 15) not yet received/ingested.
- Docket entries 16–27 are not catalogued in the repo (Dkt 22 and 23 are referenced in Dkt 29 / Dkt 30).

## Analysis pass (2026-10-14)

- [`ANALYSIS.md`](ANALYSIS.md): production analysis by Bates range and claim; Title 15 § 3574 decision framework; Matter 5 continuation map; precedent; and a ranked discovery plan.
- [`NEXT_MOVES.md`](NEXT_MOVES.md): concrete actions from the October 15 disclosure review through the October 27 CMC and the first response cycle.
- The analysis treats the San Joaquin requests and responses as leads, not portable federal admissions.
- It recommends a narrow first wave focused on the challenged decisions, native event communications, audit trails, transmissions, and the corresponding CDCR/DAPO records.
- No discovery request, subpoena, letter, filing, or communication was created, served, or sent in this pass.
- The San Joaquin protective order does not presently authorize use of HOPE_000001–542 in Matter 28. Obtain re-production, consent, or appropriate court relief before using the material.
