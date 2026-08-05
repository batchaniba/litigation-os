# Cross-Matter Risk Index

Generated from `CONSISTENCY_AUDIT.md`, matter JSON records, and a full-text scan of archived PDFs.

## Summary

- Active matters scanned: 12
- Archived matters scanned: 19
- Contradiction findings indexed: 19
- Archived→active cross-reference signals: 211

## Active matter risk scores

| Matter | Score | Exposed to archived matters |
|---|---|---|
| Matter 19 | 78 | 01, 02, 03, 04, 05, 06, 07, 09, 10, 11, 13, 14, 15, 16, 17, 18, 21, 22, 23, 24, 30, 46 |
| Matter 28 | 72 | 03, 04, 05, 06, 11, 13, 14, 15, 16, 17, 18, 21, 30 |
| Matter 07 | 31 | 00, 01, 02, 03, 05, 06, 08, 09, 10, 11, 12, 14, 17, 18, 19, 20, 24, 30, 32, 33, 35, 37, 54, 55, 56, 69 |
| Matter 20 | 30 | 01, 02, 03, 04, 05, 06, 07, 08, 12, 14, 15, 18, 21, 24, 30, 33, 35, 69 |
| Matter 01 | 25 | 00, 02, 03, 04, 05, 06, 07, 08, 09, 11, 12, 13, 14, 15, 17, 18, 19, 20, 22, 23, 24, 30, 32, 33, 35, 37, 46, 54, 55, 56, 69 |
| Matter 24 | 17 | 01, 02, 03, 04, 06, 07, 08, 09, 11, 12, 13, 14, 17, 18, 19, 20, 22, 23, 46 |
| Matter 02 | 15 | 01, 03, 04, 05, 06, 07, 08, 09, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24, 30, 33, 35, 46, 69 |
| Matter 25 | 11 | 22, 23, 26, 27, 29, 31 |
| Matter 12 | 7 | 00, 01, 02, 06, 07, 08, 09, 11, 18, 20, 24, 32, 37, 54, 55, 56 |
| Matter 27 | 5 | 22, 23, 25, 26, 29, 31 |
| Matter 29 | 5 | 22, 23, 25, 26, 27, 31 |
| Matter 26 | 0 | 22, 23, 25, 27, 29, 31 |

## Contradiction findings

### #1 — Finding 1 (high)
- Matters: Matter 01, Matter 01, Matter 07, Matter 08, Matter 20, Matter 01, Matter 07, Matter 08, Matter 20, Matter 01, Matter 18, Matter 20, Matter 24
- Type: sworn_contradiction

**1. "Arrest" vs. "detention only" — argued both ways, each time picking whichever position serves the forum.** (Matters 1, 7, 8, 20) Matter 1's federal Complaint pleads that CHP's "detention" recharacterization is "factually and legally incorrect," and that handcuffing, transport, and chemical-test advisements are "all indicia of a full custodial arrest" under *Dunaway v. New York*. Matters 7, 8, and 20 take the opposite position — that the same Detention Certificate is dispositive proof the event "ceased to be an arrest as a matter of law," calling it "legally equivalent to a judicial finding that no crime was committed." > Matter 1 Complaint ¶18: *"Plaintiff asserts that this characterization is factually and legally incorrect. He was subjected to handcuffing, placed in the back of a patrol vehicle, transported under guard, and read chemical test advisements — all indicia of a full custodial arrest within the meaning of *Dunaway v. New York*, 442 U.S. 200 (1979)."* > > Matter 20 Petition (§B heading): *"The Detention Certificate and Statutory Nullification of the Arrest ... By operation of law, the event ceased to be an arrest more than two months before the January 24, 2025 APS hearing."* These are irreconcilable sworn positions on the same historical fact, each adopted only when convenient. Classic impeachment/judicial-estoppel material.

### #2 — Finding 2 (high)
- Matters: Matter 02, Matter 07, Matter 20, Matter 07, Matter 30, Matter 01, Matter 20, Matter 05, Matter 03, Matter 07, Matter 03, Matter 30, Matter 01, Matter 20, Matter 33, Matter 05, Matter 03
- Type: sworn_contradiction

**2. Employment start date conflict.** (Matters 7, 20) Matter 7 repeatedly and specifically pleads employment with Centerline began "October 30, 2024 — just two days before" the Nov. 1 encounter. Matter 20's verified petition instead states wages are documented on "twenty-six consecutive weekly pay stubs covering the pay periods from May 5, 2024 through January 3, 2025" — over five months earlier than the claimed start date. > Matter 7 FAC ¶3: *"He had commenced his employment with Centerline Drivers, LLC on October 30, 2024—just two days before the November 1, 2024 CHP encounter."* > > Matter 20 Petition ¶33: *"...reflected on twenty-six consecutive weekly pay stubs covering the pay periods from May 5, 2024 through January 3, 2025."* Both cannot be true as pled.

### #3 — Finding 3 (high)
- Matters: Matter 03, Matter 05, Matter 06, Matter 06, Matter 19, Matter 09, Matter 17, Matter 10, Matter 10, Matter 05, Matter 05, Matter 06, Matter 07, Matter 09, Matter 06, Matter 06, Matter 10
- Type: sworn_contradiction

**3. HOPE's per-parolee revenue figure changed between two of the litigant's own sworn complaints.** (Matters 5, 6) Matter 6's original Complaint (verified Jan. 19, 2026) computes "$9,690 annually" from a single contract, with shown math. Its FAC (verified Feb. 17, 2026, one month later) drops the math and asserts "$10,600 annually" from three contracts. The $10,600 figure is then repeated in Matter 5's FAC. No document produced in discovery supports either number — `matters.js`'s own notes for Matter 5 already flag it as "a discovery-compulsion target." > Matter 6 original Complaint p.7: *"...generates approximately $9,690 annually in group and CTM fees alone."* > > Matter 6 FAC p.6: *"...generates approximately $10,600 per year in baseline fees alone."*

### #4 — Finding 4 (high)
- Matters: Matter 04, Matter 03, Matter 05, Matter 03, Matter 05, Matter 20
- Type: sworn_contradiction

**4. Grace-period revocation date is off by six weeks against the litigant's own produced evidence.** (Matters 3, 5) Matter 3's FAC pleads the revocation happened "in or about early April 2025." HOPE's own business records (Bates HOPE_000190, cited in Matter 5's case notes) date the same event to February 20, 2025. Already flagged internally as unreconciled.

### #5 — Finding 5 (high)
- Matters: Matter 05, Matter 15, Matter 09, Matter 15, Matter 19, Matter 15, Matter 09, Matter 19, Matter 09, Matter 04, Matter 04, Matter 06, Matter 05, Matter 09, Matter 04, Matter 06, Matter 05, Matter 15
- Type: sworn_contradiction

**5. The "Eagan" misidentification — the central theory of Matter 15 — was quoted without the error in two earlier, still-pending filings.** (Matters 9, 15, 19) Matter 15's entire liability theory turns on CDCR Form 1502-DR misidentifying the litigant as a different parolee, "Eagan," in the Unit Supervisor Comments — offered as proof no individualized review occurred. But Matter 9's verified FAC and Matter 19's signed habeas petition, both filed months earlier and quoting the *same* underlying document, silently substitute "Newanforbi" for "Eagan" in their own body text, even though the actual attached exhibit in both says "Eagan." > Matter 9 FAC ¶4 (as pled): *"Newanforbi has only completed approximately 4 years of the required 6.5 years of supervision."* > > Matter 9's own attached Exhibit A (actual document text): *"Eagan has only completed approximately 4 years of the required 6.5 years of supervision."* Opposing counsel can argue either that the quote was altered from a verified exhibit in two separate courts, or that the "Eagan" defect wasn't actually apparent/material to the litigant when he read the same document twice before — undermining Matter 15's claim that the misidentification is "facially obvious."

### #6 — Finding 6 (high)
- Matters: Matter 06, Matter 24, Matter 24, Matter 20, Matter 02, Matter 24, Matter 12, Matter 20, Matter 20, Matter 02, Matter 18, Matter 24
- Type: sworn_contradiction

**6. Matter 24 swears, under penalty of perjury, that no related action names the same defendant or challenges the same decision — which is false.** (Matters 24, 20, 2) Matter 24's verified federal complaint (signed June 12, 2026) lists only two related actions and affirmatively states: *"Neither related action asserts any claim against Captain Serrato. Neither related action challenges the April 20, 2026 denial of the U Visa certification request... This action raises no claims that duplicate or overlap with the related actions."* This is contradicted by the portfolio's own data: Matter 20 (filed three weeks earlier) already names "G. Serrato, Captain and Commander CHP Dublin Area" and seeks a writ compelling the identical U-visa certification — and is never mentioned. Matter 2, which *is* listed, has a fully-briefed U-Visa Certification Motion with a hearing the very next day (June 18, 2026) that Matter 24's disclosure never mentions. This is a duplicative-litigation / candor-to-the-court exposure, not a wording issue — the kind of thing that gets a case dismissed or sanctioned if a defendant notices.

### #7 — Finding 7 (medium)
- Matters: Matter 07, Matter 01, Matter 07, Matter 20, Matter 01, Matter 07, Matter 69, Matter 33, Matter 35, Matter 20, Matter 02, Matter 07, Matter 20
- Type: sworn_contradiction

**7. Three non-reconciling lost-wage totals for the identical CDL suspension period.** (Matters 1, 7, 20) — Matter 1 gives a vague range ("$175,000–$450,000+"); Matter 7 computes $69,368/year from a flat $33.35/hr rate; Matter 20 states "$900–$2,800/week" pay stubs totaling "approximately $112,000." None reconcile, and the wage methodology itself differs between Matter 7 and 20 despite both citing the same Centerline employment.

### #8 — Finding 8 (medium)
- Matters: Matter 08, Matter 01, Matter 07, Matter 20, Matter 01, Matter 07, Matter 20
- Type: sworn_contradiction

**8. The pre-stop "impairment cue" explanation changed between filings.** (Matters 1, 7, 20) — Matter 1 attributes roadside rest to "a long night of social activity," never mentioning any medical condition. Matters 7 and 20 drop that explanation entirely and introduce, for the first time, that the litigant "is pre-diabetic" — a condition said to mimic intoxication signs. Not mutually exclusive, but the complete disappearance of one narrative in favor of a new one in the more legally aggressive filings reads as tailoring.

### #9 — Finding 9 (medium)
- Matters: Matter 09, Matter 03, Matter 06, Matter 03, Matter 06
- Type: sworn_contradiction

**9. Agent Derrick is portrayed as an actively engaged retaliator in one federal case and as procedurally derelict/absent in another.** (Matters 3, 6) — Matter 3 describes Derrick personally threatening the litigant, revoking his grace period, and escalating supervision. Matter 6's original complaint instead says "Agent Derrick failed to initiate CTMs or complete Form 3043 ... directly causing the procedural void." Not strictly irreconcilable, but the two portraits are in tension.

### #10 — Finding 10 (medium)
- Matters: Matter 10, Matter 14, Matter 15, Matter 16, Matter 19, Matter 21, Matter 14, Matter 15, Matter 19, Matter 16, Matter 21
- Type: sworn_contradiction

**10. Gary Noguchi holds two different job titles depending on which line of cases you read.** (Matters 14, 15, 16, 19, 21) — "Unit Supervisor" in the Urrea/discharge-review line (Matter 14's real complaint; `matters.js` text for 15/19); "Supervising Parole Agent ... with final authority over parole travel approvals" in the Rojo/travel-request line (Matters 16 and 21's real complaints). Likely the same role described informally two ways, but it's a sworn, verified statement about a recurring named defendant, and the specific authority held can matter for supervisory-liability theories.

### #11 — Finding 11 (low)
- Matters: Matter 11, Matter 12, Matter 54, Matter 01, Matter 08, Matter 12, Matter 55, Matter 07
- Type: sworn_contradiction

**11.** One-minute discrepancy in the sworn stop time — 12:54 a.m. (Matters 1, 8) vs. 12:55 a.m. (Matter 7) — trivial alone, but later filings anchor legal arguments to precise dashcam timestamps down to the second.

### #12 — Finding 12 (low)
- Matters: Matter 12, Matter 07, Matter 32, Matter 00, Matter 55, Matter 37, Matter 00, Matter 56, Matter 09, Matter 01
- Type: sworn_contradiction

**12.** Matter 7's FAC labels a 32-second dashcam gap (00:55:37 to 00:56:09) as "approximately fourteen seconds" — an internally consistent but objectively wrong arithmetic statement repeated in Matter 1's narrative too.

### #13 — Finding 13 (low)
- Matters: Matter 13, Matter 16, Matter 21, Matter 15, Matter 19, Matter 16, Matter 14, Matter 02
- Type: sworn_contradiction

**13.** Both the Rojo travel-denial storyline (Matters 16/21) and the unrelated Dodd/Noguchi discharge-review storyline (Matter 15) hinge on the same date, November 19, 2025, for two different events. Not a contradiction, but very likely the root cause of the Matter 16 recordkeeping error below (finding #14) — worth double-checking no future filing conflates the two. --- ## Part 2 — Portfolio recordkeeping errors (`src/data/matters.js`) These are errors in the app's own case-tracking summaries, not in the sworn court filings. Lower litigation risk, but worth fixing so the portfolio doesn't misinform future drafting.

### #14 — Finding 14 (high)
- Matters: Matter 14, Matter 16, Matter 16, Matter 19, Matter 21, Matter 16, Matter 21, Matter 16
- Type: recordkeeping

**14. Matter 16's summary describes a completely different incident than what was actually filed.** `matters.js` says Matter 16 is about "Agent Rojo assum[ing] AOR on Nov. 19, 2025 and withhold[ing the] finalized Discharge Review Report" — but the real, filed complaint is the state-law mirror of Matter 21's Reno church-travel-denial dispute (same dates, same text quotes, same narrative). The two real complaints (16 and 21) agree with each other; only the app's summary of Matter 16 is wrong.

### #15 — Finding 15 (high)
- Matters: Matter 15, Matter 14, Matter 14
- Type: recordkeeping

**15. Matter 14's defendant list is wrong.** `matters.js` lists Keely Dodd as a Matter 14 defendant; she appears nowhere in the actual filed complaint. The real fourth defendant, Bryan Bishop (DAPO Director, sued officially), is omitted entirely from `matters.js`.

### #16 — Finding 16 (medium)
- Matters: Matter 16, Matter 15, Matter 11
- Type: recordkeeping

**16. Jury vs. bench trial — stale.** The last pre-filing draft demanded a jury trial; the actual court-stamped operative complaint (Matter 15, file-stamped June 11, 2026) elects a bench trial instead. `matters.js` still says "jury trial demanded."

### #17 — Finding 17 (medium)
- Matters: Matter 17, Matter 09, Matter 01, Matter 09, Matter 15, Matter 19
- Type: recordkeeping

**17. Discharge-review date — stale and internally unreconciled.** Matter 9's own pleading text says "December 1, 2025" throughout; `matters.js`'s Matter 9 summary says "November 2025 Discharge Review." (Matter 15 separately anchors to November 19, 2025, using a different field on the same physical form — reconcilable, but never explained in any of the pleadings.)

### #18 — Finding 18 (medium)
- Matters: Matter 18, Matter 12
- Type: recordkeeping

**18. Matter 12's summary overstates what's actually pled.** `matters.js` states as settled fact that the prior owner "expressly disclosed" the truck's defect to Diamond and that an out-of-service order existed. Both the original complaint and the FAC (filed three months apart) plead these same two facts only "on information and belief," explicitly flagged as unconfirmed.

### #19 — Finding 19 (low)
- Matters: Matter 19, Matter 14, Matter 04, Matter 09, Matter 03, Matter 04, Matter 11, Matter 13, Matter 17, Matter 18, Matter 04, Matter 03, Matter 04, Matter 04, Matter 22, Matter 23, Matter 46, Matter 22, Matter 23, Matter 23, Matter 01, Matter 24, Matter 06, Matter 02, Matter 01, Matter 11, Matter 18, Matter 24
- Type: recordkeeping

**19. Matter 14's causes-of-action list undercounts the real complaint.** `matters.js` lists 4 causes; the actual filed complaint pleads 9, including a Writ of Mandate and two California Constitution claims omitted from the summary entirely. --- ## Part 3 — Documentation gaps (no pleadings uploaded) Matters 4, 11, 13, 17, and 18 have no PDFs in `public/documents/`, so they could only be checked against `matters.js`'s own text, not against a primary source. None of the five showed an obvious internal inconsistency in that text, but none can be verified either — flagged as a gap, not a finding. If any of these are ever refiled, their complaints should be checked directly against the sibling matters they mirror (especially Matter 4 against Matter 3's FAC, given the grace-period date issue at finding #4). --- ## Part 4 — Clean result **Matters 22 and 23** (Pilot Travel Centers / Macy's) were checked specifically for whether the shared PC §290.46(j) legal theory was described consistently across an adjudicated matter and a never-filed one. No inconsistency found — the statutory framing, the FCRA/ICRAA/UCL/Tameny theory stack, and the "sophisticated employer received an explicit statutory warning" narrative are identical in both, and the factual differences between them (Matter 22: hired then terminated; Matter 23: offer only, never started) are exactly what should differ between two independent events. `matters.js`'s hedged, anticipatory language for Matter 23 accurately reflects that no complaint was ever filed. --- ## Priority ranking If only two things get fixed, they should be: 1. **Matter 24's related-actions disclosure** (finding #6) — this is the one finding with real procedural downside (dismissal, sanctions, candor-to-the-court exposure) rather than just impeachment risk, and it's fixable by amending the complaint's Related Actions section before it's relied on. 2. **The arrest-vs-detention contradiction** (finding #1) — the most exploitable factual conflict, spanning four matters and two forums; worth deciding on one consistent position going forward even if some pending filings can't be un-said. --- *Report prepared: July 11, 2026* *Methodology: five parallel document-reading analysis passes across 18 of 24 matters' primary pleadings (complaints, FACs, petitions, declarations), cross-referenced against `src/data/matters.js` case-tracking summaries. Matters without uploaded pleadings were checked against summary text only and flagged as documentation gaps.*


## Archived → active cross-reference signals

| Archived matter | File | Signal type | Active matter | Detail |
|---|---|---|---|---|
| 03 | 2.Newanforbi v. Derrick.pdf | active_defendant_name | 19 | archived matter 03 filing '2.Newanforbi v. Derrick.pdf' names active matter 19 defendant(s): CDCR |
| 03 | 2.Newanforbi v. Derrick.pdf | active_defendant_name | 25 | archived matter 03 filing '2.Newanforbi v. Derrick.pdf' names active matter 25 defendant(s): FedEx |
| 03 | 2.Newanforbi v. Derrick.pdf | active_defendant_name | 28 | archived matter 03 filing '2.Newanforbi v. Derrick.pdf' names active matter 28 defendant(s): HOPE, Noguchi, Palacios |
| 03 | 28 Notice of Related Cases.pdf | active_defendant_name | 28 | archived matter 03 filing '28 Notice of Related Cases.pdf' names active matter 28 defendant(s): HOPE, Noguchi, Palacios |
| 03 | 8_Jscott.pdf | active_defendant_name | 19 | archived matter 03 filing '8_Jscott.pdf' names active matter 19 defendant(s): CDCR |
| 03 | 8_MTQ.pdf | active_defendant_name | 19 | archived matter 03 filing '8_MTQ.pdf' names active matter 19 defendant(s): CDCR |
| 03 | 8_MTQ.pdf | active_defendant_name | 25 | archived matter 03 filing '8_MTQ.pdf' names active matter 25 defendant(s): FedEx |
| 03 | 8_MTQ.pdf | active_defendant_name | 28 | archived matter 03 filing '8_MTQ.pdf' names active matter 28 defendant(s): HOPE, Noguchi, Palacios |
| 03 | 8_OpM4L.pdf | active_defendant_name | 28 | archived matter 03 filing '8_OpM4L.pdf' names active matter 28 defendant(s): Noguchi |
| 03 | 8_reply.pdf | active_defendant_name | 28 | archived matter 03 filing '8_reply.pdf' names active matter 28 defendant(s): Noguchi |
| 03 | LIVE 1.8.5 NEXTGEN CM-ECF - U.S. District Court for Eastern California.pdf | active_defendant_name | 28 | archived matter 03 filing 'LIVE 1.8.5 NEXTGEN CM-ECF - U.S. District Court for Eastern California.pdf' names active matter 28 defendant(s): Noguchi, Palacios |
| 03 | Notice of Appearance Blaze.pdf | active_defendant_name | 28 | archived matter 03 filing 'Notice of Appearance Blaze.pdf' names active matter 28 defendant(s): HOPE, Noguchi, Palacios |
| 03 | Notice of Change of Address (July 7, 2026).pdf | active_defendant_name | 19 | archived matter 03 filing 'Notice of Change of Address (July 7, 2026).pdf' names active matter 19 defendant(s): CDCR |
| 03 | Notice of Change of Address (July 7, 2026).pdf | active_defendant_name | 28 | archived matter 03 filing 'Notice of Change of Address (July 7, 2026).pdf' names active matter 28 defendant(s): HOPE, Noguchi, Palacios |
| 03 | Notice of Voluntary Dismissal - Derrick and Noguchi (Jul 22 2026).pdf | active_defendant_name | 28 | archived matter 03 filing 'Notice of Voluntary Dismissal - Derrick and Noguchi (Jul 22 2026).pdf' names active matter 28 defendant(s): Noguchi, Palacios |
| 03 | SLB MTD.pdf | active_defendant_name | 19 | archived matter 03 filing 'SLB MTD.pdf' names active matter 19 defendant(s): Board of Parole |
| 03 | SLB MTD.pdf | active_defendant_name | 25 | archived matter 03 filing 'SLB MTD.pdf' names active matter 25 defendant(s): FedEx |
| 03 | SLB MTD.pdf | active_defendant_name | 28 | archived matter 03 filing 'SLB MTD.pdf' names active matter 28 defendant(s): HOPE, Noguchi, Palacios |
| 03 | SLBStipulation.pdf | active_defendant_name | 28 | archived matter 03 filing 'SLBStipulation.pdf' names active matter 28 defendant(s): HOPE, Noguchi, Palacios |
| 03 | SummonsReturnedExecuted.pdf | active_defendant_name | 28 | archived matter 03 filing 'SummonsReturnedExecuted.pdf' names active matter 28 defendant(s): Palacios |
| 05 | BBS Complaint Palacios LMFT 44555.pdf | active_defendant_name | 19 | archived matter 05 filing 'BBS Complaint Palacios LMFT 44555.pdf' names active matter 19 defendant(s): CDCR |
| 05 | BBS Complaint Palacios LMFT 44555.pdf | active_defendant_name | 28 | archived matter 05 filing 'BBS Complaint Palacios LMFT 44555.pdf' names active matter 28 defendant(s): CASOMB, HOPE, Noguchi, Palacios |
| 05 | BBS Complaint Palacios LMFT 44555.pdf | active_defendant_name | 29 | archived matter 05 filing 'BBS Complaint Palacios LMFT 44555.pdf' names active matter 29 defendant(s): Housing |
| 05 | CASOMB Complaint - HOPE Program.pdf | active_defendant_name | 19 | archived matter 05 filing 'CASOMB Complaint - HOPE Program.pdf' names active matter 19 defendant(s): CDCR |
| 05 | CASOMB Complaint - HOPE Program.pdf | active_defendant_name | 20 | archived matter 05 filing 'CASOMB Complaint - HOPE Program.pdf' names active matter 20 defendant(s): Certification |
| 05 | CASOMB Complaint - HOPE Program.pdf | active_defendant_name | 24 | archived matter 05 filing 'CASOMB Complaint - HOPE Program.pdf' names active matter 24 defendant(s): Certification |
| 05 | CASOMB Complaint - HOPE Program.pdf | active_defendant_name | 28 | archived matter 05 filing 'CASOMB Complaint - HOPE Program.pdf' names active matter 28 defendant(s): CASOMB, HOPE, Noguchi, Palacios |
| 05 | CASOMB Complaint Continuation Sheet .pdf | active_defendant_name | 19 | archived matter 05 filing 'CASOMB Complaint Continuation Sheet .pdf' names active matter 19 defendant(s): CDCR |
| 05 | CASOMB Complaint Continuation Sheet .pdf | active_defendant_name | 20 | archived matter 05 filing 'CASOMB Complaint Continuation Sheet .pdf' names active matter 20 defendant(s): Certification |
| 05 | CASOMB Complaint Continuation Sheet .pdf | active_defendant_name | 24 | archived matter 05 filing 'CASOMB Complaint Continuation Sheet .pdf' names active matter 24 defendant(s): Certification |
| 05 | CASOMB Complaint Continuation Sheet .pdf | active_defendant_name | 28 | archived matter 05 filing 'CASOMB Complaint Continuation Sheet .pdf' names active matter 28 defendant(s): CASOMB, HOPE, Noguchi, Palacios |
| 05 | DISC001_SEC_4a2 HOPE1.pdf | active_defendant_name | 19 | archived matter 05 filing 'DISC001_SEC_4a2 HOPE1.pdf' names active matter 19 defendant(s): CDCR |
| 05 | DISC001_SEC_4a2 HOPE1.pdf | active_defendant_name | 28 | archived matter 05 filing 'DISC001_SEC_4a2 HOPE1.pdf' names active matter 28 defendant(s): HOPE, Palacios |
| 05 | DISC001_SEC_4a2 Palacios .pdf | active_defendant_name | 19 | archived matter 05 filing 'DISC001_SEC_4a2 Palacios .pdf' names active matter 19 defendant(s): CDCR |
| 05 | DISC001_SEC_4a2 Palacios .pdf | active_defendant_name | 28 | archived matter 05 filing 'DISC001_SEC_4a2 Palacios .pdf' names active matter 28 defendant(s): CASOMB, HOPE, Palacios |
| 05 | DRFT HOPE resp plntf RFA1.pdf | active_defendant_name | 19 | archived matter 05 filing 'DRFT HOPE resp plntf RFA1.pdf' names active matter 19 defendant(s): CDCR |
| 05 | DRFT HOPE resp plntf RFA1.pdf | active_defendant_name | 28 | archived matter 05 filing 'DRFT HOPE resp plntf RFA1.pdf' names active matter 28 defendant(s): CASOMB, HOPE, Palacios |
| 05 | Declaration Pal ISO Opposition.pdf | active_defendant_name | 07 | archived matter 05 filing 'Declaration Pal ISO Opposition.pdf' names active matter 07 defendant(s): Centerline |
| 05 | Declaration Pal ISO Opposition.pdf | active_defendant_name | 19 | archived matter 05 filing 'Declaration Pal ISO Opposition.pdf' names active matter 19 defendant(s): CDCR |
| 05 | Declaration Pal ISO Opposition.pdf | active_defendant_name | 28 | archived matter 05 filing 'Declaration Pal ISO Opposition.pdf' names active matter 28 defendant(s): CASOMB, HOPE, Palacios |
| 05 | Demurrer-(NEWpal) (052226)).pdf | active_defendant_name | 19 | archived matter 05 filing 'Demurrer-(NEWpal) (052226)).pdf' names active matter 19 defendant(s): CDCR |
| 05 | Demurrer-(NEWpal) (052226)).pdf | active_defendant_name | 28 | archived matter 05 filing 'Demurrer-(NEWpal) (052226)).pdf' names active matter 28 defendant(s): HOPE, Noguchi, Palacios |
| 05 | Demurrer-Decl (NEWpal) (052226)).pdf | active_defendant_name | 25 | archived matter 05 filing 'Demurrer-Decl (NEWpal) (052226)).pdf' names active matter 25 defendant(s): Federal Express |
| 05 | Demurrer-Decl (NEWpal) (052226)).pdf | active_defendant_name | 28 | archived matter 05 filing 'Demurrer-Decl (NEWpal) (052226)).pdf' names active matter 28 defendant(s): HOPE, Palacios |
| 05 | Demurrer-PO (NEWpal) (052226)).pdf | active_defendant_name | 25 | archived matter 05 filing 'Demurrer-PO (NEWpal) (052226)).pdf' names active matter 25 defendant(s): Federal Express |
| 05 | Demurrer-PO (NEWpal) (052226)).pdf | active_defendant_name | 28 | archived matter 05 filing 'Demurrer-PO (NEWpal) (052226)).pdf' names active matter 28 defendant(s): HOPE, Palacios |
| 05 | Demurrer-RJN (NEWpal) (052226)).pdf | active_defendant_name | 28 | archived matter 05 filing 'Demurrer-RJN (NEWpal) (052226)).pdf' names active matter 28 defendant(s): HOPE, Palacios |
| 05 | Demurrer-Reply (NEWpal) (070726).pdf | active_defendant_name | 19 | archived matter 05 filing 'Demurrer-Reply (NEWpal) (070726).pdf' names active matter 19 defendant(s): Board of Parole, CDCR |
| 05 | Demurrer-Reply (NEWpal) (070726).pdf | active_defendant_name | 25 | archived matter 05 filing 'Demurrer-Reply (NEWpal) (070726).pdf' names active matter 25 defendant(s): Federal Express |
| 05 | Demurrer-Reply (NEWpal) (070726).pdf | active_defendant_name | 28 | archived matter 05 filing 'Demurrer-Reply (NEWpal) (070726).pdf' names active matter 28 defendant(s): CASOMB, HOPE, Palacios |
| 05 | Demurrer-Reply Decl (NEWpal) (070726).pdf | active_defendant_name | 25 | archived matter 05 filing 'Demurrer-Reply Decl (NEWpal) (070726).pdf' names active matter 25 defendant(s): Federal Express |
| 05 | Demurrer-Reply Decl (NEWpal) (070726).pdf | active_defendant_name | 28 | archived matter 05 filing 'Demurrer-Reply Decl (NEWpal) (070726).pdf' names active matter 28 defendant(s): HOPE, Palacios |
| 05 | Evidentiary Pal Objections to Defendants RJN.pdf | active_defendant_name | 19 | archived matter 05 filing 'Evidentiary Pal Objections to Defendants RJN.pdf' names active matter 19 defendant(s): CDCR |
| 05 | Evidentiary Pal Objections to Defendants RJN.pdf | active_defendant_name | 28 | archived matter 05 filing 'Evidentiary Pal Objections to Defendants RJN.pdf' names active matter 28 defendant(s): HOPE, Palacios |
| 05 | FAC_STK-CV-UF-2026-1032.pdf | active_defendant_name | 07 | archived matter 05 filing 'FAC_STK-CV-UF-2026-1032.pdf' names active matter 07 defendant(s): Centerline |
| 05 | FAC_STK-CV-UF-2026-1032.pdf | active_defendant_name | 19 | archived matter 05 filing 'FAC_STK-CV-UF-2026-1032.pdf' names active matter 19 defendant(s): CDCR |
| 05 | FAC_STK-CV-UF-2026-1032.pdf | active_defendant_name | 28 | archived matter 05 filing 'FAC_STK-CV-UF-2026-1032.pdf' names active matter 28 defendant(s): CASOMB, HOPE, Noguchi, Palacios |
| 05 | Fee Waiver - Newanforbi v. Palacios, et al..pdf | active_defendant_name | 28 | archived matter 05 filing 'Fee Waiver - Newanforbi v. Palacios, et al..pdf' names active matter 28 defendant(s): Palacios |
| 05 | HOPE resp plntf FROGS1 (NEWpal) (061526).pdf | active_defendant_name | 19 | archived matter 05 filing 'HOPE resp plntf FROGS1 (NEWpal) (061526).pdf' names active matter 19 defendant(s): CDCR |
| 05 | HOPE resp plntf FROGS1 (NEWpal) (061526).pdf | active_defendant_name | 20 | archived matter 05 filing 'HOPE resp plntf FROGS1 (NEWpal) (061526).pdf' names active matter 20 defendant(s): Certification |
| 05 | HOPE resp plntf FROGS1 (NEWpal) (061526).pdf | active_defendant_name | 24 | archived matter 05 filing 'HOPE resp plntf FROGS1 (NEWpal) (061526).pdf' names active matter 24 defendant(s): Certification |
| 05 | HOPE resp plntf FROGS1 (NEWpal) (061526).pdf | active_defendant_name | 28 | archived matter 05 filing 'HOPE resp plntf FROGS1 (NEWpal) (061526).pdf' names active matter 28 defendant(s): CASOMB, HOPE, Noguchi, Palacios |
| 05 | HOPE resp plntf RFP1 (newpal) (061526).pdf | active_defendant_name | 19 | archived matter 05 filing 'HOPE resp plntf RFP1 (newpal) (061526).pdf' names active matter 19 defendant(s): CDCR |
| 05 | HOPE resp plntf RFP1 (newpal) (061526).pdf | active_defendant_name | 28 | archived matter 05 filing 'HOPE resp plntf RFP1 (newpal) (061526).pdf' names active matter 28 defendant(s): CASOMB, HOPE, Noguchi, Palacios |
| 05 | HOPE resp plntf SROGS1 (NEWpal) (061526).pdf | active_defendant_name | 19 | archived matter 05 filing 'HOPE resp plntf SROGS1 (NEWpal) (061526).pdf' names active matter 19 defendant(s): CDCR |
| 05 | HOPE resp plntf SROGS1 (NEWpal) (061526).pdf | active_defendant_name | 28 | archived matter 05 filing 'HOPE resp plntf SROGS1 (NEWpal) (061526).pdf' names active matter 28 defendant(s): HOPE, Palacios |
| 05 | Meet and Confer Letter 061626.pdf | active_defendant_name | 19 | archived matter 05 filing 'Meet and Confer Letter 061626.pdf' names active matter 19 defendant(s): CDCR |
| 05 | Meet and Confer Letter 061626.pdf | active_defendant_name | 28 | archived matter 05 filing 'Meet and Confer Letter 061626.pdf' names active matter 28 defendant(s): HOPE, Palacios |
| 05 | Notice of Change of Address (July 7, 2026).pdf | active_defendant_name | 28 | archived matter 05 filing 'Notice of Change of Address (July 7, 2026).pdf' names active matter 28 defendant(s): HOPE, Palacios |
| 05 | Opposition to Demurrer Pal.pdf | active_defendant_name | 19 | archived matter 05 filing 'Opposition to Demurrer Pal.pdf' names active matter 19 defendant(s): Macomber, CDCR |
| 05 | Opposition to Demurrer Pal.pdf | active_defendant_name | 28 | archived matter 05 filing 'Opposition to Demurrer Pal.pdf' names active matter 28 defendant(s): CASOMB, HOPE, Palacios |
| 05 | Order Sustaining Demurrer to FAC WOLA - Jul 15 2026.pdf | active_defendant_name | 25 | archived matter 05 filing 'Order Sustaining Demurrer to FAC WOLA - Jul 15 2026.pdf' names active matter 25 defendant(s): Federal Express |
| 05 | Order Sustaining Demurrer to FAC WOLA - Jul 15 2026.pdf | active_defendant_name | 28 | archived matter 05 filing 'Order Sustaining Demurrer to FAC WOLA - Jul 15 2026.pdf' names active matter 28 defendant(s): HOPE, Palacios |
| 05 | PALACIOS resp plntf FROGS1 (NEWpal) (061526).pdf | active_defendant_name | 19 | archived matter 05 filing 'PALACIOS resp plntf FROGS1 (NEWpal) (061526).pdf' names active matter 19 defendant(s): CDCR |
| 05 | PALACIOS resp plntf FROGS1 (NEWpal) (061526).pdf | active_defendant_name | 28 | archived matter 05 filing 'PALACIOS resp plntf FROGS1 (NEWpal) (061526).pdf' names active matter 28 defendant(s): HOPE, Noguchi, Palacios |
| 05 | PALACIOS resp plntf RFA1 (NEWpal) (060826).pdf | active_defendant_name | 19 | archived matter 05 filing 'PALACIOS resp plntf RFA1 (NEWpal) (060826).pdf' names active matter 19 defendant(s): CDCR |
| 05 | PALACIOS resp plntf RFA1 (NEWpal) (060826).pdf | active_defendant_name | 28 | archived matter 05 filing 'PALACIOS resp plntf RFA1 (NEWpal) (060826).pdf' names active matter 28 defendant(s): HOPE, Palacios |
| 05 | PALACIOS resp plntf RFP1 (NEWpal) (061526).pdf | active_defendant_name | 19 | archived matter 05 filing 'PALACIOS resp plntf RFP1 (NEWpal) (061526).pdf' names active matter 19 defendant(s): CDCR |
| 05 | PALACIOS resp plntf RFP1 (NEWpal) (061526).pdf | active_defendant_name | 28 | archived matter 05 filing 'PALACIOS resp plntf RFP1 (NEWpal) (061526).pdf' names active matter 28 defendant(s): HOPE, Noguchi, Palacios |
| 05 | PALACIOS resp plntf SROGS1 (NEWpal) (061226).pdf | active_defendant_name | 19 | archived matter 05 filing 'PALACIOS resp plntf SROGS1 (NEWpal) (061226).pdf' names active matter 19 defendant(s): CDCR |
| 05 | PALACIOS resp plntf SROGS1 (NEWpal) (061226).pdf | active_defendant_name | 28 | archived matter 05 filing 'PALACIOS resp plntf SROGS1 (NEWpal) (061226).pdf' names active matter 28 defendant(s): HOPE, Noguchi, Palacios |
| 05 | Plaintiff's Notice of Intent to Appear and Argue Tentative Ruling (July 13, 2026).pdf | active_defendant_name | 28 | archived matter 05 filing 'Plaintiff's Notice of Intent to Appear and Argue Tentative Ruling (July 13, 2026).pdf' names active matter 28 defendant(s): HOPE |
| 05 | RFA to Pl (NEWpal) (061826).pdf | active_defendant_name | 19 | archived matter 05 filing 'RFA to Pl (NEWpal) (061826).pdf' names active matter 19 defendant(s): CDCR |
| 05 | RFA to Pl (NEWpal) (061826).pdf | active_defendant_name | 25 | archived matter 05 filing 'RFA to Pl (NEWpal) (061826).pdf' names active matter 25 defendant(s): Federal Express |
| 05 | RFA to Pl (NEWpal) (061826).pdf | active_defendant_name | 28 | archived matter 05 filing 'RFA to Pl (NEWpal) (061826).pdf' names active matter 28 defendant(s): HOPE, Palacios |
| 05 | RFP to Pl (NEWpal) (061826).pdf | active_defendant_name | 19 | archived matter 05 filing 'RFP to Pl (NEWpal) (061826).pdf' names active matter 19 defendant(s): CDCR |
| 05 | RFP to Pl (NEWpal) (061826).pdf | active_defendant_name | 25 | archived matter 05 filing 'RFP to Pl (NEWpal) (061826).pdf' names active matter 25 defendant(s): Federal Express |
| 05 | RFP to Pl (NEWpal) (061826).pdf | active_defendant_name | 28 | archived matter 05 filing 'RFP to Pl (NEWpal) (061826).pdf' names active matter 28 defendant(s): HOPE, Palacios |
| 05 | RJN Pal ISO Opposition.pdf | active_defendant_name | 19 | archived matter 05 filing 'RJN Pal ISO Opposition.pdf' names active matter 19 defendant(s): Macomber, CDCR |
| 05 | RJN Pal ISO Opposition.pdf | active_defendant_name | 28 | archived matter 05 filing 'RJN Pal ISO Opposition.pdf' names active matter 28 defendant(s): CASOMB, HOPE, Palacios |
| 05 | SROG Set Two HOPE NEWpal .pdf | active_defendant_name | 19 | archived matter 05 filing 'SROG Set Two HOPE NEWpal .pdf' names active matter 19 defendant(s): CDCR |
| 05 | SROG Set Two HOPE NEWpal .pdf | active_defendant_name | 28 | archived matter 05 filing 'SROG Set Two HOPE NEWpal .pdf' names active matter 28 defendant(s): CASOMB, HOPE, Noguchi, Palacios |
| 05 | SROG Set Two PALACIOS NEWpal .pdf | active_defendant_name | 19 | archived matter 05 filing 'SROG Set Two PALACIOS NEWpal .pdf' names active matter 19 defendant(s): CDCR |
| 05 | SROG Set Two PALACIOS NEWpal .pdf | active_defendant_name | 28 | archived matter 05 filing 'SROG Set Two PALACIOS NEWpal .pdf' names active matter 28 defendant(s): HOPE, Noguchi, Palacios |
| 05 | SROGS to Pl (NEWpal) (061826).pdf | active_defendant_name | 25 | archived matter 05 filing 'SROGS to Pl (NEWpal) (061826).pdf' names active matter 25 defendant(s): Federal Express |
| 05 | SROGS to Pl (NEWpal) (061826).pdf | active_defendant_name | 28 | archived matter 05 filing 'SROGS to Pl (NEWpal) (061826).pdf' names active matter 28 defendant(s): HOPE, Palacios |
| 05 | Stipulated Protective Order SIGNED.pdf | active_defendant_name | 20 | archived matter 05 filing 'Stipulated Protective Order SIGNED.pdf' names active matter 20 defendant(s): Certification |
| 05 | Stipulated Protective Order SIGNED.pdf | active_defendant_name | 24 | archived matter 05 filing 'Stipulated Protective Order SIGNED.pdf' names active matter 24 defendant(s): Certification |
| 05 | Stipulated Protective Order SIGNED.pdf | active_defendant_name | 28 | archived matter 05 filing 'Stipulated Protective Order SIGNED.pdf' names active matter 28 defendant(s): HOPE, Palacios |
| 05 | Summons + Complaint - Newanforbi v. Palacios, et al. .pdf | active_defendant_name | 19 | archived matter 05 filing 'Summons + Complaint - Newanforbi v. Palacios, et al. .pdf' names active matter 19 defendant(s): CDCR |
| 05 | Summons + Complaint - Newanforbi v. Palacios, et al. .pdf | active_defendant_name | 28 | archived matter 05 filing 'Summons + Complaint - Newanforbi v. Palacios, et al. .pdf' names active matter 28 defendant(s): HOPE, Palacios |
| 05 | Tentative Ruling on Demurrer (posted July 13, 2026, hearing July 15, 2026).pdf | active_defendant_name | 28 | archived matter 05 filing 'Tentative Ruling on Demurrer (posted July 13, 2026, hearing July 15, 2026).pdf' names active matter 28 defendant(s): HOPE |
| 05 | Tentative Ruling on Demurrer RTF - Jul 10 2026.pdf | active_defendant_name | 28 | archived matter 05 filing 'Tentative Ruling on Demurrer RTF - Jul 10 2026.pdf' names active matter 28 defendant(s): HOPE, Palacios |
| 06 | 5. Notice of Related Cases.pdf | active_defendant_name | 19 | archived matter 06 filing '5. Notice of Related Cases.pdf' names active matter 19 defendant(s): Macomber |
| 06 | 5. Notice of Related Cases.pdf | active_defendant_name | 28 | archived matter 06 filing '5. Notice of Related Cases.pdf' names active matter 28 defendant(s): CASOMB, HOPE, Palacios |
| 06 | Notice of Voluntary Dismissal Newanforbi v HOPE.pdf | active_defendant_name | 19 | archived matter 06 filing 'Notice of Voluntary Dismissal Newanforbi v HOPE.pdf' names active matter 19 defendant(s): Macomber |
| 06 | Notice of Voluntary Dismissal Newanforbi v HOPE.pdf | active_defendant_name | 28 | archived matter 06 filing 'Notice of Voluntary Dismissal Newanforbi v HOPE.pdf' names active matter 28 defendant(s): CASOMB, HOPE |
| 08 | Civil Case Cover Sheet CM-010 (electronically filed May 18 2026).pdf | active_defendant_name | 01 | archived matter 08 filing 'Civil Case Cover Sheet CM-010 (electronically filed May 18 2026).pdf' names active matter 01 defendant(s): Candelaria |
| 08 | Civil Case Cover Sheet CM-010 (electronically filed May 18 2026).pdf | active_defendant_name | 07 | archived matter 08 filing 'Civil Case Cover Sheet CM-010 (electronically filed May 18 2026).pdf' names active matter 07 defendant(s): Candelaria |
| 08 | Civil Case Cover Sheet CM-010 (electronically filed May 18 2026).pdf | active_defendant_name | 20 | archived matter 08 filing 'Civil Case Cover Sheet CM-010 (electronically filed May 18 2026).pdf' names active matter 20 defendant(s): Candelaria |
| 08 | Court Minutes (Jul 17 2026) and Civil Case Cover Sheet CM-010 pp.2-3.pdf | active_defendant_name | 01 | archived matter 08 filing 'Court Minutes (Jul 17 2026) and Civil Case Cover Sheet CM-010 pp.2-3.pdf' names active matter 01 defendant(s): Candelaria |
| 08 | Court Minutes (Jul 17 2026) and Civil Case Cover Sheet CM-010 pp.2-3.pdf | active_defendant_name | 07 | archived matter 08 filing 'Court Minutes (Jul 17 2026) and Civil Case Cover Sheet CM-010 pp.2-3.pdf' names active matter 07 defendant(s): Candelaria |
| 08 | Court Minutes (Jul 17 2026) and Civil Case Cover Sheet CM-010 pp.2-3.pdf | active_defendant_name | 20 | archived matter 08 filing 'Court Minutes (Jul 17 2026) and Civil Case Cover Sheet CM-010 pp.2-3.pdf' names active matter 20 defendant(s): Candelaria, Certification |
| 08 | Court Minutes (Jul 17 2026) and Civil Case Cover Sheet CM-010 pp.2-3.pdf | active_defendant_name | 24 | archived matter 08 filing 'Court Minutes (Jul 17 2026) and Civil Case Cover Sheet CM-010 pp.2-3.pdf' names active matter 24 defendant(s): Certification |
| 08 | Court Minutes - Fee Waiver Hearing DENIED, Non-Appearance (Jul 17 2026).pdf | active_defendant_name | 01 | archived matter 08 filing 'Court Minutes - Fee Waiver Hearing DENIED, Non-Appearance (Jul 17 2026).pdf' names active matter 01 defendant(s): Candelaria |
| 08 | Court Minutes - Fee Waiver Hearing DENIED, Non-Appearance (Jul 17 2026).pdf | active_defendant_name | 07 | archived matter 08 filing 'Court Minutes - Fee Waiver Hearing DENIED, Non-Appearance (Jul 17 2026).pdf' names active matter 07 defendant(s): Candelaria |
| 08 | Court Minutes - Fee Waiver Hearing DENIED, Non-Appearance (Jul 17 2026).pdf | active_defendant_name | 20 | archived matter 08 filing 'Court Minutes - Fee Waiver Hearing DENIED, Non-Appearance (Jul 17 2026).pdf' names active matter 20 defendant(s): Candelaria |
| 08 | Newanforbi v. Candelaria Mandamus.pdf | active_defendant_name | 01 | archived matter 08 filing 'Newanforbi v. Candelaria Mandamus.pdf' names active matter 01 defendant(s): Candelaria, Highway Patrol, CHP |
| 08 | Newanforbi v. Candelaria Mandamus.pdf | active_defendant_name | 02 | archived matter 08 filing 'Newanforbi v. Candelaria Mandamus.pdf' names active matter 02 defendant(s): CHP, Highway Patrol |
| 08 | Newanforbi v. Candelaria Mandamus.pdf | active_defendant_name | 07 | archived matter 08 filing 'Newanforbi v. Candelaria Mandamus.pdf' names active matter 07 defendant(s): Candelaria, Highway Patrol, CHP |
| 08 | Newanforbi v. Candelaria Mandamus.pdf | active_defendant_name | 20 | archived matter 08 filing 'Newanforbi v. Candelaria Mandamus.pdf' names active matter 20 defendant(s): Candelaria, CHP |
| 08 | Newanforbi v. Candelaria Mandamus.pdf | active_defendant_name | 24 | archived matter 08 filing 'Newanforbi v. Candelaria Mandamus.pdf' names active matter 24 defendant(s): CHP |
| 08 | Notice of Change of Address (July 7, 2026).pdf | active_defendant_name | 01 | archived matter 08 filing 'Notice of Change of Address (July 7, 2026).pdf' names active matter 01 defendant(s): Candelaria |
| 08 | Notice of Change of Address (July 7, 2026).pdf | active_defendant_name | 07 | archived matter 08 filing 'Notice of Change of Address (July 7, 2026).pdf' names active matter 07 defendant(s): Candelaria |
| 08 | Notice of Change of Address (July 7, 2026).pdf | active_defendant_name | 20 | archived matter 08 filing 'Notice of Change of Address (July 7, 2026).pdf' names active matter 20 defendant(s): Candelaria |
| 08 | Order on Court Fee Waiver After Hearing - FW-008 (Jul 17 2026).pdf | active_defendant_name | 01 | archived matter 08 filing 'Order on Court Fee Waiver After Hearing - FW-008 (Jul 17 2026).pdf' names active matter 01 defendant(s): Candelaria |
| 08 | Order on Court Fee Waiver After Hearing - FW-008 (Jul 17 2026).pdf | active_defendant_name | 07 | archived matter 08 filing 'Order on Court Fee Waiver After Hearing - FW-008 (Jul 17 2026).pdf' names active matter 07 defendant(s): Candelaria |
| 08 | Order on Court Fee Waiver After Hearing - FW-008 (Jul 17 2026).pdf | active_defendant_name | 20 | archived matter 08 filing 'Order on Court Fee Waiver After Hearing - FW-008 (Jul 17 2026).pdf' names active matter 20 defendant(s): Candelaria |
| 09 | 26WM000028_Reply_to_Opp.pdf | active_defendant_name | 19 | archived matter 09 filing '26WM000028_Reply_to_Opp.pdf' names active matter 19 defendant(s): Macomber, CDCR |
| 09 | 31626-43188-NTCHNG_69ce9f1e7ab52 2.pdf | active_defendant_name | 01 | archived matter 09 filing '31626-43188-NTCHNG_69ce9f1e7ab52 2.pdf' names active matter 01 defendant(s): Highway Patrol |
| 09 | 31626-43188-NTCHNG_69ce9f1e7ab52 2.pdf | active_defendant_name | 02 | archived matter 09 filing '31626-43188-NTCHNG_69ce9f1e7ab52 2.pdf' names active matter 02 defendant(s): Highway Patrol |
| 09 | 31626-43188-NTCHNG_69ce9f1e7ab52 2.pdf | active_defendant_name | 07 | archived matter 09 filing '31626-43188-NTCHNG_69ce9f1e7ab52 2.pdf' names active matter 07 defendant(s): Highway Patrol |
| 09 | 31626-43188-NTCHNG_69ce9f1e7ab52 2.pdf | active_defendant_name | 19 | archived matter 09 filing '31626-43188-NTCHNG_69ce9f1e7ab52 2.pdf' names active matter 19 defendant(s): Macomber, Board of Parole, CDCR |
| 09 | Amended Notice of Hearing on Petition for Writ of Mandate.pdf | active_defendant_name | 01 | archived matter 09 filing 'Amended Notice of Hearing on Petition for Writ of Mandate.pdf' names active matter 01 defendant(s): Highway Patrol |
| 09 | Amended Notice of Hearing on Petition for Writ of Mandate.pdf | active_defendant_name | 02 | archived matter 09 filing 'Amended Notice of Hearing on Petition for Writ of Mandate.pdf' names active matter 02 defendant(s): Highway Patrol |
| 09 | Amended Notice of Hearing on Petition for Writ of Mandate.pdf | active_defendant_name | 07 | archived matter 09 filing 'Amended Notice of Hearing on Petition for Writ of Mandate.pdf' names active matter 07 defendant(s): Highway Patrol |
| 09 | Amended Notice of Hearing on Petition for Writ of Mandate.pdf | active_defendant_name | 19 | archived matter 09 filing 'Amended Notice of Hearing on Petition for Writ of Mandate.pdf' names active matter 19 defendant(s): Macomber, Board of Parole, CDCR |
| 09 | CU_26WM000028_e91359ab-2598-4573-a45a-fa7893fc4cb07.pdf | active_defendant_name | 19 | archived matter 09 filing 'CU_26WM000028_e91359ab-2598-4573-a45a-fa7893fc4cb07.pdf' names active matter 19 defendant(s): Macomber, CDCR |
| 09 | WOM FAC.pdf | active_defendant_name | 01 | archived matter 09 filing 'WOM FAC.pdf' names active matter 01 defendant(s): Highway Patrol |
| 09 | WOM FAC.pdf | active_defendant_name | 02 | archived matter 09 filing 'WOM FAC.pdf' names active matter 02 defendant(s): Highway Patrol |
| 09 | WOM FAC.pdf | active_defendant_name | 07 | archived matter 09 filing 'WOM FAC.pdf' names active matter 07 defendant(s): Highway Patrol |
| 09 | WOM FAC.pdf | active_defendant_name | 19 | archived matter 09 filing 'WOM FAC.pdf' names active matter 19 defendant(s): Macomber, Board of Parole, CDCR |
| 09 | WOM-Case Assignment.pdf | active_defendant_name | 19 | archived matter 09 filing 'WOM-Case Assignment.pdf' names active matter 19 defendant(s): Macomber |
| 09 | WOM-Fee Waiver.pdf | active_defendant_name | 19 | archived matter 09 filing 'WOM-Fee Waiver.pdf' names active matter 19 defendant(s): Macomber |
| 09 | WOM-efile.pdf | active_defendant_name | 19 | archived matter 09 filing 'WOM-efile.pdf' names active matter 19 defendant(s): Macomber |
| 09 | WOM_Opening Brief.pdf | active_defendant_name | 19 | archived matter 09 filing 'WOM_Opening Brief.pdf' names active matter 19 defendant(s): Macomber, CDCR |
| 09 | WOM_Opening Brief.pdf | active_defendant_name | 28 | archived matter 09 filing 'WOM_Opening Brief.pdf' names active matter 28 defendant(s): CASOMB, HOPE |
| 10 | Notice of Change of Address (July 7, 2026).pdf | active_case_number | 19 | archived matter 10 filing 'Notice of Change of Address (July 7, 2026).pdf' mentions active matter 19 case number |
| 10 | Notice of Change of Address (July 7, 2026).pdf | active_defendant_name | 19 | archived matter 10 filing 'Notice of Change of Address (July 7, 2026).pdf' names active matter 19 defendant(s): Macomber, CDCR |
| 14 | Newanforbi v Urrea.pdf | active_defendant_name | 01 | archived matter 14 filing 'Newanforbi v Urrea.pdf' names active matter 01 defendant(s): Highway Patrol, CHP |
| 14 | Newanforbi v Urrea.pdf | active_defendant_name | 02 | archived matter 14 filing 'Newanforbi v Urrea.pdf' names active matter 02 defendant(s): CHP, Highway Patrol |
| 14 | Newanforbi v Urrea.pdf | active_defendant_name | 07 | archived matter 14 filing 'Newanforbi v Urrea.pdf' names active matter 07 defendant(s): Centerline, Highway Patrol, CHP |
| 14 | Newanforbi v Urrea.pdf | active_defendant_name | 19 | archived matter 14 filing 'Newanforbi v Urrea.pdf' names active matter 19 defendant(s): Macomber, CDCR |
| 14 | Newanforbi v Urrea.pdf | active_defendant_name | 20 | archived matter 14 filing 'Newanforbi v Urrea.pdf' names active matter 20 defendant(s): CHP |
| 14 | Newanforbi v Urrea.pdf | active_defendant_name | 24 | archived matter 14 filing 'Newanforbi v Urrea.pdf' names active matter 24 defendant(s): CHP |
| 14 | Newanforbi v Urrea.pdf | active_defendant_name | 28 | archived matter 14 filing 'Newanforbi v Urrea.pdf' names active matter 28 defendant(s): Noguchi |
| 14 | Newanforbi v Urrea.pdf | active_defendant_name | 29 | archived matter 14 filing 'Newanforbi v Urrea.pdf' names active matter 29 defendant(s): Housing |
| 15 | 5417 CM010 Civil Case Cover Sheet.pdf | active_defendant_name | 20 | archived matter 15 filing '5417 CM010 Civil Case Cover Sheet.pdf' names active matter 20 defendant(s): Certification |
| 15 | 5417 CM010 Civil Case Cover Sheet.pdf | active_defendant_name | 24 | archived matter 15 filing '5417 CM010 Civil Case Cover Sheet.pdf' names active matter 24 defendant(s): Certification |
| 15 | 5417 Clerk s Certificate of Service by Mail.pdf | active_defendant_name | 20 | archived matter 15 filing '5417 Clerk s Certificate of Service by Mail.pdf' names active matter 20 defendant(s): Certification |
| 15 | 5417 Clerk s Certificate of Service by Mail.pdf | active_defendant_name | 24 | archived matter 15 filing '5417 Clerk s Certificate of Service by Mail.pdf' names active matter 24 defendant(s): Certification |
| 15 | 5417 Complaint.pdf | active_defendant_name | 19 | archived matter 15 filing '5417 Complaint.pdf' names active matter 19 defendant(s): Macomber, CDCR |
| 15 | 5417 Complaint.pdf | active_defendant_name | 28 | archived matter 15 filing '5417 Complaint.pdf' names active matter 28 defendant(s): Noguchi |
| 15 | 5417 SUM100 Summons - Civil.pdf | active_defendant_name | 28 | archived matter 15 filing '5417 SUM100 Summons - Civil.pdf' names active matter 28 defendant(s): Noguchi |
| 15 | CCP 430.41 Meet and Confer Calendar Invite (Gronna, Jul. 17, 2026).pdf | active_defendant_name | 19 | archived matter 15 filing 'CCP 430.41 Meet and Confer Calendar Invite (Gronna, Jul. 17, 2026).pdf' names active matter 19 defendant(s): CDCR |
| 15 | DODD.pdf | active_defendant_name | 19 | archived matter 15 filing 'DODD.pdf' names active matter 19 defendant(s): Macomber, Board of Parole, CDCR |
| 15 | DODD.pdf | active_defendant_name | 28 | archived matter 15 filing 'DODD.pdf' names active matter 28 defendant(s): Noguchi |
| 15 | Dodd.pdf | active_defendant_name | 19 | archived matter 15 filing 'Dodd.pdf' names active matter 19 defendant(s): Macomber, Board of Parole, CDCR |
| 15 | Dodd.pdf | active_defendant_name | 28 | archived matter 15 filing 'Dodd.pdf' names active matter 28 defendant(s): Noguchi |
| 15 | Newanforbi v Dodd RECALIBRATED.pdf | active_defendant_name | 07 | archived matter 15 filing 'Newanforbi v Dodd RECALIBRATED.pdf' names active matter 07 defendant(s): Centerline |
| 15 | Newanforbi v Dodd RECALIBRATED.pdf | active_defendant_name | 19 | archived matter 15 filing 'Newanforbi v Dodd RECALIBRATED.pdf' names active matter 19 defendant(s): Macomber, CDCR |
| 15 | Newanforbi v Dodd RECALIBRATED.pdf | active_defendant_name | 28 | archived matter 15 filing 'Newanforbi v Dodd RECALIBRATED.pdf' names active matter 28 defendant(s): HOPE, Noguchi |
| 15 | Newanforbi v. CDCR, et al.pdf | active_defendant_name | 07 | archived matter 15 filing 'Newanforbi v. CDCR, et al.pdf' names active matter 07 defendant(s): Centerline |
| 15 | Newanforbi v. CDCR, et al.pdf | active_defendant_name | 19 | archived matter 15 filing 'Newanforbi v. CDCR, et al.pdf' names active matter 19 defendant(s): Macomber, CDCR |
| 15 | Newanforbi v. CDCR, et al.pdf | active_defendant_name | 28 | archived matter 15 filing 'Newanforbi v. CDCR, et al.pdf' names active matter 28 defendant(s): HOPE, Noguchi |
| 15 | Newanforbi v. Dodd, et al..pdf | active_defendant_name | 07 | archived matter 15 filing 'Newanforbi v. Dodd, et al..pdf' names active matter 07 defendant(s): Centerline |
| 15 | Newanforbi v. Dodd, et al..pdf | active_defendant_name | 19 | archived matter 15 filing 'Newanforbi v. Dodd, et al..pdf' names active matter 19 defendant(s): Board of Parole, CDCR |
| 15 | Newanforbi v. Dodd, et al..pdf | active_defendant_name | 28 | archived matter 15 filing 'Newanforbi v. Dodd, et al..pdf' names active matter 28 defendant(s): HOPE, Noguchi |
| 15 | Newanforbi v. Dodd, et al.pdf | active_defendant_name | 07 | archived matter 15 filing 'Newanforbi v. Dodd, et al.pdf' names active matter 07 defendant(s): Centerline |
| 15 | Newanforbi v. Dodd, et al.pdf | active_defendant_name | 19 | archived matter 15 filing 'Newanforbi v. Dodd, et al.pdf' names active matter 19 defendant(s): Macomber, Board of Parole, CDCR |
| 15 | Newanforbi v. Dodd, et al.pdf | active_defendant_name | 28 | archived matter 15 filing 'Newanforbi v. Dodd, et al.pdf' names active matter 28 defendant(s): HOPE, Noguchi |
| 15 | Newanforbi v. Dodd.pdf | active_defendant_name | 19 | archived matter 15 filing 'Newanforbi v. Dodd.pdf' names active matter 19 defendant(s): Macomber, Board of Parole, CDCR |
| 15 | Newanforbi v. Dodd.pdf | active_defendant_name | 28 | archived matter 15 filing 'Newanforbi v. Dodd.pdf' names active matter 28 defendant(s): Noguchi |
| 15 | Notice of Change of Address (July 7, 2026).pdf | active_defendant_name | 19 | archived matter 15 filing 'Notice of Change of Address (July 7, 2026).pdf' names active matter 19 defendant(s): CDCR |
| 15 | Notice of Change of Address (July 7, 2026).pdf | active_defendant_name | 28 | archived matter 15 filing 'Notice of Change of Address (July 7, 2026).pdf' names active matter 28 defendant(s): Noguchi |
| 15 | Print_GCP_INTAKE_FORM.pdf | active_defendant_name | 19 | archived matter 15 filing 'Print_GCP_INTAKE_FORM.pdf' names active matter 19 defendant(s): Macomber, CDCR |
| 15 | Print_GCP_INTAKE_FORM.pdf | active_defendant_name | 28 | archived matter 15 filing 'Print_GCP_INTAKE_FORM.pdf' names active matter 28 defendant(s): HOPE, Noguchi |
| 15 | Request for Extension of Time in Newanforbi v. CDCR, Case No. STK-CV-UPI-2026-54.pdf | active_defendant_name | 19 | archived matter 15 filing 'Request for Extension of Time in Newanforbi v. CDCR, Case No. STK-CV-UPI-2026-54.pdf' names active matter 19 defendant(s): CDCR |
| 16 | Newanforbi v. Rojo.pdf | active_defendant_name | 19 | archived matter 16 filing 'Newanforbi v. Rojo.pdf' names active matter 19 defendant(s): Macomber, CDCR |
| 16 | Newanforbi v. Rojo.pdf | active_defendant_name | 28 | archived matter 16 filing 'Newanforbi v. Rojo.pdf' names active matter 28 defendant(s): Noguchi |
| 22 | Confidential Settlement Agreement and Release - Pilot (Signed Jul 14 2026).pdf | active_defendant_name | 29 | archived matter 22 filing 'Confidential Settlement Agreement and Release - Pilot (Signed Jul 14 2026).pdf' names active matter 29 defendant(s): Fair Employment, Housing |
| 22 | Demand Letter Newanforbi v Pilot Travel Centers.pdf | active_defendant_name | 20 | archived matter 22 filing 'Demand Letter Newanforbi v Pilot Travel Centers.pdf' names active matter 20 defendant(s): Certification |
| 22 | Demand Letter Newanforbi v Pilot Travel Centers.pdf | active_defendant_name | 24 | archived matter 22 filing 'Demand Letter Newanforbi v Pilot Travel Centers.pdf' names active matter 24 defendant(s): Certification |
| 22 | Post-adverse action notice - Pilot Travel Centers LLC 2.pdf | active_defendant_name | 29 | archived matter 22 filing 'Post-adverse action notice - Pilot Travel Centers LLC 2.pdf' names active matter 29 defendant(s): DFEH, Housing |
| 23 | HireRight Report to Macy's Corporate Services (Pre-Employment - BGC). Subject- C 2.pdf | active_defendant_name | 27 | archived matter 23 filing 'HireRight Report to Macy's Corporate Services (Pre-Employment - BGC). Subject- C 2.pdf' names active matter 27 defendant(s): Macy |
| 23 | Job Offer-Selling and Support Captain, Stockton Sherwood - Full Time.pdf | active_defendant_name | 27 | archived matter 23 filing 'Job Offer-Selling and Support Captain, Stockton Sherwood - Full Time.pdf' names active matter 27 defendant(s): Macy |
| 30 | CASOMB Complaint Submission – HOPE Psychotherapy, Inc. 2.pdf | active_defendant_name | 19 | archived matter 30 filing 'CASOMB Complaint Submission – HOPE Psychotherapy, Inc. 2.pdf' names active matter 19 defendant(s): CDCR |
| 30 | CASOMB Complaint Submission – HOPE Psychotherapy, Inc. 2.pdf | active_defendant_name | 28 | archived matter 30 filing 'CASOMB Complaint Submission – HOPE Psychotherapy, Inc. 2.pdf' names active matter 28 defendant(s): CASOMB, HOPE |
| 30 | CASOMB Complaint Submission – HOPE Psychotherapy, Inc. 3.pdf | active_defendant_name | 19 | archived matter 30 filing 'CASOMB Complaint Submission – HOPE Psychotherapy, Inc. 3.pdf' names active matter 19 defendant(s): CDCR |
| 30 | CASOMB Complaint Submission – HOPE Psychotherapy, Inc. 3.pdf | active_defendant_name | 28 | archived matter 30 filing 'CASOMB Complaint Submission – HOPE Psychotherapy, Inc. 3.pdf' names active matter 28 defendant(s): CASOMB, HOPE, Palacios |
| 30 | CASOMB Complaint Submission – HOPE Psychotherapy, Inc. 4.pdf | active_defendant_name | 19 | archived matter 30 filing 'CASOMB Complaint Submission – HOPE Psychotherapy, Inc. 4.pdf' names active matter 19 defendant(s): CDCR |
| 30 | CASOMB Complaint Submission – HOPE Psychotherapy, Inc. 4.pdf | active_defendant_name | 28 | archived matter 30 filing 'CASOMB Complaint Submission – HOPE Psychotherapy, Inc. 4.pdf' names active matter 28 defendant(s): CASOMB, HOPE |
| 30 | Complaint v9 Newanforbi v Moua NDCAL.pdf | active_defendant_name | 19 | archived matter 30 filing 'Complaint v9 Newanforbi v Moua NDCAL.pdf' names active matter 19 defendant(s): CDCR |
| 30 | Complaint v9 Newanforbi v Moua NDCAL.pdf | active_defendant_name | 27 | archived matter 30 filing 'Complaint v9 Newanforbi v Moua NDCAL.pdf' names active matter 27 defendant(s): Macy |
| 30 | Complaint v9 Newanforbi v Moua NDCAL.pdf | active_defendant_name | 28 | archived matter 30 filing 'Complaint v9 Newanforbi v Moua NDCAL.pdf' names active matter 28 defendant(s): CASOMB, HOPE, Noguchi |
| 30 | Complaint v9 Newanforbi v Moua NDCAL.pdf | active_defendant_name | 29 | archived matter 30 filing 'Complaint v9 Newanforbi v Moua NDCAL.pdf' names active matter 29 defendant(s): Housing |
| 30 | Job Offer-Selling and Support Captain, Stockton Sherwood - Full Time.pdf | active_defendant_name | 27 | archived matter 30 filing 'Job Offer-Selling and Support Captain, Stockton Sherwood - Full Time.pdf' names active matter 27 defendant(s): Macy |
| 30 | My Schedule.pdf | active_defendant_name | 27 | archived matter 30 filing 'My Schedule.pdf' names active matter 27 defendant(s): Macy |
| 30 | Newanforbi v. CDCR, et al 3.pdf | active_defendant_name | 19 | archived matter 30 filing 'Newanforbi v. CDCR, et al 3.pdf' names active matter 19 defendant(s): Macomber, CDCR |
| 30 | Newanforbi v. CDCR, et al 3.pdf | active_defendant_name | 28 | archived matter 30 filing 'Newanforbi v. CDCR, et al 3.pdf' names active matter 28 defendant(s): Noguchi |
| 30 | Proof of Service of Summons - Gary Noguchi (served Jul 7 2026).pdf | active_defendant_name | 28 | archived matter 30 filing 'Proof of Service of Summons - Gary Noguchi (served Jul 7 2026).pdf' names active matter 28 defendant(s): Noguchi |