#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Matter 37 — verified complaint, Home Depot U.S.A., Inc. (Tracy DC).

San Joaquin Superior Court. Penal Code § 290.46(j) is the load-bearing count.
Registry use is pleaded on information and belief. The Tracy building is the
worksite, not the legal defendant.

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
    ("      §§ 1786.40, 1786.50;", False, False),
    ("(2) UCL, B&P Code § 17200;", False, False),
    ("(3) Penal Code § 290.46(j)", False, False),
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
        "information. On information and belief, on or about August 2024, "
        "Defendant Home Depot U.S.A., Inc. hired Plaintiff to work at its "
        "distribution and fulfillment center at 5395 Hopkins Road, Tracy, "
        "California 95377. Plaintiff accepted that hire and began onboarding. "
        "Thereafter Home Depot ceased communication and ghosted him. Plaintiff "
        "is informed and believes, and on that basis alleges, that Home Depot "
        "used information disclosed pursuant to Penal Code section 290.46 — "
        "Plaintiff's status as "
        "a person required to register under Penal Code section 290, as published "
        "on the California Sex Offender Registry — for purposes relating to that "
        "employment.",
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
        "3. Plaintiff does not allege registry use merely because he is "
        "registered. The inference is pleaded on information and belief and "
        "rests on concrete facts: (a) Home Depot hired Plaintiff; (b) Home Depot "
        "thereafter made an employment decision affecting that hire; (c) Home "
        "Depot is a sophisticated national employer that, on information and "
        "belief, subjects distribution-center hires to standardized background "
        "screening; (d) Plaintiff is, and at the time of the events was, a "
        "person whose identifying information appeared on the California Megan's "
        "Law website; (e) commercial consumer reporting agencies had already "
        "matched this same Plaintiff to the California Sex Offender Registry in "
        "an employment report; (f) Home Depot did not, to Plaintiff's knowledge, "
        "identify to him any independent, lawful, job-related basis for the "
        "decision; and (g) the screening file, adjudication log, and "
        "decision-maker communications are exclusively within Defendants' "
        "possession.",
    ),
    (
        "PARA",
        "4. In July 2024 — the same summer as the Home Depot hire — First "
        "Advantage prepared an employment background report on Plaintiff for "
        "United Parcel Service. That report, later lodged in federal court by "
        "UPS, identified a Department of Justice website / National Sex Offender "
        "Registry search as decisional, stated 'SOURCE OF RECORD: CALIFORNIA "
        "SEX OFFENDER REGISTRY,' and produced an overall INELIGIBLE result. "
        "That report is not alleged to be the Home Depot report. It is alleged "
        "because it shows that, immediately before or contemporaneous with the "
        "Home Depot hire, commercial screeners could and did identify this "
        "Plaintiff through the California registry and treat that identification "
        "as dispositive of employment eligibility.",
    ),
    (
        "PARA",
        "5. The contents, vendor, order time, completion time, transmission, "
        "access log, adjudication status, and reason codes of any Home Depot "
        "background check concerning Plaintiff are exclusively within "
        "Defendants' possession. Plaintiff does not attach a Home Depot report "
        "because he does not have one. He does not allege the contents of that "
        "report as a known fact. Code of Civil Procedure section 425.10 "
        "requires a statement of the facts constituting the cause of action in "
        "ordinary and concise language. Section 452 requires this Court to "
        "construe the pleading liberally with a view to substantial justice "
        "between the parties. Facts exclusively in Defendants' possession are "
        "properly pleaded on information and belief. Plaintiff states the "
        "facts supporting that belief and will seek the report in discovery."
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
        "an IIED count, or a FEHA or Fair Chance Act count. The load-bearing "
        "claim is the statutory prohibition in Penal Code section 290.46(j). "
        "Companion consumer-report and unfair-competition counts are pleaded "
        "only to the extent the same employment use, if proven, also violated "
        "those statutes. Plaintiff preserves all timely rights to seek leave "
        "to amend if discovery supports additional theories.",
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
        "for the section 290.46(j) count. Those statutes, if raised as "
        "affirmative defenses, will be addressed on the nature of the right "
        "sued upon. Plaintiff does not plead a Tameny or personal-injury count "
        "in this Complaint.",
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
        "27. On information and belief, Home Depot required Plaintiff to "
        "complete, or caused him to be subjected to, a pre-employment or "
        "post-hire background investigation as a condition of the hire, of "
        "continued employment, or of assignment at the Tracy Center.",
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
        "prevented his work at the Tracy Center. Home Depot sent no written "
        "termination, no explanation, and no further reporting instruction. "
        "The precise day communication stopped is a fact of Home Depot's "
        "personnel and screening records.",
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
    ("SUBHEAD", "C. Facts Supporting the Registry-Use Inference"),
    (
        "PARA",
        "33. Plaintiff is a person as to whom information is disclosed on the "
        "California Megan's Law website. That website, and the statute that "
        "created it, warn that the information may not be used for employment.",
    ),
    (
        "PARA",
        "34. Home Depot is among the largest private employers in the United "
        "States. On information and belief, it maintains written background-"
        "screening policies for distribution-center and fulfillment associates, "
        "contracts with one or more consumer reporting agencies, and "
        "adjudicates hits through a centralized or regional process rather than "
        "by ad hoc decision of a single Tracy supervisor.",
    ),
    (
        "PARA",
        "35. On information and belief, the ordinary sequence for a Home Depot "
        "Tracy Center hire in 2024 included a background check that searched, "
        "or caused a vendor to search, sex-offender registry or Department of "
        "Justice public-notification sources, including sources that republish "
        "or are derived from California Penal Code section 290.46 disclosures.",
    ),
    (
        "PARA",
        "36. In July 2024, First Advantage Background Services Corp. matched "
        "this Plaintiff to the California Sex Offender Registry on an "
        "employment report ordered by United Parcel Service. The report labeled "
        "the registry component Decisional and the overall result INELIGIBLE, "
        "while a national criminal-file component returned no record. That "
        "document is already in a public court file in the Eastern District of "
        "California, No. 2:26-cv-02847-DAD-CKD.",
    ),
    (
        "PARA",
        "37. The First Advantage/UPS report is alleged for three limited "
        "purposes: it shows that Plaintiff's registry status was commercially "
        "retrievable for employment screening in the same season as the Home "
        "Depot hire; it shows that at least one national CRA treated a "
        "California-registry source as an employment-eligibility bar for this "
        "Plaintiff; and it identifies the kind of record Home Depot's own "
        "vendor, whoever that vendor was, would have been able to return. "
        "Plaintiff does not allege that First Advantage was Home Depot's vendor, "
        "and does not allege that UPS sent its report to Home Depot.",
    ),
    (
        "PARA",
        "38. On information and belief, Home Depot or its vendor obtained, "
        "accessed, displayed, scored, or was informed of information disclosed "
        "pursuant to Penal Code section 290.46 concerning Plaintiff — including "
        "a California Sex Offender Registry listing, a Department of Justice "
        "website result, or a derivative national sex-offender compilation "
        "whose source of record was the California registry — in connection "
        "with the Tracy Center hire or the later employment decision.",
    ),
    (
        "PARA",
        "39. On information and belief, Home Depot used that information for "
        "purposes relating to employment when it made the decision alleged in "
        "paragraph 29. The use was a substantial factor in the decision.",
    ),
    (
        "PARA",
        "40. The basis for paragraphs 38 and 39 is the combination of: the "
        "hire; the subsequent employment decision; Home Depot's ordinary "
        "screening practice; Plaintiff's contemporaneous presence on the "
        "California registry; the demonstrated commercial retrievability of "
        "that listing in July 2024; the absence of any other basis communicated "
        "to Plaintiff; and Home Depot's exclusive control of the file that will "
        "confirm or refute the inference.",
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
        "report. This Complaint does not attach Home Depot's report. A court "
        "cannot perform a Lerma analysis on the face of a complaint that does "
        "not contain the employer's report. Defendants may not obtain a "
        "pleading-stage dismissal by withholding the one document that would "
        "confirm or refute the inference. Plaintiff pleads the opposite "
        "inference here. If production shows ordinary court records and no "
        "California-registry source, this count will stand or fall on that "
        "record — after production, not before."
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
        "by law. Plaintiff pleads each element. Elements (a) and (b) are "
        "pleaded on information and belief because the report, the "
        "source-of-record line, and the adjudication code are exclusively in "
        "Defendants' files. Elements (c) and (d) follow from the Tracy Center "
        "hire and the later employment decision, which are purposes relating "
        "to employment and are not, without more, protection of a person at "
        "risk.",
    ),
    (
        "PARA",
        "49. A demurrer tests the pleading, not the unproduced report. "
        "Defendants may deny registry use. They may not convert that denial "
        "into a Lerma dismissal while the report remains in their possession. "
        "The Second Cause of Action under Civil Code sections 1786.40 and "
        "1786.50 is independent of the registry-use inference. A notice "
        "failure can reach discovery even if the section 290.46(j) count "
        "later fails on the contents of the report.",
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
        "at Home Depot's request.",
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
        "68. The omission prevented Plaintiff from timely obtaining the Home "
        "Depot-specific report, testing whether its source was the California "
        "registry or ordinary court records, and invoking his statutory "
        "inspection and dispute rights. This ICRAA count does not depend on "
        "proving Penal Code section 290.46(j). A notice failure under Civil "
        "Code section 1786.40 is independently actionable if an investigative "
        "consumer report was obtained and employment was denied or ended "
        "without the required advice. That count can reach discovery even if "
        "the registry-use inference later fails.",
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
        "He does not presently allege nonauthorization as an established fact.",
    ),
    ("HEADER", "VII.\nSECOND CAUSE OF ACTION"),
    (
        "SUBHEAD",
        "Unlawful and Unfair Business Practices\n"
        "Business and Professions Code section 17200 — Against All Defendants",
    ),
    (
        "PARA",
        "72. Plaintiff realleges paragraphs 1 through 71 to the extent "
        "consistent with this equitable cause.",
    ),
    (
        "PARA",
        "73. Defendants engaged in unlawful practices by violating Penal Code "
        "section 290.46(j) and, if proven, Civil Code section 1786.40, as "
        "alleged.",
    ),
    (
        "PARA",
        "74. Defendants engaged in unfair practices by structuring employment "
        "screening so a hire at the Tracy Center could be undone on secret "
        "registry-derived information while denying the worker the source, "
        "the report, and an opportunity to respond.",
    ),
    (
        "PARA",
        "75. Plaintiff suffered injury in fact and lost money or property "
        "through lost wages from the ended Tracy Center employment and other "
        "economic losses to be proven. Plaintiff does not seek future unearned "
        "wages as UCL restitution. He seeks restitution only of money or "
        "property in which he had a vested interest and that Defendants "
        "acquired or caused him to lose through the challenged practices.",
    ),
    (
        "PARA",
        "76. Legal damages are not an adequate remedy for Defendants' "
        "retention, use, and dissemination of registry-derived screening data "
        "or their ongoing employment-screening practices.",
    ),
    (
        "PARA",
        "77. Plaintiff seeks an injunction requiring Defendants to cease "
        "prohibited employment use of California registry information at "
        "California facilities including the Tracy Center; preserve and "
        "disclose the source and audit trail of Plaintiff's screening; and "
        "correct or segregate unlawfully used data.",
    ),
    (
        "PARA",
        "78. Plaintiff also seeks restitution and declaratory relief ancillary "
        "to the injunction to the extent authorized by Business and Professions "
        "Code section 17203.",
    ),
    ("HEADER", "VIII.\nTHIRD CAUSE OF ACTION"),
    (
        "SUBHEAD",
        "Unauthorized Employment Use of Registry Information\n"
        "Penal Code section 290.46(j) — Against All Defendants",
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
        "twenty-five thousand dollars ($25,000).",
    ),
    (
        "PARA",
        "55. The $25,000 figure in subdivision (j)(4)(A) is a cap on the civil "
        "penalty, not a substitute floor that displaces actual damages. "
        "Plaintiff seeks the remedies the statute authorizes according to proof.",
    ),
    (
        "PARA",
        "56. On information and belief, each element alleged in paragraph 48 "
        "is satisfied. Home Depot, and such DOE Defendants as ordered, "
        "furnished, scored, or acted on the report, used information disclosed "
        "pursuant to section 290.46 concerning Plaintiff.",
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
        "including actual and statutory relief according to proof, and "
        "preventive relief under subdivision (j)(4)(B) to restrain any pattern "
        "or practice of employment use of Megan's Law information at Home "
        "Depot's California facilities, including the Tracy Center.",
    ),
    ("HEADER", "IX.\nPRESERVATION OF EVIDENCE"),
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
        "81. The July 2024 First Advantage/UPS report is relevant to "
        "retrievability and matching methodology. It is not a substitute for "
        "Home Depot's own file.",
    ),
    ("HEADER", "X.\nPRAYER FOR RELIEF"),
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
        "4. For punitive damages against only those Defendants for whom Civil "
        "Code section 3294 is proven, in an amount to be determined by the "
        "trier of fact, with no amount pleaded;",
    ),
    (
        "LIST_ITEM",
        "5. For restitution under Business and Professions Code section 17203 "
        "to the extent available;",
    ),
    (
        "LIST_ITEM",
        "6. For preventive and injunctive relief under Penal Code section "
        "290.46(j)(4)(B), Business and Professions Code section 17203, and "
        "other applicable law;",
    ),
    (
        "LIST_ITEM",
        "7. For declaratory relief concerning Defendants' prohibited registry "
        "use to the extent an actual controversy remains;",
    ),
    (
        "LIST_ITEM",
        "8. For costs of suit and attorney's fees where authorized if Plaintiff "
        "obtains counsel;",
    ),
    (
        "LIST_ITEM",
        "9. For prejudgment and post-judgment interest as allowed by law; and",
    ),
    (
        "LIST_ITEM",
        "10. For such other relief as the Court deems just and proper.",
    ),
    ("HEADER", "XI.\nDEMAND FOR JURY TRIAL"),
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
