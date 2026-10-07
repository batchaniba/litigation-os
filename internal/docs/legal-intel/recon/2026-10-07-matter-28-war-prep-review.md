# Matter 28 — War-Prep Review (adversarial, record-keyed)
## *Newanforbi v. Shannon Smith, LCSW, and HOPE Program*, N.D. Cal. No. 3:26-cv-07504-LJC

**Prepared:** October 7, 2026. **Posture reviewed through:** Dkt. 15 (motion to dismiss, filed Sept. 21, 2026) and the portfolio record as of today.
**Use restriction:** This memo quotes HOPE production pages stamped CONFIDENTIAL (HOPE_000001–542, Matter 5 stipulated protective order) and Plaintiff's clinical and criminal-history records. Keep it internal. Nothing here goes into a filing or a letter until the protective-order question in Threat 5 is resolved.

---

### Fact labels used throughout

| Tag | Meaning |
|---|---|
| **[V]** | Verified: I read the source page myself in this review (Bates, docket, or order cited) |
| **[V-p]** | Verified only through a portfolio summary. I did not read the underlying document. Re-verify before filing. |
| **[A]** | Alleged (complaint or Plaintiff's account) but not yet proven |
| **[I]** | Reasonable inference from verified material |
| **[U]** | Unsupported by anything in the record I reviewed |
| **[X]** | Contradicted by the record |

### Sources actually read for this review

- **Dkt. 15 and attachments.** Dkt. 15 (30 pp.); Dkt. 15-1 RJN with Exs. A (state FAC), B (state demurrer), and C (July 15, 2026 order); Dkt. 15-2 proposed order. Source: the `documents` backup branch, because the store's text sidecar is not extracted.
- **San Joaquin minute order and tentative ruling (July 10/15, 2026).** Repo-root scans `Minute_Order_rtf.pdf` and `1032_TentativeRuling_ProbateNote_rtf.pdf`.
- **The HOPE production, all 542 pages by Bates number.** Text layer on the `documents` branch. Page images were checked where OCR failed (HOPE_000002, 044, 224).
- **CDCR Form 1502-DR Discharge Review Report (5 pp.).** Signed Nov. 14 and 19, 2025.
- ***In re Frederick Dwyer*, San Mateo Super. Ct. No. SC-080355A / HC-3020, Order (Mar. 20, 2023).** All 12 pages, read from Exhibit A to the Matter 5 RJN.
- **HOPE's verified responses to Special Interrogatories, Set One** (June 15, 2026; verified by Carrie Shinske, June 12, 2026).
- **Portfolio JSON for Matters 3, 5, 6, 11, 15, 19 and 28**, plus the legal-intel recon set.

### Not available to me (gaps)

- **The federal complaint (Dkt. 1).** Not in the repo or in the readable store. Complaint paragraphs below are cited as quoted in Dkt. 15.
- **Plaintiff's filed opposition.** Not ingested. The Sept. 21 draft was reviewed instead.
- **Any reply.** Due Oct. 13.
- **Live docket and register.** CourtListener and PACER are blocked from this environment.
- **The RFA responses.** Only the `evidence.json` summaries were available.
- **The HOPE–CDCR contract.** Never produced.
- **Form 3043s.** None were produced.

---

# 1. One-page command brief

### Current posture (verify on PACER today)

- **Dkt. 15 motion.** Rule 12(b)(6) motion filed Sept. 21, 2026, on two grounds: res judicata, and failure to state any of the five counts. **[V]**
- **Opposition.** Due Oct. 5 and reported filed. The stamped copy is not in the record. **[V-p]**
- **Reply.** Due Oct. 13, 2026. **[V]** (CM/ECF pull of Sept. 21)
- **Hearing date conflict.** Dkt. 15 notices the hearing for **Oct. 20, 2026, 10:30 a.m.**, and the Sept. 21 CM/ECF pull matches. `clocks.json` says **Oct. 27**, from a Sept. 29 update that cites no docket entry. **Treat Oct. 20 as live until PACER shows a reset.**
- **CMC.** Case Management Statement due Oct. 15; initial CMC Oct. 22, 1:30 p.m. (videoconference). **[V]**
- **ADR certification.** Due Oct. 1; `clocks.json` still shows it "open." **Confirm it was filed.**

### Top three strengths

1. **The preclusion defense rests on a mischaracterized order.**
   - The minute order and tentative ruling say the state court sustained the demurrer because "exhaustion of administrative remedies herein is a jurisdictional requirement" that Plaintiff "failed to meet." **[V]**
   - Both are already on this docket as Dkt. 9 exhibits.
   - Dkt. 15 tells the Court the demurrer was sustained "with prejudice." The order says "without leave to amend." No § 581d judgment of dismissal is in Defendants' RJN. **[V]**
   - Smith was not a party to the state case. **[V]**
2. **HOPE's own manual states the structural retention rule.**
   - HRSO clients (Static-99R ≥ 4) must complete the entire Core phase **twice**. HOPE_000288, 000293. **[V]**
   - The Aftercare phase exists "to comply with state law requiring registered 290 offenders to maintain their connection with treatment for the duration of their term on community supervision." HOPE_000294. **[V]**
   - HOPE "is prohibited from discharging a client from treatment for any reason." HOPE_000294. **[V]**
   - The Completion Certificate goes into CDCR's ARMS database; clinicians "are not permitted to provide this certificate directly to clients." HOPE_000295. **[V]**
   - HOPE's verified SROG 13 admits that before October 2024, "CDCR policy required supervised persons to continue some form of treatment as part of the 'aftercare' phase... until they were discharged from parole." **[V]**
3. **HOPE has a credibility problem it created under oath.**
   - In verified SROGs 28 and 30, HOPE says it "has no knowledge of the 'DWYER decision.'" **[V]**
   - The Dwyer order records that HOPE's own Executive Director of Clinical Training and Development, Dr. Cristina Loree, testified at that hearing. She explained HOPE's four-phase program and her view that "a continuous connection to treatment is required for all sex offender parolees." Dwyer Order at 2, 4, 7. **[V]**

### Top five threats

1. **Causation.**
   - CDCR's Nov. 2025 discharge denial rests expressly on **Policy 19-03 (Amended)**: "not eligible for EDC at this time due to having a 10-year parole term... only completed approximately 4 years of the required 6.5 years." Form 1502-DR p. 4, signed by Agent Moua and by Supervisor Noguchi. **[V]**
   - That is a CDCR rule independent of HOPE. Even a HOPE completion certificate would not have produced parole discharge in 2025.
   - Plaintiff's own Matter 11 papers call Policy 19-03 Noguchi's "sole basis." **[V-p]**
2. **State action.** On July 24, 2026, E.D. Cal. (Mag. Peterson, Matter 3, Doc. 31) held that HOPE Site Director Palacios was not a state actor under any of the four tests. The same order gave Plaintiff a Rule 11(b)(2) reminder over a misquoted *Rawson* citation. **[V-p]** Defendants did not cite this ruling in Dkt. 15. Expect it in the reply.
3. **The "no-show" theory is contradicted.** The Mar. 31, 2026 email at HOPE_000142/194 shows **CDCR Parole Agent L. Moua**, not HOPE or Smith, writing: "there seems to have been a technological error... Please mark him as a no show." **[V]** The portfolio has been calling this HOPE/Smith retaliation. **[X]**
4. **A latent two-dismissal problem (Rule 41(a)(1)(B)) that the portfolio has not spotted.**
   - Matter 6 (HOPE et al.) was voluntarily dismissed May 21, 2026. Palacios was in the original complaint; the FAC dropped her. **[V-p]**
   - Plaintiff then voluntarily dismissed Palacios from Matter 3 on Aug. 20, 2026, after a dismissal order with leave to amend. **[V-p]**
   - If the Aug. 20 notice counts as the second dismissal of "the same claim," it operates as an adjudication on the merits. Defense could then argue federal claim preclusion through employer privity. Defendants have not raised it.
5. **Use of protected material, and costs/fee-shifting exposure.**
   - **The federal protective order was denied.** The motion to use the 542-page production in federal court was denied without prejudice (Dkt. 7). **[V-p]**
   - **The state order is not yet confirmed to be released.** The state stipulated protective order's return-or-destroy and use limits have not been confirmed released.
   - **The "Dkt. 6 Protective Order" is unidentified.** Read it.
   - **Anti-SLAPP fee risk on amended state claims.** Any amended Bane or fraud claim built on HOPE's reports to CDCR invites an anti-SLAPP motion (Code Civ. Proc. § 425.16), which carries mandatory defense fees, and a Civ. Code § 47(b) privilege defense.

### Next five actions (in order)

1. **Pull PACER and the San Joaquin register today.**
   - Confirm the hearing date (Oct. 20 vs. Oct. 27).
   - Confirm the ADR certification was filed.
   - Read what Dkt. 6 is.
   - Check the register for **any § 581d judgment of dismissal** entered after July 15 and any notice of entry. That decides the "final judgment" element.
2. **Build the hearing outline now** (use the `hearing-script` skill). Lead with Dkt. 9 Exs. B–C (the tentative ruling and minute order), not with case law. Prepare a 60-second answer to Peterson's Matter 3 state-action ruling for when the reply raises it.
3. **Joint CMC statement by Oct. 15.**
   - Ask for discovery to open now, without a stay.
   - Ask for a federal protective order modeled on the N.D. Cal. model order.
   - Disclose Matters 3 and 6 under Civ. L.R. 3-13 if they are still undisclosed.
4. **Send a preservation letter to SLB.** Cover TreatAnyone audit logs and metadata, the Almax Consulting systems, CTM "Progress Report and Treatment Plan Update" reports, Form 3043s, ARMS uploads, policy-manual version history, and billing data.
5. **Decide now how claims will be narrowed, and do it only by amendment.**
   - Drop RICO and conform the fraud count when the Court grants leave.
   - **Never use a Rule 41(a)(1) notice in any HOPE-cluster case again.**

---

# 2. Claim-survival matrix (pending motion)

Probabilities are my judgment of survival **at this Rule 12 hearing on the current complaint**. "Leave" is the likelihood of leave to amend if dismissed. A pro se plaintiff gets leave unless amendment is clearly futile: *Lopez v. Smith*, 203 F.3d 1122, 1130–31 (9th Cir. 2000) (en banc).

| Claim | Survives | Leave if dismissed | Decisive issue | Cure | Evidence for the cure |
|---|---|---|---|---|---|
| Res judicata (defense) | **Defense fails ~85%** | n/a | "Final judgment on the merits" | Point to Dkt. 9 Exs. B–C. Exhaustion is not a merits ground. No § 581d judgment. Smith was not a party. | Minute order; tentative ruling; Dkt. 15-1 Ex. C (an order, not a judgment) **[V]** |
| § 1983 retaliation (1A) — HOPE | **~45%** | ~90% | State action, then whether the adverse action was more than speech | Plead the reporting channel: written reports to CDCR that tie his litigation to non-completion ("fixated on lawsuits"), plus the Feb. 20, 2025 grace-period revocation | Dkt. 15-1 Ex. B at 7 (defense quotes and defends "fixated on lawsuits") **[V]**; HOPE_000190 **[V]**; RFA 25 / Palacios RFA 16, 29 **[V-p]** |
| § 1983 due process — HOPE (Monell) | **~25%** | ~80% | Liberty interest and what process was due | Narrow to procedural due process. The interest: a § 3574(f) written good-cause determination before retention. Process denied: no Form 3043 delivered within 30 days; no individualized review. | § 3574(f) (quoted in Dkt. 15 at 25) **[V]**; HOPE_000208–217 (treatment goals frozen since 2022) **[V]**; Form 3043s **[U — not produced]** |
| Monell "policy" element (both theories) | Strong *if* state action is found | — | Whose policy: HOPE's or CDCR's? | Plead HOPE's own written rules (HRSO double-core; aftercare to end of term; no discharge) as **HOPE** policy approved by HOPE leadership | HOPE_000288, 293, 294, 295 **[V]**; SROG 10 (executive team drafted the criteria) **[V]** |
| § 1983 individual — Smith | **~15%** | ~70% | Personal participation | Plead Smith as founder and final policymaker who approved the manual, was told of each suit, and let the practice continue after Dwyer | HOPE_000231 (founder; program built on her "vision") **[V]**; HOPE_000189 (Jan. 6, 2026 notice to Smith) **[V]**; **but** SROG 10 omits Smith from the drafters **[V]** |
| Bane Act (Civ. Code § 52.1) | **~25%** | ~60% | Specific intent and coercion; and, for state claims, the exhaustion holding | Tie to the retaliation count. Allege specific intent to keep him supervised for speaking. Avoid relying on privileged reports alone. | Same as retaliation |
| Fraud / negligent misrepresentation | **~10%** | ~50% | Rule 9(b) detail; reliance; damages caused by reliance | Who, what, when, and where for each statement, **plus** what Plaintiff did differently because of it. If no reliance-caused loss exists, drop. | Matter 5 FAC ¶¶ C.2–C.4 (Akins Nov. 2022; Jan. 2024; June 2024) **[A]** |
| Civil RICO § 1962(c)–(d) | **~5%** | ~40% (and should not be sought) | Predicates; proximate cause (*Anza*; *Hemi Group*, 559 U.S. 1 (2010)); business or property injury | None realistic. **Drop by amendment.** | The billing figures come from an **Alameda County Probation** contract, not a CDCR contract **[V-p, Matter 5 RJN Ex. D]**. "Billed CDCR at…" is **[U]**. |

**What wins the motion:** the minute order, and a framing of state action as a **statutory delegation plus joint reporting**: Penal Code § 3008(d)(2) places the length determination with the "certified sex offender management professional," and § 3574(f) requires the provider's signature on the Form 3043. Generic "contract with CDCR" framing loses. Everything else is secondary.

---

# 3. Procedural and preclusion reconstruction

## 3.1 Comparison table

| | **Matter 5** — *Newanforbi v. Palacios*, San Joaquin Sup. Ct. STK-CV-UF-2026-0001032 | **Matter 6** — *Newanforbi v. HOPE Psychotherapy*, E.D. Cal. 2:26-cv-00195-TLN-AC | **Matter 3** — *Newanforbi v. Derrick*, E.D. Cal. 2:26-cv-00004-DJC-JDP | **Matter 28** — this case |
|---|---|---|---|---|
| Filed / ended | Filed Feb. 10, 2026; demurrer sustained July 15, 2026; CMC was set for Oct. 13, 2026 **[V]** | Jan. 22, 2026 → voluntary dismissal May 21; minute order June 1 **[V-p]** | Jan. 5, 2026 → Derrick and Noguchi dismissed July 22; Palacios dismissed Aug. 20; closed Aug. 26 **[V-p]** | July 20, 2026 → pending |
| Parties | Plaintiff v. Palacios, HOPE, Does 1–10. **Smith not named.** **[V]** | Original complaint: HOPE, Palacios, 4 parole officials, the CDCR Secretary (Dkt. 15 at 8 n.1). FAC: HOPE and Macomber only. **[V-p]** | Palacios, Derrick, Noguchi | Smith, HOPE |
| Claims | Fraud, negligence, IIED, interference with prospective economic advantage, Bane Act, declaratory relief, UCL (Dkt. 15 at 12) **[V]** | § 1983 procedural due process (three counts) | § 1983 retaliation, equal protection, due process | § 1983 (Monell and individual), Bane, fraud/negligent misrepresentation, RICO |
| Material allegations | Blanket retention; Dwyer; § 3574; false Form 3043 content; Aug. 2025 CTM statements; homework mischaracterization; CDL losses | Structural delegation; Form 1502-DR defects; Policy 19-03 | CTM "ringleader"; grace-period revocation; FedEx scheduling | Same core as Matter 5, plus Smith, RICO, and First Amendment |
| Ruling | Demurrer sustained **without leave**. The signed order recites only "fails to allege facts sufficient to state any cause of action." The tentative ruling and minute order give the reason: exhaustion is a "jurisdictional requirement" Plaintiff "failed to meet." **[V]** | None on the merits | Doc. 31 (July 24): Palacios's motion **granted with leave to amend** (not a state actor); Derrick/Noguchi motion granted in part **[V-p]** | Dkt. 11: Court declined to screen for preclusion sua sponte **[V-p]** |
| Judgment? | **None in the record.** No § 581d judgment in Dkt. 15-1. The register has not been checked since the end of July. | Rule 41(a)(1)(A)(i) notice; self-executing | Rule 41(a)(1)(A)(i) notices | — |
| With or without prejudice | Without leave to amend. Not stated "with prejudice." Dkt. 15 at 13 says "with prejudice." **[X]** | Without prejudice | Without prejudice on its face — **subject to the two-dismissal question** | — |
| Final? | Not final for preclusion until a judgment is entered and is no longer subject to appeal (*Franklin & Franklin v. 7-Eleven Owners*, 85 Cal.App.4th 1168 — on the portfolio safe list) | Not a merits adjudication (*Semtek*, 531 U.S. 497) | See Section 3.4 | — |

## 3.2 California claim preclusion, element by element

Federal courts give a state-court judgment the effect the state would give it (28 U.S.C. § 1738; *Migra*, 465 U.S. 75). The elements are an identical cause of action, a final judgment on the merits, and the same parties or their privies (*Boeken*, 48 Cal.4th at 797; *DKN Holdings*, 61 Cal.4th at 824).

1. **Same primary right — likely satisfied as to HOPE. Concede it.**
   - Both actions plead the same injury (being kept in treatment and the effect on work) from the same wrong (the retention policy and the reports). Dkt. 15 at 12. **[V]**
   - Calling § 1983 a "different primary right" is on the portfolio's do-not-use list. Correctly so.
   - The First Amendment retaliation theory partly overlaps. Matter 5 pleaded the Aug. 2025 CTM statements, so the overlap is not clean.
   - **Exception:** acts after the state FAC was filed (Feb./Mar. 2026 onward) were not part of that cause of action. That includes the Feb. 18, 2026 CTM report (if that is where "fixated on lawsuits" appears) and any later retention. **[I]**
2. **Final judgment on the merits — the decisive element, and it fails now.**
   - **(a) No judgment.** An order sustaining a demurrer is not a judgment. The record contains only the signed "[Proposed] Order," Dkt. 15-1 Ex. C. **[V]** *Valvo* and *Berri* are on the safe list; pin-check the exact language before quoting.
   - **(b) Not on the merits.** The court's stated reason is that exhaustion is jurisdictional (minute order). **[V]** A dismissal for want of jurisdiction, or for failure to satisfy a pre-suit condition, decides only that the plaintiff sued too early; it does not bar a later action once the condition is met (*Goddard*, 14 Cal.2d 47; *Perez v. City of San Bruno*, 27 Cal.3d 875 — both safe-listed; pin-check).
   - Defendants' *Palomar* quotation (989 F.2d at 364) is about a judgment entered after a general demurrer that adjudicates the facts "do not establish a cause of action." The minute order shows this one did not reach that question.
3. **Same parties or privies — met for HOPE; contested for Smith.**
   - HOPE was a party. **[V]**
   - Smith was not. Defendants argue employee-employer privity in a footnote, citing *Scott v. Kuhlmann*, 746 F.2d 1377, and *Drawsand*. **[V]**
   - Rebuttal: Smith is sued for her own policymaking, not as Palacios's agent. Nonparty preclusion is narrow (*Taylor v. Sturgell*, 553 U.S. 880).
   - Honest risk: once a merits judgment exists, courts routinely extend preclusion to a corporate officer for the same corporate conduct.

**Defense's strongest formulation (expect it in reply).**
- "Even if not on the merits, the state court finally decided that Plaintiff's claims require CDCR administrative exhaustion and that he did not exhaust."
- "Issue preclusion bars relitigating that point, so every state-law count here (Bane, fraud) fails for the same reason."
- "And Plaintiff did not appeal."

**Strongest record-based rebuttal.**
- Issue preclusion also requires a **final judgment**: the same finality element, still missing.
- In any event, issue preclusion on exhaustion can only bar **state-law claims premised on unexhausted 2025-or-earlier events**.
- Exhaustion of state remedies is not required for § 1983 (*Patsy*, 457 U.S. 496).
- The PLRA does not apply to a parolee at liberty (42 U.S.C. § 1997e(h); *Page v. Torrey*, 201 F.3d 1136; *Talamantes*, 575 F.3d 1021 — safe-listed).
- **Practical cure:** exhaust going forward. File timely CDCR grievances (15 C.C.R. §§ 3482, 3723) on the next Form 3043 and the **December 2026 annual discharge review**. That removes the defense for new events.

## 3.3 Other doctrines

- **Rooker-Feldman.** Does not apply. Plaintiff does not complain of an injury caused by the state judgment.
- **Younger.** Does not apply. There is no qualifying state enforcement proceeding; Matter 19 habeas is Plaintiff-initiated (*Sprint v. Jacobs*, 571 U.S. 69 — **[verify pin]**).
- **Heck / Preiser: a real but partial risk.**
  - Damages premised on **prolonged parole supervision** (the discharge denial, GPS, curfew) attack the duration of custody. Those may be Heck-barred until the discharge decision is invalidated.
  - Damages premised on the **treatment condition itself** (being kept in groups, retaliatory reports) are a challenge to a condition, not to duration, and are generally outside Heck (*Thornton v. Brown*, 757 F.3d 834 (9th Cir. 2013) **[verify holding before citing]**).
  - **Remove "remains subject to GPS, curfew... parole supervision" from the damages theory** (Dkt. 1 ¶ 50 as quoted in Dkt. 15 at 22). GPS for registrants is statutory (Penal Code § 3000.07(a), cited by the defense at 26) and is not HOPE's doing.
- **Statute of limitations (not raised yet; expect it in the answer).**
  - § 1983 and probably Bane borrow California's two-year personal-injury period (Code Civ. Proc. § 335.1). Bane may get three years (§ 338(a)); courts split — **[verify]**.
  - The complaint was filed July 20, 2026, so discrete acts before **July 20, 2024** are time-barred except as background (*Nat'l R.R. Passenger Corp. v. Morgan*, 536 U.S. 101).
  - Each retention or CTM report is a discrete act. The **Aug. 2024, Feb. 2025, Aug. 2025, and Feb. 2026 CTMs** and the Feb. 20, 2025 grace revocation are in time.
  - The Nov. 2022 Akins representation and the Oct. 18, 2023 Tassone plan are background only.
- **Matter 19 (Santa Clara habeas, C2604791, pending).**
  - This is the **correct vehicle** for the § 3008(d)(2) court-approved length determination. Dwyer's relief came that way.
  - A merits denial there could later be argued as issue-preclusive on whether he was entitled to be released from treatment. Track it.

## 3.4 The two-dismissal question (new)

Rule 41(a)(1)(B): "if the plaintiff previously dismissed any federal- or state-court action based on or including the same claim, a notice of dismissal operates as an adjudication on the merits."

**Sequence.**
- First dismissal: Matter 6 (HOPE et al.), May 21, 2026.
- Second dismissal: Matter 3, Palacios, Aug. 20, 2026.
- Matter 3 also dismissed Derrick and Noguchi on July 22. Check whether they were among Matter 6's original four parole officials. If so, that dismissal is the riskier one, mainly for Matter 30.

**Best defense argument.** The Aug. 20 Palacios dismissal is an adjudication on the merits. HOPE and Smith are Palacios's privies. Federal claim preclusion (transactional test) therefore bars the § 1983 retaliation and due-process claims arising from Palacios's conduct.

**Rebuttal.**
- When Matter 6 was dismissed, its operative FAC named only HOPE and Macomber. Palacios was dropped by amendment, not by a Rule 41 notice.
- The Matter 6 claims (structural due process) differ from Matter 3's (retaliation and equal protection against Palacios and the agents).
- The rule is read narrowly and generally requires the same defendant. **[verify Ninth Circuit authority before relying on it]**

**Assessment.**
- Risk is low to moderate.
- The defense has not raised it, and it is not a Rule 12(h) defense, so it can appear in the answer.
- **Never answer it by volunteering it.**
- **Never file another Rule 41(a)(1) notice in this cluster.** Narrow by Rule 15 amendment only.

---

# 4. Motion-to-dismiss red team, claim by claim

## 4.1 State action (gates Counts 1–2)

**Defense attack (Dkt. 15 at 14–18).** Presumption of private conduct; public function fails because sex-offender treatment is not exclusively governmental (*Reinhardt*; *Colliton*); a contract alone is not joint action (*Rendell-Baker*); no compulsion; no nexus.

**Defense's strongest reply addition.** Mag. Peterson's July 24, 2026 Matter 3 order finding Palacios not a state actor under all four tests; *Wilson v. Azinkhan / Sharper Future* (C.D. Cal.) (on the portfolio's adverse list).

**Plaintiff's best theory: statutory delegation plus joint decision.** Not public function.

1. **Penal Code § 3008(d)(2).** The program length "shall be not less than one year, up to the entire period of parole, as determined by the certified sex offender management professional in consultation with the parole officer and as approved by the court" (quoted in Dkt. 15 at 25). The State placed a liberty-affecting determination in the provider's hands by statute.
2. **15 C.C.R. § 3574(f).** A retention determination "shall be stated in writing, signed by the sex offender treatment provider **and** parole agent on the CDCR Form 3043." Dkt. 15 at 25. **[V]** That is a co-signed state decision.
3. **CDCR defers to the provider in practice.**
   - Dwyer: "the 'consultation' contemplated by the statute... worked only one way — the program told parole what was required and parole deferred." Order at 10. **[V]**
   - A CDCR administrator testified that parole denied the grievance "in deference to" the provider's decision. Order at 6. **[V]**
4. **Integration into CDCR records.**
   - HOPE operations staff update **ARMS ("CDCR database")** directly. HOPE_000269. **[V]**
   - Completion certificates are uploaded to ARMS. HOPE_000295. **[V]**
   - HOPE says the treatment plan "is completed at the request of CDCR, is transmitted to CDCR, and is the property of CDCR" (SROG 15) and that records "are the sole property of CDCR" (SROG 17). **[V]**
   - CDCR's Sex Offender Unit dictates CTM report content. HOPE_000269 ("NOT acceptable per the Sex Offender Unit"). **[V]**
   - CDCR approves treatment modifications. HOPE_000161 (Apr. 2023 teletherapy approval by Agent Alcoriza). **[V]**
5. **Compulsion and encouragement.** HOPE says the full-term aftercare rule was **CDCR policy** (SROG 13) and that its no-discharge rule comes from "guidelines within our contracts" (HOPE_000294). **[V]**
   - This helps state action.
   - It hurts the Monell theory that the policy was **HOPE's**. Plead both in the alternative: the State compelled the rule (state action), and HOPE adopted and extended it in its own manual (HRSO double-core; Sept. 23, 2024 version still carrying the aftercare rule after CDCR's Oct. 2024 change). That is the HOPE policy.

**Likely ruling.**
- About a coin flip on the current pleading. Better than that on an amended pleading that pleads items 1–4 with Bates numbers. The Court can consider them only if pleaded or incorporated.
- Most likely outcome: **dismissal with leave to amend on state action**, with preclusion rejected.

**Remove from the complaint.**
- "Sole certified provider in the Stockton region." **[U]** No CASOMB record supports it.
- *West v. Atkins* as "controlling." *West* concerned a physician treating prisoners in state custody. Use it for the principle that contracting out a state obligation does not shed the State's duty, not as a holding about parolee treatment vendors.

## 4.2 First Amendment retaliation

**Elements.** Protected activity; action that would chill a person of ordinary firmness; a substantial motivating factor. *Ariz. Students' Ass'n*, 824 F.3d at 867 (the defense's own case).

**Protected activity.**
- Pre-Aug. 2025 complaints to HOPE (Dkt. 1 ¶ 38). **[A]** Palacios RFA 29 admits pre-August complaints. **[V-p]**
- Lawsuits: Matters 3 and 6 (Jan. 2026), Matter 5 (Feb. 2026). Smith was told of the Jan. 6, 2026 complaint, per HOPE_000189. **[V]**
- The May 4, 2026 CASOMB-inquiry email to HOPE. HOPE_000139–140, 195–196. **[V]**

**Adverse actions, ranked.**

1. **The written report to CDCR that Plaintiff "is fixated on lawsuits instead of subject material,"** tied to a non-completion status.
   - The defense quoted this content and defended it as supported by "objective evidence" of his lawsuits. Dkt. 15-1 Ex. B at 7. **[V]** That is close to a direct-evidence nexus.
   - **The document itself has not been produced.** First priority for a request for production.
2. **Grace-period revocation**, Feb. 20, 2025. HOPE_000190. **[V]**
3. **Aug. 19, 2025 CTM statements** ("disruptive," "ringleader," "abhorrent") to parole agents in the meeting that sets supervision.
   - Palacios RFAs 11–12 and 16 (including "when you start complaining…"). **[V-p]**
   - **HOPE SROG 33 and 35 say "no knowledge of the alleged statements."** **[V]** HOPE's verified answers contradict its own employee's admissions.
4. **The Mar. 31, 2026 no-show.** **Not a HOPE adverse act.** The CDCR agent requested it. HOPE_000142/194. **[V] [X as to HOPE/Smith]**

**Defense attack.** Speech in response to speech is not retaliation (*Nunez*); no chill; no injury (*Nieves*).

**Answer.** Items 1 and 2 are **official reporting and program sanctions**, not counter-speech. The reports went into the meeting that determines supervision conditions, and the same reports underpin the "Discharge Denied" form.
- The Ninth Circuit's prisoner and parolee retaliation cases treat false reports and disciplinary consequences as adverse actions: *Rhodes v. Robinson*, 408 F.3d 559 (2005); *Watison v. Carter*, 668 F.3d 1108 (2012).
- Both are **not in the verified corpus. Pin-verify before use.**

**Likely ruling.** Survives if state action survives and the amended pleading leads with items 1–3.

**Remove.** The no-show allegation as HOPE/Smith retaliation. Keep it, if at all, only as evidence that CDCR directs HOPE's attendance records, which supports joint action.

## 4.3 Due process

**Defense attack (at 20–24).**
- No substantive due process right in California's parole scheme (*Styre*).
- *Neal* holds that a conviction supplies the process due.
- § 3008 creates no expectation of completion.
- Grievance procedures were available and unused.
- Footnote 3: a violation of state law is not a due process violation (*Swarthout*).

**Best answer.**
- Abandon substantive due process.
- Procedural: § 3574(f) uses mandatory language ("shall be supported by good cause," "shall be stated in writing, signed... delivered to the supervised person within 30 calendar days"). Argue that it creates a protected interest in not being retained in treatment without a written good-cause determination.

**Weakness.**
- *Sandin* and *Swarthout* make state-created liberty interests hard to establish for parolees.
- The deprivation is "more treatment sessions," not custody.
- *Neal* involved the "sex offender" label itself, not treatment length.
- The grievance argument is weak as a matter of law: available post-deprivation remedies matter only for random, unauthorized acts. **But** the policy here is a written, established procedure, which answers the "random and unauthorized" exception. **[verify Parratt/Zinermon framing]**

**Likely ruling.** Dismissed with leave. Survival roughly 25%.

**Keep only if** discovery shows Form 3043s were never prepared, signed by HOPE, or delivered within 30 days (§ 3574(f)). That is a concrete procedural failure.

## 4.4 Monell against HOPE

- **Private entities face Monell, not respondeat superior.** *Tsao v. Desert Palace*, 698 F.3d 1128 (safe-listed).
- **Policy.** The policies are written (HOPE_000288/293/294/295), so this element is the case's strongest.
- **Moving force.** The policy must have caused the constitutional injury. That fits the retention theory (due process) far better than the retaliation theory, which is an individual act by Palacios.
- **Retaliation under Monell needs one of:**
  - (a) a policy of reporting litigation to CDCR as a treatment deficit;
  - (b) ratification by a final policymaker; or
  - (c) a custom.
- Evidence for (b): HOPE's verified SROG 20 adopts the "partially completed" characterization **[V]**, and counsel defended "fixated on lawsuits" in the state demurrer **[V]**. Ratification must come from a final policymaker (*Christie v. Iopa*, 176 F.3d 1231 — **[verify]**), not from counsel.

## 4.5 Smith individually

- **Pleaded:** she "personally approved, implemented, and enforced" the policy (Dkt. 1 ¶¶ 1, 12, 45–47, per Dkt. 15 at 9).
- **Defense:** no Smith-specific act.
- **Record for Smith:**
  - Founder; the program reflects her "vision." HOPE_000231. **[V]**
  - Notified of the January 2026 suit. HOPE_000189. **[V]**
  - Named on the professional liability declarations. HOPE_000002. **[V]**
  - Her name appears as the assigning user on a July 2021 homework item. HOPE_000223. **[V]** Probably a system default; don't build on it.
- **Record against Smith:**
  - SROG 10 lists the criteria drafters as CASOMB input plus Hansen, Palacios, Loree, Shinske and Kingston. Not Smith. **[V]**
  - SROG 5 lists "executive leadership" without Smith. **[V]** That is odd for a CEO; exploit it in deposition, not in the pleading.
- **Viable theory:** supervisor liability for setting in motion or knowingly acquiescing in a policy (*Starr v. Baca*, 652 F.3d 1202 — **[verify]**), after notice from Dwyer (2023), § 3574 (2025), and the 2026 lawsuits.
- **Prediction:** dismissed with leave; ~15% now.
- **Recommendation:** keep Smith only if the amendment can plead a specific post-notice decision by her. Otherwise drop her to cut cost and the anti-SLAPP/fee exposure. Re-add after discovery if documents warrant it (Rule 15).

## 4.6 Bane Act

- **Defense:** § 3008 and § 3574 create no "rights" for Bane; no threats or coercion; the statements are not threats.
- **Law:** where the constitutional violation is intentional, a separate showing of coercion beyond the violation is not required, but **specific intent** to violate the right is. *Cornell v. City & County of S.F.*, 17 Cal.App.5th 766 (2017); *Reese v. County of Sacramento*, 888 F.3d 1030 (9th Cir. 2018). **[verify pins; not on the safe list]**
- **Problems:**
  - It rises or falls with § 1983 retaliation.
  - The state court's exhaustion holding is a direct issue-preclusion risk for a **state-law** Bane claim built on 2025 events, once a judgment is entered.
  - Civ. Code § 47(b) privilege for communications in official proceedings **[verify scope as to Bane]**.
  - Anti-SLAPP exposure (Section 12).
- **Prediction:** dismissed with leave; ~25%.

## 4.7 Fraud / negligent misrepresentation

- **Defense:** no who, what, or when; no intent; no justifiable reliance; the decision belonged to CDCR (at 27–29).
- **The real defect is reliance and damages, not particularity.**
  - The best statements to Plaintiff were made by Akins (Nov. 2022) and a clinician (Jan. 2024). **[A]**
  - The Nov. 2022 statement is likely time-barred unless he only discovered the falsity later, perhaps on reading Dwyer. Code Civ. Proc. § 338(d) runs three years from discovery.
  - He was legally compelled to attend, so what did he do differently because of these statements? Without an answer, there is no reliance-caused loss.
  - The "partially completed homework" reports were made to CDCR. California rarely allows fraud claims based on a third party's reliance. *Randi W.* is a negligent-misrepresentation case about physical harm. **[verify before use]**
- **Prediction:** dismissed; leave possible.
- **Recommendation:** drop, or replead only a **concealment** theory: HOPE concealed the HRSO double-core rule and the aftercare-to-end-of-term rule while telling him completion was achievable. That still needs a reliance-caused loss: for example, he forwent a court-approved § 3008(d)(2) habeas route because he was told completion was close. Plead that only if true.

## 4.8 RICO

**Elements and defects.**
- **Conduct of an enterprise.** HOPE cannot be both the defendant "person" and the enterprise. Smith plus HOPE is distinct (*Cedric Kushner*, 533 U.S. 158).
- **Predicates.**
  - Mail and wire fraud require a scheme to obtain money or property by false pretenses.
  - Billing for sessions actually delivered is not fraud unless the services were misrepresented.
  - "False reports to parole" are clinical opinions; CDCR, not Plaintiff, lost any money.
  - "Obstruction" does not fit.
- **Pattern.** Continuity is pleadable; that is not the problem.
- **Business or property injury.** Lost employment can qualify (*Diaz v. Gates*, 420 F.3d 897 (en banc), safe-listed). Emotional injury and liberty restrictions cannot.
- **Proximate cause.** If anyone was defrauded, it was CDCR, the payor. Plaintiff's injury is derivative (*Anza*, 547 U.S. 451; *Hemi Group*, 559 U.S. 1).
- **Factual base is wrong.** The rate schedule ($100 group / $200 individual / $1,800 evaluation) comes from an **Alameda County Probation** contract (state RJN Ex. D), not a CDCR contract. **[V-p]** "HOPE billed CDCR at…" is **[U]**.

**Conspiracy (§ 1962(d)).** Adds nothing if § 1962(c) fails.

**Recommendation.** Drop RICO in the amended complaint. It gives the insurer coverage defenses (fraud and personal-profit exclusions, HOPE_000005), raises Rule 11 risk, and absorbs pages.

---

# 5. *In re Dwyer* — what it actually is (read in full, Order of Mar. 20, 2023)

**Procedure.**
- Habeas petition filed June 22, 2021 in Alameda County; transferred to San Mateo (the committing court).
- Order to show cause Jan. 13, 2022; evidentiary hearing Mar. 9, 2023; order Mar. 20, 2023 (Hon. Elizabeth M. Hill).
- The respondent was represented by the Attorney General. **HOPE was not a party.** **[V]**

**Material facts.**
- Paroled May 30, 2017.
- One violation, in 2019.
- Recommended for early discharge by parole. BPH denied it for not serving the minimum term.
- Completed Shaping Success's treatment phase. Certificate Jan. 12, 2021.
- Moved to HOPE Mar. 5, 2021.
- Static-99R **4 ("high risk")**; Stable-2007 **2**; LS/CMI **6** (both low).
- "Near perfect" attendance.
- Married, employed journeyman carpenter, in college.
- Order at 2–5. **[V]**

**Testimony.**
- **Dr. Cristina Loree, HOPE's Executive Director of Clinical Training and Development:** described the four phases. Aftercare is voluntary for non-parolees but "mandatory for those who have not yet discharged from parole," and she "believes a continuous connection to treatment is required for all sex offender parolees." Order at 4; see also 7. **[V]**
- **CDCR's Daniel Stout:** CDCR/DAPO policy is that a § 3008 program "cannot be completed short of discharge from parole." Order at 6–7. **[V]**
- **CDCR's Gilberto Haro:** parole deferred to the provider. Order at 6. **[V]**

**Holdings.**
1. Exhaustion was excused as futile, because DAPO defers to the provider. Order at 6–7.
2. The petition was not moot.
3. **The habeas petition was DENIED.** The parole condition requiring treatment is valid under *Lent*, and he never "completed" a program.
4. Exercising its power under Penal Code § 3008(d)(2) "as approved by the court," the court **disapproved further participation and fixed the program as terminating Mar. 20, 2023.**
   - It found HOPE's "determined level of necessary treatment for parolees who had completed Shaping Success's treatment phase was not dependent on individualized criteria." Order at 10.
   - It found that discretion exercised to require full-term participation for all parolees "vitiates the Legislature's directive." Order at 11. **[V]**

**What it did not decide.**
- No damages, § 1983, Monell, state action, fraud, or RICO.
- No finding against HOPE as a party.
- No holding that full-term treatment is unlawful for everyone. The court expressly noted parolees "for whom public safety demands participation... for the entire term," citing "resistance to supervision, refusal to genuinely engage in treatment" (order at 11).

**Similarities to this case.**
- HOPE, the East Bay/Stockton region, 2021 transition.
- Same Static-99R (4).
- Low dynamic scores in both cases: Plaintiff's LS/CMI is 5 and STABLE 6, rated "Level 2 below average Risk" on the 1502-DR. **[V]**
- Same CDCR full-term policy; same HOPE aftercare structure.

**Differences the defense will exploit (all [V]).**

| Dwyer | Plaintiff |
|---|---|
| Completed a prior provider's treatment phase | In Core Block I/II after 5 years (SROG 11; HOPE_000224) |
| Near-perfect attendance | Missed 6 sessions this period; 2025 failure-to-attend violations (1502-DR p. 1) |
| One violation, in 2019 | Five violations this review period |
| Employed | Unemployed at the 1502-DR |
| Agent recommended discharge | Agent recommended "Discharge Denied" |
| — | Oct. 2023 polygraph with significant reactions (HOPE_000174) |
| — | In custody Nov. 1–12, 2024 (HOPE_000185–186) |

**The defense is half right that Plaintiff "misunderstands Dwyer."**
- The **portfolio is wrong in the other direction.** The `HOPE_SMITH_SOMP_CASES.md` and UNIFIED flag that the Loree attribution is "MISCITED" is incorrect. The order does recite Loree's testimony about HOPE's mandatory aftercare. Correct that flag.
- The Matter 5 FAC's statement that the court "found the policy vitiates…" is accurate as quoted.
- What was wrong: calling Dwyer a "judicial condemnation of HOPE's blanket retention policy" as if it were a judgment against HOPE.

**Narrowest accurate use.**
- (1) As notice: HOPE's senior clinical executive testified in March 2023 about the full-term aftercare rule, and a court rejected that practice as applied to an individual. That is the foundation for knowledge, deliberate indifference, punitive damages, and impeaching SROG 28/30.
- (2) As an example of the correct remedy: a § 3008(d)(2) court determination (Matter 19).
- (3) As evidence of joint action: parole defers to the provider.

**Stronger authority for propositions now attributed to Dwyer.**
- For "completion and discharge are separate," cite **15 C.C.R. § 3574** itself (the OAL materials are in the repo research folder).
- For CDCR's policy change, cite HOPE's own **SROG 13** ("CDCR amended that policy in October of 2024").
- *ACSOL v. Macomber* (L.A. Super. Ct. 23STCP02378) is a demurrer ruling only. Do not overuse it.

---

# 6. Regulatory and contractual machinery — responsibility map

| Step | Legal authority | Who controls in law | Who controls in practice (record) | Document trail | Status |
|---|---|---|---|---|---|
| Referral to SOMP | Penal Code § 3008(d)(2) (condition of parole) | CDCR/DAPO | CDCR refers; HOPE enrolls ("Clients are referred to HOPE by CDCR," SROG 17) | Referral; parole conditions (CDCR 1515) | [V] |
| Risk tier (HRSO vs. non-HRSO) | SARATSO / Static-99R (Penal Code § 3008(a), (c); Dwyer at 9) | CDCR's state-authorized risk tool | HOPE uses Static-99R ≥ 4 to set 2x/week groups **and** double Core (HOPE_000288, 293) | Static-99R (1502-DR: 4) | [V] |
| Treatment plan | CASOMB standards; HOPE manual | HOPE clinician | Plan by Tassone 10/18/2023, "provided to CDCR and has not been revised" (SROG 14). Goals set 6/11/2021, target 12/31/2022, no progress log after 11/10/2022 (HOPE_000208–217) | Individualized Treatment Plan; TreatAnyone goals | [V] |
| Progress and dynamic risk | HOPE manual (HOPE_000290: advancement "directly dependent" on measurable progress; STABLE-2007, LS/CMI) | HOPE | 10/15/2024: STABLE 6 / LS/CMI 5 (1502-DR p. 4) | CTM "Progress Report & Treatment Plan Update" | [V] |
| Phase titration | HOPE manual (HOPE_000290, 295) | HOPE Clinical Director or supervisor approves | "Not eligible for titration" (1502-DR p. 4) | CASOMB titration tracking form in TreatAnyone | [V]; forms not produced |
| CTM retention decision | 15 C.C.R. § 3574(e)–(f) (Containment Team; good cause; Form 3043 signed by provider **and** agent; delivered within 30 days) | Containment Team; CDCR form | HOPE's verified reason at every CTM, Aug. 2022–Aug. 2025: "had not completed Block I"; Feb. 2026: Block II (SROG 11) | **Form 3043 (Rev. 07/24 or 11/24)** | Not produced; HOPE says CDCR creates and retains it (SROG 3) **[V]** |
| Completion / graduation | HOPE manual (HOPE_000295, six steps) | HOPE team; Clinical Director approves | Graduation leads to Aftercare until parole ends (HOPE_000294) | HOPE Treatment Completion Certificate → ARMS | [V] |
| Length of program | Penal Code § 3008(d)(2): provider "in consultation with the parole officer **and as approved by the court**" | Provider + agent + **court** | Parole defers to the provider (Dwyer at 6, 10) | Court order (Dwyer model) | [V] |
| Annual discharge review | 15 C.C.R. §§ 3720–3723; Policy 19-03 (Amended) | Agent → Unit Supervisor → Parole Administrator | Denied 11/2025 on Policy 19-03 time-served **and** treatment, employment and violations | Form 1502-DR (Moua 11/14/25; Noguchi and Dodd 11/19/25) | [V] |
| Grievance | 15 C.C.R. §§ 3480 et seq., 3723 | CDCR Office of Grievances | Not used for 2025 events (state-court finding) | CDCR 602-1 / 602-2 | [V]; but Matter 11 shows a Form 602 exhausted on Policy 19-03 **[V-p]** |
| Attendance / no-shows | HOPE manual ("Missed Session Alerts," HOPE_000266) | HOPE records; agent sanctions | The agent directed the no-show (HOPE_000142/194) | Missed-session alerts; collateral notes | [V] |

**HOPE's actual legal authority.** Co-signer of retention (§ 3574(f)); recommender of program length (§ 3008(d)(2)); sole authority over titration and graduation in its own program.

**HOPE's practical influence.** Decisive on treatment length (Dwyer). Material but **not decisive** on parole discharge (Policy 19-03 is separate).

**CDCR's retained authority.** Parole conditions, GPS (§ 3000.07), discharge, violations, risk tier, Form 3043 custody.

**Plaintiff's assumptions to retire.**
- That HOPE decides parole discharge. **[X]**
- That HOPE created the Form 3043. **[X]** It is a CDCR form, signed by both.
- That "no parolee can ever complete." **Imprecise.** The manual allows graduation and a certificate while on parole, but then requires aftercare until parole ends. The accurate theory is **"no exit from treatment before parole ends, and a static score doubles the time."**

**Evidence of joint decision-making.** § 3574(f) dual signature; Dwyer at 6 and 10; HOPE_000161; HOPE_000199/143 (the agent requests the group change, HOPE complies); HOPE_000269 (ARMS); the agent directs the no-show (HOPE_000142).

---

# 7. Evidence ledger

## 7.1 Allegation-to-proof (highest leverage first)

| # | Allegation | Required proof | Best support (Bates) | Admissibility | Authenticating witness | Defense reading | Missing | Discovery |
|---|---|---|---|---|---|---|---|---|
| 1 | HOPE has a categorical rule making static risk, not progress, drive duration | Written policy plus application to Plaintiff | HOPE_000288 (HRSO = Static-99R ≥ 4 → 2x/week); 000293 (HRSO completes Core **twice**); 000294 (aftercare for the full term; no discharge); 000295 (certificate to ARMS only) | Party admission (FRE 801(d)(2)); business record | Shinske, Loree, HOPE 30(b)(6) | "Risk-responsive, per RNR and CASOMB" | Policy versions before Sept. 23, 2024; whether HRSO double-Core applied to Plaintiff | RFP versions and history; RFA 1–4 |
| 2 | The full-term rule existed and was CDCR-sanctioned | Admission | SROG 13 ("Prior to October of 2024, CDCR policy required…") [V] | Verified answer (FRE 801(d)(2)) | Shinske (verifier) | "It was CDCR's rule, not ours; it changed Oct. 2024" | Post-Oct. 2024 HOPE practice | RFA 5–6; 30(b)(6) topics 3–4 |
| 3 | HOPE knew of Dwyer in 2023 | Loree testimony | Dwyer Order 2, 4, 7 [V]; contrast SROG 28/30 | Order judicially noticeable for existence and testimony recited; not for truth unless offered as an admission of HOPE's agent (Loree) — **[verify FRE 801(d)(2)(D) fit]** | Loree; Dwyer transcript (Feb./Mar. 2023) | "Institutional knowledge ≠ Loree's attendance" | The hearing transcript | Subpoena the San Mateo transcript; RFA 7–8 |
| 4 | Litigation was reported to CDCR as a treatment deficit | The report itself | Dkt. 15-1 Ex. B at 7 (counsel quotes "fixated on lawsuits" and defends it) [V]; SROG 20 | Party admission; the report itself once produced | Author clinician; Palacios | "Clinical observation" | **The report** (likely Feb. 2026 CTM) | RFP 1 (all CTM reports 2024–2026) |
| 5 | No individualized plan review | Plan history | HOPE_000208–217 (goals 6/11/21; target 12/31/22; no updates); SROG 14 (10/18/23 plan "has not been revised") [V] | Business record; admission | Tassone; Leibowitz | "Plans live in the CTM reports" | CTM reports; titration forms | RFP 2–3 |
| 6 | HOPE lost or reset homework | Reset evidence | HOPE_000224 (Block I modules all dated 3/24/25, four years in); 000105–111 (Block I assigned 3/23/25 by Boatner); 000204/206 ("Catch Up Homework" created **Mar. 9–10, 2026** by Hansen, recording 2025 completions "per PN") [V] | Business record; metadata | Boatner; Hansen; Almax | "Normal curriculum; catch-up is good recordkeeping" | Pre-2025 Block I records; TreatAnyone audit trail | RFP 5; ESI; Almax subpoena |
| 7 | HOPE disrupted progress (cancellations, turnover) | Pattern | HOPE_000147, 162, 166, 170, 175, 177, 179, 181, 182 (group or individual cancellations, 2022–2024); clinicians across the file: Stewart, Smith (system), Leibowitz, Akins, Tassone, Boatner, You, Felix, Hansen [V] | Business records | Ops manager | "Rescheduled; no effect" | The make-up schedule | RFP 6 |
| 8 | "Partially completed" characterization | Report content and basis | SROG 20 (basis = clinician knowledge, CTM reports, tracking) [V]; RFA 18 [V-p] | Admission | Clinician | Supported by HOPE_000224 | The reports | RFP 1 |
| 9 | Aug. 19, 2025 CTM statements | Statements and attendees | SROG 32 (attendees: Plaintiff, Palacios, Derrick, Noguchi) [V]; Palacios RFAs 11–12, 16 [V-p]; HOPE SROG 33/35 deny knowledge [V] | Admission (Palacios as HOPE's agent) | Palacios; Derrick; Noguchi | "Clinical candor" | Recording, if Plaintiff has one (FAC refers to a "recorded" Aug. 2025 group) | Plaintiff to locate the recording; Penal Code § 632 consent issue **[verify]** |
| 10 | Grace-period revocation was retaliatory | Date and motive | HOPE_000190 (Feb. 20, 2025; "AOR is aware") [V] | Business record | Felix; Palacios | "Chronic lateness" | Body of the collateral note (page not produced: HOPE_000191 is blank) | RFP 7 |
| 11 | Low dynamic risk | Scores | 1502-DR p. 4: "10/15/2024 Stable 6 / LSCMI 5. Level 2 below average Risk" [V]; § 3574(f)(1) LS/CMI ≥ 11 as an example of good cause | Public record (FRE 803(8)) | Noguchi | "Static-99R 4 = high risk; polygraph" | Later scores; Static-99R scoring | RFP 8; RFA 9–10 |
| 12 | HOPE revenue stops on discharge | Admission | SROG 27 ("would no longer receive compensation") [V]; RFA 22 [V-p] | Admission | 30(b)(6) | "True of every provider" | Rates; census; compensation incentives (SROG 23–26 refused) | RFP 10–12; motion to compel |
| 13 | Smith knew and directed | Her acts | HOPE_000231, 000189 [V] | Admission | Smith; Palacios; Delucchi | SROG 10 excludes her | Smith emails and approvals | ESI custodians |
| 14 | HOPE knew of his work obligations | Notice | HOPE_000199 (Apr. 2022 agent email: "works fulltime, gets home daily around 2 pm"); HOPE_000143 (moved to a 6:30 pm group "to accommodate work") [V]; contrast SROG 36–40 ("no knowledge") | Business records | Arestad; Serrano | "We did accommodate" | The 2025 FedEx request (Matter 3) | RFP 13 |
| 15 | Prolonged supervision harmed him | Causation | — | — | — | Policy 19-03 (1502-DR p. 4) [V] | — | Probably cannot be proven against HOPE before ~mid-2027 |

## 7.2 Ten strongest Plaintiff exhibits

1. HOPE_000293–295: HRSO double-Core, aftercare for the full term, no discharge, certificate to ARMS only.
2. HOPE SROG 13 (verified): CDCR's pre-October 2024 full-term policy.
3. Dwyer Order at 4, 6–7, 10–11: Loree's testimony; parole defers to the provider; "vitiates the Legislature's directive."
4. HOPE SROG 28/30 against the Dwyer Order: impeachment.
5. Dkt. 15-1 Ex. B at 7: the defense quotes "fixated on lawsuits" and defends it.
6. HOPE_000208–217 and SROG 14: no plan revision since 2022/2023.
7. HOPE_000224 with 000105–111 and 000204/206: the March 2025 reset and the March 2026 post-suit catch-up entries.
8. Form 1502-DR p. 4: LS/CMI 5, "Level 2 below average Risk," "HOPE SOT recommends continued treatment," and "Eagan."
9. HOPE_000269 and 000295, plus SROG 15/17: HOPE in CDCR's ARMS; CDCR owns the records (state action).
10. HOPE_000190: grace revocation, Feb. 20, 2025.

## 7.3 Ten most damaging defense exhibits

1. Form 1502-DR p. 4: Policy 19-03 time-served as the stated basis (causation).
2. SROG 11: Block I incomplete at every CTM from 2022 to 2025 (failure to complete).
3. HOPE_000224: preparatory modules mostly blank; Block II about a quarter complete as of March 2026.
4. Form 1502-DR p. 1: two 2025 failure-to-attend-treatment violations; missed 6 sessions; five violations.
5. HOPE_000174: Oct. 2023 polygraph with significant reactions. The examiner described him as "without concern and indifferent."
6. HOPE_000184–186: in custody Nov. 1–12, 2024.
7. HOPE_000142/194: the CDCR agent ordered the no-show (undercuts the retaliation story).
8. HOPE_000143/199: HOPE accommodated work in 2022 (undercuts "no CDL accommodation").
9. Static-99R 4 ("high risk") per the manual and Dwyer (supports the "risk-based" defense).
10. Matter 3 Doc. 31 (state action rejected; Rule 11 reminder), plus the defense's catalogue of dismissed suits (Dkt. 15 at 8 n.1).

## 7.4 Contradictions to lock in

- **SROG 28/30 vs. the Dwyer Order.** HOPE claims no knowledge of Dwyer; its executive testified there.
- **SROG 33/35 vs. Palacios RFAs 11–12 and 16.** HOPE claims no knowledge of statements its Site Director admitted. **[V-p on the RFAs]**
- **SROG 36–40 vs. HOPE_000143/199.** HOPE claims no knowledge of his work, against its own notes of a work-based schedule change.
- **SROG 11 (Aug. 19, 2025: "had not completed Block I") vs. HOPE_000224.** The audit shows every Block I module dated 3/24/25 except 1.7.4 "Denial 2." Pin down whether a single module kept him in Block I for a further five months.
- **SROG 12 ("individualized factors") vs. HOPE_000293 (HRSO double-Core regardless of progress) and HOPE_000208–217 (stale goals).**
- **Dkt. 15 at 13 ("with prejudice") vs. Ex. C ("without leave to amend").**

---

# 8. Defense roadmap: what competent counsel does next, and the answer

| Next defense move | When | Plaintiff's answer |
|---|---|---|
| Reply adding Matter 3 Doc. 31 (state action), *Wilson/Sharper Future*, and "Plaintiff concedes…" points | Oct. 13 | At the hearing: Doc. 31 addressed Palacios on a different pleading. The theory here is § 3008(d)(2) delegation plus § 3574(f) co-signature plus Dwyer deference. Ask for leave to plead the Bates-keyed facts. |
| Ask for dismissal **without leave** citing serial filings | Oct. 13 / hearing | *Lopez*. Identify concrete curative facts by Bates number (Section 4). |
| Move to stay discovery pending the motion | With the CMC statement | Oppose. No automatic stay in N.D. Cal. Offer targeted first-wave discovery (Section 9, Wave 1). |
| Answer raising statute of limitations, the two-dismissal rule, Heck, § 47(b) | After any amended complaint | Plead discrete post-July 20, 2024 acts. Do not concede the two-dismissal point. Drop GPS/discharge damages. |
| Anti-SLAPP motion against amended Bane/fraud | Within 60 days of service of the amended complaint **[verify federal timing]** | Do not replead state claims premised solely on reports to CDCR. Build the state claims on non-communicative acts (grace revocation; HRSO double-Core rule), or drop them. |
| Rule 11 letter (RICO; miscited Dwyer; unsupported "sole provider" and revenue figures) | Any time | Remove those allegations now (Section 13). |
| Early Rule 68 offer (low) | After the motion is decided | Rule 68 shifts only *costs*, unless an underlying statute defines costs to include fees. § 1988 fees are not shifted against a pro se plaintiff (*Marek v. Chesny*; *Hughes v. Rowe*) **[verify]**. Run the settlement-guard ledger first. |
| Summary judgment: causation (Policy 19-03), failure to complete, risk, no state action | After discovery | Section 10. |
| Vexatious-litigant narrative or pre-filing order request | If more suits follow | Stop new HOPE-cluster filings. Keep Matter 28 as the single vehicle and Matter 19 as the habeas track. |

---

# 9. Discovery strike plan (leverage-ranked)

**Timing.** The Rule 26(f) conference reportedly happened Sept. 29 **[V-p]**, so discovery is open (Rule 26(d)(1)). Serve **Wave 1 now**: it is narrow, it supports state action and retaliation, and it is hard to resist. Serve **Wave 2** (financial, comparators, Smith ESI) after the motion is decided.

## 9.1 Wave 1 — serve immediately (requests for production)

| # | Request | Element | Expected objection | Narrowing |
|---|---|---|---|---|
| RFP 1 | Every "Progress Report and Treatment Plan Update" and every other CTM submission about Plaintiff, Aug. 2024 – present | Retaliation; due process; Monell | "CDCR property" (SROG 17) | HOPE prepares them in TreatAnyone (HOPE_000272), so HOPE has possession, custody, or control (Rule 34) |
| RFP 2 | Every Form 3043 for Plaintiff, signed or unsigned, plus proof of delivery within 30 days | § 3574(f) process | "CDCR form" (SROG 3) | HOPE signs as provider; its copy or draft is within its control |
| RFP 3 | Titration tracking forms and Clinical Director approvals or denials | Individualization | Burden | One client, one file |
| RFP 4 | Every version of the Clinical Operational Manual, 2019 – present, with redlines | Monell policy; post-Dwyer and post-§ 3574 changes | Proprietary | Protective order |
| RFP 5 | TreatAnyone audit log for Plaintiff's chart (creation, edit, user, timestamp), 2021 – present | Reset; post-suit alteration (Mar. 9, 2026 entries) | ESI burden | One chart; export report |
| RFP 6 | Group schedules, cancellations and clinician assignments for Plaintiff's groups | HOPE-caused delay | Third-party privacy | Anonymize other clients |
| RFP 7 | The body and attachments of HOPE_000190 (grace period) and HOPE_000192 (Palacios forward) | Retaliation | None strong | Specific Bates |
| RFP 8 | Every risk instrument scored for Plaintiff (Static-99R, STABLE-2007, LS/CMI, ACUTE) with score sheets | Risk defense | None | Own file |
| RFP 9 | Every communication about Plaintiff's complaints, CASOMB inquiry, or lawsuits (Palacios, Delucchi, Shinske, Smith, Hansen), Jan. 2025 – present | Knowledge; motive | Privilege | Log communications not involving counsel |

**Preservation letter (send this week).** TreatAnyone data and logs; Almax Consulting systems; hopeprogram.biz and almaxconsulting.com email for the custodians below; ARMS upload logs; CTM recordings if any; policy-version files.

## 9.2 Wave 2 — after the motion is decided

| # | Request | Element | Objection | Narrowing |
|---|---|---|---|---|
| RFP 10 | HOPE–CDCR/DAPO master contract(s), statements of work, and rate sheets, 2021 – present (Matter 6 notes cite Master Contract No. 901949 **[U]**) | State action (contract terms: "prohibited from discharging"); motive | Confidential | Protective order; it is a public contract, so also send a CPRA request to CDCR |
| RFP 11 | Stockton census, admissions, graduations, titrations and aftercare transfers of parolees, by year (anonymized) | Comparators; custom | Privacy; burden (SROG 6 refused) | Aggregate counts only |
| RFP 12 | Revenue per CDCR client by category; compensation and bonus metrics for site directors | Motive; punitive damages | Financial privacy (SROG 23–26 refused) | Aggregate; attorneys'-eyes-only tier |
| RFP 13 | Communications with parole agents about Plaintiff's schedule or employment | Damages; retaliation | Burden | Named agents, date range |
| RFP 14 | Smith's communications about retention or completion policy, Dwyer, § 3574 and NCR 25-01 | Smith's personal participation | Apex / burden | Search terms |
| RFP 15 | CASOMB certification file and audits for the Stockton site | Policy compliance | Third party | Subpoena CASOMB |

**ESI custodians.** Smith; Shinske; Loree; Hansen; Kingston; Palacios; Delucchi; Akins; Tassone; Boatner. Mailboxes on almaxconsulting.com: operations; kphaysaleum; jaldana.
**Date range.** Mar. 1, 2021 – present.
**Search terms.** Newanforbi OR BF3571; "aftercare" w/10 parole; Dwyer; "3574"; "3043"; titrat*; "HRSO" w/10 "twice"; "lawsuit*" w/20 (Newanforbi OR client); "grace period"; ringleader; "fixated"; "catch up".

## 9.3 Third-party subpoenas

- **CDCR/DAPO** (Rule 45, or a CPRA request for public contract records):
  - Plaintiff's Form 3043s, 1502-DRs and CTM files.
  - Policy 19-03 (Amended) and the October 2024 policy change.
  - The SOMP contract with HOPE.
  - The Sex Offender Unit's CTM report standards.
  - ARMS entries for Plaintiff.
- **San Mateo Superior Court:** the *Dwyer* hearing transcript and exhibits (Loree testimony).
- **Almax Consulting LLC:** the TreatAnyone audit trail.
- **California Forensic Credibility Assessments (Legg):** the polygraph report and charts. The defense will use the results, so get them first.
- **CASOMB:** certification and provider list for the Stockton region. This decides the "sole provider" allegation.

## 9.4 Twenty highest-value RFAs (draft)

1. Admit that HOPE's Clinical Operational Manual dated Sept. 23, 2024 was in effect at HOPE's Stockton facility from Sept. 23, 2024 to the present.
2. Admit that under that manual a client designated HRSO must complete all Core Treatment Phase modules twice.
3. Admit that HOPE designated Plaintiff HRSO throughout his enrollment.
4. Admit that a Static-99R score does not decrease because of progress in treatment.
5. Admit that, as of Sept. 23, 2024, HOPE's manual required parolees who completed the Maintenance Phase to remain in the Aftercare Phase until discharge from parole.
6. Admit that between Apr. 17, 2025 and the present, HOPE did not revise the "Aftercare Phase" section of its Clinical Operational Manual.
7. Admit that Dr. Cristina Loree testified at the March 9, 2023 evidentiary hearing in *In re Dwyer*, San Mateo Super. Ct. No. SC-080355A.
8. Admit that Dr. Cristina Loree was HOPE's Executive Director of Clinical Training and Development on March 9, 2023.
9. Admit that Plaintiff's LS/CMI score on Oct. 15, 2024 was 5.
10. Admit that HOPE did not score Plaintiff at an LS/CMI of 11 or higher at any time after Apr. 17, 2025.
11. Admit that HOPE did not sign a CDCR Form 3043 stating good cause to retain Plaintiff after the Aug. 19, 2025 CTM.
12. Admit that HOPE did not deliver to Plaintiff, within 30 calendar days, a written retention determination for the Aug. 19, 2025 CTM.
13. Admit that the same as RFA 12 is true for the Feb. 18, 2026 CTM.
14. Admit that a HOPE report transmitted to CDCR in 2026 stated, in substance, that Plaintiff "is fixated on lawsuits instead of subject material."
15. Admit that Plaintiff's lawsuits were a reason stated in a HOPE report for Plaintiff's lack of progress.
16. Admit that HOPE revoked Plaintiff's attendance grace period on or about Feb. 20, 2025.
17. Admit that Plaintiff's Individualized Treatment Plan dated Oct. 18, 2023 has not been revised.
18. Admit that Plaintiff was not shown the Oct. 18, 2023 Individualized Treatment Plan before Jan. 1, 2026.
19. Admit that HOPE's Stockton facility issued no HOPE Treatment Completion Certificate to any CDCR parolee between Mar. 1, 2021 and Oct. 14, 2024.
20. Admit that the "Catch Up Homework" entries at HOPE_000204 and HOPE_000206 were created on or after March 9, 2026.

## 9.5 Twenty Rule 30(b)(6) topics

1. Versions, authorship, approval and revision history of the Clinical Operational Manual sections on HRSO, titration, graduation, aftercare and discharge (2019 – present).
2. The origin of, and contract basis for, "Due to specific guidelines within our contracts, HOPE is prohibited from discharging a client from treatment for any reason" (HOPE_000294).
3. The "CDCR policy" described in SROG 13 and the change HOPE says CDCR made in October 2024, including the documents by which HOPE learned of it.
4. HOPE's practice changes, if any, after Mar. 20, 2023 (Dwyer), Oct. 14, 2024 (emergency § 3574), and Apr. 17, 2025 (permanent § 3574).
5. HOPE's knowledge of *Dwyer*, including Dr. Loree's testimony, and the basis for SROG 28/30.
6. The HRSO designation: criteria, effect on frequency and Core repetition, and whether it is ever removed.
7. How HOPE prepares, signs, transmits and delivers Form 3043s; its retention of copies; and its compliance with the § 3574(f) 30-day delivery requirement.
8. CTM report preparation (HOPE_000268–276), including the Sex Offender Unit's content requirements and the CTM representative's editing role.
9. Plaintiff's treatment chronology: assignments, resets, clinician changes, cancellations, titration reviews.
10. The March 2025 Block I reassignment and the March 2026 "Catch Up Homework" entries.
11. TreatAnyone and Almax systems: audit logs, user accounts (including "Shannon Smith" as an assigning user), retention.
12. Homework intake, logging and loss (SROG 18–22).
13. Static and dynamic risk scoring of Plaintiff, and the use of scores in retention decisions.
14. The basis for each CTM retention reason in SROG 11.
15. The Aug. 19, 2025 CTM: attendees, statements, report, and HOPE's investigation (SROG 32–35).
16. The Feb. 20, 2025 grace-period revocation.
17. HOPE's receipt of, and response to, Plaintiff's complaints, CASOMB inquiry and lawsuits (including the HOPE_000189 notice to Smith and Shinske).
18. Compensation structure under the CDCR contract(s), and revenue effects of discharge (SROG 23–27).
19. Stockton graduation, titration and aftercare counts for CDCR parolees, 2021 – present (SROG 6).
20. Document preservation steps taken since Jan. 6, 2026.

---

# 10. Summary-judgment survival plan (assuming some claims survive)

| Claim | Fact dispute that defeats SJ | Already possessed | Controlled by defense or CDCR | Declarations and authentication | Hearsay | Expert? | Causation proof | Defense's best SJ point |
|---|---|---|---|---|---|---|---|---|
| 1A retaliation (HOPE) | Whether the litigation reference and the grace revocation were motivated by protected activity | Dkt. 15-1 Ex. B at 7; HOPE_000190; Palacios RFAs [V-p] | The CTM reports; emails | Plaintiff's declaration (complaints made, dates); Palacios's deposition | Party admissions | No | Timing plus the express litigation reference; a *Mt. Healthy* same-decision defense is likely **[verify standard]** | Same decision: "he hadn't finished Block I anyway" (SROG 11) |
| Due process (HOPE) | Whether written good cause and delivery occurred | § 3574(f); HOPE_000208–217 | Form 3043s | Plaintiff's declaration: never received | Public records (FRE 803(8)) | Possibly a CASOMB-standards expert | Treatment sessions he would not have had to attend | No protected interest; any defect is CDCR's |
| Monell policy | Whether the written rules (not risk) dictated duration | HOPE_000288–295; SROG 13 | Comparator counts | 30(b)(6) | Admissions | **Yes: SOMP/CASOMB expert** on whether HRSO double-Core and aftercare-to-term follow from RNR/CASOMB or contradict them | Expert: individualized review would have titrated him by date X | "Static-99R 4 is high risk; the policy is evidence-based" |
| Smith | A post-notice decision to keep the policy | HOPE_000189, 231 | Her emails | Smith deposition | — | — | — | No personal act (SROG 10) |
| Bane | Specific intent | As for retaliation | — | — | — | — | — | Privilege; no intent |

**Narrow before SJ if discovery does not produce the following.**
- **Due process:** drop if Form 3043s were signed and delivered on time.
- **Smith:** drop if no Smith email or approval about retention, Dwyer, § 3574 or Plaintiff exists.
- **Bane:** drop if the retaliation count weakens.
- **Fraud and RICO:** should already be gone.
- **Discharge-based damages:** drop in all events (Policy 19-03).

---

# 11. Depositions and cross-examination

## 11.1 HOPE Rule 30(b)(6) (probably Shinske or Hansen) — take first

**Sequence.**
1. Authenticate the manual (HOPE_000225–349) and its versions.
2. Lock HRSO double-Core (000293) and aftercare (000294).
3. Pin down "contracts" (000294) and SROG 13.
4. Ask whether anything changed after Dwyer or § 3574, and when.
5. Plaintiff's file: SROG 11 reasons; HOPE_000224; the March 2026 catch-up entries.
6. Form 3043 practice.
7. Knowledge of Dwyer (SROG 28/30).

**Expected evasions.** "CDCR's form, CDCR's policy, CDCR's records."

**Follow-ups.**
- "Who at HOPE signs the 3043?"
- "Is a draft in TreatAnyone?"
- "Did HOPE ever refuse to sign a retention?"
- "Name one Stockton parolee titrated to aftercare before 2025."

**Impeachment.** Dwyer Order at 4 and 7 against SROG 28/30.

**Do not assume without foundation:**
- that the HRSO double-Core rule was applied to Plaintiff (ask);
- that Plaintiff's file contains a 3043;
- the per-parolee revenue figures.

## 11.2 Shannon Smith

**Sequence.**
1. Background; founding (HOPE_000231 "her vision").
2. Roles in 2021–2026; why SROG 5 omits her.
3. Approval authority over the manual.
4. Knowledge of Loree's 2023 testimony.
5. Response to CDCR's October 2024 change and to § 3574.
6. HOPE_000189: what she did on receiving the January 2026 suit.
7. Compensation tied to census (if the defense's apex objection fails).

**Needed admissions.** She approves manual policy, or delegated it to named executives. She knew by 2023 or 2025.

**Expected evasion.** "Operations are delegated." **Follow-up:** "To whom, in writing, and did you review the aftercare section?"

**Foundation trap.** Do not ask "why do you keep everyone until discharge." Ask whether a Stockton CDCR parolee has ever left HOPE's treatment by graduation rather than by parole discharge or custody.

## 11.3 Clinicians

- **Palacios.** Aug. 19, 2025 statements; the "when you start complaining…" line; grace revocation; authorship of "fixated on lawsuits"; the June 2024 "no homework found" statement (SROG 22 denies knowledge).
- **Boatner.** Why Block I was reassigned in March 2025.
- **Hansen.** The March 9, 2026 catch-up entries, and who asked for them after the suit.
- **Tassone.** The Oct. 18, 2023 plan: was it shown to Plaintiff?
- **Akins.** Nov. 2022 statements; the cancellations.
- **Loree.** Dwyer testimony; whether aftercare remained mandatory after October 2024.

## 11.4 Parole: Moua, Derrick, Noguchi, Dodd; CDCR SOU (Stout or successor)

**Purpose: neutralize causation and build joint action at the same time.**
- "Does parole defer to HOPE's treatment recommendation?" (Dwyer at 6)
- "Who drafted the 1502-DR treatment paragraph? Did HOPE supply the 'Stable 6/LSCMI 5... HOPE SOT recommends continued treatment' text?"
- "Absent Policy 19-03, would you have recommended discharge?" Ask only if the answer is known from an interview or prior record. **Otherwise do not ask.**
- **Moua:** the Mar. 31, 2026 no-show instruction (HOPE_000142).

## 11.5 Defense expert (if any)

**Lock in:**
- Static-99R is static.
- RNR calls for **less** intensity for lower-need clients.
- CASOMB guidelines treat the completion determination as individualized.
- What dynamic-score threshold would justify titration?

## 11.6 Cross plan for "he remained because he was high risk and failed to complete"

1. **"High risk" means one number that never moves.**
   - "His Static-99R is 4." "That score cannot go down with treatment." "Your manual sets frequency and double-Core by that score alone." (HOPE_000288, 293)
2. **His changeable risk is low.**
   - "Your own Oct. 15, 2024 numbers: STABLE 6, LS/CMI 5." "CDCR wrote 'Level 2 below average Risk.'" (1502-DR p. 4)
   - "The regulation's example of good cause to retain is an LS/CMI of 11 or higher." (§ 3574(f)(1))
3. **"Failure to complete" is measured on a track HOPE reset.**
   - "Block I modules all dated 3/24/25, four years in." (HOPE_000224)
   - "Assigned 3/23/25 by a new clinician." (000105–111)
   - "Your catch-up entries were made Mar. 9, 2026, after he sued." (000204/206)
4. **Completion would not have ended treatment anyway.**
   - "Graduation moves him to Aftercare until parole ends." (000294–295)
5. **HOPE disrupted his progress.**
   - Name each cancellation and each clinician change.
6. **Concede the bad facts first** (missed sessions, 2025 violations, the polygraph). Then show they appear nowhere in SROG 11's stated reasons, which were Block I or II only.

---

# 12. Trial architecture

**Theory in one sentence.** HOPE ran a treatment program in which a fixed risk score and a full-term aftercare rule, not the client's progress, set how long a parolee stayed. When Plaintiff complained and sued, HOPE told his parole team that his lawsuits were the problem.

**Plaintiff's opening theme.** "Finish line on a treadmill." **Defense's theme.** "A high-risk sex offender who did not do the work, and who sues everyone."

**Three facts the jury must believe.**
1. HOPE's own written rules kept him in treatment regardless of progress.
2. HOPE's reports to parole linked his complaints and lawsuits to non-completion.
3. That cost him something real: time, work, or dignity.

**Three facts the defense will emphasize.** The offense and the Static-99R score; missed sessions, violations and the polygraph; Policy 19-03 (parole would have kept him anyway).

**Witness order.**
1. Plaintiff (short; complaints chronology).
2. HOPE 30(b)(6) adverse.
3. Loree adverse (Dwyer).
4. Palacios adverse.
5. Hansen (catch-up entries).
6. Noguchi or Moua (deference).
7. Damages witness (employer or W-2 custodian).
8. Plaintiff's expert.
9. Plaintiff (rebuttal).

**Exhibit order.** Manual pages 288 → 293 → 294 → 295; SROG 13; Dwyer pp. 4, 10–11; CTM report ("fixated on lawsuits"); HOPE_000190; HOPE_000224 / 105–111 / 204–206; 1502-DR p. 4.

**Demonstratives.**
- A timeline of five years with phase position, clinician changes, cancellations and complaints.
- A "risk dashboard" showing Static (fixed) against STABLE and LS/CMI (low).
- A flowchart showing that completion leads to aftercare, which ends only at parole discharge.

**Evidentiary motions.**
- Motion in limine to exclude or limit offense details (FRE 403). Plaintiff will not get full exclusion, because the defense needs risk context. Seek a stipulated neutral description.
- Exclude other lawsuits except to the extent they are the protected activity (FRE 404(b), 403).
- Limit the polygraph. Polygraph evidence is generally inadmissible for truth in the Ninth Circuit **[verify current standard]**.
- Admit the Dwyer order only for notice and for Loree's statements, with a limiting instruction.

**Jury instructions.**
- Ninth Circuit Model Civil Instructions on § 1983 private-entity liability (Monell), retaliation (including but-for and substantial-factor causation), nominal damages, and punitive damages **[verify current model numbering]**.
- State action is a question for the court where the facts are undisputed. Otherwise use special interrogatories.

**Verdict form.**
1. State action (if submitted).
2. Retaliation by HOPE through policy or ratification.
3. Damages: compensatory, then nominal.
4. Punitive damages against HOPE and/or Smith (separate phase for net worth).

**Closing.** "Their rules; their reports; their timing." Then the damages ask, scaled to proof.

**Emotional versus legally material facts.**
- *Emotional:* years in group, the "ringleader" label, lost trucking career.
- *Material:* HOPE_000293/294, SROG 13, the "fixated on lawsuits" report, the § 3574(f) process, the timing.

---

# 13. Damages and causation audit

| Category | Against HOPE? | Proof | Problems |
|---|---|---|---|
| Lost CDL wages ($72k/yr "but-for") | **Weak** | W-2s 2022–2024 total $109,408+, an average of about **$36k/yr**, not $72k **[V-p]** | He worked full time while enrolled in 2022 (HOPE_000199) **[V]**. Gaps are attributable to other events (custody Nov. 2024; CHP matters 1/20; Derrick's FedEx scheduling in Matter 3; Policy 19-03). **Do not repeat "$72k but-for."** |
| FedEx ($20/hr, resigned ~Apr. 17, 2025) | Partial (Palacios's role in the scheduling denial) | Offer letter; resignation; pay records | Also claimed in Matter 3 and Matter 30 (Derrick/Moua). **Shared-loss rule: claim it once, apportion by defendant.** |
| Treatment burden (time, travel, copays if any) | Yes | Attendance records; Plaintiff's declaration | Who pays for treatment? If CDCR pays, there is no out-of-pocket loss **[U]** |
| Emotional distress | Yes (garden variety) | Plaintiff's testimony | No treating-provider evidence; keep it garden variety to avoid a Rule 35 exam |
| Nominal | Yes, for any proven violation | — | $1 (*Carey v. Piphus*, 435 U.S. 247) |
| Punitive — Smith | Only if she is personally liable | Post-Dwyer knowledge | Reckless indifference standard (*Smith v. Wade*, 461 U.S. 30) |
| Punitive — HOPE | Arguable (private entity) **[verify]** | Same | Insurance excludes intentional acts, so collection comes from corporate assets |
| Prolonged parole, GPS, curfew | **No** | — | Heck risk; Policy 19-03; § 3000.07. **Remove.** |
| Declaratory or injunctive relief | Possible against HOPE (prospective) | — | The real length remedy is the § 3008(d)(2) court approval (Matter 19) |
| RICO treble damages | **No** | — | Drop |
| Bane fees and damages | Only if Bane survives | — | — |

**Shared-loss rule.** One wage-loss figure, documented once, apportioned across Matters 3, 20 (CHP), 28 and 30, with HOPE's share limited to HOPE-caused scheduling or treatment conflicts. The damages range in `damages.json` ($249,000 – $1,510,000+) is not supported by the record for this defendant. Rebuild it from line items.

---

# 14. Settlement and insurance

**No offer ledger exists for Matter 28** (`internal/private/negotiation/28.jsonl` is missing). Per `.claude/skills/settlement-guard`, build the ledger and a valuation file, and run `npm run negotiate:check`, **before** any number goes to the defense. The brackets below are analytic valuations, not proposed moves. The rejected $280,000 demand plus certificate plus 3043 recommendation, with no counteroffer, is on the record **[V-p]**. Do not bid against it unprompted.

**Insurance structure.**

| Policy | What it covers | Key terms | Status |
|---|---|---|---|
| Philadelphia Indemnity No. 067968, professional liability | Occurrence-based, per policy year | Corporation: $1M each incident / $5M aggregate. **Individual limits "N/A."** Coverage B supplemental $1M/$5M. Defense costs paid **outside** limits ("will not reduce the limits"). | HOPE_000002, 007 **[V]**. Only the **2023–24** declarations were produced. **Get 2021–2026.** |
| Same policy — exclusions | — | Intentional wrongful acts (f); criminal, dishonest, fraudulent or malicious acts; personal profit; unfair competition; publication with knowledge of falsity | HOPE_000005–006 **[V]** |
| D&O / EPL No. PHSD1838240-007 | Claims-made, 11/27/2025 – 11/27/2026 | D&O Part 1 limit **blank**; EPL $1M; aggregate $1M | HOPE_000044 **[V]**. **Smith probably has no D&O coverage** **[I]**. EPL does not apply (Plaintiff is not an employee). |

**Coverage pressure.**
- Fraud, RICO, punitive and intentional-retaliation theories give the carrier exclusion arguments and reservation-of-rights leverage. They **reduce** the funds actually available to pay.
- A negligence-framed "professional incident" theory (failure to follow § 3574 or CASOMB standards in the clinical determination) sits squarely within Coverage A. That theory is now mainly available inside the due-process and Monell framing.
- **Smith's personal exposure is probably uninsured.** That is real pressure, but only if a Smith-specific claim survives.

**Defense-cost accumulation.** Defense is outside limits and paid by the carrier, so HOPE feels little cost pressure. The carrier feels it through the motion, discovery and SJ: roughly **$75k – $175k** through SJ for two defendants **[I — estimate, not record]**. The carrier's "deterrence posture" is rational while the dispositive motion is pending. It changes when discovery costs become real.

**Events that create leverage.**
- Denial of the motion on § 1983 against HOPE.
- An order compelling SROG 6 and 23–27 (comparators and revenue).
- 30(b)(6) testimony confirming the HRSO double-Core and aftercare rules, and impeachment on Dwyer.
- Production of the "fixated on lawsuits" report.

**Effect of narrowing.**
- Losing RICO **improves** clarity and value: it removes coverage exclusions and Rule 11 noise.
- Surviving on constitutional claims only does not lower value much, since RICO's value was near zero.

**Certificate and Form 3043 relief.**
- A completion **certificate** issues only on graduation from Maintenance (HOPE_000295). HOPE cannot ethically or practically certify completion as part of a settlement unless its clinical criteria are met. Expect refusal.
- Form 3043 is CDCR's form, co-signed by the agent. HOPE can **recommend** but cannot deliver discharge.

**Non-monetary terms HOPE can actually perform.**
- Within 30 days, an independent titration review by a clinician outside the Stockton chain, with written criteria and reasons.
- Credit for completed modules, with the record corrected.
- Removal of litigation references from clinical reports.
- An HRSO-to-non-HRSO group pathway on a written timeline.
- A CDL-compatible group schedule or telehealth.
- Delivery of every Form 3043 and CTM report to Plaintiff within 30 days.
- A neutral statement to CDCR.
- A non-retaliation term.
- Support for a stipulated § 3008(d)(2) length determination in Matter 19.

**Rational value brackets by stage [I — judgment, not a demand].**

| Stage | Bracket |
|---|---|
| Now, before ruling | Defense-cost value only: $5k – $20k plus performable terms |
| § 1983 against HOPE survives Rule 12 | $25k – $75k |
| Discovery confirms policy, impeachment and a retaliation document | $75k – $175k |
| SJ denied on retaliation and Monell | $100k – $250k |
| Trial | Wide variance: nominal to low six figures. Causation limits economic damages. |

---

# 15. Costs and downside exposure

**Rule 54(d)(1) and 28 U.S.C. § 1920 — taxable to a prevailing defendant.**
- Clerk and marshal fees.
- Transcripts "necessarily obtained": Plaintiff's deposition is the big item, roughly $1,000 – $3,000 per day with exhibits.
- Witness fees and mileage.
- Exemplification and copies necessarily obtained.
- N.D. Cal. Civ. L.R. 54 governs the procedure: the bill of costs is due within 14 days of judgment **[verify]**.

**Not taxable.** Attorney fees; the defense's own time; most e-discovery processing **[verify for N.D. Cal.]**; mediation; expert fees beyond the statutory witness fee.

**Expected amount.**

| Stage | Expected taxable costs |
|---|---|
| Dismissal at Rule 12 | ~$0 – $500 |
| After discovery and SJ | ~$3k – $12k |
| After trial | ~$8k – $25k |

**Indigence and discretion.** The Court may decline to tax costs in light of the losing party's limited resources, the case's public importance, and the chilling effect (*Ass'n of Mexican-American Educators v. California*, 231 F.3d 572 (9th Cir. 2000) (en banc); *Escriba v. Foster Poultry Farms*, 743 F.3d 1236 (9th Cir. 2014)) **[verify pins]**. The IFP application was denied as moot after the fee was paid. Keep a current financial declaration ready.

**Fee shifting.**
- **§ 1988.** Fees to a prevailing defendant only if the claim was frivolous, unreasonable or without foundation (*Christiansburg*, 434 U.S. 412; *Hughes v. Rowe*, 449 U.S. 5 (pro se)).
- **RICO.** § 1964(c) shifts fees only to a prevailing plaintiff.
- **Bane § 52.1.** Fees run to a prevailing plaintiff.
- **The real risks:**
  - **Anti-SLAPP (Code Civ. Proc. § 425.16(c)):** mandatory fees for a defendant who strikes a **state-law** claim built on protected statements made in official proceedings, such as reports to parole. The Ninth Circuit's treatment of anti-SLAPP in federal court is evolving **[verify current law before relying on it either way]**.
  - **Rule 11:** RICO, unsupported revenue and "sole provider" figures, miscited authority. There is a prior Rule 11(b)(2) reminder in Matter 3.
  - **A vexatious-litigant / pre-filing order:** the narrative of serial filings.

**Steps that reduce exposure.**
1. Drop RICO and the fraud count by amendment.
2. Do not replead Bane or fraud on reports to CDCR alone.
3. Strip [U] and [X] allegations (Section 16).
4. Cite only from `MATTER_28_SAFE_CITE_LIST.md` and pin-check everything.
5. Take only the depositions you need. Plaintiff's own deposition cost is the defense's.
6. File no new HOPE-cluster actions.
7. Use Rule 15, never Rule 41(a)(1).

---

# 16. 30/60/90-day action plan

| # | Action | Owner | Deadline | Dependency | Deliverable |
|---|---|---|---|---|---|
| 1 | Pull PACER docket: hearing date, Dkt. 6, ADR certification, any reply; pull the San Joaquin register for a § 581d judgment and notice of entry | Plaintiff | **Oct. 8** | None | Updated `clocks.json` / `docket.json` |
| 2 | If the ADR certification was not filed, file it now | Plaintiff | Oct. 8 | #1 | ADR L.R. 3-5 certification |
| 3 | Send a preservation letter to SLB (systems, custodians, logs) | Plaintiff | Oct. 10 | None | Letter (no repo links) |
| 4 | Read the reply; build the hearing outline (preclusion → state action → leave to amend) | Plaintiff (`hearing-script` skill) | Oct. 15 | Reply Oct. 13 | Lectern card |
| 5 | Joint CMC statement: discovery open; protective order; related cases (Matters 3, 5, 6, 19); proposed schedule | Plaintiff + SLB | **Oct. 15** | #1 | Joint statement |
| 6 | Move for or stipulate to an N.D. Cal. protective order covering the HOPE production; confirm the state stipulated protective order permits use | Plaintiff | Oct. 15 – 22 | #5 | Proposed protective order |
| 7 | MTD hearing | Plaintiff | Oct. 20 (or 27 — verify) | #4 | Argument |
| 8 | CMC | Plaintiff | Oct. 22 | #5 | Schedule |
| 9 | Serve Wave 1 RFPs 1–9 and RFAs 1–20 | Plaintiff | Oct. 23 | #6 for confidential items | Discovery set |
| 10 | Subpoena the San Mateo *Dwyer* transcript | Plaintiff | Oct. 31 | None | Transcript order |
| 11 | CPRA request to CDCR for the SOMP–HOPE contract and Policy 19-03 (Amended) | Plaintiff | Oct. 31 | None | Request |
| 12 | Draft the amended complaint (do not file before the order): delegation/joint-action facts by Bates; retaliation centered on the litigation report and grace revocation; drop RICO and fraud; drop GPS/discharge damages; plead post-July 20, 2024 acts | Plaintiff | Ready by the order date | #7 | Amended complaint draft |
| 13 | File the amended complaint | Plaintiff | Per order (usually 21–30 days) | Order | Amended complaint |
| 14 | File CDCR grievances (15 C.C.R. §§ 3482, 3723) on any new Form 3043, CTM, or the December 2026 discharge review | Plaintiff | Within the regulatory window after each event **[verify window]** | Event | Grievance; exhaustion record |
| 15 | Build the Matter 28 offer ledger and valuation file; run `negotiate:check` before any settlement communication | Plaintiff | Before any reply to defense | None | `28.jsonl`; `28.valuation.json` |
| 16 | Meet and confer, then move to compel SROG 6 and 23–27 if discovery is open | Plaintiff | ~Day 60 | #9 responses | Joint letter (Cisneros standing order format **[verify]**) |
| 17 | Wave 2 discovery and third-party subpoenas (CDCR, Almax, CASOMB, polygraph examiner) | Plaintiff | ~Day 60 – 75 | Protective order | Subpoenas |
| 18 | 30(b)(6) deposition of HOPE | Plaintiff | ~Day 90 | #9, #17 | Transcript |
| 19 | Correct portfolio records (Section 17 list) | Plaintiff / agent | Oct. 10 | None | `matter.json`, `prose.json`, `evidence.json`, the SOMP cases doc |

---

# 17. Fatal-gap list

**Cannot presently be cured.**
- **Economic damages for prolonged parole.** Policy 19-03 independently required retention until ~mid-2027 (1502-DR p. 4) **[V]**. This also raises a Heck problem.
- **RICO.** No proximate-cause path for Plaintiff (the payor is CDCR); the predicates are clinical opinions.
- **The "$72k/yr but-for" wage rate.** His own W-2s average about $36k/yr, and he worked full time while enrolled in 2022.

**Claims to narrow or abandon (by amendment only).**
- RICO (§ 1962(c) and (d)).
- Fraud / negligent misrepresentation, unless a reliance-caused loss can be honestly pleaded.
- Substantive due process.
- Smith individually, unless the amendment can plead a specific post-notice act.
- Bane, if the retaliation count fails or the anti-SLAPP risk cannot be designed around.

**Factual assertions to stop repeating.**

| Assertion | Status | Correct version |
|---|---|---|
| "Smith directed logging no-shows for sessions Plaintiff attended (HOPE_000142/194)" | **[X]** | CDCR Agent Moua wrote "Please mark him as a no show." |
| "Dwyer judicially condemned HOPE's blanket retention policy" | **[X] as phrased** | A habeas order (petition **denied**). The court fixed one parolee's program length under § 3008(d)(2) and found HOPE's level for transferred parolees "not dependent on individualized criteria." HOPE was not a party. |
| "Loree attribution is MISCITED" (portfolio note) | **[X]** | The order recites Loree's testimony on mandatory aftercare (pp. 4, 7). Correct the citation-audit row. |
| "No parolee can ever complete before discharge" | **[X] as phrased** | Graduation and a certificate are possible; treatment (aftercare) continues until discharge. |
| "HOPE billed CDCR at $100/$200/$1,800… $106k–$111k per parolee" | **[U]** | The rates come from an Alameda County Probation contract. Revenue per CDCR parolee is unknown (SROG 23–25 refused). |
| "HOPE is the sole certified provider in Stockton" | **[U]** | Subpoena CASOMB before repeating. |
| "Res judicata… state dismissal *with prejudice*" (defense) | **[X]** | Without leave to amend; exhaustion; no judgment in the record. |
| "West v. Atkins makes CDCR contractors state actors" (`matter.json`) | Overstated | Contract alone is insufficient (*Rendell-Baker*). The theory is delegation plus joint action. |
| "Philadelphia Indemnity $1M/$5M covers this case" | Incomplete | Occurrence-year specific; corporate limits only (individual "N/A"); intentional, fraud and profit exclusions; no D&O Part 1. |
| "GPS and curfew continue because of HOPE" | **[X]** | GPS is statutory (§ 3000.07); discharge turns on Policy 19-03. |

**Unresolved record items that could change this analysis.**
1. Whether a § 581d judgment was entered in Matter 5 after July 15, 2026.
2. The as-filed opposition (did it use Dkt. 9 Exs. B–C?).
3. The actual Dkt. 1 paragraphs.
4. What Dkt. 6 is.
5. The Matter 6 original-complaint defendants, and whether Derrick/Noguchi were in it.
6. The Matter 3 Doc. 31 text.
7. The RFA response documents (RFAs 4, 9, 18, 22, 25; Palacios RFAs 6, 8, 11–12, 16, 29).

---

# 18. Direct verdict

**What this case is actually about.**
- Whether a private treatment vendor, exercising a decision the Penal Code assigns to it and co-signing CDCR's retention forms, kept a parolee in mandatory treatment because of written structural rules (a fixed-score HRSO double-Core and aftercare until parole ends) rather than his progress.
- Whether it reported his complaints and lawsuits to his parole team as a reason he was not progressing.

It is **not** a parole-discharge case. Policy 19-03 controls that.

**Strongest path to victory.**
1. Defeat preclusion with the minute order.
2. Win leave to amend on state action pleaded as § 3008(d)(2) delegation plus § 3574(f) co-signature plus Dwyer deference.
3. Replead a lean complaint: First Amendment retaliation (litigation report; grace revocation; CTM statements) and Monell (HOPE_000288/293/294).
4. Use Wave 1 discovery to obtain the CTM reports and Form 3043s.
5. Depose HOPE's 30(b)(6) on its manual and on Dwyer (SROG 28/30 impeachment).

Settlement value moves at items 2, 4 and 5, not before.

**Most likely way it dies.**
- Dismissal for lack of state action, possibly echoing Peterson's Matter 3 reasoning, if the amended pleading still reads as "HOPE had a contract with CDCR."
- Or summary judgment on causation and same-decision grounds ("he had not finished Block I," "Policy 19-03"), if discovery never produces the litigation-linked report.
- Secondary risks: an amended state-law claim drawing anti-SLAPP fees; any new Rule 41 dismissal triggering the two-dismissal bar.

**What must be done before the next major deadline (reply Oct. 13; joint CMC statement Oct. 15; hearing Oct. 20 or 27).**
1. Verify the docket and the San Joaquin register (hearing date; any § 581d judgment; Dkt. 6; ADR certification).
2. Prepare to put Dkt. 9 Exs. B–C (the tentative ruling and minute order) in front of the Court as the first thing it hears.
3. Prepare a one-paragraph distinction of the Matter 3 Doc. 31 state-action ruling.
4. File the joint CMC statement asking for discovery and a protective order.
5. Send the preservation letter.
6. Stop repeating the five [X]/[U] assertions above.
