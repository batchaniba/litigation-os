#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Matter 38 — San Joaquin filing review draft (Swift).

REVIEW DRAFT. Not LOCKED. File in San Joaquin Superior Court on or before
September 26, 2026 if accrual is the pre-adverse letter. Post-adverse outer
bound is October 5, 2026.

This is not an E.D. Cal. FCRA clone. Swift sent FCRA pre-adverse and
post-adverse letters in 2023. The two-year FCRA discovery clock from those
letters closed. The role is Class A Driver (DOT exception risk). LLC
membership is not in the file; do not plead 28 U.S.C. section 1332. No
count uses a May 29, 2026 delayed-discovery date.

The September 8, 2026 verified packet is historical work product; it was
never clerk-filed.

    python3 internal/scripts/matter38-filing-complaint.py
    python3 internal/scripts/matter38-filing-complaint.py --dump-md
"""

from __future__ import annotations

import os
import sys
from pathlib import Path

SCRIPT_DIR = Path(__file__).resolve().parent
sys.path.insert(0, str(SCRIPT_DIR / "lib"))

from pleading_paper import CONTENT_LEFT, COURT_LINE1, PleadingPaper  # noqa: E402

ROOT = SCRIPT_DIR.parents[1]
DEFAULT_OUT = (
    ROOT
    / "internal/public/documents/matter-38"
    / "Filing Complaint Review Draft - Ngwa Nforbi v Swift Transportation"
    " Co of Arizona LLC (Sep 15 2026).pdf"
)

DOC_TITLE_FOOTER = (
    "COMPLAINT FOR DAMAGES -- NGWA NFORBI v. SWIFT TRANSPORTATION CO. OF "
    "ARIZONA LLC (SAN JOAQUIN REVIEW DRAFT)"
)

COURT_LINE2 = "COUNTY OF SAN JOAQUIN"

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
    ("SWIFT TRANSPORTATION CO. OF", True, False),
    ("ARIZONA LLC, a Delaware limited", True, False),
    ("liability company, d/b/a SWIFT", True, False),
    ("TRANSPORTATION,", True, False),
    ("", False, False),
    ("                          Defendant.", False, False),
]

CAPTION_RIGHT = [
    ("Case No. ________________", False, False),
    ("", False, False),
    ("COMPLAINT FOR DAMAGES", True, False),
    ("", False, False),
    ("(1) Cal. Penal Code", False, False),
    ("      section 290.46(j);", False, False),
    ("(2) ICRAA, Cal. Civ. Code", False, False),
    ("      sections 1786.40, 1786.50;", False, False),
    ("(3) UCL, Cal. Bus. & Prof.", False, False),
    ("      Code section 17200", False, False),
    ("", False, False),
    ("[Unlimited Civil]", False, True),
    ("[Jury Trial Demanded]", False, True),
    ("", False, False),
    ("[REVIEW DRAFT -- FILE ON OR", True, False),
    ("BEFORE SEPTEMBER 26, 2026]", True, False),
]

CONTENT = [
    (
        "NOTICE",
        "REVIEW DRAFT -- NOT FOR FILING UNTIL PLAINTIFF SIGNS. File in this "
        "Court on or before September 26, 2026 if the September 26, 2023 "
        "pre-adverse letter is accrual. The October 5, 2023 post-adverse "
        "letter is October 5, 2026. This complaint does not plead the Fair "
        "Credit Reporting Act and does not plead diversity jurisdiction. No "
        "count uses a delayed-discovery date of May 29, 2026. Serve Swift's "
        "current California Secretary of State agent, not a terminal. Do not "
        "republish identifiers from the decrypted packet.",
    ),
    (
        "PARA",
        "Plaintiff BRENDAN NGWA NFORBI, appearing in propria persona, alleges "
        "against Defendant SWIFT TRANSPORTATION CO. OF ARIZONA LLC ('Swift') "
        "as follows:",
    ),
    ("HEADER", "INTRODUCTION"),
    (
        "PARA",
        "1. In September 2023, Plaintiff applied to Swift for a Class A "
        "Driver position. On September 26, 2023, Swift sent a password-"
        "protected pre-adverse packet. The National Sex Offender Public "
        "Website component of that packet remained 'Processing' on every "
        "snapshot furnished to Plaintiff. On October 5, 2023, Swift sent a "
        "post-adverse letter stating that it had decided not to employ him "
        "based in whole or in part on consumer reports from Asurint, "
        "Tenstreet, DriverIQ, FMCSA-DOT, and Equifax Work Number.",
    ),
    (
        "PARA",
        "2. The September 26 packet has been decrypted. Plaintiff alleges "
        "its adjudication results as known facts. He does not republish "
        "Social Security, date-of-birth, CDL, or telephone identifiers from "
        "that packet. National criminal without a sex-offender component "
        "returned Clear. Federal criminal returned Clear. Completed county "
        "criminal searches returned Clear. NSOPW remained Processing. The "
        "furnished packet contains neither a completed NSOPW hit nor a "
        "completed NSOPW no-record, and it does not state 'SOURCE OF RECORD: "
        "CALIFORNIA SEX OFFENDER REGISTRY.' FMCSA Clearinghouse returned "
        "Driver Not Prohibited.",
    ),
    (
        "PARA",
        "3. What the packet does contain -- a Class A commercial driver's "
        "license, an April 22, 2022 improper-lane moving violation with zero "
        "points, PSP inspection history, and a CDLIS license-identity match "
        "-- is not information disclosed pursuant to Penal Code section "
        "290.46. Those components do not themselves explain a registry-based "
        "denial.",
    ),
    (
        "PARA",
        "4. Plaintiff alleges, on information and belief and as an ultimate "
        "fact, that Swift used preliminary sex-offender-registry information "
        "from that still-Processing NSOPW component -- including information "
        "disclosed pursuant to Penal Code section 290.46 or a derivative "
        "national compilation whose source was the California registry -- in "
        "whole or in part in the October 5, 2023 decision. The vendor "
        "adjudication log, any later NSOPW return, and the decision-maker "
        "communications are exclusively in Defendants' possession.",
    ),
    (
        "PARA",
        "5. Federal motor-carrier screening does not swallow this claim. The "
        "Clearinghouse and Pre-Employment Screening Program concern drug-and-"
        "alcohol violations and crash or inspection history. They are not "
        "Penal Code section 290.46 disclosures. An employer that may lawfully "
        "obtain ordinary safety records is not thereby authorized to use "
        "Megan's Law website information for employment. Penal Code section "
        "290.46(j)(3) says so.",
    ),
    (
        "PARA",
        "6. This complaint does not plead the Fair Credit Reporting Act. "
        "Swift sent FCRA-captioned pre-adverse and post-adverse letters in "
        "2023. The two-year FCRA discovery clock from those letters would "
        "have closed in 2025. The position is a Class A commercial-driver "
        "assignment. Plaintiff does not presently plead 15 U.S.C. section "
        "1681b(b)(3)(A) or the DOT-driver notice provisions. He reserves "
        "amendment if production shows a timely FCRA claim that those letters "
        "did not cure.",
    ),
    (
        "PARA",
        "7. Plaintiff does not name Knight-Swift Transportation Holdings, "
        "Inc., merely as parent. He does not presently name Asurint, "
        "Tenstreet, DriverIQ / Cisive, or Equifax as defendants. Robin "
        "Kaufman and Matt Hutto are witnesses. This complaint is unverified. "
        "No count uses a delayed-discovery date of May 29, 2026.",
    ),
    ("HEADER", "JURISDICTION AND VENUE"),
    (
        "PARA",
        "8. This Court has subject-matter jurisdiction under article VI, "
        "section 10 of the California Constitution and Code of Civil "
        "Procedure section 410.10.",
    ),
    (
        "PARA",
        "9. This action is unlimited civil because the aggregate relief "
        "sought exceeds $35,000, exclusive of interest and costs. No "
        "specific personal-injury or punitive-damages amount is pleaded.",
    ),
    (
        "PARA",
        "10. This Court has personal jurisdiction over Swift because Swift "
        "recruited Plaintiff, a California resident; caused consumer reports "
        "to be procured about him; sent the pre-adverse and post-adverse "
        "communications to him in California; and is, on information and "
        "belief, qualified to transact business in California.",
    ),
    (
        "PARA",
        "11. Venue is proper in San Joaquin County under Code of Civil "
        "Procedure sections 395 and 395.5 because Plaintiff resides here, he "
        "received the recruiting, screening, and adverse-action "
        "communications here, and the liability and injury arose here.",
    ),
    (
        "PARA",
        "12. Plaintiff has not pleaded a federal claim. This is a California "
        "statutory action. Plaintiff does not plead 28 U.S.C. section 1332. "
        "Swift is a limited liability company. Complete diversity would "
        "require the citizenship of every member. Those membership facts are "
        "not in Plaintiff's possession.",
    ),
    ("HEADER", "PARTIES"),
    (
        "PARA",
        "13. Plaintiff BRENDAN NGWA NFORBI is a natural person residing in "
        "Stockton, San Joaquin County, California. He is also identified in "
        "records as Brendan Ngehsi Ngwa Nforbi and Brendan Ngehsi "
        "Ngwanforbi. Those name variants refer to Plaintiff.",
    ),
    (
        "PARA",
        "14. Plaintiff is required to register under Penal Code section 290. "
        "At all times relevant, information identifying him appeared on "
        "California's Megan's Law website operated pursuant to Penal Code "
        "section 290.46.",
    ),
    (
        "PARA",
        "15. Defendant SWIFT TRANSPORTATION CO. OF ARIZONA LLC is a Delaware "
        "limited liability company doing business as Swift Transportation. "
        "Its October 5, 2023 letter lists 2200 South 75th Avenue, Phoenix, "
        "Arizona 85043. On September 25, 2023, the FMCSA Clearinghouse "
        "identified the querying employer as SWIFT TRANSPORTATION CO OF "
        "ARIZONA LLC, USDOT number 54283.",
    ),
    (
        "PARA",
        "16. Plaintiff will serve Swift through its designated agent for "
        "service of process on the California Secretary of State record as of "
        "the date of service. Public listings have used National Registered "
        "Agents, Inc. Plaintiff will confirm the current listing immediately "
        "before service. Service is not to be made at a terminal or a "
        "recruiter's phone number.",
    ),
    (
        "PARA",
        "17. Asurint, Tenstreet, LLC, DriverIQ / Cisive, FMCSA, and Equifax "
        "Workforce Solutions / The Work Number are named in Swift's own "
        "October 5 letter as sources of consumer reports. They are inspection "
        "targets and fact witnesses, not presently named as defendants.",
    ),
    (
        "PARA",
        "18. Robin Kaufman and Matt Hutto communicated as Swift driver "
        "recruiters. They are percipient witnesses, not presently named as "
        "defendants. Matt Hutto's message used a Class A Recruiting address "
        "while stating it was sent on behalf of Swift Transportation Co. of "
        "Arizona LLC by Tenstreet, LLC, 120 West 3rd Street, Tulsa, Oklahoma.",
    ),
    ("HEADER", "TIMELINESS"),
    (
        "PARA",
        "19. Penal Code section 290.46 does not prescribe its own limitations "
        "period. Count One is a liability created by statute, timely under "
        "Code of Civil Procedure section 338(a). Three years from September "
        "26, 2023, is September 26, 2026. Three years from October 5, 2023, "
        "is October 5, 2026. This complaint is prepared to be filed inside "
        "both dates. Plaintiff does not plead a delayed-discovery date for "
        "this count.",
    ),
    (
        "PARA",
        "20. Plaintiff does not concede that Code of Civil Procedure section "
        "335.1 or section 340(a) supplies the period for Count One. The "
        "actual-damages and discretionary enhancement in section "
        "290.46(j)(4)(A) are a liability created by statute, not an action "
        "upon a statute for a penalty. The labeled civil-penalty slice is "
        "pleaded in the alternative and is not the sole theory.",
    ),
    (
        "PARA",
        "21. Civil Code section 1786.52 requires that an ICRAA action be "
        "brought within two years from the date the plaintiff knew or should "
        "have known of the violation. The 2023 letters described consumer "
        "reports and named agencies. They did not advise that an "
        "investigative consumer report had been obtained. The face of this "
        "complaint does not establish the discovery date as a complete bar. "
        "No count uses May 29, 2026.",
    ),
    (
        "PARA",
        "22. The Unfair Competition Law claim is timely under Business and "
        "Professions Code section 17208's four-year period. That period is "
        "independent of any shorter period that may apply to a borrowed "
        "predicate.",
    ),
    ("HEADER", "FACTUAL ALLEGATIONS"),
    ("SUBHEAD", "A. The Swift Application"),
    (
        "PARA",
        "23. On Friday, September 22, 2023, at 3:02 p.m., Robin Kaufman, "
        "identifying herself as a Swift Transportation Driver Recruiter, "
        "emailed Plaintiff that she had received his information and asked "
        "him to complete the full application. The message was sent on "
        "behalf of Swift Transportation Co. of Arizona LLC by Tenstreet, LLC.",
    ),
    (
        "PARA",
        "24. That evening at 10:03 p.m., Matt Hutto, also identifying himself "
        "as a Swift Driver Recruiter, emailed that he was trying to reach "
        "Plaintiff, asked him to complete the full driver application, and "
        "gave 803-564-3092 as a return number.",
    ),
    (
        "PARA",
        "25. The application was for a Class A Driver position. The file "
        "does not contain the completed application, a written offer, a "
        "terminal assignment, or a rate of pay. Plaintiff does not invent "
        "those figures.",
    ),
    ("SUBHEAD", "B. The September 25, 2023 Screen"),
    (
        "PARA",
        "26. On Monday, September 25, 2023, at 11:54 a.m., Tenstreet notified "
        "Plaintiff that a DriverIQ employment background document ordered in "
        "connection with Swift was available in Driver Pulse.",
    ),
    (
        "PARA",
        "27. Four minutes later, the FMCSA Office of Safety Programs emailed "
        "that SWIFT TRANSPORTATION CO OF ARIZONA LLC (USDOT 54283) had "
        "requested access to Plaintiff's FMCSA Drug and Alcohol Clearinghouse "
        "record.",
    ),
    (
        "PARA",
        "28. At 1:20 p.m. the same day, Tenstreet notified Plaintiff that his "
        "Clearinghouse result ordered by Swift was available. The decrypted "
        "pre-adverse packet includes a Clearinghouse result of Driver Not "
        "Prohibited, with no open violations.",
    ),
    (
        "PARA",
        "29. The Clearinghouse query proves Swift was then treating Plaintiff "
        "as a prospective commercial-driver hire. It is not a Penal Code "
        "section 290.46 disclosure.",
    ),
    ("SUBHEAD", "C. The Pre-Adverse and Post-Adverse Letters"),
    (
        "PARA",
        "30. On Tuesday, September 26, 2023, at 3:09 a.m., Swift Recruiting "
        "(recruitadmin@swifttrans.com) emailed a message titled 'Swift "
        "Transportation - FCRA,' stating that an important communication was "
        "attached as Pre_Adverse_Action_Letter_76326281-1916808-encrypted.pdf "
        "and that the password was the last four digits of Plaintiff's Social "
        "Security number.",
    ),
    (
        "PARA",
        "31. The pre-adverse attachment has been decrypted. It is a composite "
        "screening packet. It includes completed criminal-file components "
        "returning Clear, an NSOPW component that remained Processing on "
        "every snapshot, a Clearinghouse result of Driver Not Prohibited, an "
        "MVR, PSP inspection history, and CDLIS information.",
    ),
    (
        "PARA",
        "32. On Thursday, October 5, 2023, at 3:09 a.m., Swift Recruiting "
        "emailed a second 'Swift Transportation - FCRA' message attaching "
        "Post_Adverse_Action_Letter_76326281-1916809_em.pdf.",
    ),
    (
        "PARA",
        "33. The enclosed letter is on Swift Transportation Co. of Arizona "
        "LLC letterhead, dated October 5, 2023, 5:09 a.m., addressed to "
        "Brendan Ngehsi Nforbi at 1455 Cat Tail Drive, Stockton, California "
        "95204. It states that offers of employment at Swift are contingent "
        "upon successful completion of a background check, and that the "
        "letter serves as notification that Swift had decided not to employ "
        "Plaintiff based in whole or in part on a consumer report.",
    ),
    (
        "PARA",
        "34. The letter states that Asurint (Cleveland, Ohio), Tenstreet "
        "(Tulsa, Oklahoma), DriverIQ (Tulsa, Oklahoma; disputes at Cisive), "
        "FMCSA-DOT, and The Work Number / Equifax Workforce Solutions "
        "provided consumer reports which, in whole or in part, influenced the "
        "employment decision.",
    ),
    (
        "PARA",
        "35. The October 5 letter says a copy of the consumer report and a "
        "Summary of Rights were attached. The decrypted September 26 packet "
        "is the report-side paper in Plaintiff's files. It does not contain "
        "a completed NSOPW result, a California Sex Offender Registry source "
        "line, or a separate later Asurint, Tenstreet, or DriverIQ printout "
        "showing a completed registry hit.",
    ),
    (
        "PARA",
        "36. Civil Code section 1786.40(a) required, if an investigative "
        "consumer report had been obtained, that Swift advise Plaintiff that "
        "an investigative consumer report had been obtained and supply the "
        "agency's name and address. The October 5 letter named agencies and "
        "stated that consumer reports influenced the decision. It did not "
        "advise that an investigative consumer report had been obtained. "
        "Naming agencies is not that advice.",
    ),
    (
        "SUBHEAD",
        "D. Screening Inference, Comparators, and Pretext",
    ),
    (
        "PARA",
        "37. Plaintiff is a person as to whom information is disclosed on "
        "California's Megan's Law website. That website, and the statute that "
        "created it, warn that the information may not be used for employment.",
    ),
    (
        "PARA",
        "38. Swift ordered an NSOPW sex-offender-website search. That "
        "component remained Processing on every snapshot in the packet sent "
        "with the pre-adverse notice. Swift then denied employment based in "
        "whole or in part on consumer reports. The completed criminal, "
        "Clearinghouse, and MVR components in the packet do not themselves "
        "explain a registry-based denial.",
    ),
    (
        "PARA",
        "39. Plaintiff alleges, on information and belief, that between the "
        "September 26 snapshots and the October 5 decision, Swift or a vendor "
        "acting for Swift obtained, displayed, scored, or was informed of "
        "preliminary information from that in-process NSOPW component citing "
        "a sex-offender registry -- including information disclosed pursuant "
        "to Penal Code section 290.46 -- and used that preliminary "
        "information in whole or in part in the denial.",
    ),
    (
        "PARA",
        "40. Plaintiff possesses a First Advantage employment background "
        "report concerning himself generated for United Parcel Service. In "
        "that report, ordinary criminal-search components returned "
        "non-adverse results, while the sex-offender-registry component was "
        "the adverse or decisional component and expressly identified the "
        "source of record as the California Sex Offender Registry.",
    ),
    (
        "PARA",
        "41. In a separate First Advantage employment screening for Federal "
        "Express Corporation, FedEx later admitted in its responsive pleading "
        "that the report identified Plaintiff as a California registrant.",
    ),
    (
        "PARA",
        "42. Plaintiff does not allege that UPS's or FedEx's report is "
        "Swift's report, and he does not allege that Asurint, Tenstreet, or "
        "DriverIQ is First Advantage. He alleges those comparator records "
        "because they concern the same consumer, the same underlying "
        "California registry entry, and the same type of employment "
        "background screening contemporaneous with Swift's decision. They "
        "are not attached to this complaint.",
    ),
    (
        "PARA",
        "43. Searching a public website is not a free pass. Subdivision "
        "(j)(3)'s reference to publicly available information does not "
        "authorize employment use of Megan's Law disclosures. Information "
        "disclosed pursuant to Penal Code section 290.46 does not lose that "
        "character because a vendor also searched NSOPW or another public "
        "sex-offender compilation.",
    ),
    (
        "PARA",
        "44. Alternative explanations -- a failed Clearinghouse result, a "
        "driving-record or crash disqualification, a lawful criminal-history "
        "adjudication under a statute that actually authorizes the use, a CDL "
        "defect, or a withdrawal of the application -- can be tested against "
        "a discrete set of records in Swift's and its vendors' possession.",
    ),
    (
        "PARA",
        "45. If production later shows a completed NSOPW returning no record "
        "and no preliminary registry use, Count One will stand or fall on "
        "that file after production. Counts Two and Three do not depend on "
        "proving a completed registry hit.",
    ),
    (
        "PARA",
        "46. The use was not to protect a person at risk within the meaning "
        "of section 290.46(j)(1). A general commercial-driver assignment is "
        "not, without more, that narrow authorization. FMCSA authorization "
        "to query the Clearinghouse or PSP is not authorization to use "
        "Megan's Law website information.",
    ),
    ("SUBHEAD", "E. Harm"),
    (
        "PARA",
        "47. As a result of the decision, Plaintiff lost the Class A Driver "
        "opportunity, including the wages and benefits of that position, "
        "according to proof and subject to mitigation. The file does not "
        "state a wage rate. Plaintiff does not invent one.",
    ),
    (
        "PARA",
        "48. He also suffered emotional distress, humiliation, and anxiety "
        "from an unexplained denial he is informed and believes rested on a "
        "status the Legislature has forbidden employers to use.",
    ),
    (
        "PARA",
        "49. Plaintiff has sought replacement employment and does not claim "
        "a guaranteed lifetime expectancy from an unaccepted driver "
        "application. Economic damages will be limited to losses proven with "
        "reasonable certainty and without double recovery against other "
        "dockets that arise from different employers and different decisions.",
    ),
    ("HEADER", "FIRST CAUSE OF ACTION"),
    (
        "SUBHEAD",
        "Unauthorized Employment Use of Registry Information\n"
        "Cal. Penal Code section 290.46(j)(2)(E) and (j)(4)(A)\n"
        "Against Swift Transportation Co. of Arizona LLC",
    ),
    (
        "PARA",
        "50. Plaintiff realleges paragraphs 1 through 49. This count is a "
        "liability created by statute. It is timely under Code of Civil "
        "Procedure section 338(a) from the September 26 / October 5, 2023 "
        "employment use. This count does not plead a delayed-discovery date.",
    ),
    (
        "PARA",
        "51. Penal Code section 290.46(j)(2)(E) prohibits use of information "
        "disclosed pursuant to section 290.46 for purposes relating to "
        "employment except as authorized by paragraph (1) or another "
        "provision of law.",
    ),
    (
        "PARA",
        "52. Plaintiff alleges, on information and belief and as an ultimate "
        "fact, that Swift used preliminary information from the still-"
        "Processing NSOPW component citing a sex-offender registry -- "
        "including information disclosed pursuant to section 290.46 "
        "concerning Plaintiff -- in whole or in part in the Class A Driver "
        "decision. The user is the employer that takes the information into "
        "account, not a vendor that merely retrieves it.",
    ),
    (
        "PARA",
        "53. Plaintiff does not allege that the printed snapshots contain a "
        "completed NSOPW hit or the words 'SOURCE OF RECORD: CALIFORNIA SEX "
        "OFFENDER REGISTRY.' The use alleged is the use of preliminary "
        "registry information from that in-process component.",
    ),
    (
        "PARA",
        "54. The use related directly to employment. It was not authorized "
        "by section 290.46(j)(1) or by any other provision of law applicable "
        "to that application. It was a substantial factor in the decision "
        "and caused the loss alleged.",
    ),
    (
        "PARA",
        "55. Plaintiff seeks the remedies authorized by section "
        "290.46(j)(4)(A), including actual damages, any amount the trier of "
        "fact determines not exceeding three times actual damage and not "
        "less than $250, attorney's fees, exemplary damages, or a civil "
        "penalty not exceeding $25,000. The $25,000 figure is a cap on the "
        "civil penalty, not a substitute floor. He does not presently allege "
        "a pattern or practice sufficient for subdivision (j)(4)(B).",
    ),
    ("HEADER", "SECOND CAUSE OF ACTION"),
    (
        "SUBHEAD",
        "California Investigative Consumer Reporting Agencies Act\n"
        "Cal. Civ. Code sections 1786.40 and 1786.50\n"
        "Against Swift Transportation Co. of Arizona LLC",
    ),
    ("PARA", "56. Plaintiff realleges paragraphs 1 through 49."),
    (
        "PARA",
        "57. On information and belief, one or more of the agencies Swift "
        "named assembled or evaluated information concerning Plaintiff's "
        "character, general reputation, personal characteristics, or mode of "
        "living for employment purposes, and Swift was the user of that "
        "information before the October 5, 2023 decision.",
    ),
    (
        "PARA",
        "58. Civil Code section 1786.40(a) required Swift, when employment "
        "was denied under circumstances in which an investigative consumer "
        "report had been obtained, to advise Plaintiff of that fact and "
        "supply the investigative consumer reporting agency's name and "
        "address. Swift's October 5 letter named agencies and cities. It "
        "did not advise that an investigative consumer report had been "
        "obtained.",
    ),
    (
        "PARA",
        "59. This section 1786.40 omission is pleaded as a separate act from "
        "Count One. Plaintiff does not allege that section 1786.40 required "
        "Swift to identify the decisive component or to complete the NSOPW "
        "search. This count does not plead a delayed-discovery date of May "
        "29, 2026.",
    ),
    (
        "PARA",
        "60. This count does not depend on proving Penal Code section "
        "290.46(j). If Defendants establish that the reports were ordinary "
        "consumer reports and not investigative, this count does not apply. "
        "Plaintiff does not presently plead a CCRAA count.",
    ),
    (
        "PARA",
        "61. Under Civil Code section 1786.50, Plaintiff seeks actual "
        "damages or $10,000, whichever is greater, together with costs and "
        "any attorney's fees recoverable if counsel later appears, and "
        "punitive damages if the violation is proven grossly negligent or "
        "willful.",
    ),
    ("HEADER", "THIRD CAUSE OF ACTION"),
    (
        "SUBHEAD",
        "Unlawful and Unfair Business Practices\n"
        "Cal. Bus. & Prof. Code section 17200\n"
        "Against Swift Transportation Co. of Arizona LLC",
    ),
    ("PARA", "62. Plaintiff realleges paragraphs 1 through 61."),
    (
        "PARA",
        "63. Swift engaged in unlawful practices by violating, to the extent "
        "proven, Penal Code section 290.46(j)(2)(E) and Civil Code section "
        "1786.40. It engaged in unfair practices because the gravity of "
        "denying employment on a criterion the Legislature has forbidden, or "
        "on consumer reports without the investigative-report advice the "
        "statute required, outweighs any utility of taking adverse action "
        "while a sex-offender-website component remained Processing.",
    ),
    (
        "PARA",
        "64. Plaintiff suffered injury in fact and lost money or property "
        "through the lost Swift employment opportunity, reliance "
        "expenditures, and employment-search costs to be proven. He seeks "
        "restitution only of vested money or property Swift acquired, not "
        "unearned future wages.",
    ),
    (
        "PARA",
        "65. On information and belief, Swift continues to use the same or "
        "similar standardized screening procedures for California driver "
        "applicants. Plaintiff seeks injunctive relief requiring Swift to "
        "cease prohibited employment use of California registry information "
        "in California recruiting and to preserve and disclose the source "
        "and audit trail of Plaintiff's screening, together with restitution "
        "under Business and Professions Code section 17203.",
    ),
    ("HEADER", "PRAYER FOR RELIEF"),
    (
        "PARA",
        "WHEREFORE, Plaintiff prays for judgment against Defendant as follows:",
    ),
    (
        "LIST_ITEM",
        "A. Actual, consequential, and economic damages according to proof, "
        "without double recovery;",
    ),
    (
        "LIST_ITEM",
        "B. The remedies authorized by Penal Code section 290.46(j)(4)(A);",
    ),
    (
        "LIST_ITEM",
        "C. ICRAA actual damages or $10,000, whichever is greater, and "
        "punitive damages upon the showing required by Civil Code section "
        "1786.50, if that count is proven;",
    ),
    (
        "LIST_ITEM",
        "D. Restitution under Business and Professions Code section 17203 of "
        "vested money or property Defendant acquired, not unearned future "
        "wages, and injunctive relief;",
    ),
    (
        "LIST_ITEM",
        "E. Costs of suit and attorney's fees only to the extent authorized "
        "and recoverable, including if counsel later appears;",
    ),
    (
        "LIST_ITEM",
        "F. Prejudgment and post-judgment interest as allowed by law; and",
    ),
    (
        "LIST_ITEM",
        "G. Such other and further relief as the Court deems just and proper.",
    ),
    ("HEADER", "DEMAND FOR JURY TRIAL"),
    (
        "PARA",
        "Plaintiff demands a trial by jury on all issues so triable.",
    ),
]

SIGNATURE_BLOCK = [
    ("", ""),
    ("left", "Dated: ____________________"),
    ("", ""),
    ("right", "Respectfully submitted,"),
    ("", ""),
    ("", ""),
    ("right", "___________________________________"),
    ("right", "BRENDAN NGWA NFORBI"),
    ("right", "Plaintiff, In Propria Persona"),
]


def dump_markdown(path: Path) -> None:
    lines = [
        "# Matter 38 — San Joaquin filing complaint review draft",
        "",
        "Generated from `internal/scripts/matter38-filing-complaint.py`. "
        "REVIEW DRAFT. File on or before **September 26, 2026** if the "
        "pre-adverse letter is accrual.",
        "",
        "Not an E.D. Cal. FCRA clone. FCRA is not pleaded. May 29, 2026 is "
        "**not** pleaded. Diversity § 1332 is not pleaded.",
        "",
        "---",
        "",
        "## Caption",
        "",
        "BRENDAN NGWA NFORBI, Plaintiff, in propria persona, v. SWIFT "
        "TRANSPORTATION CO. OF ARIZONA LLC, a Delaware limited liability "
        "company, d/b/a SWIFT TRANSPORTATION.",
        "",
        "Superior Court of California, County of San Joaquin. Unverified. "
        "Unlimited civil. Demand for jury trial.",
        "",
    ]
    for kind, text in CONTENT:
        if kind == "NOTICE":
            lines.extend([f"> **{text}**", ""])
        elif kind == "HEADER":
            lines.extend([f"## {text}", ""])
        elif kind == "SUBHEAD":
            heading = " / ".join(
                part.strip() for part in text.split("\n") if part.strip()
            )
            lines.extend([f"### {heading}", ""])
        elif kind in ("PARA", "LIST_ITEM"):
            lines.extend([text, ""])
        else:
            raise ValueError(f"unknown content kind {kind!r}")
    lines.extend(
        [
            "---",
            "",
            "Dated: ____________________",
            "",
            "Respectfully submitted,",
            "",
            "___________________________________",
            "",
            "BRENDAN NGWA NFORBI",
            "",
            "Plaintiff, In Propria Persona",
            "",
        ]
    )
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text("\n".join(lines), encoding="utf-8")
    print(f"Wrote {path}")


def main() -> None:
    if "--dump-md" in sys.argv:
        dump_markdown(
            ROOT / "internal/docs/matter-38" / "FILING_COMPLAINT_REVIEW_DRAFT.md"
        )
        return
    out = Path(os.path.abspath(sys.argv[1] if len(sys.argv) > 1 else DEFAULT_OUT))
    out.parent.mkdir(parents=True, exist_ok=True)
    d = PleadingPaper(str(out), doc_title_footer=DOC_TITLE_FOOTER)

    c = d.c
    atty_y = d._line_y(0)
    for i, (txt, fn, sz) in enumerate(PLAINTIFF_BLOCK):
        c.setFont(fn, sz)
        c.drawString(CONTENT_LEFT, atty_y - i * 15, txt)
    d.current_line = 4
    d.blank_line()

    d.write_line(COURT_LINE1, bold=True, center=True)
    d.write_line(COURT_LINE2, bold=True, center=True)
    d.blank_line()

    d.draw_caption_block(
        CAPTION_LEFT, CAPTION_RIGHT, caption_size=10, tight_lh=13, boxed=True
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
            d.ensure_space(len(lines) + 3)
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
            raise ValueError(f"unknown content kind {kind!r}")

    d.ensure_space(len(SIGNATURE_BLOCK))
    for align, text in SIGNATURE_BLOCK:
        if align == "":
            d.blank_line()
        elif align == "left":
            d.write_line(text)
        elif align == "right":
            d.write_line(text, right=True, right_margin_offset=20)
        else:
            raise ValueError(f"unknown signature alignment {align!r}")

    d.save()
    print(f"Wrote {out}")


if __name__ == "__main__":
    main()
