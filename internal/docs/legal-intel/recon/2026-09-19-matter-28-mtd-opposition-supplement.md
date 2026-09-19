# Matter 28 — MTD opposition supplement (Sep. 19, 2026)
## *Newanforbi v. Shannon Smith, LCSW, CEO, et al.*, N.D. Cal. No. 3:26-cv-07504-LJC

**Compiled 2026-09-19, two days before the responsive-pleading deadline.** Doctrinal research memorandum; not legal advice; requester is pro se. Nothing here was filed or served.

Read after `2026-09-12-matter-28-UNIFIED.md` (the spine) and `2026-09-18-matter-28-mtd-opposition-deep-research.md` (the strategy). This file does four things the earlier passes did not:

1. Records that the September 18 research was **deleted from `main`** and has been restored.
2. Pins the **Rule 12 evidentiary gateway** — the doctrine the preclusion fight will actually be decided through, and the largest gap in the prior passes.
3. Closes two long-open text queues: **Penal Code § 3008(d)(2)** and **15 C.C.R. § 3574**.
4. Flags a **direct conflict** between the September 18 memo and the audited safe-cite list on *Estate of Esche*, and corrects three cite forms.

---

## 0. Research-integrity finding — the September 18 work was silently deleted

`main` lost 1,856 lines of research on September 18, 2026 at 22:52 PDT.

Commit `f264f2e` — **PR #876, "Matter 41: Nuro, Inc. — pending pre-dispute monitoring file"** — was built from a base predating PRs #870–#873 and, on merge, deleted files it never mentions:

| File | Lines | Matter |
|---|---:|---|
| `legal-intel/recon/2026-09-18-matter-28-mtd-opposition-deep-research.md` | 734 | **28** |
| `matter-28-eval/MTD_OPPOSITION_RESEARCH_ARCHITECTURE_Sep18.md` | 330 | **28** |
| `legal-intel/recon/2026-09-18-cluster-05-carrillo-vons-asurint-stress-test.md` | 792 | Cluster 5 |
| `counsel/raymond-y-kim.md` + `.json` | 145 | Matter 29 intel |

It also reverted in-place edits to `README.md`, `PC_29046_EMPLOYMENT_CASES.md`, `counsel/matter29/STANZICK_FREDERICK.md`, `clusters/05-screening-locked-facts.md`, `legal-intel/matters/27.md`, and stripped the September 18 pointer paragraph out of the UNIFIED spine.

The two **Matter 28** files and the UNIFIED pointer are restored on this branch, byte-identical to `f5dc00e` / `e8d9ba9`. **The cluster-5 and Matter 29 files are still missing from `main`** and are out of this task's scope — recover them with:

```
git checkout 24d0dcc -- internal/docs/legal-intel/recon/2026-09-18-cluster-05-carrillo-vons-asurint-stress-test.md
git checkout e96ceaa -- internal/docs/legal-intel/counsel/raymond-y-kim.md internal/docs/legal-intel/counsel/raymond-y-kim.json
```

**Process note.** Nothing in the repo caught this. `validate-portfolio` checks data, not prose; the pre-push hook has no "did this PR delete research it does not mention" gate. Any PR whose diffstat shows deletions in `internal/docs/legal-intel/` that its own message does not describe should be treated as a stale-base clobber until proven otherwise.

---

## 1. The clock, derived forward from Monday

The answer is due **Monday, September 21, 2026** (Rule 12(a)(1)(A)(i), 21 days from the August 31 acceptance Van Dine confirmed). Martinez memorialized on September 11 that meet-and-confer is exhausted and motion practice is unavoidable. Assume a Rule 12(b)(6) motion, not an answer.

If the motion is filed Monday, these follow from the N.D. Cal. Civil Local Rules:

| Event | Rule | Date |
|---|---|---|
| Motion filed | — | Mon. Sep. 21, 2026 |
| **Opposition due** | **Civ. L.R. 7-3(a)** — 14 days after the motion is filed | **Mon. Oct. 5, 2026** |
| Reply due | Civ. L.R. 7-3(c) — 7 days after opposition | Mon. Oct. 12, 2026 |
| Joint CMC statement | Dkt. 4 | Thu. Oct. 15, 2026 |
| **Initial CMC** | Dkt. 4 | **Thu. Oct. 22, 2026, 1:30 p.m.** |
| Earliest noticeable hearing | Civ. L.R. 7-2(a) — not less than 35 days after filing | on/after Mon. Oct. 26, 2026 |

Two consequences the earlier passes did not draw:

- **The opposition is due before the CMC statement, and the MTD will still be pending at the CMC.** He will appear October 22 with the motion fully briefed and undecided. The joint CMC statement (Oct. 15) is written in the shadow of his own opposition — the two papers must not contradict each other on what the state court decided, on Matter 6, or on the wage allocation with Matter 26.
- **Fourteen days is the real constraint.** The opposition cannot be researched from scratch on October 5. The architecture file's §XVII checklist is the intake protocol; run it the day the motion lands.

Verify the hearing date against Judge Cisneros's actual civil motion calendar and standing order when the notice issues — L.R. 7-2 sets a floor, not the date.

---

## 2. The Rule 12 evidentiary gateway — the biggest gap in the prior passes

Every earlier memo argues *what* the state court decided. None of them argues *how the district court is permitted to find that out on a motion to dismiss.* That is the fight.

Defendants cannot prove preclusion from the four corners of the complaint. They must put the Matter 5 tentative, minute order, and defense-drafted formal order in front of Judge Cisneros — almost certainly by a Request for Judicial Notice. The doctrine governing that request is where this motion is won or lost, and it is strongly favorable.

### 2.1 Preclusion is an affirmative defense; the bar must be obvious on the face of the complaint

***ASARCO, LLC v. Union Pacific Railroad Co.*, 765 F.3d 999, 1004 (9th Cir. 2014):** "Dismissal under Rule 12(b)(6) on the basis of an affirmative defense is proper only if the defendant shows some obvious bar to securing relief on the face of the complaint." If the complaint's allegations together with judicially noticeable material leave the defense raising **disputed issues of fact**, Rule 12(b)(6) dismissal is improper. Claim preclusion may be reached on a motion to dismiss only where "the defense raises no disputed issues of fact."

This is the frame for the whole preclusion section. It converts every gap in their showing into a reason to deny rather than a matter to brief on the merits:

- Whether a judgment of dismissal was ever entered in STK-CV-UF-2026-0001032 — disputed.
- Whether the actual basis of the state adjudication was exhaustion/prematurity or § 430.10(e) insufficiency — disputed, because the tentative, minute order, and the prevailing party's own proposed order do not say the same thing.
- Whether Shannon Smith stands in privity with HOPE — disputed, and their burden.

Each of those is a fact question. Under *ASARCO*, that is the end of a Rule 12 preclusion defense, without the court needing to resolve *Perez*, *Heath*, or *Costello* at all. Lead the preclusion argument here, then give the merits kill (UNIFIED § 5.2) as the alternative the court should write down anyway.

### 2.2 Judicial notice proves existence, not truth

***Lee v. City of Los Angeles*, 250 F.3d 668 (9th Cir. 2001):** a court may notice matters of public record, but may not notice **the truth of disputed factual matters** contained in them. The district court in *Lee* was reversed for doing exactly that. Pin the year as **2001** — several secondary sources print 2000; confirm against the reporter before filing.

Applied here: Judge Cisneros may notice **that** the formal order exists and **that** it contains the sentence "fails to allege facts sufficient to state any cause of action." She may not notice **that the state court so held** — because the tentative and the minute order in the same record say the ground was a jurisdictional exhaustion precondition unmet "prior to the filing of" the FAC. The recital's accuracy is the disputed fact. That is a one-sentence argument, and it defeats the strongest version of their paper.

### 2.3 *Khoja* is the controlling framework, and it was written about this abuse

***Khoja v. Orexigen Therapeutics, Inc.*, 899 F.3d 988 (9th Cir. 2018)** is the Ninth Circuit's governing treatment of both exceptions to the four-corners rule. Three usable propositions:

1. District courts generally may **not** consider material outside the pleadings on Rule 12(b)(6); the only doors are incorporation by reference and Rule 201 judicial notice.
2. A court may notice public records **but not disputed facts within them** — the same rule as *Lee*, restated and enforced.
3. The court expressly criticized a "concerning pattern" of litigants "exploiting these procedures improperly to defeat what would otherwise constitute adequately stated claims at the pleading stage."

Point 3 is the tone of the section. Do not accuse counsel of bad faith; quote *Khoja* and let the framing do the work.

**Incorporation by reference cuts the other way too.** *Khoja* holds the doctrine exists to stop a plaintiff from cherry-picking a document. If Defendants lodge the formal order, the **entire state record they rely on comes in** — tentative, minute order, and register. Do not resist their RJN of the state papers. Ask the Court to take the whole record, and lodge the tentative, the minute order, and the register print yourself under the same request. Their best sentence is quarantined only when the court reads it next to the court's own words.

### 2.4 Section order for the opposition's preclusion argument

Restructure the architecture file's Argument I as:

1. Preclusion is an affirmative defense; Rule 12 reaches it only on an obvious, undisputed bar (*ASARCO*).
2. The Court may notice the state papers' existence but not the truth of the prevailing party's recital (*Lee*, *Khoja*); the whole record comes in together.
3. On that record, there is no judgment of dismissal (*Berri*; *Valvo*; CCP § 581d; *Kay*, 504 F.3d at 808).
4. The actual basis was a jurisdictional precondition — not merits (*Perez*; *Heath*, 708 F.2d at 1380 n.4; *Costello*; Restatement (Second) of Judgments § 20(2)).
5. § 1983 requires no state administrative exhaustion (*Patsy*), so the one issue actually decided is not an element of any federal claim.
6. Smith was not a party and privity is theirs to prove (*DKN Holdings*; *Taylor v. Sturgell*).

Steps 1–2 are new. They are also the cheapest win in the brief.

---

## 3. Statutory and regulatory machinery — queues closed

Two items were flagged "pin before briefing" on September 12 (leginfo was egress-blocked) and again on September 18. Both are now confirmed from secondary sources. **Both still need a primary-source read before they go in a filed paper** — see § 8.

### 3.1 Penal Code § 3008(d)(2) — confirmed

For persons placed on parole **on or after July 1, 2012**, the period in the sex offender management program "shall be not less than one year, up to the entire period of parole," and **the length of that period is determined by the certified sex offender management professional in consultation with the parole officer and as approved by the court.** Participation follows the standards developed under § 9003.

That is the statutory hook, and it is better than the September 12 paraphrase. Three things follow:

- The statute assigns the duration decision to **a private certified professional**, not to CDCR alone. That is the state-action allegation stated in the Legislature's own words.
- The statute contemplates an **individualized** determination ("in consultation," "as approved by the court"). A blanket rule that no one graduates before the parole term ends does not exercise that discretion; it removes it. This is the § 3008 argument *Dwyer* reached, and it survives without *Dwyer*.
- "**not less than one year, up to** the entire period of parole" is a range. A policy that always selects the ceiling is the allegation.

Do **not** convert this into a federal right to graduate at one year. § 3008 defines the state-created process; the constitutional theory is that the process was replaced by a predetermined result and false inputs. The September 18 memo's § VIII framing is correct and should not be loosened.

### 3.2 15 C.C.R. § 3574 — confirmed, with a date caveat that matters

Adopted by CDCR rulemaking **NCR 25-01 (dated January 3, 2025)**, which adopts § 3574 into Title 15 "concerning the three treatment phases included in the sex offender management program, pursuant to Penal Code section 3008(d)." Confirmed operative text:

- A determination to **retain** a participant "shall be supported by good cause, as defined in Section 3000."
- The retention determination "shall be stated in writing, **signed by the sex offender treatment provider and parole agent** on the **CDCR Form 3043** Containment Team Meeting / Earned Discharge Consideration Committee (**Rev. 11/24**), which is incorporated by reference."
- The completed form "shall be delivered to the supervised person **within 30 calendar days** of the CTM" and maintained in the file.
- Retention reasons "may include, but are not limited to" an LS/CMI score of 11 or higher under § 3573.

This is the strongest single piece of the state-action theory, and better than the September 18 characterization. The regulation does not merely permit provider input — it makes the **provider's signature** a required element of a written state retention decision on a state form incorporated into the California Code of Regulations. The "three treatment phases" framing ties the regulation directly to the blanket-phase allegation.

It also supplies a clean procedural-due-process spine: a mandatory written good-cause determination, on a specified form, signed by both the provider and the agent, delivered to the supervised person within 30 days. Those are ascertainable process requirements — allege which ones were not met and what false inputs drove the ones that were.

**Date caveat — do not skip this.** NCR 25-01 is dated January 3, 2025, and the permanent regulation took effect during 2025. The cluster-2 locked facts put the grace-period revocation at **February 20, 2025** and Form 1502-DR at **November 14, 2025**; the "ringleader"/"abhorrent" statements are **August 19, 2025**. Some of that conduct may predate § 3574's operative date. Before briefing:

- Pin the **operative date** of § 3574 from the OAL filing, not from the notice date.
- For conduct predating it, rely on § 3008(d)(2) (in force since 2012) and the emergency/predecessor regulation, not on § 3574.
- Do not allege that § 3574 governed a CTM that happened before it took effect. That is exactly the kind of overclaim the safe-cite discipline exists to prevent.

---

## 4. State action — three pins the prior passes did not have

The September 18 theory is right. These make it citable.

### 4.1 The sentence to build the section around

***Rawson v. Recovery Innovations, Inc.*, 975 F.3d 742, 753 (9th Cir. 2020):** "private parties may act under color of state law when the state significantly involves itself in the private parties' actions and decisionmaking at issue."

That is the pin — **753**, not a bare cite to 742. The phrase "decisionmaking at issue" is the whole Matter 28 theory in the Ninth Circuit's own words, and it maps onto § 3574's signature requirement without translation. *Rawson* found a close nexus on a combination of factors including the necessity of state imprimatur to continue the deprivation, a statutory command to render treatment, reliance on the State's police power, and extensive involvement of a government official. Track those factors in the opposition; four of the five have a § 3574 or § 3008 analogue.

### 4.2 The four tests, properly attributed

***Kirtley v. Rainey*, 326 F.3d 1088, 1092 (9th Cir. 2003):** public function; joint action; governmental compulsion or coercion; governmental nexus. The central question remains whether the alleged infringement is "fairly attributable to the government." Cite *Kirtley* for the framework rather than deriving it from *Rawson* — it is the cleaner pin and the one the district courts use.

Matter 28 should run **joint action** and **governmental nexus** as the leads, with public function as a fallback. Do not lead with public function; it is the test most vulnerable to *Merrill* and *Gross*.

### 4.3 The conduct-specific rule — and its double edge

***Caviness v. Horizon Community Learning Center, Inc.*, 590 F.3d 806 (9th Cir. 2010):** the nexus inquiry "begins by identifying the specific conduct of which the plaintiff complains," because "an entity may be a State actor for some purposes but not for others."

This is the doctrinal basis for the September 18 instruction to reframe away from corporate status and onto retention decisionmaking. **But brief it carefully: *Caviness* found the charter school was *not* a state actor for the employment conduct at issue.** Expect Defendants to cite it against him. Take it first, concede its rule, and apply the rule to the right conduct: HOPE's treatment of Plaintiff as a paying private client would be one thing; HOPE's signature on a Form 3043 retention determination that the State requires and that governs a compulsory parole condition is another. *Caviness* is the reason that distinction is legally operative rather than rhetorical.

---

## 5. Corrections and conflicts in the September 18 memo

The September 18 research is sound. Five items need fixing before any of it reaches paper.

### 5.1 *Estate of Esche* — direct conflict with the audited safe-cite list

The September 18 memo calls *Estate of Esche v. Bunuel-Jordana* (9th Cir. Sept. 29, 2025) "the most useful fresh Ninth Circuit authority" and builds QI Step 1 on it.

`MATTER_28_SAFE_CITE_LIST.md` flags the same case **MISCHARACTERIZED**, on four separate pages of an existing memo: "**REASONING only — holding is jurisdictional, not QI threshold.**" Its "briefing leads" line says to "cite *Estate of Esche* only for its reasoning, not as a QI-threshold holding."

**The safe-cite list governs.** `legal-intel/matters/28.md` says to pull from it "only," and it is the product of a completed citation audit; the September 18 memo is a research pass that did not run against it.

Practical resolution: the QI section stands on ***Richardson v. McKnight*, 521 U.S. 399 (1997)**, ***Halvorsen v. Baird*, 146 F.3d 680 (9th Cir. 1998)**, ***Jensen v. Lane County*, 222 F.3d 570 (9th Cir. 2000)**, ***Ace Beverage*, 144 F.3d 1218 (9th Cir. 1998)**, and ***Clement v. City of Glendale*, 518 F.3d 1090 (9th Cir. 2008)**, distinguishing ***Filarsky v. Delia*, 566 U.S. 377 (2012)**. All are SAFE. *Esche* may be cited for its reasoning about why the rationales for qualified immunity do not transfer to private parties — never as a holding on the QI threshold, and never as the section's anchor.

Independent verification of *Esche*'s disposition was **not possible in this environment** — the Ninth Circuit CDN, FindLaw, Justia, CourtListener, and the California Appellate Report are all blocked by the egress proxy. Until someone reads the opinion, the safe-cite list's audited determination is the operative one.

### 5.2 *Wicklund* — the characterization is not supported and may be wrong

The September 18 memo describes *Wicklund v. Idaho Department of Correction*, 623 F. App'x 338 (9th Cir. 2015) as a case where a supervised person engaged in litigation and speech outside treatment was threatened with incarceration, and where the Ninth Circuit "affirmed denial of QI on the retaliation theory."

What is verifiable: the Ninth Circuit appeal is **No. 12-35294, decided November 23, 2015**; Mark Wicklund was a convicted sex offender suspected of violating probation in January 2008, arrested by his probation officer, jailed, and taken to James F. Page for a polygraph; the decision recites the five-element First Amendment retaliation standard. The QI disposition described in the memo is **not confirmed**, and there are at least three related Wicklund district-court actions (*v. Page*, *v. Ada County*, *v. Huntsman*) that are easy to conflate.

Treat *Wicklund* as **UNVERIFIED** until the memorandum disposition is read. It is unpublished and non-precedential in any event (9th Cir. R. 36-3), so it can never be more than persuasive. The retaliation section does not need it: ***Watison v. Carter*, 668 F.3d 1108 (9th Cir. 2012)**, ***Brodheim v. Cry*, 584 F.3d 1262 (9th Cir. 2009)**, and ***Pratt v. Rowland*, 65 F.3d 802 (9th Cir. 1995)** are published and carry the argument. Do not let an unverified unpublished memo appear in the "clearly established" string — that is precisely where a bad cite is fatal.

### 5.3 *Medical Marijuana, Inc. v. Horn* — official cite, and what it did not do

Now reportable as ***Medical Marijuana, Inc. v. Horn*, 604 U.S. 593 (2025)** (No. 23-365, decided April 2, 2025). Stop citing it by docket number.

It was **5–4**. It holds that a plaintiff may seek treble damages for business or property loss even where the loss resulted from a personal injury. It expressly **preserves** civil RICO's proximate-cause limitation barring claims where the harm is too remote, and Justice Barrett's majority declined to decide whether Horn's injury was personal, whether his "business" encompassed his employment, or whether he suffered a property injury.

So the September 18 warning is confirmed and should be stated more sharply: *Horn* removes a categorical bar and decides nothing about this case's causal chain. *Anza v. Ideal Steel Supply Corp.*, 547 U.S. 451 (2006), and *Canyon County v. Syngenta Seeds, Inc.*, 519 F.3d 969 (9th Cir. 2008), are undisturbed. The billing-fraud-on-CDCR theory still has CDCR as its direct victim. **Keep RICO last and lean, and plead the leave-to-amend fallback in the same breath.**

### 5.4 Bane Act — add the Ninth Circuit pin

***Sandoval v. County of Sonoma*, 912 F.3d 509 (9th Cir. 2018)** is the federal-court pin for *Cornell*'s specific-intent standard, and it is better than citing *Cornell* alone to a federal judge. Two-part inquiry: whether the right is clearly delineated and plainly applicable, and whether the defendant acted with the particular purpose of depriving the victim of it. Specific intent is satisfied by **reckless disregard** of the right, "even if the defendant did not in fact recognize the unlawfulness of his act." The Ninth Circuit confined the independent-coercion rule to cases of merely **negligent** violations — which is the answer to *Shoyoye*.

Caption caution: this case is also reported as *Mateos-Sandoval* and the Ninth Circuit posted the opinion under *Sandoval v. City of Santa Rosa* (No. 16-16122, Dec. 21, 2018). Confirm the caption form against the F.3d reporter before filing.

### 5.5 Pro se construction and leave to amend — pin both

- ***Hebbe v. Pliler*, 627 F.3d 338, 342 & n.7 (9th Cir. 2010)** — pro se pleadings are liberally construed, and liberal construction remains appropriate **after *Iqbal***. The footnote is the point; cite it as `342 & n.7`.
- ***Lopez v. Smith*, 203 F.3d 1122, 1130–31 (9th Cir. 2000) (en banc)** — before dismissing, the court should identify the deficiencies and give an opportunity to cure if it appears at all possible the defects can be corrected; leave is unnecessary only where amendment would be futile.

These belong in the Rule 12 standard section at the front and in the leave-to-amend conclusion at the back. They are the reason the Rule 9(b) exposure on fraud is a survivable problem rather than a case-ending one.

Pair with ***Moore v. Kayport Package Express, Inc.*, 885 F.2d 531 (9th Cir. 1989)** on Rule 9(b): particularity "may be relaxed as to matters within the opposing party's knowledge," and information-and-belief allegations can satisfy the rule when "accompanied by a statement of the facts on which the belief is founded." *Moore* also shows the limit — the plaintiffs there still lost because they could not say who received what. Use it to justify pleading HOPE's internal billing and reporting practices on information and belief **with the Bates-numbered basis stated**, not to excuse a thin fraud count.

---

## 6. Defenses nobody previewed

Van Dine's September 3 letter named seven grounds. These were not among them. Two are non-issues; say so once in the CMC statement rather than briefing them unprompted.

### 6.1 Statute of limitations — not a live risk on the pleaded conduct

§ 1983 borrows California's personal-injury limitation: **two years**, Cal. Civ. Proc. Code § 335.1; *Jones v. Blanas*, 393 F.3d 918 (9th Cir. 2004). Accrual is when the plaintiff knows or has reason to know of the injury.

The complaint was filed **July 20, 2026**. The anchor conduct — the February 20, 2025 grace-period revocation, the August 19, 2025 statements, the November 14, 2025 Form 1502-DR — is all within two years. Bane Act is likewise two years; fraud is three (CCP § 338(d)); RICO is four. **Nothing pleaded is time-barred.**

The exposure is the other direction: the key facts describe a ten-year supervision relationship and HOPE discovery running to HOPE_000542. If the opposition or an amended pleading reaches back to conduct before **July 20, 2024** to establish the blanket policy, that older conduct is background and notice evidence, not a timely claim. Plead it as such. Do not invite a continuing-violation fight — the doctrine is narrow and rarely applied in § 1983 actions.

### 6.2 *Rooker-Feldman* — available to them, and meritless

If they reach for it: ***Exxon Mobil Corp. v. Saudi Basic Industries Corp.*, 544 U.S. 280 (2005)** confines the doctrine to cases brought by a state-court loser seeking federal-court review and rejection of a state judgment. Matter 28 does not ask Judge Cisneros to review or overturn the July 15 order; it pleads federal claims against a defendant who was not a state-court party, on conduct the state court never adjudicated. And there is no state **judgment** to be reviewed — the same record gap that defeats claim preclusion defeats *Rooker-Feldman* twice over.

One paragraph, held in reserve. Do not brief it unless they raise it.

### 6.3 Already covered elsewhere — do not re-research

*Heck* / habeas exclusivity is handled at deep-research § XII (*Wilkinson v. Dotson*, 544 U.S. 74 (2005)). Penal Code § 9003(c) immunity is handled at UNIFIED § 9 — it immunizes certified professionals for **patients'** crimes, not the vendor's own constitutional torts.

---

## 7. What changed in the ranking

| Issue | Sep. 18 assessment | Sep. 19 |
|---|---|---|
| Preclusion | Strong rebuttal | **Stronger** — *ASARCO* + *Lee* / *Khoja* win it at Rule 12 without reaching *Perez* |
| State action | Materially strengthened | **Stronger and now citable** — *Rawson* at 753; § 3574 signature requirement confirmed |
| Monell | Strong once gate cleared | Unchanged |
| Retaliation | Potentially strongest count | Unchanged; **drop *Wicklund*** from the string until verified |
| QI | Stronger after *Esche* | **Downgraded** — *Esche* is reasoning only; the *Richardson* line carries it |
| Due process | Needs disciplined framing | **Improved** — § 3574's written / signed / 30-day requirements are concrete process |
| Bane | Viable if falsification specific | Unchanged; add *Sandoval* pin |
| Fraud / negligent misrep. | Vulnerable, curable | Unchanged; *Moore* + *Lopez* make the cure explicit |
| RICO | Proximate cause structural defect | Unchanged; *Horn* at 604 U.S. 593 confirms it did not help on causation |

The center of gravity moved **earlier in the brief**. The September 18 memo's best insight — that Defendants are asking the Court to resolve factual questions against the pleader at Rule 12 — is not just a theme. Under *ASARCO*, *Lee*, and *Khoja*, it is a rule of decision. Say it in the introduction, prove it in Argument I, and repeat it at each gateway.

---

## 8. Verification status

Everything below was confirmed this pass through search-result summaries, **not** by reading a primary source. Direct egress to CourtListener, Justia, FindLaw, leginfo, Cornell LII, and `cdn.ca9.uscourts.gov` is blocked by the proxy in this environment. Run `npm run court:sync` and the citation funnel on the laptop before any of this is filed.

| Authority | Proposition | Status |
|---|---|---|
| *ASARCO v. Union Pacific*, 765 F.3d 999, 1004 (9th Cir. 2014) | Affirmative defense at Rule 12 needs an obvious bar on the face | Confirmed via search; **pin 1004** |
| *Khoja v. Orexigen Therapeutics*, 899 F.3d 988 (9th Cir. 2018) | Judicial notice / incorporation limits | Confirmed via search |
| *Lee v. City of Los Angeles*, 250 F.3d 668 (9th Cir. **2001**) | Existence, not truth of disputed facts | Confirmed; **year varies in secondaries — verify** |
| *Rawson v. Recovery Innovations*, 975 F.3d 742, **753** (9th Cir. 2020) | "significantly involves itself in the … decisionmaking at issue" | Confirmed via search; quote must be read in the F.3d text |
| *Kirtley v. Rainey*, 326 F.3d 1088, 1092 (9th Cir. 2003) | Four state-action tests | Confirmed via search |
| *Caviness v. Horizon Cmty. Learning Ctr.*, 590 F.3d 806 (9th Cir. 2010) | Conduct-specific inquiry; **adverse outcome** | Confirmed via search |
| *Sandoval v. County of Sonoma*, 912 F.3d 509 (9th Cir. 2018) | Bane specific intent / reckless disregard | Confirmed; **caption form to verify** |
| *Hebbe v. Pliler*, 627 F.3d 338, 342 & n.7 (9th Cir. 2010) | Liberal construction post-*Iqbal* | Confirmed via search |
| *Lopez v. Smith*, 203 F.3d 1122, 1130–31 (9th Cir. 2000) (en banc) | Notice of deficiencies + chance to cure | Confirmed via search |
| *Moore v. Kayport Package Express*, 885 F.2d 531 (9th Cir. 1989) | Rule 9(b) relaxed as to opposing party's knowledge | Confirmed via search |
| *Medical Marijuana, Inc. v. Horn*, **604 U.S. 593** (2025) | Property loss from personal injury; proximate cause preserved | Confirmed; official cite now available |
| *Exxon Mobil v. Saudi Basic Indus.*, 544 U.S. 280 (2005) | *Rooker-Feldman* is narrow | Confirmed via search |
| *Jones v. Blanas*, 393 F.3d 918 (9th Cir. 2004); CCP § 335.1 | Two-year § 1983 limitation | Confirmed via search |
| Penal Code § 3008(d)(2) | Duration set by certified professional in consultation with parole officer | Confirmed via search; **read the code text** |
| 15 C.C.R. § 3574 (NCR 25-01, Jan. 3, 2025) | Good cause; written; signed by provider **and** agent; Form 3043 Rev. 11/24; 30 days | Confirmed via search; **operative date still to pin** |
| Civ. L.R. 7-2(a), 7-3(a), 7-3(c), 7-4(b) | 35-day notice; 14-day opposition; 7-day reply; 25 pages | Confirmed via search; **read the local rules** |
| *Estate of Esche v. Bunuel-Jordana* (9th Cir. Sept. 29, 2025) | Private-party QI | **CONFLICTED** — safe-cite list says reasoning only; unverifiable here |
| *Wicklund v. Idaho Dep't of Corr.*, 623 F. App'x 338 (9th Cir. 2015) | Retaliation / QI on community supervision | **UNVERIFIED** — do not brief |

---

## 9. Work queue

**Before Monday**

1. Watch for the motion. If an **answer** arrives instead, this entire file goes to the CMC statement and discovery plan, not to an opposition.
2. Re-pull the Stockton portal register for STK-CV-UF-2026-0001032. If Van Dine has moved for a judgment of dismissal in Dept. 10A, the preclusion posture changes and UNIFIED § 6 ¶ 2 becomes the whole argument. Snapshot it either way — the September 12 print will be six weeks stale by the opposition deadline.
3. Confirm whether Matter 6 has been disclosed on the Matter 28 docket. Still open since September 12. It must be disclosed before the CMC statement, not after they find it.

**When the motion lands (day 1 of 14)**

4. Run the architecture file's § XVII intake checklist. Build the defense-authority table and the complaint-paragraph map the same day.
5. Diff the filed grounds against Van Dine's seven previewed grounds. Anything new was not met and conferred on; note it.
6. Capture their RJN and exhibit list first. Decide immediately what to lodge in response under § 2.3 — the whole state record, not a fight about their half of it.

**Before anything is filed**

7. Read the primary sources for every row in § 8 marked for verification. Everything in this file came through a search summary.
8. Pin § 3574's operative date and map it against the conduct dates in cluster-2 locked facts.
9. Run the citation funnel and the fabricated-citation gate. Nothing goes in that is not SAFE on `MATTER_28_SAFE_CITE_LIST.md`, and add the new authorities in this file to that list first.
10. Decide the Matter 26 / Matter 28 CDL wage allocation. Open since September 12 and it will be visible in both the opposition and the CMC statement.

**Housekeeping**

11. Recover the cluster-5 and Matter 29 files PR #876 deleted (§ 0).
12. The live-record drift listed at UNIFIED § 10 is still unfixed on `main` — the Bane "$25,000 per violation" figure, the *Dwyer* evidence-list characterization, and the stale `procedural_status`. None of it may be pasted into a filing.

---

Nothing in this file changes the September 21 answer deadline, the October 15 CMC statement, or the October 22 CMC. No PACER was accessed. Nothing was filed or served.
