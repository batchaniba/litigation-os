> **Superseded as spine.** Draft from `2026-09-12-matter-28-UNIFIED.md`. **§ 3.4 *Meinhardt* in this file is inverted** — the Cal. Supreme Court *rejects* deeming (UNIFIED § 5.1). Bane “rises or falls with state action” is too broad (UNIFIED § 8.3). Cisneros habits in § 4 remain good.

# Matter 28 — MTD-Prep Research Memo
## *Newanforbi v. Shannon Smith, LCSW / HOPE Psychotherapy, Inc.*, N.D. Cal. No. 3:26-cv-07504-LJC

**Compiled 2026-09-18 (evening).** Doctrinal research memorandum; not legal advice; requester is pro se.
**Defense Rule 12 response due Monday, September 21, 2026.** Defense previewed 7 grounds Sept 3, 2026
(res judicata; no state action; First Amendment retaliation; due process; Bane Act; fraud; RICO).
Meet-and-confer impasse memorialized Sept 11. CMC Oct. 22, 2026.

**What this memo is:** the NEW research pass only — live docket check, open-cite verification,
2024–2026 fresh authority, Judge Cisneros's 12(b)(6) posture. It does **not** redo the Sept 12 base.
The base lives at:
- `internal/docs/legal-intel/recon/2026-09-12-matter-28-UNIFIED.md` (briefing spine; res judicata §§ 2–6)
- `internal/docs/legal-intel/recon/2026-09-12-matter-28-hope-smith-12b6-survey.md` (7 grounds tested)
- `internal/docs/HOPE_SMITH_SOMP_CASES.md` (vendor-damages catalog; Chavez 2021 QI trap)
- `internal/docs/legal-intel/judges/lisa-j-cisneros-2026.md` (2026 docket audit)

Every item is tagged **PRIMARY** (source read directly) / **SECONDARY** (reported by a reliable
source not read directly) / **UNVERIFIED** (could not confirm). Subagent-sourced PRIMARY tags mean
the research subagent read the source text; I did not re-read each one.

> **⚠ DEPENDENCY — res judicata section pending:** A separate browser task is re-pulling the San
> Joaquin Matter 5 register (STK-CV-UF-2026-0001032) to check for a judgment entered since Sept 12.
> Its result had **not** arrived when this memo was written. The res judicata analysis below assumes
> the Sept 12 snapshot (no judgment). **Re-check the register the morning of any filing** — Van Dine
> can cure the finality defect by obtaining a judgment in Dept. 10A, and that is the single move most
> likely to change the analysis.

---

## 1. Live docket check (Matter 28, CourtListener docket 73646240)

**Result: no Rule 12 motion has surfaced; the docket could not be read directly — treat as UNVERIFIED.**

- Two direct fetch attempts on CourtListener (the `/api/rest/v3/dockets/73646240/` endpoint and the
  `/docket/73646240/` page) both failed with a browser-service `tool_failure`; no PACER token and no
  CourtListener token are in this environment, and PACER is off limits. I did not retry in a loop and
  did not work around the failure. **UNVERIFIED** as a direct docket read.
- Search-based check: Justia Dockets lists the case as *Ngehsi Newanforbi v. Smith et al*, filed
  **July 20, 2026** as **3:2026cv07504**, plaintiff Brendan Ngehsi Newanforbi, defendants Shannon
  Smith and "Hope Psychotherapy, Inc. a California corporation doing business as Hope Program,"
  cause of action 42 U.S.C. § 1983. **SECONDARY** (search-reported, not read on the docket page).
- **No motion to dismiss, answer, or other post–Sept 12 entry surfaced in any search result.**
  The Rule 12 response is due **Monday, Sept 21, 2026** — a filing today (Fri Sept 18) or Monday
  would not yet be indexed. **Re-run this check before finalizing the opposition.**
- Standing facts from the base (unchanged): served Aug 31, 2026 (Van Dine accepted for both
  defendants); Dkt. 13 POS filed Sept 3; Dkt. 11 (Aug 26) declined § 1915 screening and left
  preclusion for defendants to raise.

---

## 2. Cite verification — the seven open cites, closed

Work done by a dedicated verification subagent. Corrections first, then the table.

### Corrections that change usage

1. **Schreiber — the year is 1986, NOT 2004.** Defense's "*Schreiber Distributing Co. v. Serv-Well
   Furniture Co.*, 806 F.2d 1393 (9th Cir. 2004)" has the wrong year. Decided **December 24, 1986**.
   Use: 806 F.2d 1393 (9th Cir. 1986). One dry footnote in opposition — it signals recycled briefing.
2. **Page v. Torrey does NOT answer the parolee question.** *Page v. Torrey*, 201 F.3d 1136 (9th Cir.
   2000) is a correct cite but holds a **civil detainee** (SVP commitment), not a parolee, is not a
   PLRA "prisoner." The direct parolee-at-liberty authority is *Kerr v. Puckett*, 138 F.3d 321, 322
   (7th Cir. 1998) and *Talamantes v. Leyva*, 575 F.3d 1021, 1024 (9th Cir. 2009) — use Page only as
   supporting precedent for narrow construction of "prisoner."

### Verification table

| # | Cite (as verified) | Holding (1–2 sentences) | Tag |
|---|---|---|---|
| 1 | *Arizona Students' Ass'n v. Ariz. Bd. of Regents*, **824 F.3d 858 (9th Cir. 2016)** | Reversed 12(b)(1)/12(b)(6) dismissal: ASA stated a plausible First Amendment retaliation claim; district court erred in denying leave to amend to satisfy *Ex parte Young*. The retaliation test: (1) constitutionally protected activity; (2) defendant's actions would "chill a person of ordinary firmness"; (3) protected activity was a substantial motivating factor. | **PRIMARY** (opinion read; decided June 1, 2016, Paez, J., No. 13-16639). Pin 867 corroborated by citing orders quoting the passage at "824 F.3d at 867" — **SECONDARY for the pin number** |
| 2 | *DZ Reserve v. Meta Platforms, Inc.*, **96 F.4th 1223 (9th Cir. 2024)** | Fraud-based class action: a uniform misrepresentation communicated to all class members (Potential Reach "measures people when it really measures accounts") supports a classwide inference of reliance, sustaining class certification; rejected the defense that plaintiffs should not have relied on statements made with fraudulent intent to induce reliance. | **PRIMARY** (slip read on govinfo; filed Mar. 21, 2024, S.R. Thomas, J.). Pin 1233 maps to predominance analysis — **SECONDARY for the pin**. Cert denied, 145 S. Ct. 1051 (2025) — **SECONDARY** |
| 3 | *Zetz v. Boston Scientific Corp.*, **398 F. Supp. 3d 700 (E.D. Cal. 2019)** | Rule 9(b) requires fraud pleaded with particularity — who, what, when, where, how; "generalized allegations of misrepresentation, concealment, and unspecified sales and marketing materials lack sufficient particularity," so the fraud/negligent-misrepresentation/concealment counts were dismissed **with leave to amend**. | **PRIMARY** (order text read; No. 1:19-cv-00451-AWI-SAB, July 18, 2019). Pin 713 consistent with placement of the fraud analysis — **SECONDARY for the pin number** |
| 4 | *Cedric Kushner Promotions, Ltd. v. King*, **533 U.S. 158 (2001)** | A corporate owner/employee is a natural "person" legally distinct from the corporation itself, satisfying RICO § 1962(c)'s person/enterprise distinctness — the statute "requires no more 'separateness' than that." Key quote (533 U.S. at 163): "The corporate owner/employee, a natural person, is distinct from the corporation itself, a legally different entity with different rights and responsibilities due to its different legal status." | **PRIMARY** (read on Justia) |
| 5 | *Schreiber Distributing Co. v. Serv-Well Furniture Co.*, **806 F.2d 1393 (9th Cir. 1986)** | **Reversed** the dismissal and remanded: "the district court abused its discretion in dismissing the RICO counts **with prejudice**" instead of granting leave to amend. Authority for leave to amend, not for dismissal. | **PRIMARY** (read on openjurist; decided Dec. 24, 1986). Pins 1400–01 (leave-to-amend passage) corroborated by a federal order quoting at "806 F.2d at 1401" — **SECONDARY for the pins** |
| 6 | **Cal. Penal Code § 3008(d)(2)** — verbatim text verified on the official source, leginfo.legislature.ca.gov (egress block cleared on retry) | "[P]ersons placed on parole on or after July 1, 2012, shall **successfully complete** a sex offender management program, following the standards developed pursuant to Section 9003, as a condition of parole. The length of the period in the program shall be **not less than one year, up to the entire period of parole, as determined by the certified sex offender management professional in consultation with the parole officer and as approved by the court.** Participation in this program applies to every person described without regard to when his or her crime or crimes were committed." — (d)(1) (parole *before* July 1, 2012) requires only "participate"; (d)(2) requires "successfully complete." | **PRIMARY** |
| 7 | **42 U.S.C. § 1997e(h)** — verbatim text | "As used in this section, the term **'prisoner' means any person incarcerated or detained in any facility** who is accused of, convicted of, sentenced for, or adjudicated delinquent for, violations of criminal law or the terms and conditions of parole, probation, pretrial release, or diversionary program." — **A parolee at liberty is not "incarcerated or detained in any facility," so § 1997e(a) exhaustion does not apply to him.** Direct authority: *Kerr v. Puckett*, 138 F.3d 321, 322 (7th Cir. 1998) ("a convict out on parole is not a 'person incarcerated or detained in any facility'"); *Talamantes v. Leyva*, 575 F.3d 1021, 1024 (9th Cir. 2009) (only § 1997e(h) "prisoners" at time of filing must exhaust). | **PRIMARY** for the statutory text; **SECONDARY** for *Kerr*/*Talamantes* holdings (not read in full). *Page v. Torrey* cite confirmed but limited as noted above — **SECONDARY** |

**Net:** no item is UNVERIFIED. The three pin numbers (Zetz 713, Schreiber 1400–01, DZ Reserve 1233)
are SECONDARY — corroborated by citing authority, not checked against reporter pagination. Everything
else is PRIMARY except the parolee-carve-out holdings (SECONDARY).

---

## 3. Fresh authority (2024–2026)

Work done by a dedicated research subagent (unauthenticated sources only; no PACER; no token).

### 3.1 Adverse: the closest vendor-specific state-action authority — *Gross v. Samudio*

**[PRIMARY]** *Gross v. Samudio*, No. 14-1248 (10th Cir. Oct. 27, 2015) (Tymkovich, C.J.; Holmes,
McHugh, JJ.) — full opinion text read.
- § 1983 against the **presidents of three private sex-offender-treatment programs** (Redirecting
  Sexual Aggression, Inc.; Progressive Therapy Systems, P.C.; Sexual Offense Resource Services, LLC)
  dismissed at Rule 12(b)(6): conclusory allegations that the providers were state actors "simply
  because Colorado had contracts with the treatment providers they operated" were insufficient.
- Public-function holding: **"sex offender treatment and therapy" are not a "traditional and
  exclusive function of the state"** (citing *Wittner v. Banner Health*, 720 F.3d 770, 776–77
  (10th Cir. 2013)). Symbiotic-benefit holding: "the mere private purchase of contract services" or
  payments under government contracts are insufficient.
- **Caveats (use them):** 2015 (predates the window); Tenth Circuit; **nonprecedential** — persuasive
  value only (FRAP 32.1 / 10th Cir. R. 32.1); dismissal turned on **pleading insufficiency**, not a
  categorical rule that private vendors can never be state actors. Tension with *Chavez v. Robinson*
  (9th Cir.), where state-actor status was assumed for an individual therapist.
- **Expected use:** Van Dine will cite it for "contracts + rejection power ≠ state action." The
  answer: *West v. Atkins* (public-function delegation), the CASOMB statutory scheme (Pen. Code
  § 3008(d)(2) vests the completion determination in the certified professional — a state-conferred
  power over liberty, not mere therapy), and joint action via the Form 3043 reporting pipeline that
  gates parole discharge. *Gross* also did not involve a CEO sued for a blanket corporate policy.

### 3.2 Adverse: the 2025 N.D. Cal. preclusion authority to neutralize — *Blackwell*

**[PRIMARY]** *Blackwell v. Carrington Mortgage Servs., LLC*, No. 24-cv-06494-BLF (N.D. Cal.
Jan. 22, 2025) (Freeman, J.) — full opinion text read.
- Pro se plaintiffs; Rule 12(b)(6) **granted without leave to amend** on res judicata; dismissed
  with prejudice. Prior Monterey Superior Court action: demurrer sustained WOLA (May 15, 2018)
  **followed by a separate "Order of Dismissal With Prejudice."**
- Holding: "In California, a judgment entered after sustaining of a general demurrer is a judgment
  on the merits" — there the court sustained the demurrer **"for failure to state a cause of
  action"** and ordered dismissal with prejudice, so "there was a final judgment on the merits"
  (citing *Palomar Mobilehome Park Ass'n v. City of San Marcos*, 989 F.2d 362, 364 (9th Cir. 1993)).
- **Two clean distinguishers for Matter 28:** (a) **no judgment or order of dismissal was ever
  entered in Matter 5** — *Blackwell* anchored preclusion on the dismissal-with-prejudice order,
  not the demurrer order alone; (b) the Matter 5 demurrer ground was **exhaustion**, which the court
  itself called a "jurisdictional requirement," not failure to state a cause of action.
- **If the defense cites *Blackwell*, the opposition must lead with these two distinguishers**
  and the *Heath* n.4 / *Perez* / *Costello* line.

### 3.3 Controlling: the Ninth Circuit exhaustion rule, re-confirmed

**[PRIMARY]** *Heath v. Cleary*, 708 F.2d 1376, 1380 n.4 (9th Cir. 1983) — full opinion re-read on
Justia: "the California Superior Court denied Heath's petition for writ of mandate **on the sole
ground that he had failed to exhaust administrative remedies**… Thus the only issue necessarily
decided by the court was the propriety of granting mandamus relief in light of Heath's failure to
pursue administrative remedies." Binding circuit rule: an exhaustion-based state ruling does not
preclude a later § 1983 action.
- **[SECONDARY]** S.D. Cal. order, No. 3:14-cv-01778 (Burns, J., July 22, 2016, via Justia PDF),
  quotes the rule verbatim: **"The dismissal of an action on the ground of failure to exhaust
  administrative remedies is not on the merits."**
- **[SECONDARY]** 9th Cir. BAP memorandum (2012, via cdn.ca9.uscourts.gov): an order sustaining a
  demurrer WOLA "is considered a judgment on the merits, with res judicata effect, **as long as the
  order was based on the merits (or lack thereof) of the claims asserted and not on some formal
  defect**" (citing *Goddard*, 14 Cal.2d 47, 52; *Pollock v. Univ. of S. California*,
  112 Cal.App.4th 1416 (2003)). This is the formal-defect line that answers the defense-drafted
  formal order in Matter 5.

### 3.4 Watch: the 2024 deeming doctrine — *Meinhardt*

**[SECONDARY]** *Meinhardt v. City of Sunnyvale* (2024) 16 Cal.5th 643, 654–655 — Cal. Supreme Court
upheld deeming an order sustaining a demurrer WOLA to be a final judgment "when the ruling is
sufficiently final," quoted in *Burke v. Benworth Capital Partners*, CA4/3 No. G064478 (unpublished;
*Burke* filing date **UNVERIFIED** — crawl metadata inconsistent).
- **Why it matters:** the defense may invoke the deeming doctrine to argue the July 15 order
  *is* a judgment. **Answer:** the doctrine was articulated for **appealability**, not preclusion;
  and even a deemed judgment on an exhaustion/"jurisdictional requirement" ground is still not
  **on the merits** under *Perez* / *Heath* n.4 / *Costello*. Address it in one paragraph rather
  than letting them spring it.

### 3.5 2024–2025 generic § 1983 / QI color

- **[PRIMARY]** *Hollis Larson v. Minnesota Sex Offender Program*, No. 24-1318 (8th Cir. Oct. 7,
  2024) (unpublished per curiam; Loken, Gruender, Shepherd) — full text read on Justia. § 1983
  punitive-conditions claims precluded by the *Karsjens* class judgment; excessive-force/medical-care
  claims failed to state a claim; defendants got QI. **Caveat:** state-run MSOP — no
  *Richardson v. McKnight* private-contractor QI issue was reached. Limited use.
- **[SECONDARY]** *Montalvo*, W.D. Ky. No. 3:20-cv-00310-CHB-RSE, Doc. 128 (filed Sept. 30, 2025) —
  2025 application of *Lindke v. Freed*, 601 U.S. (2024) (via govinfo): "conduct is not attributable
  to the State unless [the defendant] was 'possessed of state authority to' act in the challenged
  way." Generic state-action framing; not vendor-specific.

### 3.6 Background intel (not a merits authority)

**[SECONDARY]** Alameda County Board of Supervisors agenda (June 18, 2024): HOPE Psychotherapy,
Inc. (Principal: Shannon Smith; Hayward) — second amendment to procurement contract **No. 26374**
for sex-offender therapy services, increased to **$150,000**, term 7/1/2023–6/30/2025 (acgov.org
PDF). Confirms HOPE's county-vendor status. Useful color for the state-action nexus; not a federal
case.

### 3.7 Verified absences (a finding, not a gap)

1. **No 2024–2026 decision** (any court) applying *West v. Atkins*, *Monell*,
   *Richardson v. McKnight*, or *Filarsky v. Delia* QI to a private sex-offender-treatment contractor
   or CASOMB-certified SOMP vendor. Closest: *Chavez* (base; state actor assumed, QI to therapist),
   *Gross v. Samudio* (2015; private providers not state actors), *Larson* (2024; state-run program).
2. **No damages ruling** (any year located; 2024–2026 priority searched) against a SOMP /
   sex-offender-treatment vendor or its CEO under § 1983, Bane Act, RICO, or fraud. The vendor-CEO
   damages question remains first impression as a located matter.
3. **No 2024–2026 federal decision directly holding** a state exhaustion-based demurrer ruling (or a
   demurrer with no judgment entered) preclusive or non-preclusive in federal court — the 9th Cir.
   rule is *Heath* n.4 (1983); contrast support from *Blackwell* and the *Goddard*/*Pollock*
   formal-defect line.
4. **No federal case naming "HOPE Psychotherapy" or "HOPE Program" (Hayward, CA)** other than the
   two known: 3:26-cv-07504 (N.D. Cal.) and 2:26-cv-00195 (E.D. Cal.).
5. **No 2024–2026 MTD ruling involving Sims Lawrence & Broghammer or Blaze Van Dine** defending a
   § 1983/Bane case — searches matched unrelated "Sims" litigants only.

---

## 4. Judge Cisneros's 12(b)(6) posture — the new layer

Work done by a dedicated judge-research subagent. Sources read in full (PRIMARY): *K.J. v. United
States*, 25-cv-07161-LJC, Docs. 34 (4/7/26) & 40 (6/22/26); *Gold Club SF, LLC v. SBA*,
24-cv-04241-LJC, Doc. 45 (9/30/25); *Goldberg v. TeachBK, Inc.*, 24-cv-04525-LJC, Doc. 41 (1/24/25);
*Stebbins v. Garcia Baz*, 3:24-cv-00398-LJC, Doc. 13 (5/2/24); her Civil Standing Order (eff.
2/17/26) and courtroom procedures page.

### 4.1 Leave to amend — default is without prejudice + leave

Her boilerplate (verbatim, *Gold Club*, Doc. 45 at 22):
> "Courts generally do not dismiss a complaint with prejudice under Rule 12(b)(6) unless it is
> clear the complaint cannot be saved by amendment. *See United States v. Corinthian Colls.*,
> 655 F.3d 984, 995 (9th Cir. 2011). '[L]eave to amend "shall be freely given when justice so
> requires."' *Leadsinger, Inc. v. BMG Music Publ'g*, 512 F.3d 522, 532 (9th Cir. 2008) (quoting
> Fed. R. Civ. P. 15(a))."

- **Default posture: dismissal WITHOUT prejudice + leave to amend.** In *Gold Club* (~18 counts),
  every dismissed count was dismissed without prejudice; plaintiffs "may file an amended [complaint]
  by October 31, 2025 consistent with this order."
- **Pro se standard** (*K.J.*, Doc. 34 at 4–5): "Where a plaintiff is proceeding pro se, as
  Plaintiffs are here, pleadings must be construed liberally and leave to amend must be given unless
  the pleading deficiency cannot be cured. *See Lopez v. Smith*, 203 F.3d 1122, 1130-31 (9th Cir.
  2000); *Erickson v. Pardus*, 551 U.S. 89, 94 (2007)." **PRIMARY** — quote this back to her.
- **The one with-prejudice dismissal found was concession-driven:** in *K.J.*, plaintiffs "do not
  oppose dismissal" of the § 1983 theory; she "deem[ed]" it withdrawn and dismissed it **with
  prejudice** (*Quisenberry*). **Tactical warning: never concede or "not oppose" any count.**
- Second chances, then consequences: when the *K.J.* plaintiffs missed the amendment deadline, she
  issued an OSC, **extended** the deadline with explicit warning, and only then dismissed —
  **without prejudice** — under Rule 41(b). She does not rush to terminate.
- Her 12(b)(6) standard follows *Starr v. Baca*'s two-part test and *Khoja* (review limited to the
  complaint, incorporated materials, and judicial-notice materials). **PRIMARY**.

### 4.2 QI at the pleading stage — UNVERIFIED (not found)

Six targeted searches ("qualified immunity," "Harlow," "Pearson v. Callahan," "clearly established"
paired with her name) returned only other judges' or other parties' cases. **No 2024–2026 order of
hers deciding QI on 12(b)(6)/12(c), and no private-contractor/state-actor QI ruling, was found.**
QI is in any event peripheral here unless the private defendants claim state action to get it.

### 4.3 Res judicata at the pleading stage — SECONDARY, thin

The only trace: her July 26, 2024 OSC in *Udo v. Bank of America*, No. 4:24-cv-01310-YGR, raising
res judicata **sua sponte via OSC** (not decided on a 12(b)(6)); case was reassigned and dismissed
without prejudice. **No order of hers deciding preclusion on a Rule 12 motion with judicial notice
of a prior judgment was found, and no statement of how demanding she is on the "final judgment on
the merits" element.** Consistent with Dkt. 11: she does not rush to preclusion; she makes parties
carry their own burdens.

### 4.4 § 1983 state-actor analysis vs. a private defendant — UNVERIFIED (not found)

No 2024–2026 order of hers deciding a state-actor / under-color-of-law / joint-action / nexus
question against a private defendant surfaced. The *Sareminaeini* 7/1/26 MTD-denial order text was
not pulled (SECONDARY via the dossier).

### 4.5 Procedure and practice notes (PRIMARY)

- **Standing Order (eff. 2/17/26):** civil motions heard Tuesdays 10:30 a.m. in person (Thursdays
  1:30 p.m. during criminal-duty months); "**matters may be decided without a hearing**"; meet-and-
  confer certification required before *any* motion; **failure to timely oppose "may be construed as
  consent to the granting of the motion ... as unopposed"** (§§ E.1–E.2).
- **AI/hallucination warning, Standing Order § E.4:** AI tools permitted, but parties "remain fully
  responsible for the final products they submit"; "Failure to verify the accuracy of briefs, and
  particularly the accuracy of citations to law and evidence, may be grounds for **sanctions and/or
  striking a filing**." Cite clean — every cite in the opposition must be verified.
- **She strikes freelancing on the docket:** in *Gold Club* she **struck** both sides' post-hearing
  supplemental filings under Civil L.R. 7-3(c) — but softened it by letting plaintiffs add the
  allegations to their SAC. Put every fact and authority in the opposition itself; no sur-replies or
  "supplemental authority" notices without leave.
- **Opposition facts can win leave to amend:** "A court should not consider facts first alleged in a
  plaintiff's opposition papers, **although such new facts may be considered when deciding whether
  to dismiss with or without prejudice.** *See Orion Tire Corp. v. Goodyear Tire & Rubber Co.*,
  268 F.3d 1133, 1137-38 (9th Cir. 2001)" (*Gold Club*, Doc. 45 at 22). **Treat the opposition as a
  leave-to-amend audition** — attach a proposed amended complaint or a detailed proffer of curative
  facts.
- **Fact-disclaimer habit:** "As factual allegations are taken as true at the motion to dismiss
  stage, this section summarizes Plaintiffs' allegations as if true. Nothing in this Order should be
  construed as resolving any issue of fact..." — she signals the MTD is not a merits adjudication.
- **Pro se support footnote** (*K.J.*, Doc. 34 at 12): she "strongly encourages" pro se litigants to
  use the N.D. Cal. Legal Help Center (415-782-8982).
- **Measured sanctioner confirmed:** *Goldberg* — denied the anti-SLAPP motion *and* denied the
  plaintiff's fee request because the motion was "not so 'totally devoid of merit' as to be
  frivolous." If defendants seek with-prejudice dismissal or sanctions on the fraud/RICO counts,
  frame it as the overreach she trims.
- **Timing:** weeks-to-months from full briefing to order; her orders are long and fully reasoned.
  No tentative-ruling practice found (standing order silent). **UNVERIFIED.**

---

## 5. Tactical takeaways for the opposition

1. **Never concede or "not oppose" any count.** She converts concessions into with-prejudice
   dismissals (*K.J.* / *Quisenberry*). Oppose every count, even weakly; argue in the alternative
   for leave to amend.
2. **Load the opposition with the facts you would add on amendment.** Per her own *Orion Tire*
   cite, new facts in the opposition can't save the claim but *can* win leave to amend. Attach a
   proposed amended complaint or a detailed proffer of curative facts.
3. **Lead with her own pro se language:** "pleadings must be construed liberally and leave to amend
   must be given unless the pleading deficiency cannot be cured" (*Lopez*; *Erickson*); "Courts
   generally do not dismiss a complaint with prejudice under Rule 12(b)(6) unless it is clear the
   complaint cannot be saved by amendment" (*Corinthian Colleges*). Make defendants carry the
   futility burden on each count.
4. **Attack preclusion on "final judgment on the merits" with precision.** She has never (on the
   public record) decided preclusion on a 12(b)(6); in *this* case she left preclusion for
   defendants to raise (Dkt. 11). Frame Matter 5's minute order — demurrer sustained WOLA, no
   dismissal language, no judgment of dismissal — as the classic non-merits disposition, and demand
   judicial notice of the actual prior-judgment documents rather than defendants' characterization.
   Ask for the § 6 ¶ 2 finding from the UNIFIED memo (even-if-a-judgment-is-later-entered, the
   ground was prematurity, not merits) in the alternative.
5. **Neutralize *Blackwell* before they cite it** (or the moment they do): two distinguishers —
   (a) no dismissal-with-prejudice order exists in Matter 5, (b) the Matter 5 ground was exhaustion
   ("jurisdictional requirement"), not failure to state a claim. Pair with *Heath* n.4 (binding).
6. **Answer *Gross v. Samudio* (if cited) with *West* + the § 3008(d)(2) scheme:** the certified
   professional's completion determination is a state-conferred power over liberty, not mere
   therapy; the Form 3043 reporting pipeline gates parole discharge (joint action); *Gross* was a
   pleading-insufficiency dismissal, nonprecedential, Tenth Circuit, 2015.
7. **One dry footnote on *Schreiber*:** defense cited it as "(9th Cir. 2004)"; it is 1986 — and it
   reversed a RICO dismissal with instructions to grant leave to amend. Signals recycled briefing;
   also use it affirmatively for leave to amend on the RICO count.
8. **Rule 9(b)-proof the fraud count in the opposition's leave-to-amend proffer:** name the
   speaker, document, date, and representation for each alleged misrepresentation (*Zetz* tells you
   exactly what she will demand: who, what, when, where, how). This is also the count most exposed
   on preclusion — particularity is its armor.
9. **Cite clean — she sanctions sloppy verification** (Standing Order § E.4). Every cite in the
   opposition must be verified; the portfolio's citation-audit history makes this non-optional.
10. **File nothing outside the briefing without leave** (no sur-replies, no supplemental-authority
    notices — she strikes them under L.R. 7-3(c)). **Calendar the opposition deadline with margin:**
    failure to timely oppose "may be construed as consent" (Standing Order § E.2).
11. **Use the *Cedric Kushner* quote** for the RICO enterprise element (Smith as "person" distinct
    from HOPE as "enterprise"); keep RICO lean and secondary per the base memo's standing guidance.
12. **The § 1997e(h) / *Kerr* / *Talamantes* point** closes the Patsy carve-out: a parolee at liberty
    is not a "prisoner," so PLRA exhaustion is inapplicable — the state exhaustion ruling cannot
    touch the § 1983 counts even if given full preclusive effect.

---

## 6. What could NOT be verified

- **Whether a Rule 12 motion has been filed in Matter 28 yet.** CourtListener fetches failed
  (tool_failure, twice); no motion surfaced via search. **UNVERIFIED** — re-check before filing.
  (Deadline: Monday, Sept 21, 2026.)
- **Whether a judgment has been entered in Matter 5 since Sept 12.** Pending the separate
  San Joaquin register re-pull. **This is the highest-priority open item** — see the dependency
  flag at the top.
- **Pin numbers** at *Zetz* 713, *Schreiber* 1400–01, *DZ Reserve* 1233: corroborated by citing
  authority, not checked against reporter pagination. **SECONDARY** on the pins.
- **QI at the pleading stage in front of Judge Cisneros:** no 2024–2026 order found after six
  targeted searches. **UNVERIFIED.**
- **Res judicata decided on a Rule 12 motion by Judge Cisneros:** only the sua sponte *Udo* OSC
  (SECONDARY). **UNVERIFIED** as a decided ruling.
- **§ 1983 state-actor analysis by Judge Cisneros against a private defendant:** none found.
  **UNVERIFIED.**
- ***Sareminaeini* 7/1/26 MTD-denial order text:** SECONDARY via the dossier; not pulled.
- **Tentative-ruling practice:** no evidence for or against. **UNVERIFIED.**
- ***Burke v. Benworth Capital Partners* filing date:** **UNVERIFIED** (metadata inconsistent);
  opinion content SECONDARY.
- **No PACER; no CourtListener token** — all reads unauthenticated; failed page fetches were not
  retried in a loop and no exec/curl was used for page fetching.
- **Dwyer March 9, 2023 evidentiary-hearing transcript:** still unobtained (base § 14 item 5).
  The order itself is verified via the Matter 19 exhibit.
- **Matter 6 still undisclosed on the Matter 28 docket** (base § 14 item 7) — disclose it; never
  voluntarily dismiss.

## Sources and method note

- Research executed by three parallel subagents (citation verification; 2024–2026 fresh authority;
  Cisneros 12(b)(6) posture) plus direct docket/search checks by the coordinating agent.
- Nothing was written into `~/workspace/interactive-litigation-portfolio/`. No email sent. No
  documents signed. No PACER accessed. No live-browser actions taken.
- The Sept 12 base memos were read in full and not duplicated; open gaps from their § 14 / § 6
  sections were the work list. Gaps closed by this pass: *Ariz. Students' Ass'n*, *DZ Reserve*,
  *Zetz*, *Cedric Kushner*, *Schreiber* (year + holding), § 3008(d)(2) verbatim text, § 1997e(h)
  text + parolee carve-out. Gaps remaining: see § 6.
