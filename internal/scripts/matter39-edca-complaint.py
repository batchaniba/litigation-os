#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Matter 39 — E.D. Cal. federal complaint review draft (Best Buy).

REVIEW DRAFT. Not for filing until the FCRA/ICRAA discovery date is filled
and Plaintiff signs. The September 8, 2026 San Joaquin packet is historical
work product; it was never clerk-filed.

    python3 internal/scripts/matter39-edca-complaint.py
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
    / "internal/public/documents/matter-39"
    / "EDCA Complaint Review Draft - Ngwa Nforbi v Best Buy Co Inc"
    " (Sep 15 2026).pdf"
)

DOC_TITLE_FOOTER = (
    "COMPLAINT FOR DAMAGES -- NGWA NFORBI v. BEST BUY CO., INC. "
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
    ("BEST BUY CO., INC.,", True, False),
    ("a Minnesota corporation,", True, False),
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
        "REVIEW DRAFT -- NOT FOR FILING. Confirm that May 29, 2026 is the "
        "first date Plaintiff understood the FCRA and ICRAA process omissions "
        "in the Tracy screen. Count Three does not use that date. Count Three "
        "is timely under Code of Civil Procedure section 338(a) from the "
        "October 2023 employment use; three years from October 17, 2023 is "
        "October 17, 2026. Confirm the Tracy position is not DOT-excepted, "
        "and have Plaintiff sign before any filing. Serve Best Buy's current "
        "California Secretary of State agent, not 6653 Hopkins Road.",
    ),
    (
        "PARA",
        "Plaintiff BRENDAN NGWA NFORBI, appearing in propria persona, alleges "
        "against Defendant BEST BUY CO., INC. ('Best Buy') as follows:",
    ),
    ("HEADER", "INTRODUCTION"),
    (
        "PARA",
        "1. This action arises from an accepted Best Buy hire at its warehouse "
        "at 6653 Hopkins Road, Tracy, California. On October 17, 2023, Best "
        "Buy offered Plaintiff the General Warehouse Worker / 2nd Shift "
        "position at $22.60 per hour, requisition 928556BR. Plaintiff accepted "
        "the offer. The same afternoon Best Buy required a background check, "
        "named First Advantage as the screening vendor, and through First "
        "Advantage ordered a drug test. Plaintiff completed the drug "
        "screening. On information and belief, that screen came back clean. "
        "Best Buy then ceased communication and ghosted him.",
    ),
    (
        "PARA",
        "2. Best Buy procured or caused First Advantage to prepare a consumer "
        "report concerning Plaintiff for employment purposes and took adverse "
        "action based in whole or in part on that report without first "
        "providing Plaintiff (i) a copy of the report and (ii) a written "
        "description of his rights under the Fair Credit Reporting Act, "
        "15 U.S.C. section 1681b(b)(3)(A).",
    ),
    (
        "PARA",
        "3. When Best Buy denied, withdrew, ended, or prevented the employment "
        "under circumstances in which it had obtained an investigative "
        "consumer report, it also did not advise Plaintiff that such a report "
        "had been obtained and did not provide First Advantage's name and "
        "address as required by California Civil Code section 1786.40.",
    ),
    (
        "PARA",
        "4. California Penal Code section 290.46(j)(2)(E) prohibits use of "
        "information disclosed pursuant to California's Megan's Law website "
        "for purposes relating to employment except where another law "
        "authorizes the use. Plaintiff alleges, on information and belief and "
        "as an ultimate fact, that First Advantage furnished Best Buy "
        "information concerning Plaintiff that was disclosed pursuant to "
        "section 290.46, including Plaintiff's California registry information, "
        "and that Best Buy used that information for the purpose of deciding "
        "whether Plaintiff would begin or continue the accepted Tracy "
        "employment.",
    ),
    (
        "PARA",
        "5. That allegation is supported by specific facts rather than "
        "conjecture: Best Buy made a written offer and required a same-day "
        "background check; Best Buy's own October 17, 2023 emails named First "
        "Advantage as the screening vendor and First Advantage ordered a Best "
        "Buy drug test the same afternoon; Plaintiff accepted the offer and "
        "completed the drug screening; Plaintiff was contemporaneously listed "
        "on California's Megan's Law website; First Advantage reports "
        "concerning this same Plaintiff for other employers during the "
        "surrounding period included sex-offender-registry screening and "
        "California-registry information; and Best Buy then ceased "
        "communication without communicating an independent reason. The "
        "transaction-specific report, source fields, adjudication codes, "
        "access logs, and decision records are in Best Buy's and First "
        "Advantage's possession.",
    ),
    (
        "PARA",
        "6. A written rejection letter is not an element of 15 U.S.C. section "
        "1681b(b)(3)(A), Civil Code section 1786.40, or Penal Code section "
        "290.46(j). Silence after an accepted offer is the employment "
        "decision. No written rejection is in Plaintiff's files.",
    ),
    ("HEADER", "JURISDICTION AND VENUE"),
    (
        "PARA",
        "7. This Court has original subject-matter jurisdiction under 28 U.S.C. "
        "section 1331 because Count One arises under the Fair Credit Reporting "
        "Act, 15 U.S.C. section 1681 et seq. Section 1681p expressly "
        "authorizes an action to enforce FCRA liability in an appropriate "
        "United States district court without regard to the amount in "
        "controversy.",
    ),
    (
        "PARA",
        "8. This Court has supplemental jurisdiction over Counts Two and Three "
        "under 28 U.S.C. section 1367(a) because those California claims arise "
        "from the same employment screening, consumer report, and adverse "
        "employment decision as the FCRA claim and form part of the same case "
        "or controversy.",
    ),
    (
        "PARA",
        "9. This Court also has original jurisdiction in the alternative "
        "under 28 U.S.C. section 1332(a) because the matter in controversy "
        "exceeds $75,000, exclusive of interest and costs, and is between "
        "citizens of different States. Plaintiff is a citizen of California. "
        "Best Buy Co., Inc. is a corporation organized under the laws of "
        "Minnesota with its principal place of business in Richfield, "
        "Minnesota. The amount-in-controversy allegation aggregates lost "
        "compensation from the accepted Tracy employment according to proof "
        "at the offered rate of $22.60 per hour; FCRA actual damages and, if "
        "willfulness is proven, statutory and punitive damages; ICRAA actual "
        "damages or $10,000, whichever is greater, plus punitive damages if "
        "the statutory showing is met; and remedies authorized by Penal Code "
        "section 290.46(j)(4)(A). The offer does not state weekly hours or a "
        "start date. Plaintiff does not invent those figures.",
    ),
    (
        "PARA",
        "10. Venue is proper in the Eastern District of California under "
        "28 U.S.C. section 1391(b)(2) because a substantial part of the events "
        "giving rise to the claims occurred in Tracy, San Joaquin County, "
        "California.",
    ),
    (
        "PARA",
        "11. Under Eastern District of California Local Rule 120(d), civil "
        "actions arising in San Joaquin County are commenced in the Sacramento "
        "Division.",
    ),
    ("HEADER", "PARTIES"),
    (
        "PARA",
        "12. Plaintiff BRENDAN NGWA NFORBI is a natural person and resident of "
        "San Joaquin County, California. He is also identified in employment "
        "and court records as Brendan Ngehsi Ngwanforbi. Those name variants "
        "refer to Plaintiff. He was the consumer and accepted hire who was "
        "the subject of the employment background report and adverse "
        "employment decision alleged herein. The October 17, 2023 First "
        "Advantage drug-test order used BRENDAN NGWA NFORBI.",
    ),
    (
        "PARA",
        "13. Defendant BEST BUY CO., INC. is a corporation organized under "
        "the laws of the State of Minnesota, doing business as Best Buy. Its "
        "principal place of business is 7601 Penn Avenue South, Richfield, "
        "Minnesota 55423. The October 17, 2023 background-check authorization "
        "identifies 'Best Buy and/or its subsidiaries, affiliates other "
        "related entities, successors, and/or assigns' as the 'Company,' and "
        "directs correspondence to Best Buy Co. Inc., ATTN: Employment "
        "Screening, at that Richfield address. The First Advantage drug-test "
        "order lists the employer as BEST BUY, same Richfield address. On "
        "information and belief, Best Buy Co., Inc. offered Plaintiff the "
        "warehouse job and caused the background check and drug test to be "
        "ordered. The Tracy warehouse is a worksite, not a separate legal "
        "entity.",
    ),
    (
        "PARA",
        "14. Plaintiff will serve Best Buy through its designated agent for "
        "service of process on the California Secretary of State record as of "
        "the date of service. Public records identify C T Corporation System "
        "as Best Buy's registered agent in multiple jurisdictions. Plaintiff "
        "will confirm the current California listing immediately before "
        "service. Service is not to be made at 6653 Hopkins Road, Tracy, "
        "merely because that is the worksite, and is not to be made at Jose "
        "Tapia's telephone number merely because he signed the offer email.",
    ),
    (
        "PARA",
        "15. First Advantage Background Services Corp. ('First Advantage') is "
        "the consumer reporting agency Best Buy used for Plaintiff's "
        "screening. Best Buy's October 17, 2023 Minnesota disclosure named "
        "First Advantage Consumer Center, P.O. Box 105292, Atlanta, GA "
        "30348-5292, (800) 845-6004, www.FADV.com. The same afternoon First "
        "Advantage Corporation Reporting Service emailed Plaintiff a Best Buy "
        "drug-test order, Re:Quest QPassport/Barcode Q09078711, account BEST "
        "BUY (11759586), and stated that the employer had been sent a copy. "
        "Plaintiff does not presently name First Advantage as a defendant. "
        "The report, order records, transmission logs, access logs, "
        "adjudication data, user certifications, service agreement, screening "
        "package, and client-specific adjudication criteria are discoverable "
        "from Best Buy and First Advantage.",
    ),
    (
        "PARA",
        "16. Jose Tapia identified himself as General Manager on the October "
        "17, 2023 offer email. Daisy Calvary (daisy.calvary@bestbuy.com) was "
        "named as a drug-screen contact. They are percipient witnesses, not "
        "presently named as defendants.",
    ),
    ("HEADER", "FACTUAL ALLEGATIONS"),
    ("SUBHEAD", "A. The Application, the Offer, and the Tracy Warehouse"),
    (
        "PARA",
        "17. On Friday, October 13, 2023, at 7:29 a.m., Best Buy Human "
        "Resources emailed Plaintiff that it had received his submission for "
        "General Warehouse Worker / 2nd Shift at $22.60, requisition 928556BR. "
        "The email described the work as loading, unloading, and processing "
        "merchandise, moving product inside a distribution center, and using "
        "forklifts and other powered equipment, with a basic qualification of "
        "lifting up to 75 pounds.",
    ),
    (
        "PARA",
        "18. On Tuesday, October 17, 2023, at 3:47 p.m., Jose Tapia, General "
        "Manager, emailed a congratulations offer for that job at Best Buy's "
        "warehouse at 6653 Hopkins Road, Tracy, California 95377, and "
        "required, within 24 hours, Candidate Zone signature, background-check "
        "information, and background-check authorization.",
    ),
    (
        "PARA",
        "19. The Tracy warehouse is a warehouse / distribution facility. The "
        "offered position was General Warehouse Worker / 2nd Shift. On "
        "information and belief, the position was not a position regulated by "
        "the Secretary of Transportation within the limited exception in "
        "15 U.S.C. section 1681b(b)(3)(B)-(C). Plaintiff was not hired as a "
        "commercial motor-vehicle driver for that Best Buy assignment.",
    ),
    (
        "PARA",
        "20. Plaintiff accepted the offer. At 5:31 p.m. that day, Best Buy HR "
        "wrote 'Congratulations on accepting your offer.' That sentence is "
        "Best Buy's characterization. Plaintiff independently accepted.",
    ),
    (
        "SUBHEAD",
        "B. First Advantage's Screening of Plaintiff\nand the Comparator Record",
    ),
    (
        "PARA",
        "21. At 4:22 p.m. on October 17, 2023, Best Buy sent a "
        "background-authorization confirmation naming First Advantage "
        "Consumer Center. California disclosure PDFs were attached to the "
        "offer sequence. Those PDFs are not in Plaintiff's present files, and "
        "Plaintiff does not allege their internal wording as known fact.",
    ),
    (
        "PARA",
        "22. At 4:30 p.m., First Advantage ordered a Best Buy drug test, "
        "order Q09078711, account BEST BUY 11759586. A Quest Diagnostics "
        "collection site in Modesto, California, appears on the order as one "
        "available site. That is a collection option, not the worksite.",
    ),
    (
        "PARA",
        "23. Plaintiff completed the drug screening. On information and "
        "belief, that screen came back clean. No drug-test result PDF is in "
        "Plaintiff's files.",
    ),
    (
        "PARA",
        "24. On information and belief, First Advantage prepared an employment "
        "consumer report concerning Plaintiff at Best Buy's request on or "
        "about October 17, 2023, and furnished or made that report available "
        "to Best Buy through First Advantage's employer-screening platform.",
    ),
    (
        "PARA",
        "25. Plaintiff does not presently possess Best Buy's copy of that "
        "report or its complete First Advantage order file. Best Buy and "
        "First Advantage possess the precise order date, completion date, "
        "client/requestor profile, package identifier, component results, "
        "source fields, adjudication status, client criteria, access history, "
        "transmission history, and records identifying the information Best "
        "Buy reviewed.",
    ),
    (
        "PARA",
        "26. Plaintiff alleges that the Best Buy report contained information "
        "disclosed pursuant to Penal Code section 290.46, including "
        "Plaintiff's California sex-offender-registry information. That "
        "allegation is made on information and belief because the report and "
        "source fields are within Best Buy's and First Advantage's control, "
        "and it is supported by the factual pattern alleged below.",
    ),
    (
        "PARA",
        "27. At the time of Best Buy's screening, Plaintiff was publicly "
        "listed on California's Megan's Law website. Plaintiff's identity and "
        "underlying California registry entry were the same regardless of "
        "which employer requested a First Advantage employment screen; what "
        "could vary by employer was the screening package, adjudication "
        "configuration, or presentation of the underlying data.",
    ),
    (
        "PARA",
        "28. Plaintiff possesses a First Advantage employment background "
        "report concerning himself generated for United Parcel Service during "
        "the surrounding period. In that report, ordinary criminal-search "
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
        "29. In a separate employment screening for Federal Express "
        "Corporation, also conducted by First Advantage, FedEx later admitted "
        "in its responsive pleading that the report identified Plaintiff as a "
        "California registrant. Together, these separate First Advantage "
        "screenings of the same Plaintiff provide additional factual support "
        "for the allegation that First Advantage's contemporaneous Best Buy "
        "screening likewise contained Plaintiff's California registry "
        "information.",
    ),
    (
        "PARA",
        "30. Plaintiff does not allege that UPS's or FedEx's report is Best "
        "Buy's report. He alleges those comparator records because they "
        "concern the same consumer, the same CRA, the same underlying "
        "California registry entry, and the same type of employment background "
        "screening, and therefore make the alleged contents of the Best Buy "
        "report more than speculative.",
    ),
    (
        "PARA",
        "31. On information and belief, the registry information in the Best "
        "Buy report was adverse, decisional, review-triggering, ineligible, "
        "or otherwise material to Best Buy's screening result and employment "
        "decision. Best Buy's actual report, adjudication matrix, access "
        "history, applicant-tracking record, reason codes, and decisionmaker "
        "communications will identify the precise mechanism.",
    ),
    ("SUBHEAD", "C. The Adverse Employment Action"),
    (
        "PARA",
        "32. After the report was completed and transmitted, Best Buy ceased "
        "communication and stopped Plaintiff from beginning work at the Tracy "
        "warehouse. That cessation is the adverse employment action: it "
        "denied, withdrew, or ended the accepted warehouse job.",
    ),
    (
        "PARA",
        "33. The adverse action occurred on or after October 17, 2023, after "
        "the First Advantage report had been completed and made available to "
        "Best Buy. The file contains no dated rejection letter.",
    ),
    (
        "PARA",
        "34. Best Buy did not identify to Plaintiff any independent "
        "post-report event that caused the accepted employment to end. "
        "Plaintiff alleges that Best Buy used the report, in whole or in "
        "part, in making the decision.",
    ),
    (
        "PARA",
        "35. The FCRA defines adverse action in the employment context to "
        "include a denial of employment or any other decision for employment "
        "purposes that adversely affects a current or prospective employee. "
        "Best Buy's withdrawal, ending, prevention, or non-finalization of "
        "the accepted employment was an adverse action.",
    ),
    (
        "SUBHEAD",
        "D. Best Buy Did Not Provide the Required\nPre-Adverse Package",
    ),
    (
        "PARA",
        "36. Before the adverse action became final, Best Buy did not provide "
        "Plaintiff a copy of the First Advantage report.",
    ),
    (
        "PARA",
        "37. Before the adverse action became final, Best Buy did not provide "
        "Plaintiff the written description of FCRA rights prescribed by "
        "15 U.S.C. section 1681g(c)(3).",
    ),
    (
        "PARA",
        "38. Plaintiff therefore was not given the report and statutory rights "
        "information before Best Buy acted on the report. Had Best Buy "
        "complied, Plaintiff would have been able, before the employment "
        "decision became final, to identify that the report contained his "
        "California registry information, challenge or explain the report as "
        "appropriate, and advise Best Buy that Penal Code section "
        "290.46(j)(2)(E) prohibited use of information disclosed pursuant to "
        "section 290.46 for this employment purpose.",
    ),
    (
        "PARA",
        "39. Best Buy's failure caused concrete injury. Plaintiff lost an "
        "accepted employment opportunity and resulting wages at the offered "
        "rate of $22.60 per hour. The omitted pre-adverse process was "
        "directly tied to that injury because it deprived Plaintiff of the "
        "opportunity to identify and challenge Best Buy's contemplated use of "
        "the same registry information that Plaintiff alleges Best Buy was "
        "legally prohibited from using for the employment decision.",
    ),
    (
        "SUBHEAD",
        "E. Best Buy Did Not Provide the ICRAA\nAdverse-Action Advice",
    ),
    (
        "PARA",
        "40. The First Advantage report was an investigative consumer report "
        "within the meaning of the California Investigative Consumer Reporting "
        "Agencies Act ('ICRAA') because it was prepared for employment "
        "purposes and contained information bearing on Plaintiff's character, "
        "general reputation, personal characteristics, or mode of living, "
        "including criminal / public-record and registry information.",
    ),
    (
        "PARA",
        "41. When Best Buy denied, withdrew, ended, or prevented the "
        "employment under circumstances in which the First Advantage "
        "investigative consumer report had been obtained, Best Buy did not "
        "advise Plaintiff that the report had been obtained and did not supply "
        "First Advantage's name and address as required by Civil Code section "
        "1786.40. Naming First Advantage on the earlier authorization is not "
        "the section 1786.40 advice due at adverse action.",
    ),
    (
        "PARA",
        "42. The omission alleged in paragraph 41 is distinct from the FCRA "
        "omission alleged in Count One. Count One concerns Best Buy's "
        "failure before adverse action to furnish the report and federal "
        "Summary of Rights. Count Two concerns Best Buy's separate California "
        "duty, upon denying employment under circumstances in which an "
        "investigative report was obtained, to advise Plaintiff and identify "
        "the investigative consumer reporting agency.",
    ),
    (
        "PARA",
        "43. No pre-adverse letter, adverse letter, or copy of the Best Buy "
        "First Advantage report is in Plaintiff's files.",
    ),
    (
        "SUBHEAD",
        "F. Discovery of the FCRA and ICRAA Violations\nand Timeliness",
    ),
    (
        "PARA",
        "44. At the time Best Buy stopped communicating after the October 17, "
        "2023 offer, Plaintiff knew that the employment opportunity had ended. "
        "That is when he knew he had been harmed in the ordinary sense: he "
        "had lost the accepted Tracy hire. Best Buy had already identified "
        "First Advantage as the screening vendor on the authorization. Best "
        "Buy did not give him the consumer report, disclose the report's "
        "contents, provide the statutory pre-adverse package, or advise him "
        "at the time of adverse action that an investigative consumer report "
        "had been obtained. The 2023 employment result is not discovery of "
        "the FCRA or ICRAA violations alleged in Counts One and Two.",
    ),
    (
        "PARA",
        "45. Plaintiff still does not possess Best Buy's copy of the First "
        "Advantage report or First Advantage's Best Buy-specific consumer "
        "file. First Advantage reports generated for other employers support "
        "the information-and-belief allegations about what Best Buy's screen "
        "contained. They are not Best Buy's report, and they are not pleaded "
        "as the discovery event for Counts One and Two.",
    ),
    (
        "PARA",
        "46. On or about May 29, 2026, Plaintiff first understood that Best "
        "Buy had obtained a consumer report and an investigative consumer "
        "report in connection with the Tracy hire and had taken adverse "
        "action without providing the FCRA pre-adverse package or the Civil "
        "Code section 1786.40 advice. Until that date, Best Buy's silence "
        "had disclosed only the employment result. That is the date of "
        "discovery of the violations alleged in Counts One and Two. Plaintiff "
        "does not allege that May 29, 2026 is the date he first knew he had "
        "lost the job.",
    ),
    (
        "PARA",
        "47. Counts One and Two are filed within two years after that "
        "discovery and within five years after the FCRA violation occurred. "
        "See 15 U.S.C. section 1681p; Cal. Civ. Code section 1786.52. "
        "Plaintiff has prepared statutory inspection requests to First "
        "Advantage under Civil Code sections 1786.10 and 1786.22, and a "
        "personnel-file request to Best Buy under Labor Code section 1198.5. "
        "Those requests have not yet been treated as served.",
    ),
    (
        "SUBHEAD",
        "G. California Registry Information and Best Buy's Use",
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
        "fact, that the First Advantage report furnished to Best Buy "
        "contained Plaintiff's information disclosed pursuant to Penal Code "
        "section 290.46.",
    ),
    (
        "PARA",
        "50. Plaintiff further alleges, on information and belief and as an "
        "ultimate fact, that Best Buy received, accessed, considered, and "
        "used that section 290.46 information for the purpose of deciding "
        "whether Plaintiff would begin or continue the accepted Tracy "
        "employment.",
    ),
    (
        "PARA",
        "51. Plaintiff alleges that the registry information was a substantial "
        "factor in Best Buy's adverse employment decision. The factual basis "
        "includes the written offer, the same-day First Advantage background "
        "check, Plaintiff's contemporaneous California registry listing, First "
        "Advantage's demonstrated reporting of that same California registry "
        "information in other employment screens of Plaintiff, the cessation "
        "of communication after the screen, and the absence of any "
        "communicated independent reason.",
    ),
    (
        "PARA",
        "52. The temporal sequence was: Best Buy offered Plaintiff the Tracy "
        "warehouse job; Plaintiff accepted; Best Buy procured the First "
        "Advantage employment screen the same afternoon; on information and "
        "belief, First Advantage furnished Plaintiff's California registry "
        "information as part of that screen; Best Buy received or accessed "
        "the screening result; and Best Buy then stopped the accepted "
        "employment. Plaintiff does not allege the Best Buy-specific "
        "source-field wording as known fact.",
    ),
    (
        "PARA",
        "53. Best Buy's use was for a purpose relating to employment within "
        "the meaning of section 290.46(j)(2)(E). The Tracy warehouse position "
        "was not a position for which Plaintiff is aware of any law "
        "authorizing Best Buy to use information disclosed pursuant to "
        "section 290.46.",
    ),
    (
        "PARA",
        "54. The precise report labels, source-field wording, adjudication "
        "code, access timestamps, internal reason codes, and identity of the "
        "decisionmaker are evidentiary details within Best Buy's and First "
        "Advantage's possession. Plaintiff's inability to quote those internal "
        "records before discovery does not alter the factual allegation that "
        "Best Buy used Plaintiff's section 290.46 information for the "
        "employment decision.",
    ),
    (
        "PARA",
        "55. Any contention that Best Buy relied on some different source or "
        "reason is a merits defense to the factual allegations above. For "
        "purposes of this Complaint, Plaintiff alleges that the California "
        "registry information reported through First Advantage was used by "
        "Best Buy and was a substantial factor in the adverse employment "
        "action.",
    ),
    ("HEADER", "FIRST CAUSE OF ACTION"),
    (
        "SUBHEAD",
        "Fair Credit Reporting Act -- 15 U.S.C. section 1681b(b)(3)(A)\n"
        "Against Best Buy Co., Inc.",
    ),
    (
        "PARA",
        "56. Plaintiff realleges paragraphs 1 through 55, including paragraphs "
        "44 through 47 as to this count.",
    ),
    (
        "PARA",
        "57. Plaintiff was a 'consumer,' the First Advantage report was a "
        "'consumer report,' Best Buy procured or caused it to be procured "
        "for 'employment purposes,' and Best Buy was a 'person' using the "
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
        "59. Best Buy took adverse employment action based in whole or in "
        "part on the First Advantage report.",
    ),
    (
        "PARA",
        "60. Best Buy did not provide Plaintiff a copy of the report before "
        "the adverse action.",
    ),
    (
        "PARA",
        "61. Best Buy did not provide Plaintiff the written Summary of "
        "Rights before the adverse action.",
    ),
    (
        "PARA",
        "62. Best Buy therefore violated section 1681b(b)(3)(A).",
    ),
    (
        "PARA",
        "63. Best Buy's noncompliance was negligent within the meaning of "
        "15 U.S.C. section 1681o and, on proof, willful within the meaning of "
        "15 U.S.C. section 1681n. Willfulness is plausibly supported by Best "
        "Buy's own October 17, 2023 authorization, which named First Advantage "
        "and required background-check authorization the same afternoon as a "
        "written job offer, demonstrating corporate awareness that it was "
        "procuring an employment consumer report. Plaintiff does not presently "
        "plead a claim under 15 U.S.C. section 1681b(b)(2)(A). Plaintiff "
        "pleads negligence and willfulness in the alternative.",
    ),
    (
        "PARA",
        "64. As a direct result, Plaintiff suffered actual damages including "
        "lost employment compensation at the offered rate of $22.60 per hour "
        "according to proof, and the loss of the statutory opportunity to "
        "review and respond to the report before the employment decision. If "
        "willfulness is proven, Plaintiff also seeks statutory and punitive "
        "damages authorized by section 1681n.",
    ),
    ("HEADER", "SECOND CAUSE OF ACTION"),
    (
        "SUBHEAD",
        "California Investigative Consumer Reporting Agencies Act\n"
        "Cal. Civ. Code sections 1786.40, 1786.50\n"
        "Against Best Buy Co., Inc.",
    ),
    (
        "PARA",
        "65. Plaintiff realleges paragraphs 1 through 55, including paragraphs "
        "44 through 47 as to this count.",
    ),
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
        "68. Best Buy denied, withdrew, ended, or prevented Plaintiff's "
        "employment under circumstances in which it had obtained the First "
        "Advantage investigative consumer report.",
    ),
    (
        "PARA",
        "69. Best Buy did not provide the advice required by section 1786.40 "
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
        "punitive damages as authorized by section 1786.50(b). Best Buy's own "
        "October 17, 2023 disclosure publicly identified First Advantage by "
        "name, address, and telephone number the same day as the offer, "
        "supporting an inference that Best Buy was familiar with the identity "
        "of its investigative CRA and the California regulatory framework "
        "governing those reports.",
    ),
    ("HEADER", "THIRD CAUSE OF ACTION"),
    (
        "SUBHEAD",
        "Unauthorized Employment Use of Registry Information\n"
        "Cal. Penal Code section 290.46(j)(2)(E) and (j)(4)(A)\n"
        "Against Best Buy Co., Inc.",
    ),
    (
        "PARA",
        "72. Plaintiff realleges paragraphs 1 through 43 and 48 through 55. "
        "Plaintiff does not reallege paragraphs 44 through 47. This count is a "
        "liability created by statute. It is timely under Code of Civil "
        "Procedure section 338(a) from the on-or-about October 2023 employment "
        "use. Three years from October 17, 2023 is October 17, 2026.",
    ),
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
        "fact, that the First Advantage report furnished to Best Buy contained "
        "information disclosed pursuant to Penal Code section 290.46, "
        "including Plaintiff's California registry information.",
    ),
    (
        "PARA",
        "76. Plaintiff alleges, on information and belief and as an ultimate "
        "fact, that Best Buy received, accessed, considered, and used that "
        "section 290.46 information for a purpose relating to employment.",
    ),
    (
        "PARA",
        "77. Plaintiff alleges that the section 290.46 information was a "
        "substantial factor in Best Buy's decision to deny, withdraw, end, or "
        "prevent Plaintiff's Tracy employment. The factual basis is stated in "
        "paragraphs 17 through 35 and 48 through 55, including First "
        "Advantage's reporting of this same Plaintiff's California registry "
        "information in comparator employment screens, Best Buy's procurement "
        "of the intervening background check, the cessation of communication "
        "after that screen, and the absence of any communicated independent "
        "reason.",
    ),
    (
        "PARA",
        "78. The pleaded use was not authorized by section 290.46(j)(1), and "
        "Plaintiff is unaware of another law authorizing Best Buy to use "
        "information disclosed pursuant to section 290.46 for the Tracy "
        "warehouse position.",
    ),
    (
        "PARA",
        "79. Best Buy thereby violated section 290.46(j)(2)(E).",
    ),
    (
        "PARA",
        "80. Section 290.46(j)(4)(A) makes a prohibited user liable for the "
        "civil remedies specified in that subdivision. Plaintiff seeks actual "
        "damages, any additional amount authorized by the statute, exemplary "
        "relief to the extent proven and legally available, attorney's fees "
        "if counsel later appears and the statute authorizes recovery, and any "
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
        "82. As a direct result of the conduct alleged, Plaintiff lost the "
        "accepted Tracy warehouse employment and the compensation that "
        "employment would have provided at the offered rate of $22.60 per "
        "hour, according to proof.",
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
        "BEST BUY CO., INC. as follows:",
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
