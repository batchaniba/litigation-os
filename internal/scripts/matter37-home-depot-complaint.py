#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Matter 37 — verified complaint, Home Depot U.S.A., Inc. (Tracy DC).

LOCKED after the September 8, 2026 execute. Do not rewrite pleading prose
unless a new Home Depot document appears.

San Joaquin Superior Court. Penal Code § 290.46(j) is the load-bearing count.
Hire, acceptance, onboarding, the background check, the ghost, Plaintiff's
Megan's Law listing, and exclusive control of the file are the supporting
facts. Report contents and Home Depot's use are information and belief.
The Tracy building is the worksite, not the legal defendant.

Default output is unsigned because the requested execution date
(September 8, 2026) is in the future. On or after that date, rerun with
``--execute`` only after Plaintiff confirms the hire, the employment
decision, and the nonreceipt/notice allegations.

    python3 internal/scripts/matter37-home-depot-complaint.py
    python3 internal/scripts/matter37-home-depot-complaint.py --execute
"""

from __future__ import annotations

import argparse
import datetime as dt
import re
import sys
from pathlib import Path

_DRAFT_NOTE = re.compile(r"\s*\[[^\[\]]+\]")


def _filing_text(text: str, execute: bool) -> str:
    if not execute:
        return text
    return _DRAFT_NOTE.sub("", text).rstrip()

SCRIPT_DIR = Path(__file__).resolve().parent
sys.path.insert(0, str(SCRIPT_DIR / "lib"))
sys.path.insert(0, str(SCRIPT_DIR))

from pleading_paper import CONTENT_LEFT, COURT_LINE1, PleadingPaper  # noqa: E402
from signature_stamp import SIGNATURE_NATIVE_PX, SIGNATURE_PATH  # noqa: E402

ROOT = SCRIPT_DIR.parents[1]
DEFAULT_OUT = (
    ROOT
    / "internal/public/documents/matter-37"
    / "Verified Complaint - Ngwa Nforbi v Home Depot USA Inc"
    " (Sep 8 2026).pdf"
)
DEFAULT_EXEC_DATE = "September 8, 2026"
EARLIEST_EXECUTION_DATE = dt.date(2026, 9, 8)
COURT_LINE2 = "COUNTY OF SAN JOAQUIN"
FOOTER = "VERIFIED COMPLAINT -- BRENDAN NGWA NFORBI v. HOME DEPOT U.S.A., INC."

PLAINTIFF_BLOCK = [
    ("BRENDAN NGWA NFORBI", "Times-Bold", 12),
    ("Plaintiff, In Propria Persona", "Times-Roman", 12),
    ("1455 Cat Tail Drive", "Times-Roman", 12),
    ("Stockton, CA 95204", "Times-Roman", 12),
    ("Telephone: (209) 801-4442", "Times-Roman", 12),
    ("E-mail: bnn.cdl@gmail.com", "Times-Roman", 12),
]

CAPTION_LEFT = [
    ("BRENDAN NGWA NFORBI,", True, False),
    ("", False, False),
    ("                          Plaintiff,", False, False),
    ("", False, False),
    ("       v.", False, False),
    ("", False, False),
    ("HOME DEPOT U.S.A., INC., a", True, False),
    ("Delaware corporation, d/b/a THE", True, False),
    ("HOME DEPOT and THE HOME DEPOT", True, False),
    ("DISTRIBUTION CENTER; and DOES 1", True, False),
    ("through 20, inclusive,", True, False),
    ("", False, False),
    ("                          Defendants.", False, False),
]

CAPTION_RIGHT = [
    ("Case No. _________________", False, False),
    ("", False, False),
    ("VERIFIED COMPLAINT FOR", True, False),
    ("DAMAGES, DECLARATORY AND", True, False),
    ("INJUNCTIVE RELIEF", True, False),
    ("", False, False),
    ("(1) ICRAA, Civ. Code", False, False),
    ("      § 1786.40;", False, False),
    ("(2) CCRAA, Civ. Code", False, False),
    ("      § 1785.20.5;", False, False),
    ("(3) UCL, B&P Code § 17200;", False, False),
    ("(4) Penal Code § 290.46(j)", False, False),
    ("      (I&B — report", False, False),
    ("      contents and use)", False, False),
    ("", False, False),
    ("[Unlimited Civil]", False, True),
    ("[Jury Trial Demanded]", False, True),
]

SIGNOFF_NAME = "BRENDAN NGWA NFORBI"
SIGNOFF_ROLE = "Plaintiff, In Propria Persona"
SIG_LINE = "___________________________________"

CONTENT = [
    (
        "NOTICE",
        "REVIEW DRAFT — DO NOT FILE OR SIGN BEFORE SEPTEMBER 8, 2026. "
        "PLAINTIFF MUST CONFIRM THE HIRE, THE EMPLOYMENT DECISION, THE "
        "DATE OF THAT DECISION, ANY BACKGROUND-CHECK VENDOR OR NOTICES, "
        "AND WHETHER HE RECEIVED WAGES OR A WRITTEN ADVERSE-ACTION "
        "EXPLANATION, BEFORE EXECUTION.",
    ),
    ("PARA", 'Plaintiff BRENDAN NGWA NFORBI ("Plaintiff") alleges as follows:'),
    ("HEADER", "I.\nINTRODUCTION"),
    (
        "PARA",
        "1. This is an action under Penal Code section 290.46, subdivision (j), "
        "for the unauthorized employment use of California Megan's Law registry "
        "information. On or about August 2024, Defendant Home Depot U.S.A., Inc. "
        "hired Plaintiff to work at its distribution and fulfillment center at "
        "5395 Hopkins Road, Tracy, California 95377. Plaintiff accepted that "
        "hire and began onboarding. Home Depot ran a background check concerning "
        "Plaintiff. Thereafter Home Depot ceased communication and ghosted him. "
        "That cessation is the adverse employment action: it denied, withdrew, "
        "or ended the accepted Tracy Center employment. Plaintiff is a person "
        "as to whom information is disclosed on the California Megan's Law "
        "website. The Home Depot background report remains in Defendants' "
        "files. Plaintiff does not possess it and does not allege its contents "
        "as a known fact. He is informed and believes, and on that basis "
        "alleges, that the report contained information disclosed pursuant to "
        "Penal Code section 290.46, including his listing on the California "
        "Sex Offender Registry, and that Home Depot used that information, in "
        "whole or in part, to ghost him and make the employment decision. The "
        "basis for that belief is the hire, the screen, the unexplained ghost, "
        "Plaintiff's contemporaneous Megan's Law listing, and Home Depot's "
        "exclusive control of the file.",
    ),
    (
        "PARA",
        "2. Penal Code section 290.46(j)(1) authorizes use of information "
        "disclosed under that section only to protect a person at risk. "
        "Subdivision (j)(2)(E) prohibits use of that information for purposes "
        "relating to employment, except as another law authorizes. A warehouse "
        "or fulfillment-center hiring, continuation, or termination decision is "
        "a purpose relating to employment.",
    ),
    (
        "PARA",
        "3. Those are two different classes of allegation. Plaintiff alleges "
        "as known facts: (a) Home Depot hired him, on information and belief "
        "on or about August 2024, at the Tracy Center; (b) he accepted and "
        "began onboarding; (c) Home Depot ran a background check; (d) Home "
        "Depot then ghosted him; (e) he is a person as to whom information is "
        "disclosed pursuant to Penal Code section 290.46; and (f) the report "
        "is in Home Depot's files. He is informed and believes, and on that "
        "basis alleges, that the report contained information disclosed "
        "pursuant to Penal Code section 290.46, including his California Sex "
        "Offender Registry listing, and that Home Depot used that information "
        "to ghost him and to make an employment decision. A warehouse or "
        "fulfillment-center hiring, continuation, or termination decision is "
        "a purpose relating to employment, which section 290.46(j)(2)(E) "
        "forbids.",
    ),
    (
        "PARA",
        "4. Taking the known facts and the well-pleaded information-and-belief "
        "allegations as true, as this Court must on demurrer, Plaintiff states "
        "a cause of action under Penal Code section 290.46(j) that is plausible "
        "on its face. Code of Civil Procedure section 425.10 requires a "
        "statement of the facts constituting the cause of action in ordinary "
        "and concise language. Section 452 requires this Court to construe the "
        "pleading liberally with a view to substantial justice between the "
        "parties. A demurrer admits the material facts properly pleaded, "
        "including facts alleged on information and belief when the supporting "
        "basis is stated. It does not test whether Home Depot will later "
        "produce a different report.",
    ),
    (
        "PARA",
        "5. Plaintiff does not presently possess a copy of the Home Depot "
        "background report. The report, the vendor file, the order time, the "
        "access log, and the adjudication notes are in Defendants' possession. "
        "He does not attach the report because Home Depot has not given it to "
        "him. He does not allege, as a known fact, what that report contained. "
        "Withholding the report does not make the information-and-belief "
        "allegations disappear at the pleading stage. The precise hire date, "
        "job title, rate of pay, and vendor name are likewise facts of Home "
        "Depot's personnel and screening records. Plaintiff alleges them on "
        "information and belief as to August 2024 and the Tracy Center. A "
        "demurrer for uncertainty under Code of Civil Procedure section "
        "430.10(f) is not a substitute for records Defendant possesses and "
        "has not produced. Plaintiff will seek the report and those records "
        "in discovery."
    ),
    (
        "PARA",
        "6. Plaintiff does not presently know the legal name of the consumer "
        "reporting agency, if any, that Home Depot used. He has sued DOES 1 "
        "through 10 for that vendor and for any Home Depot affiliate that was "
        "the actual employing or decision-making entity. He does not name "
        "The Home Depot, Inc., the publicly traded parent, merely because it "
        "owns affiliated entities.",
    ),
    (
        "PARA",
        "7. This Complaint does not plead a Tameny wrongful-termination count, "
        "an IIED count, or a FEHA or Government Code section 12952 Fair "
        "Chance Act count. The Fair Chance reservation is not a count. "
        "Plaintiff will timely exhaust California Civil Rights Department "
        "rights and seek leave to amend if discovery shows conviction history "
        "caused or contributed to the decision after the hire. He does not "
        "presently plead unpaid-wage, waiting-time, or wage-statement counts. "
        "'Began onboarding' is not, without more, compensable work. He "
        "preserves those theories if badge, time, training, or pay records "
        "later show he performed employer-controlled activity for which "
        "wages were due. The load-bearing claim is the statutory prohibition "
        "in Penal Code section 290.46(j). Companion consumer-report and "
        "unfair-competition counts are pleaded only to the extent the same "
        "employment use, if proven, also violated those statutes. ICRAA and "
        "CCRAA are pleaded in the alternative so the notice claim survives "
        "whether the report was investigative or an ordinary consumer credit "
        "report. Plaintiff does not presently plead Labor Code section 432.7 "
        "as a cause of action. He has not alleged that any report used an "
        "arrest that did not result in a conviction, diversion, or a "
        "dismissed conviction. He preserves leave to amend if the file later "
        "supports those reserved theories.",
    ),
    ("HEADER", "II.\nPARTIES"),
    (
        "PARA",
        "8. Plaintiff BRENDAN NGWA NFORBI is a natural person residing in "
        "Stockton, San Joaquin County, California. He is also identified in "
        "employment and court records as Brendan Ngehsi Ngwanforbi. Those name "
        "variants refer to Plaintiff.",
    ),
    (
        "PARA",
        "9. Plaintiff is required to register under California Penal Code "
        "section 290. At all times relevant to this Complaint, information "
        "identifying him appeared on California's Megan's Law website and "
        "California Sex Offender Registry, operated pursuant to Penal Code "
        "section 290.46.",
    ),
    (
        "PARA",
        "10. Defendant HOME DEPOT U.S.A., INC. ('Home Depot') is a corporation "
        "organized under the laws of the State of Delaware, qualified to "
        "transact business in California, and doing business as The Home Depot "
        "and The Home Depot Distribution Center. On information and belief, "
        "Home Depot U.S.A., Inc. owned, operated, staffed, and controlled the "
        "distribution and fulfillment center located at 5395 Hopkins Road, "
        "Tracy, California 95377 (the 'Tracy Center'), and was the legal "
        "employer that hired Plaintiff and made the employment decision "
        "challenged here.",
    ),
    (
        "PARA",
        "11. The Tracy Center is a Home Depot warehouse and fulfillment "
        "facility in the International Park of Commerce in Tracy, San Joaquin "
        "County. It is a worksite, not a separate legal entity. Plaintiff sues "
        "the corporation that operates it.",
    ),
    (
        "PARA",
        "12. If discovery establishes that another Home Depot subsidiary or "
        "affiliate was the employing or decision-making entity, Plaintiff has "
        "sued DOES 11 through 15 for that purpose and will amend to substitute "
        "the correct entity.",
    ),
    (
        "PARA",
        "13. On information and belief, Home Depot's designated agent for "
        "service of process in California is CSC Lawyers Incorporating Service, "
        "2710 Gateway Oaks Drive, Suite 150N, Sacramento, California 95833. "
        "Plaintiff will serve Home Depot through the agent listed on the "
        "California Secretary of State record as of the date of service. "
        "Service is not to be made at the Tracy Center merely because that is "
        "where Plaintiff worked.",
    ),
    (
        "PARA",
        "14. The true names and capacities of DOES 1 through 20 are unknown to "
        "Plaintiff, who therefore sues them by fictitious names under Code of "
        "Civil Procedure section 474. DOES 1 through 10 include the consumer "
        "reporting agency, investigative consumer reporting agency, or other "
        "vendor that assembled, evaluated, furnished, or scored background "
        "information about Plaintiff for Home Depot, and the individuals who "
        "ordered, reviewed, or acted on that information. Plaintiff will amend "
        "this Complaint when their identities and roles are ascertained.",
    ),
    (
        "PARA",
        "15. Plaintiff is informed and believes that each DOE Defendant "
        "participated in, authorized, directed, furnished information for, "
        "implemented, concealed, or ratified one or more acts alleged and is "
        "legally responsible for the resulting harm.",
    ),
    ("HEADER", "III.\nJURISDICTION AND VENUE"),
    (
        "PARA",
        "16. This Court has subject-matter jurisdiction under article VI, "
        "section 10 of the California Constitution and Code of Civil Procedure "
        "section 410.10.",
    ),
    (
        "PARA",
        "17. This action is properly designated unlimited civil under Code of "
        "Civil Procedure sections 85 and 88 because the aggregate relief sought "
        "exceeds $35,000, exclusive of interest and costs, including actual, "
        "statutory, exemplary, and equitable relief according to proof. No "
        "specific personal-injury or punitive-damages amount is pleaded.",
    ),
    (
        "PARA",
        "18. This Court has personal jurisdiction over Home Depot because Home "
        "Depot is qualified to do business in California, operates the Tracy "
        "Center in this County, hired Plaintiff for work in this County, and "
        "made or implemented the challenged employment decision in California.",
    ),
    (
        "PARA",
        "19. Venue is proper in the County of San Joaquin under Code of Civil "
        "Procedure sections 395 and 395.5 because Plaintiff resides here, the "
        "Tracy Center is here, the hire and the employment decision occurred "
        "here, and the liability and injury arose here.",
    ),
    (
        "PARA",
        "20. Plaintiff has not pleaded a federal claim. If a later amendment "
        "adds one, that fact will be stated then. This Complaint is a "
        "California statutory action belonging in this Court.",
    ),
    ("HEADER", "IV.\nTIMELINESS"),
    (
        "PARA",
        "21. Penal Code section 290.46 does not prescribe its own limitations "
        "period. This action upon a liability created by that statute is timely "
        "under Code of Civil Procedure section 338, subdivision (a), which "
        "requires that such an action, other than a penalty or forfeiture, be "
        "commenced within three years after accrual.",
    ),
    (
        "PARA",
        "22. The cause of action accrued, if at all, when Home Depot used "
        "registry information for purposes relating to Plaintiff's employment — "
        "that is, on the date of the employment decision challenged here, not "
        "on the date of hire, and not on the date Plaintiff first registered "
        "under section 290.",
    ),
    (
        "PARA",
        "23. Plaintiff is informed and believes that the challenged employment "
        "decision — Home Depot's cessation of communication after he accepted "
        "the hire and began onboarding — occurred on or after on or about "
        "August 2024, and in any event within three years before the filing "
        "of this Complaint. The precise day is a fact of Home Depot's "
        "personnel and screening records.",
    ),
    (
        "PARA",
        "24. Plaintiff does not concede that Code of Civil Procedure section "
        "335.1 or section 340, subdivision (a), supplies the limitations period "
        "for the section 290.46(j) count. The actual-damages and discretionary "
        "enhancement authorized by section 290.46(j)(4)(A) are a liability "
        "created by statute under Code of Civil Procedure section 338(a), "
        "not an action upon a statute for a penalty. The "
        "labeled civil-penalty slice is pleaded in the alternative and is not "
        "the sole theory. Those statutes, if raised as affirmative defenses, "
        "will be addressed on the nature of the right sued upon. Plaintiff "
        "does not plead a Tameny or personal-injury count in this Complaint.",
    ),
    (
        "PARA",
        "24A. Civil Code section 1786.52 requires that an ICRAA action be "
        "brought within two years from the date the plaintiff knew or should "
        "have known of the violation. Plaintiff received no Civil Code "
        "section 1786.40 advice and no copy of any Home Depot report. He "
        "could not discover from a notice he never received that an "
        "investigative consumer report had been obtained and used. He knew, "
        "on or about August 2024, that communication had stopped. He did not "
        "then know that an investigative consumer report had actually been "
        "obtained. The precise day communication stopped is a fact of Home "
        "Depot's file. The face of this Complaint does not establish a "
        "discovery date that bars the ICRAA count. If Defendants interpose "
        "section 1786.52, the date is a fact to be proven.",
    ),
    (
        "PARA",
        "24B. The Unfair Competition Law claim is timely under Business and "
        "Professions Code section 17208's four-year period. That period is "
        "independent of any shorter period that may apply to a borrowed "
        "predicate. The UCL count is not pleaded to resurrect a time-barred "
        "statutory right.",
    ),
    ("HEADER", "V.\nCOMMON FACTUAL ALLEGATIONS"),
    ("SUBHEAD", "A. The Tracy Center Hire"),
    (
        "PARA",
        "25. On information and belief, on or about August 2024, Home Depot "
        "hired Plaintiff to work at the Tracy Center, 5395 Hopkins Road, "
        "Tracy, California 95377. Plaintiff accepted that position and began "
        "onboarding. The precise start date, job title, shift, and rate of "
        "pay are facts of Home Depot's personnel file.",
    ),
    (
        "PARA",
        "26. The hire was for work in San Joaquin County. Plaintiff resided in "
        "San Joaquin County and traveled to the Tracy Center for that work.",
    ),
    (
        "PARA",
        "27. Home Depot required Plaintiff to complete, or caused him to be "
        "subjected to, a pre-employment or post-hire background investigation "
        "as a condition of the hire, of continued employment, or of assignment "
        "at the Tracy Center. That is the background check alleged in "
        "paragraphs 1 and 34.",
    ),
    (
        "PARA",
        "28. Plaintiff does not presently possess a written offer letter, "
        "onboarding packet, time records, or wage statements from the Tracy "
        "Center hire. Those documents, if they exist, are in Home Depot's "
        "possession or the possession of its vendors. Their absence from "
        "Plaintiff's files does not negate the hire or the onboarding he began.",
    ),
    ("SUBHEAD", "B. The Employment Decision"),
    (
        "PARA",
        "29. After Plaintiff accepted the hire and began onboarding, Home Depot "
        "ceased communication and ghosted him. That cessation ended or "
        "prevented his work at the Tracy Center. Ghosting after an accepted "
        "hire is an adverse employment action: it denied, withdrew, or ended "
        "the employment. A written termination letter is not an element of "
        "Civil Code section 1786.40, Civil Code section 1785.20.5, or Penal "
        "Code section 290.46(j). Silence after an accepted hire is the "
        "decision. Home Depot sent no written termination, no explanation, "
        "and no further reporting instruction. The precise day communication "
        "stopped is a fact of Home Depot's personnel and screening records.",
    ),
    (
        "PARA",
        "30. To Plaintiff's knowledge, Home Depot did not tell him that the "
        "decision rested on a criminal conviction, a safety incident at the "
        "Tracy Center, a failed drug screen, a falsified application, or any "
        "other independent, lawful, job-related ground. If Home Depot later "
        "asserts such a ground, Plaintiff will test it against the contemporaneous "
        "file.",
    ),
    (
        "PARA",
        "31. On information and belief, Home Depot did not provide Plaintiff, "
        "before the decision, a copy of any consumer report used in the "
        "decision or a written description of his rights under the Fair Credit "
        "Reporting Act. No such package arrived by email, portal, or mail.",
    ),
    (
        "PARA",
        "32. On information and belief, Home Depot did not, at the time of the "
        "decision, advise Plaintiff that an investigative consumer report had "
        "been obtained or supply the name and address of the agency that "
        "prepared it, as Civil Code section 1786.40 requires when employment "
        "is denied under circumstances in which such a report was obtained.",
    ),
    ("SUBHEAD", "C. The Background Report and Home Depot's Use of It"),
    (
        "PARA",
        "33. Plaintiff is a person as to whom information is disclosed on the "
        "California Megan's Law website. That website, and the statute that "
        "created it, warn that the information may not be used for employment.",
    ),
    (
        "PARA",
        "34. Home Depot ran a background check concerning Plaintiff in "
        "connection with the Tracy Center hire. The check was a condition of "
        "the hire, of continued employment, or of assignment at the Tracy "
        "Center.",
    ),
    (
        "PARA",
        "35. Plaintiff is informed and believes, and on that basis alleges, "
        "that the background report that came back contained information "
        "disclosed pursuant to Penal Code section 290.46 concerning Plaintiff, "
        "including his listing on the California Sex Offender Registry, a "
        "Department of Justice website or Megan's Law website result, or a "
        "derivative sex-offender compilation whose source of record was the "
        "California registry.",
    ),
    (
        "PARA",
        "36. Plaintiff is informed and believes, and on that basis alleges, "
        "that Home Depot used that registry information, in whole or in part, "
        "to cease communication, ghost Plaintiff, and make the employment "
        "decision alleged in paragraph 29. The use was a substantial factor "
        "in that decision. The use was a purpose relating to employment. The "
        "basis for paragraphs 35 and 36 is the combination of: the accepted "
        "hire and begun onboarding; Home Depot's background check; Plaintiff's "
        "contemporaneous presence on the California Megan's Law website; the "
        "unexplained ghost; the absence of any other basis communicated to "
        "Plaintiff; and Defendants' exclusive control of the Home Depot report.",
    ),
    (
        "PARA",
        "37. This claim is Home Depot's report and Home Depot's decision. "
        "Plaintiff does not presently know "
        "the legal name of the consumer reporting agency, if any, that "
        "assembled the report. He has sued DOES 1 through 10 for that vendor.",
    ),
    (
        "PARA",
        "38. Home Depot did not give Plaintiff a copy of the report. It did "
        "not identify any independent, lawful, job-related ground for the "
        "decision. On information and belief, it did not tell him that the "
        "report contained registry information. The report remains in "
        "Defendants' possession.",
    ),
    (
        "PARA",
        "39. Taking the allegations in paragraphs 34 through 36 as true, "
        "including those pleaded on information and belief, Plaintiff states "
        "a plausible claim under Penal Code section 290.46(j): Home Depot "
        "used information disclosed pursuant to that section for a purpose "
        "relating to employment, which subdivision (j)(2)(E) prohibits.",
    ),
    (
        "PARA",
        "40. A demurrer admits those well-pleaded facts. It is not an occasion "
        "for Home Depot to substitute a different account of its own "
        "unproduced file. Plaintiff does not allege the report's contents as "
        "a known fact. If production later shows ordinary court records and "
        "no California-registry source, this count will stand or fall on that "
        "record — after production, not before.",
    ),
    (
        "PARA",
        "41. Alternative explanations — a safety incident, a no-show, a failed "
        "drug screen, a lawful criminal-history adjudication under Labor Code "
        "section 432.7 or another authorizing statute, or a business "
        "slowdown — can be tested against a discrete set of records. Plaintiff "
        "will seek the personnel file, time and pay records, background-check "
        "order and report, adjudication notes, and communications of the "
        "decision-maker.",
    ),
    (
        "PARA",
        "42. Penal Code section 290.46(j)(3) does not authorize employment use "
        "of Megan's Law website information merely because an employer may "
        "obtain criminal-history information from another lawful source. A "
        "conviction that appears in ordinary court records is not this claim. "
        "This claim is the use of information disclosed pursuant to section "
        "290.46. Lerma v. Amazon.com Services, LLC, C.D. Cal. No. 8:22-cv-01727, "
        "Dkt. 36, dismissed a Megan's Law count after the employer's report was "
        "in the record and showed ordinary court records and a national "
        "sex-offender search returning no record. That dismissal turned on the "
        "report. This Complaint does not attach Home Depot's report. Plaintiff "
        "does not allege its contents as a known fact. He is informed and "
        "believes, and on that basis alleges, that Home Depot's report "
        "contained registry information and that Home Depot used it. A court "
        "cannot perform a Lerma analysis on the face of a complaint that does "
        "not contain the employer's report. Defendants may not obtain a "
        "pleading-stage dismissal by withholding the one document that would "
        "confirm or refute the inference."
    ),
    ("SUBHEAD", "D. Knowledge, Concealment, and Harm"),
    (
        "PARA",
        "43. Home Depot knew or should have known that employment use of "
        "Megan's Law information is prohibited. The registry website displays "
        "that warning. Home Depot is a sophisticated employer with dedicated "
        "background-check and legal functions. On information and belief, its "
        "vendor contracts and adjudication guides address or should address "
        "California registry restrictions.",
    ),
    (
        "PARA",
        "44. On information and belief, Home Depot did not disclose to "
        "Plaintiff that registry information had been obtained or used, and "
        "thereby deprived him of a meaningful opportunity to inspect the "
        "source, dispute a mismatch, and invoke the statutory remedies before "
        "the decision became final.",
    ),
    (
        "PARA",
        "45. The use was not to protect a person at risk within the meaning of "
        "section 290.46(j)(1). A general warehouse or fulfillment assignment at "
        "the Tracy Center is not, without more, the narrow authorization that "
        "subdivision (j)(1) describes. Plaintiff does not allege facts "
        "bringing any other statutory authorization into play, and Home Depot "
        "has the burden of proving any such authorization as a defense.",
    ),
    (
        "PARA",
        "46. As a result of the decision, Plaintiff lost the Tracy Center "
        "employment, including the opportunity to earn the wages and benefits "
        "of that position, according to proof and subject to mitigation. "
        "Plaintiff also suffered emotional distress, humiliation, and anxiety "
        "from an unexplained employment decision he is informed and believes "
        "rested on a status the Legislature has forbidden employers to use. "
        "Wages earned or lost, if any, will be proven from Home Depot's "
        "records. Plaintiff does not invent a rate or duration here.",
    ),
    (
        "PARA",
        "47. Plaintiff has sought and continues to seek replacement employment "
        "and does not claim a guaranteed lifetime expectancy from an at-will "
        "position. Economic damages will be limited to losses proven with "
        "reasonable certainty and without double recovery against other "
        "dockets that arise from different employers and different decisions.",
    ),
    ("SUBHEAD", "E. Inspection Rights and Why a Demurrer Cannot Replicate Lerma"),
    (
        "PARA",
        "48. The section 290.46(j) claim has four elements: (a) information "
        "disclosed pursuant to section 290.46; (b) use of that information by "
        "a defendant; (c) a purpose relating to employment; and (d) the use "
        "was not to protect a person at risk and was not otherwise authorized "
        "by law. Plaintiff is informed and believes, and on that basis "
        "alleges, each element. On that belief, the report contained "
        "information disclosed pursuant to section 290.46. Home Depot used "
        "that information. The use related to the Tracy Center hire and the "
        "later employment decision. The use was not, without more, protection "
        "of a person at risk. The basis is alleged in paragraphs 1, 3, 5, and "
        "34 through 36. Taking those allegations as true, the claim is "
        "plausible.",
    ),
    (
        "PARA",
        "49. A demurrer tests the pleading, not the unproduced report. "
        "Defendants may deny that the report contained registry information. "
        "They may not convert that denial into a Lerma dismissal while the "
        "report remains in their possession. The First Cause of Action under "
        "Civil Code sections 1786.40 and 1786.50 is independent of the "
        "section 290.46(j) count. A notice failure can reach discovery even "
        "if production later shows a different source of record.",
    ),
    (
        "PARA",
        "50. If Plaintiff was an employee of Home Depot, Labor Code section "
        "1198.5 entitles him to inspect and receive a copy of the personnel "
        "records Home Depot maintained relating to his performance or to any "
        "grievance concerning him. Plaintiff has not yet served a section "
        "1198.5 request. He will. Those records, together with the "
        "background-check order and report, are the discrete set that will "
        "confirm or refute registry use. Their present absence from "
        "Plaintiff's files is not a defect in this pleading.",
    ),
    ("HEADER", "VI.\nFIRST CAUSE OF ACTION"),
    (
        "SUBHEAD",
        "California Investigative Consumer Reporting Agencies Act\n"
        "Civil Code sections 1786.40 and 1786.50 — Against Home Depot and User DOES\n"
        "(Pleaded on Information and Belief)",
    ),
    (
        "PARA",
        "62. Plaintiff realleges paragraphs 1 through 50 and 56 through 60 to "
        "the extent consistent with this cause.",
    ),
    (
        "PARA",
        "63. On information and belief, a consumer reporting agency or "
        "investigative consumer reporting agency assembled or evaluated "
        "information concerning Plaintiff's character, general reputation, "
        "personal characteristics, or mode of living for employment purposes "
        "at Home Depot's request. Civil Code section 1786.2 defines an "
        "investigative consumer report as one in which information on those "
        "subjects is obtained. Plaintiff alleges the product concerned those "
        "subjects. He does not invent personal interviews. If this Court "
        "concludes that interviews are required and none occurred, this "
        "ICRAA count does not apply and the CCRAA count does.",
    ),
    (
        "PARA",
        "64. Home Depot procured or caused that report to be prepared and was "
        "the user of its information.",
    ),
    (
        "PARA",
        "65. On information and belief, the report was obtained before Home "
        "Depot made the employment decision alleged in paragraph 29.",
    ),
    (
        "PARA",
        "66. Civil Code section 1786.40(a) required Home Depot, under "
        "circumstances in which employment was denied or ended and an "
        "investigative consumer report had been obtained, to advise Plaintiff "
        "of that fact and supply the agency's name and address.",
    ),
    (
        "PARA",
        "67. Home Depot did not comply. Plaintiff was not told a report had "
        "been obtained and was not given the agency's name and address.",
    ),
    (
        "PARA",
        "68. The omission caused incremental harm distinct from the denial "
        "itself. Plaintiff could not timely obtain the Home Depot-specific "
        "report, test whether its source was the California registry or "
        "ordinary court records, or invoke his statutory inspection and "
        "dispute rights before the decision became final. Ghosting after "
        "an accepted hire is the adverse action. This ICRAA count does not "
        "depend on proving Penal Code section 290.46(j). A notice failure "
        "under Civil Code section 1786.40 is independently actionable if an "
        "investigative consumer report was obtained and employment was "
        "denied or ended without the required advice. If Defendants "
        "establish that the product was an ordinary consumer credit report "
        "and not investigative, this count does not apply and the CCRAA "
        "count does.",
    ),
    (
        "PARA",
        "69. Under Civil Code section 1786.50, Plaintiff seeks actual damages "
        "or $10,000, whichever is greater, costs, attorney's fees if later "
        "represented, and punitive damages upon proof of gross negligence or "
        "willfulness.",
    ),
    (
        "PARA",
        "70. This ICRAA count is not a Fair Credit Reporting Act count. "
        "Plaintiff has not pleaded 15 U.S.C. section 1681b(b)(3) in this "
        "Complaint. He reserves amendment if production shows Home Depot based "
        "the decision in whole or in part on a consumer report and failed to "
        "provide a copy of the report and a federal rights summary before the "
        "adverse action.",
    ),
    (
        "PARA",
        "71. Plaintiff also reserves amendment under Civil Code section 1786.16 "
        "if production shows Home Depot procured the report before providing "
        "the required standalone disclosure and obtaining written authorization. "
        "He does not presently allege nonauthorization as an established fact. "
        "No Home Depot disclosure form is in Plaintiff's files. On information "
        "and belief, Home Depot did not provide a standalone section 1786.16 "
        "disclosure clearly stating that an investigative consumer report "
        "would include information on character, general reputation, personal "
        "characteristics, or mode of living.",
    ),
    ("HEADER", "VII.\nSECOND CAUSE OF ACTION"),
    (
        "SUBHEAD",
        "California Consumer Credit Reporting Agencies Act\n"
        "Civil Code sections 1785.20.5 and 1785.31 — Against Home Depot and User DOES\n"
        "(Pleaded in the Alternative to ICRAA)",
    ),
    (
        "PARA",
        "71A. Plaintiff realleges paragraphs 1 through 50 and 62 through 71 "
        "to the extent consistent with this cause.",
    ),
    (
        "PARA",
        "71B. In the alternative, if the background report was an ordinary "
        "consumer credit report rather than an investigative consumer report, "
        "the California Consumer Credit Reporting Agencies Act applies. "
        "Civil Code section 1785.20.5 required Home Depot, before procuring "
        "a consumer credit report for employment purposes, to provide written "
        "notice that a report would be used, and, before taking adverse "
        "action based in whole or in part on the report, to provide a copy "
        "of the report and a notice of rights.",
    ),
    (
        "PARA",
        "71C. The file contains no copy of any Home Depot consumer credit "
        "report and no rights notice before the ghosting. No such package "
        "arrived by email, portal, or mail. On information and belief, the "
        "decision was based in whole or in part on the background report "
        "Home Depot obtained.",
    ),
    (
        "PARA",
        "71D. If the report was investigative, this count does not apply and "
        "the ICRAA count does. If it was an ordinary consumer credit report, "
        "the failure to furnish the report and rights notice before adverse "
        "action violated section 1785.20.5.",
    ),
    (
        "PARA",
        "71E. Under Civil Code section 1785.31, Plaintiff seeks actual "
        "damages, costs, attorney's fees if later represented, and punitive "
        "damages upon proof of willfulness, according to proof.",
    ),
    ("HEADER", "VIII.\nTHIRD CAUSE OF ACTION"),
    (
        "SUBHEAD",
        "Unlawful and Unfair Business Practices\n"
        "Business and Professions Code section 17200 — Against All Defendants",
    ),
    (
        "PARA",
        "72. Plaintiff realleges paragraphs 1 through 71E to the extent "
        "consistent with this equitable cause.",
    ),
    (
        "PARA",
        "73. Defendants engaged in unlawful practices by violating, to the "
        "extent proven, Civil Code section 1786.40, Civil Code section "
        "1785.20.5, and Penal Code section 290.46(j)(2)(E).",
    ),
    (
        "PARA",
        "74. Defendants engaged in unfair practices because the gravity of "
        "the harm — ending a Tracy Center hire on a criterion the Legislature "
        "has forbidden, or on a consumer report without the advice the "
        "statute required — outweighs any utility of undoing the hire on "
        "secret registry-derived information while denying the worker the "
        "source, the report, and an opportunity to respond.",
    ),
    (
        "PARA",
        "75. Plaintiff suffered injury in fact and lost money or property "
        "through lost wages from the ended Tracy Center employment, "
        "reliance expenditures, employment-search costs, and other economic "
        "losses to be proven. Injury in fact sufficient for UCL standing is "
        "not the same as recoverable restitution. Plaintiff does not seek "
        "future unearned wages as UCL restitution. He seeks restitution "
        "only of money or property in which he had a vested interest and "
        "that Defendants acquired through the challenged practices — "
        "including, according to proof, reliance expenditures, "
        "employment-search costs, and any vested unpaid wages if the "
        "personnel file later shows earned work. He does not seek "
        "restitution of an abstract value of personal information. He does "
        "not allege that Home Depot holds a fund of unearned future wages.",
    ),
    (
        "PARA",
        "76. Legal damages are not an adequate remedy for Defendants' "
        "retention, use, and dissemination of registry-derived screening data. "
        "On information and belief, Home Depot continues to use the same or "
        "similar standardized screening procedures for California applicants, "
        "including at the Tracy Center.",
    ),
    (
        "PARA",
        "77. That continuing practice is the basis for UCL injunctive relief "
        "and for declaratory relief under Code of Civil Procedure section "
        "1060. Plaintiff seeks an injunction requiring Defendants to cease "
        "prohibited employment use of California registry information at "
        "California facilities including the Tracy Center; preserve and "
        "disclose the source and audit trail of Plaintiff's screening; and "
        "correct or segregate unlawfully used data.",
    ),
    (
        "PARA",
        "78. Plaintiff also seeks restitution of vested money or property "
        "actually acquired, and declaratory relief ancillary to the "
        "injunction, to the extent authorized by Business and Professions "
        "Code section 17203.",
    ),
    ("HEADER", "IX.\nFOURTH CAUSE OF ACTION"),
    (
        "SUBHEAD",
        "Unauthorized Employment Use of Registry Information\n"
        "Penal Code section 290.46(j) — Against All Defendants\n"
        "(Pleaded on Information and Belief — Report Contents and Use)",
    ),
    (
        "PARA",
        "51. Plaintiff realleges paragraphs 1 through 50, except allegations "
        "expressly pleaded in the alternative are incorporated only to the "
        "extent consistent with this cause.",
    ),
    (
        "PARA",
        "52. Penal Code section 290.46(j)(1) authorizes use of information "
        "disclosed under that section only to protect a person at risk, except "
        "as otherwise authorized by law.",
    ),
    (
        "PARA",
        "53. Section 290.46(j)(2)(E) prohibits use of information disclosed "
        "under that section for purposes relating to employment unless another "
        "law authorizes the use.",
    ),
    (
        "PARA",
        "54. Section 290.46(j)(4)(A) makes the user liable for the actual "
        "damages, and any amount that may be determined by a jury or a court "
        "sitting without a jury, not exceeding three times the amount of actual "
        "damage, and not less than two hundred fifty dollars ($250), and "
        "attorney's fees, exemplary damages, or a civil penalty not exceeding "
        "twenty-five thousand dollars ($25,000). Plaintiff seeks the civil "
        "remedies the statute authorizes for unauthorized employment use of "
        "information disclosed pursuant to section 290.46, whether this Court "
        "locates those remedies in subdivision (j)(4)(A) or in another "
        "subdivision of section 290.46. He does not rest this cause on a "
        "criminal-enhancement theory.",
    ),
    (
        "PARA",
        "55. The $25,000 figure in subdivision (j)(4)(A) is a cap on the civil "
        "penalty, not a substitute floor that displaces actual damages. "
        "Plaintiff seeks the remedies the statute authorizes according to proof.",
    ),
    (
        "PARA",
        "56. Each element alleged in paragraph 48 is satisfied on the "
        "information-and-belief basis stated there. Plaintiff is informed and "
        "believes, and on that basis alleges, that Home Depot used information "
        "disclosed pursuant to section 290.46 concerning Plaintiff. The user "
        "is the employer that takes the information into account in making "
        "the employment decision, not a consumer reporting agency that merely "
        "retrieves, scores, or republishes it. Plaintiff does not name a "
        "vendor as a defendant on this count. This count is directed at Home "
        "Depot's use.",
    ),
    (
        "PARA",
        "57. The use related directly to employment: it concerned the Tracy "
        "Center hire or the later decision that ended or prevented Plaintiff's "
        "work there.",
    ),
    (
        "PARA",
        "58. The use was not authorized by section 290.46(j)(1) or by any other "
        "provision of law applicable to this warehouse and fulfillment "
        "assignment.",
    ),
    (
        "PARA",
        "59. Defendants knew or should have known that employment use was "
        "prohibited, for the reasons alleged in paragraph 43.",
    ),
    (
        "PARA",
        "60. Defendants' use was a substantial factor in the employment "
        "decision and caused the loss and injury alleged.",
    ),
    (
        "PARA",
        "61. Plaintiff seeks the remedies authorized by section 290.46(j)(4)(A), "
        "or by whichever subdivision this Court holds supplies the civil "
        "remedy for unauthorized employment use. He does not presently allege "
        "a multi-incident pattern or practice at Home Depot sufficient for "
        "subdivision (j)(4)(B) preventive relief. He seeks that remedy only "
        "if discovery shows reasonable cause to believe such a pattern or "
        "practice. The damages claim under subdivision (j)(4)(A) does not "
        "depend on pattern or practice. Civil Code section 3294 punitive "
        "damages, if any, are pleaded in the alternative to the statute's "
        "exemplary damages or civil penalty for the same conduct. Plaintiff "
        "will elect. He does not seek double punitive recovery.",
    ),
    (
        "PARA",
        "61A. On information and belief, Home Depot's human-resources and "
        "centralized background-adjudication personnel are managing agents "
        "within the meaning of Civil Code section 3294(b): they exercise "
        "substantial discretionary authority over hiring and screening "
        "policy, not merely the power to hire or fire a single applicant. "
        "Those managing agents established, implemented, and ratified the "
        "standardized screening practices alleged. Plaintiff seeks section "
        "3294 punitive damages only upon proof of oppression, fraud, or "
        "malice and of managing-agent authorization, ratification, or "
        "personal participation. ICRAA punitive damages, if any, rest on "
        "Civil Code section 1786.50 and do not depend on section 3294.",
    ),
    ("HEADER", "X.\nPRESERVATION OF EVIDENCE"),
    (
        "PARA",
        "79. Defendants are on notice to preserve Plaintiff's complete Tracy "
        "Center personnel and hiring file, including records subject to Labor "
        "Code section 1198.5; offer, onboarding, badge, time, attendance, and "
        "pay records; the background-check order, disclosure, authorization, "
        "report, component searches, adjudication, access, and cancellation "
        "logs; communications of every person who recommended, approved, or "
        "implemented the employment decision; vendor contracts and "
        "adjudication guides in effect in 2024; and policies governing "
        "Megan's Law, FCRA, ICRAA, and fair-chance review.",
    ),
    (
        "PARA",
        "80. Relevant electronically stored information includes applicant-"
        "tracking and HRIS audit fields, event timestamps, reason codes, "
        "report-view logs, emails, chats, SMS, and data-retention records from "
        "July 1, 2024 through December 31, 2024, and any later date on which "
        "the employment decision was recorded or revisited.",
    ),
    (
        "PARA",
        "81. Home Depot's own background-check file is the document that "
        "will confirm the contents Plaintiff has alleged.",
    ),
    ("HEADER", "XI.\nPRAYER FOR RELIEF"),
    ("PARA", "WHEREFORE, Plaintiff prays for judgment against Defendants as follows:"),
    (
        "LIST_ITEM",
        "1. For actual, consequential, and economic damages according to proof, "
        "without double recovery;",
    ),
    (
        "LIST_ITEM",
        "2. For the remedies authorized by Penal Code section 290.46(j)(4)(A), "
        "including statutory, treble, exemplary, or civil-penalty relief as "
        "the trier of fact and law permit;",
    ),
    (
        "LIST_ITEM",
        "3. For ICRAA actual damages or $10,000, whichever is greater, and "
        "punitive damages upon the showing required by Civil Code section "
        "1786.50, if that count is proven;",
    ),
    (
        "LIST_ITEM",
        "4. For CCRAA actual damages and punitive damages upon the showing "
        "required by Civil Code section 1785.31, if that alternative count "
        "is proven;",
    ),
    (
        "LIST_ITEM",
        "5. For punitive damages under Civil Code section 3294 against only "
        "those Defendants for whom the statutory prerequisites are proven, "
        "pleaded in the alternative to any exemplary damages or civil penalty "
        "awarded under Penal Code section 290.46 for the same conduct, with "
        "no double recovery and no amount pleaded;",
    ),
    (
        "LIST_ITEM",
        "6. For restitution under Business and Professions Code section 17203 "
        "of vested money or property Defendants acquired, not unearned future "
        "wages;",
    ),
    (
        "LIST_ITEM",
        "7. For injunctive relief under Business and Professions Code section "
        "17203, and for Penal Code section 290.46(j)(4)(B) preventive relief "
        "only if discovery shows reasonable cause to believe a pattern or "
        "practice;",
    ),
    (
        "LIST_ITEM",
        "8. For declaratory relief under Code of Civil Procedure section 1060 "
        "concerning whether Defendants' standardized California screening "
        "practices may use information disclosed pursuant to Penal Code "
        "section 290.46 for employment;",
    ),
    (
        "LIST_ITEM",
        "9. For costs of suit and attorney's fees where authorized if Plaintiff "
        "obtains counsel;",
    ),
    (
        "LIST_ITEM",
        "10. For prejudgment and post-judgment interest as allowed by law; and",
    ),
    (
        "LIST_ITEM",
        "11. For such other relief as the Court deems just and proper.",
    ),
    ("HEADER", "XII.\nDEMAND FOR JURY TRIAL"),
    (
        "PARA",
        "82. Plaintiff demands trial by jury on all causes of action and issues "
        "so triable.",
    ),
]


def _signature_block(d: PleadingPaper, exec_date: str, execute: bool) -> None:
    d.ensure_space(12)
    d.write_line(f"Dated: {exec_date}")
    d.blank_line()
    d.write_line("Respectfully submitted,", right=True, right_margin_offset=20)
    d.blank_line()
    d.blank_line()
    if execute:
        d.draw_signature_image(
            SIGNATURE_PATH, SIGNATURE_NATIVE_PX[0], SIGNATURE_NATIVE_PX[1], SIG_LINE
        )
    d.write_line(SIG_LINE, right=True, right_margin_offset=20)
    d.write_line(SIGNOFF_NAME, right=True, right_margin_offset=20)
    d.write_line(SIGNOFF_ROLE, right=True, right_margin_offset=20)


def _verification(d: PleadingPaper, exec_date: str, execute: bool) -> None:
    d.start_new_page()
    d.write_line("VERIFICATION", bold=True, center=True)
    d.blank_line()
    d.write_wrapped("I, BRENDAN NGWA NFORBI, declare:", first_indent=36)
    d.blank_line()
    d.write_wrapped(
        "I am the Plaintiff in this action. I have read the foregoing VERIFIED "
        "COMPLAINT and know its contents. The matters stated are true of my own "
        "knowledge, except those stated on information and belief, and as to those "
        "matters I believe them to be true.",
        first_indent=36,
    )
    d.blank_line()
    d.write_wrapped(
        "I declare under penalty of perjury under the laws of the State of "
        "California that the foregoing is true and correct.",
        first_indent=36,
    )
    d.blank_line()
    d.write_wrapped(
        f"Signed on {exec_date}, at Milpitas, California.", first_indent=36
    )
    d.ensure_space(10)
    d.blank_line()
    d.blank_line()
    if execute:
        d.draw_signature_image(
            SIGNATURE_PATH, SIGNATURE_NATIVE_PX[0], SIGNATURE_NATIVE_PX[1], SIG_LINE
        )
    d.write_line(SIG_LINE, right=True, right_margin_offset=20)
    d.write_line(SIGNOFF_NAME, right=True, right_margin_offset=20)


def build(out: Path, exec_date: str, execute: bool) -> Path:
    if execute and not Path(SIGNATURE_PATH).is_file():
        raise SystemExit(f"Missing universal signature: {SIGNATURE_PATH}")
    out.parent.mkdir(parents=True, exist_ok=True)
    d = PleadingPaper(str(out), doc_title_footer=FOOTER)
    c = d.c

    atty_y = d._line_y(0)
    for i, (txt, font_name, size) in enumerate(PLAINTIFF_BLOCK):
        c.setFont(font_name, size)
        c.drawString(CONTENT_LEFT, atty_y - i * 15, txt)
    d.current_line = 4
    d.blank_line()
    d.write_line(COURT_LINE1, bold=True, center=True)
    d.write_line(COURT_LINE2, bold=True, center=True)
    d.blank_line()
    d.draw_caption_block(
        CAPTION_LEFT, CAPTION_RIGHT, caption_size=8.2, tight_lh=10.5, boxed=True
    )
    d.blank_line()

    for kind, text in CONTENT:
        if kind == "NOTICE":
            if execute:
                continue
            d.ensure_space(7)
            d.write_wrapped(text, bold=True)
            d.blank_line()
        elif kind == "HEADER":
            lines = text.split("\n")
            d.ensure_space(len(lines) + 3)
            for line in lines:
                d.write_line(line, bold=True, center=True)
            d.blank_line()
        elif kind == "SUBHEAD":
            lines = text.split("\n")
            d.ensure_space(len(lines) + 2)
            for line in lines:
                d.write_line(line, bold=True)
            d.blank_line()
        elif kind == "PARA":
            d.write_wrapped(_filing_text(text, execute), first_indent=36)
            d.blank_line()
        elif kind == "LIST_ITEM":
            d.write_wrapped(_filing_text(text, execute), indent=36, first_indent=0)
            d.blank_line()
        else:
            raise ValueError(f"Unknown content kind: {kind}")

    _signature_block(d, exec_date, execute)
    _verification(d, exec_date, execute)
    d.save()
    return out


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("out", nargs="?", default=str(DEFAULT_OUT))
    parser.add_argument("--date", default=DEFAULT_EXEC_DATE)
    parser.add_argument(
        "--execute",
        action="store_true",
        help="Affix Plaintiff's signature and drop review-draft notices",
    )
    args = parser.parse_args()
    path = build(Path(args.out).resolve(), args.date, args.execute)
    print(f"Generated: {path}")


if __name__ == "__main__":
    main()
