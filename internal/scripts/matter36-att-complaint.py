#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Matter 36 — review draft of verified complaint for AT&T offer rescission.

The default output is deliberately unsigned because the requested execution date
(September 8, 2026) is in the future. On or after that date, rerun with
``--execute`` only after Plaintiff confirms every allegation, especially the
acceptance/reliance allegations identified in the preflight report.
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
    / "internal/public/documents/matter-36"
    / "Verified Complaint - Ngwa Nforbi v AT&T Mobility Services LLC"
    " (Sep 8 2026).pdf"
)
DEFAULT_EXEC_DATE = "September 8, 2026"
EARLIEST_EXECUTION_DATE = dt.date(2026, 9, 8)
COURT_LINE2 = "COUNTY OF SAN JOAQUIN"
FOOTER = "VERIFIED COMPLAINT -- BRENDAN NGWA NFORBI v. AT&T MOBILITY SERVICES LLC"

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
    ("company; and DOES 1 through 20,", True, False),
    ("inclusive,", True, False),
    ("", False, False),
    ("                          Defendants.", False, False),
]

CAPTION_RIGHT = [
    ("Case No. _________________", False, False),
    ("", False, False),
    ("VERIFIED COMPLAINT FOR", True, False),
    ("DAMAGES, RESTITUTION,", True, False),
    ("DECLARATORY AND", True, False),
    ("INJUNCTIVE RELIEF", True, False),
    ("", False, False),
    ("(1) Penal Code § 290.46(j);", False, False),
    ("(2) FCRA, 15 U.S.C.", False, False),
    ("      § 1681b(b)(3)(A);", False, False),
    ("(3) ICRAA, Civ. Code", False, False),
    ("      §§ 1786.40, 1786.50;", False, False),
    ("(4) Breach of Contract;", False, False),
    ("(5) Breach of Implied Covenant;", False, False),
    ("(6) Promissory Estoppel;", False, False),
    ("(7) Negligent Misrepresentation;", False, False),
    ("(8) Fraud / Concealment;", False, False),
    ("(9) UCL, B&P Code § 17200", False, False),
    ("", False, False),
    ("[Unlimited Civil]", False, True),
    ("[Jury Trial Demanded]", False, True),
]

SIGNOFF_NAME = "BRENDAN NGWA NFORBI"
SIGNOFF_ROLE = "Plaintiff, In Propria Persona"
SIG_LINE = "___________________________________"

# Paragraphs 55, 83, 104, 118, 132, 145, and 160 depend materially on facts
# Plaintiff must personally confirm before execution.
CONTENT = [
    ("NOTICE", "REVIEW DRAFT — DO NOT FILE OR SIGN BEFORE SEPTEMBER 8, 2026. "
               "PLAINTIFF MUST CONFIRM THE ACCEPTANCE, ONBOARDING, RELIANCE, "
               "DAMAGES, AND NONRECEIPT ALLEGATIONS BEFORE EXECUTION."),
    ("PARA", 'Plaintiff BRENDAN NGWA NFORBI ("Plaintiff") alleges as follows:'),
    ("HEADER", "I.\nINTRODUCTION"),
    ("PARA", "1. On May 28, 2026, Defendant AT&T Mobility Services LLC approved Plaintiff for employment as a Retail Sales Consultant at its Lodi, California store, sent him a written offer identifying compensation of $24.95 per hour, part-time targeted variable compensation, and a tentative June 15, 2026 start date, and commenced its formal onboarding process."),
    ("PARA", "2. AT&T's written offer listed formal acceptance, required hiring documents, work authorization, any applicable export review, absence of restrictive agreements, any applicable rehire-eligibility check, and satisfactory standardized background checks as contingencies. It did not list Spanish proficiency or passage of the earlier language assessment as an offer contingency. The assessment AT&T later invoked was administered before the offer, and its testing window closed on May 25, 2026."),
    ("PARA", "3. At 10:13 a.m. on May 28, AT&T's Workday system told Plaintiff that AT&T was 'excited to officially offer' him requisition R-106742. At 10:15, 10:16, and 10:17 a.m., AT&T issued offer-document, government-identifier, and personal-information tasks. At 10:19 a.m., First Advantage Background Services Corp. sent Plaintiff the screening task AT&T had ordered. First Advantage is not named as a defendant."),
    ("PARA", "4. At 12:23 p.m.—approximately two hours after AT&T issued the offer and immediately after the hiring process entered background screening—AT&T recruiter Richard Patterson told Plaintiff that the manager no longer wanted to proceed with 'your offer.' Patterson attributed the reversal to a supposedly failed Spanish assessment."),
    ("PARA", "5. That chronology presents two competing explanations. AT&T's stated explanation is that Plaintiff failed an assessment completed before the offer. The competing and more plausible explanation, pleaded on information and belief, is that information surfaced or was escalated during the intervening background-screening process and caused or substantially motivated AT&T to reverse an already-approved hiring decision."),
    ("PARA", "6. Plaintiff does not allege registry use merely because he is registered. The inference rests on the sequence, the absence of any primary Spanish score in AT&T's communications, AT&T's decision to issue the offer after the assessment window closed, the immediate screening order, the abrupt reversal, the absence of required background-based adverse-action notices, and First Advantage's documented prior matching of this same Plaintiff to the California Sex Offender Registry for another employer."),
    ("PARA", "7. In July 2024, First Advantage prepared an employment report on Plaintiff for United Parcel Service. That report—later filed in federal court by UPS—identified a 'National Sex Offender Registry' and 'Department Of Justice Web Site' search as decisional, stated 'SOURCE OF RECORD: CALIFORNIA SEX OFFENDER REGISTRY,' and produced an overall 'INELIGIBLE' result. First Advantage therefore had previously identified Plaintiff through the same prohibited registry source and had the capability, identifiers, and matching methodology to do so again."),
    ("PARA", "8. The contents, completion time, transmission time, access log, adjudication status, and cancellation history of the May 28 AT&T screening are exclusively within Defendants' possession. Plaintiff does not attach an AT&T First Advantage report because he does not have one. He does not allege the contents of that report as a known fact. Code of Civil Procedure section 425.10 requires a statement of the facts constituting the cause of action in ordinary and concise language. Section 452 requires this Court to construe the pleading liberally with a view to substantial justice between the parties. Facts exclusively in Defendants' possession are properly pleaded on information and belief. Plaintiff states the facts supporting that belief and will seek the report in discovery."),
    ("PARA", "9. In the alternative, if Defendants establish that no consumer report was completed or transmitted before 12:23 p.m., AT&T remains answerable under the independent offer, contract, estoppel, and misrepresentation theories pleaded below to the extent established by the offer, acceptance, reliance, and internal approval records."),
    ("PARA", "10. Plaintiff pleads alternative and inconsistent theories because Defendants exclusively control the evidence that will determine whether the offer was reversed because of registry information, another consumer-report item, a preexisting language score, a manager's undisclosed reconsideration, or an automated workflow failure. Each theory is pleaded separately and does not depend upon success of every other theory."),
    ("HEADER", "II.\nPARTIES"),
    ("PARA", "11. Plaintiff BRENDAN NGWA NFORBI is a natural person residing in Stockton, San Joaquin County, California. Plaintiff applied for, received an offer for, and was denied employment in San Joaquin County."),
    ("PARA", "12. Plaintiff is the person identified in AT&T candidate records as Brendan Ngwa Nforbi and in other records as Brendan Ngehsi Ngwanforbi. Those name variants refer to Plaintiff."),
    ("PARA", "13. Plaintiff is required to register under California Penal Code section 290, and information identifying him appeared on California's Megan's Law website and California Sex Offender Registry at the time of the events alleged."),
    ("PARA", "14. Defendant AT&T MOBILITY SERVICES LLC ('AT&T') is a Delaware limited liability company doing business throughout California, including at the AT&T retail store located at 2439 West Kettleman Lane, Lodi, California 95242."),
    ("PARA", "15. AT&T Mobility Services LLC is identified in publicly available AT&T/CWA labor materials as the employer of covered mobility retail employees, and the Lodi position was designated within AT&T's Mobility bargaining structure. On information and belief, AT&T owned, operated, staffed, controlled, and made hiring decisions for the Lodi store and was the legal employer offering Plaintiff requisition R-106742."),
    ("PARA", "16. If discovery establishes that another AT&T subsidiary was the employing or decisionmaking entity, Plaintiff has sued DOES 1 through 5 for that purpose and will amend to substitute the correct entity. Plaintiff does not presently name AT&T Inc., the holding company, merely because it owns affiliated entities."),
    ("PARA", "17. First Advantage Background Services Corp. ('First Advantage') is a Florida corporation that provides employment background reports and screening services. It is not named as a defendant. Plaintiff reserves DOES 6 through 10 for any furnishing affiliate if later amendment is warranted."),
    ("PARA", "18. First Advantage is a 'consumer reporting agency' under 15 U.S.C. section 1681a(f) and an 'investigative consumer reporting agency' under Civil Code section 1786.2(d) when it assembles or evaluates information concerning consumers for employment reports."),
    ("PARA", "19. On May 28, 2026, First Advantage identified 'AT&T Non Management' as its client and sent Plaintiff a secure-site task relating to disclosure, authorization, identity verification, and employment screening. The email displayed AT&T client account number 132156."),
    ("PARA", "20. Plaintiff is informed and believes that First Advantage was the legal screening entity responsible for the May 28 order. Plaintiff will seek its file under Civil Code sections 1786.10 and 1786.22 and, if necessary, by subpoena. He does not name First Advantage as a defendant."),
    ("PARA", "21. Defendant RICHARD PATTERSON is not presently named as a defendant. He is an AT&T recruiter and percipient witness whose AT&T email address, recruiting communications, offer signature, and May 28 text identify him as the person who issued the offer and communicated the manager's decision. The formal offer identifies Orville R. Bell (ob3824) as Plaintiff's reporting manager. Bell is also a percipient witness and is not presently named individually."),
    ("PARA", "22. The true names and capacities of DOES 1 through 20 are unknown to Plaintiff, who therefore sues them by fictitious names under Code of Civil Procedure section 474. Plaintiff will amend this Complaint when their identities and roles are ascertained."),
    ("PARA", "23. Plaintiff is informed and believes that each DOE Defendant participated in, authorized, directed, furnished information for, implemented, concealed, or ratified one or more acts alleged and is legally responsible for the resulting harm."),
    ("HEADER", "III.\nJURISDICTION AND VENUE"),
    ("PARA", "24. This Court has subject-matter jurisdiction under article VI, section 10 of the California Constitution and Code of Civil Procedure section 410.10. It has concurrent jurisdiction over Plaintiff's federal FCRA claim."),
    ("PARA", "25. This action is properly designated unlimited civil because the aggregate relief sought exceeds $35,000, exclusive of interest and costs, including statutory, actual, consequential, exemplary, and equitable relief according to proof. No specific personal-injury or punitive-damages amount is pleaded."),
    ("PARA", "26. This Court has personal jurisdiction over AT&T because AT&T operates the Lodi store, recruited Plaintiff for work in this County, sent the offer into this County, and made or implemented the challenged hiring decision in California."),
    ("PARA", "27. First Advantage is not named as a defendant. Plaintiff will obtain its AT&T screening file by statutory inspection and, if necessary, by subpoena. DOES 6 through 10 remain reserved for any furnishing affiliate."),
    ("PARA", "28. Venue is proper in San Joaquin County under Code of Civil Procedure sections 395 and 395.5 because Plaintiff resides here, the offered workplace is in Lodi, the offer and rescission were received here, and the obligations, liability, and injury arose here."),
    ("PARA", "29. Plaintiff files this action in the Superior Court of California, County of San Joaquin. The FCRA count creates a federal question and may permit removal. It is pleaded because it is an independent statutory protection implicated if AT&T based its decision in whole or in part on a consumer report. It is not pleaded to manufacture federal jurisdiction, and it is not required for the Penal Code, ICRAA, contract, estoppel, or UCL counts."),
    ("HEADER", "IV.\nCOMMON FACTUAL ALLEGATIONS"),
    ("SUBHEAD", "A. Two AT&T Applications Advance in Parallel"),
    ("PARA", "30. On May 16, 2026 at approximately 1:15 p.m., Plaintiff applied for AT&T requisition R-107776, Retail Sales Consultant—Stockton Pacific, located at 5756 Pacific Avenue #94, Stockton, California."),
    ("PARA", "31. Workday confirmed receipt, and Modern Hire immediately invited Plaintiff to a Virtual Job Tryout and an in-person interview. The Stockton position was not identified as bilingual."),
    ("PARA", "32. On May 16 at approximately 2:31 p.m., Plaintiff applied for AT&T requisition R-106742, Bilingual Spanish Retail Sales Consultant—Lodi, located at 2439 West Kettleman Lane."),
    ("PARA", "33. Workday confirmed receipt of the Lodi application. AT&T recruiter Patterson immediately invited Plaintiff to schedule an interview."),
    ("PARA", "34. The Stockton interview was initially scheduled for May 19 at 4:45 p.m. AT&T canceled it at 3:46 p.m., 59 minutes before the appointment, and simultaneously rescheduled it for May 22 at 10:30 a.m."),
    ("PARA", "35. The Lodi interview was initially scheduled for May 20 at 2:00 p.m. AT&T canceled it at 1:51 p.m., nine minutes before the appointment, and simultaneously rescheduled it for May 21 at 2:00 p.m."),
    ("PARA", "36. AT&T sent reminders for the rescheduled interviews. The subsequent Spanish test and formal Lodi offer confirm that Plaintiff's Lodi candidacy remained active and advanced beyond initial screening."),
    ("PARA", "37. AT&T's records contain the attendance logs, interview scorecards, manager notes, Virtual Job Tryout result, and ultimate disposition of both requisitions. Those records have not been provided to Plaintiff."),
    ("SUBHEAD", "B. AT&T Requests the Spanish Assessment Before Issuing the Offer"),
    ("PARA", "38. On May 22 at 11:11 a.m., AT&T's language-testing provider told Plaintiff he had reached the next step for Bilingual Spanish Retail Sales Consultant position code 16000025 and must complete a pre-employment assessment within five days for an 'upcoming start date.'"),
    ("PARA", "39. At 11:37 a.m., Language Testing International ('LTI') stated that AT&T Taleo had requested an ACTFL Telephone OPIc Spanish speaking-proficiency test. It provided a telephone number and test access code and stated that the rating would be sent to AT&T Taleo."),
    ("PARA", "40. The test instructions required 30 to 40 minutes of spoken Spanish and stated that the test would expire at midnight on May 25, 2026."),
    ("PARA", "41. The LTI communication did not identify a passing threshold, did not state that Plaintiff had failed, did not provide a score, and did not disclose when AT&T received or reviewed any rating."),
    ("PARA", "42. The testing and transmission logs, audio, rating, rubric, rater identity, quality review, AT&T receipt time, and any retest or appeal process are exclusively controlled by AT&T, LTI, and their agents."),
    ("PARA", "43. By May 28, the assessment window had closed. AT&T nevertheless approved Plaintiff, generated the formal offer, and advanced him to onboarding and background screening."),
    ("SUBHEAD", "C. AT&T Issues a Specific Written Offer"),
    ("PARA", "44. On May 28 at 10:13 a.m., Workday sent Plaintiff an email titled 'Welcome to the team.'"),
    ("PARA", "45. AT&T stated: 'Congratulations are in order! We're impressed by the skills and experience you bring to AT&T and are excited to officially offer you the position of R-106742 Bilingual Spanish Retail Sales Consultant.'"),
    ("PARA", "46. AT&T directed Plaintiff to sign into Candidate Home to review and accept the formal offer and identified Patterson as the recruiter for questions."),
    ("PARA", "47. The formal written offer identified the position as 'Retail Sales Consultant,' reporting to Orville R. Bell, at 2439 West Kettleman Lane; compensation of $24.95 per hour paid biweekly; annual targeted variable compensation of $13,700 prorated for part-time hours under the AT&T my-comp Sales Compensation Plan; and a tentative June 15, 2026 start date."),
    ("PARA", "48. The offer stated that employment was contingent upon formal acceptance and required hiring documents, proof of identity and work authorization, any applicable deemed-export review, absence of restrictive agreements, any applicable rehire-eligibility check, and satisfactory standardized background checks. It stated that unmet contingencies before the start date risked rescission. The two-page offer did not list Spanish proficiency, passage of the ACTFL assessment, at-will status, arbitration, a guaranteed weekly schedule, or an unrestricted pre-start withdrawal right. The Workday acceptance audit and any separate incorporated documents remain in AT&T's possession."),
    ("PARA", "49. The offer did not tell Plaintiff that AT&T considered him disqualified for Spanish proficiency. To the contrary, it announced that AT&T had officially selected him for the expressly bilingual requisition after the assessment window had closed."),
    ("SUBHEAD", "D. AT&T Commences Offer and Screening Tasks"),
    ("PARA", "50. At 10:15 a.m., Workday assigned Plaintiff 'Review Documents—Offer for Job Application' for R-106742 and candidate application C-1690172."),
    ("PARA", "51. At 10:16 a.m., Workday assigned a 'Change Government Identifiers' task within the same offer business process."),
    ("PARA", "52. At 10:17 a.m., Workday assigned a 'Change Personal Information' task within the same offer business process."),
    ("PARA", "53. At 10:19 a.m., First Advantage stated that AT&T Non Management had contracted with it and assigned Plaintiff a task. It directed Plaintiff to a secure site, referenced FCRA disclosure and authorization, and described possible ID.me identity verification."),
    ("PARA", "54. The 10:19 communication establishes that AT&T placed a screening order with First Advantage. Defendants' systems will show the order time, package, searches, candidate activity, completion status, results, adjudication, access, and cancellation history."),
    ("PARA", "55. Plaintiff accepted the offer through AT&T's Workday process, timely undertook the mandatory onboarding and screening steps presented to him, furnished personal information for that purpose, and remained ready, willing, and able to begin on June 15. [PLAINTIFF MUST CONFIRM THIS PARAGRAPH BEFORE EXECUTION.]"),
    ("SUBHEAD", "E. AT&T Reverses the Approved Decision at 12:23 p.m."),
    ("PARA", "56. At 12:23 p.m., Patterson sent Plaintiff a text message stating: 'Hi Brendan. Unfortunately, the manager advised me that he no longer wants to move forward with your offer. He stated that he need a Spanish speaker and you did not pass the Spanish assessment. Sorry for the inconvenience.'"),
    ("PARA", "57. Plaintiff replied politely: 'No worries sir, thank you for the opportunity.' That response did not release any claim, waive any right, admit that the explanation was accurate, or indicate that Plaintiff had seen the underlying score."),
    ("PARA", "58. Patterson attributed the decision to 'the manager.' The formal offer identifies Orville R. Bell as Plaintiff's reporting manager, but the current record does not establish whether Bell made the rescission decision. The text did not provide the score, test date, passing standard, identity of the actual decisionmaker, or any formal rescission or appeal process."),
    ("PARA", "59. The text's reference to 'your offer' corroborates that AT&T had made an offer. Its statement that the manager 'no longer' wished to move forward corroborates a reversal of an approved decision."),
    ("PARA", "60. AT&T did not provide Plaintiff, before the 12:23 decision, a copy of any First Advantage report or a written summary of rights under the FCRA."),
    ("PARA", "61. AT&T did not advise Plaintiff that a First Advantage investigative consumer report had been obtained or provide First Advantage's name and address as the source of information used in the decision, as ICRAA requires when an employment denial occurs under circumstances in which such a report was obtained."),
    ("PARA", "62. AT&T did not provide a preliminary criminal-history decision notice, individualized assessment, opportunity to respond, or final background-based notice. It instead supplied the Spanish explanation."),
    ("SUBHEAD", "F. Facts Supporting the Screening and Pretext Inference"),
    ("PARA", "63. The Spanish assessment necessarily preceded the May 28 offer because the test expired on May 25."),
    ("PARA", "64. AT&T's systems were capable of preventing an offer if a mandatory qualification had already been finally failed. AT&T instead issued a specific offer and three onboarding tasks."),
    ("PARA", "65. The abrupt reversal occurred only after AT&T placed the First Advantage order and the hiring process entered the background stage."),
    ("PARA", "66. No primary score or failure notice was sent to Plaintiff before or with the offer. The first and only failure assertion in the current record is Patterson's secondhand text after screening began."),
    ("PARA", "67. Plaintiff's simultaneous Stockton requisition did not require Spanish. Its unexplained disposition is relevant because a Spanish-proficiency issue cannot rationally disqualify Plaintiff from a non-bilingual position."),
    ("PARA", "68. First Advantage had previously matched Plaintiff to the California Sex Offender Registry in an employment report. The July 2024 UPS report marked the sex-offender search 'Decisional' and the overall result 'INELIGIBLE' while a national criminal-file component returned 'No Record Found.'"),
    ("PARA", "69. On information and belief, First Advantage retained identifying information, matching rules, or adjudication data from its prior screening of Plaintiff and used the same or materially similar registry-search process for AT&T."),
    ("PARA", "70. On information and belief, between 10:19 a.m. and 12:23 p.m., First Advantage's screening system returned, flagged, reused, transmitted, displayed, or escalated sex-offender registry information concerning Plaintiff, or informed AT&T that the screening would produce an adverse result."),
    ("PARA", "71. On information and belief, AT&T's hiring manager, recruiter, centralized adjudication personnel, or screening personnel accessed, received, or learned of that information and it caused or substantially motivated the reversal."),
    ("PARA", "72. Plaintiff states the basis for paragraphs 69 through 71: the precise sequence; the already-completed assessment period; the offer and onboarding approval; First Advantage's immediate involvement; its documented prior registry match to Plaintiff; the abrupt reversal; the lack of primary language-score evidence; and the absence of consumer-report adverse-action notices."),
    ("PARA", "73. The alternative explanations and exact timestamps can be resolved from a discrete set of electronic records in Defendants' possession. Plaintiff will seek the First Advantage order and component logs, report and audit history, AT&T Workday business-process history, LTI transmission logs, and Patterson/manager communications. Lerma v. Amazon.com Services, LLC, C.D. Cal. No. 8:22-cv-01727, Dkt. 36, dismissed a Megan's Law count after the employer's report was in the record and showed ordinary court records and a national sex-offender search returning no record. That dismissal turned on the report. This Complaint does not attach the AT&T First Advantage report. A court cannot perform a Lerma analysis on the face of a complaint that does not contain the employer's report. Defendants may not obtain a pleading-stage dismissal by withholding the one document that would confirm or refute the inference. If production shows ordinary court records and no California-registry source, the section 290.46(j) count will stand or fall on that record — after production, not before. The offer, contract, estoppel, and ICRAA counts do not depend on that inference."),
    ("SUBHEAD", "G. Reliance, Harm, and Continuing Effects"),
    ("PARA", "74. AT&T intended the offer and onboarding communications to induce Plaintiff to accept the position, complete mandatory tasks, disclose sensitive identifying information, prepare for the June 15 start, and refrain from treating the Lodi position as unavailable."),
    ("PARA", "75. Plaintiff reasonably understood 'officially offer,' the specified compensation, start date, and immediate onboarding sequence to mean AT&T had approved him subject to the written contingencies being administered lawfully and in good faith."),
    ("PARA", "76. Plaintiff had no reason to believe AT&T would issue an offer for an expressly bilingual position while secretly treating a completed language assessment as already disqualifying."),
    ("PARA", "77. Defendants' conduct deprived Plaintiff of a meaningful opportunity to review and respond to any consumer report, dispute its source or lawful use, preserve the AT&T and Stockton opportunities, and make informed employment decisions."),
    ("PARA", "78. Plaintiff lost the offered Lodi employment opportunity, including the opportunity to earn $24.95 per hour and targeted variable compensation beginning on or about June 15, subject to mitigation and proof."),
    ("PARA", "79. Plaintiff also suffered out-of-pocket and reliance losses, loss of other employment opportunities pursued or forgone in reliance on the offer, time devoted to onboarding and screening, emotional distress, anxiety, humiliation, and frustration from the abrupt and unexplained reversal."),
    ("PARA", "80. Plaintiff has sought and continues to seek replacement employment and does not claim a guaranteed lifetime or one-year expectancy from an at-will position. Economic damages will be limited to losses proven with reasonable certainty and without double recovery."),
    ("HEADER", "V.\nALTERNATIVE PLEADING AND PRESERVATION"),
    ("PARA", "81. Plaintiff pleads the statutory screening counts on the good-faith inference that a consumer report or registry result reached or influenced AT&T before rescission. Defendants may possess evidence disproving that inference. If so, the offer-based counts remain independent. The section 290.46(j) claim has four elements: (a) information disclosed pursuant to section 290.46; (b) use of that information by a defendant; (c) a purpose relating to employment; and (d) the use was not to protect a person at risk and was not otherwise authorized by law. Elements (a) and (b) are pleaded on information and belief because the AT&T report is exclusively in Defendants' files. A demurrer tests the pleading, not the unproduced report."),
    ("PARA", "82. Plaintiff pleads contract and implied-covenant theories if the Workday acceptance formed an agreement. If no enforceable contract formed, Plaintiff pleads promissory estoppel and misrepresentation in the alternative."),
    ("PARA", "83. Plaintiff specifically relied by accepting the offer, completing or beginning required onboarding and screening, disclosing personal information, preparing for the June 15 start, ceasing further pursuit of the Lodi opening, and foregoing or delaying pursuit of identified alternative work. [PLAINTIFF MUST CONFIRM EACH FORM OF RELIANCE AND IDENTIFY THE ALTERNATIVE WORK BEFORE EXECUTION.]"),
    ("PARA", "84. Plaintiff does not plead a FEHA or Fair Chance Act cause of action in this Complaint because the present portfolio does not contain a California Civil Rights Department charge and right-to-sue notice. Plaintiff preserves all timely rights to exhaust and seek leave to amend if discovery supports those theories."),
    ("PARA", "85. The omission of an unexhausted FEHA count is deliberate. Plaintiff does not allege that requiring Spanish for an expressly bilingual position is inherently unlawful. The relevant issue is whether AT&T's stated assessment reason was accurate or pretextual."),
    ("HEADER", "VI.\nFIRST CAUSE OF ACTION"),
    ("SUBHEAD", "Unauthorized Employment Use of Registry Information\nPenal Code section 290.46(j) — Against All Defendants"),
    ("PARA", "86. Plaintiff realleges paragraphs 1 through 85, except that allegations expressly pleaded in the alternative are incorporated only to the extent consistent with this cause."),
    ("PARA", "87. Penal Code section 290.46(j)(1) authorizes use of information disclosed under that section only to protect a person at risk, except as otherwise authorized by law."),
    ("PARA", "88. Section 290.46(j)(2)(E) prohibits use of information disclosed under that section for purposes relating to employment unless another law authorizes the use."),
    ("PARA", "89. Section 290.46(j)(4)(A) makes the user liable for actual damages and an amount not exceeding three times actual damages and not less than $250, attorney's fees, exemplary damages, or a civil penalty not exceeding $25,000."),
    ("PARA", "90. First Advantage's own prior report identifies its registry component as a Department of Justice website search, states that the source of record was the California Sex Offender Registry, labels Plaintiff a registered sex offender, and treats the result as decisional for employment."),
    ("PARA", "91. On information and belief, First Advantage used information disclosed through the California registry directly or through a derivative national/DOJ compilation when it processed, scored, flagged, furnished, or escalated Plaintiff's AT&T employment screening."),
    ("PARA", "92. On information and belief, AT&T used the same information when it accessed, reviewed, acted upon, or accepted First Advantage's screening result and rescinded Plaintiff's offer."),
    ("PARA", "93. The use related directly to employment. The only purpose of the First Advantage order was to screen Plaintiff for the offered AT&T position."),
    ("PARA", "94. The use was not to protect a person at risk and was not otherwise authorized by law for this retail-sales hiring decision."),
    ("PARA", "95. Defendants knew or should have known that employment use was prohibited because the California registry itself displays misuse warnings; First Advantage is a professional CRA; First Advantage's prior report identified the California source; and AT&T is a sophisticated employer that publicly describes itself as a fair-chance employer."),
    ("PARA", "96. Defendants concealed the screening basis by supplying a preexisting Spanish-assessment rationale and omitting the disclosures and review process that would have revealed consumer-report use."),
    ("PARA", "97. Defendants' use was a substantial factor in the rescission and caused the loss and injury alleged."),
    ("PARA", "98. Plaintiff seeks the remedies authorized by section 290.46(j)(4), including actual and statutory relief according to proof, and preventive relief under subdivision (j)(4)(B) to restrain any pattern or practice of employment use."),
    ("HEADER", "VII.\nSECOND CAUSE OF ACTION"),
    ("SUBHEAD", "Fair Credit Reporting Act — Pre-Adverse Action\n15 U.S.C. section 1681b(b)(3)(A) — Against AT&T and Employer DOES"),
    ("PARA", "99. Plaintiff realleges paragraphs 1 through 85 and 90 through 97 to the extent consistent with this cause."),
    ("PARA", "100. The First Advantage background screening was a consumer report obtained for employment purposes within the FCRA."),
    ("PARA", "101. AT&T was a person using or intending to use the consumer report for employment purposes."),
    ("PARA", "102. On information and belief, AT&T's rescission was based in whole or in part on information in, produced by, or communicated through the First Advantage report or screening process."),
    ("PARA", "103. Before taking the adverse action, AT&T was required to provide Plaintiff a copy of the report and a written description of his FCRA rights."),
    ("PARA", "104. AT&T provided neither before the 12:23 p.m. rescission and gave Plaintiff no meaningful opportunity to review or respond. [PLAINTIFF MUST CONFIRM THAT NO SUCH MATERIALS WERE RECEIVED THROUGH ANY PORTAL OR EMAIL BEFORE EXECUTION.]"),
    ("PARA", "105. The violation caused concrete informational and procedural injury: Plaintiff was denied the report and rights Congress required before an employment decision, was unable to identify or challenge the source and use of registry information, and lost the offered position before any review period."),
    ("PARA", "106. AT&T's violation was negligent under 15 U.S.C. section 1681o and, on information and belief, willful or reckless under section 1681n because AT&T maintained standardized screening procedures, knew the pre-adverse requirement, and bypassed it by communicating another reason immediately after screening began."),
    ("PARA", "107. Plaintiff seeks actual damages, statutory damages if willfulness is proven, punitive damages as authorized by federal law, costs, and any attorney's fees available if Plaintiff later obtains counsel."),
    ("HEADER", "VIII.\nTHIRD CAUSE OF ACTION"),
    ("SUBHEAD", "California Investigative Consumer Reporting Agencies Act\nCivil Code sections 1786.40 and 1786.50 — Against AT&T and User DOES"),
    ("PARA", "108. Plaintiff realleges paragraphs 1 through 85 and 90 through 97 to the extent consistent with this cause."),
    ("PARA", "109. First Advantage is an investigative consumer reporting agency, and its employment background report concerns Plaintiff's character, general reputation, personal characteristics, or mode of living."),
    ("PARA", "110. AT&T procured or caused that report to be prepared for employment purposes and was the user of its information."),
    ("PARA", "111. On information and belief, the report was obtained before AT&T denied employment."),
    ("PARA", "112. Civil Code section 1786.40(a) required AT&T, under circumstances in which employment was denied and an investigative consumer report had been obtained, to advise Plaintiff of that fact and supply the agency's name and address."),
    ("PARA", "113. AT&T did not comply. The First Advantage task invitation preceded the report and did not advise Plaintiff, at the time of rescission, that a report had been obtained or used."),
    ("PARA", "114. The omission prevented Plaintiff from timely obtaining the AT&T-specific report, testing its source, and invoking his statutory inspection and dispute rights. This ICRAA count does not depend on proving Penal Code section 290.46(j). A notice failure under Civil Code section 1786.40 is independently actionable if an investigative consumer report was obtained and employment was denied without the required advice. That count can reach discovery even if the registry-use inference later fails. Civil Code sections 1786.10 and 1786.22 entitle Plaintiff to inspect and obtain a copy of the information First Advantage maintains on him. Plaintiff has not yet served that inspection request. He will."),
    ("PARA", "115. Under Civil Code section 1786.50, Plaintiff seeks actual damages or $10,000, whichever is greater, costs, attorney's fees if represented, and punitive damages upon proof of gross negligence or willfulness."),
    ("PARA", "116. This ICRAA count rests on an act or omission distinct from the FCRA count. The FCRA count challenges AT&T's pre-decision failure to furnish the report and federal rights summary; this count challenges AT&T's separate failure, when communicating the denial, to advise that an investigative report had been obtained and to supply the agency's name and address. Plaintiff pleads no duplicative ICRAA theory for the same act or omission and will elect remedies to the extent Civil Code section 1786.52 requires."),
    ("PARA", "116A. Plaintiff reserves amendment under Civil Code section 1786.16 if production shows AT&T procured the report before providing the required standalone disclosure and obtaining written authorization. Plaintiff does not presently allege nonauthorization as an established fact."),
    ("HEADER", "IX.\nFOURTH CAUSE OF ACTION"),
    ("SUBHEAD", "Breach of Contract — Against AT&T and Employer DOES\n(Pleaded in the Alternative)"),
    ("PARA", "117. Plaintiff realleges paragraphs 1 through 85, except the no-contract alternative."),
    ("PARA", "118. AT&T made a written offer containing the material position, compensation, start-date, acceptance, and contingency terms, and Plaintiff timely accepted it through Workday. [PLAINTIFF MUST CONFIRM THE ACCEPTANCE METHOD AND TIMESTAMP BEFORE EXECUTION.]"),
    ("PARA", "119. The accepted offer formed an agreement for at-will employment subject to stated pre-employment conditions administered lawfully and in good faith."),
    ("PARA", "120. Plaintiff performed, commenced performance, or was excused from further performance because AT&T repudiated the agreement and prevented completion of the remaining conditions."),
    ("PARA", "121. Plaintiff remained ready, willing, and able to perform the Retail Sales Consultant role and to complete lawful conditions."),
    ("PARA", "122. AT&T breached by rescinding the accepted offer based on a reason it had already evaluated or waived before contracting, by preventing satisfaction of conditions, and/or by using an unlawful screening criterion."),
    ("PARA", "123. AT&T may not rely on failure of a condition that it wrongfully caused, prevented, waived, or applied in violation of law."),
    ("PARA", "124. The at-will nature of prospective employment limits but does not erase reliance and other damages caused before Plaintiff received a good-faith opportunity to begin performance."),
    ("PARA", "125. AT&T's breach caused damages according to proof, subject to mitigation and the prohibition against double recovery."),
    ("HEADER", "X.\nFIFTH CAUSE OF ACTION"),
    ("SUBHEAD", "Breach of the Implied Covenant of Good Faith and Fair Dealing\nAgainst AT&T and Employer DOES (Alternative)"),
    ("PARA", "126. Plaintiff realleges paragraphs 117 through 125."),
    ("PARA", "127. Every contract contains an implied covenant that neither party will unfairly frustrate the other's right to receive the agreement's benefits."),
    ("PARA", "128. The accepted offer gave AT&T discretion to evaluate standardized background checks and other contingencies. That discretion had to be exercised honestly, in good faith, for authorized purposes, and consistently with the parties' justified expectations."),
    ("PARA", "129. AT&T frustrated the agreement by issuing and inducing acceptance of an offer after the language-assessment period, commencing onboarding, and then invoking that preexisting assessment only after screening began."),
    ("PARA", "130. Alternatively, AT&T exercised screening discretion in bad faith by considering a prohibited registry source, concealing that consideration, and denying the contractual pre-adverse review process required by law."),
    ("PARA", "131. The conduct deprived Plaintiff of the opportunity to satisfy lawful conditions and receive the benefit of the accepted offer."),
    ("PARA", "132. Plaintiff suffered the reliance and economic losses alleged in paragraphs 78 through 80 and 83. [PLAINTIFF MUST CONFIRM THOSE LOSSES BEFORE EXECUTION.]"),
    ("HEADER", "XI.\nSIXTH CAUSE OF ACTION"),
    ("SUBHEAD", "Promissory Estoppel — Against AT&T and Employer DOES\n(Alternative if No Contract Formed)"),
    ("PARA", "133. Plaintiff realleges paragraphs 1 through 85 except allegations requiring an enforceable contract."),
    ("PARA", "134. AT&T made a clear promise by stating that it was 'excited to officially offer' Plaintiff the identified Lodi position and by providing specific compensation, a tentative start date, and immediate onboarding tasks."),
    ("PARA", "135. AT&T reasonably expected the promise to induce acceptance, disclosure of sensitive information, completion of screening, preparation for work, and employment-related action or forbearance."),
    ("PARA", "136. Plaintiff reasonably relied because the offer followed completion of AT&T's interview and assessment stages and was communicated as official rather than tentative selection."),
    ("PARA", "137. The reliance was foreseeable because the purpose of an employment offer and onboarding workflow is to cause the applicant to commit to the position and prepare to begin."),
    ("PARA", "138. Plaintiff changed position in the ways alleged in paragraphs 55, 74 through 80, and 83."),
    ("PARA", "139. AT&T withdrew the promise before giving Plaintiff a good-faith opportunity to begin, causing substantial detriment."),
    ("PARA", "140. Injustice can be avoided only by enforcing the promise to the extent justice requires or awarding reliance damages."),
    ("PARA", "141. Plaintiff seeks reliance losses, not a speculative guarantee of indefinite employment. California law permits proven employment-opportunity losses caused by reasonable reliance on a rescinded offer. (Sheppard v. Morgan Keegan & Co. (1990) 218 Cal.App.3d 61; Toscano v. Greene Music (2004) 124 Cal.App.4th 685.)"),
    ("HEADER", "XII.\nSEVENTH CAUSE OF ACTION"),
    ("SUBHEAD", "Negligent Misrepresentation — Against AT&T and Representation DOES\n(Pleaded in the Alternative)"),
    ("PARA", "142. Plaintiff realleges paragraphs 1 through 85 except allegations of intentional falsity."),
    ("PARA", "143. AT&T represented at 10:13 a.m. that it had officially offered Plaintiff R-106742 and then represented through onboarding tasks that the approved offer process was proceeding."),
    ("PARA", "144. If AT&T had already received and treated the Spanish result as finally disqualifying, AT&T's representation that it was officially offering the expressly bilingual position was false or misleading when made."),
    ("PARA", "145. If AT&T had not obtained managerial approval, had already decided not to hire Plaintiff, or knew its workflow would automatically disqualify him based on existing data, AT&T lacked reasonable grounds for believing the representation true. [THIS THEORY DEPENDS ON INTERNAL RECORDS AND PLAINTIFF'S CONFIRMED RELIANCE.]"),
    ("PARA", "146. AT&T made the representation to induce Plaintiff to accept, undertake onboarding and screening, disclose personal information, and prepare to begin work."),
    ("PARA", "147. Plaintiff did not know the undisclosed internal facts and reasonably relied on the official offer and onboarding sequence."),
    ("PARA", "148. Plaintiff's reliance caused the detriment alleged in paragraphs 78 through 80 and 83."),
    ("PARA", "149. AT&T's failure to use reasonable care in communicating an approved offer after the assessment period was a substantial factor in causing the harm."),
    ("HEADER", "XIII.\nEIGHTH CAUSE OF ACTION"),
    ("SUBHEAD", "Intentional Misrepresentation and Fraudulent Concealment\nAgainst AT&T and Fraud DOES (Alternative; Subject to Proof)"),
    ("PARA", "150. Plaintiff realleges paragraphs 1 through 85 and 143 through 149, except allegations expressly limited to negligence."),
    ("PARA", "151. The speaker and medium were specific: AT&T, through its Workday recruiting system and the personnel who approved its business process, represented to Plaintiff at 10:13 a.m. on May 28 that AT&T was officially offering him R-106742."),
    ("PARA", "152. The representation concerned an existing fact—that AT&T had approved and was extending the offer—not merely future performance."),
    ("PARA", "153. AT&T also concealed material facts known only to it: whether it already possessed an adverse Spanish result; whether the manager had approved or opposed the offer; whether a First Advantage result caused the reversal; and whether AT&T intended to use a prohibited criterion."),
    ("PARA", "154. AT&T had exclusive knowledge of those facts, actively supplied a different explanation after screening began, and made partial representations likely to mislead absent full disclosure."),
    ("PARA", "155. On information and belief, if AT&T already knew at 10:13 a.m. that it would not honor the offer, it made the representation knowingly or recklessly and intended Plaintiff to act through the onboarding and screening process."),
    ("PARA", "156. Alternatively, if AT&T genuinely approved the offer at 10:13 and changed its decision only after receiving prohibited screening information, the fraud count may not apply, but the statutory counts do."),
    ("PARA", "157. Plaintiff reasonably relied as alleged, and AT&T's misrepresentation or concealment caused the resulting harm."),
    ("PARA", "158. Fraudulent inducement of an employment agreement may support tort damages for reliance injuries distinct from contract expectancy. (Lazar v. Superior Court (1996) 12 Cal.4th 631.)"),
    ("PARA", "159. Plaintiff seeks tort damages caused by the inducement and concealment without duplicating contract damages."),
    ("PARA", "160. Plaintiff seeks punitive damages against AT&T only upon proof that an officer, director, or managing agent authorized, ratified, or personally engaged in fraud, malice, or oppression under Civil Code section 3294(b). [MANAGING-AGENT FACTS ARE NOT YET ESTABLISHED; NO SPECIFIC AMOUNT IS PLEADED.]"),
    ("HEADER", "XIV.\nNINTH CAUSE OF ACTION"),
    ("SUBHEAD", "Unlawful and Unfair Business Practices\nBusiness and Professions Code section 17200 — Against All Defendants"),
    ("PARA", "161. Plaintiff realleges paragraphs 1 through 160 to the extent consistent with this equitable cause."),
    ("PARA", "162. Defendants engaged in unlawful practices by violating Penal Code section 290.46(j), the FCRA, and ICRAA as alleged."),
    ("PARA", "163. Defendants engaged in unfair practices by structuring employment screening so an offer could be reversed immediately upon secret adverse information while denying the applicant the source, report, review period, and opportunity to respond."),
    ("PARA", "164. AT&T engaged in fraudulent practices likely to mislead a reasonable applicant by announcing an official offer and demanding sensitive onboarding action while concealing a known disqualification or undisclosed screening basis."),
    ("PARA", "165. Plaintiff suffered injury in fact and lost money or property through the reliance expenditures, employment-search costs, and other economic losses alleged and to be proven."),
    ("PARA", "166. Plaintiff does not seek future unearned wages as UCL restitution. He seeks restitution only of money or property in which he had a vested interest and that Defendants acquired or caused him to expend through the challenged practices, according to proof."),
    ("PARA", "167. Legal damages are not an adequate remedy for Defendants' retention, use, and dissemination of registry-derived screening data or their ongoing secret-screening practices."),
    ("PARA", "168. Plaintiff seeks an injunction requiring Defendants to cease prohibited employment use of California registry information; preserve and disclose the source and audit trail of AT&T screening; correct or segregate unlawfully used data; and implement lawful pre-adverse procedures."),
    ("PARA", "169. Plaintiff also seeks restitution and declaratory relief ancillary to the injunction to the extent authorized by Business and Professions Code section 17203."),
    ("HEADER", "XV.\nPRESERVATION OF EVIDENCE"),
    ("PARA", "170. Defendants are on notice to preserve the AT&T Workday record for C-1690172 and requisitions R-106742 and R-107776; offer versions and acceptance logs; approvals and communications involving Orville R. Bell and Richard Patterson; LTI/ACTFL score and transmission data; the individual First Advantage order under client account 132156, report, component, adjudication, access and cancellation logs, and the First Advantage file subject to Civil Code sections 1786.10 and 1786.22; ID.me events; text and email communications; and policies governing registry, FCRA, ICRAA, and fair-chance review."),
    ("PARA", "171. Relevant electronically stored information includes audit fields, event timestamps, reason codes, API messages, report views, internal chats, emails, SMS, candidate-status history, and data-retention records from May 16 through June 30, 2026."),
    ("PARA", "172. The same First Advantage identifiers and prior UPS report are relevant to whether First Advantage reused, matched, or retained registry data concerning Plaintiff."),
    ("HEADER", "XVI.\nPRAYER FOR RELIEF"),
    ("PARA", "WHEREFORE, Plaintiff prays for judgment against Defendants as follows:"),
    ("LIST_ITEM", "1. For actual, reliance, consequential, and economic damages according to proof, without double recovery;"),
    ("LIST_ITEM", "2. For the remedies authorized by Penal Code section 290.46(j)(4)(A), including statutory, treble, exemplary, or civil-penalty relief as the trier of fact and law permit;"),
    ("LIST_ITEM", "3. For FCRA actual damages under 15 U.S.C. section 1681o and statutory and punitive damages upon proof of willfulness under section 1681n;"),
    ("LIST_ITEM", "4. For ICRAA actual damages or $10,000, whichever is greater, and punitive damages upon the showing required by Civil Code section 1786.50;"),
    ("LIST_ITEM", "5. For contract and promissory-estoppel reliance damages according to proof;"),
    ("LIST_ITEM", "6. For tort damages caused by negligent or intentional misrepresentation and concealment;"),
    ("LIST_ITEM", "7. For punitive damages against only those Defendants for whom the statutory prerequisites are proven, in an amount to be determined by the trier of fact;"),
    ("LIST_ITEM", "8. For restitution under Business and Professions Code section 17203 to the extent available;"),
    ("LIST_ITEM", "9. For preventive and injunctive relief under Penal Code section 290.46(j)(4)(B), Business and Professions Code section 17203, and other applicable law;"),
    ("LIST_ITEM", "10. For declaratory relief concerning Defendants' prohibited registry use and screening practices to the extent an actual controversy remains;"),
    ("LIST_ITEM", "11. For costs of suit and attorney's fees where authorized if Plaintiff obtains counsel;"),
    ("LIST_ITEM", "12. For prejudgment and post-judgment interest as allowed by law; and"),
    ("LIST_ITEM", "13. For such other relief as the Court deems just and proper."),
    ("HEADER", "XVII.\nDEMAND FOR JURY TRIAL"),
    ("PARA", "173. Plaintiff demands trial by jury on all causes of action and issues so triable."),
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
