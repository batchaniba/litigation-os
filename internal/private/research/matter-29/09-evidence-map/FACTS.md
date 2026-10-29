# Matter 29 — Facts ledger (research)

Epistemic labels follow Matter 0 / Matter 20 practice:

- **FACT** — on the face of a cited document in this room or the live Matter 29 graph
- **INFERENCE** — a conclusion that needs the next sentence of proof
- **UNVERIFIED** — asserted in a source but not independently confirmed here
- **QUESTION** — open; see `12-open-questions/`
- **MISSING** — needed document not in the snapshot

Do not convert INFERENCE into FACT for a brief or a 26(f) statement.

## A. Identity and case

| # | Label | Statement | Source |
|---|---|---|---|
| F01 | FACT | This action is Matter 29, N.D. Cal. No. 4:26-cv-09249-ASK, caption Newanforbi v. Amazon.com Services, LLC | matter.json |
| F02 | FACT | Judge is Magistrate Judge Ajay S. Krishnan | matter.json; Dkt. 9 |
| F03 | FACT | Defendants include Amazon.com Services, LLC and Accurate Background LLC | parties.json |
| F04 | FACT | Plaintiff is proceeding in propria persona | matter.json; user request |
| F05 | FACT | Amazon counsel of record include Andrew P. Frederick; correspondence/clocks also name Douglass G. Brown and Suga A. Ikeda (Morgan Lewis) | counsel.json; events.jsonl Sep. 23 service; clock 29-rule26f-meet-confer |
| F06 | FACT | Accurate counsel include Jasmine J. Stanzick and John Drury (Seyfarth) | events.jsonl; clock 29-rule26f-meet-confer |
| F07 | FACT | Both defendants were served Jul. 31, 2026 | parties.json |
| F08 | FACT | Amazon removed the action Aug. 31, 2026 (Dkt. 1) | docket.json; matter.json |

## B. Hiring / screening timeline (from matter.json key_facts and evidence.json)

Treat matter.json `key_facts` as the portfolio's narrative compilation of documents, not as a new primary source. Pin to evidence.json where an exhibit id exists.

| # | Label | Statement | Source |
|---|---|---|---|
| F10 | FACT | Conditional Amazon offer email Jul. 3, 2026, 2:09 p.m.: XL Warehouse Associate, Fremont, 44051 Osgood Rd; conditioned on background check, drug test, and pre-hire activities; stated range $21.50–$24.00/hour | evidence e17; matter.json |
| F11 | FACT | Pre-hire appointment Jul. 7, 2026, 9:00–9:30 a.m. at the Fremont site | evidence e16, e19 |
| F12 | FACT | Accurate identified itself as a CRA retained by "Amazon Salesforce" for screening Y94611404 (Jul. 7 email) | evidence e27 |
| F13 | FACT | Accurate search ID 496623722 appears on the Jul. 7 "Other Information Needed" email and on later reports | evidence e28; CR-2026-10-14; CR-2026-10-28 |
| F14 | FACT | Plaintiff replied START to Accurate SMS on Jul. 17, 2026, 7:54 a.m. — 10 days after Accurate's Jul. 7 START request | evidence e26 |
| F15 | FACT | Amazon Jobs Jul. 8 SMS: background checks "usually returned 5 days after they are submitted" | evidence e25 |
| F16 | FACT | As of Jul. 27, 2026, 3:23 p.m., Simple Hire showed Background Check PENDING and "You do not have a shift selected" | evidence e14, e15 |
| F17 | FACT | No formal FCRA/ICRAA adverse-action notice is in the Matter 29 snapshot | matter.json; evidence.json (no such exhibit) |
| F18 | FACT | Amazon Jobs email Oct. 14, 2026, 5:06 a.m. PT: application "still in progress" | events.jsonl |

## C. Pleadings / MTD

| # | Label | Statement | Source |
|---|---|---|---|
| F20 | FACT | Claims 1–7 are listed live in claims.json: § 290.46(j)(2)(E); Fair Chance Act § 12952; FCRA; ICRAA; privacy; UCL; IIED | claims.json |
| F21 | FACT | Amazon moved to dismiss the **fifth, sixth, and seventh** claims (Dkt. 19, filed Sep. 22, 2026) | docket.json; Dkt. 19 filename |
| F22 | FACT | Accurate filed an answer Sep. 22, 2026 (Dkt. 21) | docket.json |
| F23 | FACT | Plaintiff served an opposition to Dkt. 19 by email Sep. 23, 2026, 11:00 p.m. PT, to Morgan Lewis (Frederick, Brown; cc Ikeda) and Seyfarth (Stanzick, Drury) | events.jsonl; clocks retired_reason |
| F24 | FACT | No ECF number for that opposition is ingested (`dkt: null`) | docket.json |
| F25 | FACT | Amazon served a 6-page reply Oct. 13, 2026, 12:02 p.m. PT (Suga Ikeda); served copy, not file-stamped in repo | clocks `29-deadline-mtd-reply` |
| F26 | FACT | MTD hearing: Nov. 18, 2026, 1:30 p.m., Courtroom 4 | clocks `29-hearing-mtd` |

## D. Oct. 14 report and dispute

| # | Label | Statement | Source |
|---|---|---|---|
| F30 | FACT | Accurate issued/updated consumer report ref 496623722 (Amazon HVH) Oct. 14, 2026, ordered Jul. 7, 2026 | events.jsonl; CR-2026-10-14 |
| F31 | FACT | Oct. 14 CR reported AKA "NGWA NFORBI, NEWANSORBI" labeled "Provided by Applicant" | accuracy audit §2 #3; evidence e38 |
| F32 | FACT | Oct. 14 CR National Sex Offender Database Search ID 496623723: NO RECORD FOUND, completed 2026-07-07 | accuracy audit; evidence e38 |
| F33 | FACT | Oct. 14 CR Santa Clara County: RECORD FOUND, C1761642, completion 2026-10-14 | accuracy audit |
| F34 | FACT | Plaintiff emailed a dispute and complete-file request Oct. 14, 2026, 1:58 p.m. PT, cc Seyfarth, disputing (1) the NEWANSORBI AKA and (2) the NSOR result as inaccurate/incomplete, and requesting the § 1681g / § 1786.10 file | events.jsonl; Gmail PDF path in clocks |
| F35 | FACT | Accurate Support auto-acked at 2:03 p.m. PT, SR 20261014-15421955 | events.jsonl |
| F36 | FACT | The Oct. 14 dispute asked Accurate to disclose NSOR names searched, identifiers, source database, and run time; it did **not** ask Accurate to add a registry hit | events.jsonl title; dispute draft snapshot |

## E. Oct. 28 reinvestigation packet (this room)

| # | Label | Statement | Source |
|---|---|---|---|
| F40 | FACT | Letter dated October 28, 2026, from Consumer Dispute Department, Accurate Background, 200 Spectrum Center Drive Suite 1100, Irvine CA 92618, to Brendan Ngwa Nforbi, 1455 Cat Tail Dr, Stockton CA 95204 | CR-2026-10-28 p.1–2 |
| F41 | FACT | Letter states: "We received your disputes on October 15, 2026" | same |
| F42 | FACT | Letter lists two disputed items: AKA 'Ngwa Nforbi, Newansorbi'; National Sex Offender Database Search | same |
| F43 | FACT | Letter states the updated report **removes** that AKA | same |
| F44 | FACT | Letter states there was **no reported information** in the National Sex Offender Database Search on the background check report | same |
| F45 | FACT | Letter states Accurate forwarded a copy of the revised report to the employer who requested the report | same |
| F46 | FACT | Letter recites rights to append a dispute statement; to request notification to persons who received a report within two years; and to request a description of the reinvestigation procedure including furnisher identity | same |
| F47 | FACT | Enclosed report header: Background Check Report Y94611404; ordered 07/07/2026; **updated on 10/14/2026** | packet p.15 |
| F48 | FACT | Enclosed report RESULT NOTE: `***DISPUTE COMPLETED***` / `2026-10-19 09:42:29: Dispute has been initiated` | packet p.16 |
| F49 | FACT | Enclosed report AKA table lists NFORBI, BRENDAN (Provided by Applicant) and NEWANFORBI, BRENDAN (Discovered through Address History); it does **not** list NEWANSORBI | packet p.16 |
| F50 | FACT | Enclosed report NSOR: NO RECORD FOUND, search ID 496623723, completion 2026-07-07 | packet p.22 |
| F51 | FACT | Enclosed report still shows Santa Clara RECORD FOUND C1761642; charge disposition dates 10/25/2017; "RELEASED FROM PRISON ONTO PAROLE; CURRENTLY ON PAROLE"; conviction-question ANSWER: No; [LINK]/[ENLACE] placeholders | packet pp.15–24 |
| F52 | FACT | NAME(S) SEARCHED blocks in the enclosed report use NEWANFORBI/BRENDAN, NFORBI/BRENDAN, and Ngwa Nforbi/Brendan/Ngehsi — not NEWANSORBI | packet pp.17–23 |

## F. Inferences (do not treat as findings)

| # | Label | Statement | Why it is only an inference |
|---|---|---|---|
| I01 | INFERENCE | Accurate concluded the NEWANSORBI AKA should not remain on the report | Letter says it was removed; that is not a written admission of 1681e(b) liability |
| I02 | INFERENCE | The Oct. 14 report was inaccurate as to that AKA | Follows from deletion after dispute; still needs intake proof of source |
| I03 | INFERENCE | Accurate's NSOR reinvestigation did not change the July 7 "NO RECORD FOUND" result | Face of letter + enclosed report; we do not have the workpapers |
| I04 | INFERENCE | The July 27 shift loss occurred **before** either consumer report was completed (Oct. 14) | Dates on the documents; causation still NEEDED |
| I05 | INFERENCE | Accurate's report, including after reinvestigation, is a weak vehicle for a "Accurate furnished Megan's Law website data" theory, and is closer to *Lerma*'s NSOR-negative pattern | Compare F50 with *Lerma* Dkt. 36 as described in matter.json / evidence e35–e36. That is a litigation-risk inference, not a holding in this case |
| I06 | INFERENCE | Amazon may now have a revised report | Letter says it was forwarded; Amazon receipt is UNVERIFIED |

## G. *Lerma* (comparator, not this docket)

| # | Label | Statement | Source |
|---|---|---|---|
| F60 | FACT | *Miguel Lerma, Jr. v. Amazon.com Services, LLC et al.*, C.D. Cal. No. 8:22-cv-01727-FWS-JDE, is lodged at `documents/matter-29/lerma-v-amazon/` | documents.json; evidence e35 |
| F61 | FACT | Dkt. 36 (May 26, 2023) granted both MTDs and dismissed Megan's Law, FCRA, and UCL claims without prejudice on that record | matter.json key_facts; evidence e36 |
| F62 | FACT | The Matter 29 key_facts narrative states the incorporated Accurate report showed court-record sourcing and National Sex Offender Database Search "NO RECORD FOUND" | matter.json; locked cluster fact |
| F63 | FACT | Notice of settlement Dkt. 46 (Sep. 21, 2023); only the Fair Chance Act claim against Amazon had remained after the MTD | matter.json |
| F64 | — | **Do not write** that Amazon settled the identical § 290.46 claim | standing lock / PLAYBOOK / cluster lock |
