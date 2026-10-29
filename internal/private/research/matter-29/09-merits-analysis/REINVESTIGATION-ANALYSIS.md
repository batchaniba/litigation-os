# Accurate Oct. 28, 2026 reinvestigation packet — analysis

**Document:** `00-user-inputs/accurate-reinvestigation-2026-10-28.pdf` (25 pages). SHA-256 `862f953d69751cadbdf55af29369e2bee4e4f41bd1eeb2a8646a710c667a7316`.

**Not legal advice. Not a filing.** Face of the PDF + the Oct. 14 dispute record. Statutory labels are the FCRA/ICRAA sections already in the matter graph.

## 1. What the packet is

| Part | Pages (packet) | Contents |
|---|---|---|
| Letter | 1–2 | Consumer Dispute Department, dated October 28, 2026 |
| Blank / spacer | 2–3 | Mostly empty pages in the extract |
| CA 1786.22 / .10 / .26 disclosure | 3–5 | English then Spanish |
| CFPB FCRA Summary of Rights | 6–9 | Form |
| California § 1785.15(f) credit-file notice | 10–12 | Form (CCRRA-style; not a substitute for ICRAA) |
| ICRAA 1786.22 summary | 13–14 | Form |
| Consumer report Y94611404 | 15–25 | Enclosed "revised" report |

Enclosures listed in the letter: Consumer Report; California Notice of Rights by an Investigative Consumer Reporting Agency; Summary of Rights Under the FCRA; applicable state notices.

## 2. Letter — established text

Accurate says it received disputes on **October 15, 2026**, of:

1. the AKA name **'Ngwa Nforbi, Newansorbi'**;
2. the **National Sex Offender Database Search**.

It says reinvestigation is complete, the report is revised, the AKA is **removed**, and there was **no reported information** in the NSOR search. It says a copy of the background check is enclosed and a copy of the **revised report was forwarded to the employer**. It recites the right to append a statement, to request two-year recipient notification, and to request a description of the procedure (including furnisher name, address, and telephone if reasonably available). Contact: disputes@accurate.com; 800-216-8024; fax 855-785-4434.

## 3. Date chain (do not collapse)

| Event | Date | Source |
|---|---|---|
| Dispute **sent** | Oct. 14, 2026, 1:58 p.m. PT | events.jsonl |
| Auto-ack SR 20261014-15421955 | Oct. 14, 2:03 p.m. PT | events.jsonl |
| Letter: disputes **received** | Oct. 15, 2026 | R001 p.1 |
| Report RESULT NOTE: dispute initiated | **2026-10-19 09:42:29** | R001 p.16 |
| Letter / claimed completion | Oct. 28, 2026 | R001 p.1 |
| Statutory 30-day mark from Oct. 14 send | Nov. 13, 2026 | clocks `29-accurate-reinvestigation`; 15 U.S.C. § 1681i(a)(1)(A) as cited there |

**FACT:** Oct. 28 is within 30 days of Oct. 14. **QUESTION:** why three different internal dates (14 / 15 / 19). Discovery: the SR file.

User seed said "after his Oct. 15, 2026 dispute." Live record: **sent Oct. 14**. The letter's "received Oct. 15" is Accurate's statement. Report both; do not pick one silently.

## 4. FCRA § 1681i / ICRAA § 1786.24

### What appears satisfied on the face (conditional)

- Written notice of results (the letter).
- Enclosure of a consumer report Accurate calls revised.
- Statement that the employer received a copy.
- Recitation of addendum / procedure-description / two-year-notification rights.
- Timing inside 30 days of the Oct. 14 send (and of an Oct. 15 receipt, if that date controls).

### What the Oct. 14 dispute asked for that the letter does not answer

From the sent-dispute description (events.jsonl) and the pre-send draft snapshot:

| Ask | Result in R001 |
|---|---|
| Delete NEWANSORBI | **Done** on the enclosed report's AKA table and search-name blocks |
| Correct "Provided by Applicant" / state the **source** | Source **not** disclosed |
| Identify every search run under that AKA | **Not** disclosed |
| NSOR: names searched, identifiers, source DB, date/time | Result repeated as no information reported; procedure **not** disclosed |
| Complete file (all info, sources, every version + furnish dates, every recipient, intake names, disclosure/authorization) | Packet is a letter + current report + form notices. That is **not**, on its face, a full 1681g file |

### Scope discipline

The Oct. 14 dispute was **two items** plus a file request. Parole status, disposition dates, conviction-question "No", empty address history, and [LINK] placeholders were **not** in that dispute. Failure to change them is not a § 1681i breach **as to this dispute**. They remain § 1681e(b) / § 1786.20 accuracy issues and can be a **new** dispute.

## 5. FCRA § 1681e(b) / ICRAA § 1786.20(b)

**AKA.** Deletion after dispute is the strongest new accuracy evidence in the file: the prior report contained an AKA Accurate will not stand on. That supports an inaccuracy theory as to the Oct. 14 (and any earlier) version. It is **not** a finding of willfulness. Intake provenance is still NEEDED.

**NSOR.** Reinvestigation **left** "NO RECORD FOUND" / "no reported information." Other CRAs' CA-registry hits (Oct. 14 audit) remain procedure evidence. The dispute asked how the search was run, not for a hit to be added. **Do not dispute this result into a registry hit.** A hit would feed Amazon a Megan's Law-adjacent fact the report currently lacks.

**Unchanged face problems** (still on the "revised" report): C1761642 details; "CURRENTLY ON PAROLE"; disposition date = filing date; incomplete address history; [LINK]/[ENLACE]; header still "updated on 10/14/2026"; NSOR completion date still 07/07/2026.

**Stale header.** A report enclosed with an Oct. 28 reinvestigation letter that still says "updated on 10/14/2026" is incomplete on its face as a version identifier. RESULT NOTE dated 10/19 is the only on-report dispute timestamp.

## 6. Claims, damages, 26(f)

See `CLAIMS-MATRIX.md` and `03-discovery-production/DISCOVERY-PLAN.md`. Short version:

- **Count 1 (§ 290.46):** this packet makes the Accurate-report-as-registry-source theory **harder**, not easier. Same NSOR-negative pattern *Lerma* used to dismiss. Distinguish with Amazon-side proof or non-report sources, or do not run the theory as if the report contained a hit.
- **Count 2 (Fair Chance):** Amazon now allegedly has a revised report. Still no assessment or adverse-action paper in the snapshot. Discovery, not the MTD of Claims 5–7, is the vehicle.
- **Counts 3–4 (FCRA/ICRAA):** AKA deletion + unanswered procedure/file requests + remaining face inaccuracies. Complete-file gap is live.
- **Counts 5–7:** keep R001 out of Rule 12 argument unless the Court asks about amendment.
- **Damages:** Jul. 27 shift loss still predates both reports. AKA error is an October-report fact unless a pre-Oct. 14 furnish is proved. No number in anything counsel sees.
- **26(f):** preserve and request the **reinvestigation file**, all **versions/furnish logs**, Amazon **receipt of the Oct. 28 report**, and the **1681g file**. Supplement the Oct. 19 RFP set. Ask Accurate whether the enclosed packet is their complete-file response; if yes, identify what is missing on the record.

## 7. Immediate consumer options (not directed; listed)

The letter itself lists: append a statement; request two-year notifications; request the procedure description. A **new** dispute could cover parole / disposition dates / complete file if the Oct. 14 file request is treated as unanswered. None of that is drafted here. Nothing is to be sent from this room.
