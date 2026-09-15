#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Matter 37 — E.D. Cal. federal complaint review draft (Home Depot).

REVIEW DRAFT. Not for filing until the FCRA/ICRAA discovery date is filled
and Plaintiff signs. The September 8, 2026 San Joaquin generator remains
LOCKED historical work product.

    python3 internal/scripts/matter37-edca-complaint.py
"""

from __future__ import annotations

import os
import sys
from pathlib import Path

SCRIPT_DIR = Path(__file__).resolve().parent
sys.path.insert(0, str(SCRIPT_DIR / "lib"))

from pleading_paper import CONTENT_LEFT, PleadingPaper  # noqa: E402

ROOT = SCRIPT_DIR.parents[1]
DEFAULT_OUT = (
    ROOT
    / "internal/public/documents/matter-37"
    / "EDCA Complaint Review Draft - Ngwa Nforbi v Home Depot USA Inc"
    " (Sep 15 2026).pdf"
)

DOC_TITLE_FOOTER = (
    "COMPLAINT FOR DAMAGES -- NGWA NFORBI v. HOME DEPOT U.S.A., INC. "
    "(E.D. Cal. REVIEW DRAFT)"
)

COURT_LINE1 = "UNITED STATES DISTRICT COURT"
COURT_LINE2 = "EASTERN DISTRICT OF CALIFORNIA -- SACRAMENTO DIVISION"

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
    ("HOME DEPOT U.S.A., INC.,", True, False),
    ("a Delaware corporation,", True, False),
    ("", False, False),
    ("                          Defendant.", False, False),
]

CAPTION_RIGHT = [
    ("Case No. ________________", False, False),
    ("", False, False),
    ("COMPLAINT FOR DAMAGES", True, False),
    ("", False, False),
    ("(1) FCRA, 15 U.S.C.", False, False),
    ("      section 1681b(b)(3)(A);", False, False),
    ("(2) ICRAA, Cal. Civ. Code", False, False),
    ("      sections 1786.40, 1786.50;", False, False),
    ("(3) Cal. Penal Code", False, False),
    ("      section 290.46(j)", False, False),
    ("", False, False),
    ("[DEMAND FOR JURY TRIAL]", True, False),
    ("", False, False),
    ("[REVIEW DRAFT -- NOT FOR", True, False),
    ("FILING UNTIL DISCOVERY", True, False),
    ("DATE IS FILLED]", True, False),
]

CONTENT = [
    (
        "NOTICE",
        "REVIEW DRAFT -- NOT FOR FILING. Fill the FCRA/ICRAA discovery date "
        "in paragraphs 44 through 47, confirm the Tracy position is not "
        "DOT-excepted, and have Plaintiff sign before any filing. Serve CSC, "
        "not 5395 Hopkins Road.",
    ),
    (
        "PARA",
        "Plaintiff BRENDAN NGWA NFORBI, appearing in propria persona, alleges "
        "against Defendant HOME DEPOT U.S.A., INC. ('Home Depot') as follows:",
    ),
    ("HEADER", "INTRODUCTION"),
    (
        "PARA",
        "1. This action arises from an accepted Home Depot hire at its "
        "warehouse, distribution, and fulfillment facility at 5395 Hopkins "
        "Road, Tracy, California. Plaintiff accepted the position and began "
        "Home Depot's onboarding process. Home Depot then required and ran an "
        "employment background check. On information and belief, Home Depot "
        "used First Advantage Background Services Corp. ('First Advantage') "
        "as the consumer reporting agency for that screening.",
    ),
    (
        "PARA",
        "2. The First Advantage relationship is not pleaded from guesswork "
        "alone. Public federal-court records contain a Home Depot-branded "
        "'BACKGROUND CHECK DISCLOSURE AND AUTHORIZATION' identifying First "
        "Advantage as the consumer reporting agency Home Depot would use to "
        "procure California investigative consumer reports. Other federal "
        "litigation describes First Advantage furnishing a consumer report to "
        "Home Depot for a prospective employee, and First Advantage itself "
        "later publicly featured a Home Depot representative in a program "
        "devoted to workforce screening practices. The precise order, package, "
        "transmission, and adjudication records for Plaintiff's screening are "
        "in Home Depot's and First Advantage's possession.",
    ),
    (
        "PARA",
        "3. On information and belief, First Advantage prepared and furnished "
        "Plaintiff's employment background report to Home Depot in connection "
        "with the Tracy hire, and Home Depot received and used that report. "
        "After the background check, Home Depot ceased the onboarding process "
        "and ended, withdrew, or prevented Plaintiff from beginning or "
        "continuing the accepted Tracy employment on or about August 2024.",
    ),
    (
        "PARA",
        "4. Before taking that adverse employment action, Home Depot did not "
        "provide Plaintiff a copy of the First Advantage report and did not "
        "provide the written Summary of Rights required by the Fair Credit "
        "Reporting Act ('FCRA'), 15 U.S.C. section 1681b(b)(3)(A). Home Depot "
        "thereby deprived Plaintiff of the statutory pre-decision opportunity "
        "to review the report, dispute its contents with the consumer "
        "reporting agency, and respond before the employment decision became "
        "final.",
    ),
    (
        "PARA",
        "5. When Home Depot denied, withdrew, ended, or prevented the "
        "employment under circumstances in which it had obtained an "
        "investigative consumer report, it also did not advise Plaintiff that "
        "such a report had been obtained and did not provide First Advantage's "
        "name and address as required by California Civil Code section 1786.40.",
    ),
    (
        "PARA",
        "6. California Penal Code section 290.46(j)(2)(E) prohibits use of "
        "information disclosed pursuant to California's Megan's Law website "
        "for purposes relating to employment except where another law "
        "authorizes the use. Plaintiff alleges, on information and belief and "
        "as an ultimate fact, that First Advantage furnished Home Depot "
        "information concerning Plaintiff that was disclosed pursuant to "
        "section 290.46, including Plaintiff's California registry information, "
        "and that Home Depot used that information for the purpose of deciding "
        "whether Plaintiff would begin or continue the accepted Tracy "
        "employment.",
    ),
    (
        "PARA",
        "7. That allegation is supported by specific facts rather than "
        "conjecture: Home Depot accepted Plaintiff for the Tracy position and "
        "began onboarding him; Home Depot then ran an employment background "
        "check through a screening vendor that public records identify as "
        "First Advantage; Plaintiff was contemporaneously listed on "
        "California's Megan's Law website; First Advantage reports concerning "
        "this same Plaintiff for other employers during the surrounding period "
        "included sex-offender-registry screening and California-registry "
        "information; and Home Depot terminated the onboarding sequence after "
        "the background check without communicating an independent reason. "
        "The transaction-specific report, source fields, adjudication codes, "
        "access logs, and decision records are in Home Depot's and First "
        "Advantage's possession.",
    ),
    ("HEADER", "JURISDICTION AND VENUE"),
    (
        "PARA",
        "8. This Court has original subject-matter jurisdiction under 28 U.S.C. "
        "section 1331 because Count One arises under the Fair Credit Reporting "
        "Act, 15 U.S.C. section 1681 et seq. Section 1681p expressly "
        "authorizes an action to enforce FCRA liability in an appropriate "
        "United States district court without regard to the amount in "
        "controversy.",
    ),
    (
        "PARA",
        "9. This Court has supplemental jurisdiction over Counts Two and Three "
        "under 28 U.S.C. section 1367(a) because those California claims arise "
        "from the same employment screening, consumer report, and adverse "
        "employment decision as the FCRA claim and form part of the same case "
        "or controversy.",
    ),
    (
        "PARA",
        "10. This Court also has original jurisdiction in the alternative "
        "under 28 U.S.C. section 1332(a) because the matter in controversy "
        "exceeds $75,000, exclusive of interest and costs, and is between "
        "citizens of different States. Plaintiff is a citizen of California. "
        "Home Depot U.S.A., Inc. is a corporation organized under the laws of "
        "Delaware with its principal place of business in Atlanta, Georgia. "
        "The amount-in-controversy allegation aggregates lost compensation "
        "from the accepted Tracy employment according to proof; FCRA actual "
        "damages and, if willfulness is proven, statutory and punitive "
        "damages; ICRAA actual damages or $10,000, whichever is greater, plus "
        "punitive damages if the statutory showing is met; and remedies "
        "authorized by Penal Code section 290.46(j)(4)(A). Plaintiff does not "
        "presently plead a specific hourly wage because no wage rate for this "
        "hire is in the record.",
    ),
    (
        "PARA",
        "11. Venue is proper in the Eastern District of California under "
        "28 U.S.C. section 1391(b)(2) because a substantial part of the events "
        "giving rise to the claims occurred in Tracy, San Joaquin County, "
        "California.",
    ),
    (
        "PARA",
        "12. Under Eastern District of California Local Rule 120(d), civil "
        "actions arising in San Joaquin County are commenced in the Sacramento "
        "Division.",
    ),
    ("HEADER", "PARTIES"),
    (
        "PARA",
        "13. Plaintiff BRENDAN NGWA NFORBI is a natural person and resident of "
        "San Joaquin County, California. He was the consumer and job applicant "
        "/ accepted hire who was the subject of the employment background "
        "report and adverse employment decision alleged herein.",
    ),
    (
        "PARA",
        "14. Defendant HOME DEPOT U.S.A., INC. is a corporation organized "
        "under the laws of the State of Delaware, qualified to transact "
        "business in California (California Secretary of State entity number "
        "01648357), and doing business as The Home Depot and The Home Depot "
        "Distribution Center. Its principal place of business is in Atlanta, "
        "Georgia. On information and belief, Home Depot U.S.A., Inc. owned, "
        "operated, staffed, and controlled the warehouse, distribution, and "
        "fulfillment facility at 5395 Hopkins Road, Tracy, California 95377 "
        "(the 'Tracy Center'), and was the legal employer that hired Plaintiff "
        "and made the employment decision challenged here. The Tracy Center is "
        "a worksite, not a separate legal entity.",
    ),
    (
        "PARA",
        "15. Home Depot's designated agent for service of process in "
        "California is CSC Lawyers Incorporating Service, 2710 Gateway Oaks "
        "Drive, Suite 150N, Sacramento, California 95833. Plaintiff will serve "
        "Home Depot through that registered agent. Service is not to be made "
        "at 5395 Hopkins Road merely because that is the worksite.",
    ),
    (
        "PARA",
        "16. On information and belief, First Advantage is the consumer "
        "reporting agency Home Depot used for Plaintiff's screening. Plaintiff "
        "does not presently name First Advantage as a defendant in this "
        "action. The report, order records, transmission logs, access logs, "
        "adjudication data, user certifications, service agreement, screening "
        "package, and client-specific adjudication criteria are discoverable "
        "from Home Depot and First Advantage.",
    ),
    (
        "PARA",
        "17. In Ford v. Home Depot U.S.A., Inc., No. 3:19-cv-00754-AJB-LL "
        "(S.D. Cal.), the plaintiff attached as Exhibit 1 a Home Depot-branded "
        "'BACKGROUND CHECK DISCLOSURE AND AUTHORIZATION.' The California "
        "notice in that document states that, in connection with an "
        "application for employment with Home Depot, Home Depot intended to "
        "procure an investigative consumer report and identified 'First "
        "Advantage Background Services Corp.' as the consumer reporting agency "
        "Home Depot would use to procure those reports.",
    ),
    (
        "PARA",
        "18. The same Home Depot-branded disclosure directed background-report "
        "requests to 'Home Depot c/o First Advantage Background Services "
        "Corp.' and stated that before information from a consumer or "
        "investigative consumer report was used to make an adverse employment "
        "decision, Home Depot would provide the applicant a copy of the report "
        "and a summary of FCRA rights. Plaintiff alleges this public document "
        "as evidence of Home Depot's longstanding knowledge of both its First "
        "Advantage screening relationship and the federal pre-adverse process "
        "required when it uses a consumer report for employment.",
    ),
    (
        "PARA",
        "19. In Bolton v. First Advantage LNS Screening Solutions, Inc., "
        "No. 1:14-cv-05735 (S.D.N.Y.), the district court's July 1, 2015 "
        "opinion recounts allegations by plaintiff Staples arising from a "
        "report First Advantage furnished to his prospective employer, Home "
        "Depot, in July 2013. That separate federal record independently "
        "corroborates a Home Depot-First Advantage employment-screening "
        "relationship.",
    ),
    (
        "PARA",
        "20. In December 2019, First Advantage publicly announced a "
        "workforce-screening webinar in which a First Advantage senior "
        "director would appear with representatives from The Home Depot, Gap, "
        "and IKEA to discuss screening practices for extended workforces. The "
        "announcement further corroborates an ongoing institutional "
        "relationship between First Advantage and Home Depot around workforce "
        "screening.",
    ),
    (
        "PARA",
        "21. Taken together with Plaintiff's own allegation that Home Depot "
        "required and ran a background check immediately before the accepted "
        "Tracy employment ended, these public records provide a concrete basis "
        "for alleging on information and belief that First Advantage was Home "
        "Depot's CRA for Plaintiff's 2024 screening. Whether a particular Home "
        "Depot affiliate placed the order, the exact First Advantage package "
        "ordered, the report's component results, and the particular "
        "adjudication fields are matters uniquely documented in Home Depot's "
        "and First Advantage's records.",
    ),
    ("HEADER", "FACTUAL ALLEGATIONS"),
    ("SUBHEAD", "A. The Tracy Hire and Onboarding"),
    (
        "PARA",
        "22. On or about August 2024, Home Depot hired Plaintiff for work at "
        "its Tracy Center at 5395 Hopkins Road.",
    ),
    (
        "PARA",
        "23. Plaintiff accepted the employment and began onboarding. The "
        "Tracy Center is a warehouse, distribution, and fulfillment facility. "
        "On information and belief, the position for which Plaintiff was hired "
        "was warehouse, distribution, or fulfillment work at that facility and "
        "was not a position regulated by the Secretary of Transportation "
        "within the limited exception in 15 U.S.C. section 1681b(b)(3)(B)-(C). "
        "Plaintiff was not hired as a commercial motor-vehicle driver for that "
        "Home Depot assignment.",
    ),
    (
        "PARA",
        "24. As part of the onboarding and employment-screening process, Home "
        "Depot procured or caused First Advantage to prepare a consumer report "
        "concerning Plaintiff for employment purposes.",
    ),
    (
        "SUBHEAD",
        "B. First Advantage's Screening of Plaintiff\nand the Comparator Record",
    ),
    (
        "PARA",
        "25. On information and belief, First Advantage prepared an employment "
        "consumer report concerning Plaintiff at Home Depot's request in or "
        "about August 2024 and furnished or made that report available to Home "
        "Depot through First Advantage's employer-screening platform.",
    ),
    (
        "PARA",
        "26. Plaintiff does not presently possess Home Depot's copy of that "
        "report or its complete First Advantage order file. Home Depot and "
        "First Advantage possess the precise order date, completion date, "
        "client/requestor profile, package identifier, component results, "
        "source fields, adjudication status, client criteria, access history, "
        "transmission history, and records identifying the information Home "
        "Depot reviewed.",
    ),
    (
        "PARA",
        "27. Plaintiff alleges that the Home Depot report contained "
        "information disclosed pursuant to Penal Code section 290.46, "
        "including Plaintiff's California sex-offender-registry information. "
        "That allegation is made on information and belief because the report "
        "and source fields are within Home Depot's and First Advantage's "
        "control, and it is supported by the factual pattern alleged below.",
    ),
    (
        "PARA",
        "28. At the time of Home Depot's screening, Plaintiff was publicly "
        "listed on California's Megan's Law website. Plaintiff's identity and "
        "underlying California registry entry were the same regardless of "
        "which employer requested a First Advantage employment screen; what "
        "could vary by employer was the screening package, adjudication "
        "configuration, or presentation of the underlying data.",
    ),
    (
        "PARA",
        "29. Plaintiff possesses a First Advantage employment background "
        "report concerning himself generated for United Parcel Service during "
        "the same general period. In that report, ordinary criminal-search "
        "components returned non-adverse results, while the "
        "sex-offender-registry component was the adverse or decisional "
        "component and expressly identified the source of record as the "
        "California Sex Offender Registry. That report demonstrates that First "
        "Advantage's screening of this same Plaintiff was capable of "
        "retrieving, reporting, and adjudicating his California registry "
        "information in an employment-screening product.",
    ),
    (
        "PARA",
        "30. In a separate employment screening for Federal Express "
        "Corporation, also conducted by First Advantage, FedEx later admitted "
        "in its responsive pleading that the report identified Plaintiff as a "
        "California registrant. Together, these separate First Advantage "
        "screenings of the same Plaintiff provide additional factual support "
        "for the allegation that First Advantage's contemporaneous Home Depot "
        "screening likewise contained Plaintiff's California registry "
        "information.",
    ),
    (
        "PARA",
        "31. Plaintiff does not allege that UPS's or FedEx's report is Home "
        "Depot's report. He alleges those comparator records because they "
        "concern the same consumer, the same CRA, the same underlying "
        "California registry entry, and the same type of employment background "
        "screening, and therefore make the alleged contents of the Home Depot "
        "report more than speculative.",
    ),
    (
        "PARA",
        "32. On information and belief, the registry information in the Home "
        "Depot report was adverse, decisional, review-triggering, ineligible, "
        "or otherwise material to Home Depot's screening result and employment "
        "decision. Home Depot's actual report, adjudication matrix, access "
        "history, applicant-tracking record, reason codes, and decisionmaker "
        "communications will identify the precise mechanism.",
    ),
    ("SUBHEAD", "C. The Adverse Employment Action"),
    (
        "PARA",
        "33. After the report was completed and transmitted, Home Depot ceased "
        "the onboarding process and stopped Plaintiff from beginning or "
        "continuing work at the Tracy Center.",
    ),
    (
        "PARA",
        "34. The adverse action occurred on or about August 2024, after the "
        "First Advantage report had been completed and made available to Home "
        "Depot.",
    ),
    (
        "PARA",
        "35. Home Depot did not identify to Plaintiff any independent "
        "post-report event that caused the accepted employment to end. "
        "Plaintiff alleges that Home Depot used the report, in whole or in "
        "part, in making the decision.",
    ),
    (
        "PARA",
        "36. The FCRA defines adverse action in the employment context to "
        "include a denial of employment or any other decision for employment "
        "purposes that adversely affects a current or prospective employee. "
        "Home Depot's withdrawal, ending, prevention, or non-finalization of "
        "the accepted employment was an adverse action.",
    ),
    (
        "SUBHEAD",
        "D. Home Depot Did Not Provide the Required\nPre-Adverse Package",
    ),
    (
        "PARA",
        "37. Before the adverse action became final, Home Depot did not "
        "provide Plaintiff a copy of the First Advantage report.",
    ),
    (
        "PARA",
        "38. Before the adverse action became final, Home Depot did not "
        "provide Plaintiff the written description of FCRA rights prescribed "
        "by 15 U.S.C. section 1681g(c)(3).",
    ),
    (
        "PARA",
        "39. Plaintiff therefore was not given the report and statutory rights "
        "information before Home Depot acted on the report. Had Home Depot "
        "complied, Plaintiff would have been able, before the employment "
        "decision became final, to identify that the report contained his "
        "California registry information, challenge or explain the report as "
        "appropriate, and advise Home Depot that Penal Code section "
        "290.46(j)(2)(E) prohibited use of information disclosed pursuant to "
        "section 290.46 for this employment purpose.",
    ),
    (
        "PARA",
        "40. Home Depot's failure caused concrete injury. Plaintiff lost an "
        "accepted employment opportunity and resulting wages and benefits. The "
        "omitted pre-adverse process was directly tied to that injury because "
        "it deprived Plaintiff of the opportunity to identify and challenge "
        "Home Depot's contemplated use of the same registry information that "
        "Plaintiff alleges Home Depot was legally prohibited from using for "
        "the employment decision.",
    ),
    (
        "SUBHEAD",
        "E. Home Depot Did Not Provide the ICRAA\nAdverse-Action Advice",
    ),
    (
        "PARA",
        "41. The First Advantage report was an investigative consumer report "
        "within the meaning of the California Investigative Consumer Reporting "
        "Agencies Act ('ICRAA') because it was prepared for employment "
        "purposes and contained information bearing on Plaintiff's character, "
        "general reputation, personal characteristics, or mode of living, "
        "including criminal / public-record and registry information.",
    ),
    (
        "PARA",
        "42. When Home Depot denied, withdrew, ended, or prevented the "
        "employment under circumstances in which the First Advantage "
        "investigative consumer report had been obtained, Home Depot did not "
        "advise Plaintiff that the report had been obtained and did not supply "
        "First Advantage's name and address.",
    ),
    (
        "PARA",
        "43. The omission alleged in paragraph 42 is distinct from the FCRA "
        "omission alleged in Count One. Count One concerns Home Depot's "
        "failure before adverse action to furnish the report and federal "
        "Summary of Rights. Count Two concerns Home Depot's separate "
        "California duty, upon denying employment under circumstances in which "
        "an investigative report was obtained, to advise Plaintiff and "
        "identify the investigative consumer reporting agency.",
    ),
    (
        "SUBHEAD",
        "F. Discovery of the Violations and Timeliness",
    ),
    (
        "PARA",
        "44. At the time Home Depot stopped the onboarding process in 2024, "
        "Plaintiff knew that the employment opportunity had ended. Home Depot "
        "did not give him the consumer report, identify First Advantage, "
        "disclose the report's contents, provide the statutory pre-adverse "
        "package, or otherwise reveal the report-based statutory violations "
        "alleged here. The 2024 employment result is not itself discovery of "
        "the FCRA or ICRAA omissions.",
    ),
    (
        "PARA",
        "45. Plaintiff still does not possess Home Depot's copy of the First "
        "Advantage report or First Advantage's Home Depot-specific consumer "
        "file. First Advantage reports generated for other employers, and "
        "public records identifying First Advantage as a Home Depot vendor, "
        "are not a substitute for discovery of what Home Depot obtained and "
        "used in this transaction. Those materials support the "
        "information-and-belief allegations in this Complaint; they do not "
        "fill the FCRA/ICRAA discovery date.",
    ),
    (
        "PARA",
        "46. Plaintiff has prepared statutory inspection requests to First "
        "Advantage under Civil Code sections 1786.10 and 1786.22, and a "
        "personnel-file request to Home Depot under Labor Code section 1198.5, "
        "to obtain the transaction-specific records. Those requests have not "
        "yet been treated as served. If they produce the Home Depot-specific "
        "report or file, that production may supply the precise discovery "
        "event. Plaintiff does not invent a discovery date in this review "
        "draft.",
    ),
    (
        "PARA",
        "47. Before filing, Plaintiff will insert the true date and event by "
        "which he first discovered the FCRA and ICRAA violations alleged in "
        "Counts One and Two. This action will be filed within two years after "
        "that discovery and within five years after the FCRA violation "
        "occurred. See 15 U.S.C. section 1681p; Cal. Civ. Code section "
        "1786.52. Do not file this Complaint with a blank or bracketed "
        "discovery date.",
    ),
    (
        "SUBHEAD",
        "G. California Registry Information and Home Depot's Use",
    ),
    (
        "PARA",
        "48. Plaintiff is a person as to whom information is disclosed on "
        "California's Megan's Law internet website established under Penal "
        "Code section 290.46.",
    ),
    (
        "PARA",
        "49. Plaintiff alleges, on information and belief and as an ultimate "
        "fact, that the First Advantage report furnished to Home Depot "
        "contained Plaintiff's information disclosed pursuant to Penal Code "
        "section 290.46.",
    ),
    (
        "PARA",
        "50. Plaintiff further alleges, on information and belief and as an "
        "ultimate fact, that Home Depot received, accessed, considered, and "
        "used that section 290.46 information for the purpose of deciding "
        "whether Plaintiff would begin or continue the accepted Tracy "
        "employment.",
    ),
    (
        "PARA",
        "51. Plaintiff alleges that the registry information was a substantial "
        "factor in Home Depot's adverse employment decision. The factual basis "
        "includes the accepted hire, the intervening First Advantage "
        "background check, Plaintiff's contemporaneous California registry "
        "listing, First Advantage's demonstrated reporting of that same "
        "California registry information in other employment screens of "
        "Plaintiff, the cessation of onboarding after the screen, and the "
        "absence of any communicated independent reason.",
    ),
    (
        "PARA",
        "52. The temporal sequence was: Home Depot accepted Plaintiff and "
        "began onboarding him; Home Depot procured the First Advantage "
        "employment screen; on information and belief, First Advantage "
        "furnished Plaintiff's California registry information as part of that "
        "screen; Home Depot received or accessed the screening result; and "
        "Home Depot then stopped the accepted employment. Plaintiff does not "
        "allege the Home Depot-specific source-field wording as known fact.",
    ),
    (
        "PARA",
        "53. Home Depot's use was for a purpose relating to employment within "
        "the meaning of section 290.46(j)(2)(E). The Tracy warehouse, "
        "distribution, and fulfillment position was not a position for which "
        "Plaintiff is aware of any law authorizing Home Depot to use "
        "information disclosed pursuant to section 290.46.",
    ),
    (
        "PARA",
        "54. The precise report labels, source-field wording, adjudication "
        "code, access timestamps, internal reason codes, and identity of the "
        "decisionmaker are evidentiary details within Home Depot's and First "
        "Advantage's possession. Plaintiff's inability to quote those internal "
        "records before discovery does not alter the factual allegation that "
        "Home Depot used Plaintiff's section 290.46 information for the "
        "employment decision.",
    ),
    (
        "PARA",
        "55. Any contention that Home Depot relied on some different source or "
        "reason is a merits defense to the factual allegations above. For "
        "purposes of this Complaint, Plaintiff alleges that the California "
        "registry information reported through First Advantage was used by "
        "Home Depot and was a substantial factor in the adverse employment "
        "action.",
    ),
    ("HEADER", "FIRST CAUSE OF ACTION"),
    (
        "SUBHEAD",
        "Fair Credit Reporting Act -- 15 U.S.C. section 1681b(b)(3)(A)\n"
        "Against Home Depot U.S.A., Inc.",
    ),
    ("PARA", "56. Plaintiff realleges paragraphs 1 through 55."),
    (
        "PARA",
        "57. Plaintiff was a 'consumer,' the First Advantage report was a "
        "'consumer report,' Home Depot procured or caused it to be procured "
        "for 'employment purposes,' and Home Depot was a 'person' using the "
        "report within the meaning of the FCRA.",
    ),
    (
        "PARA",
        "58. Under 15 U.S.C. section 1681b(b)(3)(A), before taking adverse "
        "action based in whole or in part on an employment consumer report, "
        "the person intending to take the adverse action must provide the "
        "consumer (i) a copy of the report and (ii) a written description of "
        "the consumer's rights under the FCRA.",
    ),
    (
        "PARA",
        "59. Home Depot took adverse employment action based in whole or in "
        "part on the First Advantage report.",
    ),
    (
        "PARA",
        "60. Home Depot did not provide Plaintiff a copy of the report before "
        "the adverse action.",
    ),
    (
        "PARA",
        "61. Home Depot did not provide Plaintiff the written Summary of "
        "Rights before the adverse action.",
    ),
    (
        "PARA",
        "62. Home Depot therefore violated section 1681b(b)(3)(A).",
    ),
    (
        "PARA",
        "63. Home Depot's noncompliance was negligent within the meaning of "
        "15 U.S.C. section 1681o and, on proof, willful within the meaning of "
        "15 U.S.C. section 1681n. Willfulness is plausibly supported by Home "
        "Depot's own publicly filed background-check form, which expressly "
        "recognized that before information from a consumer or investigative "
        "consumer report is used to make an adverse employment decision, Home "
        "Depot would provide the applicant the report and a summary of FCRA "
        "rights. That standardized language demonstrates corporate awareness "
        "of the pre-adverse obligation years before Plaintiff's screening. "
        "Home Depot has also previously litigated FCRA employment-screening "
        "obligations in federal court, including Harris v. Home Depot U.S.A., "
        "Inc., 114 F. Supp. 3d 868 (N.D. Cal. 2015), which addressed Home "
        "Depot's employment consumer-report disclosure practices. Plaintiff "
        "does not presently plead a claim under 15 U.S.C. section "
        "1681b(b)(2)(A). Harris is alleged as additional evidence that Home "
        "Depot is a sophisticated FCRA user of employment consumer reports, "
        "together with the Ford form's own pre-adverse language. Plaintiff "
        "pleads negligence and willfulness in the alternative.",
    ),
    (
        "PARA",
        "64. As a direct result, Plaintiff suffered actual damages including "
        "lost employment compensation and the loss of the statutory "
        "opportunity to review and respond to the report before the employment "
        "decision. If willfulness is proven, Plaintiff also seeks statutory "
        "and punitive damages authorized by section 1681n.",
    ),
    ("HEADER", "SECOND CAUSE OF ACTION"),
    (
        "SUBHEAD",
        "California Investigative Consumer Reporting Agencies Act\n"
        "Cal. Civ. Code sections 1786.40, 1786.50\n"
        "Against Home Depot U.S.A., Inc.",
    ),
    ("PARA", "65. Plaintiff realleges paragraphs 1 through 55."),
    (
        "PARA",
        "66. The First Advantage employment background report was an "
        "investigative consumer report within ICRAA.",
    ),
    (
        "PARA",
        "67. California Civil Code section 1786.40(a) provides that when "
        "employment involving a consumer is denied under circumstances in "
        "which a report regarding the consumer was obtained from an "
        "investigative consumer reporting agency, the user shall advise the "
        "consumer against whom the adverse action was taken and supply the "
        "name and address of the investigative consumer reporting agency "
        "making the report.",
    ),
    (
        "PARA",
        "68. Home Depot denied, withdrew, ended, or prevented Plaintiff's "
        "employment under circumstances in which it had obtained the First "
        "Advantage investigative consumer report.",
    ),
    (
        "PARA",
        "69. Home Depot did not provide the advice required by section 1786.40 "
        "and did not supply First Advantage's name and address at the time of "
        "the adverse employment action.",
    ),
    (
        "PARA",
        "70. This section 1786.40 omission is pleaded as a separate act or "
        "omission from the pre-adverse FCRA violation in Count One.",
    ),
    (
        "PARA",
        "71. Under Civil Code section 1786.50, Plaintiff seeks actual damages "
        "or $10,000, whichever is greater, together with costs and any "
        "attorney's fees recoverable if counsel later appears. If the "
        "violation is proven grossly negligent or willful, Plaintiff seeks "
        "punitive damages as authorized by section 1786.50(b). Home Depot's "
        "California-specific background-check disclosure publicly identified "
        "First Advantage by name, address, and telephone number years before "
        "the events here, supporting an inference that Home Depot was familiar "
        "with the identity of its investigative CRA and the California "
        "regulatory framework governing those reports.",
    ),
    ("HEADER", "THIRD CAUSE OF ACTION"),
    (
        "SUBHEAD",
        "Unauthorized Employment Use of Registry Information\n"
        "Cal. Penal Code section 290.46(j)(2)(E) and (j)(4)(A)\n"
        "Against Home Depot U.S.A., Inc.",
    ),
    ("PARA", "72. Plaintiff realleges paragraphs 1 through 55."),
    (
        "PARA",
        "73. Penal Code section 290.46(j)(1) authorizes use of information "
        "disclosed pursuant to section 290.46 only to protect a person at "
        "risk, except as otherwise authorized by law.",
    ),
    (
        "PARA",
        "74. Section 290.46(j)(2)(E) prohibits use of information disclosed "
        "pursuant to section 290.46 for purposes relating to employment except "
        "as authorized by paragraph (1) or another provision of law.",
    ),
    (
        "PARA",
        "75. Plaintiff alleges, on information and belief and as an ultimate "
        "fact, that the First Advantage report furnished to Home Depot "
        "contained information disclosed pursuant to Penal Code section "
        "290.46, including Plaintiff's California registry information.",
    ),
    (
        "PARA",
        "76. Plaintiff alleges, on information and belief and as an ultimate "
        "fact, that Home Depot received, accessed, considered, and used that "
        "section 290.46 information for a purpose relating to employment.",
    ),
    (
        "PARA",
        "77. Plaintiff alleges that the section 290.46 information was a "
        "substantial factor in Home Depot's decision to deny, withdraw, end, "
        "or prevent Plaintiff's Tracy employment. The factual basis is stated "
        "in paragraphs 25 through 32 and 48 through 55, including First "
        "Advantage's reporting of this same Plaintiff's California registry "
        "information in comparator employment screens, Home Depot's "
        "procurement of the intervening background check, the cessation of "
        "onboarding after that screen, and the absence of any communicated "
        "independent reason.",
    ),
    (
        "PARA",
        "78. The pleaded use was not authorized by section 290.46(j)(1), and "
        "Plaintiff is unaware of another law authorizing Home Depot to use "
        "information disclosed pursuant to section 290.46 for the Tracy "
        "warehouse, distribution, and fulfillment position.",
    ),
    (
        "PARA",
        "79. Home Depot thereby violated section 290.46(j)(2)(E).",
    ),
    (
        "PARA",
        "80. Section 290.46(j)(4)(A) makes a prohibited user liable for the "
        "civil remedies specified in that subdivision. Plaintiff seeks actual "
        "damages, any additional amount authorized by the statute, exemplary "
        "relief to the extent proven and legally available, attorney's fees if "
        "counsel later appears and the statute authorizes recovery, and any "
        "other nonduplicative remedy available under section 290.46(j)(4)(A).",
    ),
    (
        "PARA",
        "81. Plaintiff does not presently seek preventive relief under "
        "section 290.46(j)(4)(B). This complaint alleges Plaintiff's "
        "transaction. If discovery establishes a pattern or practice and "
        "Article III requirements are independently satisfied, Plaintiff may "
        "seek leave to amend.",
    ),
    ("HEADER", "DAMAGES"),
    (
        "PARA",
        "82. As a direct and proximate result of Home Depot's conduct, "
        "Plaintiff suffered economic loss including lost wages, lost "
        "employment benefits, lost earning opportunity, job-search and "
        "reliance expenses according to proof.",
    ),
    (
        "PARA",
        "83. Plaintiff also suffered emotional distress, humiliation, "
        "frustration, and loss of dignity resulting from the manner in which "
        "the accepted employment was ended without the report and process "
        "required by law, to the extent recoverable under the governing causes "
        "of action.",
    ),
    (
        "PARA",
        "84. Plaintiff seeks only nonduplicative recovery. Where multiple "
        "statutes provide remedies for the same injury, Plaintiff will elect "
        "or apportion remedies as required to prevent double recovery.",
    ),
    ("HEADER", "PRAYER FOR RELIEF"),
    (
        "PARA",
        "WHEREFORE, Plaintiff respectfully requests judgment against Defendant "
        "HOME DEPOT U.S.A., INC. as follows:",
    ),
    (
        "LIST_ITEM",
        "A. Actual and compensatory damages according to proof, including lost "
        "employment compensation and consequential economic loss;",
    ),
    (
        "LIST_ITEM",
        "B. The remedies authorized by 15 U.S.C. sections 1681n and 1681o, "
        "including statutory and punitive damages if willfulness is proven;",
    ),
    (
        "LIST_ITEM",
        "C. The remedies authorized by California Civil Code section 1786.50, "
        "including actual damages or $10,000, whichever is greater, and "
        "punitive damages upon the showing required by statute;",
    ),
    (
        "LIST_ITEM",
        "D. The remedies authorized by California Penal Code section "
        "290.46(j)(4)(A), without duplicative recovery;",
    ),
    (
        "LIST_ITEM",
        "E. Taxable costs and attorney's fees only to the extent authorized "
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
        "Pursuant to Federal Rule of Civil Procedure 38 and the Seventh "
        "Amendment, Plaintiff demands a trial by jury on all issues so "
        "triable.",
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


def main() -> None:
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
