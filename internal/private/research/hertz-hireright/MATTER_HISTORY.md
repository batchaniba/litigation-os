# Hertz / HireRight — repository history compilation

**Compiled:** October 31, 2026  
**Question answered:** what did this repo already contain about Hertz, HireRight, Gloria Williams, requisition 43711, `OR-102326-NH87V`, Manager Trainee Palo Alto, the sex-offender registry, and Penal Code § 290.46 — and is a matter number already assigned?

**Answer:** **Yes. Matter 43 is Hertz.** It was opened on the October 22, 2026 offer, updated October 23 when HireRight began, and last touched in the live graph on October 28. No lawsuit is filed. The October 31 HireRight report in this packet is **new** to the repository; the live Matter 43 siblings still stop at the MVR furnishing **notice**.

This file is a path index and chronology of **prior** repo work. It is not a pleading and not a substitute for `clocks.json` or the October 31 evidence dump.

Times below that come from the live graph are as those files stored them. Times that come from this packet’s `.eml` files were re-read from Date headers (see [`TIMELINE.md`](TIMELINE.md)).

---

## 1. Matter number

| Question | Finding |
|---|---|
| Is Hertz / HireRight already a numbered matter? | **Yes — Matter 43.** |
| Caption | Brendan Ngwa Nforbi v. Hertz Global Holdings, Inc. |
| Case no. | `TBD` |
| Court | `TBD — no action filed` |
| Lifecycle | `pre_filing` |
| Claims | None asserted (`counts: []`) |
| Docket | `[]` |
| Index row | `internal/src/data/index/matters.json` (number 43, last_updated 2026-10-28, `next_clock` null) |

No other matter number is Hertz. Nearby HireRight or Hertz **strings** that are **not** this employment screen:

| Path / matter | What it is |
|---|---|
| Matter **23** | HireRight report for **Macy’s**, request `OR-052826-TD9W3` (May 28–29, 2026). Abandoned after Macy’s hired. |
| Matter **31** | First Advantage vendor-liability candidate. Mentions HireRight only as the Matter 23 comparator. |
| Matter **42** Staples complaint source paragraphs | Cites the May 2026 HireRight / Macy’s report as corroboration of recurring source identification. Not Hertz. |
| `internal/docs/westlaw_*` *Hertz Corp. v. Friend*, *Lazar v. Hertz* | Unrelated published cases (citizenship / consumer). |

---

## 2. Live Matter 43 graph

Front door: `internal/src/data/index/matters.json` → `internal/src/data/matters/43/`.

| File | What it holds (as of 2026-10-28) |
|---|---|
| `internal/src/data/matters/43/matter.json` | Identity, pre-filing status, entity split (The Hertz Corporation vs. Hertz Global Holdings), key facts through the Oct. 23 MVR **notice** |
| `internal/src/data/matters/43/prose.json` | Shorter status / key_facts / damages / risk mirroring matter.json |
| `internal/src/data/matters/43/events.jsonl` | 15 employment events, Oct. 21 interview texts through Oct. 23 3:05 p.m. MVR notice |
| `internal/src/data/matters/43/evidence.json` | e01–e18 (iMessages, offer, portal, ADP WOTC, HireRight consents, MVR notice) |
| `internal/src/data/matters/43/documents.json` | 16 registered `/documents/matter-43/…` paths |
| `internal/src/data/matters/43/clocks.json` | Four undated `contingent` watches: onboarding, report copy, background status, identity/alias |
| `internal/src/data/matters/43/claims.json` | No counts |
| `internal/src/data/matters/43/docket.json` | `[]` |
| `internal/src/data/matters/43/parties.json` | Holdings (requested caption / ADP) vs. The Hertz Corporation (offer issuer) |
| `internal/src/data/matters/43/damages.json` | No known loss; $23/hour is offered pay, not damages |
| `internal/src/data/matters/43/counsel.json` | `appearances: []` |

**Gap vs. this packet:** none of those files mention Santa Clara C1761642, “In Registry,” “APPLICANT IS LISTED,” Oct. 25 “Brendan Ngwa / Not in Registry,” Managed Adjudication Pending, or the October 31 print. The graph still says the underlying MVR and criminal results “are not yet in the record.”

Public README inventory row (generated; not live): `README.md` line for matter 43 — “Offer accepted — HireRight screening active.”

---

## 3. Private intake and October 23 workshop

### 3.1 Evidence intake (original 18 files)

`internal/private/matters/43/EVIDENCE_INTAKE.md`

SHA-256 register for the October 22–23 conversation uploads (two iMessage JPEGs + 16 PDFs). States that those **bytes were not uploaded to Git or R2** by the opening PR; `documents.json` paths were filled later. Controlling distinctions already recorded:

- HireRight is the CRA; ADP WOTC is separate.
- Gloria Williams named Oracle + HireRight tasks.
- California disclosure lists National Sex Offender Registry as a **product**, not a hit.
- MVR PDF is a furnishing notice, not the MVR.
- Signed forms use **Brendan Ngehsi Ngwanforbi**; recruiting uses **Brendan Ngwa Nforbi**.
- No adverse action as of October 23.

Three consent PDFs in **this** packet are byte-identical to intake items 12, 15, and 17:

| Intake # | Filename | SHA-256 (shared) |
|---|---|---|
| 12 | Acknowledgement and Authorization.pdf | `e6bf9c1759f7062b51aa43be9943ea87e51dac7ff16b66322c4271a91db75a6f` |
| 15 | Other Disclosures and Authorizations.pdf | `be42a13b2c50e446efe71c9a7f514b4ab5998ec5a10e0cf8d0bcd1e9b7d900e8` |
| 17 | Screening Disclosure and Authorization.pdf | `2d726d995a5640f9bef60ca0c9bdc05657fdaf15fa05635c81ab120031269162` |

### 3.2 Strategy workshop (cross-model handoff)

All under `internal/docs/matter-43/workshop/`:

| File | Role |
|---|---|
| `internal/docs/matter-43/workshop/README.md` | Handoff for ChatGPT / Claude / Gemini / Grok. As-of Oct. 23. Companion then cited as PR #1024. Analytical firewall: strong offer ≠ present liability. |
| `internal/docs/matter-43/workshop/OCT_23_HIRERIGHT_UPDATE.md` | HireRight confirmed; consents signed 3:03–3:04 p.m.; free-copy box checked; MVR notice 3:05 p.m.; gate **G2**. |
| `internal/docs/matter-43/workshop/EVIDENCE_DECISION_TREE.md` | E01–E18 matrix; dated sequence; gates G0–G6; competing hypotheses H0–H6 (including Megan’s Law website vs. court-record vs. MVR). |
| `internal/docs/matter-43/workshop/CROSS_MATTER_ASSESSMENT.md` | Stage compare to FedEx 25, UPS 26, Amazon 29, AT&T 36, Best Buy 39, Staples 42, Nuro 41. Hertz: best offer baseline, **zero established liability**. |
| `internal/docs/matter-43/workshop/LLM_REVIEW_PROTOCOL.md` | Copyable independent-LLM task. This packet’s README is the October 31 successor. |
| `internal/docs/matter-43/workshop/REVIEW_LOG.md` | H43-R01 through R12 (open findings). No external-reviewer block filled. |

Workshop as-of date is **October 23**. It does not know the October 31 report.

---

## 4. Registered Matter 43 document paths (bytes not on this tree)

`documents/matter-43/` in this checkout is **`.gitkeep` only**. Paths exist in `documents.json`, `internal/src/data/documents/manifest.json`, and `registry.json`. Commits that registered them include `fb2714a1`, `0cc3acd6`, `118c45de`, `84ddef1c`, `03a84fc6`.

| Registered path (may be R2-only) |
|---|
| `/documents/matter-43/Offer Letter - Manager Trainee, Palo Alto ($23 per hour) (Oct 22 2026).pdf` |
| `/documents/matter-43/Hertz Careers - Additional Application Information Request (Oct 22 2026).pdf` |
| `/documents/matter-43/Hertz Careers - Manager Trainee Offer Extended (Oct 22 2026).pdf` |
| `/documents/matter-43/Hertz Talent Acquisition - Offer Follow-Up (Oct 22 2026).pdf` |
| `/documents/matter-43/ADP - WOTC Screening Request (Hertz Global Holdings, Oct 22 2026).pdf` |
| `/documents/matter-43/Hertz Careers - Offer Acceptance Confirmation (Oct 22 2026).pdf` |
| `/documents/matter-43/Hertz Careers - Application Status Offer Accepted (Req 43711, Oct 22 2026).pdf` |
| `/documents/matter-43/ADP - Tax Credit Screening Confirmation (Oct 22 2026).pdf` |
| `/documents/matter-43/Hertz - Pre-Boarding Instructions (Req 43711, Oct 23 2026).pdf` |
| `/documents/matter-43/HireRight - Acknowledgments and Authorization (Signed Oct 23 2026).pdf` |
| `/documents/matter-43/HireRight - Submission Received (Request OR-102326-NH87V, Oct 23 2026).pdf` |
| `/documents/matter-43/HireRight - Background Verification Consent Forms Email (Oct 23 2026).pdf` |
| `/documents/matter-43/HireRight - Other Disclosures and Authorizations (Signed Oct 23 2026).pdf` |
| `/documents/matter-43/HireRight - Background Verification Request (Oct 23 2026).pdf` |
| `/documents/matter-43/HireRight - Screening Disclosure and Authorization (Signed Oct 23 2026).pdf` |
| `/documents/matter-43/HireRight - MVR Express Furnishing Notice to Hertz (Oct 23 2026).pdf` |

The October 31 report is **not** among those paths. It lives only in this packet: `evidence/2026-10-31_HireRight_Report_to_Hertz_OR-102326-NH87V.pdf`.

The two iMessage screenshots (IMG_8701, IMG_8702) remain hash-registered in EVIDENCE_INTAKE only; `evidence.json` e01–e02 paths are `null`.

---

## 5. Git history of Matter 43 (selected)

| Commit | What landed |
|---|---|
| `c633f51b` | feat: register Matter 43 Hertz conditional offer and evidence chronology |
| `72dfba6d` | docs: add cross-LLM Hertz Matter 43 evidence and strategy workshop |
| `fb2714a1` | Matter 43: add Hertz offer and HireRight screening record |
| `959fd33a` | Matter 43: add Hertz screening strategy workshop |
| Oct. 23 series (`e4d21ef3` … `6c137036`, `513d7b27`, `2a05f559`–`2945d1bf`) | HireRight update into matter siblings, intake, and workshop |
| `0cc3acd6` / `118c45de` / `84ddef1c` / `03a84fc6` | Register Hertz PDFs in manifest / documents.json |
| `aeac4f75` (#1043) | Drop PENDING badge on 43; captions |
| `567b802c` / `4797773b` (#1039) | Oct. 28 portfolio true-up (Matter 43 last_updated) |

Opening workshop text referred to **PR #1024** (`feat/matter-43-hertz-offer`) as then-unmerged. The Matter 43 files are on `main` now.

There is **no** `internal/private/negotiation/43.jsonl`.

---

## 6. Chronology of what the repo already knew (before this packet)

### September 2026 applications — **not in the live Matter 43 graph**

The October 31 email export is the first repo copy of the September Hertz Careers traffic. Matter 43 events begin at the October 21–22 interview/offer. The workshop noted the Kathleen iMessage weekday/date conflict (“Thursday 10/21”) but did not ingest the September 9 / 15 / 16 / 24 / 29 application and interview-scheduling emails (requisitions 42215, 42537, 42544). Those emails are in `evidence/messages/` and [`TIMELINE.md`](TIMELINE.md).

### October 21–22, 2026 — offer (in the graph)

From `events.jsonl` and workshop E01–E10:

- Kathleen HERTZ iMessage: interview at 725 Ridder Park Dr., San Jose; text says “Thursday 10/21 at 1pm” (calendar conflict preserved).
- Oct. 22 1:03 p.m.: applicant traffic-delay text.
- **Oct. 22 3:38 p.m.:** Gloria Williams, Talent Acquisition Partner — team wants to extend a Palo Alto Manager Trainee offer.
- 3:39 p.m.: Hertz Careers formal offer-extended notice.
- 3:40 p.m.: Kathleen text that an offer should arrive.
- **4:49 p.m.:** applicant emails Gloria accepting.
- 5:00 p.m.: Hertz Careers “you just accepted”; portal requisition **43711** = Offer Accepted.
- 5:00 p.m.: ADP WOTC for **Hertz Global Holdings, Inc.**; separate additional-information / Oracle request.
- Offer letter (workshop): The Hertz Corporation; full-time Manager Trainee; $23/hour; 816 San Antonio Rd., Palo Alto, CA 94303; supervisor Kathleen Williams; MVR if applicable + criminal/employment/education checks; at-will.

### October 23, 2026 — HireRight start (in the graph)

- 12:37 p.m.: Gloria Williams pre-boarding for **43711 Manager Trainee** — Oracle task + HireRight.
- 12:37 p.m.: HireRight request for The Hertz Corporation / Brendan Ngwa Nforbi.
- 3:03–3:04 p.m.: consents signed; California free-copy election checked; request **OR-102326-NH87V**.
- ~3:05 p.m. (graph) / **3:04:58 p.m. PDT** (this packet’s MVR `.eml` Date): HireRight notifies that an MVR Express report with public-record information was provided to Gloria Williams, The Hertz Corporation, Estero, FL.
- Graph and workshop: **underlying MVR not in the record**; no adverse action.

### October 24–30, 2026 — **absent from the repo until this packet**

No Matter 43 event, clock, or workshop note for the Oct. 25 “Brendan Ngwa / Not in Registry” result, the Oct. 30 Santa Clara hit, or the registry staff notes. Those facts exist only in the October 31 report (and this packet’s OCR / forensic review).

### October 28, 2026 — graph true-up only

`last_updated` moved to 2026-10-28 with other portfolio clocks. No new Hertz facts.

### October 31, 2026 — this packet

Applicant-side print of the complete report. See [`TIMELINE.md`](TIMELINE.md) and `evidence/`.

---

## 7. Cross-reference — Matter 26 (UPS / First Advantage), E.D. Cal. 2:26-cv-02847

**Why it matters here:** Matter 26 is the filed § 290.46(j)(2)(E) case whose live fight is **source** (NSOR / DOJ vs. California Megan’s Law website). The Hertz report uses the same two-layer pattern: a product line that says the search ran “through the United States Department of Justice,” plus staff notes that name “THE SEX OFFENDER REGISTRY IN THE STATE OF CA” and quote Penal Code § 290.46.

| Item | Path |
|---|---|
| Identity | `internal/src/data/matters/26/matter.json` — *Newanforbi v. United Parcel Service, Inc.*, **2:26-cv-02847-DAD-CKD**, Drozd / Delaney |
| Count 1 | `internal/src/data/matters/26/claims.json` — “Violation of Cal. Penal Code § 290.46(j)(2)(E)” (`live`) |
| Exhibit A | `documents/matter-26/Dkt 07 Exhibit A - First Advantage Background Report (Filed Aug 26 2026).pdf` |
| What Exhibit A is cited for | Matter 29 evidence e39: “DOJ-site National Sex Offender Registry search returned Record Found and identified the California Sex Offender Registry as the source.” |
| Dkt. 14 reply | UPS admits NSOR was searched, Record Found, and “when UPS learned that Plaintiff was included on the National Sex Offender Registry, it used that information when making its employment decisions”; denies accessing the Megan’s Law website. Exhibit A’s own `SOURCE OF RECORD: CALIFORNIA SEX OFFENDER REGISTRY` sentence is the construction fight. |
| Adverse action | First Advantage pre-adverse July 22, 2024; final adverse July 31, 2024. **Hertz has no analogue yet.** |
| Audit row | `internal/docs/legal-intel/recon/2026-10-14-background-report-cross-vendor-audit.md` — Jul. 18, 2024 First Advantage `Record Found`; source `CALIFORNIA SEX OFFENDER REGISTRY` |

Use Matter 26 to frame the **source question**, not to assume Hertz used the website or denied the job.

---

## 8. Cross-reference — Matter 29 (Accurate / Amazon), N.D. Cal. 4:26-cv-09249

**Why it matters here:** same person, same Santa Clara case **C1761642**, opposite registry result from a different CRA, plus the alias / name-variant problem the Hertz report also displays.

| Item | Path |
|---|---|
| Identity | `internal/src/data/matters/29/matter.json` — *Newanforbi v. Amazon.com Services, LLC*, **4:26-cv-09249-ASK** (Oakland; formerly 3:26-cv-09249-ASK) |
| Count 1 | `claims.json` — § 290.46(j)(2)(E) |
| Accurate report | `documents/matter-29/Accurate Background - Consumer Report (Amazon HVH, Ref 496623722, updated Oct 14 2026).pdf` |
| What it shows | Santa Clara **C1761642** found; **National Sex Offender Database Search = NO RECORD FOUND**; identity table included unsupported alias **NEWANSORBI** (“Provided by Applicant”). USER REPORT Oct. 28: reinvestigation removed NEWANSORBI; NSOR stayed negative. |
| Evidence row | `internal/src/data/matters/29/evidence.json` e38 |
| HireRight comparator (Macy’s) | same file e42 → `documents/matter-23/HireRight - Macy's - Background Check Report (Requested May 28 2026).pdf` |
| Accuracy audit | `internal/docs/matter-29/matter29-accurate-accuracy-audit.md` and `internal/private/research/matter-29/05-prior-analysis/matter29-accurate-accuracy-audit.md` |
| Cross-vendor audit | `internal/docs/legal-intel/recon/2026-10-14-background-report-cross-vendor-audit.md` |
| Private research room | `internal/private/research/matter-29/` (facts, claims matrix, *Lerma* lock, discovery plan) |

**Alias / name pattern already in Matter 29 work** (comparators use these; Accurate invented NEWANSORBI):

- NEWANFORBI
- NGWANFORBI
- NGWA-NFORBI
- NFORBI
- Brendan Ngwa Nforbi / Brendan Ngehsi Newanforbi

The Hertz report header uses **Ngwanforbi**; the court and registry hits print **Newanforbi**; the SSN trace prints **BRENDAN NGWA NFORBI**; NSOR #2 on **Brendan Ngwa** returned **Not in Registry**. That is the same family of variants Matter 29 already mapped — plus Hertz did **not** run NSOR on “Brendan Ngwa Nforbi.”

**Standing lock (do not break in any Hertz write-up):** never write that Amazon settled the identical § 290.46 claim. *Lerma v. Amazon.com Services, LLC*, C.D. Cal. 8:22-cv-01727, Dkt. 36 dismissed the Megan’s Law theory because Accurate’s report showed court-record sourcing and NSOR **NO RECORD FOUND**. The later settlement was the surviving Fair Chance Act claim.

Hertz is the **inverse** of Accurate on the registry component (hit vs. miss) and the **same** on C1761642 (court record found). Do not collapse those into one theory.

---

## 9. Cross-reference — Matter 23 (HireRight / Macy’s) — same vendor, earlier screen

| Item | Path |
|---|---|
| Identity | `internal/src/data/matters/23/matter.json` — abandoned; Macy’s hired May 28, 2026 |
| Request | `OR-052826-TD9W3` |
| Report | `documents/matter-23/HireRight - Macy's - Background Check Report (Requested May 28 2026).pdf` |
| Registry notes (May 29, 2026) | “APPLICANT IS LISTED ON THE SEX OFFENDER REGISTRY IN THE STATE OF CA” (S Arun, 3:56 p.m.); “Verified by Aka Name, DOB and Address” (3:57 p.m.); § 290.46 warning (3:57 p.m.); delay ETA Jun. 3; Managed Adjudication Pending |
| Outcome | No registry-based rejection. Plaintiff worked the Stockton job until a CDCR transfer (Matter 30). **Matter 23 is not a Hertz precedent for damages.** |

The October 31 Hertz report repeats the same HireRight sentence and the same § 290.46 warning, with different analysts (Satish Kumar R; Kumar Dilip) and a later “Verified by Name and DOB” (no address this time). Analyst **S Arun** appears on **both** the Macy’s file (May 29) and the Hertz NSOR #3 delay (Oct. 26 6:53 a.m.).

---

## 10. Other repo hits (HireRight / registry theory, not Hertz facts)

| Path | Relevance |
|---|---|
| `internal/docs/matter-42/ndcal/staples-complaint-source-paragraphs.json` | Draft paragraph citing May 2026 HireRight / July 2026 InfoMart as source-identification corroboration |
| `internal/docs/settlement/fcra-file-requests/Accurate Background - Dispute of Accuracy… (Sent Oct 14 2026).txt` | Lists HireRight (May 2026) among comparator reports |
| `internal/private/research/matter-29/09-evidence-map/EXHIBIT-INDEX.md` | R034 / e42 HireRight–Macy’s |
| `internal/src/data/matters/31/matter.json` | First Advantage candidate; HireRight named as Matter 23 vendor analogue |
| `documents/matter-29/Dkt 21 - Accurate Background Answer…` | Accurate’s answer refers to separate matters involving Checkr, HireRight, and InfoMart |
| `internal/docs/CROSS_MATTER_RISK_INDEX.md` | Filename collision note on a Matter 23 HireRight PDF, not Hertz |
| Westlaw inventory / queue | *Hertz Corp. v. Friend*; *Lazar v. Hertz* — **not this matter** |

Searches for `Gloria Williams`, `43711`, `OR-102326-NH87V`, and `Manager Trainee Palo Alto` hit **only** Matter 43 files (plus this packet). They do not appear in Matters 26 or 29 except as this compilation now cross-references them.

---

## 11. What did **not** exist in the repo before this branch

- The October 31 HireRight report PDF, OCR pages, or forensic review.
- The 28 `.eml` files (including the entire September application/interview series).
- Any Matter 43 event after October 23 3:05 p.m.
- Any Hertz adverse-action notice, start date, or negotiation ledger.
- Any assigned matter number **other than 43**.

Treat the live Matter 43 graph as **stale relative to the report**. Updating `events.jsonl` / `evidence.json` is a separate, reviewed data change — not part of this research packet.
