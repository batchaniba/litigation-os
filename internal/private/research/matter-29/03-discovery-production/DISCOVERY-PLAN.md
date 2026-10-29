# Matter 29 — Discovery plan (research)

Not a stipulation. Not served. Labels: **HELD**, **NEEDED**, **QUESTION**. Live calendar: `clocks.json`, not this file.

## 1. Timing gates

| Gate | Status | Basis |
|---|---|---|
| Discovery open? | **Not yet.** FRCP 26(d)(1) bars discovery before the Rule 26(f) conference, except early Rule 34 delivery under 26(d)(2). Conference is set **Fri. Nov. 6, 2026, 1:00–1:30 p.m. PT** (clocks `29-rule26f-meet-confer`). After that conference, discovery is open unless a stay is ordered. | FRCP 26(d)(1), (d)(2); clocks.json |
| Pending MTD stay? | **No stay in the snapshot.** Amazon's Dkt. 19 attacks Claims 5–7 only. Accurate answered (Dkt. 21). A pending Rule 12(b)(6) motion does not by itself stay discovery. **QUESTION:** Krishnan standing order — confirm no different rule. Standing-order PDF is cited in clocks but is not copied into this room. | Dkt. 19; Dkt. 21; clocks |
| Early Rule 34 | Window open since ~Aug. 22, 2026 (service Jul. 31 + 21 days). Deemed served at the **first actual** 26(f) conference (Nov. 6 if held). Oct. 19 packet service is **UNVERIFIED**. | FRCP 26(d)(2); parties.json service Jul. 31; discovery-set-one README |
| Rule 34 response date if deemed served Nov. 6 | **Dec. 7, 2026** if 30 days from Nov. 6 and no agreement otherwise. The Oct. 14 calendar's Dec. 10 date assumed a Nov. 10 conference. | FRCP 34(b)(2)(A); 26(d)(2)(B) |
| Initial disclosures | Due **Nov. 24, 2026** with the Joint CMC Statement (Dkt. 9 clock `29-deadline-2`). Default 26(a)(1)(C) is 14 days after 26(f) (Nov. 20 if conference is Nov. 6); Dkt. 9's Nov. 24 date is the court-set date in the snapshot. | Dkt. 9; clocks |
| Protective order | **No stipulated PO in the snapshot.** Discuss Nov. 6. N.D. Cal. model / Krishnan order: **UNVERIFIED** until the standing-order PDF is read in this room. | MISSING |
| 30(b)(6) | Drafts on the discovery-set-one branch are marked **HOLD**. Do not serve before refinement. | discovery-set-one README |

## 2. Highest-value records (updated for Oct. 28)

### Amazon

| Fact to prove | Held | Needed | Candidate discovery |
|---|---|---|---|
| Conditional offer, training dates, Fremont XL Warehouse Associate | Offer email Jul. 3; Simple Hire / I-9 / pre-hire emails (evidence.json e14–e31) | Native .eml of key Amazon Jobs messages | RFP: ATS/Simple Hire file; all emails/SMS to Plaintiff |
| Shift disappeared Jul. 27 while BGC pending | Simple Hire screenshot Jul. 27 3:23 p.m. (e15) | Reason code, actor, timestamp, whether screening status caused it | RFP: shift-change log; status codes; who could edit shifts |
| Amazon received Accurate reports | Oct. 28 letter **says** revised report was forwarded to the employer | Receipt, version IDs, who accessed, dates of every furnishing (pre-Oct. 14, Oct. 14, Oct. 28) | RFP: all Accurate transmissions; portal access logs; adjudication notes |
| Individualized Fair Chance assessment (Gov. Code § 12952) | No written assessment in the snapshot | Decision file, job-duty comparison, notice timing | RFP/ROG: assessment worksheet; who decided; notices |
| Use of registry information (§ 290.46) | Accurate NSOR = NO RECORD FOUND even after reinvestigation | Whether Amazon used any **other** registry source, or treated conviction/parole lines as a proxy | RFP: search queries, Megan's Law access, notes containing "registry" / "290" / "sex offender" |
| Formal adverse action / FCRA user notices | **MISSING** in snapshot; Oct. 14 Amazon Jobs email still said application in progress (events.jsonl) | Pre-adverse / adverse notices, or a decision that no adverse action issued | RFP: all 1681b(b)(3) notices; current application status |

### Accurate

| Fact to prove | Held | Needed | Candidate discovery |
|---|---|---|---|
| CRA status and order | Jul. 7 notices; report Y94611404 / ref 496623722 | End-user certification; contract with Amazon | RFP: certification, subscriber agreement |
| Oct. 14 inaccuracy of NEWANSORBI AKA | Oct. 14 CR; Oct. 28 letter **removes** it | Intake record, data-entry log, who labeled it "Provided by Applicant" | RFP: intake; alias provenance; all searches run under that string |
| NSOR "NO RECORD FOUND" despite other CRAs' CA hits | Oct. 14 CR; Oct. 28 reinvestigation **confirms** no reported NSOR information | Names searched, identifiers, source DB, run time — asked in the dispute, **not** disclosed in the letter | RFP: NSOR product definition, query log for ID 496623723, reinvestigation workpapers |
| Reinvestigation completeness (§ 1681i / § 1786.24) | Letter 10/28; RESULT NOTE 10/19 "Dispute has been initiated" | Complete dispute file SR 20261014-15421955; what was verified; who decided | RFP: entire reinvestigation file; procedure description (consumer may also request it under the letter's own terms) |
| Complete file (§ 1681g / § 1786.10) | Requested 10/14 | All versions, recipients, sources, disclosure/authorization | RFP + the statutory file request (still outstanding on the face of the letter) |
| Santa Clara 99-day search / package review 10/13 before result 10/14 | Face of both reports | Vendor/court-runner timestamps; identifiers matched | RFP: search 496644204 log |
| "CURRENTLY ON PAROLE" | Face of both reports | Source and verification date | RFP: source document; CDCR (Plaintiff-side) |
| Versions furnished to Amazon | Letter says Oct. 28 revision forwarded | Every furnish date | Recipients list |

## 3. ESI (carry forward Oct. 17 proposal; add reinvestigation)

Preserve from **July 1, 2026** through final screening/dispute disposition, plus the **Oct. 14–28 reinvestigation** file.

Add to the Oct. 17 ESI proposal:

- Dispute ticket SR 20261014-15421955 and all timestamps (intake 10/14 ack vs. letter "received 10/15" vs. RESULT NOTE 10/19).
- All report-generation jobs for Y94611404 / 496623722, including the job that produced the enclosed Oct. 28 report that still says "updated on 10/14/2026".
- Proof of transmission of the revised report to Amazon.

Full text: `05-prior-analysis/07_Rule_26f_ESI_Proposal.snapshot-2026-10-17.md`.

## 4. Protective order / privilege

Discuss a standard N.D. Cal. PO for identifiers (SSN, DOB), screening records, and vendor source-system details. Confidentiality is not a reason to withhold Plaintiff's own consumer-report file. FRE 502(d) clawback: propose. Privilege-log date: discuss.

## 5. Phasing

Plaintiff position for the conference (research only): **no stay** pending the Nov. 18 MTD of Claims 5–7. Claims 1–4 (and Accurate's entire answer) are live. Targeted first-wave RFPs on the screening file, report versions, and the Jul. 27 shift change.

## 6. Cross-defendant seam (internal)

Amazon's best story may be "we only saw court records / NSOR was negative." Accurate's best story may be "we only transmit; Amazon decides." Those can conflict. Discovery should force a **common identifier crosswalk** (order IDs, version IDs, timestamps, actor IDs) so each desk cannot point at a gap in the other's production. Do not say this out loud as a "gotcha"; ask for the crosswalk as ordinary ESI.
