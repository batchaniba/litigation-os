> **Absorbed into UNIFIED (2026-09-19 merge).** CDN holdings (*Esche*, *Wicklund*, *Meinhardt*, *Horn* 604 U.S. 593) now live in the spine.

# Matter 28 — CourtListener / web verification (pass 2)
## *Newanforbi v. Shannon Smith, LCSW, et al.*, N.D. Cal. No. 3:26-cv-07504-LJC

**Compiled 2026-09-19 (evening).** Doctrinal research memorandum; not legal advice; requester is pro se.
**Clock:** Rule 12 / answer still **Monday, September 21, 2026**. Do not dismiss.

This is the CourtListener + CDN + web pass that PRs **#880** and **#881** could not run. Their egress proxy blocked the Ninth Circuit CDN, CourtListener, FindLaw, and Justia. This environment reached those sources. Read after the UNIFIED spine and `2026-09-19-matter-28-mtd-prep.md`. Do not draft the opposition from this file alone.

**What this file is for:** corrections that change a cite, a distinguisher, or a judge-habit claim; plus the vendor / counsel / regulation zeros that are now searched rather than assumed.

---

## 0. Relation to the other Shannon PRs

| PR | Branch | What it added | What it could not do |
|---|---|---|---|
| **#879** (this branch) | `cursor/shannon-mtd-research-b781` | Inventory + first-pass hole-close (PLRA, § 3008(d)(2), *Gross*, *Rawson* cert, *Horn* slip, *Sullivan*) | CDN / CL re-reads of *Esche*, *Wicklund*, *Meinhardt*, Cisneros MTD dockets |
| **#880** | `claude/shannon-research-mtd-ota4zv` | Restored the Sept. 18 deep-research files; Rule 12 gateway (*ASARCO* / *Khoja*); flagged *Esche* conflict and *Wicklund* as UNVERIFIED | "Independent verification of *Esche*'s disposition was not possible"; CDN blocked |
| **#881** | `intel/matter-28-mtd-prep` | Seven-cite table; *Blackwell* distinguisher; Cisneros leave-to-amend habit | *Meinhardt* holding inverted (SECONDARY); Cisneros 12(b)(6) docket-level UNVERIFIED; CL docket 73646240 unread |

Do not merge #880/#881 into this branch. Steal the holdings they got right; correct the ones they got wrong. Briefing spine remains UNIFIED.

No PACER. Unauthenticated CL search + CDN PDFs + published Cal. Supreme / N.D. Cal. text. Tokened `sweep-matter28.mjs` still unset.

---

## 1. Corrections that change a Monday opposition

### 1.1 *Meinhardt* — PR #881 has the holding backwards

**#881 § 3.4 said (SECONDARY):** the Cal. Supreme Court "upheld deeming an order sustaining a demurrer WOLA to be a final judgment 'when the ruling is sufficiently final.'" That is the *Court of Appeal* rule the Supreme Court **rejected**.

**PRIMARY.** *Meinhardt v. City of Sunnyvale*, 16 Cal.5th 643 (July 29, 2024) (Jenkins, J., unanimous), No. S274147. Opinion PDF read (Horvitz & Levy host of the filed opinion; courts.ca.gov listing confirmed).

**Holding, one sentence.** In administrative-mandate proceedings, the time to appeal "starts to run with entry of 'judgment' or service of notice of entry of 'judgment,' rather than with the filing of, or service of notice of the filing of, an 'order,' minute order, or other ruling." The Court of Appeal had treated the August 6, 2020 **Order** denying the writ as the judgment because it "did not contemplate any further action." The Supreme Court reversed that dismissal and held the clock ran from the September 25, 2020 document **titled "JUDGMENT."**

**What it is not.** It is not a demurrer case. It is not a preclusion case. It is appealability in administrative mandate.

**Opposition use, one paragraph if they invoke "deeming."** California's highest court just refused to treat a fully dispositive **order** as a judgment in order to start a clock against the appellant. The July 15 Matter 5 paper is an order sustaining a demurrer. The Stockton register still has no Judgment entry. *Meinhardt* cuts **against** converting that order into a judgment, even on the weaker appealability analogy. The merits kill remains *Perez* / *Heath* n.4 / *Costello* — exhaustion is not a judgment on the merits even if they later obtain a § 581d dismissal.

**Do not brief *Meinhardt* the way #881 wrote it.** That paragraph would hand them a doctrine the Supreme Court reversed.

### 1.2 *Estate of Esche* — safe-cite MISCHARACTERIZED is correct

**#880** flagged a conflict: the Sept. 18 deep-research memo built QI Step 1 on *Esche*; `MATTER_28_SAFE_CITE_LIST.md` marks it MISCHARACTERIZED ("REASONING only — holding is jurisdictional, not QI threshold"). #880 could not read the opinion.

**PRIMARY.** *Estate of Esche v. Bunuel-Jordana*, Nos. 24-6244, 24-6245, 24-6382 (9th Cir. Sept. 29, 2025) (Berzon, J.; Bennett, Sung) — **published**. CDN PDF `datastore/opinions/2025/09/29/24-6244.pdf` read. CL FOUND (`/opinion/10679498/`).

**Holding (staff summary + opinion):** the panel **dismissed for lack of jurisdiction**. Denial of a private hospital's **good-faith defense** to § 1983 is not immediately appealable under the collateral-order doctrine, because good faith is "a defense to § 1983 liability and not an immunity from suit." The cross-appeal on the constitutional merits fell with it. **The panel did not decide QI, state action, or the merits.**

**Reasoning that is usable (do not lead with it).** Private health-care providers can be state actors when they detain under involuntary-commitment statutes (*Rawson* / *Jensen* cited). QI "usually do[es] not apply when the defendant is a private party not serving at the government's behest." The published string is the same SAFE list already on disk: *Richardson*, *Wyatt*, *Clement*, *Jensen*, *Ace Beverage*, *Halvorsen*. *Filarsky* is distinguished as the "hired by the government to assist" case; Renown "does not assert immunity as an independent contractor acting on behalf of the government."

**Opposition use.** If they claim QI: the lead remains *Richardson* / *Jensen* / *Clement*, distinguishing *Filarsky* (brief-retention / hired-to-assist, not a standing statewide vendor CEO). Cite *Esche* only as recent published confirmation of that reasoning. **Never** as "the Ninth Circuit denied QI to private providers." That is the MISCHARACTERIZED trap. If they raise a **good-faith / followed-the-statute** defense at 12(b)(6), *Esche* + *Danielson* say it is a liability defense, not immunity from suit — and it is fact-bound, so it is a poor 12(b)(6) vehicle under *ASARCO*.

### 1.3 *Wicklund* — verified, unpublished, drop from the clearly-established string

**#880** left it UNVERIFIED and told the opposition to drop it until read. The Sept. 18 memo cited it as *Wicklund v. Idaho Department of Correction*, **623 F. App'x 338** (9th Cir. 2015).

**PRIMARY.** *Wicklund v. Idaho Dep't of Corr.*, No. **12-35294** (9th Cir. Nov. 23, 2015) (Fisher, Berzon, Watford) — **unpublished memorandum**. CDN PDF `datastore/memoranda/2015/11/23/12-35294.pdf` read. Caption is Idaho Department of **Corrections** (plural). **623 F. App'x 338 does not exist in CourtListener** (`citation:("623 F. App") Wicklund` = 0). Do not use that reporter cite.

**What it actually held.** Affirmed denial of **qualified immunity** to Ken Bennett, Director of Probation and Parole, at summary judgment. Wicklund presented evidence Bennett threatened to jail him for pursuing litigation against the county prosecutor and a polygrapher **outside** court-ordered therapy. Five-element *Rhodes* retaliation test; threat is enough (*Brodheim*); right clearly established by *Pratt* (1995).

**Why it still does not go in the brief.**

1. **9th Cir. R. 36-3.** Not precedent. Putting an unpublished memo in a "clearly established" string is how a cite becomes a sanction under Cisneros Standing Order § E.4.
2. **Footnote 1 is a Smith exhibit.** "Restraints on Wicklund's disruptive behavior during his court-ordered therapy sessions **did not violate his First Amendment rights.**" If they find this memo, they will argue the protected activity here is inside treatment. The answer is the same one UNIFIED already has: the ringleader report / Form 1502 / no-show pipeline is **official reporting into parole**, not a clinical restraint inside a session. Do not hand them the footnote by citing the case.
3. The published carriers are already on the safe list: *Watison*, *Brodheim*, *Pratt*, and **their own** *Arizona Students' Ass'n*.

**Use.** None, unless they cite it first. Then: unpublished; QI denial was for a **state** probation director, not a vendor; fn.1 is limited to in-session disruption.

### 1.4 *Horn* — official cite is now 604 U.S. 593

This branch's first-pass memo and UNIFIED § 13 still say `604 U.S. ___`. **#880** and LII / the U.S. Reports page proof report ***Medical Marijuana, Inc. v. Horn*, 604 U.S. 593 (2025)** (No. 23-365, Apr. 2, 2025). Slip `23-365_6k47.pdf` still prints blanks; the bound volume is 604 U.S. starting at 593.

Holding unchanged from the morning pass: no categorical antecedent-personal-injury bar. The Court **did not** decide whether "business" includes employment, whether Horn suffered a personal injury, or the property question. *Anza* proximate cause is untouched. Stop using the docket number as the cite.

---

## 2. Gateway and distinguisher verifications

### 2.1 *ASARCO* / *Lee* / *Khoja* — the Rule 12 frame #880 named, now existence-checked here

| Authority | Cite | CL | Holding that matters |
|---|---|---|---|
| *ASARCO, LLC v. Union Pac. R.R.* | 765 F.3d 999, **1004** (9th Cir. 2014) | FOUND `/opinion/8441949/` | "Dismissal under Rule 12(b)(6) on the basis of an affirmative defense is proper **only if** the defendant shows some **obvious bar** to securing relief **on the face of the complaint.**" Disputed facts → deny. CDN HTML 404 this pass; pin corroborated by HallApproved / vLex quotations of 765 F.3d at 1004. Pin = **SECONDARY** until the F.3d page is re-opened. |
| *Lee v. City of Los Angeles* | 250 F.3d 668 (9th Cir. **2001**) | FOUND | Judicial notice of another court's records does not notice the **truth** of disputed facts inside them. Year is 2001 (not a 1990s cite). |
| *Khoja v. Orexigen Therapeutics* | 899 F.3d 988 (9th Cir. 2018) | FOUND `/opinion/4525969/` | Incorporation-by-reference / judicial-notice limits. #881 already notes Cisneros cites *Khoja* in her 12(b)(6) boilerplate. |

**Opposition use.** Lead the preclusion section with *ASARCO* 1004 (confirm pin), then the three disputed facts UNIFIED already lists: no judgment; exhaustion vs. merits; Smith not in privity. *Lee* stops them from converting the July 15 tentative / formal-order mismatch into a noticed "fact." *Khoja* is how Cisneros will describe the record.

### 2.2 *Blackwell* — #881's distinguisher holds on a primary read

**PRIMARY.** *Blackwell v. Carrington Mortg. Servs., LLC*, No. **24-cv-06494-BLF** (N.D. Cal. Jan. 22, 2025) (Freeman, J.), ECF 28. Justia / order text read.

The RJN took **eight** exhibits. The two that matter:

- **Exhibit 3** — Order Sustaining Demurrer (Monterey Super. Ct. 17CV004560).
- **Exhibit 4** — **Order of Dismissal With Prejudice** in the same action.

Freeman's "final judgment on the merits" paragraph is built on **both**: the state court "sustained CMS's demurrer … without leave to amend **for failure to state a cause of action and ordered that the State Action be dismissed with prejudice.**" Cite: *Palomar Mobilehome Park Ass'n v. City of San Marcos*, 989 F.2d 362, 364 (9th Cir. 1993) (CL FOUND). Not Cisneros. Not a § 1983 case. Not an exhaustion demurrer.

**Distinguishers, in this order if they cite it:**

1. Matter 5 has **no** Order of Dismissal With Prejudice and **no** Judgment. *Blackwell*'s RJN needed Exhibit 4. They will not have an Exhibit 4.
2. Matter 5's ground was **jurisdictional exhaustion**, which the state court itself called a jurisdictional requirement — *Heath* n.4 / *Perez* / *Costello*. *Blackwell* was failure to state a cause of action.
3. Shannon Smith was **not a party** to Matter 5.

### 2.3 15 C.C.R. § 3574 — dates versus the conduct they will attack

Already pinned in the morning memo (Cornell LII + CDCR adopted-regs). This pass adds the **effective-date sequence** so they cannot call the regulation an anachronism or we cannot overclaim it.

| Event | Date | Source |
|---|---|---|
| Emergency § 3574 | **Oct. 14, 2024** | CDCR NCR 25-01 / OAL emergency file |
| Grace-period revocation (HOPE_000190) | **Feb. 20, 2025** | Cluster-2 lock — **during the emergency** |
| Emergency refiled | **Mar. 24, 2025** | CDCR NCR 25-01 |
| Certificate of Compliance (permanent) | **Apr. 17, 2025** (Cal. Regulatory Notice Register 2025, No. 16) | Cornell LII currentness line |
| Ringleader report | **Aug. 19, 2025** | After permanent |
| Form 1502 | **Nov. 14, 2025** | After permanent |

**Use.** (d) / (e)(2) / (f) are the current paper: supervised persons **may complete** before discharge; the one-year CTM is the **first review**; later retention needs **written good cause** on Form 3043 signed by provider **and** agent. Do **not** cite § 3574 as if it governed 2021–23 conduct. The **statute** — Pen. Code § 3008(d)(2), "as determined by the certified … professional" — has said that since 2012. *Dwyer* (Mar. 20, 2023) found the no-completion policy three years before this complaint. Post-April 2025 conduct (ringleader / 1502) is under the permanent regulation.

### 2.4 *Rawson* "significantly involves itself" — reconfirmed on CDN

*Rawson v. Recovery Innovations, Inc.*, 975 F.3d 742 (9th Cir. 2020) (CL FOUND `/opinion/4783621/`). Cert denied Oct. 4, 2021 (morning pass). The published close-nexus line — the State "significantly involves itself with the private party" — is the bridge UNIFIED already uses. Involuntary-commitment facts still distinguish; do not hide the distinction.

### 2.5 Remaining existence checks from the 33-query sweep

CL `type=o` unless noted. Full query log: `/tmp/shannon-cl-sweep.json` (not copied into the repo).

| Query | Result | Use |
|---|---|---|
| *Valvo*, 67 Cal. App. 3d 887 | FOUND `/opinion/2173877/` | Existence only. Pin 891–92 n.3 still needs the reporter PDF. |
| *Palomar*, 989 F.2d 362 | FOUND | Their *Blackwell* cite. Distinguish as above. |
| *Kirtley v. Rainey*, 326 F.3d 1088 | FOUND | GAL / child-welfare state-action analog — poor fit; do not recruit. |
| *Caviness v. Horizon*, 590 F.3d 806 | FOUND | Charter-school no-state-action. Defense color; *Jensen* / *Rawson* still closer. |
| *Hebbe v. Pliler*, 627 F.3d 338 | FOUND | Pro se liberal construction. Cisneros already quotes *Lopez*. |
| *Lopez v. Smith*, 203 F.3d 1122 | FOUND | Leave-to-amend. Already in her boilerplate. |
| *Exxon Mobil v. Saudi Basic*, 544 U.S. 280 | FOUND | *Rooker-Feldman*. They should not need it; if they run it, it is a judgment-review doctrine and there is no judgment. |
| *Jones v. Blanas*, 393 F.3d 918 | FOUND | Civil detainee — not this plaintiff. |
| *Sandoval v. County of Sonoma*, 912 F.3d 509 | FOUND | Impound / seizure. No load-bearing use. |
| *Moore v. Kayport*, 885 F.2d 531 | FOUND | Rule 9(b) group-pleading. Pair with *Zetz*. |
| `"16 Cal.5th 643"` | **0** (CL reporter field empty) | Found by case name. Cite from the official reporter, not CL. |

---

## 3. Cisneros does decide motions to dismiss

#881 § 4.2–4.4 left QI, private-defendant state action, and a 12(b)(6) preclusion ruling **UNVERIFIED** as to her. This pass does not read her opinion PDFs. It does kill the claim that she does not decide MTDs.

CL RECAP `court_id:cand "Lisa J. Cisneros" "motion to dismiss"` — **182 hits**. Docket-level only. Sample that actually has an **order** on a motion to dismiss (not a stay, not a stipulation):

| Case | No. | Order | Disposition (docket text) |
|---|---|---|---|
| *Frankovich v. Varin* | 3:25-cv-01015 | Apr. 27, 2026, Dkt. 46 | **Denied** MTD **without prejudice** |
| *D.J. v. Walnut Creek Sch. Dist.* | 3:24-cv-02660 | Feb. 6, 2025, Dkt. 58; Apr. 15, 2025, Dkt. 77 | **Granted** (amended complaint due Feb. 20); later order on FAC MTD |
| *Vicious Brands, Inc. v. Face Co.* | 3:24-cv-04996 | Nov. 12, 2024 Dkt. 25; July 25, 2025 Dkt. 60; Feb. 3, 2026 Dkt. 95 | 12(b)(1) **denied**; later 12(b)(6) **granted in part / denied in part** (leave to amend); later SAC / MSJ order |
| *McConnell & Malek v. Proof Mark* | 3:23-cv-00010 | May 25, 2023, Dkt. 49 | **Denied** 12(b)(1); denied remand |
| *Yousefisahi v. Edlow* | 3:25-cv-09728 | May 18, 2026, Dkt. 32 | "ORDER REGARDING" Dkt. 11 MTD — answer / MSJ dates set (read the order before characterizing) |

**What this is worth.** She is not a judge who never reaches Rule 12. She **denies** (*Frankovich*), **grants with leave** (*D.J.*, *Vicious Brands* in part), and mixes. That matches #881's leave-to-amend default from *Gold Club* / *K.J.* — PRIMARY for those two, docket-level for this table.

**What this is not.** It is not a holding on res judicata, private-vendor state action, or QI. Those three remain **unread** as to her. Do not invent a Cisneros preclusion test from docket text. *Udo* OSC (sua sponte, then reassigned) is still the only preclusion trace #881 found.

Opinion-title search `"Cisneros" "Lisa J" (12(b)(6) OR "motion to dismiss")` was **noise** (Medtronic / Texas criminal / Williams habeas). Use RECAP dockets, not opinion search, for her.

---

## 4. Van Dine's RECAP book — private government-adjacent contractors, not SOMP

CL `type=r` `"Blaze Van Dine"` — **14 hits**. Pattern, not a merits analog:

| Case | No. | Client | What it is |
|---|---|---|---|
| *Doe v. Five Keys Schools and Programs* | 3:25-cv-08457 (N.D. Cal.) | Five Keys | Jail / community-school contractor |
| *A.S. v. Point Quest* | 2:23-cv-02029 (E.D. Cal.) | Point Quest | Nonpublic school / behavioral contractor |
| *Prado v. City of Berkeley* | 3:23-cv-04537 (N.D. Cal.) | Insight Housing | Homeless-housing contractor (appearance Mar. 19, 2026) |
| *Stark v. Guiding Hands Sch.* | 2:20-cv-00635 (E.D. Cal.) | Guiding Hands + individuals | Nonpublic school |
| *C.R. v. Elk Grove USD* | 2:20-cv-02296 (E.D. Cal.) | Capitol Elementary / Ira Ross | Nonpublic school |

**Finding.** He defends **private entities that sit next to a public function**. That is the *Merrill* / *Gross* fact pattern he already previewed. **No RECAP hit is a CASOMB / SOMP / Pen. Code § 3008 vendor sued under § 1983.** There is still no located Van Dine brief that won a sex-offender-treatment state-action dismissal.

Do not email counsel about this research. Do not put these captions in the opposition unless they open the door. The use is internal: expect a contractor-is-not-the-state brief, and have *Jensen* / *Rawson* / Form 3043 joint action ready.

---

## 5. Verified zeros (a finding, not a gap)

Same conclusion as #881 § 3.7, now against a 33-query CL sweep plus targeted web searches. "0" means the query returned no on-point opinion, not that the universe is empty.

| Search | Hits that matter | Carry-forward |
|---|---|---|
| `"HOPE Psychotherapy"` opinions | **0** on-point (Hayward OR-query exploded into unrelated *Hayward* criminal cases) | Still first impression as a named vendor |
| `"HOPE Psychotherapy"` RECAP | Matter **6** only (2:26-cv-00195) besides this docket | Disclose Matter 6 |
| Matter 28 RECAP `docket_id:73646240` | Last listed recap docs in this sweep's truncated row are early July; morning pass's fuller pull ended at **Dkt. 14 (Sept. 10)** CIE / Rule 7.1 | **No MTD on the public RECAP docket.** They can still file Monday without it indexing. |
| CASOMB / "California Sex Offender Management Board" | 19 opinions — **all criminal** (*Malbry*, *Molina*, *Forney*, *Williams*, *Rebulloza*, *Garcia*…) | No civil vendor-damages case |
| `"3008(d)(2)"` / "Penal Code section 3008" | Criminal / inapposite (*Gonzales*; *Rebulloza*; a First Circuit EPA case that collided on "3008") | Statute text is still the authority, not a damages holding |
| `"9003" "sex offender" immunit` | **0** | No statutory-immunity opinion to steal or fear |
| `"Sharper Future" 1983` | **0** | |
| `"Pacific Forensic" "sex offender"` | **0** | |
| `"Counseling and Psychotherapy Center" 1983` | 1 (R.I. family case — miss) | |
| `"Merrill" "Mental Health Systems" Atkins OR 1983` | No subsequent S.D. Cal. 3:16-cv-01090 merits opinion | Subsequent history still **UNVERIFIED** (docket-number collision across districts) |

**Vendor-damages catalog is unchanged.** Zero located damages holding against a California CASOMB vendor or its CEO. *Chavez* 2021 **granted** QI. *Gross* dismissed for no state action (admission refusal, public-function only). Do not invent a cousin.

---

## 6. Cite table — this pass only

| Authority | Cite | Tag | Role |
|---|---|---|---|
| *Meinhardt v. City of Sunnyvale* | 16 Cal.5th 643 (2024) | PRIMARY (opinion PDF) | Clock runs from a document titled "judgment." **Corrects #881.** Admin-mandate / appealability only. |
| *Estate of Esche v. Bunuel-Jordana* | Nos. 24-6244 et al. (9th Cir. Sept. 29, 2025) | PRIMARY (CDN published PDF) | **No jurisdiction** over interlocutory good-faith appeal. Reasoning on private-party QI is usable; holding is not a QI denial. |
| *Wicklund v. Idaho Dep't of Corr.* | No. 12-35294 (9th Cir. Nov. 23, 2015) (mem.) | PRIMARY (CDN memo PDF) | QI denied to probation director. **R. 36-3. Drop.** Fn.1 is a Smith exhibit. **623 F. App'x 338 is a bad cite.** |
| *Medical Marijuana, Inc. v. Horn* | **604 U.S. 593** (2025) | PRIMARY slip + LII / U.S. Reports page proof | Official cite. No antecedent-PI bar. Does not decide "business" = employment. |
| *ASARCO* | 765 F.3d 999, 1004 (9th Cir. 2014) | CL FOUND; pin SECONDARY | Affirmative defense at 12(b)(6) only if obvious on the face. |
| *Lee v. City of Los Angeles* | 250 F.3d 668 (9th Cir. 2001) | CL FOUND | Notice the document, not the disputed facts inside it. |
| *Khoja* | 899 F.3d 988 (9th Cir. 2018) | CL FOUND | Her 12(b)(6) record rule. |
| *Blackwell* | 24-cv-06494-BLF (N.D. Cal. Jan. 22, 2025) | PRIMARY (order text) | RJN needed the **dismissal-with-prejudice order**. Freeman, not Cisneros. |
| *Palomar* | 989 F.2d 362, 364 (9th Cir. 1993) | CL FOUND | Their *Blackwell* cite. |
| 15 C.C.R. § 3574 effective dates | emergency 10/14/24; permanent 4/17/25 | PRIMARY (CDCR / Register) | Grace during emergency; ringleader / 1502 after permanent. |
| *Frankovich* Dkt. 46 | 3:25-cv-01015 (Apr. 27, 2026) | RECAP docket text | She **denies** MTDs. Opinion unread. |

---

## 7. Guardrails added by this pass

Carry the morning-pass list. Additions in **bold**.

- **Do not brief *Meinhardt* as a deeming-an-order-is-a-judgment case.** That is the reversed Court of Appeal rule.
- **Do not brief *Esche* as a QI-threshold holding.** Safe-cite MISCHARACTERIZED stands. Holding = no interlocutory jurisdiction over a good-faith defense.
- **Do not cite *Wicklund*.** Unpublished; bad F. App'x; fn.1 helps Smith.
- **Cite *Horn* as 604 U.S. 593 (2025).** Still do not brief it as "lost wages are a RICO injury."
- **If they cite *Blackwell*, lead with Exhibit 4.** Matter 5 has no dismissal-with-prejudice order.
- **Do not cite § 3574 for pre-October 2024 conduct.** Use the statute and *Dwyer*.
- Do not treat docket-level Cisneros MTD orders as holdings.
- Do not email Van Dine about the contractor-docket research.

---

## 8. Still open after both September 19 passes

1. Dept. 10A — § 581d judgment / notice of appeal. Re-pull the Stockton register the morning the opposition is drafted.
2. *Valvo* / *Beazell* / *Sartor* / *Lippert* / *Patsy* / *ASARCO* reporter-page PDFs. Existence is not the pin.
3. *Merrill* subsequent history after the Sept. 13, 2016 60-day jurisdictional-discovery order.
4. Authenticated CL sweep (`sweep-matter28.mjs`) — token still unset.
5. Cisneros opinion **text** in *Frankovich*, *D.J.*, *Vicious Brands* — docket disposition only.
6. Whether an MTD is on file the morning of Sept. 21. RECAP as of this compile still ends at Dkt. 14.
7. Housekeeping from the morning memo that is not research: disclose Matter 6; fix Bane `$25,000` in `28/damages.json`; Rule 9(b)-proof Count IV; wage-loss allocation with Matter 26.

Nothing here changes the September 21 answer, the October 15 CMC statement, or the October 22 CMC. No PACER was accessed. Nothing was filed.
