# Matter 28 — verification pass and new finds (Sep. 19, 2026, second pass)
## *Newanforbi v. Shannon Smith, LCSW, CEO, et al.*, N.D. Cal. No. 3:26-cv-07504-LJC

**Compiled 2026-09-19.** Doctrinal research memorandum; not legal advice; requester is pro se. Nothing filed or served. No PACER accessed.

Three Shannon MTD-prep drafts are open at once — **#879**, **#880**, **#881** — plus the Sep. 12 spine and the restored Sep. 18 pair. That is the September 12 four-way all over again. This file does what UNIFIED did then: it tests the conflicts and picks.

**Read this for the conflicts and the new regulatory finds. Read UNIFIED for the preclusion spine.**

---

## 0. CourtListener is not reachable from this session

The `citation-verify` skill lists CourtListener `/api/rest/v4/search/` and CAP `static.case.law` as OK unauthenticated. **That is not true in this container.** Both return a proxy `403 connect_rejected` (organization egress policy), and `COURTLISTENER_TOKEN` is unset. `WebFetch` is blocked for every external host tried, including `courtlistener.com`, `law.justia.com`, `caselaw.findlaw.com`, `cdn.ca9.uscourts.gov`, `www.supremecourt.gov`, `www.govinfo.gov`, `openjurist.org`, `law.cornell.edu`, and `leginfo.legislature.ca.gov`. The proxy README says to report blocked hosts rather than route around them.

**So: no CourtListener pulls happened in this pass, and none can.** Everything below was confirmed through web-search result summaries — real corroboration, weaker than a reporter read, and **not** a substitute for the funnel. Steps 2–4 of the pipeline (`citations:lookup`, overlay, `citations:verify`) must run on the laptop where the token and egress exist.

What did run: `citations:check` — **passes**, 28 debt-tracked hits, no new plaintiff-filing fabrications. The P0 queue is 8 items and **none of them is Matter 28** (they are M25, M26, M32, M33). Matter 28's exposure is characterization, not existence.

---

## 1. Conflicts between the three open PRs — resolved

### 1.1 *Page v. Torrey* — #881 is right, #879 is wrong. Do not brief #879's version.

| Draft | What it says |
|---|---|
| **#879** | *Page v. Torrey*, 201 F.3d 1136, 1139–40, holds PLRA "prisoner" requires current detention; a person "ceased being a 'prisoner' at the time he was released **on parole**." Listed as a lead parolee authority. |
| **#881** | *Page* "does NOT answer the parolee question" — it holds a **civil detainee** (SVP commitment) is not a prisoner. Use it "only as supporting precedent for narrow construction." |

**#881 is correct.** *Page v. Torrey* is a **Sexually Violent Predator Act civil-commitment** case. Page had been a prisoner while serving his sentence, ceased to be one when released from CDCR custody, and his *current* detention was a civil commitment for non-punitive purposes. The holding is that a civilly committed SVP is not a PLRA "prisoner." The parole language in #879 is from the opinion's discussion, not its holding.

**Why this matters more than a pin correction.** Matter 28's plaintiff is a **parolee at liberty**, not a civil detainee. If the opposition leads the PLRA paragraph with *Page*, Van Dine answers that *Page* is an SVP-commitment case and the analogy runs the wrong way — a detained civil committee is a worse posture than a parolee, not a better one. Lead instead with:

- ***Talamantes v. Leyva*, 575 F.3d 1021, 1024 (9th Cir. 2009)** — status measured at the time of filing; a person not incarcerated or detained then is not a § 1997e(h) prisoner. **Binding.**
- ***Kerr v. Puckett*, 138 F.3d 321, 322 (7th Cir. 1998)** — "a convict out on parole is not a 'person incarcerated or detained in any facility.'" **Persuasive, but directly on the facts.**
- § 1997e(h) text itself, which both drafts quote consistently and correctly.

Cite *Page* third, for narrow construction of "prisoner," and say what it is. Do not let it carry the paragraph.

### 1.2 *Meinhardt* — the risk appears inverted. On the available evidence it helps.

**#881 flags** *Meinhardt v. City of Sunnyvale* (2024) 16 Cal.5th 643, 654–55 as a defense weapon: the Cal. Supreme Court "upheld deeming an order sustaining a demurrer WOLA to be a final judgment 'when the ruling is sufficiently final,'" and warns the defense may use it to argue the July 15 order *is* a judgment.

Every source located describes the opposite disposition. *Meinhardt* adopted a **bright-line rule** that the time to appeal runs **from entry of judgment or service of notice of entry of judgment — not from the filing of an order or other ruling.** The Court of Appeal had dismissed Meinhardt's appeal as untimely on precisely the "sufficiently final order" theory, and the Supreme Court **rejected that approach** in favor of requiring a formal judgment. Sources also report the opinion observing that many orders are not statutorily appealable and an appeal "must therefore be taken from a 'judgment,'" **expressly including orders sustaining demurrers without leave to amend.**

If that is the holding, *Meinhardt* is not a deeming case that rescues Van Dine. It is a 2024 California Supreme Court decision **reinforcing the order/judgment distinction** that UNIFIED § 5.1 and *Berri* / *Valvo* / CCP § 581d already rest on — and it is far more recent than any of them.

**Do not flip this into an affirmative argument yet.** Read the opinion before citing it either way; the "sufficiently final" language #881 quotes exists somewhere in the opinion and the context matters. But **the risk ranking changes now**: *Meinhardt* moves off the "watch — they may spring it" list and onto the "read it, it may be ours" list. If it holds up, it belongs in the opposition's § II.A.1 as the current statement of California law, and #881's tactical instruction to spend a defensive paragraph on it should be rewritten.

### 1.3 *Medical Marijuana, Inc. v. Horn* — the official cite exists. Stop using "604 U.S. ___".

Both #879 and #881 cite it as `604 U.S. ___ (2025)` and #879 expressly says "until the U.S. Reports page lands. Do not invent a volume/page."

**The page has landed.** The official cite is **604 U.S. 593 (2025)**; the Supreme Court's own preliminary print is "Volume 604 U.S. Part 2, Pages 593–649." My Sep. 19 supplement already uses it. Update both drafts.

On substance the three drafts agree and are correct: 5–4, Barrett, J.; § 1964(c) has no categorical antecedent-personal-injury bar; the Court expressly declined to decide whether "business" encompasses employment; the proximate-cause limitation survives, so *Anza* and *Canyon County* are undisturbed. **Do not brief *Horn* as holding that lost CDL wages are a RICO injury.** #879's framing of this is the best of the three — keep its wording.

### 1.4 *Estate of Esche* and *Wicklund* — unchanged from the Sep. 19 supplement

*Esche* stays **reasoning only** per `MATTER_28_SAFE_CITE_LIST.md` (MISCHARACTERIZED on four pages; "holding is jurisdictional, not QI threshold"). The Sep. 18 deep-research memo's use of it as the QI Step 1 anchor is still the outlier. Unverifiable here — the Ninth Circuit CDN and every mirror are blocked.

*Wicklund*, 623 F. App'x 338, stays **UNVERIFIED**. Nothing this pass changed it. Unpublished, non-precedential under 9th Cir. R. 36-3, and the described QI disposition is still unconfirmed. Keep it out of the clearly-established string.

### 1.5 Agreement worth recording

Where the drafts agree, they agree correctly and the point is closed: § 3008(d)(2) verbatim text; § 1997e(h) text; *Schreiber* is 1986 and helps on leave to amend; *Chavez* 2021 granted QI; *Gross v. Samudio* is unpublished Tenth Circuit pleading-insufficiency, not a categorical rule; *Rawson* cert denied Oct. 4, 2021; no located damages holding against a CASOMB vendor or its CEO.

**Independent corroboration for #881's Cisneros work:** her Rule 12 standard reportedly cites ***Khoja***. That is the same doctrine my Sep. 19 supplement builds Argument I's evidentiary gateway on, arrived at separately. Two drafts converging on *Khoja* from opposite directions is the strongest signal in this whole corpus — **the judicial-notice fight is the fight**, and she already has the framework in her own boilerplate.

---

## 2. The best sentence in the regulation — and nobody has quoted it yet

15 C.C.R. § 3574 is now confirmed further than any prior pass. Three pieces, in ascending order of value:

**(a) Completion before discharge is expressly contemplated.**

> "Supervised persons **may complete** a sex offender management program **before discharge from parole**, as contemplated by PC section 3008(d)."

#879 has this. It is good, and it directly contradicts a blanket "finish parole first" rule.

**(b) The CTM is an individualized review by enumerated factors.** A Containment Team Meeting reviews

> "the supervised person's treatment progress, dynamic risk factors, polygraph results, community reintegration, response to parole supervision, supervision category, and relevant individual case factors **to evaluate the supervised person's readiness for sex offender management program completion**."

That is a list of **individual** criteria. A policy that reaches the same answer for every parolee regardless of those factors does not apply them. This is the *Dwyer* finding restated as a current CDCR regulation — and it does not need *Dwyer* to carry it.

**(c) The sentence to build the state-action and Monell sections around.**

> "The review of the sex offender management program **completion is independent of** whether the supervised person should be **discharged from parole** and independent of their electronic monitoring requirements."

**Read that against the pleaded policy.** The complaint alleges HOPE maintained a blanket rule requiring completion of the full parole term before graduating from treatment — that is, it **tied treatment completion to parole discharge**. The governing regulation says in terms that the two are **independent**. The alleged policy is not a permissible exercise of clinical discretion under a discretionary statute; it is the precise linkage the regulation forbids.

No draft in the corpus quotes this sentence. It should be in the opposition's state-action section, its Monell moving-force paragraph, and its due-process section. It is the shortest path from "HOPE had a policy" to "the policy contradicted the state scheme HOPE was required to operate inside."

**The date caveat from my Sep. 19 supplement still governs.** § 3574 was adopted by NCR 25-01 (dated January 3, 2025) and the LII text is current through an **April 17, 2025 Certificate of Compliance** (per #879). Cluster-2 locked facts put the grace-period revocation at **February 20, 2025** — likely before the operative date. Pin the operative date from the OAL filing and map it to each pleaded act. For conduct predating it, § 3008(d)(2) has said "as determined by the certified sex offender management professional" since 2012, and *Dwyer* (March 20, 2023) found the categorical practice three years before this complaint. **Do not allege § 3574 governed a CTM that predates it.**

---

## 3. A risk the corpus is under-weighting: general vs. special demurrer

#881 leans on a 2012 BAP memorandum for the proposition that a demurrer sustained WOLA is preclusive "as long as the order was based on the merits … **and not on some formal defect**," citing *Goddard* and *Pollock v. University of Southern California*, 112 Cal.App.4th 1416 (2003).

The California rule is narrower than that quotation reads standing alone:

> A judgment on a **special** demurrer for technical or formal defects is **not** on the merits and does not bar a new action. A judgment entered after sustaining a **general** demurrer **is** a judgment on the merits, and to the extent it adjudicates that the facts alleged do not establish a cause of action, it bars a second action on the same facts.

Van Dine's demurrer was almost certainly a **general** demurrer. So the "formal defect" line does **not** do the work by itself, and an opposition that leans on it invites the answer that this was a general demurrer and *Blackwell* / *Palomar* control.

**The argument that survives that answer** is the one UNIFIED § 5.2 already makes, and it must be framed as the exception rather than the rule:

1. The **actual ground decided** was failure to exhaust, which Judge Abdallah called a **"jurisdictional requirement"** unmet "prior to the filing of" the FAC. Under CCP § 430.10, lack of subject-matter jurisdiction is **subdivision (a)** — a separate ground from failure to state a cause of action, which is **subdivision (e)**. The defense-drafted order recites (e). **The court's own words sound in (a).** That mismatch is worth stating explicitly; no draft in the corpus has made it.
2. *Goddard* itself concedes that even a general-demurrer judgment "may not be on the merits" where the defect is technical. Exhaustion as an unmet precondition is that class of defect — *Perez*, *Heath* n.4, *Costello*, Restatement § 20(2).
3. *Keidatz*: the ground is temporally capped ("prior to the filing of his FAC") and is not "equally applicable" to a federal complaint requiring no state administrative exhaustion.

**And, as the Sep. 19 supplement argues, none of it is reachable at Rule 12 anyway** if the actual basis of the state decision is disputed on the face of the record — *ASARCO*, 765 F.3d at 1004; *Lee*, 250 F.3d 668; *Khoja*, 899 F.3d 988.

*Blackwell v. Carrington Mortgage Servs.*, No. 24-cv-06494-BLF (N.D. Cal. Jan. 22, 2025) is confirmed: Freeman, J., dismissed pro se plaintiffs with prejudice on res judicata, resting on "a **judgment entered after** sustaining of a general demurrer," with a separate order of dismissal with prejudice in the state case. **#881's distinguisher (a) is exactly right and is the whole ballgame** — *Blackwell* is judgment-dependent, and Matter 5 has no judgment.

---

## 4. New substantive finds

### 4.1 HOPE's own website corroborates two pleaded facts

Publicly stated by the company, on the record, before this suit:

- **"All 16 locations are staffed with certified professionals specializing in psychological evaluations and risk assessments."** The complaint's "16 California locations" allegation matches HOPE's own count.
- HOPE is "one of the few providers **fully certified by both the state of California and the California Sex Offender Management Board (CASOMB)**," and is a "CASOMB-certified" provider of "sex-offence specific treatment."
- **Shannon Smith, LCSW is identified as Founder, Director and Chief Executive Officer**, who "leads the organization's mission."

**Use.** This is admission-quality material on the two elements the defense will contest hardest: (1) that HOPE is a state-certified participant in California's SOMP scheme, not an ordinary private therapy practice; and (2) that Smith is the corporate policymaker for Monell / individual-capacity purposes. A defendant's own public description of itself is ordinary judicial-notice or incorporation material and costs nothing to lodge.

**Two cautions.** A website is not a pleading — quote it, date the capture, and do not treat marketing copy as a stipulation. And "CASOMB-certified" on a website is the company's characterization; the CASOMB certification itself is the document worth having.

### 4.2 *Richardson*'s own language is the *Filarsky* distinguisher

From the opinion: the Court emphasized that **"a private firm [was] systematically organized to manage the prison,"** and found "nothing special enough about the job or about its **organizational structure**" to warrant immunity.

"Systematically organized" is the phrase. A sixteen-location, CASOMB-certified, multi-county corporation with a founder-CEO who sets clinical and compliance policy is the *Richardson* firm, not the *Filarsky* individual retained "on a temporary or occasional basis." Brief the QI threshold in *Richardson*'s words and the distinction argues itself — **without** needing *Estate of Esche*, which the safe-cite list has locked down.

### 4.3 Verified absence, reconfirmed

No 2024–2026 Ninth Circuit decision applying *Richardson* / *Filarsky* QI to a private sex-offender-treatment contractor surfaced this pass either. That matches #881's finding. It is a finding, not a gap: the QI threshold for this defendant class is open in this circuit, which is why the threshold argument is worth making and why *Chavez* 2021 (state action **assumed**, QI **granted**) is the trap to avoid rather than the rule to concede.

### 4.4 *Ariz. Students' Ass'n* — their own retaliation cite reversed a dismissal

Confirmed: *Arizona Students' Ass'n v. Arizona Board of Regents*, 824 F.3d 858 (9th Cir. June 1, 2016). The Ninth Circuit **ruled for the student association**, holding its claim for prospective injunctive and declaratory relief was not barred by sovereign immunity as against individual Board members, and that the district court **abused its discretion in failing to grant leave to amend** to conform to *Ex parte Young*.

Van Dine previewed this as support for dismissal. It reversed one, and it reversed a denial of leave to amend. Both halves help. Pin 867 for the three-element retaliation test remains **SECONDARY** across all drafts — corroborated by citing orders, not checked against the reporter.

---

## 5. Status of every authority touched this pass

| Authority | This pass | Status |
|---|---|---|
| *Page v. Torrey*, 201 F.3d 1136 (9th Cir. 2000) | SVP civil-commitment holding; **not** a parolee case | **#879 CORRECTED** |
| *Talamantes v. Leyva*, 575 F.3d 1021, 1024 (9th Cir. 2009) | Prisoner status measured at filing | Confirmed — lead with this |
| *Kerr v. Puckett*, 138 F.3d 321, 322 (7th Cir. 1998) | Parolee is not detained in a facility | Confirmed — persuasive |
| *Meinhardt v. City of Sunnyvale*, 16 Cal.5th 643 (2024) | Bright line: appeal runs from **judgment**, not order | **#881 characterization appears INVERTED — read the opinion** |
| *Medical Marijuana, Inc. v. Horn* | **604 U.S. 593 (2025)** | Official cite confirmed — supersedes "604 U.S. ___" |
| *Blackwell v. Carrington Mortg. Servs.*, No. 24-cv-06494-BLF (N.D. Cal. Jan. 22, 2025) | Res judicata, with prejudice; **judgment-dependent** | Confirmed — #881's distinguisher (a) holds |
| *Pollock v. USC*, 112 Cal.App.4th 1416 (2003) | General vs. special demurrer distinction | Confirmed — **narrower than the BAP quote reads** |
| *Palomar Mobilehome Park Ass'n v. City of San Marcos*, 989 F.2d 362 (9th Cir. 1993) | The 9th Cir. case *Blackwell* rests on | Exists; **read before the opposition** |
| 15 C.C.R. § 3574 | Completion "independent of" parole discharge; CTM factor list | **Confirmed — new, and the best sentence located** |
| Pen. Code § 3008(d)(2) | Certified professional determines the period | Confirmed (all three drafts agree) |
| CCP § 430.10(a) vs (e) | Jurisdiction is (a); failure to state is (e) | Confirmed — **new argument** |
| *Richardson v. McKnight*, 521 U.S. 399 (1997) | "systematically organized" private firm | Confirmed — the *Filarsky* distinguisher |
| *Ariz. Students' Ass'n*, 824 F.3d 858 (9th Cir. 2016) | Reversed dismissal + denial of leave to amend | Confirmed; pin 867 still SECONDARY |
| HOPE website: 16 locations, CASOMB-certified, Smith founder/CEO | Party's own public statements | Confirmed — capture and date it |
| *Estate of Esche* (9th Cir. 2025) | Safe-cite list governs: reasoning only | **Still CONFLICTED, unverifiable here** |
| *Wicklund*, 623 F. App'x 338 | Described QI disposition unconfirmed | **Still UNVERIFIED — do not brief** |

Everything in this table is search-corroborated, **not** reporter-verified. Nothing here is cleared for filing until the funnel runs with egress and a token.

---

## 6. What to do with three open PRs

They do not conflict structurally — #879 is an inventory-plus-closed-holes memo, #881 is a fresh-authority-plus-judge memo with an opposition skeleton, #880 is the restoration plus the Rule 12 gateway. Merged together they are close to complete. But **three files all called "the Sept. 19 MTD prep" is how the Sep. 18 deletion happened in the first place**, and each one edits `legal-intel/matters/28.md` and the UNIFIED pointer block differently.

Recommended order, and why:

1. **#880 first** — it is the only one that restores deleted files. Merging the others first risks another stale-base clobber of the same two files.
2. **#879 next** — largest set of independently closed queue items.
3. **#881 last** — its Cisneros dossier and opposition skeleton are additive, and its two corrections (*Page*, *Meinhardt*) can be applied on merge.
4. Then fold all four Sept. 18–19 files into the UNIFIED spine the way #763–#767 were folded, and delete nothing without saying so in the commit message.

**Before any merge, check the diffstat for deletions in `internal/docs/legal-intel/` that the PR body does not describe.** That is the check that would have caught #876.

---

## 7. Queue

**Cannot be done here — laptop only**

1. `npm run court:sync` / `citations:lookup:matter -- --matter 28`, then the overlay and `citations:verify`. Everything in § 5 is search-corroborated only.
2. Read the opinions that decide something: ***Meinhardt*** (does it help or hurt?), ***Estate of Esche*** (holding or reasoning?), ***Wicklund*** (what was the QI disposition?), *Palomar*, *Valvo* at 891–92 n.3.
3. Pin § 3574's **operative date** from the OAL filing and map it against every pleaded act.

**Before the opposition**

4. Capture and date HOPE's website pages (locations count, CASOMB language, Smith bio) before they change. Obtain the CASOMB certification itself.
5. Re-pull the San Joaquin register. Still the one defense move that changes the preclusion analysis.
6. Confirm the state demurrer's actual subdivision — (a) or (e) — from the demurrer papers themselves, not the order.
7. Disclose Matter 6. Open since September 12 across all drafts.
8. Fix the Bane "$25,000 per violation" figure in the live data before it reaches an opposition or the CMC statement.

**Monday**

9. Docket check. RECAP ended at Dkt. 14 (Sept. 10) as of #879's Sept. 19 pull; a Monday filing will not be indexed immediately.
10. If it is an answer and not a motion, all of this goes to the CMC statement and the discovery plan instead.

---

Nothing here changes the September 21 answer deadline, the October 15 CMC statement, or the October 22 CMC. No PACER was accessed. Nothing was filed or served.
