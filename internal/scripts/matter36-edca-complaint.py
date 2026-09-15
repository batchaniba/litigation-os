#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Matter 36 — E.D. Cal. federal complaint review draft (AT&T).

REVIEW DRAFT. Not for filing until Plaintiff confirms Workday acceptance,
onboarding, nonreceipt, and signs. The September 8, 2026 San Joaquin packet
is historical work product; it was never clerk-filed.

May 29, 2026 is not pleaded. The offer, screening task, and rescission are
all May 28, 2026. No count needs a delayed-discovery date.

    python3 internal/scripts/matter36-edca-complaint.py
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
    / "internal/public/documents/matter-36"
    / "EDCA Complaint Review Draft - Ngwa Nforbi v ATT Mobility Services LLC"
    " (Sep 15 2026).pdf"
)

DOC_TITLE_FOOTER = (
    "COMPLAINT FOR DAMAGES -- NGWA NFORBI v. AT&T MOBILITY SERVICES LLC "
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
    ("AT&T MOBILITY SERVICES LLC,", True, False),
    ("a Delaware limited liability", True, False),
    ("company,", True, False),
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
    ("      section 290.46(j);", False, False),
    ("(4) Breach of Contract;", False, False),
    ("(5) Implied Covenant;", False, False),
    ("(6) Promissory Estoppel;", False, False),
    ("(7) Negligent", False, False),
    ("      Misrepresentation", False, False),
    ("", False, False),
    ("[DEMAND FOR JURY TRIAL]", True, False),
    ("", False, False),
    ("[REVIEW DRAFT -- NOT FOR", True, False),
    ("FILING UNTIL PLAINTIFF", True, False),
    ("SIGNS]", True, False),
]

CONTENT = [
    (
        "NOTICE",
        "REVIEW DRAFT -- NOT FOR FILING. Confirm Workday acceptance, "
        "onboarding, nonreceipt of the report and Summary of Rights, and "
        "have Plaintiff sign. No count uses a delayed-discovery date. The "
        "operative events are May 28, 2026. Serve AT&T's current California "
        "Secretary of State agent, not the Lodi store.",
    ),
    (
        "PARA",
        "Plaintiff BRENDAN NGWA NFORBI, appearing in propria persona, alleges "
        "against Defendant AT&T MOBILITY SERVICES LLC ('AT&T') as follows:",
    ),
    ("HEADER", "INTRODUCTION"),
    (
        "PARA",
        "1. On May 28, 2026, AT&T officially offered Plaintiff employment as "
        "a Retail Sales Consultant at 2439 West Kettleman Lane, Lodi, "
        "California, at $24.95 per hour, with a $13,700 annual targeted "
        "variable-compensation figure prorated for part-time hours and a "
        "tentative June 15, 2026 start date. Plaintiff accepted through "
        "Workday and began onboarding. Approximately two hours later, AT&T "
        "rescinded the offer.",
    ),
    (
        "PARA",
        "2. AT&T's written offer listed formal acceptance, required hiring "
        "documents, work authorization, any applicable export review, absence "
        "of restrictive agreements, any applicable rehire-eligibility check, "
        "and satisfactory standardized background checks as contingencies. It "
        "did not list Spanish proficiency or passage of the earlier language "
        "assessment as an offer contingency. That assessment was administered "
        "before the offer. Its testing window closed on May 25, 2026.",
    ),
    (
        "PARA",
        "3. At 10:13 a.m. on May 28, AT&T's Workday system told Plaintiff "
        "that AT&T was excited to officially offer him requisition R-106742. "
        "At 10:15, 10:16, and 10:17 a.m., AT&T issued offer-document, "
        "government-identifier, and personal-information tasks. At 10:19 a.m., "
        "First Advantage Background Services Corp. sent Plaintiff the "
        "screening task AT&T had ordered for 'AT&T Non Management,' client "
        "account 132156. First Advantage is not named as a defendant.",
    ),
    (
        "PARA",
        "4. At 12:23 p.m., AT&T recruiter Richard Patterson texted that the "
        "manager no longer wanted to proceed with 'your offer' because "
        "Plaintiff did not pass Spanish. That text is AT&T's stated reason. "
        "It is not a conceded true fact. Plaintiff does not admit that he "
        "failed the assessment, that the assessment was a lawful basis for "
        "reversing an official bilingual offer issued after the testing "
        "window closed, or that the stated reason was the actual reason.",
    ),
    (
        "PARA",
        "5. The chronology presents two competing explanations. AT&T's stated "
        "explanation is a language score completed before the offer. The "
        "competing explanation, pleaded on information and belief as an "
        "ultimate fact, is that information surfaced or was escalated during "
        "the intervening First Advantage screen and caused or substantially "
        "motivated the reversal. Alternative pleading is authorized. If "
        "discovery shows no consumer report was completed or transmitted "
        "before 12:23 p.m., the contract, estoppel, and misrepresentation "
        "counts still stand on the offer, acceptance, and reliance.",
    ),
    (
        "PARA",
        "6. Before the 12:23 p.m. rescission, AT&T did not provide Plaintiff "
        "a copy of any First Advantage report or a written Summary of Rights "
        "under 15 U.S.C. section 1681b(b)(3)(A). When it denied the "
        "employment, AT&T did not advise Plaintiff that an investigative "
        "consumer report had been obtained or supply First Advantage's name "
        "and address as required by Civil Code section 1786.40.",
    ),
    (
        "PARA",
        "7. Plaintiff alleges, on information and belief and as an ultimate "
        "fact, that First Advantage furnished AT&T information concerning "
        "Plaintiff disclosed pursuant to Penal Code section 290.46, including "
        "Plaintiff's California registry information, and that AT&T used that "
        "information for the purpose of deciding whether to honor the "
        "accepted Lodi offer. Plaintiff does not possess the AT&T First "
        "Advantage report and does not allege its source-field wording as "
        "known fact.",
    ),
    (
        "PARA",
        "8. The Lodi position is a retail-sales assignment, not a commercial "
        "motor-vehicle driving job. The FCRA driving exception in 15 U.S.C. "
        "section 1681b(b)(3)(B)-(C) does not apply.",
    ),
    ("HEADER", "JURISDICTION AND VENUE"),
    (
        "PARA",
        "9. This Court has original subject-matter jurisdiction under 28 U.S.C. "
        "section 1331 because Count One arises under the Fair Credit Reporting "
        "Act. Section 1681p authorizes an action in an appropriate United "
        "States district court without regard to the amount in controversy.",
    ),
    (
        "PARA",
        "10. This Court has supplemental jurisdiction over Counts Two through "
        "Seven under 28 U.S.C. section 1367(a) because those California claims "
        "arise from the same offer, screening, and rescission as the FCRA "
        "claim and form part of the same case or controversy.",
    ),
    (
        "PARA",
        "11. Plaintiff does not presently plead diversity jurisdiction. AT&T "
        "Mobility Services LLC is a limited liability company. Complete "
        "diversity would require the citizenship of every member. Those "
        "membership facts are not in Plaintiff's possession.",
    ),
    (
        "PARA",
        "12. Venue is proper in the Eastern District of California under "
        "28 U.S.C. section 1391(b)(2) because a substantial part of the events "
        "occurred in Lodi, San Joaquin County, California.",
    ),
    (
        "PARA",
        "12A. Plaintiff has Article III standing. His injury is concrete and "
        "particularized and is not a bare procedural violation. AT&T's conduct "
        "caused Plaintiff the loss of the accepted Lodi Retail Sales Consultant "
        "position and its compensation at $24.95 per hour, a tangible economic "
        "injury. Plaintiff also lost the pre-adverse review-and-response "
        "opportunity protected by 15 U.S.C. section 1681b(b)(3)(A). Had AT&T "
        "furnished the report and Summary of Rights before acting, Plaintiff "
        "could have identified and challenged any California-registry source "
        "before the employment decision became final. See TransUnion LLC v. "
        "Ramirez, 594 U.S. 413 (2021). These injuries are fairly traceable to "
        "the conduct alleged and redressable by the relief sought.",
    ),
    (
        "PARA",
        "13. Under Eastern District of California Local Rule 120(d), civil "
        "actions arising in San Joaquin County are commenced in the Sacramento "
        "Division.",
    ),
    ("HEADER", "PARTIES"),
    (
        "PARA",
        "14. Plaintiff BRENDAN NGWA NFORBI is a natural person and resident of "
        "San Joaquin County, California. He is also identified in records as "
        "Brendan Ngehsi Ngwanforbi. Those name variants refer to Plaintiff. "
        "AT&T candidate records used Brendan Ngwa Nforbi.",
    ),
    (
        "PARA",
        "15. Defendant AT&T MOBILITY SERVICES LLC is a Delaware limited "
        "liability company doing business in California, including at 2439 "
        "West Kettleman Lane, Lodi. On information and belief, it was the "
        "legal employer that offered requisition R-106742. The Lodi store is "
        "a worksite, not a separate legal entity. Plaintiff does not presently "
        "name AT&T Inc. merely as parent.",
    ),
    (
        "PARA",
        "16. Plaintiff will serve AT&T through its designated agent for "
        "service of process on the California Secretary of State record as of "
        "the date of service. Multiple AT&T entities use CSC Lawyers "
        "Incorporating Service. Plaintiff will confirm the current listing "
        "for AT&T Mobility Services LLC immediately before service. Service "
        "is not to be made at 2439 West Kettleman Lane merely because that is "
        "the worksite.",
    ),
    (
        "PARA",
        "17. First Advantage is the consumer reporting agency AT&T used for "
        "Plaintiff's screening. The May 28, 2026 task invitation named AT&T "
        "Non Management as the client, displayed account 132156, and "
        "referenced FCRA disclosure and authorization. Plaintiff does not "
        "presently name First Advantage as a defendant.",
    ),
    (
        "PARA",
        "18. Richard Patterson is an AT&T recruiter and percipient witness. "
        "Orville R. Bell is identified on the offer as the reporting manager "
        "and is also a witness. Neither is presently named as a defendant.",
    ),
    ("HEADER", "FACTUAL ALLEGATIONS"),
    ("SUBHEAD", "A. Two AT&T Applications"),
    (
        "PARA",
        "19. On May 16, 2026, Plaintiff applied for R-107776, Retail Sales "
        "Consultant, Stockton Pacific, 5756 Pacific Avenue #94, Stockton. "
        "That requisition was not identified as bilingual.",
    ),
    (
        "PARA",
        "20. The same day he applied for R-106742, Bilingual Spanish Retail "
        "Sales Consultant, Lodi, 2439 West Kettleman Lane.",
    ),
    (
        "PARA",
        "21. Both applications advanced through interviews. AT&T canceled and "
        "rescheduled both in-person interviews. The subsequent Spanish test "
        "and formal Lodi offer confirm that the Lodi candidacy remained "
        "active.",
    ),
    (
        "PARA",
        "22. AT&T's records contain the interview scorecards, manager notes, "
        "Virtual Job Tryout result, and disposition of both requisitions. "
        "Those records have not been provided to Plaintiff. The unexplained "
        "disposition of the non-bilingual Stockton requisition is relevant "
        "because a Spanish-proficiency issue cannot rationally disqualify "
        "Plaintiff from a position that did not require Spanish.",
    ),
    ("SUBHEAD", "B. The Spanish Assessment Preceded the Offer"),
    (
        "PARA",
        "23. On May 22, 2026, Language Testing International stated that AT&T "
        "Taleo had requested an ACTFL Telephone OPIc Spanish speaking test. "
        "The test expired at midnight on May 25, 2026. The rating was to be "
        "sent to AT&T Taleo.",
    ),
    (
        "PARA",
        "24. The LTI communication did not identify a passing threshold, did "
        "not state that Plaintiff had failed, did not provide a score, and "
        "did not disclose when AT&T received or reviewed any rating.",
    ),
    (
        "PARA",
        "25. By May 28, the assessment window had closed. AT&T nevertheless "
        "approved Plaintiff, generated the formal offer, and advanced him to "
        "onboarding and background screening.",
    ),
    ("SUBHEAD", "C. The Written Offer"),
    (
        "PARA",
        "26. On May 28, 2026 at 10:13 a.m., Workday sent 'Welcome to the "
        "team' and stated that AT&T was excited to officially offer Plaintiff "
        "R-106742 Bilingual Spanish Retail Sales Consultant.",
    ),
    (
        "PARA",
        "27. The formal written offer identified the position as Retail Sales "
        "Consultant, reporting to Orville R. Bell, at 2439 West Kettleman "
        "Lane; $24.95 per hour paid biweekly; annual targeted variable "
        "compensation of $13,700 prorated for part-time hours; and a "
        "tentative June 15, 2026 start date. Candidate application "
        "C-1690172.",
    ),
    (
        "PARA",
        "28. The offer stated that employment was contingent upon formal "
        "acceptance and required hiring documents, proof of identity and work "
        "authorization, any applicable deemed-export review, absence of "
        "restrictive agreements, any applicable rehire-eligibility check, and "
        "satisfactory standardized background checks. The two-page offer did "
        "not list Spanish proficiency, passage of the ACTFL assessment, "
        "at-will status, arbitration, a guaranteed weekly schedule, or an "
        "unrestricted pre-start withdrawal right.",
    ),
    (
        "PARA",
        "29. The offer did not tell Plaintiff that AT&T considered him "
        "disqualified for Spanish. It announced that AT&T had officially "
        "selected him for the expressly bilingual requisition after the "
        "assessment window had closed.",
    ),
    ("SUBHEAD", "D. Onboarding and the First Advantage Order"),
    (
        "PARA",
        "30. At 10:15, 10:16, and 10:17 a.m., Workday assigned Review "
        "Documents, Change Government Identifiers, and Change Personal "
        "Information tasks for R-106742 / C-1690172.",
    ),
    (
        "PARA",
        "31. At 10:19 a.m., First Advantage stated that AT&T Non Management "
        "had contracted with it and assigned Plaintiff a task. It directed "
        "him to a secure site, referenced FCRA disclosure and authorization, "
        "and described possible ID.me identity verification. Client account "
        "132156.",
    ),
    (
        "PARA",
        "32. The 10:19 communication establishes that AT&T placed a screening "
        "order with First Advantage. Defendants' systems will show the order "
        "time, package, searches, completion status, results, adjudication, "
        "access, and cancellation history.",
    ),
    (
        "PARA",
        "33. Plaintiff accepted the offer through Workday, timely undertook "
        "the mandatory onboarding and screening steps presented to him, "
        "furnished personal information for that purpose, and remained ready, "
        "willing, and able to begin on June 15.",
    ),
    ("SUBHEAD", "E. The 12:23 p.m. Rescission"),
    (
        "PARA",
        "34. At 12:23 p.m., Patterson texted: 'Hi Brendan. Unfortunately, the "
        "manager advised me that he no longer wants to move forward with your "
        "offer. He stated that he need a Spanish speaker and you did not pass "
        "the Spanish assessment. Sorry for the inconvenience.'",
    ),
    (
        "PARA",
        "35. Plaintiff replied: 'No worries sir, thank you for the "
        "opportunity.' That response did not release any claim, waive any "
        "right, or admit that the explanation was accurate.",
    ),
    (
        "PARA",
        "36. The text's reference to 'your offer' and 'no longer' corroborates "
        "a reversal of an approved decision. The text did not provide the "
        "score, test date, passing standard, or the identity of the actual "
        "decisionmaker.",
    ),
    (
        "PARA",
        "37. Before 12:23 p.m., AT&T did not provide a copy of any First "
        "Advantage report or a written description of FCRA rights.",
    ),
    (
        "PARA",
        "38. When AT&T denied the employment, it did not advise Plaintiff "
        "that an investigative consumer report had been obtained and did not "
        "supply First Advantage's name and address. The 10:19 task invitation "
        "preceded any report and is not the Civil Code section 1786.40 advice "
        "due at adverse action.",
    ),
    (
        "PARA",
        "39. The FCRA defines adverse action in the employment context to "
        "include a denial of employment. The 12:23 p.m. rescission was an "
        "adverse action.",
    ),
    (
        "SUBHEAD",
        "F. Screening Inference, Comparators, and Pretext",
    ),
    (
        "PARA",
        "40. The Spanish assessment necessarily preceded the May 28 offer "
        "because the test expired on May 25. AT&T's systems were capable of "
        "preventing an offer if a mandatory qualification had already been "
        "finally failed. AT&T instead issued a specific offer and three "
        "onboarding tasks. The first and only failure assertion in the "
        "current record is Patterson's secondhand text after screening began.",
    ),
    (
        "PARA",
        "41. Plaintiff alleges that the AT&T First Advantage report contained "
        "information disclosed pursuant to Penal Code section 290.46, "
        "including Plaintiff's California sex-offender-registry information. "
        "That allegation is made on information and belief because the report "
        "and source fields are within AT&T's and First Advantage's control.",
    ),
    (
        "PARA",
        "42. At the time of AT&T's screening, Plaintiff was publicly listed "
        "on California's Megan's Law website. Plaintiff's identity and "
        "underlying California registry entry were the same regardless of "
        "which employer requested a First Advantage employment screen.",
    ),
    (
        "PARA",
        "43. Plaintiff possesses a First Advantage employment background "
        "report concerning himself generated for United Parcel Service. In "
        "that report, ordinary criminal-search components returned "
        "non-adverse results, while the sex-offender-registry component was "
        "the adverse or decisional component and expressly identified the "
        "source of record as the California Sex Offender Registry.",
    ),
    (
        "PARA",
        "44. In a separate First Advantage employment screening for Federal "
        "Express Corporation, FedEx later admitted in its responsive pleading "
        "that the report identified Plaintiff as a California registrant.",
    ),
    (
        "PARA",
        "45. Plaintiff does not allege that UPS's or FedEx's report is AT&T's "
        "report. He alleges those comparator records because they concern the "
        "same consumer, the same CRA, the same underlying California registry "
        "entry, and the same type of employment background screening.",
    ),
    (
        "PARA",
        "46. On information and belief, between 10:19 a.m. and 12:23 p.m. on "
        "May 28, 2026, First Advantage's screening system returned, flagged, "
        "transmitted, displayed, or escalated Plaintiff's California registry "
        "information, or informed AT&T that the screening would produce an "
        "adverse result, and AT&T used that information in reversing the "
        "offer. The precise timestamps, access logs, and reason codes are in "
        "Defendants' possession.",
    ),
    (
        "PARA",
        "47. If production later shows that no report was completed or "
        "accessed before 12:23 p.m., Counts One through Three will stand or "
        "fall on that record after production. Counts Four through Seven do "
        "not depend on that inference.",
    ),
    ("SUBHEAD", "G. Reliance and Harm"),
    (
        "PARA",
        "48. AT&T intended the offer and onboarding communications to induce "
        "Plaintiff to accept, complete mandatory tasks, disclose identifying "
        "information, prepare for June 15, and treat the Lodi position as "
        "no longer available to pursue elsewhere.",
    ),
    (
        "PARA",
        "49. Plaintiff reasonably understood 'officially offer,' the specified "
        "compensation, start date, and immediate onboarding sequence to mean "
        "AT&T had approved him subject to the written contingencies being "
        "administered lawfully and in good faith.",
    ),
    (
        "PARA",
        "50. Plaintiff lost the offered Lodi employment, including the "
        "opportunity to earn $24.95 per hour and targeted variable "
        "compensation beginning on or about June 15, according to proof. The "
        "offer does not state weekly hours. Plaintiff does not invent them. "
        "He does not claim a guaranteed lifetime expectancy from prospective "
        "employment.",
    ),
    (
        "PARA",
        "51. Had AT&T furnished the report and Summary of Rights before the "
        "rescission, Plaintiff would have been able to identify any "
        "California-registry source and advise AT&T that Penal Code section "
        "290.46(j)(2)(E) prohibited using that information for this "
        "employment purpose.",
    ),
    ("HEADER", "FIRST CAUSE OF ACTION"),
    (
        "SUBHEAD",
        "Fair Credit Reporting Act -- 15 U.S.C. section 1681b(b)(3)(A)\n"
        "Against AT&T Mobility Services LLC",
    ),
    ("PARA", "52. Plaintiff realleges paragraphs 1 through 51."),
    (
        "PARA",
        "53. Plaintiff was a 'consumer,' the First Advantage report was a "
        "'consumer report,' AT&T procured or caused it to be procured for "
        "'employment purposes,' and AT&T was a 'person' using the report "
        "within the meaning of the FCRA.",
    ),
    (
        "PARA",
        "54. Under 15 U.S.C. section 1681b(b)(3)(A), before taking adverse "
        "action based in whole or in part on an employment consumer report, "
        "the person intending to take the adverse action must provide the "
        "consumer (i) a copy of the report and (ii) a written description of "
        "the consumer's rights under the FCRA.",
    ),
    (
        "PARA",
        "55. On information and belief, AT&T's rescission was based in whole "
        "or in part on the First Advantage report or screening process.",
    ),
    (
        "PARA",
        "56. AT&T did not provide the report or the written Summary of Rights "
        "before the 12:23 p.m. adverse action.",
    ),
    (
        "PARA",
        "57. AT&T therefore violated section 1681b(b)(3)(A). This count is "
        "timely under 15 U.S.C. section 1681p. The violation occurred on May "
        "28, 2026. This count does not plead a delayed-discovery date.",
    ),
    (
        "PARA",
        "58. AT&T's noncompliance was negligent within the meaning of "
        "15 U.S.C. section 1681o and, on proof, willful within the meaning of "
        "section 1681n. Willfulness includes reckless disregard of the FCRA's "
        "requirements. See Safeco Ins. Co. of America v. Burr, 551 U.S. 47 "
        "(2007). AT&T's own First Advantage workflow referenced FCRA disclosure "
        "and authorization immediately before the alleged adverse action, "
        "supporting an inference that AT&T knew it was administering an "
        "employment consumer-report process. Plaintiff pleads negligence and "
        "willfulness in the alternative and does not presently assert a "
        "section 1681b(b)(2)(A) claim.",
    ),
    (
        "PARA",
        "59. As a direct result, Plaintiff lost the accepted Lodi employment "
        "and the statutory opportunity to review and respond to the report "
        "before the decision. If willfulness is proven, Plaintiff also seeks "
        "statutory and punitive damages authorized by section 1681n.",
    ),
    ("HEADER", "SECOND CAUSE OF ACTION"),
    (
        "SUBHEAD",
        "California Investigative Consumer Reporting Agencies Act\n"
        "Cal. Civ. Code sections 1786.40, 1786.50\n"
        "Against AT&T Mobility Services LLC",
    ),
    ("PARA", "60. Plaintiff realleges paragraphs 1 through 51."),
    (
        "PARA",
        "61. The First Advantage employment background report was an "
        "investigative consumer report within ICRAA.",
    ),
    (
        "PARA",
        "62. Civil Code section 1786.40(a) required AT&T, when employment was "
        "denied under circumstances in which an investigative consumer report "
        "had been obtained, to advise Plaintiff and supply the investigative "
        "consumer reporting agency's name and address.",
    ),
    (
        "PARA",
        "63. AT&T denied the employment under circumstances in which it had "
        "obtained the First Advantage investigative consumer report. It did "
        "not provide the section 1786.40 advice at the time of the "
        "rescission.",
    ),
    (
        "PARA",
        "64. This section 1786.40 omission is pleaded as a separate act or "
        "omission from the pre-adverse FCRA violation in Count One. This "
        "count is timely under Civil Code section 1786.52. It does not plead "
        "a delayed-discovery date.",
    ),
    (
        "PARA",
        "65. Under Civil Code section 1786.50, Plaintiff seeks actual damages "
        "or $10,000, whichever is greater, together with costs and any "
        "attorney's fees recoverable if counsel later appears, and punitive "
        "damages if the violation is proven grossly negligent or willful.",
    ),
    ("HEADER", "THIRD CAUSE OF ACTION"),
    (
        "SUBHEAD",
        "Unauthorized Employment Use of Registry Information\n"
        "Cal. Penal Code section 290.46(j)(2)(E) and (j)(4)(A)\n"
        "Against AT&T Mobility Services LLC",
    ),
    (
        "PARA",
        "66. Plaintiff realleges paragraphs 1 through 51. This count is a "
        "liability created by statute. It is timely under Code of Civil "
        "Procedure section 338(a) from the May 28, 2026 employment use. Three "
        "years from May 28, 2026 is May 28, 2029. This count does not plead a "
        "delayed-discovery date.",
    ),
    (
        "PARA",
        "67. Penal Code section 290.46(j)(2)(E) prohibits use of information "
        "disclosed pursuant to section 290.46 for purposes relating to "
        "employment except as authorized by paragraph (1) or another "
        "provision of law.",
    ),
    (
        "PARA",
        "68. Plaintiff alleges, on information and belief and as an ultimate "
        "fact, that the First Advantage report furnished to AT&T contained "
        "Plaintiff's information disclosed pursuant to Penal Code section "
        "290.46, and that AT&T received, accessed, considered, and used that "
        "information for a purpose relating to employment.",
    ),
    (
        "PARA",
        "69. Plaintiff alleges that the registry information was a substantial "
        "factor in AT&T's decision to rescind the accepted offer. The factual "
        "basis includes the two-hour sequence after the First Advantage "
        "order, the already-closed Spanish-assessment window, the official "
        "offer that did not list Spanish as a contingency, Plaintiff's "
        "contemporaneous California registry listing, First Advantage's "
        "demonstrated reporting of that same California registry information "
        "in other employment screens of Plaintiff, and the absence of any "
        "primary language-score document in the communications to Plaintiff.",
    ),
    (
        "PARA",
        "70. The pleaded use was not authorized by section 290.46(j)(1), and "
        "Plaintiff is unaware of another law authorizing AT&T to use "
        "information disclosed pursuant to section 290.46 for this "
        "retail-sales hiring decision.",
    ),
    (
        "PARA",
        "71. AT&T thereby violated section 290.46(j)(2)(E). Plaintiff seeks "
        "the civil remedies authorized by section 290.46(j)(4)(A), without "
        "duplicative recovery. Plaintiff does not presently seek preventive "
        "relief under section 290.46(j)(4)(B).",
    ),
    ("HEADER", "FOURTH CAUSE OF ACTION"),
    (
        "SUBHEAD",
        "Breach of Contract\nAgainst AT&T Mobility Services LLC",
    ),
    (
        "PARA",
        "72. Plaintiff realleges paragraphs 1 through 51, except allegations "
        "that no contract formed.",
    ),
    (
        "PARA",
        "73. AT&T made a written offer containing the material position, "
        "compensation, start-date, acceptance, and contingency terms. "
        "Plaintiff timely accepted it through Workday.",
    ),
    (
        "PARA",
        "74. The accepted offer formed an agreement for employment subject to "
        "the stated pre-employment conditions administered lawfully and in "
        "good faith.",
    ),
    (
        "PARA",
        "75. Plaintiff performed, commenced performance, or was excused from "
        "further performance because AT&T repudiated the agreement two hours "
        "later and prevented completion of the remaining conditions. "
        "Plaintiff remained ready, willing, and able to perform.",
    ),
    (
        "PARA",
        "76. AT&T breached by rescinding the accepted offer based on a reason "
        "it had already evaluated or waived before contracting, by preventing "
        "satisfaction of conditions, and/or by using an unlawful screening "
        "criterion. AT&T may not rely on failure of a condition that it "
        "wrongfully caused, prevented, waived, or applied in violation of law.",
    ),
    (
        "PARA",
        "77. Any at-will character of prospective employment limits but does "
        "not erase damages caused before Plaintiff received a good-faith "
        "opportunity to begin. Plaintiff seeks those damages according to "
        "proof, without double recovery.",
    ),
    ("HEADER", "FIFTH CAUSE OF ACTION"),
    (
        "SUBHEAD",
        "Breach of the Implied Covenant of Good Faith and Fair Dealing\n"
        "Against AT&T Mobility Services LLC",
    ),
    ("PARA", "78. Plaintiff realleges paragraphs 72 through 77."),
    (
        "PARA",
        "79. Every contract contains an implied covenant that neither party "
        "will unfairly frustrate the other's right to receive the agreement's "
        "benefits. The accepted offer gave AT&T discretion to evaluate "
        "standardized background checks. That discretion had to be exercised "
        "honestly, in good faith, for authorized purposes, and consistently "
        "with the parties' justified expectations.",
    ),
    (
        "PARA",
        "80. AT&T frustrated the agreement by issuing and inducing acceptance "
        "of an offer after the language-assessment period, commencing "
        "onboarding, and then invoking that preexisting assessment only after "
        "screening began. Alternatively, AT&T exercised screening discretion "
        "in bad faith by considering a prohibited registry source.",
    ),
    (
        "PARA",
        "81. Plaintiff suffered the losses alleged in paragraphs 50 and 77.",
    ),
    ("HEADER", "SIXTH CAUSE OF ACTION"),
    (
        "SUBHEAD",
        "Promissory Estoppel\n"
        "Against AT&T Mobility Services LLC\n"
        "(Alternative if no contract formed)",
    ),
    (
        "PARA",
        "82. Plaintiff realleges paragraphs 1 through 51 except allegations "
        "requiring an enforceable contract.",
    ),
    (
        "PARA",
        "83. AT&T made a clear promise by stating that it was excited to "
        "officially offer Plaintiff the identified Lodi position and by "
        "providing specific compensation, a tentative start date, and "
        "immediate onboarding tasks.",
    ),
    (
        "PARA",
        "84. AT&T reasonably expected that promise to induce acceptance, "
        "disclosure of sensitive information, completion of screening, and "
        "preparation for work. Plaintiff reasonably relied because the offer "
        "followed completion of AT&T's interview and assessment stages and "
        "was communicated as official.",
    ),
    (
        "PARA",
        "85. Plaintiff changed position as alleged in paragraphs 33 and 48 "
        "through 50. AT&T withdrew the promise before giving him a good-faith "
        "opportunity to begin. Injustice can be avoided only by enforcing the "
        "promise to the extent justice requires or awarding reliance damages. "
        "Plaintiff seeks reliance losses, not a speculative guarantee of "
        "indefinite employment.",
    ),
    ("HEADER", "SEVENTH CAUSE OF ACTION"),
    (
        "SUBHEAD",
        "Negligent Misrepresentation\n"
        "Against AT&T Mobility Services LLC\n"
        "(Pleaded in the alternative)",
    ),
    (
        "PARA",
        "86. Plaintiff realleges paragraphs 1 through 51 except allegations "
        "of intentional falsity.",
    ),
    (
        "PARA",
        "87. AT&T represented at 10:13 a.m. that it had officially offered "
        "Plaintiff R-106742 and then represented through onboarding tasks "
        "that the approved offer process was proceeding.",
    ),
    (
        "PARA",
        "88. If AT&T had already received and treated the Spanish result as "
        "finally disqualifying, that representation was false or misleading "
        "when made. If AT&T had not obtained managerial approval or knew its "
        "workflow would automatically reverse the offer, it lacked reasonable "
        "grounds for believing the representation true.",
    ),
    (
        "PARA",
        "89. AT&T made the representation to induce Plaintiff to accept, "
        "undertake onboarding and screening, disclose personal information, "
        "and prepare to begin work. Plaintiff's reliance was reasonable. "
        "AT&T's failure to use reasonable care in communicating an approved "
        "offer after the assessment period was a substantial factor in the "
        "harm alleged in paragraph 50.",
    ),
    (
        "PARA",
        "90. Plaintiff does not presently plead intentional fraud or "
        "concealment. He reserves leave to amend if internal records later "
        "support that showing under Rule 9(b).",
    ),
    ("HEADER", "DAMAGES"),
    (
        "PARA",
        "91. Plaintiff seeks only nonduplicative recovery. Where multiple "
        "theories provide remedies for the same injury, Plaintiff will elect "
        "or apportion as required to prevent double recovery.",
    ),
    ("HEADER", "PRAYER FOR RELIEF"),
    (
        "PARA",
        "WHEREFORE, Plaintiff respectfully requests judgment against Defendant "
        "AT&T MOBILITY SERVICES LLC as follows:",
    ),
    (
        "LIST_ITEM",
        "A. Actual, reliance, compensatory, and consequential damages "
        "according to proof, including lost employment compensation at the "
        "offered rate of $24.95 per hour;",
    ),
    (
        "LIST_ITEM",
        "B. The remedies authorized by 15 U.S.C. sections 1681n and 1681o, "
        "including statutory and punitive damages if willfulness is proven;",
    ),
    (
        "LIST_ITEM",
        "C. The remedies authorized by California Civil Code section 1786.50, "
        "including actual damages or $10,000, whichever is greater;",
    ),
    (
        "LIST_ITEM",
        "D. The remedies authorized by California Penal Code section "
        "290.46(j)(4)(A), without duplicative recovery;",
    ),
    (
        "LIST_ITEM",
        "E. Contract and promissory-estoppel reliance damages according to "
        "proof;",
    ),
    (
        "LIST_ITEM",
        "F. Taxable costs and attorney's fees only to the extent authorized "
        "and recoverable, including if counsel later appears;",
    ),
    (
        "LIST_ITEM",
        "G. Prejudgment and post-judgment interest as allowed by law; and",
    ),
    (
        "LIST_ITEM",
        "H. Such other and further relief as the Court deems just and proper.",
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


def dump_markdown(path: Path) -> None:
    lines = [
        "# Matter 36 — E.D. Cal. complaint review draft",
        "",
        "Generated from `internal/scripts/matter36-edca-complaint.py`. "
        "REVIEW DRAFT. Not for filing until Plaintiff confirms Workday "
        "acceptance, onboarding, nonreceipt, and signs.",
        "",
        "May 29, 2026 is **not** pleaded. The offer, First Advantage task, "
        "and rescission are all May 28, 2026.",
        "",
        "---",
        "",
        "## Caption",
        "",
        "BRENDAN NGWA NFORBI, Plaintiff, in propria persona, v. AT&T MOBILITY "
        "SERVICES LLC, a Delaware limited liability company.",
        "",
        "United States District Court, Eastern District of California — "
        "Sacramento Division. Unverified. Demand for jury trial.",
        "",
    ]
    for kind, text in CONTENT:
        if kind == "NOTICE":
            lines.extend([f"> **{text}**", ""])
        elif kind == "HEADER":
            lines.extend([f"## {text}", ""])
        elif kind == "SUBHEAD":
            heading = " / ".join(part.strip() for part in text.split("\n") if part.strip())
            lines.extend([f"### {heading}", ""])
        elif kind == "PARA":
            lines.extend([text, ""])
        elif kind == "LIST_ITEM":
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
        md_out = (
            ROOT
            / "internal/docs/matter-36"
            / "EDCA_FEDERAL_COMPLAINT_REVIEW_DRAFT.md"
        )
        dump_markdown(md_out)
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
