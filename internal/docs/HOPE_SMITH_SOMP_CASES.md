# HOPE / Shannon Smith / SOMP-vendor damages cases

Research memo. Compiled September 12, 2026.

Scope: every located case that applies (1) *West v. Atkins* state-actor doctrine to a
California sex-offender management program (SOMP) / CASOMB-certified treatment
vendor; (2) qualified immunity to a private CDCR or SOMP contractor, especially
a standing vendor CEO; (3) *Monell* to a private treatment firm; (4) the Bane
Act or RICO to a SOMP vendor; plus the *Dwyer* / ACSOL satellites and the
portfolio matters that name HOPE or Shannon Smith.

**This is not a cite-from-memory document.** Each item is tagged
`PRIMARY` / `SECONDARY` / `UNVERIFIED` against the source actually read.

---

## How to use this memo

- A case is a **merits decision on the Shannon theories** only if a court
  ruled on state-actor status, QI for a private SOMP contractor, *Monell*
  liability of a treatment vendor, Bane Act liability of a treatment vendor,
  or RICO liability of a treatment vendor.
- *In re Dwyer* is a habeas order about **CDCR / DAPO policy**. It is not a
  damages judgment and HOPE was not a party.
- *ACSOL v. Macomber* (L.A. Super. Ct. No. **23STCP02378**) is a demurrer
  ruling against the Secretary, later settled. It is not a merits holding
  and it is not the Sacramento 2025 ACSOL case.
- *Chavez v. Robinson* assumed a private Oregon therapist was a state actor
  and then granted QI. Do not cite it as a holding that a SOMP therapist
  *is* a state actor, and do not cite the 2021 opinion as a QI denial.
- No located published or unpublished order holds a California
  CASOMB-certified SOMP vendor or its CEO liable in damages.

---

## 1. What Matter 28 actually asks a court to decide

Caption: *Newanforbi v. Shannon Smith, LCSW, CEO, et al.*, N.D. Cal.
No. **3:26-cv-07504-LJC** (Judge Lisa J. Cisneros). Filed July 20, 2026
(complaint docketed July 21). CourtListener docket id **73646240**.

Defendants: HOPE Psychotherapy, Inc. (d/b/a HOPE Program), a
CASOMB-certified LCSW professional corporation (Hayward; 16 California
locations; Cal. Sec'y of State no. 3112323, filed Oct. 16, 2009); and
Shannon Smith, LCSW, founder and CEO, individually.

Live theories: § 1983 *Monell* (HOPE); § 1983 individual capacity (Smith);
Bane Act; fraud / negligent misrepresentation; RICO §§ 1962(c)–(d).

Posture as of September 12, 2026: served August 31, 2026 (Blaze Van Dine
accepted for both). Dkt. 13 POS filed September 3. Rule 12 / answer due
**September 21**. Martinez memorialized September 11 that the defense
theories are res judicata and insufficiency; meet-and-confer exhausted.
Dkt. 11 (August 26) declined § 1915 screening, including preclusion, after
the filing fee was paid. **Not a ruling on any live claim.**

Predecessor vehicles: Matter 5 (state tort / Bane against HOPE and Palacios)
died on **exhaustion**, not merits, July 15, 2026. Matter 6 (federal § 1983
against HOPE and Macomber) was dismissed without prejudice June 1, 2026.
Smith was not a party in Matter 5. Matter 6 is still an undisclosed overlap
on the Matter 28 docket.

---

## 2. Method and coverage

Searched (September 12, 2026):

- CourtListener Search API (unauthenticated): `type=o/r/d` for
  `"HOPE Psychotherapy"`, `"HOPE Program" Hayward`, `"Shannon Smith" LCSW`,
  `"sex offender management" 1983`, `"sex offender treatment" "state actor"`,
  `CASOMB 1983`, `"In re Dwyer"`, `"Alliance for Constitutional Sex Offense"
  Macomber`, Newanforbi + Hope/Smith/Palacios, and named-vendor strings
  (Sharper Future, Pacific Forensic, Counseling & Psychotherapy Center).
  `COURTLISTENER_TOKEN` was **unset**. Tokened `/dockets/{id}/` and
  citation-lookup were not available.
- Ninth Circuit PDFs: *Chavez v. Robinson*, 817 F.3d 1162 (2016) and
  12 F.4th 978 (2021), extracted from the court CDN copies.
- *ACSOL v. Macomber* December 13, 2023 tentative (Beckloff, J.) via
  rulings.law reprint.
- ACSOL contemporaneous write-ups of *Dwyer* (March 24, 2023) and the
  Macomber demurrer / 2024 settlement.
- Portfolio: Matters 5, 6, 19, 28, 34; `citation_audit.json`;
  `MATTER_28_SAFE_CITE_LIST.md`; `ADVERSARIAL_PLEADING_REVIEW.md`.
- Web 2020–2026: HOPE / Shannon Smith lawsuit; SOMP vendor § 1983;
  RICO / Bane + treatment vendor; private-contractor QI.

**Opinion-corpus finding:** CourtListener `type=o` `"HOPE Psychotherapy"`
= **0**. `"Shannon Smith" LCSW` opinions = **0**. The only federal civil
docket that names HOPE Psychotherapy as a defendant is Matter 6
(`2:26-cv-00195`, CL 72184552). Matter 28 is indexed as
*Ngehsi Newanforbi v. Smith*, `3:26-cv-07504`.

**Not found as named-case alerts:** practitioner pieces (Littler, Seyfarth,
Ogletree, Fisher Phillips) that name a California SOMP-vendor damages
judgment. Absence is a search result, not proof none exist behind a paywall.

---

## 3. Controlling doctrine (not SOMP-vendor holdings)

These cases supply the law Matter 28 will argue. None of them decided a
California CASOMB vendor or Shannon Smith.

### 3.1 *West v. Atkins*, 487 U.S. 42 (1988)

| Field | Value |
|---|---|
| Court | U.S. Supreme Court |
| Publication | **Published** |
| Holding | A physician under contract with a state prison to provide inmate medical care acts under color of state law. The public function is medical care the State is obligated to provide. |
| Source | `PRIMARY` (standard U.S. Reports holding; reconfirmed in the Matter 28 citation funnel as FOUND) |

**What this is not.** It is not a parole-treatment case. It is not a holding
that a community SOMP vendor is a state actor. The fit to HOPE is an
application: CDCR vendor contract + mandatory parole condition + Form 3043
reporting pipeline. The Matter 6 adversarial review correctly called that
fit weaker than a prison doctor, because CDCR still conducts multi-tier
discharge review.

### 3.2 *Richardson v. McKnight*, 521 U.S. 399 (1997)

Published. Private prison guards employed by a firm that systematically
runs an institution for profit, with limited direct government supervision,
do **not** get qualified immunity. Self-consciously narrow. `PRIMARY` as
to the holding.

### 3.3 *Filarsky v. Delia*, 566 U.S. 377 (2012)

Published. A private attorney briefly retained by a city to help conduct
an official investigation **does** get QI. Distinguishes *Richardson*'s
standing for-profit firm. This is the defense cite for Smith. The
portfolio's distinguish line is the right one: Smith is a standing
statewide vendor CEO, not a one-off hire. `PRIMARY` as to the holding.

### 3.4 Ninth Circuit private-contractor QI (medical / firm)

| Case | Cite | Who | QI? | Published? | Source |
|---|---|---|---|---|---|
| *Jensen v. Lane County* | 222 F.3d 570 (9th Cir. 2000) | Private psychiatrist asked to commit persons suspected of mental illness | No | Yes | `PRIMARY` (safe-cite list + cert-petition description matching the opinion) |
| *Halvorsen v. Baird* | **146 F.3d 680** (9th Cir. 1998) | Private nonprofit detox firm (Central City Concern) | No — *Richardson* firm | Yes | `PRIMARY` (opinion text / reprint). Do not cite as 366 F.3d 619 |
| *Ace Beverage Co. v. Lockheed Info. Mgmt. Servs.* | **144 F.3d 1218** (9th Cir. 1998) | Private parking-ticket processor | No — *Richardson* firm | Yes | `PRIMARY` (opinion text / reprint). Do not cite as 144 F.3d 1240 |

These are the closest published circuit cases to "a private firm doing a
standing government job does not get QI." None of them is a SOMP vendor.
None of them is a CEO of a 16-site CASOMB program.

*Clement v. City of Glendale*, 518 F.3d 1090 (9th Cir. 2008), and
*Danielson v. Inslee*, 945 F.3d 1096 (9th Cir. 2019), appear on the
Matter 28 safe-cite list as Theory A support. They were not re-opened
in this run. Treat as `SECONDARY` until the opinion text is re-read
for this file.

---

## 4. The one published case that actually sued a private sex-offender therapist

### 4.1 *Chavez v. Robinson*, 817 F.3d 1162 (9th Cir. 2016)

| Field | Value |
|---|---|
| Caption | *Daniel Mike Chavez v. David R. Robinson; Lisa Moore* |
| Court | 9th Cir. (from D. Or. 1:11-cv-03025) |
| Docket | No. 14-35384 |
| Panel | McKeown, Tallman, Gleason (D. Alaska, sitting by designation) |
| Publication | **Published** |
| Source | `PRIMARY` (2016 CDN PDF extracted) |

Facts the court recited: Oregon post-prison supervision required Chavez to
complete a sex-offender treatment program. The Department "contracted with
Robinson, a therapist in private practice." Moore was the probation
officer. Robinson required admission of guilt; later terminated treatment
after Chavez sued.

Exact disposition:

> "We hold that a district court may dismiss a claim on qualified immunity
> grounds under 28 U.S.C. § 1915(e)(2)(B)(iii) … [but] pre-service
> dismissal on the basis of qualified immunity is appropriate only in
> limited circumstances."

And:

> "Further amendment or proceedings would be necessary to clarify, for
> example, whether Robinson was acting under color of state law in
> operating the sex offender treatment program and whether Robinson or
> Moore violated any clearly established law."

**What this is.** A pleading-stage reversal of a sua sponte QI dismissal.
The state-actor question was left **open**.

**What this is not.** A holding that a private SOMP therapist is a state
actor. Not California. Not a vendor CEO. Not *Monell*. Not a
retention-policy case.

### 4.2 *Chavez v. Robinson*, 12 F.4th 978 (9th Cir. 2021)

| Field | Value |
|---|---|
| Docket | No. 18-36083 |
| Panel | Ikuta, J. (majority); Berzon, J., concurring in part and dissenting in part; Lemelle, D.J., sitting by designation |
| Publication | **Published** |
| Source | `PRIMARY` (2021 CDN PDF extracted; 68 pages) |

After remand, the district court granted a motion to dismiss. The 2021
panel **affirmed**.

The district court "assum[ed] without deciding that Robinson was a state
actor" and held both defendants entitled to QI on the Fifth, Sixth, and
First Amendment claims. The majority agreed: no Fifth Amendment violation
until a coerced statement is used in a criminal case; QI on the Sixth
Amendment right-to-counsel-at-treatment theory; QI on the First Amendment
retaliation theory. Berzon would have let the First Amendment claim past
QI.

Exact majority close:

> "we affirm the district court's dismissal of this claim. We also affirm
> the dismissal of Chavez's [remaining] claims."

**Do not cite *Chavez* 2021 as a QI denial.** The Matter 28 safe-cite list
already flags this. The 2021 opinion is a published **grant** of QI to a
private sex-offender therapist, after assuming state action.

**Use.** Closest published analog to suing a contracted sex-offender
therapist. Useful to show the Ninth Circuit will *entertain* the state-actor
question and will then decide QI issue-by-issue. Dangerous if offered as
proof that Smith cannot get QI, or that HOPE is a state actor as a matter
of law.

---

## 5. California orders that condemned the *policy* — not HOPE, and not damages

### 5.1 *In re Frederick Dwyer*

| Field | Value |
|---|---|
| Caption | *In re Frederick Dwyer* |
| Court | San Mateo Super. Ct. |
| Docket | **SC-080355A / HC-3020** |
| Judge | Hon. Elizabeth M. Hill (confirmed against the attached order in the Matter 19 habeas exhibit). Matter 5's RJN once named "Jakubowski / Novak" — that caption is wrong; do not repeat it |
| Date | Evidentiary hearing February 9, 2023; order **March 20, 2023** |
| Publication | **Unpublished** trial-court habeas order. Not in CourtListener's opinion corpus. Dozens of unrelated *In re Dwyer* clusters (N.J., N.Y., Pa., bankruptcy) will contaminate a naive search |
| Source | `PRIMARY` as to existence, caption, date, and the CDCR-policy findings **as quoted** in the December 13, 2023 *ACSOL v. Macomber* tentative (Beckloff, J.), which judicially noticed the *Dwyer* order as Exhibit A. The *Dwyer* PDF itself was not re-opened in this run; quote-check the Matter 19 Exhibit B / Matter 5 RJN Exhibit A before filing a quotation. `SECONDARY` as to ACSOL's March 24, 2023 news write-up |

What the Beckloff tentative recites from the *Dwyer* order and transcript
(`PRIMARY` as a quotation of that order):

> "The Court held an evidentiary hearing at which it found that the sole
> basis for retaining the Registrant in the management program was CDCR’s
> policy of requiring all Registrants to participate in the program for
> the duration of parole, regardless of their individual treatment needs.
> (Exh. A, at p. 10.)"

CDCR witnesses:

> "THE COURT: Is it essentially the policy of the Department of
> Corrections that completion of the program is not possible before the
> discharge from parole program … ? THE [CDCR] WITNESS: Yes."

And from a former East Bay region supervisor:

> "it is the policy of the California Department of Corrections and
> Rehabilitation and the Division of Adult Parole Operations that a sex
> offender management program as defined in Penal Code § 3008 cannot be
> completed short of discharge from parole."

Relief (ACSOL March 24, 2023, `SECONDARY`): the court terminated further
treatment for that petitioner under Penal Code § 3008(d)(2). He remained
on GPS, travel, and computer conditions. The statutory hook is the
court's power to disapprove further participation after one year, not
§ 1983.

**What this is.** An unpublished habeas finding that **CDCR / DAPO**
maintained a blanket no-completion-before-discharge policy, and an
individual § 3008(d)(2) termination.

**What this is not.**

- Not a damages case.
- HOPE was **not a party**.
- Not a holding that HOPE's corporate Aftercare Phase is unconstitutional.
- Not binding appellate precedent.
- The Matter 5 FAC proposition that "HOPE's own Executive Director of
  Clinical Training testified under oath that HOPE requires continuous
  treatment" is **`MISCITED`** in `citation_audit.json`. The testimony
  the order actually recites is CDCR / DAPO. Do not repeat the FAC
  attribution.
- ACSOL's news piece describes a "new treatment program provider"
  requiring a restart after the original provider said treatment was
  finished. That is a vendor-change fact pattern. The article **does
  not name HOPE**. Treating *Dwyer* as a HOPE judgment is a
  characterization error.

### 5.2 *Alliance for Constitutional Sex Offense Laws, Inc. v. Macomber*

| Field | Value |
|---|---|
| Caption | *Alliance for Constitutional Sex Offense Laws, Inc.; Christopher Sandahl; Joshua Morales; Alexander Flores; John Doe #1; John Doe #2 v. Jeff Macomber, Secretary of CDCR* |
| Court | L.A. Super. Ct., Dept. 86 |
| Docket | **23STCP02378** |
| Judge | Hon. Mitchell L. Beckloff |
| Hearing | December 13, 2023 |
| Publication | Unpublished tentative / minute ruling. Not in the CL opinion corpus |
| Source | `PRIMARY` (full tentative text from the rulings.law reprint). Settlement terms `SECONDARY` (ACSOL July 2024 write-up; later petitions reciting 15 C.C.R. § 3574) |

Exact disposition of the only order located:

> "[Tentative] ORDER OVERRULING DEMURRER"

The petition sought a writ directing CDCR to amend its regulations so
parolees could complete and terminate SOMP after one year, before
discharge from parole, as § 3008(d) contemplates. Respondent argued
exhaustion, no ministerial duty, and adequate habeas remedy. The court
held the petition challenged statewide regulations and policy, not
individual parole conditions; exhaustion was excused; ultimate facts
plus the *Dwyer* testimony stated a claim.

**What survived:** the writ and declaratory-relief counts, at the
pleading stage, against the **Secretary**. Trial was set for June 14,
2024.

**What did not happen:** no merits finding, no judgment against HOPE,
no § 1983, no QI, no *Monell*, no Bane, no RICO.

**Settlement (public, `SECONDARY`):** ACSOL (July 2024) reported CDCR
agreed in writing that participation may terminate before discharge;
annual individualized consultations; written reasons within 30 days.
CDCR then issued NCR 25-01 and 15 C.C.R. § 3574 language that
supervised persons "may complete a sex offender management program
before discharge from parole" (later petitions quote subd. (d)) and
require written good-cause for retention (subd. (f)). Dollar terms:
none. This is regulatory reform, not a damages precedent.

**Citation trap.** There is a **second** ACSOL v. Macomber:
Sacramento Super. Ct. **25WM000131**, filed July 16, 2025, about a
policy affecting female registrants. That is a different case. Matter 19's
evidence list still reads `ACSOL v. Macomber (Sacramento Super. Ct.
No. 23STCP02378)` — court and number do not belong together. Matters 5
and 6 correctly used the L.A. 2023 action. Do not merge them.

---

## 6. Docket-only / complaint-level / unverified

### 6.1 Portfolio vehicles that name HOPE or Smith — no merits ruling

| Matter | Caption | Court / no. | What was pled | Disposition of the Shannon theories |
|---|---|---|---|---|
| 5 | *Newanforbi v. Palacios et al.* | San Joaquin Super. Ct. STK-CV-UF-2026-0001032; Abdallah, J. | State fraud, negligence, IIED, Bane, UCL, declaratory relief against HOPE and Palacios. **No § 1983** | Demurrer to FAC sustained **without leave** July 15, 2026 **on exhaustion**. Not a ruling that HOPE is or is not a state actor, and not a Bane merits ruling |
| 6 | *Newanforbi v. HOPE et al.* | E.D. Cal. **2:26-cv-00195-TLN-AC** (CL 72184552); Nunley / Claire | § 1983 damages against HOPE; injunctive / *Ex parte Young* against HOPE and Macomber; delegation-without-safeguards | Voluntarily dismissed **without prejudice** May 21 / June 1, 2026 (FRCP 41(a)(1)(A)(i)). **No order on state actor, QI, or *Monell*** |
| 28 | *Newanforbi v. Smith* | N.D. Cal. **3:26-cv-07504-LJC** (CL 73646240) | The live Shannon complaint | Pleading stage. **Not a ruling** |
| 19 | *Newanforbi v. Macomber* | Santa Clara Super. Ct. C2604791; Hawk, J. | Habeas for discharge; attaches *Dwyer* | Pending as of the September 1, 2026 HC-004. Not a vendor-damages case |
| 34 | *Newanforbi v. Counseling and Psychotherapy Center, Inc.* | Unfiled | Mirror of Matter 28 against CPC / McNamara | Pre-filing. Do not treat as a decision |

CourtListener `type=o` and `type=d` for `"HOPE Psychotherapy"` returned
**only Matter 6**. No third-party civil docket naming HOPE as a defendant
was located.

### 6.2 *(HC) Y.S.G. v. Andrews*, E.D. Cal. 2:25-cv-01884

RECAP / docket string-hit for `"HOPE Program" Hayward`. Filed July 3,
2025. Caption is a habeas. **The petition was not opened.** Treat as an
`UNVERIFIED` candidate for a provider mention, not as a HOPE damages
case.

### 6.3 Other Shannon Smith LCSW docket hits

CL `type=d` `"Shannon Smith" LCSW` returned seven dockets (New Orleans
civil rights, Oregon SSA, *Raniere*, two Delaware bankruptcies, Google
Assistant privacy, KServicing). None is the Hayward HOPE CEO. Do not
treat them as related.

---

## 7. Related authorities that are not SOMP-vendor damages cases

Do not cite these as "HOPE cases" or as holdings that a treatment vendor
is liable.

| Case | What it actually is |
|---|---|
| *People v. Garcia*, 2 Cal.5th 792 (2017); *People v. Forney*, 3 Cal.App.5th 1091 (2016); *People v. Friday*; *In re E.J.*, 47 Cal.4th 1258 (2010) | Chelsea's Law / SOMP as a **condition of supervision**. Criminal or habeas. Not a civil damages action against a vendor |
| *Whitehair v. Superior Court*, JAD23-03 (Cal. Ct. App. 2023) | Appeared in a `CASOMB 1983` opinion search. Not confirmed as a vendor-damages case. `UNVERIFIED` — do not cite |
| *Turner v. Smith*, A164194 (Cal. Ct. App. Apr. 26, 2023) (unpublished) | Bane Act against **DAPO employees** over parole conditions and a threat. Gov. Code § 845.8. Not a vendor case |
| *Doe v. Butte County Probation Dept.*, E.D. Cal. 2:20-cv-02248 | PRCS special conditions; Bane + constitutional claims against **probation**. TRO mostly denied. Not a SOMP vendor |
| *Doe v. State of California*, 8 Cal.App.5th 832 (2017) | Bane / registry / anti-SLAPP against DOJ. Not treatment |
| *Reinhardt v. Kopcow*, 65 F. Supp. 3d 1164 (D. Colo. 2014); *Greiman v. Hodges*, 79 F. Supp. 3d 933 (S.D. Iowa 2015) | Out-of-circuit treatment / civil-commitment conditions. Not California SOMP vendors. Do not import as if they decided HOPE |
| Penal Code **§ 9003(c)** | Statutory immunity for certified SOMP professionals for **criminal acts committed by** the persons they treat. It is not immunity for the professional's **own** constitutional torts, fraud, or RICO. Defense will wave it; it does not answer Matter 28 |

---

## 8. Bane Act and RICO pairings

**Bane Act against a SOMP vendor.** No published or unpublished order
was located that imposes — or even reaches the merits of — Civil Code
§ 52.1 liability on a CASOMB-certified treatment firm or its CEO.
Located Bane cases in this neighborhood are against parole/probation
officers or the registry (*Turner*, *Doe v. Butte*, *Doe v. State*).
Matter 5 pled Bane against HOPE and died on exhaustion.

**RICO against a SOMP / containment-model billing enterprise.** CourtListener
and 2020–2026 news searches returned **zero** named cases. Matter 28's
own risk field already treats RICO as an aggressive-scenario multiplier
with a *Twombly* particularity problem. A published RICO dismissal would
be used against the next parolee. Do not pitch RICO as the
precedent-setting count.

---

## 9. News and practitioner items that name cases (2020–2026)

| Source | Date | Case named | Notes |
|---|---|---|---|
| ACSOL, "CA Court Halts Treatment Requirements…" | Mar. 24, 2023 | **Dwyer** | Habeas; § 3008(d)(2); CDCR testimony; does not name HOPE |
| ACSOL, "CA Court Denies Government's Demurrer" | Dec. 13, 2023 | **Macomber** 23STCP02378 | Demurrer overruled; trial set June 14, 2024 |
| ACSOL, "Changes to be Made in Treatment…" | July 2024 | **Macomber** settlement | Written CDCR agreement; regulations to follow; no dollars |
| hopeprogram.biz / LinkedIn | current | none | Marketing and bio pages. No lawsuit disclosure located |
| CASOMB complaint procedure (2024/2025 PDF) | 2024–25 | none | Administrative ethics channel, not a damages case |

No 2024–2026 news item was found that reports a published or unpublished
§ 1983 / Bane / RICO merits ruling against HOPE, Smith, or any other
named California SOMP vendor.

---

## 10. Scoreboard

### Decisions that actually ruled on a Shannon-adjacent question

| Case | Who was sued | Vehicle | Result on the relevant question | Published? |
|---|---|---|---|---|
| *West* (1988) | Contract prison doctor | Supreme Court | State actor | Yes |
| *Richardson* (1997) | Private prison guards | Supreme Court | No QI | Yes |
| *Filarsky* (2012) | Briefly retained city lawyer | Supreme Court | QI | Yes |
| *Jensen* (2000) | Private committing psychiatrist | 9th Cir. | No QI | Yes |
| *Halvorsen* (1998) | Private detox firm | 9th Cir. | No QI | Yes |
| *Ace Beverage* (1998) | Private ticket processor | 9th Cir. | No QI | Yes |
| *Chavez* (2016) | Private OR therapist + PO | 9th Cir. | Sua sponte QI dismissal reversed; state actor **open** | Yes |
| *Chavez* (2021) | Same | 9th Cir. | Dismissal **affirmed**; state actor assumed; **QI granted** | Yes |
| *Dwyer* (2023) | Custody / CDCR (habeas) | San Mateo Super. Ct. | Individual § 3008(d)(2) termination; CDCR no-completion policy | No |
| *Macomber* (2023) | CDCR Secretary | L.A. Super. Ct. | Demurrer **overruled**; later settled; regulations amended | No |

### Not merits decisions on the Shannon theories

All Newanforbi / portfolio HOPE matters. *Pastrana* is irrelevant here.
*Y.S.G. v. Andrews* (unverified habeas string-hit). Criminal Chelsea's
Law cases. Bane cases against parole agents. The 2025 Sacramento ACSOL
file.

### Vendor / CEO damages liability

**Zero** located decisions impose § 1983, Bane, or RICO damages on a
California CASOMB-certified SOMP vendor or its CEO. The only published
Ninth Circuit case that actually sued a private sex-offender therapist
(*Chavez*) ended in a QI win for the therapist.

---

## 11. What would actually be first impression — and what would not

**Not first impression.** *West* already makes a CDCR medical contractor
a state actor when it performs a public function. *Monell* already
requires a policy or custom. *Richardson* / *Jensen* / *Halvorsen* /
*Ace Beverage* already deny QI to a standing for-profit (or firm-like)
contractor. *Dwyer* already found the **CDCR** no-completion policy.
*Macomber* already forced regulatory paper on individualized completion.

**The hole that is real.** No published Ninth Circuit opinion decides
which box a **CASOMB-certified, 16-site, CDCR-contracted SOMP CEO**
occupies: *Richardson* firm or *Filarsky* adjunct. *Chavez* 2021 assumed
state action and then **gave** QI to a single Oregon therapist on
different constitutional theories (self-incrimination, counsel, speech).
It does not decide Smith's QI, HOPE's *Monell* custom, or a California
retention-policy due-process claim.

A written N.D. Cal. order that Smith does **not** get QI — because HOPE
is a standing statewide contractor, not a one-off hire — would be the
first located application of that distinction to this industry. That is
the Shannon analogue to *Mendoza*'s "sue the employer" sentence: existing
law points at the answer; nobody has written it down for this actor.

A *Monell* damages holding that HOPE_000294's Aftercare Phase / full-term
tie is an unconstitutional custom would be the first **damages** vehicle
for a fact pattern *Dwyer* and *Macomber* only reached in habeas and
mandate. It would still be an application of *Monell*, not a new
constitutional rule, and an unpublished district order would not bind
anyone.

**Weaker than UPS, not stronger.** UPS asks a court to say, for the first
time, that an employer who acts on a CRA report sourced to the California
registry "uses" it under § 290.46(j)(2)(E). Shannon asks a court to apply
*West* / *Monell* / *Richardson* to a named vendor. Applying old law to a
new defendant is not the same as filling a statutory gap.

**The first paper will likely be preclusion, not the constitutional
question.** Matter 5 died on exhaustion. Smith was not a state-court
party. Matter 6 is an undisclosed without-prejudice federal predecessor.
A preclusion order is case-specific. It sets no law.

**Settlement pressure cuts against a published opinion.** Philadelphia
Indemnity Policy No. 067968 ($1 million / $5 million) plus Smith's
personal-capacity exposure make a confidential settlement more likely
than in the UPS case. Settlement produces no opinion. Same fork as Pilot
and *Lerma*.

---

## 12. Open gaps (say so, do not fill them)

1. **Dwyer order PDF body** — existence, caption, date, and CDCR-policy
   quotations are primary via the Beckloff tentative and the portfolio
   exhibit. The FAC's HOPE-ED-testimony sentence is already flagged
   MISCITED. Re-read Exhibit B before quoting the order in a filing.
2. **Macomber settlement agreement and the entered December 13, 2023
   minute order** — tentative text is primary; whether the tentative
   was adopted verbatim is `UNVERIFIED`. Settlement dollars: none
   public.
3. **Y.S.G. v. Andrews** petition — not opened.
4. **Clement / Danielson / Ace Beverage / Halvorsen** — holdings used
   from opinion reprints and the safe-cite list; Ace Beverage and
   Halvorsen were read in reprint; Clement / Danielson were not
   re-opened in this file.
5. **California superior-court dockets** that never hit RECAP
   (almost all state filings against vendors). A paid Westlaw/Lexis
   "CASOMB /p 1983" or "sex offender management /p qualified immunity"
   run on unpublished Cal. Super. Ct. is still worth doing. This run
   did not have a paid terminal.
6. **CourtListener authenticated RECAP PDFs** — token was not in the
   environment.
7. **Other named California SOMP vendors** (Sharper Future, Pacific
   Forensic, CPC) — opinion search empty. CPC is Matter 34, unfiled.
8. **Penal Code § 9003(c) case law** — the third-party-crime immunity
   was not briefed out. No opinion was located that extends it to the
   vendor's own constitutional torts. Flag before treating that silence
   as a holding.

---

## 13. Source list (primary)

- *West v. Atkins*, 487 U.S. 42 (1988).
- *Richardson v. McKnight*, 521 U.S. 399 (1997).
- *Filarsky v. Delia*, 566 U.S. 377 (2012).
- *Jensen v. Lane County*, 222 F.3d 570 (9th Cir. 2000).
- *Halvorsen v. Baird*, 146 F.3d 680 (9th Cir. 1998).
- *Ace Beverage Co. v. Lockheed Info. Mgmt. Servs.*, 144 F.3d 1218
  (9th Cir. 1998).
- *Chavez v. Robinson*, 817 F.3d 1162 (9th Cir. 2016) (CDN PDF).
- *Chavez v. Robinson*, 12 F.4th 978 (9th Cir. 2021) (CDN PDF).
- *Alliance for Constitutional Sex Offense Laws, Inc. v. Macomber*,
  L.A. Super. Ct. No. 23STCP02378, tentative Dec. 13, 2023
  (Beckloff, J.) (rulings.law reprint).
- CourtListener dockets: 73646240 (Matter 28), 72184552 (Matter 6).
- Cal. Penal Code §§ 3008(d), 9003(c); 15 C.C.R. § 3574 (as quoted
  in later mandate petitions).
- Portfolio `citation_audit.json` (Dwyer MISCITED attribution;
  Macomber 2023 vs 2025 split).
