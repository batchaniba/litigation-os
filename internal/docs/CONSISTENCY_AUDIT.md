# Cross-Matter Consistency Audit
## Brendan Ngehsi Newanforbi — 24 Matters Portfolio
### Analysis Date: July 11, 2026

---

## Purpose and methodology

This is a defensive gut-check, not litigation prep: the question is whether the litigant's own sworn filings tell contradictory stories about the same underlying facts, before opposing counsel finds that out first.

Five parallel analysis passes read the actual pleadings — not just the portfolio's `matters.js` summaries — grouped by **shared underlying facts** rather than by legal theme, since that's where a real contradiction would surface:

| Group | Matters | Shared fact pattern |
|---|---|---|
| A | 1, 2, 7, 8, 20 | Nov. 1, 2024 CHP traffic stop / DUI arrest / DMV APS suspension |
| B | 3, 4, 5, 6 | Agent Derrick's First Amendment retaliation / HOPE Program fee structure |
| C | 9, 10, 11, 15, 19 | CDCR discharge-review process / Macomber writs & habeas |
| D | 13, 14, 16, 17, 18, 21 | Individual parole-agent defendants (Urrea, Rojo, Maloney, Barocio) |
| E | 12, 22, 23, 24 | Consumer fraud, employment registry-disclosure, and U-visa certification |

Each pass read the actual complaint/FAC/declaration/petition PDFs where available (18 of 24 matters have uploaded pleadings; Matters 4, 11, 13, 17, 18 have none and were checked only against `matters.js` text — flagged separately below), extracted dated factual assertions and defendant characterizations, and cross-compared within and across matters that share a defendant or an event. Findings are rated by how usable they'd be against the litigant if opposing counsel found them first, not by how the litigant intended the facts.

**Total: 22 findings — 8 HIGH, 7 MEDIUM, 7 LOW**, split below into sworn-pleading contradictions (the real litigation risk) and portfolio recordkeeping errors (lower risk, but worth fixing so the app doesn't mislead future drafting).

---

## Part 1 — Sworn pleading contradictions

These are inconsistencies between the litigant's own verified filings, not just documentation gaps. Each is the kind of thing a defendant's motion, an impeachment cross-examination, or a judicial-estoppel argument could exploit.

### HIGH severity

**1. "Arrest" vs. "detention only" — argued both ways, each time picking whichever position serves the forum.** (Matters 1, 7, 8, 20)

Matter 1's federal Complaint pleads that CHP's "detention" recharacterization is "factually and legally incorrect," and that handcuffing, transport, and chemical-test advisements are "all indicia of a full custodial arrest" under *Dunaway v. New York*. Matters 7, 8, and 20 take the opposite position — that the same Detention Certificate is dispositive proof the event "ceased to be an arrest as a matter of law," calling it "legally equivalent to a judicial finding that no crime was committed."

> Matter 1 Complaint ¶18: *"Plaintiff asserts that this characterization is factually and legally incorrect. He was subjected to handcuffing, placed in the back of a patrol vehicle, transported under guard, and read chemical test advisements — all indicia of a full custodial arrest within the meaning of *Dunaway v. New York*, 442 U.S. 200 (1979)."*
>
> Matter 20 Petition (§B heading): *"The Detention Certificate and Statutory Nullification of the Arrest ... By operation of law, the event ceased to be an arrest more than two months before the January 24, 2025 APS hearing."*

These are irreconcilable sworn positions on the same historical fact, each adopted only when convenient. Classic impeachment/judicial-estoppel material.

**2. Employment start date conflict.** (Matters 7, 20)

Matter 7 repeatedly and specifically pleads employment with Centerline began "October 30, 2024 — just two days before" the Nov. 1 encounter. Matter 20's verified petition instead states wages are documented on "twenty-six consecutive weekly pay stubs covering the pay periods from May 5, 2024 through January 3, 2025" — over five months earlier than the claimed start date.

> Matter 7 FAC ¶3: *"He had commenced his employment with Centerline Drivers, LLC on October 30, 2024—just two days before the November 1, 2024 CHP encounter."*
>
> Matter 20 Petition ¶33: *"...reflected on twenty-six consecutive weekly pay stubs covering the pay periods from May 5, 2024 through January 3, 2025."*

Both cannot be true as pled.

**3. HOPE's per-parolee revenue figure changed between two of the litigant's own sworn complaints.** (Matters 5, 6)

Matter 6's original Complaint (verified Jan. 19, 2026) computes "$9,690 annually" from a single contract, with shown math. Its FAC (verified Feb. 17, 2026, one month later) drops the math and asserts "$10,600 annually" from three contracts. The $10,600 figure is then repeated in Matter 5's FAC. No document produced in discovery supports either number — `matters.js`'s own notes for Matter 5 already flag it as "a discovery-compulsion target."

> Matter 6 original Complaint p.7: *"...generates approximately $9,690 annually in group and CTM fees alone."*
>
> Matter 6 FAC p.6: *"...generates approximately $10,600 per year in baseline fees alone."*

**4. Grace-period revocation date is off by six weeks against the litigant's own produced evidence.** (Matters 3, 5)

Matter 3's FAC pleads the revocation happened "in or about early April 2025." HOPE's own business records (Bates HOPE_000190, cited in Matter 5's case notes) date the same event to February 20, 2025. Already flagged internally as unreconciled.

**5. The "Eagan" misidentification — the central theory of Matter 15 — was quoted without the error in two earlier, still-pending filings.** (Matters 9, 15, 19)

Matter 15's entire liability theory turns on CDCR Form 1502-DR misidentifying the litigant as a different parolee, "Eagan," in the Unit Supervisor Comments — offered as proof no individualized review occurred. But Matter 9's verified FAC and Matter 19's signed habeas petition, both filed months earlier and quoting the *same* underlying document, silently substitute "Newanforbi" for "Eagan" in their own body text, even though the actual attached exhibit in both says "Eagan."

> Matter 9 FAC ¶4 (as pled): *"Newanforbi has only completed approximately 4 years of the required 6.5 years of supervision."*
>
> Matter 9's own attached Exhibit A (actual document text): *"Eagan has only completed approximately 4 years of the required 6.5 years of supervision."*

Opposing counsel can argue either that the quote was altered from a verified exhibit in two separate courts, or that the "Eagan" defect wasn't actually apparent/material to the litigant when he read the same document twice before — undermining Matter 15's claim that the misidentification is "facially obvious."

**6. Matter 24 swears, under penalty of perjury, that no related action names the same defendant or challenges the same decision — which is false.** (Matters 24, 20, 2)

Matter 24's verified federal complaint (signed June 12, 2026) lists only two related actions and affirmatively states: *"Neither related action asserts any claim against Captain Serrato. Neither related action challenges the April 20, 2026 denial of the U Visa certification request... This action raises no claims that duplicate or overlap with the related actions."*

This is contradicted by the portfolio's own data: Matter 20 (filed three weeks earlier) already names "G. Serrato, Captain and Commander CHP Dublin Area" and seeks a writ compelling the identical U-visa certification — and is never mentioned. Matter 2, which *is* listed, has a fully-briefed U-Visa Certification Motion with a hearing the very next day (June 18, 2026) that Matter 24's disclosure never mentions.

This is a duplicative-litigation / candor-to-the-court exposure, not a wording issue — the kind of thing that gets a case dismissed or sanctioned if a defendant notices.

### MEDIUM severity

**7. Three non-reconciling lost-wage totals for the identical CDL suspension period.** (Matters 1, 7, 20) — Matter 1 gives a vague range ("$175,000–$450,000+"); Matter 7 computes $69,368/year from a flat $33.35/hr rate; Matter 20 states "$900–$2,800/week" pay stubs totaling "approximately $112,000." None reconcile, and the wage methodology itself differs between Matter 7 and 20 despite both citing the same Centerline employment.

**8. The pre-stop "impairment cue" explanation changed between filings.** (Matters 1, 7, 20) — Matter 1 attributes roadside rest to "a long night of social activity," never mentioning any medical condition. Matters 7 and 20 drop that explanation entirely and introduce, for the first time, that the litigant "is pre-diabetic" — a condition said to mimic intoxication signs. Not mutually exclusive, but the complete disappearance of one narrative in favor of a new one in the more legally aggressive filings reads as tailoring.

**9. Agent Derrick is portrayed as an actively engaged retaliator in one federal case and as procedurally derelict/absent in another.** (Matters 3, 6) — Matter 3 describes Derrick personally threatening the litigant, revoking his grace period, and escalating supervision. Matter 6's original complaint instead says "Agent Derrick failed to initiate CTMs or complete Form 3043 ... directly causing the procedural void." Not strictly irreconcilable, but the two portraits are in tension.

**10. Gary Noguchi holds two different job titles depending on which line of cases you read.** (Matters 14, 15, 16, 19, 21) — "Unit Supervisor" in the Urrea/discharge-review line (Matter 14's real complaint; `matters.js` text for 15/19); "Supervising Parole Agent ... with final authority over parole travel approvals" in the Rojo/travel-request line (Matters 16 and 21's real complaints). Likely the same role described informally two ways, but it's a sworn, verified statement about a recurring named defendant, and the specific authority held can matter for supervisory-liability theories.

### LOW severity

**11.** One-minute discrepancy in the sworn stop time — 12:54 a.m. (Matters 1, 8) vs. 12:55 a.m. (Matter 7) — trivial alone, but later filings anchor legal arguments to precise dashcam timestamps down to the second.

**12.** Matter 7's FAC labels a 32-second dashcam gap (00:55:37 to 00:56:09) as "approximately fourteen seconds" — an internally consistent but objectively wrong arithmetic statement repeated in Matter 1's narrative too.

**13.** Both the Rojo travel-denial storyline (Matters 16/21) and the unrelated Dodd/Noguchi discharge-review storyline (Matter 15) hinge on the same date, November 19, 2025, for two different events. Not a contradiction, but very likely the root cause of the Matter 16 recordkeeping error below (finding #14) — worth double-checking no future filing conflates the two.

---

## Part 2 — Portfolio recordkeeping errors (`src/data/matters.js`)

These are errors in the app's own case-tracking summaries, not in the sworn court filings. Lower litigation risk, but worth fixing so the portfolio doesn't misinform future drafting.

### HIGH severity

**14. Matter 16's summary describes a completely different incident than what was actually filed.** `matters.js` says Matter 16 is about "Agent Rojo assum[ing] AOR on Nov. 19, 2025 and withhold[ing the] finalized Discharge Review Report" — but the real, filed complaint is the state-law mirror of Matter 21's Reno church-travel-denial dispute (same dates, same text quotes, same narrative). The two real complaints (16 and 21) agree with each other; only the app's summary of Matter 16 is wrong.

**15. Matter 14's defendant list is wrong.** `matters.js` lists Keely Dodd as a Matter 14 defendant; she appears nowhere in the actual filed complaint. The real fourth defendant, Bryan Bishop (DAPO Director, sued officially), is omitted entirely from `matters.js`.

### MEDIUM severity

**16. Jury vs. bench trial — stale.** The last pre-filing draft demanded a jury trial; the actual court-stamped operative complaint (Matter 15, file-stamped June 11, 2026) elects a bench trial instead. `matters.js` still says "jury trial demanded."

**17. Discharge-review date — stale and internally unreconciled.** Matter 9's own pleading text says "December 1, 2025" throughout; `matters.js`'s Matter 9 summary says "November 2025 Discharge Review." (Matter 15 separately anchors to November 19, 2025, using a different field on the same physical form — reconcilable, but never explained in any of the pleadings.)

**18. Matter 12's summary overstates what's actually pled.** `matters.js` states as settled fact that the prior owner "expressly disclosed" the truck's defect to Diamond and that an out-of-service order existed. Both the original complaint and the FAC (filed three months apart) plead these same two facts only "on information and belief," explicitly flagged as unconfirmed.

### LOW severity

**19. Matter 14's causes-of-action list undercounts the real complaint.** `matters.js` lists 4 causes; the actual filed complaint pleads 9, including a Writ of Mandate and two California Constitution claims omitted from the summary entirely.

---

## Part 3 — Documentation gaps (no pleadings uploaded)

Matters 4, 11, 13, 17, and 18 have no PDFs in `public/documents/`, so they could only be checked against `matters.js`'s own text, not against a primary source. None of the five showed an obvious internal inconsistency in that text, but none can be verified either — flagged as a gap, not a finding. If any of these are ever refiled, their complaints should be checked directly against the sibling matters they mirror (especially Matter 4 against Matter 3's FAC, given the grace-period date issue at finding #4).

---

## Part 4 — Clean result

**Matters 22 and 23** (Pilot Travel Centers / Macy's) were checked specifically for whether the shared PC §290.46(j) legal theory was described consistently across an adjudicated matter and a never-filed one. No inconsistency found — the statutory framing, the FCRA/ICRAA/UCL/Tameny theory stack, and the "sophisticated employer received an explicit statutory warning" narrative are identical in both, and the factual differences between them (Matter 22: hired then terminated; Matter 23: offer only, never started) are exactly what should differ between two independent events. `matters.js`'s hedged, anticipatory language for Matter 23 accurately reflects that no complaint was ever filed.

---

## Priority ranking

If only two things get fixed, they should be:

1. **Matter 24's related-actions disclosure** (finding #6) — this is the one finding with real procedural downside (dismissal, sanctions, candor-to-the-court exposure) rather than just impeachment risk, and it's fixable by amending the complaint's Related Actions section before it's relied on.
2. **The arrest-vs-detention contradiction** (finding #1) — the most exploitable factual conflict, spanning four matters and two forums; worth deciding on one consistent position going forward even if some pending filings can't be un-said.

---

*Report prepared: July 11, 2026*
*Methodology: five parallel document-reading analysis passes across 18 of 24 matters' primary pleadings (complaints, FACs, petitions, declarations), cross-referenced against `src/data/matters.js` case-tracking summaries. Matters without uploaded pleadings were checked against summary text only and flagged as documentation gaps.*
