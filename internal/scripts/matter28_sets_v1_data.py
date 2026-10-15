"""Matter 28 discovery sets v1 -- single source of truth for the .md and .pdf renders.
Claims assumed live: 42 U.S.C. 1983 (First Amendment retaliation; Fourteenth Amendment due process)
against HOPE (Monell/Tsao) and Smith (individual/supervisory); Bane Act (Civ. Code 52.1).
Fraud and RICO assumed dismissed; their theories are not pursued.
Items tagged note= carry internal notes that are stripped from service renders.
"""

HOPE = "HOPE"
SMITH = "SMITH"

PARTY_NAME = {
    HOPE: "HOPE PSYCHOTHERAPY, INC. (d/b/a HOPE PROGRAM)",
    SMITH: "SHANNON SMITH, LCSW",
}

# ---------------------------------------------------------------- shared text
DEFS_COMMON = [
    ('"PLAINTIFF"', "Brendan Ngehsi Newanforbi."),
    ('"HOPE"', "Defendant HOPE Psychotherapy, Inc. (d/b/a HOPE Program, appearing as HOPE Program, A Licensed Clinical Social Worker Professional Corporation), including its officers, employees, and agents, and any management or records contractor acting for it."),
    ('"SMITH"', "Defendant Shannon Smith, LCSW."),
    ('"CDCR"', "the California Department of Corrections and Rehabilitation, including its Division of Adult Parole Operations (DAPO) and any parole agent or supervisor."),
    ('"CTM"', "a Containment Team Meeting or similar case conference among a treatment provider, CDCR, and/or a polygraph examiner concerning a parolee."),
    ('"COMPLETION DETERMINATION"', "any recommendation, decision, or report about whether a parolee has completed, graduated from, or may be discharged or titrated from sex-offender treatment, including any statement that the parolee has not completed treatment."),
    ('"SAN JOAQUIN ACTION"', "Newanforbi v. Palacios et al., San Joaquin County Superior Court, in which HOPE was a party."),
    ('"STOCKTON SITE"', "HOPE's Stockton, California treatment location."),
    ('"DOCUMENT"', "has the full meaning of Fed. R. Civ. P. 34(a)(1)(A), including electronically stored information (ESI) such as email, text and app-based messages, EHR entries, audit logs, and audio or video recordings."),
    ('"COMMUNICATION"', "any transmission of information by any means, including email, text or app message (on any device, including a personal device used for work), letter, portal message, and recorded meeting."),
    ('"IDENTIFY"', "(a) for a person: full name, last known employer, title, and business contact; (b) for a DOCUMENT: type, date, author, recipients, and Bates number if produced."),
    ('"RELEVANT PERIOD"', "January 1, 2021 to the date of response, unless a request states otherwise."),
]

INSTR_ROG = [
    "Answer each interrogatory separately and fully in writing under oath (Fed. R. Civ. P. 33(b)(3)), within 30 days after service.",
    "Answer on all information available to you, including information held by your employees, agents, attorneys, and contractors. If you cannot answer fully after reasonable inquiry, answer to the extent possible and state what you did to obtain the rest.",
    "State every objection with specificity (Rule 33(b)(4)); answer any part not objected to. A privilege claim must be made as Rule 26(b)(5)(A) requires.",
    "If you rely on Rule 33(d), specify the records by Bates number in enough detail for Plaintiff to locate them as readily as you could.",
    "These interrogatories are continuing to the extent required by Rule 26(e).",
]
INSTR_RFA = [
    "Each matter is admitted unless, within 30 days after service, you serve a written answer or objection signed under Rule 26(g) (Fed. R. Civ. P. 36(a)(3)).",
    "A denial must fairly respond to the substance of the matter; when good faith requires, specify the part admitted and qualify or deny only the rest (Rule 36(a)(4)).",
    "You may assert lack of knowledge only if you state that you have made reasonable inquiry and that the information you know or can readily obtain is insufficient (Rule 36(a)(4)).",
    "A party that fails to admit a matter later proved may be ordered to pay the reasonable expenses of proof (Rule 37(c)(2)).",
]
INSTR_RFP = [
    "Respond in writing within 30 days after service (Fed. R. Civ. P. 34(b)(2)(A)) and produce at a reasonable time and place agreed by the parties, or by secure electronic transfer.",
    "For each objection, state whether any responsive materials are being withheld on the basis of that objection (Rule 34(b)(2)(C)), and permit inspection of the rest.",
    "Produce documents as kept in the usual course of business or organized and labeled to correspond to the request (Rule 34(b)(2)(E)(i)), with Bates numbers.",
    "Produce ESI in native format with metadata intact for email, spreadsheets, EHR exports, audit logs, and recordings; other ESI may be produced as searchable PDF. Produce recordings in their original file format.",
    "These requests reach documents in your possession, custody, or control, including documents you have the legal right to obtain on demand from employees, contractors, and vendors (including EHR, email, and cloud-storage vendors), and work-related messages on personal devices or accounts.",
    "Withhold nothing on a claim of privilege without serving a privilege log that meets Rule 26(b)(5)(A) with your written response.",
    "Confidential material may be designated under the Stipulated Protective Order once entered; confidentiality is not a basis to withhold. Records of other clients may be produced de-identified where a request so states.",
    "If responsive material no longer exists, identify what existed, its former custodian, when and why it became unavailable, and any available copy.",
    "Preserve parent-attachment relationships and produce metadata sufficient to identify the author, custodian, and creation, modification, and transmission dates of each item.",
    "Where third-party information is protected, redact it rather than withhold an otherwise responsive document.",
    "These requests are continuing to the extent required by Rule 26(e).",
]

# ---------------------------------------------------------------- HOPE ROGs
# 21 served, 4 reserved. Each is a single primary question; listed details are
# subsumed in it (Kendall, 174 F.R.D. at 685-86; Safeco, 181 F.R.D. 441).
HOPE_ROGS = [
    dict(t="IDENTIFY each person who participated in making, approving, or communicating any COMPLETION DETERMINATION concerning PLAINTIFF during the RELEVANT PERIOD, stating for each the determination(s) and date(s) involved and the person's role.", c=["1983-HOPE", "1983-SMITH", "DP"]),
    dict(t="For each CTM concerning PLAINTIFF during the RELEVANT PERIOD, state the date, the COMPLETION DETERMINATION HOPE communicated to CDCR at that CTM, and each reason HOPE gave for not recommending completion.", c=["1983-HOPE", "DP", "STATE"]),
    dict(t="Describe each policy, practice, or custom (written or unwritten) that governed whether a parolee at the STOCKTON SITE could receive a favorable COMPLETION DETERMINATION while on active parole supervision, stating the period each was in effect.", c=["1983-HOPE", "MONELL", "DP"]),
    dict(t="Describe the change to HOPE's treatment-completion or aftercare policy that HOPE has stated occurred in or about October 2024, including what changed, the effective date, and who approved it.", c=["MONELL", "STATE"], note="Matter 5 FROG 17.1 / SROG 7."),
    dict(t="IDENTIFY each contract term, CDCR directive, guideline, or other CDCR requirement that HOPE contends required, limited, or influenced any COMPLETION DETERMINATION concerning parolees during the RELEVANT PERIOD.", c=["STATE", "MONELL"], note="Targets the contract-guideline basis seen at HOPE_000294 without disclosing it."),
    dict(t="Describe each way in which CDCR participated in, reviewed, approved, or could override a COMPLETION DETERMINATION by HOPE concerning a parolee during the RELEVANT PERIOD (including through CDCR Form 3043, CTMs, CDCR's ARMS system, or any titration form).", c=["STATE"]),
    dict(t="State all facts supporting HOPE's contention that it did not act under color of state law with respect to the COMPLETION DETERMINATIONS concerning PLAINTIFF.", c=["STATE"], note="Contention ROG on Dkt 15/30 defense."),
    dict(t="State all facts supporting any contention by HOPE that each COMPLETION DETERMINATION concerning PLAINTIFF was an individualized clinical judgment rather than the application of a HOPE policy, practice, or custom.", c=["MONELL", "DP"], note="Matter 5 SROG 12."),
    dict(t="State all facts supporting any contention by HOPE that PLAINTIFF had an adequate procedure (including any CDCR grievance or appeal) to challenge HOPE's COMPLETION DETERMINATIONS or HOPE's reports to CDCR about him.", c=["DP"], note="Dkt 30 §III relies on 15 CCR §§3482, 3484."),
    dict(t="For each year from 2021 through 2026, state the number of parolee clients at the STOCKTON SITE who received a favorable COMPLETION DETERMINATION while still on parole supervision (de-identified counts only).", c=["MONELL", "DP"], note="Matter 5 SROG 6 (objected). Count-only; Jaffee-safe."),
    dict(t="IDENTIFY each complaint, grievance, objection, or request PLAINTIFF made to HOPE (orally or in writing) during the RELEVANT PERIOD concerning his treatment, completion, schedule, homework, or HOPE's reports to CDCR, stating the date and the HOPE recipient of each.", c=["FA"]),
    dict(t="Describe each statement made by Katie Palacios or any other HOPE employee to CDCR between January 1, 2025 and the present characterizing PLAINTIFF's behavior, attitude, participation, or complaints (including any use of the words \"disruptive\" or \"ringleader\"), stating the speaker, date, and recipient.", c=["FA", "BANE"], note="Palacios RFA 11/12/16 (Matter 5) -- not binding here."),
    dict(t="State all facts supporting any contention by HOPE that it would have taken the same actions concerning PLAINTIFF (including its statements to CDCR about him) in the absence of his complaints, grievances, or lawsuits.", c=["FA"], note="Mt. Healthy same-decision defense; Nieves causation. Reworded Oct 14 from the #1001 draft ROG 18."),
    dict(t="State all facts supporting any contention by HOPE that it did not threaten, intimidate, or coerce PLAINTIFF within the meaning of California Civil Code section 52.1.", c=["BANE"]),
    dict(t="Describe how and when HOPE first learned of In re Dwyer (San Joaquin County Superior Court habeas proceeding) and of the April 17, 2025 amendments to Cal. Code Regs., tit. 15, section 3574, and state what HOPE did in response to each.", c=["MONELL", "DP"], note="Discrete-subpart risk: Dwyer vs. regulation could count as 2. Budgeted as 2."),
    dict(t="IDENTIFY each officer, director, or managing agent of HOPE with final authority over HOPE's treatment-completion policies during the RELEVANT PERIOD, stating the period of that authority.", c=["MONELL", "1983-SMITH"]),
    dict(t="Describe SMITH's role in adopting, approving, enforcing, or changing HOPE's treatment-completion policies for parolees during the RELEVANT PERIOD.", c=["1983-SMITH", "MONELL"]),
    dict(t="IDENTIFY each recording (audio or video) of a CTM or group session involving PLAINTIFF made during the RELEVANT PERIOD, stating its date, custodian, current location, and, if it no longer exists, when and why it was deleted or overwritten.", c=["FA", "PRESERVATION"], note="Matter 5 FROG 12.4: CTMs are video recorded."),
    dict(t="IDENTIFY each electronic system HOPE used during the RELEVANT PERIOD to create or store information about PLAINTIFF or about COMPLETION DETERMINATIONS (including EHR, email and archive accounts, messaging platforms, cloud drives or internal websites, and any CDCR system HOPE accessed), stating for each its custodian and retention setting.", c=["ESI"]),
    dict(t="State the date HOPE first anticipated litigation by PLAINTIFF, and describe each litigation-hold or preservation step HOPE has taken (date, scope, and recipients, but not privileged content).", c=["ESI", "PRESERVATION"]),
    dict(t="IDENTIFY each insurance policy (including any excess or umbrella policy) under which an insurer may be liable to satisfy all or part of a judgment against HOPE or SMITH in this action, and state each insurer's coverage position (including any reservation of rights).", c=["INSURANCE"], note="26(a)(1)(A)(iv) overlap is intentional: the coverage-position part may draw an objection; RFP 34-35 back it up."),
]
HOPE_ROG_RESERVED = 4
HOPE_ROG_COUNT_NOTE = "21 numbered; counted conservatively as 22 (No. 15 may be treated as two). Reserve: 3."

# ---------------------------------------------------------------- SMITH ROGs
SMITH_ROGS = [
    dict(t="Describe each position you have held with HOPE during the RELEVANT PERIOD, stating the dates and your duties regarding clinical policy, the STOCKTON SITE, and HOPE's relationship with CDCR.", c=["1983-SMITH"]),
    dict(t="Describe your role in drafting, approving, enforcing, or changing any HOPE policy, practice, or custom governing COMPLETION DETERMINATIONS for parolees during the RELEVANT PERIOD.", c=["1983-SMITH", "MONELL"]),
    dict(t="Describe the change to HOPE's treatment-completion or aftercare policy that HOPE has stated occurred in or about October 2024, including your role in it.", c=["1983-SMITH", "MONELL"]),
    dict(t="State the date and manner in which you first learned of PLAINTIFF, and describe each later occasion on which you received information about him before this action was filed.", c=["1983-SMITH"]),
    dict(t="State the date and manner in which you first learned that PLAINTIFF had complained about, or sued over, HOPE's COMPLETION DETERMINATIONS, and describe what you did in response.", c=["1983-SMITH", "FA"]),
    dict(t="Describe each COMMUNICATION you had with CDCR during the RELEVANT PERIOD concerning treatment-completion, aftercare, or discharge policy for parolees, stating the date and participants.", c=["STATE", "1983-SMITH"]),
    dict(t="Describe each COMMUNICATION you had with any HOPE employee concerning PLAINTIFF, stating the date, participants, and substance.", c=["1983-SMITH", "FA"]),
    dict(t="State how and when you first learned of In re Dwyer (San Joaquin County Superior Court habeas proceeding), and describe what, if anything, you did in response.", c=["1983-SMITH", "MONELL"]),
    dict(t="State how and when you first learned of the April 17, 2025 amendments to Cal. Code Regs., tit. 15, section 3574, and describe what, if anything, you did in response.", c=["1983-SMITH", "MONELL"]),
    dict(t="State all facts supporting your contention that you are in privity with Katie Palacios or HOPE for purposes of claim preclusion based on the SAN JOAQUIN ACTION.", c=["DEFENSE-PRECLUSION"]),
    dict(t="State all facts supporting your contention that you did not act under color of state law with respect to the matters alleged in the complaint.", c=["STATE"]),
    dict(t="State all facts supporting any contention that you did not personally participate in, direct, or know of and acquiesce in the conduct alleged against you.", c=["1983-SMITH"], note="Starr v. Baca supervisory standard."),
    dict(t="State all facts supporting any contention that you did not threaten, intimidate, or coerce PLAINTIFF, directly or through HOPE's reports to CDCR, within the meaning of California Civil Code section 52.1.", c=["BANE"]),
    dict(t="IDENTIFY each email account, phone number, messaging application, and device (including any personal device or account) you used for HOPE business during the RELEVANT PERIOD.", c=["ESI"]),
    dict(t="Describe each step you took to preserve documents relevant to PLAINTIFF's claims, including the date of each step.", c=["ESI", "PRESERVATION"]),
    dict(t="IDENTIFY each insurance policy under which an insurer may be liable to satisfy all or part of a judgment against you in this action, including any individual or professional policy of your own, and state each insurer's coverage position.", c=["INSURANCE"]),
    dict(t="Describe any compensation or benefit you received during the RELEVANT PERIOD that was based in any part on HOPE's revenue, census, or client retention at the STOCKTON SITE.", c=["MONELL-MOTIVE", "PUNITIVE"], note="Kept only for Monell motive and punitive damages; fraud/RICO theory dropped."),
    dict(t="State your net worth and annual income for each of 2024 and 2025.", c=["PUNITIVE"], note="Punitive-damages financial condition. Expect objection/bifurcation request; can defer until a prima facie showing. Consider reserving."),
    dict(t="IDENTIFY each person you believe has knowledge of the facts alleged in the complaint or of your defenses, stating the subject of each person's knowledge.", c=["WITNESS"]),
    dict(t="State all facts supporting each affirmative defense you assert in your answer to the operative complaint.", c=["DEFENSE"], note="Serve only after an answer is filed. Counted as 1 but objectors argue one per defense; hold it if subparts are tight."),
    dict(t="IDENTIFY each person to whom you delegated authority over treatment-completion policy, CTM reporting, or the handling of client complaints during the RELEVANT PERIOD, and describe the authority delegated.", c=["1983-SMITH", "MONELL"], note="Supervisory delegation. Uses 1 of 5 reserve slots."),
]
SMITH_ROG_COUNT_NOTE = "21 numbered; reserve 4. Nos. 18 and 20 are timing-sensitive (see memo)."

# ---------------------------------------------------------------- HOPE RFAs (Set One -- serve-ready, no HOPE San Joaquin content)
HOPE_RFA1 = [
    ("During the RELEVANT PERIOD, HOPE provided sex-offender treatment to PLAINTIFF under a contract between HOPE and CDCR.", ["STATE"]),
    ("PLAINTIFF's participation in HOPE's program was a condition of his parole.", ["STATE", "DP"]),
    ("HOPE was certified by the California Sex Offender Management Board during the RELEVANT PERIOD.", ["STATE"]),
    ("HOPE was paid by CDCR for treatment services HOPE provided to PLAINTIFF.", ["STATE"]),
    ("HOPE reported PLAINTIFF's treatment status to CDCR at each CTM concerning PLAINTIFF.", ["STATE", "DP"]),
    ("At no CTM concerning PLAINTIFF did HOPE recommend that PLAINTIFF be found to have completed treatment.", ["MONELL", "DP"]),
    ("Under HOPE's practice during the RELEVANT PERIOD, a parolee could not be found to have completed treatment without a HOPE recommendation communicated to CDCR.", ["STATE"]),
    ("Before October 2024, HOPE's policy was that a parolee on active parole supervision continued in treatment until parole ended.", ["MONELL"]),
    ("Before October 2024, HOPE's treatment-completion policy for parolees followed a CDCR requirement.", ["STATE", "MONELL"]),
    ("HOPE's treatment-completion policy for parolees applied to all parolee clients at the STOCKTON SITE.", ["MONELL"]),
    ("HOPE did not change any treatment-completion policy for parolees after April 17, 2025.", ["MONELL", "DP"]),
    ("No HOPE parolee client at the STOCKTON SITE received a favorable COMPLETION DETERMINATION while on active parole supervision between January 1, 2021 and September 30, 2024.", ["MONELL"]),
    ("HOPE's revenue for a parolee client ends when the client is discharged from HOPE's program.", ["MONELL-MOTIVE"]),
    ("HOPE characterized PLAINTIFF's homework as \"partially completed\" in at least one communication to CDCR.", ["DP"]),
    ("HOPE did not provide PLAINTIFF a written explanation of the criteria he had to meet to complete treatment.", ["DP"]),
    ("HOPE did not provide PLAINTIFF an opportunity to contest HOPE's COMPLETION DETERMINATIONS before they were reported to CDCR.", ["DP"]),
    ("Before August 2025, PLAINTIFF complained to HOPE staff about HOPE's treatment-completion practices.", ["FA"]),
    ("In 2025, a HOPE employee described PLAINTIFF to CDCR as \"disruptive.\"", ["FA", "BANE"]),
    ("In 2025, a HOPE employee described PLAINTIFF to CDCR as a \"ringleader.\"", ["FA", "BANE"]),
    ("In 2025, Katie Palacios stated, in substance, that when PLAINTIFF complains, other clients join in.", ["FA"]),
    ("HOPE knew during the RELEVANT PERIOD that CDCR could treat a parolee's failure to attend HOPE sessions as a parole violation.", ["BANE"]),
    ("HOPE knew during the RELEVANT PERIOD that HOPE's reports to CDCR could affect the conditions of a parolee's supervision.", ["BANE", "STATE"]),
    ("CTMs concerning PLAINTIFF were video recorded.", ["FA", "PRESERVATION"]),
    ("HOPE has not deleted or overwritten any recording of a CTM concerning PLAINTIFF since January 1, 2025.", ["PRESERVATION"]),
    ("Dr. Cristina Loree testified in the In re Dwyer habeas proceeding in San Joaquin County Superior Court.", ["MONELL"]),
    ("HOPE was aware of the In re Dwyer proceeding before PLAINTIFF filed the SAN JOAQUIN ACTION.", ["MONELL"]),
    ("Cal. Code Regs., tit. 15, section 3574(f), as amended effective April 17, 2025, requires that a Containment Team determination to retain a supervised person in a sex offender management program be supported by good cause and stated in writing, signed by both the sex offender treatment provider and the parole agent on CDCR Form 3043.", ["STATE", "DP"]),
    ("SMITH had final authority over HOPE's treatment-completion policies during the RELEVANT PERIOD.", ["MONELL", "1983-SMITH"]),
    ("HOPE's verified response to Special Interrogatory No. 7 in the SAN JOAQUIN ACTION stated that, before October 2024, CDCR policy required supervised persons to continue some form of treatment as part of their supervision.", ["MONELL", "STATE"]),
    ("HOPE's verified response to Special Interrogatory No. 38 in the SAN JOAQUIN ACTION stated that Responding Party \"had no knowledge of Plaintiff's 'CDL employment obligations.'\"", ["CONTRA"]),
    ("HOPE's response to Special Interrogatory No. 28 in the SAN JOAQUIN ACTION stated that HOPE had no knowledge of the Dwyer decision.", ["CONTRA"]),
    ("HOPE knew of PLAINTIFF's employment as a commercial driver before January 1, 2023.", ["CONTRA", "DAMAGES"]),
    ("In at least one written report concerning PLAINTIFF transmitted to CDCR, HOPE stated that PLAINTIFF \"is fixated on lawsuits instead of subject material.\"", ["FA", "DP"]),
    ("The statement quoted in Request for Admission No. 33 refers to lawsuits filed by PLAINTIFF.", ["FA"]),
    ("HOPE signed at least one CDCR Form 3043 concerning PLAINTIFF.", ["STATE", "DP"]),
    ("HOPE did not sign a CDCR Form 3043 stating good cause to retain PLAINTIFF in a sex offender management program following the August 19, 2025 CTM.", ["DP", "STATE"]),
    ("HOPE has no record that a written determination to retain PLAINTIFF in a sex offender management program following the August 19, 2025 CTM was delivered to PLAINTIFF within 30 calendar days of that CTM.", ["DP"]),
    ("HOPE did not sign a CDCR Form 3043 stating good cause to retain PLAINTIFF in a sex offender management program following the February 18, 2026 CTM.", ["DP", "STATE"]),
    ("HOPE has no record that a written determination to retain PLAINTIFF in a sex offender management program following the February 18, 2026 CTM was delivered to PLAINTIFF within 30 calendar days of that CTM.", ["DP"]),
    ("At no time after April 17, 2025 did HOPE score PLAINTIFF at 11 or higher on the Level of Service/Case Management Inventory (LS/CMI).", ["DP", "STATE"]),
    ("Katie Palacios acted within the course and scope of her employment or agency with HOPE when communicating with CDCR about PLAINTIFF.", ["BANE", "FA"]),
]
HOPE_RFA1_NOTES = {
    29: "Quote from HOPE's San Joaquin discovery response (not the confidential production). Confirm the response was not designated Confidential and that it was verified; Nos. 29-31 track those responses.",
    32: "Contradiction lock: Plaintiff's own knowledge (work accommodations requested). Does not rely on HOPE_ production.",
    27: "Verified Oct 14, 2026 against current 15 CCR 3574(f) (Cornell LII; CDCR adopted text, COC filed 4/17/2025).",
    33: "Quote appears in Complaint para. 32 and is quoted by Defendants in Dkt 15 (public). Not from HOPE_ production.",
    35: "Defeats the San Joaquin SROG objection that Forms 3043/1502-DR are CDCR-retained forms.",
    36: "CTM dates from HOPE's verified San Joaquin SROG 11 response (not designated Confidential). 15 CCR 3574(f).",
    38: "Same basis as No. 36 (Feb 18, 2026 CTM per SROG 11).",
    40: "Basis: Plaintiff's own Form 1502-DR (LS/CMI 5 on 10/15/2024). Confirm with Brendan that no later score of 11+ exists. 15 CCR 3574(f)(1).",
    41: "Respondeat superior for the Bane Act claim (state law; Monell bar does not apply).",
}

# ---------------------------------------------------------------- HOPE RFAs Set Two -- HOLD pending PO fix
HOPE_RFA2_HOLD = [
    ("The documents Bates-numbered HOPE_000001 through HOPE_000542 are true and correct copies of documents maintained by HOPE.", "all"),
    ("The documents Bates-numbered HOPE_000139 through HOPE_000199 are records made at or near the time of the events they describe by persons with knowledge, kept in the course of HOPE's regularly conducted activity, as a regular practice of that activity.", "000139-199"),
    ("The document Bates-numbered HOPE_000225 through HOPE_000349 is HOPE's Clinical Operational Manual in effect on and after September 23, 2024.", "000225-349"),
    ("The page Bates-numbered HOPE_000294 is a genuine page of HOPE's Clinical Operational Manual.", "000294"),
    ("The statement on HOPE_000294 concerning HOPE's inability to discharge clients is attributable to the terms of HOPE's contract(s) with CDCR.", "000294"),
    ("The statement on HOPE_000294 concerning HOPE's inability to discharge clients reflected HOPE's policy at the STOCKTON SITE during 2024 and 2025.", "000294"),
    ("The page Bates-numbered HOPE_000295 accurately states HOPE's graduation criteria in effect on and after September 23, 2024.", "000295"),
    ("Under the criteria stated on HOPE_000295, a Treatment Completion Certificate cannot issue without approval by HOPE's Clinical Director.", "000295"),
    ("Under the criteria stated on HOPE_000295, a client's completion is recorded through an upload to a CDCR system.", "000295"),
    ("The pages Bates-numbered HOPE_000334 through HOPE_000335 accurately state HOPE's requirement for CTM notes in effect on and after September 23, 2024.", "000334-335"),
    ("HOPE has not produced in this action any CTM note concerning PLAINTIFF prepared under the requirement stated on HOPE_000334 through HOPE_000335.", "000334-335"),
    ("The addenda referenced on HOPE_000348 through HOPE_000349 exist in HOPE's possession, custody, or control.", "000348-349"),
    ("The document Bates-numbered HOPE_000189 is a genuine record of HOPE.", "000189"),
    ("SMITH received a copy of the communication described on HOPE_000189 on or about January 6, 2026.", "000189"),
    ("The \"policy and procedure\" referenced on HOPE_000189 is a written HOPE document.", "000189"),
    ("The document Bates-numbered HOPE_000538 through HOPE_000542 is a genuine job description for HOPE's Clinical Director position.", "000538-542"),
    ("HOPE's Clinical Director position was eligible for a performance bonus during 2024 and 2025.", "000538-542"),
    ("The Clinical Director's duties during 2024 and 2025 included auditing for compliance with HOPE's contractual requirements.", "000538-542"),
    ("HOPE moved PLAINTIFF to an evening group in or about April 2022 to accommodate his work schedule.", "000143, 000197-199"),
    ("HOPE approved a teletherapy modification for PLAINTIFF in or about April 2023.", "000159-161"),
]
HOPE_RFA2_NOTES = {
    18: "Double-edged: admits accommodation (cuts against 'no accommodation') but locks HOPE's knowledge of his work, contradicting San Joaquin SROG 38. Net useful for Monell/Bane knowledge; weigh before serving.",
    19: "Same as 18.",
    5: "May draw a 'document speaks for itself' objection; the memo has the response.",
}

SMITH_RFA_HOLD_IDX = {9, 10}  # 1-based; depend on HOPE_000189
SMITH_RFA = [
    ("You were HOPE's chief executive officer throughout the RELEVANT PERIOD.", ["1983-SMITH"]),
    ("You had final authority over HOPE's treatment-completion policies for parolees during the RELEVANT PERIOD.", ["MONELL", "1983-SMITH"]),
    ("You approved HOPE's treatment-completion policy for parolees in effect before October 2024.", ["1983-SMITH"]),
    ("You approved the change to HOPE's treatment-completion or aftercare policy that occurred in or about October 2024.", ["1983-SMITH"]),
    ("You did not cause HOPE to change any treatment-completion policy after April 17, 2025.", ["1983-SMITH", "DP"]),
    ("You knew before January 1, 2025 that HOPE did not recommend completion for parolees on active parole supervision.", ["1983-SMITH"]),
    ("You knew during the RELEVANT PERIOD that HOPE's reports to CDCR could affect the conditions of a parolee's supervision.", ["BANE", "1983-SMITH"]),
    ("You communicated with CDCR personnel during the RELEVANT PERIOD about treatment-completion or aftercare policy for parolees.", ["STATE"]),
    ("You received notice of the SAN JOAQUIN ACTION complaint in or about January 2026.", ["1983-SMITH"]),
    ("You took no action to review PLAINTIFF's treatment status after receiving notice of the SAN JOAQUIN ACTION complaint.", ["1983-SMITH", "FA"]),
    ("You were not a party to the SAN JOAQUIN ACTION.", ["DEFENSE-PRECLUSION"]),
    ("No claim against you personally was adjudicated in the SAN JOAQUIN ACTION.", ["DEFENSE-PRECLUSION"]),
    ("You did not control HOPE's defense of the SAN JOAQUIN ACTION.", ["DEFENSE-PRECLUSION"], ),
    ("You were aware of the In re Dwyer habeas proceeding before PLAINTIFF filed the SAN JOAQUIN ACTION.", ["1983-SMITH", "MONELL"]),
    ("You were aware of the April 17, 2025 amendments to Cal. Code Regs., tit. 15, section 3574 before PLAINTIFF filed the SAN JOAQUIN ACTION.", ["1983-SMITH"]),
    ("You used a personal device or personal account for HOPE business communications during the RELEVANT PERIOD.", ["ESI"]),
    ("You have not issued a litigation hold covering text messages concerning PLAINTIFF.", ["PRESERVATION"]),
    ("You held an ownership interest in HOPE during the RELEVANT PERIOD.", ["MONELL-MOTIVE", "PUNITIVE", "1983-SMITH"]),
    ("You had authority to require an internal review of a client complaint concerning HOPE personnel during the RELEVANT PERIOD.", ["1983-SMITH"]),
]
SMITH_RFA_NOTES = {
    9: "HOLD: rests on HOPE_000189 (San Joaquin production). Serve only after the PO fix.",
    10: "HOLD: same basis as No. 9.",
    13: "Privity test (DKN, 61 Cal.4th at 826): a 'No' here can surface through a later deposition; the RFA forces a position. Keep it.",
}

# ---------------------------------------------------------------- HOPE RFPs
HOPE_RFP = [
    ("A. Prior production", [
        ("All DOCUMENTS HOPE produced in the SAN JOAQUIN ACTION, including those Bates-numbered HOPE_000001 through HOPE_000542, in the form produced, with any designations.", ["ALL"]),
        ("HOPE's verified responses, and any amended or supplemental responses, to all written discovery served in the SAN JOAQUIN ACTION.", ["ALL", "CONTRA"]),
    ]),
    ("B. Plaintiff's treatment and CTM records", [
        ("PLAINTIFF's complete clinical file, including intake documents, treatment contracts and client service agreements, treatment plans in every version, progress notes, group and individual session notes, attendance records, homework records, polygraph reports and referrals, and any discharge, titration, or completion documents.", ["1983-HOPE", "DP"]),
        ("PLAINTIFF's complete electronic health record in native or system-export form, together with the system audit trail showing, for each entry, the author, creation date, and every modification, view, export, or deletion.", ["1983-HOPE", "DP", "ESI"]),
        ("All audio and video recordings of any CTM concerning PLAINTIFF, including the CTMs held on or about August 19, 2025 and February 18, 2026.", ["FA", "BANE", "DP"]),
        ("All audio and video recordings of HOPE group sessions attended by PLAINTIFF from June 1, 2025 through September 30, 2025.", ["FA"]),
        ("All CTM notes, CTM progress reports, CTM agendas, sign-in sheets, and pre-CTM submissions concerning PLAINTIFF.", ["DP", "STATE"]),
        ("All CDCR Form 3043 documents and CDCR Form 1502-DR inputs concerning PLAINTIFF, including drafts, worksheets, signature pages, transmittals, and records of delivery to PLAINTIFF.", ["STATE", "DP"]),
        ("All titration tracking forms, graduation or completion checklists, Treatment Completion Certificate materials, and records of any upload to a CDCR system (including ARMS) concerning PLAINTIFF.", ["STATE", "DP"]),
        ("All homework packets and preparatory tickets PLAINTIFF submitted, and all logs, chart notations, or records of their assignment, receipt, review, or grading.", ["DP"]),
        ("All DOCUMENTS concerning any complaint, grievance, objection, or request by PLAINTIFF, and HOPE's response to each.", ["FA"]),
        ("All DOCUMENTS in which any HOPE employee characterizes PLAINTIFF's behavior, attitude, participation, or complaints, including as \"disruptive\" or a \"ringleader.\"", ["FA", "BANE"]),
        ("All DOCUMENTS concerning PLAINTIFF's work schedule, employment, or requests for schedule changes or telehealth.", ["DAMAGES", "BANE"]),
    ]),
    ("C. Communications", [
        ("All COMMUNICATIONS between HOPE and CDCR concerning PLAINTIFF, in native form with attachments.", ["STATE", "FA", "BANE"]),
        ("All COMMUNICATIONS among HOPE personnel (including management or records contractors) concerning PLAINTIFF, including text and app-based messages and messages on personal devices or accounts used for work, and including any archive or journaling mailbox.", ["FA", "1983-SMITH"]),
        ("All COMMUNICATIONS sent or received by SMITH concerning PLAINTIFF, the SAN JOAQUIN ACTION, this action, In re Dwyer, or treatment-completion or aftercare policy for parolees.", ["1983-SMITH", "MONELL"]),
        ("All COMMUNICATIONS between HOPE and CDCR from January 1, 2023 to the present concerning treatment-completion, aftercare, titration, or discharge policy for parolees.", ["STATE", "MONELL"]),
    ]),
    ("D. CDCR relationship (state action)", [
        ("Each contract, master agreement, scope of work, statement of work, amendment, and incorporated guideline or exhibit between HOPE and CDCR covering sex-offender treatment services at the STOCKTON SITE in effect at any time during the RELEVANT PERIOD.", ["STATE", "MONELL"]),
        ("All CDCR directives, memoranda, policy statements, and guidance HOPE received during the RELEVANT PERIOD concerning treatment duration, completion, aftercare, titration, or discharge of parolees, including any received in or about October 2024 and any concerning Cal. Code Regs., tit. 15, section 3574.", ["STATE", "MONELL", "DP"]),
        ("DOCUMENTS sufficient to show each CDCR audit, review, or compliance finding concerning HOPE's sex-offender treatment services at the STOCKTON SITE during the RELEVANT PERIOD.", ["STATE"]),
        ("DOCUMENTS sufficient to show HOPE's access to, and user accounts in, any CDCR information system (including ARMS) during the RELEVANT PERIOD.", ["STATE"]),
    ]),
    ("E. Policies, manuals, and training", [
        ("Each version of HOPE's Clinical Operational Manual, treatment manual, curricula, graduation or completion criteria, and employee handbook in effect at any time during the RELEVANT PERIOD, with effective dates.", ["MONELL"]),
        ("All addenda, forms, templates, and training-library materials referenced or hyperlinked in any document produced under the preceding request, in native form, wherever hosted (including on shared drives or internal websites maintained by a contractor).", ["MONELL"]),
        ("All DOCUMENTS reflecting the adoption, approval, or announcement of the change to HOPE's treatment-completion or aftercare policy that HOPE contends occurred in or about October 2024, including drafts and staff communications.", ["MONELL", "1983-SMITH"]),
        ("All DOCUMENTS reflecting any policy, practice, or contract term under which HOPE could not discharge, complete, or titrate a parolee client while on parole supervision.", ["MONELL", "STATE"]),
        ("HOPE's written policy and procedure for responding to client complaints, grievances, and lawsuits in effect at any time from January 1, 2025 to the present.", ["FA", "1983-SMITH"]),
        ("All training materials provided to STOCKTON SITE clinical staff during the RELEVANT PERIOD concerning COMPLETION DETERMINATIONS, CTM reporting, or responding to client complaints.", ["MONELL"]),
        ("All DOCUMENTS concerning In re Dwyer, including any notes or materials concerning testimony by any HOPE employee.", ["MONELL"]),
    ]),
    ("F. Comparator data (de-identified)", [
        ("DOCUMENTS sufficient to show, for each year from 2021 through 2026 at the STOCKTON SITE, the number of parolee clients enrolled, the number who received a favorable COMPLETION DETERMINATION while on parole, and the number discharged for any other reason, with each client de-identified.", ["MONELL", "DP"]),
        ("For each STOCKTON SITE parolee client who received a favorable COMPLETION DETERMINATION while on parole from 2021 through 2026, DOCUMENTS sufficient to show (de-identified) the date of the determination, the treatment phase completed, and the time in treatment.", ["MONELL"]),
    ]),
    ("G. Personnel and discipline", [
        ("For Katie Palacios, Bernadette Marie Tassone, Pamela Akins, Dr. Cristina Loree, Kristine Hansen, Dr. Carrie Shinske, and Mark Delucchi: job descriptions, dates of employment and positions, and documents sufficient to show each person's supervisor.", ["1983-SMITH", "MONELL"]),
        ("Any complaints, investigations, discipline, or corrective action concerning Katie Palacios or any clinician assigned to PLAINTIFF that relate to client complaints, retaliation, recordkeeping, or reports to CDCR during the RELEVANT PERIOD.", ["FA", "MONELL"]),
        ("DOCUMENTS sufficient to show any component of compensation for the Clinical Director or site director of the STOCKTON SITE during 2021-2026 that was tied to client census, retention, or revenue.", ["MONELL-MOTIVE", "PUNITIVE"]),
    ]),
    ("H. Insurance", [
        ("Every insurance policy (primary, excess, or umbrella; professional, directors and officers, employment practices, or general liability) under which an insurer may be liable to satisfy all or part of a judgment against HOPE or SMITH in this action, for each policy period covering any part of 2021 to the present, with declarations and endorsements.", ["INSURANCE"]),
        ("Each notice of claim or tender to any insurer concerning PLAINTIFF's claims, and each reservation-of-rights or coverage-position letter received in response.", ["INSURANCE"]),
    ]),
    ("I. Retention and ESI", [
        ("HOPE's document-retention and destruction policies and schedules in effect during the RELEVANT PERIOD, including those for EHR records, email, text messages, and CTM or group recordings.", ["ESI", "PRESERVATION"]),
        ("DOCUMENTS sufficient to show the date, scope, and recipients of any litigation hold concerning PLAINTIFF's claims (not the privileged content).", ["PRESERVATION"]),
        ("DOCUMENTS sufficient to show HOPE's agreement with any management, records, or EHR contractor that maintains HOPE's clinical records, email, or policy documents.", ["ESI"]),
    ]),
    ("J. Defenses", [
        ("All DOCUMENTS HOPE contends support its position that it did not act under color of state law.", ["STATE"]),
        ("All DOCUMENTS HOPE contends support its position that its COMPLETION DETERMINATIONS concerning PLAINTIFF were individualized clinical judgments.", ["MONELL", "DP"]),
        ("All DOCUMENTS HOPE identified, or intends to identify, in its Rule 26(a)(1) initial disclosures.", ["ALL"]),
    ]),
    ("K. Additional requests", [
        ("Every progress report, treatment-plan update, or status report concerning PLAINTIFF that HOPE prepared for or transmitted to CDCR from August 1, 2024 to the present, including each report containing the words \"fixated on lawsuits.\"", ["FA", "DP", "STATE"]),
        ("Every risk or needs assessment scored for PLAINTIFF (including the Static-99R, STABLE-2007, ACUTE-2007, and LS/CMI), with score sheets, inputs, and any COMMUNICATION of results to CDCR.", ["DP", "STATE"]),
        ("All DOCUMENTS concerning HOPE's receipt, review, routing, or escalation of the complaint in the SAN JOAQUIN ACTION from December 1, 2025 through January 31, 2026 (privileged communications with counsel to be logged rather than produced).", ["FA", "1983-SMITH"]),
        ("Organizational charts, or DOCUMENTS sufficient to identify each person responsible during the RELEVANT PERIOD for treatment-completion policy, CTM reporting, compliance, records management, and complaint handling.", ["MONELL", "1983-SMITH"]),
        ("All DOCUMENTS HOPE prepared, and all COMMUNICATIONS between HOPE and CDCR, from September 1, 2025 through December 31, 2025 concerning PLAINTIFF's treatment status or completion eligibility, including any information HOPE supplied for the CDCR Form 1502-DR concerning PLAINTIFF signed on November 14 and 19, 2025.", ["STATE", "DP", "FA"]),
    ]),
]

SMITH_RFP = [
    ("A. Communications and knowledge", [
        ("All COMMUNICATIONS you sent or received concerning PLAINTIFF, including on any personal device or account.", ["1983-SMITH", "FA"]),
        ("All COMMUNICATIONS you sent or received concerning the SAN JOAQUIN ACTION or this action, other than privileged communications with counsel (which must be logged).", ["1983-SMITH"]),
        ("All COMMUNICATIONS between you and CDCR from January 1, 2021 to the present concerning treatment-completion, aftercare, titration, or discharge policy for parolees.", ["STATE", "1983-SMITH"]),
        ("All DOCUMENTS concerning In re Dwyer or the April 17, 2025 amendments to Cal. Code Regs., tit. 15, section 3574 that you received, authored, or reviewed.", ["1983-SMITH", "MONELL"]),
        ("All text and app-based messages you exchanged with any HOPE employee or contractor concerning treatment-completion policy, CTM reporting, or client complaints, from January 1, 2023 to the present.", ["1983-SMITH", "MONELL"]),
    ]),
    ("B. Policy role", [
        ("All DOCUMENTS reflecting your approval, review, or revision of any HOPE policy concerning COMPLETION DETERMINATIONS for parolees, including the change HOPE contends occurred in or about October 2024.", ["1983-SMITH", "MONELL"]),
        ("All board, executive-team, or management meeting agendas, minutes, and presentations from January 1, 2023 to the present that address treatment-completion, aftercare, or discharge policy for parolees, or PLAINTIFF.", ["1983-SMITH", "MONELL"]),
        ("All reports concerning STOCKTON SITE census, retention, completions, or discharges that you received or reviewed from January 1, 2021 to the present.", ["MONELL", "1983-SMITH"]),
    ]),
    ("C. Preservation, insurance, and defenses", [
        ("DOCUMENTS sufficient to show each device, phone number, email account, and messaging account you used for HOPE business during the RELEVANT PERIOD.", ["ESI"]),
        ("DOCUMENTS sufficient to show the date and scope of any preservation steps you took concerning PLAINTIFF's claims.", ["PRESERVATION"]),
        ("Every insurance policy, including any individual policy, under which an insurer may be liable to satisfy all or part of a judgment against you in this action, with declarations and endorsements, and any reservation-of-rights letter concerning PLAINTIFF's claims.", ["INSURANCE"]),
        ("All DOCUMENTS you contend support your position that you are in privity with HOPE or Katie Palacios for purposes of the SAN JOAQUIN ACTION judgment.", ["DEFENSE-PRECLUSION"]),
        ("All DOCUMENTS you contend support your position that you did not act under color of state law.", ["STATE"]),
        ("All DOCUMENTS you contend show that you did not personally participate in, direct, or know of and acquiesce in the conduct alleged against you.", ["1983-SMITH"]),
        ("DOCUMENTS sufficient to show any compensation you received during 2021-2026 that was based in any part on HOPE's revenue, census, or client retention.", ["MONELL-MOTIVE", "PUNITIVE"]),
    ]),
]
