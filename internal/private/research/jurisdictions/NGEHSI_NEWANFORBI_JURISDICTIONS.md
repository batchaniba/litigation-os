# Jurisdictions — Brendan Ngehsi Newanforbi (and close variants)

**Classification:** internal/private research only. Do not copy into the public SPA, Worker/D1, README tables, fuse board, or any paper Plaintiff will send or file.

**As of:** 2026-11-01. Sources crawled: `internal/src/data/index/matters.json`, `internal/src/data/matters/NN/` (`matter.json`, `docket.json`, `documents.json`, `events.jsonl`), `internal/private/matters/`, `internal/private/research/`, `internal/docs/name-conform/`, `internal/scripts/extracts/`, and first-page captions of complaint/petition/order PDFs that are on this branch under `documents/`.

**Name forms in scope:** `Brendan Ngehsi Newanforbi`, `Ngehsi Newanforbi`, `BRENDAN NGEHSI NEWANFORBI`, and last-name-only court captions `Newanforbi v. …` where a filed paper or CourtListener docket slug shows that surname.

**Method:** A case is listed as a Newanforbi appearance only if the user was a named party (plaintiff, petitioner, or defendant) on a filed action and the repo proves the Newanforbi form on a caption, clerk order, CourtListener slug, or contemporaneous filed paper. Pre-filing drafts are not appearances. Cases filed only as `Brendan Ngwa Nforbi` / `Ngwa Nforbi` / `Nforbi` are listed separately as excluded. Santa Clara County habeas is excluded entirely, even though those petitions use this name.

**Removed actions** are listed under both the state court of origin and the federal court of destination, because the party appeared in both.

---

## Summary

| Jurisdiction | Expected? | Confirmed? | Newanforbi appearances (filed) |
|---|---|---|---|
| U.S. District Court, E.D. Cal. | Yes | **Yes** | 1, 3, 6, 7, 13, 17, 18, 21, 25 (removed), 26 (removed); Matter 11 filed but **no case number in the graph** |
| U.S. District Court, N.D. Cal. | Yes | **Yes** | 24, 28, 29 (removed from Alameda) |
| Sacramento County Superior Court | Yes | **Yes** | 8, 9; Matter 15 original complaint (May 13, 2026) **no Sacramento number in the graph** |
| San Joaquin County Superior Court | Yes | **Yes** | 5, 15 (recalibrated), 22, 25 (state origin), 26 (state origin); 4 / 14 / 16 claimed filed with **no assigned number on disk** |
| Alameda County Superior Court | Yes | **Yes** | 2, 20, 27, 29 (state origin) |
| Santa Clara County Superior Court | Yes | **Partial** | Civil Newanforbi appearance **not confirmed** after habeas exclusion. Remaining Santa Clara civil (Matter 35) is Nforbi-only. Criminal **C1761642** is in this court; certified docket / minute-order PDF is **not in the repo** |
| Immigration Court, Aurora, Colorado | No (extra) | **Found, name-form unconfirmed** | Feb. 8, 2021 IJ order; PDF not stored |
| California Court of Appeal / Cal. Supreme Court / Ninth Circuit | No | **Not found** as a filed party appearance | Sixth District mandate packet is draft-only |
| Matter 0 (private contingency) | n/a | n/a | Not a filed case; not in the public graph |

---

## 1. U.S. District Court, Eastern District of California — CONFIRMED

Role in every row below is **Plaintiff**. Short captions are from `matter.json`. Status is from `matter.json` / `status_label`.

| Matter | Case no. | Caption | Filed | Status | Name-form proof |
|---|---|---|---|---|---|
| 1 | **2:25-cv-01460-DC-CSK** | *Newanforbi v. CHP et al.* (complaint: State of California; CHP; Meza-Gonzalez; Melano) | May 27, 2025 | Closed — voluntary dismissal without prejudice Aug. 15, 2026; refiled as Matter 32 under the Nforbi form | Complaint caption `BRENDAN NGEHSI NEWANFORBI`: `documents/matter-32/from-01/0.Newanforbi v. CHP.pdf`. Dismissal: `documents/matter-32/from-01/Notice of Voluntary Dismissal Without Prejudice (Aug 11 2026).pdf`. Identity: `internal/src/data/matters/01/matter.json`. CourtListener: `/docket/70393737/ps-newanforbi-v-state-of-california/` |
| 3 | **2:26-cv-00004-DJC-JDP** | *Newanforbi v. Derrick et al.* | Jan. 5, 2026 (FAC Jan. 12, 2026) | Closed Aug. 26, 2026 — Derrick/Noguchi dismissed Jul. 22; Palacios dismissed Aug. 20–21 | Clerk-stamped dismissal caption `BRENDAN NGEHSI NEWANFORBI`: `documents/matter-03/Notice of Voluntary Dismissal - Katie Palacios (Filed Aug 20 2026).pdf`. Identity: `internal/src/data/matters/03/matter.json`. CourtListener: `/docket/72104727/ps-newanforbi-v-derrick/` |
| 6 | **2:26-cv-00195-TLN-AC** | *Newanforbi v. HOPE et al.* | Jan. 22, 2026 | Dismissed without prejudice — notice May 21; minute order Jun. 1, 2026 | Last-name form on identity + CourtListener slug `ps-newanforbi-v-hope-psychotherapy-inc`. Same-day January 22 batch as Matter 18, whose screening order uses the full name. Complaint PDF cataloged at `documents/matter-06/Complaint.pdf` is **not on this working tree**. Identity: `internal/src/data/matters/06/matter.json` |
| 7 | **2:26-cv-00983-DC-CSK** | *Newanforbi v. Candelaria* (Candelaria individual; Gordon official capacity) | Identity JSON: Apr. 27, 2026. Dismissal paper recites initiation Mar. 19, 2026; FAC Apr. 29, 2026 | Dismissed without prejudice Aug. 15, 2026; refiled as Matter 33 under the Nforbi form | Dismissal caption `BRENDAN NGEHSI NEWANFORBI`: `documents/matter-33/from-07/Notice of Voluntary Dismissal Without Prejudice (Aug 11 2026).pdf`. Identity: `internal/src/data/matters/07/matter.json`. CourtListener: `/docket/72521399/ps-newanforbi-v-candelaria/` |
| 11 | **TBD — never assigned a live docket number in the index** | *Newanforbi v. Macomber* | Mar. 2, 2026 (events.jsonl) | Dismissed with prejudice Jun. 29, 2026 (same voluntary-dismissal batch as 13/17/18/21) | Identity + events only. `documents.json` is empty. `internal/src/data/matters/11/matter.json`; `internal/private/research/parole-habeas/INDEX.md` § Matter 11. **Case number unconfirmed.** |
| 13 | **2:26-cv-00190-DC-SCR** | *Newanforbi v. Urrea et al.* | Jan. 22, 2026 | Dismissed with prejudice Jun. 29, 2026 | Identity + CourtListener `/docket/72183511/ps-newanforbi-v-urrea/`. Complaint PDF not on this working tree. `internal/src/data/matters/13/matter.json` |
| 17 | **2:26-cv-00194-DAD-SCR** | *Newanforbi v. Maloney et al.* | Jan. 22, 2026 | Dismissed with prejudice Jun. 29, 2026 | Identity + CourtListener `/docket/72183822/ps-newanforbi-v-maloney/`. `internal/src/data/matters/17/matter.json` |
| 18 | **2:26-cv-00191-DJC-CSK (PC)** | *Newanforbi v. Barocio* | Jan. 22, 2026 | Dismissed with prejudice Jun. 29, 2026 | Screening order caption `BRENDAN NGEHSI NEWANFORBI`, No. 2:26-cv-0191 DJC CSK P: `documents/opinions/Newanforbi v Barocio - USDC EDCal - Screening Order Dismissed WLA May 18 2026.pdf`. Identity: `internal/src/data/matters/18/matter.json` |
| 21 | **2:26-cv-00193-DC-CKD** | *Newanforbi v. Rojo et al.* | Jan. 22, 2026 | Dismissed with prejudice Jun. 29, 2026 | Identity + CourtListener `/docket/72182274/ps-newanforbi-v-rojo/`. Complaint cataloged at `documents/matter-21/Complaint.pdf` is **not on this working tree**. `internal/src/data/matters/21/matter.json` |
| 25 | **2:26-cv-02881-DAD-SCR** (removed from San Joaquin **STK-CV-UWT-2026-0009118**) | *Newanforbi v. Federal Express Corporation* | State Jul. 15, 2026; removed Aug. 24, 2026 | Active — last confirmed Dkt. 10 Sep. 24, 2026; Oct. 8 conference outcome not verified | Removal caption `BRENDAN NGEHSI NEWANFORBI`: `documents/matter-25/Dkt 01 - Petition and Notice of Removal (Filed Aug 24 2026).pdf`. State complaint same name: `documents/matter-25/Newanforbi v FedEx Complaint.pdf`. Identity: `internal/src/data/matters/25/matter.json` |
| 26 | **2:26-cv-02847-DAD-CKD** (removed from San Joaquin **STK-CV-UWT-2026-0009113**) | *Newanforbi v. United Parcel Service, Inc.* | State Jul. 15, 2026; docketed in Sacramento Division Aug. 20, 2026 | Active — MTD under submission (Oct. 7 hearing vacated) | Events record the E.D. Cal. docket caption as `BRENDAN NGEHSI NEWANFORBI` (UPS’s “NGWANFORBI” misspelling did not land on the docket): `internal/src/data/matters/26/events.jsonl` (Aug. 20, 2026 CASE ASSIGNED). State complaint: `documents/matter-26/Newanforbi v UPS Complaint.pdf`. Identity: `internal/src/data/matters/26/matter.json` |

E.D. Cal. cases filed **only** as Ngwa Nforbi (36, 38, 39) are in the excluded table, not here.

---

## 2. U.S. District Court, Northern District of California — CONFIRMED

Role in every row is **Plaintiff**. N.D. Cal. help-desk email of Sep. 1, 2026 itself listed the Newanforbi docket form on 3:26-cv-07504-LJC, 3:26-cv-09249-ASK, and 4:26-cv-05953-ASK (later 3:26-cv-05953-CRB): `documents/matter-28/Gmail - Pro se e-filing one account two name forms - CAND ECF Help Desk (Sent Sep 1 2026).pdf`.

| Matter | Case no. | Caption | Filed | Status | Name-form proof |
|---|---|---|---|---|---|
| 24 | **3:26-cv-05953-CRB** (formerly 4:26-cv-05953-ASK) | *Newanforbi v. Serrato* | Jun. 17, 2026 | Active — MTD Nov. 20, 2026, 10:00 a.m. Zoom (Breyer) | Complaint caption `BRENDAN NGEHSI NEWANFORBI` / `BRENDAN NGEHSJ NEW ANFORBI` (OCR): `documents/matter-24/Complaint (Doc 1, Filed Jun 17 2026).pdf`. Name-conform packet treats current docket name as Brendan Ngehsi Newanforbi: `internal/scripts/ndcal-name-change-admin-motions.py`; `internal/docs/name-conform/`. CourtListener: `/docket/73504901/ngehsi-newanforbi-v-serrato/` |
| 28 | **3:26-cv-07504-LJC** | *Newanforbi v. Shannon Smith, LCSW, CEO, et al.* | Case filed Jul. 20, 2026; complaint docketed Jul. 21, 2026 | Active — stayed pending San Joaquin Matter 5 judgment; joint status Nov. 17, 2026 | As-filed complaint caption `BRENDAN NGEHSI NEWANFORBI`: `internal/private/research/matter-28/07-source-text/Complaint-as-filed-copy.txt`. CourtListener: `/docket/73646240/ngehsi-newanforbi-v-smith/`. Identity: `internal/src/data/matters/28/matter.json` |
| 29 | **4:26-cv-09249-ASK** (formerly 3:26-cv-09249-ASK; removed from Alameda **26CV201554**) | *Newanforbi v. Amazon.com Services, LLC* (Accurate Background LLC also a defendant) | State Jul. 28, 2026 (accepted Jul. 29); removed Aug. 31, 2026 | Active — 26(f) Nov. 6; MTD Nov. 18; CMC Dec. 1 | State/removal exhibit complaint `BRENDAN NGEHSI NEWANFORBI`: `internal/private/research/matter-29-discovery/extracts/Dkt_02_Removal_Exhibits.txt`. Federal papers: `documents/matter-29/Dkt 21 - Accurate Background Answer and Affirmative and Other Defenses (Filed Sep 22 2026).txt`; `documents/matter-29/Dkt 19 - Amazon Motion to Dismiss Fifth Sixth Seventh Claims with Memorandum (Filed Sep 22 2026).txt`. Identity: `internal/src/data/matters/29/matter.json` |

N.D. Cal. cases filed **only** as Ngwa Nforbi (32, 33) are in the excluded table. Matter 30 (*Newanforbi v. Moua*) is pre-filing — not an appearance.

---

## 3. Sacramento County Superior Court — CONFIRMED

| Matter | Case no. | Caption | Role | Filed | Status | Name-form proof |
|---|---|---|---|---|---|---|
| 8 | **26WM000135** | *Newanforbi v. Candelaria, et al.* | Petitioner (administrative mandate, CCP §§ 1094.5, 473(d); Veh. Code § 13559) | May 18, 2026 | Abandoned — fee-waiver denied on non-appearance Jul. 17, 2026; fee-payment deadline lapsed ~Jul. 27, 2026 | Identity + events (petition filed; FW-003 denied; Dept. 10C minutes). Petition PDF cataloged at `documents/matter-33/from-08/Newanforbi v. Candelaria Mandamus.pdf` is **not on this working tree**. `internal/src/data/matters/08/matter.json`; `internal/src/data/matters/08/events.jsonl` |
| 9 | **26WM000028** | *Newanforbi v. Macomber* | Petitioner (CCP § 1085 mandate) | Jan. 30, 2026 (FAC ~Feb. 2 / e-filed Mar. 31, 2026 per parole-habeas index) | Closed — demurrer sustained without leave May 29, 2026 (Arguelles, Dept. 13A) | Identity + `internal/private/research/parole-habeas/INDEX.md` § Matter 9. Tentative/order path cataloged: `documents/matter-09/CU_26WM000028_e91359ab-2598-4573-a45a-fa7893fc4cb07.pdf` (**not on this working tree**). `internal/src/data/matters/09/matter.json` |
| 15 (original) | **No Sacramento number in the graph** | *Newanforbi v. Dodd et al.* (damages complaint) | Plaintiff | Dated May 8, 2026; filed May 13, 2026 | Superseded by the San Joaquin recalibrated complaint (below). Do not treat as a live Sacramento case | Events + prose: `internal/src/data/matters/15/events.jsonl` (May 13); `internal/src/data/matters/15/prose.json`; extract of the Sacramento complaint captioning `Plaintiff BRENDAN NGEHSI NEWANFORBI`: `internal/scripts/extracts/complaint.json`. **Sacramento case number unconfirmed.** |

---

## 4. San Joaquin County Superior Court — CONFIRMED

| Matter | Case no. | Caption | Role | Filed | Status | Name-form proof |
|---|---|---|---|---|---|---|
| 5 | **STK-CV-UF-2026-0001032** | *Newanforbi v. Palacios et al.* (Katie Palacios; HOPE Psychotherapy, Inc.) | Plaintiff | Feb. 10, 2026 (FAC Apr. 22, 2026) | Demurrer to FAC sustained WOLA Jul. 15, 2026; judgment-entry / Nov. 2, 2026 ex parte pending | Order caption `BRENDAN NGEHS] NEWANFORBI` / body `Brendan Ngehsi Newanforbi`: `documents/matter-05/Order Sustaining Demurrer to FAC WOLA - Jul 15 2026.pdf`. Stipulation extract: `internal/scripts/extracts/matter5_slb_stipulation.json`. Identity: `internal/src/data/matters/05/matter.json` |
| 15 (recalibrated) | **STK-CV-UPI-2026-5417** (also written STK-CV-UPI-2026-0005417) | *Newanforbi v. California Department of Corrections and Rehabilitation, et al.* | Plaintiff | Recalibrated complaint dated Jun. 8, 2026; filed Jun. 11, 2026 | Abandoned — dismissed with prejudice Jul. 24, 2026 | Identity + events + documents inventory (`5417 Complaint.pdf`, summons, POS). PDFs cataloged under `documents/matter-15/` are **not on this working tree**. `internal/src/data/matters/15/matter.json`; `internal/src/data/matters/15/events.jsonl` |
| 22 | **STK-CV-UWT-2026-0007649** | *Newanforbi v. Pilot Travel Centers LLC* | Plaintiff | May 29, 2026 | Settled Jul. 14, 2026; CIV-110 dismissal with prejudice entered Aug. 6, 2026 | Conformed CIV-110: party line `BRENDAN NGEHSI NEWANFORBI` (attorney-block OCR `Brendan Naehsi Newanforbi`): `documents/matter-22/CIV-110 Request for Dismissal - Entire Action With Prejudice (Pilot, CONFORMED, Dismissal Entered Aug 6 2026).pdf`. Identity: `internal/src/data/matters/22/matter.json` |
| 25 (state origin) | **STK-CV-UWT-2026-0009118** | *Newanforbi v. Federal Express Corporation* | Plaintiff | Jul. 15, 2026 | Removed to E.D. Cal. Aug. 24, 2026 | Complaint caption `BRENDAN NGEHSI NEWANFORBI`, San Joaquin Superior Court: `documents/matter-25/Newanforbi v FedEx Complaint.pdf`. Events: `internal/src/data/matters/25/events.jsonl` |
| 26 (state origin) | **STK-CV-UWT-2026-0009113** | *Newanforbi v. United Parcel Service, Inc.* | Plaintiff | Jul. 15, 2026 | Removed to E.D. Cal. (docketed Aug. 20, 2026) | Complaint caption `BRENDAN NGEHSI NEWANFORBI`, San Joaquin Superior Court: `documents/matter-26/Newanforbi v UPS Complaint.pdf`. Events: `internal/src/data/matters/26/events.jsonl` |

### Claimed San Joaquin filings with no assigned number on disk

These identity records use the Newanforbi caption and an events.jsonl “filed” line, but `case_no` is `TBD` and `documents.json` is empty. Treat as **unconfirmed appearances** until a clerk number or conformed first page is ingested.

| Matter | Caption (identity) | Claimed filed | Status in graph | Paths |
|---|---|---|---|---|
| 4 | *Newanforbi v. Derrick et al.* | May 29, 2026 (bundled events line with Matter 8 / 22) | Abandoned — voluntarily dismissed | `internal/src/data/matters/04/matter.json`; `internal/src/data/matters/04/events.jsonl` |
| 14 | *Newanforbi v. Urrea et al.* | Jun. 30, 2026 | Abandoned — voluntarily dismissed | `internal/src/data/matters/14/matter.json` |
| 16 | *Newanforbi v. Rojo* | Jul. 7, 2026 | Abandoned — voluntarily dismissed | `internal/src/data/matters/16/matter.json` |

Matter 23 (*Newanforbi v. Macy's*) is **not** an appearance: `filed` is “Pending”; status is abandoned because no adverse action occurred. `internal/src/data/matters/23/matter.json`.

---

## 5. Alameda County Superior Court — CONFIRMED

| Matter | Case no. | Caption | Role | Filed | Status | Name-form proof |
|---|---|---|---|---|---|---|
| 2 | **26CV168913** | *Newanforbi v. Meza-Gonzalez et al.* (Meza-Gonzalez; Melano; State / CHP) | Plaintiff | Feb. 4, 2026 (Jan. 30 One Legal attempt rejected; same papers accepted Feb. 4) | Dismissed without prejudice Aug. 15, 2026 | Body of complaint: “incarceration of Plaintiff Brendan Ngehsi Newanforbi”: `documents/matter-32/from-02/Newanforbi v. Meza Gonzalez et al.pdf`. Dismissal caption `BRENDAN NGEHSI NEWANFORBI`, Case No. 26CV168913: `documents/matter-32/from-02/Request for Dismissal Without Prejudice (Draft, Aug 11 2026).pdf` (docket row marks it filed Aug. 15). Events: first attempt filed as `BRENDAN NGEHSI NEWANFORBI vs STATE OF CALIFORNIA, et al.` — `internal/src/data/matters/02/events.jsonl`. Identity: `internal/src/data/matters/02/matter.json` |
| 20 | **26CV191136** | *Newanforbi v. California Highway Patrol, et al.* | Petitioner (CCP § 1085 mandate / Pen. Code § 679.10) | May 29, 2026 | Active — CMC Nov. 4, 2026; opening brief Nov. 13; merits Jan. 8, 2027 | Petition caption `BRENDAN NGEHSI NEWANFORBI`: `documents/matter-32/from-20/Petition for Writ of Mandate.pdf`. Clerk order: `Brendan Ngehsi Newanforbi` v. California Highway Patrol et al., No. 26CV191136: `documents/opinions/Newanforbi v California CHP - Alameda Sup Ct - Order Continuing CMC to Sep 2 2026.pdf`. Identity: `internal/src/data/matters/20/matter.json` |
| 27 | **26CV199902** | *Newanforbi v. Randstad, et al.* (Randstad US, LLC; The RK Logistics Group, Inc.) | Plaintiff | E-filed Jul. 20, 2026; corrected summons accepted Jul. 21, 2026 | Settled; dismissal pending (Notice of Settlement Oct. 26, 2026) | Complaint caption `BRENDAN NGEHSI NEWANFORBI`: `documents/matter-27/Complaint for Damages - Newanforbi v Randstad US LLC et al (Jul 20 2026).pdf`. Identity: `internal/src/data/matters/27/matter.json` |
| 29 (state origin) | **26CV201554** | *Newanforbi v. Amazon.com Services, LLC et al.* | Plaintiff | Jul. 28, 2026 (accepted Jul. 29; Hon. Jamilah Jefferson, Dept. 520) | Removed to N.D. Cal. Aug. 31, 2026 | Same complaint as the federal removal exhibit: `internal/private/research/matter-29-discovery/extracts/Dkt_02_Removal_Exhibits.txt`. Events: `internal/src/data/matters/29/events.jsonl` |

---

## 6. Santa Clara County Superior Court — PARTIAL / EXPECTED

**Habeas (excluded entirely, per instruction — not catalogued as Newanforbi appearances):**

- Matter 10 — *Newanforbi v. Macomber*, **C2602632**, filed Feb. 23, 2026; denied without prejudice Apr. 27, 2026. Proceeding `habeas`. Identity: `internal/src/data/matters/10/matter.json`.
- Matter 19 — *Newanforbi v. Macomber* (petition also names Keely Dodd), **C2604791**, filed Apr. 3, 2026; HC-004 filed Sep. 1, 2026; ruling not verified. The petition caption is `BRENDAN NGEHSI NEWANFORBI` (`documents/matter-19/Petition for Writ of Habeas Corpus (filed Apr. 3, 2026).pdf`) but this case is **out of scope**.

**After that exclusion, a civil Newanforbi appearance in this court is not confirmed.** The only other Santa Clara civil matter in the graph is Matter 35 (*Ngwa Nforbi v. Ross Stores*), filed solely under the Nforbi form — see excluded table.

**Criminal case in this court (not habeas; extra proceeding type):**

| Case no. | Caption (as attested) | Role | Filed / conviction | Status | Name-form proof |
|---|---|---|---|---|---|
| **C1761642** | People v. [name on file] — Counts 2 and 3 (PC §§ 289(a)(1)(A), 220(a)(1)); Hon. Arthur Bocanegra | Defendant | Filing date on Accurate report: Oct. 25, 2017. Conviction / sentencing: Jan. 12, 2018 (parole-habeas index; prenup notes) | Judgment of conviction; 6-year CDCR term; parole Dec. 2, 2020. **Not a portfolio matter.** Certified register of actions / minute-order PDF **missing from the repo** | CA registry / CRA hits use `BRENDAN NGEHSI NEWANFORBI`, DOB 9/16/1996: `internal/docs/matter-29/matter29-accurate-accuracy-audit.md`; Accurate extract case block: `internal/private/research/matter-29/07-source-text/accurate-reinvestigation-2026-10-28.txt`. Narrative (minute order uploaded 2026-10-04, original not stored): `internal/private/prenup/IMMIGRATION_NOTES.md`; `internal/private/research/parole-habeas/INDEX.md`. Prenup notes also list other name variants on the same records. **Do not treat the missing minute order as ingested.** |

**Flag:** Expected jurisdiction Santa Clara County Superior Court is confirmed only as the site of C1761642 (criminal) and the excluded habeas pair. It is **not** confirmed for a non-habeas civil case filed as Newanforbi.

---

## Extra jurisdiction found

### Immigration Court, Aurora, Colorado — FOUND, NAME-FORM UNCONFIRMED

| Case | Role | Date | Status | Proof |
|---|---|---|---|---|
| Immigration Court, Aurora, CO, Judge Elizabeth McGrail | Respondent (removal) | Feb. 8, 2021 | Final — removable under INA §§ 237(a)(1)(B) and 237(a)(2)(A)(iii); asylum/withholding denied; CAT deferral granted; both sides waived appeal | `internal/private/prenup/IMMIGRATION_NOTES.md`; `internal/private/research/parole-habeas/INDEX.md` § 5. **IJ order PDF is not in the repo.** Name variants on the uploaded immigration/criminal packet are listed as “Ngwa Nforbi, Brendan Ngehsi; Newanforbi; Brendan Ngehsi Ngwa Nforbi.” This is an extra court, not one of the six expected. |

No filed party appearance was found in the California Court of Appeal, the California Supreme Court, or the Ninth Circuit. The Sixth District mandate packet under `internal/private/research/parole-habeas/coa-6th/` is **draft only**.

Administrative / non-court filings (CASOMB complaint, BBS complaint, DGS government claims) are not courts and are omitted.

---

## Excluded — filed only under Brendan Ngwa Nforbi / Ngwa Nforbi / Nforbi

Do not treat these as Newanforbi-form appearances. Several later papers discuss both names; the **filed caption** is Nforbi.

| Matter | Court | Case no. | Caption | Filed | Status | Proof the caption is Nforbi, not Newanforbi |
|---|---|---|---|---|---|---|
| 12 | San Joaquin Sup. Ct. | STK-CV-UF-2026-0001094 | *Brendan Ngwa Nforbi v. Diamond Truck Sales, Inc.* | Feb. 13, 2026 | Dismissal filed Oct. 26, 2026 — pending closure | Complaint: `BRENDAN NGWA NFORBI` — `documents/matter-12/1094 Complaint.pdf`. `internal/src/data/matters/12/matter.json` |
| 32 | USDC N.D. Cal. | 4:26-cv-08271-ASK (formerly 3:26-cv-08271-PHK) | *Nforbi v. Meza-Gonzalez, et al* | Aug. 10, 2026 (signed Aug. 7) | Active — MTD / reassignment | Conformed Dkt. 1: `BRENDAN NGWA NFORBI` — `documents/matter-32/ndcal/Dkt 01 - Complaint (CONFORMED, Filed Aug 10 2026).pdf`. Help-desk email lists this docket as the Nforbi form |
| 33 | USDC N.D. Cal. | 3:26-cv-08272-RFL (formerly LJC) | *Nforbi v. Candelaria et al.* | Aug. 10, 2026 (signed Aug. 7) | Active — FAC answered | Conformed Dkt. 1: `BRENDAN NGWA NFORBl` — `documents/matter-33/ndcal/Dkt 01 - Complaint (CONFORMED, Filed Aug 10 2026).pdf` |
| 35 | Santa Clara Sup. Ct. | 26CV501995 | *Ngwa Nforbi v. Ross Stores, Inc., et al.* | Aug. 26, 2026 | Active — Ross answered; discovery Nov. 17 | Conformed complaint footer `NGWA NFORBI v. ROSS STORES`: `documents/matter-35/Verified Complaint (CONFORMED, Filed Aug 26 2026) - 26CV501995.pdf`. Identity: `internal/src/data/matters/35/matter.json` |
| 36 | USDC E.D. Cal. | 2:26-cv-03314-DJC-AC (PS) | *Brendan Ngwa Nforbi v. AT&T Mobility Services LLC* | Filed E.D. Cal.; IFP granted Oct. 14, 2026 | Active — USM service pending | Identity + docket paths `Complaint - Ngwa Nforbi v. AT&T …`. `internal/src/data/matters/36/matter.json` |
| 38 | USDC E.D. Cal. | 2:26-cv-03312-DC-SCR | *Brendan Ngwa Nforbi v. Swift Transportation Co. of Arizona LLC* | E.D. Cal. (IFP ECF No. 2; fee/IFP outcome not verified) | Active | Identity + `Complaint - Ngwa Nforbi v. Swift …`. `internal/src/data/matters/38/matter.json` |
| 39 | USDC E.D. Cal. | 2:26-cv-03315-DC-CKD (PS) | *Brendan Ngwa Nforbi v. Best Buy Co., Inc.* | Sep. 18, 2026 | Active — fee paid Oct. 27, 2026 (user report) | Identity + Dkt. 1 path. `internal/src/data/matters/39/matter.json` |

**Not filed (not appearances under any name):** Matters 23, 30, 31, 34, 37, 40, 41, 42, 43. Matter 0 is a private contingency workspace, not a filed case (`internal/private/matters/00/`).

---

## Vendor-reported San Joaquin criminal numbers — NOT confirmed as court appearances

Accurate’s October 2026 file-disclosure JSON lists three San Joaquin numbers under the printed name `BRENDAN NGEHSI NEWANFORBI`, DOB 09/16/1996, each `identified_by_name` **false** and `identified_by_dob` **true**, charge description N/A:

- `STK-CR-FMISC-2020-0002397`
- `STK-CR-FMISC-2020-0004747`
- `STK-CR-FMISC-2025-0004687`

Source: `internal/private/research/matter-29-discovery/grok-review-2026-10-31/09-SOURCE-REGISTER.md`. These are **not** treated as confirmed party appearances. No San Joaquin criminal docket, complaint, or minute order for those numbers is in the matter graph.

---

## Flags

1. **Santa Clara County Superior Court (expected):** no non-habeas *civil* Newanforbi appearance confirmed. Habeas C2602632 / C2604791 excluded by instruction. Matter 35 is Nforbi-only. Criminal C1761642 is in this court; the court PDF is not ingested.
2. **Matter 11 (expected E.D. Cal.):** identity says filed Mar. 2, 2026 and dismissed with prejudice Jun. 29, 2026, but `case_no` remains `TBD (USDC E.D. Cal.)` and no complaint PDF is cataloged.
3. **Matter 15 original Sacramento filing:** events and the complaint extract prove a Newanforbi damages complaint filed May 13, 2026; the Sacramento case number is not in the graph.
4. **Matters 4, 14, 16:** Newanforbi captions and “filed” event lines, no clerk numbers, no PDFs on disk.
5. **Matters 6, 13, 17, 21:** CourtListener `ps-newanforbi-…` slugs plus identity captions confirm the *Newanforbi* surname; the complaint first pages are not on this working tree, so the full `Brendan Ngehsi` given-name block is inferred from the January 22, 2026 batch (Matter 18’s screening order uses the full name) rather than re-read from those PDFs.
6. **Extra court:** Immigration Court, Aurora, Colorado (Feb. 8, 2021). Name form on the IJ caption is unverified because the order is not stored.
7. **Not extra courts:** CASOMB, BBS, and DGS Government Claims Program.

---

## Source index (identity front door)

`internal/src/data/index/matters.json` is the front door for Matters 1–43. Sibling files used: each matter’s `matter.json` (`filed`, `court`, `case_no`, `caption`, `lifecycle`, `proceeding`, `status` / `status_label`), plus `docket.json` / `documents.json` / `events.jsonl` where a path or filing line was needed. Private front door `internal/private/matters/index.json` was checked; Matter 0 is not a filed case.
