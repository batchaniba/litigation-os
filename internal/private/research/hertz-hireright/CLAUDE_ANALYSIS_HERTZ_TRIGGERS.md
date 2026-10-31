# Hertz trigger analysis: FCRA § 1681b(b)(3), Fair Chance Act (Gov. Code § 12952), Penal Code § 290.46

**Matter:** 43 (pre-filing monitoring; no action filed; `claims.json` `counts: []`)
**As of:** Saturday, October 31, 2026 (America/Los_Angeles)
**Branch / base commit reviewed:** `cursor/hertz-hireright-review-2026-10-31` at `c4b2ce0`
**Scope:** Hertz only. Sources are `internal/private/research/hertz-hireright/`, `internal/src/data/matters/43/`, and `internal/docs/matter-43/` (the workshop's `CROSS_MATTER_ASSESSMENT.md` was not used). Nothing here is a claim against HireRight. HireRight shows up only as the source of the report Hertz received.
**Status of every theory below:** **PROSPECTIVE.** Hertz has made no decision (README "Still not in the record"; TIMELINE "Still open").

**Labels:** FACT = printed in a workspace document. USER REPORT = something Brendan said, as recorded in the workspace. INFERENCE = my analysis. LEGAL QUESTION = open law. UNKNOWN = not in the record. **[UNVERIFIED]** = a statute or case I stated from my own knowledge and have **not** checked against a live primary source this session. The CourtListener and Trellis connectors were not authorized, so no live citator check was run. Check every [UNVERIFIED] item against the official code or reporter before relying on it.

**How I read the report:** I read the OCR text (`evidence/ocr/p-NN.txt`) and the forensic review. I did not render the PDF page images. The README says the PDF controls if they disagree.

---

## 0. Bottom line

1. **The claims are about process. They do not attack the merits.** The October 31 report shows Hertz more than a registry line. Page 11 (`evidence/ocr/p-11.txt`; continued on `p-12.txt`) prints a **Santa Clara Superior Court felony record, case C1761642**, under the correctly spelled name "Newanforbi, Brendan Ngehsi":
   - Count 1: sexual penetration by force. Count 2: assault with intent to commit rape.
   - No-contest disposition on Jan 12, 2018. Six-year sentence.
   - Parole/release Dec 2, 2020. Protective order through **1/12/2028**.

   If that record is accurate and belongs to Brendan, California law lets Hertz lawfully decline him **based on the conviction** if it follows three steps:
   - an individualized assessment and the Fair Chance notices (§ 12952(c));
   - the FCRA pre-adverse copy and summary of rights (§ 1681b(b)(3));
   - no reliance on Megan's Law registry information (§ 290.46).

   Hertz's lawful path exists. Brendan's leverage depends on **Hertz skipping a step or citing the registry.**
2. **Three Hertz acts would turn a theory into a real claim:**
   - (a) any adverse step (rescission, a no-start, or an indefinite hold) taken before Hertz gives Brendan the report copy and the CFPB summary and a real chance to respond (**FCRA**);
   - (b) a denial based in whole or in part on conviction history without a written preliminary notice, at least 5 business days to respond (plus 5 more if he disputes accuracy), consideration of his response, and a written final notice (**FCA**);
   - (c) Hertz saying, writing, or coding "registry," "sex offender," "Megan's Law," or "In Registry" as a reason, or its adjudication ruleset flipping the two "In Registry" rows to "Does Not Meet" (**§ 290.46**). Of the three, § 290.46 is the strongest **if** it is triggered, because it does not depend on whether the registry entry is accurate.
3. **Hertz's best defense does not depend on the registry.** Hertz can rest on the conviction (with the FCA process) or on the MVR: a chemical-test-refusal suspension and a DISQ entry on a "Field (Driver Required)" package (`ocr/p-06.txt`, `p-07.txt`; TIMELINE "MVR contents"). Brendan's evidence plan has to force Hertz to name its source.
4. **Next decisive event:** Hertz's decision. There is **no deadline running today.** The Nov. 4 date is a superseded HireRight search ETA (TIMELINE key fact 8).

---

## 1. Facts that matter, labeled

| # | Statement | Label | Source |
|---|---|---|---|
| F1 | The Hertz Corporation offered a full-time Manager Trainee job in Palo Alto (req 43711) at $23/hr. The offer was at-will and contingent on a background/MVR check. | FACT (per workshop summary of the offer letter; offer bytes not on this tree) | `matter.json` key_facts; `evidence.json` e05; MATTER_HISTORY §4 |
| F2 | Offer forecast Oct 22 at 3:38:34 PM PDT; Brendan accepted Oct 22 at 4:49:01 PM; portal confirmation at 5:00:15 PM | FACT | `evidence/messages/2026-10-22_1538_…2e133c.eml`, `…1649…6813d5.eml`, `…1700…ef8932.eml`; TIMELINE key facts 1–2 |
| F3 | Hertz pre-boarding (Gloria Williams) and the HireRight request, Oct 23 at 12:37 PM | FACT | `…dfd6dd.eml`, `…ae64b4.eml` |
| F4 | Consents signed Oct 23, 3:03–3:04 PM. The California disclosure lists "National Sex Offender Registry" among the products. The free-copy box was checked. | FACT | `evidence/attachments/…74fb6e/Other Disclosures and Authorizations.pdf` (California Disclosure page); `evidence.json` e15 |
| F5 | The consent package includes the CFPB "A Summary of Your Rights Under the Fair Credit Reporting Act" | FACT | same PDF (pdftotext shows the heading); `…4d1cb5/Acknowledgement and Authorization.pdf` acknowledges it |
| F6 | The MVR Express report was provided to Gloria Williams / The Hertz Corporation (Estero, FL) on Oct 23 at 3:04:58 PM | FACT | `…78f635.eml`; report p. 15 Activity Log |
| F7 | MVR: Class C, VALID. SUSP for refusing a chemical test (Feb 20, 2025; reinstated May 19, 2026). DISQ labeled "REFUSED TO SUBMIT TO TEST - CMV" on a non-CDL personal license. Jul 2024 registration VIOL. | FACT | report pp. 6–7 (`ocr/p-06.txt`, `p-07.txt`) |
| F8 | Package name: "Field (Driver Required)" | FACT | report p. 3 |
| F9 | Santa Clara #5 "Newanforbi, Brendan Ngehsi": **Court Record Found**, C1761642, completed Oct 30 at 9:10 AM. Labeled "(Past 7 Years Search)." Confirmation line: "Name, Date Of Birth." | FACT | report p. 11 |
| F10 | NSOR subrequest 1 (NEWANFORBI): **In Registry**, Oct 30 11:25 AM. NSOR 3 (Brendan Ngehsi Newanforbi): **In Registry**, Oct 30 12:48 PM. NSOR 2 (Brendan Ngwa): **Not in Registry**, Oct 25 4:16 PM. | FACT | report p. 8; product table p. 4 |
| F11 | Staff notes: "APPLICANT IS LISTED ON THE SEX OFFENDER REGISTRY IN THE STATE OF CA" (Oct 30 at 9:17 AM, Satish Kumar R; 12:45 PM, Kumar Dilip) | FACT | report p. 8 |
| F12 | HireRight note next to each listing line: "Information from the California Sex Offenders' Registry may not be used for employment purposes except to protect a person at risk. See CA Penal Code Section 290.46. Only use this information to make an employment decision as expressly allowed by CA law." | FACT | report p. 8 (9:17 AM), p. 9 (12:46 PM) |
| F13 | Search-source line: "National Sex Offender Registry search performed through the United States Department of Justice" | FACT | report p. 8 |
| F14 | Adjudication ruleset: "The Hertz Corporation (Shell) (GL-HTZ001-001) v1.7." Both "In Registry" rows show **Undefined**. "Not in Registry" shows Meets. MVR shows Undefined. One court row shows Undefined. Widescreen #2 shows **Client Review Required**. Managed Adjudication 3.0 shows **Pending**. | FACT | report pp. 5–6, 15; forensic review §5 row mapping |
| F15 | The Activity Log shows no Hertz "Recipient" or company-user view of the report | FACT (what the log shows) / UNKNOWN (whether Hertz has actually seen it) | report pp. 15–16 |
| F16 | No pre-adverse notice, adverse notice, or Hertz email using the word "registry" was found in the Gmail export | FACT (scope of the search) | `evidence/INDEX.md` lines ~75–77 |
| F17 | Brendan's position is that he has never been on any registry. The workspace cautions that this must be reconciled with C1761642 before anyone claims an identity mismatch. | USER REPORT, recorded secondhand | forensic review §6 flag 2 "Caution for counsel" |
| F18 | No DOB is printed for the registry match ("Verified by Name and DOB"). HireRight's own Santa Clara note says DOB has been removed from court indexes. | FACT | report pp. 3, 8, 11 |
| F19 | No Hertz decision, start date, preliminary notice, individualized assessment, or rescission | UNKNOWN / absent | README; TIMELINE "Still open"; `clocks.json` (4 contingent watches) |

---

## 2. Claim 1: FCRA, 15 U.S.C. § 1681b(b)(3) (pre-adverse action)

### 2.1 Elements (statutory text summarized from my own knowledge, [UNVERIFIED] against the current U.S. Code)
1. Hertz **used a consumer report for employment purposes.** The HireRight report, including MVR Express, is a consumer report from a consumer reporting agency (§ 1681a(d), (f), (h)).
2. Hertz took **"adverse action"** against Brendan. In the employment context that includes "a denial of employment or any other decision for employment purposes that adversely affects any current or prospective employee" (§ 1681a(k)(1)(B)(ii)).
3. The action was **"based in whole or in part on"** the report.
4. **Before** taking the action, Hertz did **not** give Brendan (i) a copy of the report and (ii) the CFPB summary of rights (§ 1681b(b)(3)(A)).
5. **For money damages:** the violation was **willful** (§ 1681n: actual damages, or statutory damages of $100–$1,000, plus punitive damages and fees). Under *Safeco Ins. Co. of Am. v. Burr*, 551 U.S. 47 (2007), "willful" includes reckless disregard. Alternatively, the violation was **negligent** (§ 1681o: actual damages and fees).
6. **For federal standing:** a concrete injury (*TransUnion LLC v. Ramirez*, 594 U.S. 413 (2021); *Spokeo, Inc. v. Robins*, 578 U.S. 330 (2016)). Losing the job is concrete. A bare procedural slip with no lost job is not.

The statute sets **no fixed waiting period** between the pre-adverse notice and the final action. FTC staff guidance and common practice use about **5 business days**. That number is not a statutory requirement ([UNVERIFIED] as to any current agency guidance).

### 2.2 Facts that satisfy elements now
- Element 1 (partly): Hertz ordered the report through HireRight (F3, F4). HireRight furnished the MVR to Hertz (F6). The report is styled "HireRight Report to Hertz" (p. 3). **Use for an employment decision has not happened yet.**
- Element 4 baseline: no pre-adverse packet exists (F16). The CFPB summary Brendan got at consent (F5) is **not** a pre-adverse notice. Hertz will argue it partly satisfies element (ii). The statute ties the duty to the moment "before taking any adverse action." Treat the consent-stage copy as a LEGAL QUESTION Hertz will raise, not as compliance.
- Brendan's copy of the report: he has viewed and printed the report from the HireRight portal (Activity Log pp. 15–16; F15). Hertz will argue that he **already had the report**, so any omission caused no harm. Counter (INFERENCE): the statute puts the duty on "the person intending to take such adverse action." The purpose is a chance to respond **to Hertz** before the decision becomes final. A vendor portal does not do that.

### 2.3 Hertz conduct that would complete the claim
- Any of these, **without** a prior pre-adverse packet from Hertz or HireRight acting for Hertz:
  - a rescission email or call;
  - an Oracle or portal status change to "Withdrawn," "Not Selected," or "Offer Rescinded";
  - Brendan being removed from onboarding;
  - Hertz reposting requisition 43711 or an equivalent Palo Alto Manager Trainee opening and filling it;
  - an indefinite "on hold" that in practice denies the start. This is a weaker version. See Silence, §7.
- A **pre-adverse letter and final action on the same day**, or a final action before any response window closes. That undercuts the "meaningful opportunity" Hertz will claim.
- **Causation hook:** the action must be "in whole or in part" based on the report. Any reason sourced from the MVR, the court record, the registry, or Widescreen satisfies it. Only a reason with no connection to the report defeats element 3, such as the position being eliminated or the Oracle task being incomplete.

### 2.4 Evidence to capture the moment it happens
1. The raw `.eml` of every Hertz or HireRight message (full headers, not a forward). The Date header proves the order of events.
2. Screenshots of the Hertz Careers / Oracle "My Applications" status for 43711, with the system clock visible, **before and after** the change.
3. The HireRight Applicant Center: adjudication status rows (pp. 5–6 equivalents) and the Activity Log. Look specifically for a new "Recipient" row, "Does Not Meet Company Standards," or "Pre-Adverse"/"Adverse" entries. Print to PDF again with a fresh timestamp.
4. Any phone call: written notes the same day (who called, number, time, exact words, whether "report," "background," "registry," or "conviction" was said). Do not record a call without everyone's consent (California is an all-party-consent state, Penal Code § 632 [UNVERIFIED as to current text]).
5. Whether Hertz's notice included **(a)** a full copy of the report and **(b)** the CFPB summary. Keep the envelope or attachment list showing exactly what was enclosed.
6. Any reposting of the Palo Alto Manager Trainee job (save the page with its date).

### 2.5 Deadlines and limitations
- **Statute of limitations (§ 1681p) [UNVERIFIED]:** the earlier of **2 years after Brendan discovers the violation** or **5 years after the violation.** Example: a rescission discovered Nov 6, 2026 means file by **Nov 6, 2028** at the latest. Plan on the 2-year date.
- **Forum:** concurrent jurisdiction (§ 1681p). The federal option is N.D. Cal., because Palo Alto is in Santa Clara County (San Jose Division assignment under Civil L.R. 3-2 [UNVERIFIED]). A state-court FCRA count is also possible.
- **Response timing:** none set by statute. Respond inside whatever window the pre-adverse letter states, or within 5 business days if it states none (§6).

### 2.6 Remedies
- Willful: actual damages **or** $100–$1,000 statutory damages, punitive damages, costs, and fees (§ 1681n). Negligent: actual damages, costs, and fees (§ 1681o).
- Actual damages would be lost wages ($23/hr offered; `damages.json` warns not to value hypothetical wages before a lost start) and emotional distress.
- **Willfulness evidence already in the record (INFERENCE):** Hertz is a national employer using a managed-adjudication product with a Hertz-specific ruleset (F14). HireRight's report itself warns about pre-adverse notice ("final verification of the named individual's identity, are your responsibility," p. 16). Skipping the notice under those conditions supports a "reckless disregard" argument.

### 2.7 Hertz defenses
1. **No adverse action yet** (true today) or **no causal link to the report**: Hertz will say the role was cancelled, the Oracle task was incomplete, or there was no start date and the job was at-will.
2. **Compliance:** a vendor-sent pre-adverse packet, the CFPB summary at consent (F5), or Brendan's portal access (F15).
3. **No concrete injury / harmless error:** Hertz will argue that a response would not have changed the outcome given the conviction. This attacks standing (*TransUnion*) and damages. LEGAL QUESTION: I have not verified current Ninth Circuit authority on § 1681b(b)(3) standing where the report is accurate. **Research required.**
4. **Not willful:** Hertz relied on a vendor process. Negligence-only exposure means actual damages only.
5. **At-will:** this does not defeat FCRA, but it caps the wage damages Hertz will concede.

---

## 3. Claim 2: California Fair Chance Act, Gov. Code § 12952

### 3.1 Elements (from my own knowledge of § 12952 and Cal. Code Regs., tit. 2, § 11017.1; [UNVERIFIED] against current official text, including the Oct. 1, 2023 regulation amendments)
1. **Covered employer:** 5 or more employees. Hertz qualifies (INFERENCE; a national company).
2. Hertz **intends to deny the position "solely or in part" because of conviction history** (§ 12952(c)(1)).
3. **Individualized assessment** of whether the conviction has a "direct and adverse relationship" with the specific duties of the job. Three factors: (i) nature and gravity of the offense; (ii) time since the offense **and** since the sentence was completed; (iii) nature of the job (§ 12952(c)(1)(A)). A written assessment is optional by statute. The regulations add consideration of rehabilitation and mitigation evidence ([UNVERIFIED] as to exact text).
4. **Preliminary decision notice in writing** (§ 12952(c)(2)) that includes:
   - (A) the disqualifying conviction(s);
   - (B) a copy of the conviction history report, if any;
   - (C) an explanation of the right to respond **before** the decision becomes final, the **deadline**, and that the response may include evidence challenging accuracy and/or evidence of rehabilitation or mitigating circumstances.
5. **Response window:** **at least 5 business days.** If Brendan timely notifies Hertz **in writing** that he disputes the report's accuracy and is getting evidence, he gets **5 additional business days** (§ 12952(c)(3)).
6. Hertz **considers** whatever he submits before deciding (§ 12952(c)(4)).
7. **Final decision notice in writing** (§ 12952(c)(5)) that states:
   - (A) the final denial;
   - (B) any procedure to challenge or reconsider;
   - (C) the right to file a complaint with the **Civil Rights Department**.
8. Separately, Hertz may **not** consider certain records at all (§ 12952(a)(3)): arrests without conviction, diversion, and sealed, dismissed, expunged, or statutorily eradicated convictions.
9. **Exceptions (§ 12952(d)):** positions where state, federal, or local law requires a conviction check or bars hiring people with certain convictions; criminal-justice agencies; farm-labor contractors. I am not aware of a law that requires a criminal check, or bars hiring, for a rental-car Manager Trainee. LEGAL QUESTION; Hertz may argue the driving component.
10. **Exhaustion:** a CRD complaint, then a right-to-sue notice, then a civil action (FEHA framework, Gov. Code §§ 12960, 12965).

### 3.2 Facts that satisfy elements now
- The offer is **conditional**, and the check ran after the offer (F2, F3). So the "no pre-offer inquiry" part of the FCA (§ 12952(a)(1)–(2)) is **not** a live theory on this record. No pre-offer question appears in the workspace.
- Hertz now holds, or has access to, **conviction history** (F9), registry results (F10–F11), and the MVR (F7). The duty in elements 3–7 attaches **only if** Hertz moves to deny "solely or in part" because of conviction history.
- No sealed or dismissed status for C1761642 appears anywhere in the workspace. Element 8 has no support right now (UNKNOWN).

**Hard facts for the merits (INFERENCE; this is the weakness):**
- Gravity: two violent sex felonies (p. 11).
- Time:
  - offense Feb 26, 2017 (about 9.7 years ago);
  - disposition Jan 12, 2018 (about 8.8 years ago);
  - release Dec 2, 2020 (about 5.9 years before the Oct 30, 2026 report);
  - protective order **still active through 1/12/2028** (p. 11/12).
- Job: a customer-facing rental branch manager trainee with driving duties (F8).

If the record is accurate and his, a Hertz assessment finding a "direct and adverse relationship" is defensible. The FCA claim's value is then mainly **procedural**. A substantive challenge (that the assessment was a sham, or that rehabilitation was ignored) is possible but uphill.

### 3.3 Hertz conduct that would complete the claim
- **Clearest:** rescission or no-start where conviction history is any part of the reason, with **no** written preliminary notice, **or** no copy of the conviction report, **or** fewer than 5 business days to respond, **or** a final decision before the +5 extension after a written dispute, **or** no written final notice with the CRD-complaint language.
- **Medium:** a written preliminary notice that does not name the specific conviction (just "background check results"), or omits the statement about rehabilitation and mitigation evidence.
- **Registry crossover:** a preliminary or final notice naming **registration status** as the "disqualifying conviction." That is defective under the FCA, because registration status is not a conviction and the notice must identify the conviction. It is also the § 290.46 trigger (§4). LEGAL QUESTION whether a registry citation counts as "conviction history" under the FCA. Either answer helps Brendan: if it does, the FCA process applies; if it does not, § 290.46 bars it.
- **Pretext path:** Hertz cites the MVR only, but the internal record shows the conviction drove the decision. Discovery-dependent; weaker now.

### 3.4 Evidence to capture the moment it happens
1. The preliminary notice itself: date received, delivery method, every attachment, the exact conviction named, the stated deadline, and whether it describes the right to submit accuracy **and** rehabilitation evidence.
2. Proof of when Brendan **received** it (email Date header; mail postmark/envelope). The 5 business days run from that point ([UNVERIFIED] how the regulations treat mailed notices; assume the earliest reasonable date).
3. Brendan's written response and proof of delivery (sent email with headers; certified mail receipt).
4. The final notice: date, whether it mentions reconsideration and the CRD complaint right, and whether the stated reason changed from the preliminary notice.
5. Any written individualized assessment. Ask for it in the response (§6). The statute does not require Hertz to write it, but the request and any refusal are evidence.
6. Whether the timing shows Hertz decided before the window closed, for example a reposted job or onboarding cancelled inside the window.

### 3.5 Deadlines and limitations [UNVERIFIED subdivision numbers; verify before relying]
- **Response window:** at least 5 business days from receiving the preliminary notice, plus 5 more after a timely written dispute notice. Worked examples (weekends excluded; Veterans Day Nov 11 and Thanksgiving Nov 26–27 treated as non-business days to stay conservative):
  - notice received **Mon Nov 2, 2026**: respond by **Mon Nov 9**; extended to **Tue Nov 17**;
  - received **Wed Nov 4**: by **Thu Nov 12** (Wed Nov 11 if Veterans Day counts); extended to **Thu Nov 19**;
  - received **Mon Nov 9**: by **Tue Nov 17**; extended to **Tue Nov 24**.

  **Always use the date stated in the notice if it is later. Always send the dispute notice on day 1 or 2, not day 5.**
- **CRD complaint:** within **3 years** of the unlawful practice (Gov. Code § 12960(e), as amended by AB 9 effective 2020).
- **Civil action:** within **1 year** of the CRD right-to-sue notice (Gov. Code § 12965(c)(1)(C) [verify subsection numbering after the 2022 recodification]). Requesting an immediate right-to-sue is available.
- Practical rule: if a FCRA case is filed, ask for the CRD right-to-sue early so the FCA and FCRA claims can be joined.

### 3.6 Remedies
FEHA remedies (Gov. Code § 12965) [UNVERIFIED as to the current fee/cost subdivision]:
- back pay and front pay (or instatement);
- emotional-distress damages;
- punitive damages under Civ. Code § 3294 if malice, oppression, or fraud is shown;
- reasonable attorney's fees and costs to a prevailing plaintiff (as a self-represented litigant Brendan generally cannot recover attorney's fees; costs are recoverable);
- injunctive relief.

CRD can also pursue FCA enforcement on its own.

### 3.7 Hertz defenses
1. **The decision was not based on conviction history:** MVR (refusal suspension, DISQ "CMV"), the Oracle task, position cancellation, at-will. The MVR is Hertz's best clean alternative. The adjudication ruleset name says "Excl. MVR" and the MVR row is "Undefined" (p. 5), so Hertz may adjudicate the MVR manually.
2. **Full compliance:** documented assessment, both notices, 5+5 days honored, response considered.
3. **Direct and adverse relationship on the merits:** gravity, time since release under 6 years, the active protective order, customer contact, driving. Strong for Hertz if the record is his.
4. **The § 12952(d) exception:** Hertz may argue driving or insurance requirements. Probably weak absent a legal mandate (LEGAL QUESTION).
5. **Harmless / same decision anyway:** limits damages even where the process was defective.
6. **Failure to exhaust or untimely CRD filing.**
7. **Brendan's response was untimely or did not dispute accuracy in writing** (defeats the +5 extension).

---

## 4. Claim 3: Penal Code § 290.46 (employment use of Megan's Law information)

### 4.1 Statutory structure (from my own knowledge; [UNVERIFIED], including **subdivision lettering**)
Section 290.46 creates the California DOJ's public Megan's Law internet website and limits how its information may be used.

- **Subd. (j)(1):** a person is authorized to use information disclosed under § 290.46 **only to protect a person at risk.**
- **Subd. (j)(2):** except as authorized by (j)(1) or other law, use of that information "for purposes relating to" a list of activities is **prohibited.** The list includes **employment** (along with health insurance, insurance, loans, credit, education, housing, and business-establishment benefits).
- **Subd. (j)(3):** preserves access and use under other specified statutes.
- **Civil liability subdivision:** any use for purposes other than (j)(1), or in violation of (j)(2), makes **"the user"** liable for:
  - actual damages, and an amount set by the jury or court of up to **three times** actual damages, but **not less than $250**;
  - **attorney's fees**;
  - **exemplary damages**, or a **civil penalty up to $25,000**.

  A related provision lets the AG, a DA, a city attorney, **or any person aggrieved** seek **injunctive relief** against a **pattern or practice** of misuse.
- **Criminal-enhancement subdivision:** extra fines or prison time for using the information to **commit** a misdemeanor or felony. This is not relevant to an employment decision.

**Lettering caution:** the request refers to subdivisions **(j) and (l)**. In the versions I remember, the civil "user liable" provision is lettered **(k)**, and **(l)** covers the criminal-use enhancements. The lettering has changed with amendments. **Verify against the current official Penal Code before citing either letter in any paper.** The substance above is what matters. The exact amounts and letters are [UNVERIFIED].

### 4.2 Elements (as I would chart them)
1. **"Information disclosed pursuant to this section":** the registry information Hertz used came from California's § 290.46 Megan's Law disclosure.
2. **"Use":** Hertz **used** that information.
3. **Prohibited purpose:** the use was for a purpose **"relating to employment"** (or otherwise not "to protect a person at risk").
4. **No other legal authorization** (subd. (j)(3) / "any other provision of law").
5. **Damages:** actual damages (any amount; the $250 floor applies once liability exists), with treble/exemplary damages or a civil penalty available.

### 4.3 Facts that satisfy elements now
- **Element 1 (contested source):**
  - *For Brendan:* the HireRight staff notes say "THE SEX OFFENDER REGISTRY IN THE STATE OF CA," and HireRight itself attached the § 290.46 warning to those exact lines, describing the information as "Information from the California Sex Offenders' Registry" (F11, F12). That is the vendor's own characterization, delivered to Hertz.
  - *Against Brendan:* the search-source line says the search ran "through the United States Department of Justice" (F13), meaning the federal NSOPW portal.
  - LEGAL QUESTION: is California registrant information obtained through NSOPW, which pulls from state sites, "information disclosed pursuant to" § 290.46? I know of no appellate authority answering this. **Research required.** (INFERENCE: HireRight's own § 290.46 label makes it hard for Hertz to say it did not know the information was California Megan's Law information.)
- **Element 2:** **not yet.** Both "In Registry" rows are "Undefined" in the Hertz ruleset (F14). There is no Hertz decision (F19), and no proof Hertz has even opened the report (F15).
- **Element 3:** the context is employment by definition: a post-offer screen for req 43711 (F3, F8). There is no stated "person at risk."
- **Element 4:** no statute in the workspace authorizes a rental-car employer to use Megan's Law information. LEGAL QUESTION whether any (j)(3) carve-out could apply. None is apparent.
- **Accuracy does not matter.** Element 1 turns on the source, not truth. This claim **survives even if C1761642 and the registration are his.** That makes it the most robust of the three **once triggered** (INFERENCE).

### 4.4 Hertz conduct that would complete the claim
In rough order of strength:
1. A written notice (preliminary, final, or email) citing **"registry," "sex offender registration," "Megan's Law," "In Registry,"** or quoting the "APPLICANT IS LISTED…" line as a reason.
2. A recruiter or manager saying so orally. This needs same-day notes and, ideally, a later written confirmation.
3. Hertz's **adjudication ruleset** turning either "In Registry" row into **"Does Not Meet Company Standards,"** followed by an adverse action. INFERENCE: the ruleset is "The Hertz Corporation (Shell)" (p. 5), meaning Hertz's own criteria applied to the registry result. Hertz will argue that a vendor rule is not Hertz's "use," and that the court record was the real basis.
4. A preliminary FCA notice that lists the **registry entry** as the "conviction." That is both an FCA defect and a § 290.46 use.
5. A pattern-or-practice signal: Hertz standard language or ruleset logic that disqualifies registrants across the board. This would support injunctive relief as a "person aggrieved."

**What does NOT complete it:** a decision based on **court record C1761642** through the FCA process, with no registry reference. Conviction history from court records is not § 290.46 information. **This is Hertz's main escape route.** The registry hit came 7 minutes after the court hit (forensic review §3.3), and Hertz will say the court record is what it used.

### 4.5 Who can be liable as a "user"
- **Hertz (The Hertz Corporation):** the requesting employer and decision-maker (F1, F3; report p. 3 "Requested By: Gloria Williams, Hertz – Pre Employment (Field)"). This is the primary "user" if registry information enters the decision. **Hertz Global Holdings, Inc.** is the ADP WOTC entity (`matter.json`). Which entity is the proper defendant is UNKNOWN (`parties.json`; workshop H43-R07). Name both only after the decision document shows who acted.
- **Individual Hertz employees** (e.g., Gloria Williams or a decision-maker): the statute says "the user." LEGAL QUESTION whether an individual acting for an employer is personally a "user." Not recommended without authority.
- **HireRight:** arguably a "user" when it furnishes the information for an employment purpose (forensic review §6 flag 3). **Out of scope. Brendan will not sue HireRight.** It matters here only because Hertz may **blame the vendor** ("HireRight put it in; we didn't use it"). The answer is Hertz's own decision documents.

### 4.6 Evidence to capture the moment it happens
- Every word Hertz uses to describe the reason. **Ask Hertz in writing to identify the specific record(s) and source(s) it relied on** (§6). A written answer naming the registry completes element 2. A written answer naming only C1761642 closes off § 290.46 but locks Hertz into the FCA conviction analysis.
- HireRight Applicant Center adjudication rows for the three NSOR subrequests, before and after the decision (re-print with timestamp).
- Any later or revised version of the report delivered to Hertz (version number and print time).
- Oral statements: same-day notes, then a confirming email Brendan drafts for review ("Confirming our call today at __, you said ___").

### 4.7 Deadlines and limitations (LEGAL QUESTION)
- § 290.46 has **no internal limitations period** that I know of [UNVERIFIED].
  - The candidates are CCP § 338(a): **3 years** for "a liability created by statute, other than a penalty or forfeiture."
  - And CCP § 340(a): **1 year** for an action on a statute "for a penalty or forfeiture." This could govern the civil-penalty or exemplary-damages portion.
- **Plan on 1 year from the date of the prohibited use**, meaning the date the registry-based decision is communicated. Example: use communicated Nov 6, 2026 means file by **Nov 6, 2027**.

### 4.8 Remedies
- Actual damages (lost wages, emotional distress);
- up to treble actual damages, with a **$250 minimum**;
- **attorney's fees** (a pro se litigant generally cannot recover attorney's fees; costs only);
- **exemplary damages or a civil penalty up to $25,000**;
- injunctive relief for a pattern or practice;

all [UNVERIFIED] as to amounts and current subdivision. **Notice evidence:** HireRight's warning sat directly next to the listing (F12). If Hertz used the information anyway, that supports exemplary damages and the willfulness theme in the FCRA count (INFERENCE).

### 4.9 Hertz defenses
1. **No use:** Hertz relied on the court record, the MVR, or a neutral reason. The strongest defense.
2. **The source was not § 290.46:** NSOPW (US DOJ), not the CA DOJ website. LEGAL QUESTION.
3. **"To protect a person at risk":** customers or co-workers. INFERENCE in response: employment is expressly listed in (j)(2) as prohibited, so a generic workplace-safety rationale should not swallow the employment bar. [UNVERIFIED] whether "person at risk" is defined, and how courts read it.
4. **Authorized by other law:** (j)(3). Hertz would need a specific statute. None is evident.
5. **Vendor attribution:** HireRight's ruleset, not Hertz. Answer: Hertz configured and owns "The Hertz Corporation (Shell)" ruleset and makes the hiring decision.
6. **Statute of limitations** (§ 340(a) one-year argument).

---

## 5. Source split: which record Hertz uses decides which claim exists

| Record | Where | Lawful for Hertz to use? | Claim(s) it triggers if used without process |
|---|---|---|---|
| (a) Santa Clara court record C1761642 | p. 11–12 | **Yes**, after the FCA assessment and notices, plus FCRA pre-adverse | FCRA; FCA |
| (b) NSOR "In Registry," US DOJ source line | p. 8, p. 4 | **No** for employment if it is § 290.46 information (LEGAL QUESTION on the NSOPW route) | § 290.46; FCRA (it is still part of the consumer report); FCA if treated as conviction history |
| (c) Staff notes "LISTED…STATE OF CA" plus the § 290.46 warning | pp. 8–9 | **No** (HireRight's own label says so) | § 290.46; FCRA |
| (d) Widescreen #2 "Data found… see Sex Offender" / Client Review Required | pp. 6, 9 | Depends on what it points to | FCRA; § 290.46 if it points to the registry |
| (e) MVR SUSP/DISQ/VIOL | pp. 6–7 | **Yes**, after FCRA pre-adverse. These are not FCA conviction history (an administrative refusal suspension is not a conviction; INFERENCE) | FCRA only |

**Practical rule:** every communication Brendan sends after a notice should **ask Hertz to identify the specific record and its source.** Make Hertz choose a row in this table in writing.

---

## 6. How to respond to a pre-adverse or preliminary notice so all three claims are preserved

**Only after a notice arrives. Do not contact Hertz now** (README "What not to do"). **Draft only; Brendan reviews before anything is sent.** Finished correspondence should follow the repository's standing email-close lock. Put no repo or GitHub URLs in it.

**Day 0 (the day it arrives):**
1. Preserve everything listed in §§2.4, 3.4, and 4.6. Save the raw `.eml` and re-print the HireRight portal.
2. Calendar the response date: the later of the notice's stated deadline or 5 business days from receipt (§3.5 examples). Calendar the +5 date as well.
3. Do not call. Do everything in writing to the sender of the notice, copying the address Hertz designates.

**Day 1–2 (short written notice; this preserves the +5 extension and the record):**
- "I received your notice dated __ on __. I am responding before the decision becomes final."
- **Only if true:** "I dispute the accuracy of the report and am obtaining evidence. Under Gov. Code § 12952(c)(3), please allow the additional five business days." State that he disputes accuracy **only** where there is a real, good-faith accuracy issue. The workspace identifies these candidates (forensic review §6), each of which can be disputed without asserting the conviction is someone else's:
  - the "Past 7 Years Search" label versus 2017–2018 dates;
  - the Count 2 sentence duplicated word for word;
  - the "REFUSED TO SUBMIT TO TEST - CMV" DISQ on a non-CDL personal license;
  - name-variant matching ("Ngwanforbi" vs. "Newanforbi" vs. "Nforbi");
  - "Verified by Name and DOB" with no DOB shown.

  **Do not assert the conviction belongs to someone else unless the court file proves it** (forensic review flag 2 caution). A false identity dispute would damage every claim and his credibility.
- Request the following:
  - (a) a **complete copy** of every consumer report and version Hertz relied on;
  - (b) the **CFPB Summary of Rights** if it was not enclosed;
  - (c) **identification of each specific record and its source** Hertz considered (court record, registry, MVR, other);
  - (d) any **individualized assessment**, written or not;
  - (e) confirmation that **no decision is final** until his response is considered.
- **§ 290.46 objection, stated neutrally:** "The HireRight report sent to Hertz states, next to the registry entries, that 'Information from the California Sex Offenders' Registry may not be used for employment purposes except to protect a person at risk. See CA Penal Code Section 290.46.' I object to any use of registry information in this employment decision and ask that it be excluded from consideration." This puts Hertz on written notice and supports exemplary damages and willfulness if Hertz uses it anyway. It does not admit that the registry entry is accurate.

**By the deadline (substantive response):**
- **Accuracy:** the specific errors, with documents (court docket or abstract for C1761642 if it helps; DMV printout for the MVR items).
- **Rehabilitation and mitigation:** what Brendan can document, such as completion of parole or supervision, time since release, employment history, training, licenses, and references. Make no admissions beyond what is necessary. The FCA lets him submit this evidence and does not require him to give any particular form of it ([UNVERIFIED] as to the regulation text).
- **Job fit:** the Manager Trainee duties, a valid Class C license (p. 6), and the reinstatement of the 2025 suspension (p. 7).
- **Process reservation:** "Please send any final decision in writing, including any procedure to request reconsideration and notice of my right to file a complaint with the Civil Rights Department (Gov. Code § 12952(c)(5))."
- Make no threats and name no claims or settlement terms. A calm record is worth more.

**Before anything is sent:** run the litigation-legal / verification-foundation pass and an Apodictic stress test on the response, per Brendan's standing instructions.

---

## 7. Decision matrix

**Score scale (0–100):** my judgment of the chance of establishing liability on that claim, discounted for remedy value and Hertz's best defense, **given that scenario occurs**. These are not probabilities that the scenario will occur. Branch A assumes C1761642 and the registration are accurately attributed to Brendan. Branch B assumes the court file proves they are not his (UNKNOWN today). Scores are for Branch A unless noted.

| Outcome | FCRA § 1681b(b)(3) | FCA § 12952 | PC § 290.46 | Overall | Brendan's action |
|---|---|---|---|---|---|
| **1. Hire** (start date set, onboarding completes) | 0 | 0 | 0 (no use alleged) | **0** | Start work. Keep the packet. Nothing to pursue. A registry use that surfaces later would still be § 290.46 (low likelihood). |
| **2. Pre-adverse / preliminary notice received, no final decision yet** | 5 (no adverse action yet) | 5 (process under way) | **5, or 40 if the notice cites the registry** (a written prohibited-purpose use may already be a "use"; LEGAL QUESTION whether a preliminary decision is enough) | **10, or 40 with a registry citation** | Follow §6 exactly. Day-1 dispute and request letter. § 290.46 objection. Calendar the dates. |
| **3a. Rescission with full process, conviction-only reason (court record), no registry reference** | 5 | 15 (substantive challenge only; sham assessment or ignored rehabilitation) | 5 | **10–15** | Branch A: little leverage. Evaluate whether the assessment actually addressed the time since release and his rehabilitation evidence. Consider a CRD intake only if the record shows a perfunctory assessment. |
| **3b. Rescission with process, but the notice or reason cites the registry** | 10 | 35 (registration is not "a conviction"; the notice is defective as to identifying the conviction) | **60** | **55–60** | Strongest process-compliant scenario for Brendan. Preserve. Calendar the 1-year § 290.46 date. CRD intake within 3 years (sooner is better). |
| **3c. Rescission with process, MVR-only reason** | 5 | 10 (pretext only) | 5 | **5–10** | MVR accuracy points (CMV label) may support a reconsideration request, not a claim. |
| **4a. Rescission without process, no reason given or "background"** | **65** (adverse action plus no pre-adverse packet; damages limited by the same-decision argument) | **55** (no preliminary notice, no 5 days, no final notice, if conviction history played any part; Hertz will say it did not) | 15 (needs proof the registry was used) | **60** | Preserve. Write promptly asking for the reason, the records relied on, and the report copy (that answer fixes which claims exist). FCRA SOL is 2 years from discovery. CRD within 3 years. |
| **4b. Rescission without process, registry cited** | **70** | **60** | **70** | **75** | Best scenario. Preserve everything. Draft the CRD intake and FCRA/§ 290.46 complaint outline for review. Do not send anything to Hertz beyond preservation and a request for the reason without review. |
| **5. Silence** (no decision; onboarding stalls; adjudication stays Pending) | 10 now, rising to 50 if a start date passes or 43711 is reposted and filled | 10, rising to 45 on the same trigger | 5 (rising only with proof of registry use) | **10 now; 40–50 once silence becomes a de facto rescission** | Keep working the Oracle task and portal (`clocks.json` 43-watch-onboarding). Re-print HireRight status weekly. Silence is not yet adverse action. Do not create a deadline. Treat a reposting or a lapsed start as Outcome 4a. |

**Branch B (record proven not his):** add about **+15** to every FCRA and FCA number in rows 3–5. The accuracy dispute becomes the centerpiece, the "same decision anyway" defense collapses, and wage damages become realistic. § 290.46 scores do not change, because that claim never depended on accuracy.

**Factors that move every score:** whether Hertz's written reason names its source; whether Hertz's ruleset flips the NSOR rows; whether there is a dated reposting of req 43711; whether Brendan can document a lost start date. The last one matters because there is no start date in the record today (`damages.json`; README "Still not in the record").

---

## 8. Adjacent Hertz-side items (not requested; flagged only)

- **ICRAA copy obligation (Civ. Code § 1786.16(b)(1)) [UNVERIFIED]:** when an applicant checks the copy box (F4), the recipient employer must send a copy of the report within **3 business days** of receiving it. The MVR Express went to Hertz on Oct 23 (F6). Brendan got portal access through HireRight. LEGAL QUESTION whether vendor delivery satisfies Hertz's duty. Low value on its own. Note it if a claim is ever filed (ICRAA remedies § 1786.50; SOL § 1786.52 [UNVERIFIED]; constitutionality as applied to criminal-record reports upheld in *Connor v. First Student, Inc.*, 5 Cal.5th 1026 (2018) [UNVERIFIED pin and holding wording]).
- **ICRAA adverse-action notice (Civ. Code § 1786.40) [UNVERIFIED]:** a parallel state notice duty if Hertz acts on an investigative consumer report.
- **FCRA post-adverse notice (§ 1681m(a)) [UNVERIFIED]:** after any final action, Hertz must give the CRA's contact information, a statement that the CRA did not make the decision, and notice of the free-copy and dispute rights. Usually enforced only by regulators, so not a private claim (LEGAL QUESTION). Preserve the notice anyway.
- **Consent forms:** the California package includes a **City of Los Angeles** Fair Chance (FCIHO) notice (`Other Disclosures and Authorizations.pdf`). The job is in Palo Alto, so that ordinance does not apply. I identified no Palo Alto or Santa Clara County private-employer fair-chance ordinance in the workspace (UNKNOWN / research required). The FCRA § 1681b(b)(2) "standalone disclosure" form was not analyzed here.

---

## 9. Five things to get without contacting Hertz

1. **The Santa Clara Superior Court file for C1761642** (docket, abstract of judgment, defendant identifiers). This decides Branch A vs. Branch B for every score above (forensic review flag 2).
2. **A fresh HireRight Applicant Center print** every few days: watch the NSOR adjudication rows, Managed Adjudication status, and new Activity Log "Recipient" rows (F14, F15).
3. **Hertz Careers / Oracle status for 43711** and completion of the Oracle additional-information task. This removes Hertz's "incomplete onboarding" defense (`clocks.json` 43-watch-onboarding; `evidence.json` e10).
4. **The native or certified HireRight consumer file** under the copy election and a consumer file request. This is a consumer's own records request, not a claim against HireRight. It identifies the actual registry source (NSOPW vs. CA DOJ), which is the key § 290.46 element-1 fact (forensic review §7).
5. **A DMV record printout** to test the "REFUSED TO SUBMIT TO TEST - CMV" DISQ on a non-CDL license and the reinstatement (p. 7). This blunts Hertz's MVR alternative.

---

## 10. Uncertainty register

- Every statute paraphrase is from my own knowledge and is [UNVERIFIED] against current official text. This especially applies to the § 290.46 subdivision letters, the FEHA § 12965 subsection numbering, and the 2023 amendments to 2 CCR § 11017.1.
- The case citations (*Safeco*, *TransUnion*, *Spokeo*, *Connor*) are real decisions as I know them. They were **not** checked through a citator this session. Run the citation-verify funnel before use.
- No authority located on (i) NSOPW-sourced California data as "information disclosed pursuant to" § 290.46; (ii) whether an employer acting on a vendor ruleset "uses" the information; (iii) § 1681b(b)(3) standing where the report is accurate. All three are open research items.
- I did not render the PDF page images. OCR-dependent details such as the alias list on NSOR #1 should be confirmed against the PDF (TIMELINE note at Oct 30, 11:25 AM).
- I did not attempt to reconcile Brendan's recorded position (F17) with C1761642. Only the court file can do that.
- Scores are judgment calls on a pre-decision record and should be re-run the day Hertz acts.

*Private working analysis. Not a pleading, not a demand, not legal advice to any third party. Nothing here is to be filed, served, or sent without Brendan's review.*
