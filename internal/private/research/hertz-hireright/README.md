# Hertz / HireRight review packet (Matter 43)

**As of:** October 31, 2026 (America/Los_Angeles)  
**Audience:** an outside reviewer (ChatGPT or another authorized model) assessing the Hertz / HireRight record **in totality**  
**Lifecycle:** **Matter 43 already exists.** It is a **pre-filing monitoring workspace**, not a filed case. Caption requested: *Brendan Ngwa Nforbi v. Hertz Global Holdings, Inc.* Case number: `TBD`. Court: `TBD — no action filed`.  
**Do not draft a complaint, demand, adverse-action letter, or employer email from this packet.** Plaintiff is waiting for Hertz’s hiring decision before any drafting or filing.

This directory is private working analysis under `internal/private/`. It does **not** change the live matter graph, clocks, public SPA, Worker/D1, or R2. The October 31 HireRight report is preserved here only.

---

## What this packet is

A single room that puts three things in one place:

1. **The new evidence dump** — the October 31 HireRight report (Request `OR-102326-NH87V`), 28 Hertz/HireRight emails as `.eml`, attachments, OCR of the 16 report pages, and a page-by-page forensic review.
2. **Everything the repository already had** about Hertz and HireRight — Matter 43’s offer/screening record (opened October 22–23, last graph update October 28), the October 23 strategy workshop, the abandoned Matter 23 HireRight/Macy’s report, and the registry-source work in UPS (Matter 26) and Accurate/Amazon (Matter 29).
3. **A merged timeline** with each key fact checked against the emails and the report, not against memory or the README.

Read in this order. Do not reconstruct a docket or a calendar from this README.

| Order | File | Why first |
|---|---|---|
| 1 | This README | Scope, standing rules, what is and is not proven |
| 2 | [`MATTER_HISTORY.md`](MATTER_HISTORY.md) | What the repo already contained before this packet, with paths |
| 3 | [`TIMELINE.md`](TIMELINE.md) | Dated sequence from September 9 applications through the October 31 print |
| 4 | [`evidence/INDEX.md`](evidence/INDEX.md) | 28-email inventory, Message-IDs, SHA-256 list |
| 5 | [`evidence/HireRight_Report_Forensic_Review.md`](evidence/HireRight_Report_Forensic_Review.md) | Page-by-page transcription of the 16-page report |
| 6 | [`evidence/ocr/p-01.txt`](evidence/ocr/p-01.txt) … [`p-16.txt`](evidence/ocr/p-16.txt) | RapidOCR cross-check of each report page |
| 7 | [`evidence/2026-10-31_HireRight_Report_to_Hertz_OR-102326-NH87V.pdf`](evidence/2026-10-31_HireRight_Report_to_Hertz_OR-102326-NH87V.pdf) | The PDF controls if OCR and the review disagree |
| 8 | Live Matter 43 siblings | `internal/src/data/matters/43/` — identity, events through October 23, empty docket, no asserted claims |

---

## Matter identity (already assigned)

| Field | Value | Source |
|---|---|---|
| Portfolio id | **43** (not a new number) | `internal/src/data/index/matters.json`; `internal/src/data/matters/43/matter.json` |
| Requested caption | Brendan Ngwa Nforbi v. Hertz Global Holdings, Inc. | matter.json |
| Written-offer issuer | **The Hertz Corporation** | offer letter (workshop E05); HireRight “Requested By” |
| ADP WOTC entity | Hertz Global Holdings, Inc. | Oct. 22 5:00 p.m. ADP email |
| Case no. / court / judge | TBD — no action filed | matter.json |
| Lifecycle / phase | `pre_filing` | matter.json |
| Numbered cluster | 3 = Employment Violations | matter.json `cluster` |
| Claims asserted | **None.** `claims.json` `counts` is `[]` | `internal/src/data/matters/43/claims.json` |
| Docket | Empty array | `internal/src/data/matters/43/docket.json` |
| Next clock | `null` (four undated watches only) | index `next_clock`; `clocks.json` |
| Negotiation ledger | **None** for 43 | `internal/private/negotiation/` has no `43.jsonl` |
| Graph last_updated | 2026-10-28 | matter.json. **The October 31 report is not yet in the live graph.** |

No other matter number is assigned to Hertz. Matter **23** is the earlier **HireRight / Macy’s** screen (abandoned; Macy’s hired). Matter **31** mentions HireRight only as a comparator vendor, not as a Hertz case.

---

## What changed on October 31

The October 23 workshop and the live Matter 43 graph stop at: offer accepted, HireRight authorized, MVR Express **notice** furnished, **report contents unknown**, no adverse action.

This packet adds the actual HireRight consumer report printed by the applicant on October 31, 2026 at 2:38 p.m. PDT (Activity Log: report opened 2:36 p.m.; PDF metadata 2:40:59 p.m.). The report is a 16-page Microsoft Print-to-PDF of the HireRight web view. It has no text layer. OCR and the forensic review are reading aids; the PDF is the source.

**Now in the record (FACT):**

- Request `OR-102326-NH87V`, package “Field (Driver Required),” requisition **43711**, Manager Trainee, Palo Alto, Oracle Candidate ID 2847550.
- Subject header name: **Brendan Ngehsi Ngwanforbi**. Other last name: **Newanforbi**. SSN-trace name: **BRENDAN NGWA NFORBI**.
- Santa Clara County search #5, name **Newanforbi, Brendan Ngehsi**: **Complete - Court Record Found**, case **C1761642**, completed **Oct 30, 2026 9:10 AM PDT**.
- National Sex Offender Registry, three subrequests:
  - “Brendan Ngwa”: **Not in Registry**, completed **Oct 25, 2026 4:16 PM PDT**.
  - Subrequest 1 (NEWANFORBI): **In Registry**, completed **Oct 30, 2026 11:25 AM PDT**. Analyst note **9:17 AM**: “APPLICANT IS LISTED ON THE SEX OFFENDER REGISTRY IN THE STATE OF CA.”
  - “Brendan Ngehsi Newanforbi”: **In Registry**, completed **Oct 30, 2026 12:48 PM PDT**. Same listing sentence at **12:45 PM**.
- Both listing notes also recite Penal Code § 290.46 (employment-use warning). Search source line: “through the United States Department of Justice.” Staff notes name the California registry.
- Managed Adjudication 3.0: **Pending**. Multiple rows **Undefined**, including MVR and both “In Registry” rows. Request Completion Date blank on every page.
- NSOR delay notes of Oct 30 10:24 a.m. and 10:31 a.m. give **Estimated Completion Date: 04-Nov-2026**. Those two NSOR subrequests then completed the same afternoon. Overall adjudication is still open.

**Still not in the record (UNKNOWN):**

- Any Hertz hiring decision, preliminary adverse action, individualized assessment, rescission, or start date.
- Any Activity Log row showing Hertz opening the report (Recipient column is blank).
- A native or certified HireRight file (this is an applicant-side browser print).
- The exact registry record ID, URL, or the DOB value used for “Verified by Name and DOB.”

A report that contains registry language is **not** an adverse action and **not** a filed claim.

---

## How to review (deliverable)

Work as an independent, adversarial reviewer. Prefer the PDF and the `.eml` Date headers over any prose summary, including this one.

**Produce exactly these sections:**

1. **Bottom line (≤150 words).** Offer strength, what the October 31 report now proves, what it does not, and the next decisive event. The next event is Hertz’s decision (or a HireRight final adjudication / consumer copy), not a filing.
2. **Fact table.** Every material statement tagged **FACT / USER REPORT / INFERENCE / LEGAL QUESTION / UNKNOWN**, with a file path and page or email Date header.
3. **Defense-side red team.** At least five innocent or lawful explanations (MVR/driving record; ordinary court-record use of C1761642; incomplete Oracle task; at-will / no start date; NSOR-vs-Megan’s-Law source split; name-variant matching). Name the document that would test each.
4. **Plaintiff-side theory map (prospective only).** Element → evidence present → evidence missing → statutory exception. Mark every theory **prospective**. Hertz has not decided.
5. **Source-split chart.** Separate (a) Santa Clara court record C1761642, (b) NSOR/DOJ search language, (c) staff notes naming the California registry, (d) Widescreen “Data found… see Sex Offender,” (e) MVR SUSP/DISQ/VIOL. Do not collapse these into one “registry use” finding.
6. **Cross-matter comparison (separate scores, no win probability).**
   - Matter **26** UPS / First Advantage, E.D. Cal. **2:26-cv-02847-DAD-CKD** — live § 290.46(j)(2)(E) count; Exhibit A `SOURCE OF RECORD: CALIFORNIA SEX OFFENDER REGISTRY`; Dkt. 14 admits NSOR use for employment and denies Megan’s Law website access.
   - Matter **29** Amazon / Accurate, N.D. Cal. **4:26-cv-09249-ASK** — Accurate reported C1761642 **and** `NATIONAL SEX OFFENDER DATABASE SEARCH - NO RECORD FOUND`; unsupported alias `NEWANSORBI` later removed on reinvestigation. *Lerma* Dkt. 36 dismissed a Megan’s Law claim on an NSOR-negative Accurate report. **Never write that Amazon settled the identical § 290.46 claim.**
   - Matter **23** HireRight / Macy’s `OR-052826-TD9W3` — same vendor, same “APPLICANT IS LISTED… STATE OF CA” note (May 29, 2026, analyst S Arun). Macy’s hired. Matter abandoned.
7. **Five next documents or events** that can be obtained **without** suing Hertz. Say what each would resolve.
8. **Recommendations and uncertainty.** Preserve the job. Do not contact Hertz, Gloria Williams, HireRight (except the applicant portal the user already uses), or any third party. Do not invent a deadline. Do not value hypothetical wages.

Append findings as a new `H43-Rxx` block conceptually matching `internal/docs/matter-43/workshop/REVIEW_LOG.md`. Do not silently overwrite `events.jsonl`.

---

## Standing rules for this review

- Label **FACT / USER REPORT / INFERENCE / LEGAL QUESTION / UNKNOWN**. Model consensus is not evidence.
- Cite a concrete path: `evidence/messages/…eml` Date header, report page (`ocr/p-NN.txt` or forensic review §), or a live `internal/src/data/matters/NN/` file. If you did not open the PDF, say so.
- Do not invent a docket number. Matter 43 `dkt` is null. Do not treat `documents/matter-43/` paths as locally present — that folder is `.gitkeep` only in this checkout; the October 22–23 PDFs are registered in `documents.json` / the manifest but the bytes are not on this tree.
- Live clocks remain the four **contingent watches** in `internal/src/data/matters/43/clocks.json`. The Nov. 4 date is a HireRight **search-delay ETA** on two NSOR subrequests that later completed October 30. It is not a court deadline and not proof Hertz will decide that day.
- Do not put GitHub or repo URLs in anything Plaintiff would send or file.
- Do not draft settlement figures. There is no `43.jsonl` ledger. If a number is later discussed, the settlement guard applies (`internal/docs/settlement/SETTLEMENT_REANCHOR_MEMO.md` § 3).
- Do not import stipulation-defense voice. Nothing here is a stipulation.
- Keep this analysis **private**. Do not register the report PDF under `documents/` or push it to the public Worker.
- Verify statutes and cases independently. Do not fabricate quotations or holdings. No live law access → mark “unverified — research required.”
- *Hertz Corp. v. Friend* and *Lazar v. Hertz* in the Westlaw queue are **unrelated** citizenship / consumer cases. They are not this employment screen.

---

## Evidence checksums

All **34** SHA-256 values in [`evidence/INDEX.md`](evidence/INDEX.md) were recomputed on this branch after unpack. **34 matched, 0 mismatched, 0 missing.**

The report hash is `39482675c88672946eba5d574f1d98839bb0d2a0628f2e800d7ab4e54c2d5142`.

Three consent PDFs in this dump are byte-identical to the October 23 intake register in `internal/private/matters/43/EVIDENCE_INTAKE.md` (items 12, 15, 17).

---

## What not to do

- Do not open a pull request that files, serves, or “updates the case to ready.”
- Do not write a complaint, a preservation letter to Hertz, or a HireRight dispute **unless the user later asks after Hertz decides**.
- Do not treat Managed Adjudication “Pending” / “Undefined” as a denial.
- Do not treat “National Sex Offender Registry search performed through the United States Department of Justice” as proof of a Megan’s Law **website** visit. That is the live source fight in Matter 26.
- Do not treat Santa Clara C1761642 as a false hit without the court file. The forensic review already flags this: pull the docket before anyone asserts identity mismatch in a pleading.
- Do not contact a spouse, employer, vendor, or court from this packet.

**Success criterion:** the reviewer can say, from the emails and the report, what is proven as of October 31, what Hertz still has to do, how this screen compares to UPS and Accurate, and what to collect next — without inventing a lawsuit.
