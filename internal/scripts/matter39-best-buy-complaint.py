#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Matter 39 — verified complaint, Best Buy Co., Inc. / First Advantage.

San Joaquin Superior Court. Penal Code § 290.46(j) is the load-bearing count.
The October 17, 2023 warehouse offer, background authorization, and First
Advantage drug-test order are in the file. The employment decision and the
background report are not. Registry use is information and belief.

Default output is unsigned. On or after September 8, 2026, rerun with
``--execute`` only after Plaintiff confirms the decision, the notices, and
whether he signed the offer or completed the drug screen.

    python3 internal/scripts/matter39-best-buy-complaint.py
    python3 internal/scripts/matter39-best-buy-complaint.py --execute
"""

from __future__ import annotations

import argparse
import datetime as dt
import sys
from pathlib import Path

SCRIPT_DIR = Path(__file__).resolve().parent
sys.path.insert(0, str(SCRIPT_DIR / "lib"))
sys.path.insert(0, str(SCRIPT_DIR))

from pleading_paper import CONTENT_LEFT, COURT_LINE1, PleadingPaper  # noqa: E402
from signature_stamp import SIGNATURE_NATIVE_PX, SIGNATURE_PATH  # noqa: E402

ROOT = SCRIPT_DIR.parents[1]
DEFAULT_OUT = (
    ROOT
    / "internal/public/documents/matter-39"
    / "Verified Complaint - Newanforbi v Best Buy Co Inc et al"
    " (REVIEW DRAFT for Sep 8 2026).pdf"
)
DEFAULT_EXEC_DATE = "September 8, 2026"
EARLIEST_EXECUTION_DATE = dt.date(2026, 9, 8)
COURT_LINE2 = "COUNTY OF SAN JOAQUIN"
FOOTER = "VERIFIED COMPLAINT -- NEWANFORBI v. BEST BUY CO., INC."

PLAINTIFF_BLOCK = [
    ("BRENDAN NGEHSI NEWANFORBI", "Times-Bold", 12),
    ("Plaintiff, In Propria Persona", "Times-Roman", 12),
    ("1455 Cat Tail Drive", "Times-Roman", 12),
    ("Stockton, CA 95204", "Times-Roman", 12),
    ("Telephone: (209) 801-4442", "Times-Roman", 12),
    ("E-mail: bnn.cdl@gmail.com", "Times-Roman", 12),
]

CAPTION_LEFT = [
    ("BRENDAN NGEHSI NEWANFORBI,", True, False),
    ("", False, False),
    ("                          Plaintiff,", False, False),
    ("", False, False),
    ("       v.", False, False),
    ("", False, False),
    ("BEST BUY CO., INC., a Minnesota", True, False),
    ("corporation, d/b/a BEST BUY;", True, False),
    ("FIRST ADVANTAGE BACKGROUND", True, False),
    ("SERVICES CORP., a Florida", True, False),
    ("corporation; and DOES 1 through", True, False),
    ("20, inclusive,", True, False),
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
    ("(1) Penal Code § 290.46(j);", False, False),
    ("(2) ICRAA, Civ. Code", False, False),
    ("      §§ 1786.40, 1786.50;", False, False),
    ("(3) UCL, B&P Code § 17200", False, False),
    ("", False, False),
    ("[Unlimited Civil]", False, True),
    ("[Jury Trial Demanded]", False, True),
]

SIGNOFF_NAME = "BRENDAN NGEHSI NEWANFORBI"
SIGNOFF_ROLE = "Plaintiff, In Propria Persona"
SIG_LINE = "___________________________________"

CONTENT = [
    (
        "NOTICE",
        "REVIEW DRAFT — DO NOT FILE OR SIGN BEFORE SEPTEMBER 8, 2026. "
        "PLAINTIFF MUST CONFIRM WHAT HAPPENED AFTER THE OCTOBER 17, 2023 "
        "OFFER — DENIED, GHOSTED, OFFER WITHDRAWN, OR OTHER — AND ON WHAT "
        "DAY; WHETHER HE SIGNED THE OFFER OR COMPLETED THE DRUG SCREEN; "
        "WHETHER ANY PRE-ADVERSE OR ADVERSE NOTICE ARRIVED; AND THE "
        "WAREHOUSE LOCATION. NO REJECTION LETTER IS IN THE FILE.",
    ),
    ("PARA", 'Plaintiff BRENDAN NGEHSI NEWANFORBI ("Plaintiff") alleges as follows:'),
    ("HEADER", "I.\nINTRODUCTION"),
    (
        "PARA",
        "1. This is an action under Penal Code section 290.46, subdivision (j), "
        "for the unauthorized employment use of California Megan's Law registry "
        "information. On October 13, 2023, Plaintiff applied to Best Buy for "
        "General Warehouse Worker / 2nd Shift at $22.60, requisition 928556BR. "
        "On October 17, 2023, Best Buy offered him that job, required a "
        "background check, and through First Advantage ordered a drug test. "
        "Thereafter Best Buy made an employment decision concerning that offer. "
        "No written rejection is in Plaintiff's files.",
    ),
    (
        "PARA",
        "2. Plaintiff is informed and believes, and on that basis alleges, that "
        "Best Buy used information disclosed pursuant to Penal Code section "
        "290.46 — Plaintiff's status as a person required to register under "
        "Penal Code section 290, as published on the California Sex Offender "
        "Registry — for purposes relating to that employment.",
    ),
    (
        "PARA",
        "3. Penal Code section 290.46(j)(1) authorizes use of information "
        "disclosed under that section only to protect a person at risk. "
        "Subdivision (j)(2)(E) prohibits use of that information for purposes "
        "relating to employment, except as another law authorizes. A warehouse "
        "hiring, continuation, or revocation-of-offer decision is a purpose "
        "relating to employment.",
    ),
    (
        "PARA",
        "4. Plaintiff does not allege registry use merely because he is "
        "registered. The inference rests on concrete facts: (a) Best Buy "
        "offered him the warehouse job; (b) Best Buy required a consumer "
        "report and investigative consumer report as a condition of that "
        "offer; (c) First Advantage was the named screening vendor and "
        "ordered the drug test the same afternoon; (d) Plaintiff was then "
        "listed on the California Megan's Law website; (e) First Advantage "
        "had already shown, on another employer's report, that it could match "
        "this same Plaintiff to the California Sex Offender Registry and treat "
        "that match as dispositive; (f) Best Buy did not, to Plaintiff's "
        "knowledge, identify any independent, lawful, job-related basis for "
        "undoing the offer; and (g) the screening file is exclusively within "
        "Defendants' possession.",
    ),
    (
        "PARA",
        "5. In July 2024, First Advantage prepared an employment background "
        "report on Plaintiff for United Parcel Service. That report, later "
        "lodged in federal court by UPS, identified a Department of Justice "
        "website / National Sex Offender Registry search as decisional, stated "
        "'SOURCE OF RECORD: CALIFORNIA SEX OFFENDER REGISTRY,' and produced "
        "an overall INELIGIBLE result. That report is not the Best Buy report. "
        "It is alleged because the same vendor that Best Buy used in October "
        "2023 later matched this Plaintiff to the California registry and "
        "treated that match as an employment bar. The UPS report is "
        "methodology and matchability evidence — the same CRA, the same "
        "Plaintiff, a California-registry source of record — not the Best "
        "Buy report and not a substitute for it."
    ),
    (
        "PARA",
        "6. Plaintiff does not name Best Buy Stores, L.P., or any other "
        "affiliate, as a present defendant merely because warehouse workers "
        "are sometimes employed by an operating partnership. He has sued "
        "DOES 11 through 15 for the actual employing or decision-making "
        "Best Buy entity. He does not name First Advantage Corporation, the "
        "publicly traded parent, merely because it owns First Advantage "
        "Background Services Corp.",
    ),
    (
        "PARA",
        "7. This Complaint does not plead a Tameny count, an IIED count, a "
        "Fair Credit Reporting Act count, a contract or promissory-estoppel "
        "count, or a FEHA or Fair Chance Act count. The load-bearing claim is "
        "Penal Code section 290.46(j). Companion consumer-report and "
        "unfair-competition counts are pleaded only to the extent the same "
        "employment use, if proven, also violated those statutes. Plaintiff "
        "preserves all timely rights to seek leave to amend.",
    ),
    ("HEADER", "II.\nPARTIES"),
    (
        "PARA",
        "8. Plaintiff BRENDAN NGEHSI NEWANFORBI is a natural person residing in "
        "Stockton, San Joaquin County, California. He is also identified in "
        "employment and court records as Brendan Ngwa Nforbi and Brendan "
        "Ngehsi Ngwanforbi. Those name variants refer to Plaintiff. The "
        "October 17, 2023 First Advantage drug-test order used BRENDAN NGWA "
        "NFORBI.",
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
        "10. Defendant BEST BUY CO., INC. ('Best Buy') is a corporation "
        "organized under the laws of the State of Minnesota, doing business "
        "as Best Buy. The October 17, 2023 background-check authorization "
        "identifies 'Best Buy and/or its subsidiaries, affiliates other "
        "related entities, successors, and/or assigns' as the 'Company,' and "
        "directs New York correspondence to Best Buy Co. Inc., ATTN: "
        "Employment Screening, 7601 Penn Ave. South, Richfield, MN 55423. "
        "The First Advantage drug-test order lists the employer as BEST BUY, "
        "same Richfield address. On information and belief, Best Buy Co., "
        "Inc. offered Plaintiff the warehouse job and caused the background "
        "check and drug test to be ordered.",
    ),
    (
        "PARA",
        "11. The October 13 and October 17, 2023 emails do not state the "
        "street address of the warehouse. A Quest Diagnostics collection site "
        "in Modesto, California, appears on the drug-test order as one "
        "available site. That is a collection option, not a pleaded worksite. "
        "Plaintiff does not invent a distribution-center address. "
        "[PLAINTIFF MUST CONFIRM THE WAREHOUSE CITY AND WHETHER HE EVER "
        "REPORTED THERE.]",
    ),
    (
        "PARA",
        "12. Defendant FIRST ADVANTAGE BACKGROUND SERVICES CORP. "
        "('First Advantage') is a Florida corporation that provides employment "
        "background reports and screening services. Best Buy's October 17, "
        "2023 Minnesota disclosure named First Advantage Consumer Center, "
        "P.O. Box 105292, Atlanta, GA 30348-5292, (800) 845-6004, "
        "www.FADV.com. The same afternoon First Advantage Corporation "
        "Reporting Service emailed Plaintiff a Best Buy drug-test order, "
        "Re:Quest QPassport/Barcode Q09078711, account BEST BUY (11759586), "
        "and stated that the employer had been sent a copy. On information "
        "and belief, First Advantage was the consumer reporting agency that "
        "assembled or was to assemble the Best Buy employment report.",
    ),
    (
        "PARA",
        "13. On information and belief, Best Buy's designated agent for "
        "service of process in California is the agent listed on the "
        "California Secretary of State record as of the date of service. "
        "Plaintiff will serve Best Buy and First Advantage through those "
        "current agents. Service is not to be made at a warehouse or at "
        "Jose Tapia's telephone number merely because he signed the offer "
        "email.",
    ),
    (
        "PARA",
        "14. Jose Tapia identified himself as General Manager on the October "
        "17, 2023 offer email and listed 720-539-4284. He is a percipient "
        "witness, not presently named as a defendant. Daisy Calvary "
        "(daisy.calvary@bestbuy.com) was named as a drug-screen contact. She "
        "is likewise a witness.",
    ),
    (
        "PARA",
        "15. The true names and capacities of DOES 1 through 20 are unknown to "
        "Plaintiff, who therefore sues them by fictitious names under Code of "
        "Civil Procedure section 474. DOES 1 through 10 include any First "
        "Advantage furnishing affiliate and the individuals who ordered, "
        "reviewed, or acted on the report. DOES 11 through 15 include Best "
        "Buy Stores, L.P., or any other Best Buy affiliate that was the "
        "actual employing or decision-making entity. Plaintiff will amend "
        "when their identities and roles are ascertained.",
    ),
    (
        "PARA",
        "16. Plaintiff is informed and believes that each DOE Defendant "
        "participated in, authorized, directed, furnished information for, "
        "implemented, concealed, or ratified one or more acts alleged and is "
        "legally responsible for the resulting harm.",
    ),
    ("HEADER", "III.\nJURISDICTION AND VENUE"),
    (
        "PARA",
        "17. This Court has subject-matter jurisdiction under article VI, "
        "section 10 of the California Constitution and Code of Civil Procedure "
        "section 410.10.",
    ),
    (
        "PARA",
        "18. This action is properly designated unlimited civil under Code of "
        "Civil Procedure sections 85 and 88 because the aggregate relief sought "
        "exceeds $35,000, exclusive of interest and costs. No specific "
        "personal-injury or punitive-damages amount is pleaded.",
    ),
    (
        "PARA",
        "19. This Court has personal jurisdiction over Best Buy because Best "
        "Buy recruited and offered employment to a California resident, "
        "required a California background-check authorization, and caused a "
        "drug test to be ordered at California collection sites, including a "
        "Modesto option. This Court has personal jurisdiction over First "
        "Advantage because it furnished or was to furnish an employment "
        "report about a California resident for a California job and emailed "
        "the drug-test order to Plaintiff in California.",
    ),
    (
        "PARA",
        "20. Venue is proper in the County of San Joaquin under Code of Civil "
        "Procedure sections 395 and 395.5 because Plaintiff resides here, he "
        "received the application confirmation, the offer, the authorization "
        "copy, and the drug-test order here, and the liability and injury "
        "arose here.",
    ),
    (
        "PARA",
        "21. Plaintiff has not pleaded a federal claim. This Complaint is a "
        "California statutory action belonging in this Court.",
    ),
    ("HEADER", "IV.\nTIMELINESS"),
    (
        "PARA",
        "22. Penal Code section 290.46 does not prescribe its own limitations "
        "period. This action upon a liability created by that statute is timely "
        "under Code of Civil Procedure section 338, subdivision (a), which "
        "requires that such an action, other than a penalty or forfeiture, be "
        "commenced within three years after accrual.",
    ),
    (
        "PARA",
        "23. The cause of action accrued, if at all, when Best Buy used "
        "registry information for purposes relating to Plaintiff's employment "
        "— that is, on the date of the employment decision after the October "
        "17, 2023 offer, not on the application date, and not on the date "
        "Plaintiff first registered under section 290.",
    ),
    (
        "PARA",
        "24. The file does not contain a dated rejection. On information and "
        "belief, the decision occurred on or after October 17, 2023, and in "
        "any event within three years before the filing of this Complaint. "
        "Three years from October 17, 2023, is October 17, 2026. This "
        "Complaint is prepared for execution on September 8, 2026. "
        "[PLAINTIFF MUST CONFIRM THE DECISION DATE BEFORE EXECUTION.]",
    ),
    (
        "PARA",
        "25. Plaintiff does not concede that Code of Civil Procedure section "
        "335.1 or section 340, subdivision (a), supplies the limitations period "
        "for the section 290.46(j) count. He does not plead a Tameny or "
        "personal-injury count. A two-year clock from an October 2023 decision "
        "would have closed in October 2025. He has not pleaded the Fair Credit "
        "Reporting Act.",
    ),
    ("HEADER", "V.\nCOMMON FACTUAL ALLEGATIONS"),
    ("SUBHEAD", "A. The Application and the Offer"),
    (
        "PARA",
        "26. On Friday, October 13, 2023, at 7:29 a.m., Best Buy Human "
        "Resources emailed Plaintiff that it had received his submission for "
        "General Warehouse Worker / 2nd Shift at $22.60, requisition 928556BR. "
        "The email described the work as loading, unloading, and processing "
        "merchandise, moving product inside a distribution center, and using "
        "forklifts and other powered equipment, with a basic qualification of "
        "lifting up to 75 pounds.",
    ),
    (
        "PARA",
        "27. On Tuesday, October 17, 2023, at 3:47 p.m., Best Buy emailed "
        "'Congratulations! Please Review Your Job Offer from Best Buy!' The "
        "body stated: 'Congratulations on receiving an offer for General "
        "Warehouse Worker/2nd Shift @ $22.60 from Best Buy!' It required, "
        "within 24 hours: (1) review and sign the offer paperwork in the "
        "Candidate Zone using brennforbi@gmail.com; (2) provide additional "
        "information used to complete the background check; and (3) review "
        "and agree to the required background-check terms. The sender block "
        "was Jose Tapia, General Manager, 720-539-4284. Attached files were "
        "named DISCLOSURE REGARDING BACKGROUND CHECKS.pdf and CALIFORNIA "
        "STATE LAW DISCLOSURE.pdf.",
    ),
    (
        "PARA",
        "28. The signed offer, the Candidate Zone acceptance audit, and the "
        "two attached disclosure PDFs are not in Plaintiff's present files. "
        "Plaintiff does not allege that he signed, or that he refused to "
        "sign, as a known fact. "
        "[PLAINTIFF MUST CONFIRM WHETHER HE SIGNED THE OFFER AND COMPLETED "
        "THE CANDIDATE ZONE TASKS.]",
    ),
    ("SUBHEAD", "B. The Background Authorization and the Drug Test"),
    (
        "PARA",
        "29. On October 17, 2023, at 4:22 p.m., Best Buy emailed a Background "
        "Authorization Consent Confirmation to brennforbi@gmail.com. The "
        "confirmation recites that Plaintiff consented to Best Buy procuring "
        "consumer reports, which may include criminal background checks and "
        "investigative consumer reports as defined by California law, from a "
        "CRA or ICRA, and that the authorization would remain valid throughout "
        "employment.",
    ),
    (
        "PARA",
        "30. That confirmation includes a Minnesota disclosure naming First "
        "Advantage Consumer Center as the place to request a complete and "
        "accurate disclosure of the nature and scope of any consumer report, "
        "and a New York disclosure directing written requests to Best Buy "
        "Co. Inc., Employment Screening, 7601 Penn Ave. South, Richfield, "
        "MN 55423.",
    ),
    (
        "PARA",
        "31. Eight minutes later, at 4:30 p.m., First Advantage Corporation "
        "Reporting Service emailed 'First Advantage Corporation: BRENDAN NGWA "
        "NFORBI Best Buy Drug Test.' The order registration was Q09078711, "
        "request date October 17, 2023, 7:29 p.m. It stated: 'You are required "
        "to complete a drug test as a condition of your offer of employment "
        "from Best Buy,' and that the employer had been sent a copy. The "
        "account was BEST BUY (11759586). A listed collection site was Quest "
        "Diagnostics-Modesto, 1008 6th Street Ste C, Modesto, CA 95354.",
    ),
    (
        "PARA",
        "32. At 5:31 p.m., Best Buy Human Resources emailed a 'Best Buy Drug "
        "Screen: Reminder' stating: 'Congratulations on accepting your offer "
        "with Best Buy!' and that the drug screen had been successfully "
        "ordered, with instructions pointing to the First Advantage email. "
        "The reminder's 'accepting your offer' sentence is Best Buy's "
        "characterization. Plaintiff does not treat that sentence as a "
        "substitute for the Candidate Zone signature audit. "
        "[PLAINTIFF MUST CONFIRM WHETHER HE COMPLETED THE DRUG TEST AND "
        "WHAT RESULT, IF ANY, HE WAS TOLD.]",
    ),
    (
        "PARA",
        "33. Plaintiff does not allege that a failed drug test was the reason "
        "for any later decision. He does not know the result. A drug-test "
        "order is not a Penal Code section 290.46 disclosure.",
    ),
    ("SUBHEAD", "C. The Employment Decision"),
    (
        "PARA",
        "34. After the October 17, 2023 offer and screen, Best Buy made an "
        "employment decision concerning Plaintiff. On information and belief, "
        "that decision was a revocation of the offer, a refusal to finalize "
        "employment, a termination of the application, or other adverse action "
        "that ended or prevented the warehouse job. The file contains no "
        "pre-adverse letter, no adverse-action letter, and no explanation. "
        "[PLAINTIFF MUST CONFIRM WHAT HAPPENED AND ON WHAT DAY.]",
    ),
    (
        "PARA",
        "35. To Plaintiff's knowledge, Best Buy did not tell him that the "
        "decision rested on a failed drug screen, a safety incident, a "
        "falsified application, a criminal conviction drawn from ordinary "
        "court records, or any other independent, lawful, job-related ground. "
        "If Best Buy later asserts such a ground, Plaintiff will test it "
        "against the contemporaneous file.",
    ),
    (
        "PARA",
        "36. On information and belief, Best Buy did not advise Plaintiff that "
        "an investigative consumer report had been obtained or supply the "
        "name and address of the agency that prepared it, as Civil Code "
        "section 1786.40 requires when employment is denied under "
        "circumstances in which such a report was obtained. "
        "[PLAINTIFF MUST CONFIRM THAT NO PRE-ADVERSE OR ADVERSE PACKAGE "
        "ARRIVED BY EMAIL, PORTAL, OR MAIL.]",
    ),
    ("SUBHEAD", "D. Facts Supporting the Registry-Use Inference"),
    (
        "PARA",
        "37. Plaintiff is a person as to whom information is disclosed on the "
        "California Megan's Law website. That website, and the statute that "
        "created it, warn that the information may not be used for employment.",
    ),
    (
        "PARA",
        "38. Best Buy is among the largest consumer-electronics retailers in "
        "the United States and operates distribution centers that feed its "
        "stores. On information and belief, it maintains written background-"
        "screening policies for warehouse associates, contracts with First "
        "Advantage, and adjudicates hits through a centralized process rather "
        "than by ad hoc decision of a single general manager.",
    ),
    (
        "PARA",
        "39. On information and belief, the ordinary Best Buy warehouse screen "
        "in 2023 included a search, or caused First Advantage to search, "
        "sex-offender registry or Department of Justice public-notification "
        "sources, including sources that republish or are derived from "
        "California Penal Code section 290.46 disclosures.",
    ),
    (
        "PARA",
        "40. The July 2024 First Advantage / UPS report is alleged for three "
        "limited purposes: it shows that Plaintiff's registry status was "
        "commercially retrievable by this same vendor; it shows that First "
        "Advantage treated a California-registry source as an employment-"
        "eligibility bar for this Plaintiff; and it identifies the kind of "
        "record First Advantage would have been able to return to Best Buy. "
        "Plaintiff does not allege that UPS sent its report to Best Buy.",
    ),
    (
        "PARA",
        "41. On information and belief, Best Buy or First Advantage obtained, "
        "accessed, displayed, scored, or was informed of information disclosed "
        "pursuant to Penal Code section 290.46 concerning Plaintiff — including "
        "a California Sex Offender Registry listing, a Department of Justice "
        "website result, or a derivative national sex-offender compilation "
        "whose source of record was the California registry — in connection "
        "with the warehouse offer or the later employment decision.",
    ),
    (
        "PARA",
        "42. On information and belief, Best Buy used that information for "
        "purposes relating to employment when it made the decision alleged in "
        "paragraph 34. The use was a substantial factor in the decision. "
        "First Advantage furnished or scored the information for that use.",
    ),
    (
        "PARA",
        "43. The basis for paragraphs 41 and 42 is the combination of: the "
        "written offer; the same-day background authorization and First "
        "Advantage drug-test order; First Advantage's role as Best Buy's "
        "named CRA; Plaintiff's contemporaneous presence on the California "
        "registry; First Advantage's later documented match of this Plaintiff "
        "to SOURCE OF RECORD: CALIFORNIA SEX OFFENDER REGISTRY; the absence "
        "of any other basis communicated to Plaintiff; and Defendants' "
        "exclusive control of the Best Buy report.",
    ),
    (
        "PARA",
        "44. Alternative explanations — a failed drug screen, a no-show at "
        "collection, a Candidate Zone non-completion, a lawful criminal-"
        "history adjudication under a statute that actually authorizes the "
        "use, or a withdrawn requisition — can be tested against a discrete "
        "set of records. Plaintiff will seek the Candidate Zone audit, the "
        "First Advantage order and report, the drug-test result, adjudication "
        "notes, and communications of Tapia and Employment Screening.",
    ),
    (
        "PARA",
        "45. Lerma v. Amazon.com Services, LLC, C.D. Cal. No. 8:22-cv-01727, "
        "Dkt. 36, dismissed a Megan's Law count after the employer's report was "
        "in the record and showed ordinary court records and a national "
        "sex-offender search returning no record. That dismissal turned on the "
        "report. This Complaint does not attach the Best Buy First Advantage "
        "report. Plaintiff does not allege its contents as a known fact. A "
        "court cannot perform a Lerma analysis on the face of a complaint that "
        "does not contain the employer's report. Defendants may not obtain a "
        "pleading-stage dismissal by withholding the one document that would "
        "confirm or refute the inference. Plaintiff pleads the opposite "
        "inference here. If production shows ordinary court records and no "
        "California-registry source, this count will stand or fall on that "
        "record — after production, not before."
    ),
    (
        "PARA",
        "46. The use was not to protect a person at risk within the meaning of "
        "section 290.46(j)(1). A general warehouse assignment is not, without "
        "more, the narrow authorization that subdivision (j)(1) describes. "
        "Defendants have the burden of proving any other statutory "
        "authorization as a defense.",
    ),
    ("SUBHEAD", "E. Knowledge, Concealment, and Harm"),
    (
        "PARA",
        "47. Best Buy and First Advantage knew or should have known that "
        "employment use of Megan's Law information is prohibited. The "
        "registry website displays that warning. Both are sophisticated "
        "national actors. On information and belief, First Advantage's own "
        "notices in other matters involving this Plaintiff have recited that "
        "registry information may not be used for employment.",
    ),
    (
        "PARA",
        "48. On information and belief, Defendants did not disclose to "
        "Plaintiff that registry information had been obtained or used, and "
        "thereby deprived him of a meaningful opportunity to inspect the "
        "source, dispute a mismatch, and invoke the statutory remedies before "
        "the decision became final.",
    ),
    (
        "PARA",
        "49. As a result of the decision, Plaintiff lost the General Warehouse "
        "Worker / 2nd Shift employment at $22.60 per hour, including the "
        "opportunity to earn the wages and benefits of that position, "
        "according to proof and subject to mitigation. The offer email does "
        "not state weekly hours. Plaintiff also suffered emotional distress, "
        "humiliation, and anxiety from an unexplained collapse of a written "
        "offer he is informed and believes rested on a status the Legislature "
        "has forbidden employers to use. [PLAINTIFF MUST CONFIRM WAGES "
        "EARNED, IF ANY, HOURS OFFERED, AND REPLACEMENT WORK.]",
    ),
    (
        "PARA",
        "50. Plaintiff has sought and continues to seek replacement employment "
        "and does not claim a guaranteed lifetime expectancy from an unsigned "
        "or unfinalized warehouse offer. Economic damages will be limited to "
        "losses proven with reasonable certainty and without double recovery "
        "against other dockets that arise from different employers and "
        "different decisions.",
    ),
    ("SUBHEAD", "F. Inspection Rights, Independent ICRAA Path, and Why a Demurrer Cannot Replicate Lerma"),
    (
        "PARA",
        "51. Code of Civil Procedure section 425.10 requires a statement of "
        "the facts constituting the cause of action in ordinary and concise "
        "language. Section 452 requires this Court to construe the pleading "
        "liberally with a view to substantial justice between the parties. "
        "Facts exclusively in Defendants' possession — the Best Buy First "
        "Advantage report, the source-of-record line, the adjudication code, "
        "and the decision-maker's reason — are properly pleaded on "
        "information and belief. Plaintiff does not attach that report "
        "because he does not have it.",
    ),
    (
        "PARA",
        "52. The section 290.46(j) claim has four elements: (a) information "
        "disclosed pursuant to section 290.46; (b) use of that information by "
        "a defendant; (c) a purpose relating to employment; and (d) the use "
        "was not to protect a person at risk and was not otherwise authorized "
        "by law. Plaintiff pleads each element. Elements (a) and (b) are "
        "pleaded on information and belief. Elements (c) and (d) follow from "
        "the written warehouse offer and the later employment decision. A "
        "demurrer tests the pleading, not the unproduced report. Defendants "
        "may deny registry use. They may not convert that denial into a "
        "Lerma dismissal while the report remains in their possession.",
    ),
    (
        "PARA",
        "53. The Second Cause of Action under Civil Code sections 1786.40 and "
        "1786.50 is independent of the registry-use inference. Best Buy "
        "extended a written offer, named First Advantage, and required a "
        "consumer report and investigative consumer report as a condition of "
        "that offer. The file contains no Civil Code section 1786.40 advice "
        "that an investigative consumer report had been obtained, and no "
        "agency name and address supplied at the time of any denial. A "
        "notice failure can reach discovery even if the section 290.46(j) "
        "count later fails on the contents of the report. Civil Code "
        "sections 1786.10 and 1786.22 entitle Plaintiff to inspect and "
        "obtain a copy of the information First Advantage maintains on him. "
        "Plaintiff has not yet served that inspection request. He will. "
        "Those records, together with Best Buy's Candidate Zone and "
        "Employment Screening file, are the discrete set that will confirm "
        "or refute registry use.",
    ),
    ("HEADER", "VI.\nFIRST CAUSE OF ACTION"),
    (
        "SUBHEAD",
        "Unauthorized Employment Use of Registry Information\n"
        "Penal Code section 290.46(j) — Against All Defendants",
    ),
    (
        "PARA",
        "54. Plaintiff realleges paragraphs 1 through 53, except allegations "
        "expressly pleaded in the alternative are incorporated only to the "
        "extent consistent with this cause.",
    ),
    (
        "PARA",
        "55. Penal Code section 290.46(j)(1) authorizes use of information "
        "disclosed under that section only to protect a person at risk, except "
        "as otherwise authorized by law. Section 290.46(j)(2)(E) prohibits use "
        "of that information for purposes relating to employment unless another "
        "law authorizes the use.",
    ),
    (
        "PARA",
        "56. Section 290.46(j)(4)(A) makes the user liable for the actual "
        "damages, and any amount that may be determined by a jury or a court "
        "sitting without a jury, not exceeding three times the amount of actual "
        "damage, and not less than two hundred fifty dollars ($250), and "
        "attorney's fees, exemplary damages, or a civil penalty not exceeding "
        "twenty-five thousand dollars ($25,000). The $25,000 figure is a cap "
        "on the civil penalty, not a substitute floor that displaces actual "
        "damages.",
    ),
    (
        "PARA",
        "57. On information and belief, each element alleged in paragraph 52 "
        "is satisfied. Best Buy, First Advantage, and such DOE Defendants as "
        "ordered, furnished, scored, or acted on the report, used information "
        "disclosed pursuant to section 290.46 concerning Plaintiff.",
    ),
    (
        "PARA",
        "58. The use related directly to employment: it concerned the General "
        "Warehouse Worker / 2nd Shift offer or the later decision that ended "
        "or prevented that job. The use was not authorized by section "
        "290.46(j)(1) or by any other provision of law applicable to that "
        "warehouse assignment. Defendants knew or should have known that "
        "employment use was prohibited. The use was a substantial factor in "
        "the decision and caused the loss and injury alleged.",
    ),
    (
        "PARA",
        "59. Plaintiff seeks the remedies authorized by section 290.46(j)(4)(A) "
        "and preventive relief under subdivision (j)(4)(B) to restrain any "
        "pattern or practice of employment use of Megan's Law information in "
        "Best Buy's California warehouse hiring and in First Advantage's "
        "California employment reports.",
    ),
    ("HEADER", "VII.\nSECOND CAUSE OF ACTION"),
    (
        "SUBHEAD",
        "California Investigative Consumer Reporting Agencies Act\n"
        "Civil Code sections 1786.40 and 1786.50 — Against Best Buy, First "
        "Advantage, and User DOES\n"
        "(Pleaded on Information and Belief)",
    ),
    (
        "PARA",
        "60. Plaintiff realleges paragraphs 1 through 53 and 57 through 58 to "
        "the extent consistent with this cause.",
    ),
    (
        "PARA",
        "61. On information and belief, First Advantage assembled or evaluated "
        "information concerning Plaintiff's character, general reputation, "
        "personal characteristics, or mode of living for employment purposes "
        "at Best Buy's request, and Best Buy was the user of that information "
        "before the decision alleged in paragraph 34.",
    ),
    (
        "PARA",
        "62. Civil Code section 1786.40(a) required Best Buy, under "
        "circumstances in which employment was denied and an investigative "
        "consumer report had been obtained, to advise Plaintiff of that fact "
        "and supply the agency's name and address. On information and belief, "
        "Best Buy did not comply. The file contains no such advice. "
        "[PLAINTIFF MUST CONFIRM NONRECEIPT.]",
    ),
    (
        "PARA",
        "63. The omission prevented Plaintiff from timely obtaining the Best "
        "Buy-specific report, testing whether its source was the California "
        "registry or ordinary court records, and invoking his statutory "
        "inspection and dispute rights. This ICRAA count does not depend on "
        "proving Penal Code section 290.46(j). A notice failure under Civil "
        "Code section 1786.40 is independently actionable if an investigative "
        "consumer report was obtained and employment was denied without the "
        "required advice. That count can reach discovery even if the "
        "registry-use inference later fails.",
    ),
    (
        "PARA",
        "64. Under Civil Code section 1786.50, Plaintiff seeks actual damages "
        "or $10,000, whichever is greater, costs, attorney's fees if later "
        "represented, and punitive damages upon proof of gross negligence or "
        "willfulness.",
    ),
    (
        "PARA",
        "65. This ICRAA count is not a Fair Credit Reporting Act count. "
        "Plaintiff has not pleaded 15 U.S.C. section 1681b(b)(3). He reserves "
        "amendment if production shows Best Buy based the decision in whole or "
        "in part on a consumer report and failed to provide a copy of the "
        "report and a federal rights summary before the adverse action. He "
        "also reserves amendment under Civil Code section 1786.16 if "
        "production shows the report was procured before the required "
        "standalone disclosure and written authorization. The October 17 "
        "confirmation recites authorization; it does not prove that a report "
        "was lawfully procured or used.",
    ),
    ("HEADER", "VIII.\nTHIRD CAUSE OF ACTION"),
    (
        "SUBHEAD",
        "Unlawful and Unfair Business Practices\n"
        "Business and Professions Code section 17200 — Against All Defendants",
    ),
    (
        "PARA",
        "66. Plaintiff realleges paragraphs 1 through 65 to the extent "
        "consistent with this equitable cause.",
    ),
    (
        "PARA",
        "67. Defendants engaged in unlawful practices by violating Penal Code "
        "section 290.46(j) and, if proven, Civil Code section 1786.40. They "
        "engaged in unfair practices by extending a written warehouse offer, "
        "ordering a same-day screen, and then undoing the hire on secret "
        "registry-derived information without a source, a report, or an "
        "opportunity to respond.",
    ),
    (
        "PARA",
        "68. Plaintiff suffered injury in fact and lost money or property "
        "through the lost warehouse employment at $22.60 per hour and other "
        "economic losses to be proven. He does not seek future unearned wages "
        "as UCL restitution. He seeks restitution only of money or property "
        "in which he had a vested interest and that Defendants acquired or "
        "caused him to lose through the challenged practices.",
    ),
    (
        "PARA",
        "69. Legal damages are not an adequate remedy for Defendants' "
        "retention, use, and dissemination of registry-derived screening data "
        "or their ongoing employment-screening practices. Plaintiff seeks an "
        "injunction requiring Defendants to cease prohibited employment use of "
        "California registry information in California warehouse hiring; "
        "preserve and disclose the source and audit trail of Plaintiff's "
        "screening; and correct or segregate unlawfully used data, together "
        "with restitution and declaratory relief ancillary to the injunction "
        "under Business and Professions Code section 17203.",
    ),
    ("HEADER", "IX.\nPRESERVATION OF EVIDENCE"),
    (
        "PARA",
        "70. Defendants are on notice to preserve Plaintiff's complete Best "
        "Buy and BrassRing / Candidate Zone file for requisition 928556BR; "
        "the offer, acceptance audit, and disclosure PDFs; the background-"
        "check order, authorization, report, component searches, adjudication, "
        "access, and cancellation logs; the First Advantage file subject to "
        "Civil Code sections 1786.10 and 1786.22; the First Advantage "
        "drug-test order Q09078711 and result; communications of Tapia, "
        "Calvary, and Employment Screening; and policies governing Megan's "
        "Law, FCRA, ICRAA, and warehouse adjudication in 2023.",
    ),
    (
        "PARA",
        "71. Relevant electronically stored information includes applicant-"
        "tracking and HRIS audit fields, event timestamps, reason codes, "
        "report-view logs, emails, chats, SMS, and data-retention records "
        "from October 1, 2023 through January 31, 2024, and any later date "
        "on which the employment decision was recorded or revisited.",
    ),
    (
        "PARA",
        "72. The July 2024 First Advantage/UPS report is relevant to "
        "retrievability and matching methodology of this same vendor on this "
        "same Plaintiff. It is not a substitute for the Best Buy report.",
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
        "73. Plaintiff demands trial by jury on all causes of action and issues "
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
    d.write_line("STATE OF CALIFORNIA, COUNTY OF SAN JOAQUIN", bold=True, center=True)
    d.blank_line()
    d.write_wrapped("I, BRENDAN NGEHSI NEWANFORBI, declare:", first_indent=36)
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
        f"Executed on {exec_date}, at Stockton, California.", first_indent=36
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
    if execute and dt.date.today() < EARLIEST_EXECUTION_DATE:
        raise SystemExit(
            "Refusing to affix a signature before September 8, 2026. "
            "Generate the unsigned review draft now and rerun --execute on or after that date."
        )
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
        CAPTION_LEFT, CAPTION_RIGHT, caption_size=8.0, tight_lh=10.5, boxed=True
    )
    d.blank_line()

    for kind, text in CONTENT:
        if kind == "NOTICE":
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
            d.write_wrapped(text, first_indent=36)
            d.blank_line()
        elif kind == "LIST_ITEM":
            d.write_wrapped(text, indent=36, first_indent=0)
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
        help="Affix Plaintiff's signature (refused before September 8, 2026)",
    )
    args = parser.parse_args()
    path = build(Path(args.out).resolve(), args.date, args.execute)
    print(f"Generated: {path}")


if __name__ == "__main__":
    main()
