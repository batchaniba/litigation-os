# Matter 43 — Hertz claim foundation: what the offer letter and the report actually prove

Prepared November 2, 2026 (Pacific), as a review of PR #1063 and an independent re-read of the primary documents.
Work product. Not a complaint, not a demand, not for service. No settlement figures appear here, by design (settlement-guard).
Do not put repository or document-store links in anything sent to Hertz, HireRight, a court, or the CRD.

Companion files: `PC29046_EVIDENCE.md` (element map), `LITIGATION_CLAIMS_AUDIT_2026-11-02.md`, `PLEADING_ARCHITECTURE_AND_RESPONSE.md`. Portfolio doctrine: `internal/docs/PC_29046_EMPLOYMENT_CASES.md`.

Citation status tags: **[V]** checked this session against a primary or reliable secondary source; **[V-repo]** marked primary-verified in the portfolio memo; **[UNVERIFIED]** I could not reach it this session (leginfo, justia, findlaw, and meganslaw.ca.gov are blocked by this session's network policy). Every [UNVERIFIED] item must be pulled and read before it goes in a filing.

---

## 0. Reconciliation with `CLAIMS_FOUNDATION.md` (concurrent commit 9702b28)

A second memo landed on this branch while this one was being written. It is careful and mostly consistent with this one: Santa Clara Superior Court, The Hertz Corporation as the core defendant, the Fair Chance Act as the lead count, § 290.46 kept separable, HireRight out, and no dollar figures. Where the two memos differ, here is what controls, and why.

| Point | `CLAIMS_FOUNDATION.md` | This memo | Resolution |
|---|---|---|---|
| Offer letter | "Its bytes are not in this checkout"; told not to plead its terms | Read from R2 (sha256 a52a2598…) | **This memo.** The letter is in hand. It says "Manager Trainee (Full time)" with **no weekly hours and no start date**, so back pay will need the hours from Hertz's records. Its contingency clause (W1), "company standards" rescission clause (W2), and non-compete term (W4) are now pleadable. |
| License status | "Not an allegation that the license is currently valid. Only the report's printed dates are in the file." | Report p. 8 prints "C, issued Jul 21, 2026, expires May 12, 2027, **VALID**" | **This memo.** It's on the face of the report. |
| ICRAA § 1786.16 | "No specific missing item yet ... not pleaded on a hunch" | Specific defect identified: the California disclosure sits outside the signed document, and the signed document bundles five other states' notices and the LA ordinance (W18–W19, page-mapped) | **This memo.** It's a page-level fact, not a hunch. Plead in state court. |
| Response letter | Send the neutral draft (PLEADING_ARCHITECTURE §D): no § 290.46 mention; asks Hertz to identify every item and conviction | Revised draft (§ 9): disputes the alcohol label, invokes the § 12952(c)(3) extension, objects to registry use, does **not** invite Hertz to name a conviction | **Plaintiff's call. Real disagreement, both defensible.** The other memo's worry is that naming § 290.46 invites a *Donaleski* "independent decision" memo. This memo's worry is that asking Hertz to "identify each conviction" invites a clean re-notice on C1761642, Hertz's strongest lawful ground. Middle option: send the § 9 draft without the § 290.46 paragraph. That keeps both risks low and loses only the willfulness notice. |
| Hertz Global Holdings | Off the complaint | Name it with entity-specific facts; dismiss voluntarily if discovery shows no role | **Plaintiff's call.** The WOTC/ADP facts (W21) are real but thin. Naming HGH costs a likely motion. Leaving it off loses nothing that can't be added by amendment. If the caption must read "v. Hertz Global Holdings, Inc.," plead agency and integrated-enterprise facts separately for each entity. |
| Labor Code § 432.7 / § 12952(a)(3)(A) | Out: license actions aren't arrests | Alternative only (Exit A), flagged contested | Keep as an **alternative paragraph inside the Fair Chance count**, not a standalone lead count. Both memos agree it isn't load-bearing. |
| CRD timing | Open the charge now; request an immediate right-to-sue | After the final decision | Either works. A right-to-sue notice starts the deadline to file the civil action (confirm the current period in Gov. Code § 12965), so getting it early only shortens the runway. Prefer waiting until the final decision is in hand. |

---

## 1. Bottom line

1. **The best case against Hertz is a trap with two exits, and both are violations.** The November 2 pre-adverse letter names one ground: "[Criminal Information] Alcohols related offenses-Does not meet." The report Hertz reviewed contains **no alcohol-related criminal conviction**. The only alcohol items are DMV administrative actions: a refusal suspension (ended May 19, 2026) and a commercial-license disqualification (ended Nov. 30, 2025). The only criminal conviction flagged for review is the 2018 Santa Clara case (C1761642).
   - **Exit A: Hertz really relied on the alcohol items.** Then it treated non-conviction information as "Criminal Information." A chemical-test refusal suspension presupposes an arrest, and no conviction followed. That supports Gov. Code § 12952(a)(3)(A) (arrest not followed by conviction) and Labor Code § 432.7(a)(1).
   - **Exit B: Hertz really relied on the conviction or the registry.** Then the notice failed to identify the disqualifying conviction (§ 12952(c)(2)(A)). If the registry was part of the basis, § 290.46(j)(2)(E) is violated.
   - Hertz cannot pick an exit without admitting one of these. Plead both, in the alternative (FRCP 8(d)(2)–(3); California also permits inconsistent pleading).
2. **The "use" element of § 290.46 can be pleaded from Hertz's own system design, not just from its stated reason.** HireRight graded every registry result against Hertz's "Company Standards": "Not in Registry → **Meets Company Standards**" and "In Registry → **Client Review Required**." The offer letter makes "company standards" the condition of employment: "if my background check does not meet company standards, my contingent offer will be rescinded." Hertz therefore built California registry status into the criterion that decides employment, and then reviewed the results. That is use "for purposes relating to employment," and it is already complete.
3. **Source ("disclosed pursuant to this section") is now pleadable with a factual chain, not a guess.** DOJ's SMART Office describes NSOPW as querying each state's **public** registry website in real time, and NSOR as restricted to law enforcement [V]. A private CRA's "search performed through the United States Department of Justice" can only be NSOPW. NSOPW can return a California registrant only by querying California's § 290.46 website. HireRight's own researcher then wrote "LISTED ON THE SEX OFFENDER REGISTRY IN THE STATE OF CA" and cited § 290.46.
4. **Hertz's best defense is real, and you should plan around it.** The same report contains the 2018 Santa Clara conviction, which Hertz may lawfully consider through a compliant Fair Chance process (*Donaleski*; § 290.46(j)(3)). If Hertz re-notices correctly on that conviction and does an individualized assessment, the Fair Chance procedural claims shrink and the § 290.46 causation fight gets harder. Section 6 is built to keep Hertz from making that move cheaply.
5. **Two claims that don't depend on the background check exist today:**
   - **ICRAA standalone-disclosure defect.** The California authorization was signed on a page bundled with five other states' notices and the Los Angeles ordinance (English and Spanish), and it misnames the employer "The Herz Corporation." That is the *Gilberg* fact pattern, enforceable under Civ. Code § 1786.50.
   - **Non-compete as a condition of the offer.** Bus. & Prof. Code § 16600.5 gives a *prospective* employee a private right of action.
6. **Don't file yet.** Respond to the pre-adverse letter by **Thursday, Nov. 5** (hard stop **Monday, Nov. 9**), lock Hertz into a final written reason, then get a CRD right-to-sue and file. Waiting for the final decision turns a procedural case into a lost-job case and fixes Hertz's story in writing.

---

## 2. PR #1063 review

**Merge-worthy as a record PR.** The catalog work, the redaction discipline (no SSN, DOB, or street in the memos), the § 290.46 subdivision correction (290.46(j), not 290(j)), the *Mendoza* warning, and the "do not plead rescission yet" caution are all correct. `npm run gate` passed per the PR body.

**What it gets wrong or misses:**

| # | Issue | Fix |
|---|---|---|
| 1 | Treats "use" as provable only by the stated reason in the letter. | Plead structural use: "Company Standards" registry grading plus the offer letter's rescission clause (Section 4, item W1–W3). |
| 2 | Calls source "not proved" and stops. | NSOPW/NSOR mechanics plus HireRight's own "State of CA / § 290.46" notes make source plausible under *Twombly*. Facts peculiarly within defendants' control may be pleaded on information and belief. Cite *Soo Park v. Thompson*, 851 F.3d 910 (9th Cir. 2017) [UNVERIFIED pin; confirm the "information and belief" passage]. |
| 3 | Never notices the letter's word **"including."** | "Information ... that may result in Company deciding not to offer you ... **including** the following specific information." The notice is non-exhaustive on its face. That supports both the § 12952(c)(2)(A) defect and the inference that other report items, including the registry, were part of the basis. |
| 4 | Misses the **timing evidence**. | HireRight delivered the MVR (the only "alcohol" data) to Hertz on **Oct. 23 at 3:07 PM**. Hertz kept onboarding him for 10 days. The pre-adverse letter came **~7 hours 50 minutes** after the report carrying the registry hits and the sex-offense conviction was completed (Nov. 2, 2:29 AM → 10:19 AM). |
| 5 | Misses that the letter **short-changes the response period**. | The letter runs five business days "from the date of this letter." Hertz's own bracketed template states the standard as five business days "from the date of **receipt**," with email deemed received two business days after sending. Those conflict on the face of the letter. |
| 6 | Misses the **ICRAA standalone defect** in "Other Disclosures and Authorizations." | See Section 5, Count 4. |
| 7 | Misses the **offer letter's non-compete requirement**. | See Section 5, Count 6. |
| 8 | Misses that **HireRight adjudicated**, not just reported. | "Managed Adjudication 3.0"; activity log "Adjudicated — HireRight — Client Review Required"; each registry subrequest graded against Hertz's standards. The portfolio memo itself says a CRA "becomes materially more exposed only if ... it itself adjudicated." That is the *Mendoza* distinction, visible on the face of the report. (Strategic caution about suing HireRight is in Section 7.) |
| 9 | Doesn't address the **consent defense**. | He signed a disclosure listing "National Sex Offender Registry." Answer: § 290.46(j) regulates *use*, not acquisition, and a law established for a public reason cannot be contravened by private agreement (Civ. Code § 3513 [V-general; confirm text]). The Fair Chance Act likewise cannot be waived. |
| 10 | Response draft invites Hertz to "identify each disqualifying conviction." | That invites Hertz to cure by re-noticing on C1761642, its strongest lawful ground. Section 9 has a revised response that disputes the alcohol characterization without asking Hertz to pick a new conviction. The trade-off is flagged there. |
| 11 | PR cites *Parsonage*, *Yeh* and *McInerney* (2026). | I could not reach those opinions this session. Treat them as **[UNVERIFIED]** until read. *McInerney*'s procedural-damages limit, if accurate, is a real constraint on Fair Chance damages. |

**Recommendation on the PR:** merge it as the record layer, add this file, and leave `claims.json` untouched until the final decision arrives. I did not post a GitHub review comment.

---

## 3. Deadlines (computed; verify the regulation text)

| Clock | Computation | Date |
|---|---|---|
| Hertz's own stated hold | "At least five (5) business days from the date of this letter" (Nov. 2): Nov. 3, 4, 5, 6, 9 | No final decision before **Tue. Nov. 10** |
| Statutory response window | Gov. Code § 12952(c)(3): at least 5 business days to respond. Email notice deemed received 2 business days after sending, per 2 CCR § 11017.1 as quoted in Hertz's own template [UNVERIFIED text]. Sent Mon. Nov. 2 → received **Wed. Nov. 4** → Nov. 5, 6, 9, 10, 11 | **Wed. Nov. 11** if Veterans Day counts as a business day; **Thu. Nov. 12** if it does not |
| Dispute extension | § 12952(c)(3): a timely written notice that he disputes the accuracy of the conviction history report and is taking specific steps to obtain evidence → **5 additional business days** | Must be sent inside the first window |
| **Action date** | Use the earliest computation (the letter's own) and build in margin | **Send the response Thu. Nov. 5; hard stop Mon. Nov. 9** |
| FEHA / CRD | Administrative complaint within 3 years of the violation (Gov. Code § 12960(e)) [UNVERIFIED current text]. Immediate right-to-sue is available. | No pressure; file after the final decision |
| § 290.46, ICRAA, Labor Code § 432.7 | Limitations not computed here. ICRAA has its own period (Civ. Code § 1786.52) [UNVERIFIED]. | Calendar after the final decision |

Calendar entries: response target Nov. 5; hard stop Nov. 9; watch for the final notice from Nov. 10.

---

## 4. The documents as weapons (page-cited)

**Offer letter, Oct. 22, 2026** (`Offer Letter - Manager Trainee, Palo Alto ($23 per hour)`), 3 pp.

- **W1. Contingency is defined, and it doesn't include a registry search.** "This offer is contingent upon the successful completion of a pre-employment MVR check (as applicable), criminal, employment and education background checks ('Background Checks')." (p. 2). Hertz then ordered a "National Sex Offender Registry" product, and its package line reads "Excl. MVR, EDU, EMP." It appears no employment or education verification was run at all. The registry search sits outside the bargained-for checks, and its only conceivable purpose for a California job is employment screening.
- **W2. "Company standards" is the rescission trigger.** "If my background check does not meet company standards, my contingent offer will be rescinded, and my employment will be null and void." (p. 2). This is an automatic-rescission term. It ties directly to the report's "Meets Company Standards" grading (W5). It is also evidence of a non-individualized matrix, in tension with § 12952(c)(1).
- **W3. Employer identity.** "Offer of employment with The Hertz Corporation"; "Hertz Local Edition"; "Branch Manager Trainee ... entry position to our management career path"; reports to Kathleen Williams; 816 San Antonio Rd, Palo Alto. Accepted by email at 4:49 PM, status "Offer Accepted" at 5:42 PM.
- **W4. Non-compete as a "fundamental term and condition."** "It is a fundamental term and condition of your employment that you must execute and deliver ... the below details regarding Employee Confidentiality & Non-Competition." (p. 2). See Count 6.

**HireRight report, OR-102326-NH87V** (18 pp.)

- **W5. Registry graded against Hertz's standards.** Adjudication summary: NSOR subrequest 1 "In Registry — Client Review Required"; subrequest 2 "Not in Registry — **Meets Company Standards**"; subrequest 3 "In Registry — Client Review Required" (pp. 4, 6). Library: "The Hertz Corporation (Shell) (GL-HTZ001-001) v1.7" (p. 6). Registry status is an input to Hertz's eligibility rules.
- **W6. Source chain.** "National Sex Offender Registry search performed through the United States Department of Justice" (pp. 9–10). Notes: "APPLICANT IS LISTED ON THE SEX OFFENDER REGISTRY IN THE STATE OF CA"; "Information from the California Sex Offenders' Registry may not be used for employment purposes except to protect a person at risk. See CA Penal Code Section 290.46" (Satish Kumar R, Oct. 30, 9:17 AM; Kumar Dilip, 12:45–12:46 PM). The returned alias list (Newanforbi / Ngwanforbi / Newanforbi, Brendan N / Ngwa-Nforbi) is a registry payload, not HireRight's own data.
- **W7. Notice of illegality delivered to Hertz.** The § 290.46 warning is printed on the report Hertz reviewed. It supports knowledge, willfulness, exemplary damages under § 290.46(j)(4)(A), and malice under Civ. Code § 3294. The rules (library v1.7) are corporate policy, which supports managing-agent ratification under § 3294(b) (*White v. Ultramar* (1999) 21 Cal.4th 563 [UNVERIFIED pin]).
- **W8. The "alcohol" data was in Hertz's hands from day one.** MVR completed Oct. 23, 3:04 PM; "MVR Express report provided to The Hertz Corporation," Oct. 23, 3:07 PM (activity log p. 17; HireRight email Oct. 23, 3:05 PM naming Gloria Williams). Hertz sent no pre-adverse notice for 10 days and continued preboarding.
- **W9. The registry and sex-offense data arrived last, and the notice followed within hours.** Santa Clara court record Oct. 30, 9:10 AM; registry hits Oct. 30, 11:25 AM and 12:48 PM; report adjudicated Nov. 2, 2:29 AM; pre-adverse email Nov. 2, 10:19 AM.
- **W10. The license is valid now.** "C | Issued Jul 21, 2026 | Expires May 12, 2027 | VALID" (p. 8). Suspension reinstated May 19, 2026; CMV disqualification cleared Nov. 30, 2025. Neither is a criminal conviction. The only MVR conviction is a Vehicle Code § 4000(a) registration infraction, which is zero points and not alcohol-related.
- **W11. No DUI conviction anywhere.** All San Joaquin (Stockton/Tracy) county searches, E.D. Cal., D. Wyo., and Sheridan County searches: "No Court Record Found." The refusal suspension implies an arrest, and the report shows no conviction for it.

**Pre-adverse letter, Nov. 2** (`HireRight - CA Pre-Adverse Letter`)

- **W12.** "[Criminal Information] Alcohols related offenses-Does not meet." It mislabels administrative data as criminal and identifies no conviction.
- **W13.** "...information in your background report that may result in Company deciding not to offer you ... **including** the following." The list is non-exhaustive.
- **W14.** The deadline line is an unfilled bracket. No date is given.
- **W15.** The letter runs "five (5) business days from the date of this letter," while the bracket states the standard as "from the date of receipt" with email "deemed received two business days after it is sent." That is self-contradictory on its face.
- **W16.** No mention of the additional five business days for an accuracy dispute (§ 12952(c)(3)).
- **W17.** The letter refers to "Company's preliminary decision recinding the offer of employment." Hertz itself calls it a decision.

**Signed disclosures, Oct. 23** (`HireRight - Other Disclosures and Authorizations`), one 12-page PDF, one signature block (p. 3)

- **W18.** Pages 1–3 form a single signed document. It contains: the "Disclosure Regarding Investigative Consumer Report" (employer misnamed "The **Herz** Corporation"); Massachusetts, Minnesota, New Jersey, New York, and Washington notices; the City of Los Angeles Fair Chance ordinance notice in English and Spanish; and the California/Minnesota/Oklahoma copy checkbox. Then comes the signature.
- **W19.** The "CALIFORNIA DISCLOSURE" (p. 8) is unsigned. It sits after the signature in the same PDF, bundled with the FCRA summary (pp. 4–7), New York Correction Law Art. 23-A (pp. 9–10), and San Francisco ordinance posters (pp. 11–12).
- **W20.** By contrast, the federal FCRA "Disclosure and Authorization" is a clean standalone page. Don't plead an FCRA § 1681b(b)(2) claim; it would fail.

**Hertz Global Holdings links**

- **W21.** ADP email, Oct. 22, 5:00 PM: "Along with your recently submitted job application with **Hertz Global Holdings, Inc.**, this company requests that you complete Work Opportunity Tax Credit Questionnaire." The confirmation portal is branded "Hertz Global Holdings, Inc." (confirmation no. 12663).
- **W22.** Same address on every Hertz document: 8501 Williams Rd, Estero, FL 33928.

---

## 5. Claim architecture

Ranked by **12(b)(6) survivability × value**. "Ripe now" means the violation is complete on the Nov. 2 record.

### Count 1 — Penal Code § 290.46(j)(2)(E), (j)(4)(A), against The Hertz Corporation (and HGH on agency or integrated-enterprise facts)

| Element | Facts | Status |
|---|---|---|
| Information "disclosed pursuant to" § 290.46 | W6; NSOPW/NSOR mechanics [V]; HireRight's own § 290.46 characterization | Plausible; plead source facts specifically, with "on information and belief" only for the NSOPW → meganslaw.ca.gov link |
| Defendant "used" it | W1, W2, W5, W9, W13, W17. Hertz configured the registry product into its California package, graded registry status against "Company Standards," required review of "In Registry" hits, reviewed the report, and issued a preliminary decision "based on a review of the results of your background report and Company's eligibility criteria" | **Ripe now** (structural use plus a preliminary decision) |
| For purposes relating to employment | The report is an employment report (req. 43711); the letter is an employment decision | Clean |
| No (j)(1) / (j)(3) authorization | No statute authorizes a car-rental employer to screen with Megan's Law information (contrast *Pastrana*, Pen. Code § 11105(c)(10)(A), utility in-home workers [V-repo]). "Person at risk" is undefined. The exception is the defendant's to plead and prove (Evid. Code § 500 [V-general]). AG Op. 05-301 reads (j) as "unequivocal" [V-repo]. | Plead the negative briefly; don't over-argue |
| Remedy | Actual damages; plus up to 3× actual, **not less than $250**; plus attorney's fees; plus exemplary damages **or** a civil penalty up to $25,000. Not a floor; not automatic stacking [V-repo]. | Emotional distress counts as actual damage; lost wages only once a loss is documented |

**Their best answers:**
- *Mendoza* (182 Cal.App.4th 1644 (2010)) [V-repo]: liability rests with the employer that acts on the information. That supports suing Hertz.
- *Donaleski* (E.D. Cal. 2009) [V-repo]: an independent lawful source defeats causation. Answer: Hertz did not cite the court record. It cited "alcohol." Its registry grading is not independent of the registry. And unlike *Donaleski*, no separate decision-maker exists who never saw the registry; the reviewer saw both on the same report.
- *Lerma* (C.D. Cal. 2023) [V-repo]: the report killed the source theory because the registry search returned "NO RECORD FOUND." Here the report shows "In Registry" with California and § 290.46 notes. That is the opposite fact.
- UPS's pending argument in Matter 26 ("national registry, not California's"): answered by the NSOPW mechanics and HireRight's own notes. **Watch for Judge Delaney's ruling in 2:26-cv-02847.** It is under submission and will be the first federal construction on this exact point.

### Count 2 — Fair Chance Act, Gov. Code § 12952 (FEHA), against The Hertz Corporation (plead alternatively)

| Theory | Basis | Status |
|---|---|---|
| 2A. Notice failed to identify the disqualifying conviction(s) — § 12952(c)(2)(A) [UNVERIFIED text] | W12, W13: "Alcohols related offenses" is not a conviction; "including" is open-ended | **Ripe now** |
| 2B. No deadline stated — § 12952(c)(2)(C) [V-secondary] | W14 | **Ripe now; facially provable** |
| 2C. Response period computed short and dispute extension omitted — § 12952(c)(3) | W15, W16 | **Ripe now** |
| 2D. Exit A: considered arrest not followed by conviction — § 12952(a)(3)(A) [V-secondary] | W10, W11, W12 | Ripe once Hertz confirms the alcohol basis, or on final decision |
| 2E. Final-decision defects — § 12952(c)(4)–(5) | Must consider the response; final notice must state the CRD complaint right, among other things | Watch the final notice |
| 2F. Individualized assessment — § 12952(c)(1)(A) | W2 automatic-rescission term; minutes-long turnaround | Plead on information and belief; *McInerney* (if accurate) limits merits review, so keep it secondary |

Prerequisite: a CRD complaint and right-to-sue. Remedies: FEHA compensatory damages (emotional distress), punitive damages, injunctive and declaratory relief, and fees.
**Weakness:** procedural-violation damages need proof of harm (*McInerney* [UNVERIFIED]). Value jumps if the offer is finally rescinded.

### Count 3 — Labor Code § 432.7(a)(1), against The Hertz Corporation (Exit A)

- **Text:** an employer may not "utilize, as a factor in determining any condition of employment including hiring ... any record of arrest or detention that did not result in conviction" [V-secondary].
- **Facts:** a refusal suspension (Veh. Code § 13353 presupposes an arrest [UNVERIFIED]), no conviction anywhere (W11), and Hertz's own "[Criminal Information]" label.
- **Remedy (applicant):** actual damages or $200, whichever is greater, plus costs and fees. The treble/$500 "intentional violation" language appears only in older printings; **do not plead it until the current text is read** [UNVERIFIED].
- **Weakness:** Hertz will say a DMV administrative record is a licensing fact, not an "arrest record," and that a driver-required job justifies reviewing it. This is a real contest, but it is a legitimate reading. It also lets Hertz's "driver required" argument meet W10: the license is valid now.

### Count 4 — ICRAA standalone disclosure, Civ. Code § 1786.16(a)(2)(B), § 1786.50, against The Hertz Corporation

- **Facts:** W18 and W19. The California disclosure was not "in a document that consists solely of the disclosure." The signed document bundles multi-state notices and the Los Angeles ordinance and misnames the employer.
- **Authority:** *Gilberg v. California Check Cashing Stores, LLC*, 913 F.3d 1169 (9th Cir. 2019) [V-secondary; pull the opinion]. Extraneous state notices violated the standalone requirement, and the court treated ICRAA as parallel.
- **Remedy:** actual damages or **$10,000, whichever is greater**, plus costs and fees; punitive damages if grossly negligent or willful (§ 1786.50(a)–(b)) [V-repo].
- **Ripe now.** Strongest in **state court**. In federal court, Article III requires concrete harm (*TransUnion LLC v. Ramirez*, 594 U.S. 413 (2021) [V-general]). Plead the downstream harm: the procured report was used to issue an adverse decision.
- **Their answer:** page 8 was a separate screen in the e-sign flow. Answer: the signed record HireRight preserved is one document with one signature block; native e-sign logs are demanded in Section 10.

### Count 5 — Fair Chance / § 290.46 exemplary-damages enhancers (not a count; plead in each count)

W7: knowledge from the printed § 290.46 warning; corporate rules (v1.7) as managing-agent policy. Your response letter (Section 9) adds express notice before any final decision.

### Count 6 — Bus. & Prof. Code § 16600.5 (void non-compete required of a prospective employee), against The Hertz Corporation

- **Facts:** W4. The offer makes signing an "Employee Confidentiality & Non-Competition" document a "fundamental term and condition," and he clicked ACCEPT.
- **Statute:** an employer "shall not enter into a contract with an employee or prospective employee that includes a provision that is void"; subdivision (e)(1) gives an employee, former employee, **or prospective employee** a private action for injunctive relief and/or actual damages; (e)(2) gives prevailing-party fees [V-secondary; read the enrolled SB 699 text]. Related: § 16600.1; Labor Code § 432.5 (requiring an applicant to agree in writing to a term known to be prohibited by law) [UNVERIFIED text].
- **Gap:** get the actual Non-Competition document from the Hertz/Oracle portal before pleading. If it is only a confidentiality clause with no restraint, drop this count.
- **Value:** small in dollars, but large in leverage. It is a clean, company-wide California template problem. It survives 12(b)(6) easily if the document exists. Article III risk in federal court is moderate, so state court is safest.

### Reserve — don't plead now

- **Breach of the express contingency / implied covenant** (registry search outside the defined Background Checks). At-will employment caps damages (*Guz v. Bechtel* (2000) 24 Cal.4th 317 [V-general]). Revisit if he incurred reliance costs.
- **FEHA criminal-history disparate impact** (2 CCR § 11017.1 adverse-impact provisions [UNVERIFIED subdivision]). Needs statistics; possible later.
- **UCL § 17200.** Requires lost money or property (*Kwikset*). Revisit after any final rescission.
- **Tameny.** Failure-to-hire is vulnerable (portfolio memo).
- **FCRA § 1681b(b)(2) / (b)(3).** The federal disclosure is clean and the pre-adverse copy and summary were delivered. **No viable federal-question claim exists today.** Don't manufacture one.
- **ICRAA § 1786.18(a)(7) seven-year bar.** Release Dec. 2, 2020 is within seven years of the Nov. 2, 2026 report (*Kemp* [UNVERIFIED pin]). Dead.
- **FCRA/ICRAA accuracy against HireRight.** The report is accurate as printed; the mislabel is Hertz's. Dead unless he disputes a specific MVR entry as factually wrong.

---

## 6. The fork, pleaded

Draft paragraph architecture (alternative allegations):

> **Alternative A.** To the extent Hertz's preliminary decision rested on the "Alcohols related offenses" it identified, the only alcohol-related entries in the report are a Department of Motor Vehicles chemical-test refusal suspension that ended May 19, 2026 and a commercial-license disqualification that cleared November 30, 2025. Neither is a criminal conviction. A chemical-test refusal suspension presupposes an arrest, and the report reflects no conviction arising from that arrest in any jurisdiction searched. Hertz labeled that information "[Criminal Information]" and used it as a factor in a hiring decision, in violation of Government Code section 12952(a)(3)(A) and Labor Code section 432.7(a)(1).
>
> **Alternative B.** To the extent Hertz's preliminary decision rested in whole or in part on conviction history, the only criminal conviction flagged for review in the report was not identified in Hertz's notice, in violation of Government Code section 12952(c)(2)(A). To the extent the decision rested in whole or in part on the California sex-offender registry information that HireRight graded against Hertz's "Company Standards," Hertz used information disclosed pursuant to Penal Code section 290.46 for purposes relating to employment, in violation of section 290.46(j)(2)(E).
>
> **In every alternative**, Hertz's notice stated no response deadline, computed the response period from the date of the letter rather than the date of receipt, and omitted the additional five business days available to an applicant who disputes accuracy, in violation of Government Code section 12952(c)(2)–(3).

The shifting-reasons inference applies too: if Hertz's final notice cites a different ground than "alcohol," that shift is itself evidence of pretext. Pull a current California authority for the shifting-reasons principle before citing it [UNVERIFIED].

---

## 7. Defendants

| Defendant | Role | Recommendation |
|---|---|---|
| **The Hertz Corporation** | Offeror, report procurer, author of the pre-adverse letter, owner of the "Company Standards" | **Lead defendant on every count.** |
| **Hertz Global Holdings, Inc.** | W21 (the application was "with Hertz Global Holdings, Inc."; HGH-branded WOTC), W22. WOTC credits belong to the employer; plead on information and belief that HGH, as consolidated parent, claims them. | **Name it, with specific facts**: agency (ADP acting for HGH in the application process), integrated enterprise under FEHA (*Laird v. Capital Cities/ABC, Inc.* (1998) 68 Cal.App.4th 727 [UNVERIFIED pin]: interrelated operations, common management, centralized labor relations, common ownership), and joint participation. **Do not lump** "Hertz" in a way that invites a Rule 8 group-pleading motion; give each entity its own paragraphs. The PR's statement that HGH's 10-K says it "does not conduct operating business itself" is [UNVERIFIED]. Expect a motion. Be ready to dismiss HGH voluntarily if discovery shows no role, rather than lose it on a fee-bearing motion. Your caption preference ("v. Hertz Global Holdings, Inc.") works, with The Hertz Corporation as co-defendant. |
| **HireRight, LLC** | Adjudicated against Hertz's standards (W5, W8) | **Do not sue it now.** *Mendoza* affirmed an **anti-SLAPP strike with fee exposure** against the plaintiff on § 290.46 and ICRAA claims against a screening company. The adjudication facts distinguish *Mendoza*, but a fee award against a pro se plaintiff is a real cost. Use HireRight as a **subpoena target** for source and adjudication logs. Revisit naming it once those logs show it applied Hertz's registry rule itself. Anti-SLAPP is not a meaningful threat against Hertz: the hiring decision is the wrong complained of, not speech (*Park v. Board of Trustees of Cal. State Univ.* (2017) 2 Cal.5th 1057 [V]). |

---

## 8. Forum and 12(b)(6) engineering

**Recommendation: draft to the federal *Twombly/Iqbal* standard, and file in Santa Clara County Superior Court.**

- **Venue.** The job is in Palo Alto. For FEHA, venue lies where the practice occurred or where he would have worked (Gov. Code § 12965 [UNVERIFIED subdivision]).
- **Why state court.**
  - Every viable claim is state law.
  - ICRAA and § 16600.5 have Article III exposure in federal court.
  - State-court standing is broader (*Parsonage* / *Yeh* per the PR [UNVERIFIED]).
- **Expect removal on diversity.** Hertz entities are Delaware/Florida. HireRight is not named, so its LLC member citizenship doesn't matter. The amount in controversy will be argued from exemplary damages, the civil penalty, and FEHA punitive damages.
- **If Hertz removes and then attacks standing, the remedy is remand, not dismissal** (*Polo v. Innoventions Int'l, LLC*, 833 F.3d 1193 (9th Cir. 2016) [V-secondary]). Hertz cannot both remove and win a standing dismissal.
- **Either way, a complaint built to survive 12(b)(6) also survives a demurrer.**

**12(b)(6) checklist for the draft:**

1. Each count names one defendant and one statute, with the elements laid out in order.
2. Every "use" allegation is anchored to a document line (W1, W2, W5, W9, W13, W17), not to adjectives.
3. Source: plead NSOPW and NSOR as facts about the federal systems (cite 34 U.S.C. §§ 20921–20922 [V-secondary] and the SMART fact sheet). Plead "on information and belief" only for the final link, and say why: those facts are peculiarly within defendants' control.
4. **Plead the bad facts yourself**: the 2018 conviction exists; the MVR items exist; the license is now valid. Hertz will incorporate the report by reference (*Khoja v. Orexigen Therapeutics, Inc.*, 899 F.3d 988 (9th Cir. 2018) [UNVERIFIED pin]). Owning those facts takes away *Lerma*-style surprise.
5. Quote the report; don't attach it whole. It contains a partial SSN, DOB, and home address (FRCP 5.2; Cal. Rules of Court, rule 1.201). If attached, file a redacted copy.
6. Anticipate the affirmative defenses (person at risk, (j)(3) authorization, consent, *Donaleski*) without bearing the burden on them. One sentence each.
7. Damages: plead categories and statutory remedies. **No dollar totals and no settlement figures in the pleading** (settlement-guard; any number goes through `npm run negotiate:check`).
8. Run the full Apodictic stress test and the verification-foundation citation funnel on the drafted complaint before filing.

---

## 9. Pre-adverse response — revised draft (for Plaintiff's review; do not send without approval)

**To:** Gloria Williams (Gloria.Williams@hertz.com) and Kesha Nedio-Casey (kesha.nediocasey@hertz.com). Both appear on Hertz/HireRight documents for this order.
**Subject:** Requisition 43711 — response to November 2 preliminary notice (OR-102326-NH87V)

> Dear Ms. Williams and Ms. Nedio-Casey,
>
> I am writing in response to The Hertz Corporation's November 2, 2026 preliminary notice regarding my accepted offer for the Manager Trainee position in Palo Alto (requisition 43711, HireRight order OR-102326-NH87V). I remain committed to joining the Palo Alto team and would like this response considered before any final decision.
>
> The notice identifies "[Criminal Information] Alcohols related offenses" as the information at issue. I respectfully dispute that description. I have no alcohol-related criminal conviction, and the background report does not show one. The only alcohol-related entries are Department of Motor Vehicles administrative actions: a suspension that ended with reinstatement on May 19, 2026, and a commercial-license disqualification that cleared on November 30, 2025. Neither is a criminal conviction. The same report shows that my California Class C license is valid through May 2027.
>
> Because I dispute the accuracy of the information as characterized, and I am obtaining my certified DMV driving record to document its current status, I am notifying you under Government Code section 12952(c)(3) that I am taking specific steps to obtain that evidence and am requesting the additional five business days the statute provides. I also note that the notice did not state a response deadline, and that California measures the response period from the date an emailed notice is deemed received.
>
> I also want to raise one concern directly. The report includes California sex-offender registry information, and HireRight's own notes on that entry state that, under Penal Code section 290.46, registry information may not be used for employment purposes except to protect a person at risk. I ask that Hertz not consider that information in any way in its decision, and I would appreciate written confirmation that it has not been and will not be considered.
>
> Please preserve all records relating to this hiring decision, including the adjudication history and rules applied to order OR-102326-NH87V, reviewer notes, and communications.
>
> I would welcome the chance to answer any questions or to provide anything else that would be helpful. Could you confirm receipt and let me know the best contact for submitting the DMV record once I have it?
>
> Thank you,
>
> Brendan Ngwa Nforbi

**Choices to make before sending:**

- **Close.** The portfolio's locked close ("Plaintiff, In Propria Persona") is written for litigation participants. No case exists against Hertz, and that line would signal litigation to a recruiter. I used the name only. Override if you want the locked close.
- **Whether to keep the § 290.46 paragraph.** *Keep it (recommended):* it makes any later registry-influenced decision knowing (exemplary damages; malice under § 3294) and forces Hertz to commit in writing. *Cost:* Hertz's lawyers see it and may steer the final decision to the court record (*Donaleski* path). The report and its adjudication history are already fixed, so the structural-use evidence doesn't change.
- **No invitation to name a new conviction.** That is deliberate (PR issue #10).
- **Rehabilitation evidence.** The letter asks for mitigation "of the specific criminal information identified above," which is the alcohol item. Offering mitigation about the 2017 case would concede it is in play. If your goal is the job itself rather than the lawsuit, the calculus changes. Tell me which matters more and I'll adjust.
- **Do the DMV step for real** (certified record request) so the § 12952(c)(3) extension notice is truthful.
- **HireRight dispute.** Optional. Dispute only a specific entry that is factually wrong. The report's data is accurate as printed; the "criminal" label is Hertz's.

---

## 10. Evidence to lock down (preservation now; subpoena or discovery later)

1. Hertz/Oracle candidate history for candidate 2847550, req. 43711: status changes, user IDs, timestamps, reason codes.
2. HireRight adjudication library "The Hertz Corporation (Shell) (GL-HTZ001-001) v1.7": the rule for "National Sex Offender Registry" results, "Alcohols related offenses," and "Criminal Information." Also "Managed Adjudication 3.0 (GL-000-003) v10.3."
3. Who at Hertz performed "Client Review" between 2:29 AM and 10:19 AM on Nov. 2; the screens shown; any notes.
4. HireRight NSOR product spec: endpoint (NSOPW API vs. other), raw payload for subrequests 1 and 3, the jurisdiction field, and the California URL or source identifier.
5. Native e-sign records for the Oct. 23 disclosures: screen-by-screen presentation, page boundaries, and timestamps (IP addresses .175, .181, and .13 at 15:03–15:04).
6. The "Employee Confidentiality & Non-Competition" document and its acceptance record.
7. Hertz's written criteria for "Field (Driver Required)" packages and the Manager Trainee job description.
8. ADP WOTC record: employer name and FEIN on Form 8850 / the screening record (HGH vs. Hertz Corp.).
9. **Your side:** screenshots of the Hertz portal status every few days; the certified DMV record; any start-date communications; job-search and mitigation log from today forward.

---

## 11. Do not plead

- A completed rescission, until a final notice exists.
- That the alcohol ground is "false." The DMV entries are real; the *label* is wrong.
- HireRight as a § 290.46 defendant (for now).
- An FCRA count to create federal jurisdiction.
- A seven-year reporting violation.
- Treble or $500 damages under § 432.7, until the current text is read.
- Any dollar total, demand, or prior-matter settlement figure.

---

## 12. Authority status table

| Authority | Use | Status |
|---|---|---|
| Pen. Code § 290.46(j)(1)–(4) | Count 1 | [V-repo] structure; re-read official text before filing |
| *Mendoza v. ADP Screening & Selection Servs.* (2010) 182 Cal.App.4th 1644 | User = employer; anti-SLAPP risk for CRA | [V-repo], [V] |
| *Donaleski v. Wal-Mart Stores* (E.D. Cal. May 8, 2009) 2009 WL 1296257 | Their independent-source defense | [V-repo] |
| *Pastrana v. Local 9509, CWA* (S.D. Cal. 2008) | (j)(3) needs a specific statute | [V-repo] |
| *Lerma v. Amazon.com Servs.* (C.D. Cal. 2023), Dkt. 36 | Source at pleading | [V-repo] |
| AG Op. No. 05-301 (2006) | (j) "unequivocal" | [V-repo] |
| 34 U.S.C. §§ 20921 (NSOR), 20922 (NSOPW); SMART NSOPW/NSOR fact sheet | Source chain | [V] |
| Gov. Code § 12952(a)(3)(A), (c)(1)–(5) | Count 2 | [V-secondary]; read official text |
| 2 CCR § 11017.1 (email receipt rule) | Deadline | [UNVERIFIED]; Hertz's template quotes it |
| Lab. Code § 432.7(a)(1), (c) | Count 3 | [V-secondary]; current remedy text unconfirmed |
| Civ. Code §§ 1786.16(a)(2)(B), 1786.50 | Count 4 | [V-repo] for § 1786.50; read § 1786.16 |
| *Gilberg v. Cal. Check Cashing Stores*, 913 F.3d 1169 (9th Cir. 2019) | Count 4 | [V-secondary] |
| Bus. & Prof. Code § 16600.5(c)–(e) | Count 6 | [V-secondary] |
| *Polo v. Innoventions Int'l*, 833 F.3d 1193 (9th Cir. 2016) | Remand, not dismissal | [V-secondary] |
| *Park v. Bd. of Trustees of Cal. State Univ.* (2017) 2 Cal.5th 1057 | No anti-SLAPP for the hiring decision | [V] |
| *TransUnion LLC v. Ramirez*, 594 U.S. 413 (2021) | Article III | [V-general] |
| *Soo Park v. Thompson*, 851 F.3d 910 (9th Cir. 2017) | Information-and-belief pleading | [UNVERIFIED pin] |
| *Khoja v. Orexigen*, 899 F.3d 988 (9th Cir. 2018) | Incorporation by reference | [UNVERIFIED pin] |
| *Laird v. Capital Cities/ABC* (1998) 68 Cal.App.4th 727 | Integrated enterprise | [UNVERIFIED pin] |
| *White v. Ultramar* (1999) 21 Cal.4th 563 | Managing agent | [UNVERIFIED pin] |
| *Guz v. Bechtel* (2000) 24 Cal.4th 317 | At-will limits | [V-general] |
| *McInerney*, *Parsonage*, *Yeh* (2026) | Cited in PR #1063 | **[UNVERIFIED]**: not reached this session |
| *Kemp v. Superior Court* (2022) | Seven-year measure | [UNVERIFIED pin] |
| Civ. Code § 3513; Evid. Code § 500 | Consent; burden | [V-general]; confirm text |
