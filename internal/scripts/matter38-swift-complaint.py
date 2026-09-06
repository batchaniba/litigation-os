#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Matter 38 — verified complaint, Swift Transportation Co. of Arizona LLC.

San Joaquin Superior Court. The decrypted Sept. 26, 2023 pre-adverse packet
is in hand. NSOPW remained Processing. Plaintiff pleads on information and
belief that Swift used preliminary sex-offender-registry information from
that in-process component, in whole or in part, in the denial. ICRAA and
UCL remain independent paths.

Default output is unsigned. On or after September 8, 2026, rerun with
``--execute`` only after Plaintiff confirms the role.

    python3 internal/scripts/matter38-swift-complaint.py
    python3 internal/scripts/matter38-swift-complaint.py --execute
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
    / "internal/public/documents/matter-38"
    / "Verified Complaint - Ngwa Nforbi v Swift Transportation Co of Arizona LLC"
    " (REVIEW DRAFT for Sep 8 2026).pdf"
)
DEFAULT_EXEC_DATE = "September 8, 2026"
EARLIEST_EXECUTION_DATE = dt.date(2026, 9, 8)
COURT_LINE2 = "COUNTY OF SAN JOAQUIN"
FOOTER = "VERIFIED COMPLAINT -- BRENDAN NGWA NFORBI v. SWIFT TRANSPORTATION CO. OF ARIZONA LLC"

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
    ("ARIZONA LLC, a limited liability", True, False),
    ("company, d/b/a SWIFT", True, False),
    ("TRANSPORTATION; and DOES 1", True, False),
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
    ("(1) Penal Code § 290.46(j)", False, False),
    ("      (I&B — preliminary", False, False),
    ("      NSOPW / registry);", False, False),
    ("(2) ICRAA, Civ. Code", False, False),
    ("      §§ 1786.40, 1786.50;", False, False),
    ("(3) UCL, B&P Code § 17200", False, False),
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
        "THE SEPTEMBER 26, 2023 PRE-ADVERSE PACKET HAS BEEN DECRYPTED. "
        "NSOPW REMAINED PROCESSING. THE SECTION 290.46(j) COUNT IS "
        "PLEADED ON INFORMATION AND BELIEF THAT SWIFT USED PRELIMINARY "
        "SEX-OFFENDER-REGISTRY INFORMATION FROM THAT IN-PROCESS COMPONENT. "
        "CONFIRM THE DRIVER ROLE.",
    ),
    ("PARA", 'Plaintiff BRENDAN NGWA NFORBI ("Plaintiff") alleges as follows:'),
    ("HEADER", "I.\nINTRODUCTION"),
    (
        "PARA",
        "1. This is an action under Penal Code section 290.46, subdivision (j), "
        "the California Investigative Consumer Reporting Agencies Act, and the "
        "Unfair Competition Law. In September 2023, Plaintiff applied to Swift "
        "Transportation Co. of Arizona LLC for commercial-driver work. On "
        "September 26, 2023, Swift sent a pre-adverse packet whose National "
        "Sex Offender Public Website component remained 'Processing.' On "
        "October 5, 2023, Swift sent a post-adverse letter admitting that "
        "consumer reports from Asurint, Tenstreet, DriverIQ, FMCSA-DOT, and "
        "Equifax Work Number caused the denial. Plaintiff is informed and "
        "believes, and on that basis alleges, that Swift's decision was based "
        "in whole or in part on preliminary information from that report "
        "citing a sex-offender registry.",
    ),
    (
        "PARA",
        "2. The September 26, 2023 pre-adverse packet has been decrypted. "
        "Plaintiff alleges its contents as known facts. The packet does not "
        "state 'SOURCE OF RECORD: CALIFORNIA SEX OFFENDER REGISTRY.' The "
        "National Criminal search run without a sex-offender component "
        "returned Clear / No Reportable Records Found. Federal criminal "
        "returned Clear. The county criminal searches that had completed "
        "returned Clear. The National Sex Offender Public Website component "
        "remained 'Processing' on every snapshot in the packet. It never "
        "completed. It reported no hit. Clearinghouse returned Driver Not "
        "Prohibited. What the packet does contain — a Class A commercial "
        "driver's license, an April 22, 2022 improper-lane moving violation "
        "with zero points, PSP inspection history, and a CDLIS license-"
        "identity match — is not information disclosed pursuant to Penal Code "
        "section 290.46.",
    ),
    (
        "PARA",
        "3. Penal Code section 290.46(j)(1) authorizes use of information "
        "disclosed under that section only to protect a person at risk. "
        "Subdivision (j)(2)(E) prohibits use of that information for purposes "
        "relating to employment, except as another law authorizes. A "
        "commercial-driver hiring decision is a purpose relating to employment.",
    ),
    (
        "PARA",
        "4. Federal motor-carrier screening does not swallow this claim. The "
        "FMCSA Drug and Alcohol Clearinghouse and the Pre-Employment Screening "
        "Program concern drug-and-alcohol violations and crash or inspection "
        "history. They are not Penal Code section 290.46 disclosures. An "
        "employer that may lawfully obtain ordinary criminal-history or "
        "safety records is not thereby authorized to use Megan's Law website "
        "information for employment. Penal Code section 290.46(j)(3) says so.",
    ),
    (
        "PARA",
        "5. Plaintiff does not allege that the decrypted packet contains a "
        "completed NSOPW hit or the words 'SOURCE OF RECORD: CALIFORNIA SEX "
        "OFFENDER REGISTRY.' He does allege, on information and belief, that "
        "Swift used preliminary information from the still-Processing NSOPW "
        "component — information citing a sex-offender registry, including "
        "information disclosed pursuant to Penal Code section 290.46 or a "
        "derivative national compilation whose source was the California "
        "registry — in whole or in part in the denial. Code of Civil "
        "Procedure section 425.10 requires a statement of the facts "
        "constituting the cause of action in ordinary and concise language. "
        "Section 452 requires this Court to construe the pleading liberally. "
        "The vendor adjudication log, interim NSOPW return, and "
        "decision-maker communications are exclusively in Defendants' "
        "possession.",
    ),
    (
        "PARA",
        "6. In July 2024, First Advantage prepared an employment background "
        "report on Plaintiff for United Parcel Service. That report, later "
        "lodged in federal court by UPS, identified a Department of Justice "
        "website / National Sex Offender Registry search as decisional, stated "
        "'SOURCE OF RECORD: CALIFORNIA SEX OFFENDER REGISTRY,' and produced "
        "an overall INELIGIBLE result. That report is not the Swift report. "
        "It is alleged because it shows that commercial screeners could and "
        "did identify this Plaintiff through the California registry and treat "
        "that identification as dispositive of employment eligibility.",
    ),
    (
        "PARA",
        "7. Plaintiff does not name Knight-Swift Transportation Holdings, Inc., "
        "or any other parent, merely because it owns affiliated entities. He "
        "has sued DOES 1 through 10 for the consumer reporting agency that "
        "actually returned registry-derived information and for any Swift "
        "affiliate that was the actual employing or decision-making entity.",
    ),
    (
        "PARA",
        "8. This Complaint does not plead a Tameny wrongful-termination or "
        "failure-to-hire count, an IIED count, a Fair Credit Reporting Act "
        "count, or a FEHA or Fair Chance Act count. The section 290.46(j) "
        "count is pleaded on information and belief that Swift used "
        "preliminary sex-offender-registry information from the in-process "
        "NSOPW component. Civil Code sections 1786.40 and 1786.50 and "
        "Business and Professions Code section 17200 are independent paths "
        "that do not require a completed registry hit. Plaintiff preserves "
        "all timely rights to seek leave to amend.",
    ),
    ("HEADER", "II.\nPARTIES"),
    (
        "PARA",
        "9. Plaintiff BRENDAN NGWA NFORBI is a natural person residing in "
        "Stockton, San Joaquin County, California. He is also identified in "
        "employment and court records as Brendan Ngehsi Ngwa Nforbi and "
        "Brendan Ngehsi Ngwanforbi. Those name variants refer to Plaintiff.",
    ),
    (
        "PARA",
        "10. Plaintiff is required to register under California Penal Code "
        "section 290. At all times relevant to this Complaint, information "
        "identifying him appeared on California's Megan's Law website and "
        "California Sex Offender Registry, operated pursuant to Penal Code "
        "section 290.46.",
    ),
    (
        "PARA",
        "11. Defendant SWIFT TRANSPORTATION CO. OF ARIZONA LLC ('Swift') is a "
        "limited liability company that does business as Swift Transportation. "
        "Its October 5, 2023 letter lists 2200 South 75th Avenue, Phoenix, "
        "Arizona 85043. On September 25, 2023, the FMCSA Clearinghouse "
        "identified the querying employer as SWIFT TRANSPORTATION CO OF "
        "ARIZONA LLC, USDOT number 54283. On information and belief, Swift "
        "is qualified to transact business in California and was the entity "
        "that recruited Plaintiff, ordered the reports, and made the "
        "employment decision challenged here.",
    ),
    (
        "PARA",
        "12. On information and belief, Swift's designated agent for service "
        "of process in California is National Registered Agents, Inc. "
        "Plaintiff will serve Swift through the agent listed on the California "
        "Secretary of State record as of the date of service. Service is not "
        "to be made at a terminal or recruiter's phone number merely because "
        "that is how Plaintiff first heard from Swift.",
    ),
    (
        "PARA",
        "13. The true names and capacities of DOES 1 through 20 are unknown to "
        "Plaintiff, who therefore sues them by fictitious names under Code of "
        "Civil Procedure section 474. DOES 1 through 10 include the consumer "
        "reporting agency, investigative consumer reporting agency, or other "
        "vendor that assembled, evaluated, furnished, or scored background "
        "information about Plaintiff for Swift — including, if discovery so "
        "shows, Asurint, Tenstreet, LLC, DriverIQ / Cisive, or Equifax "
        "Workforce Solutions — and the individuals who ordered, reviewed, or "
        "acted on that information. Plaintiff will amend when their identities "
        "and roles are ascertained.",
    ),
    (
        "PARA",
        "14. Robin Kaufman and Matt Hutto communicated with Plaintiff as "
        "Swift driver recruiters. They are percipient witnesses, not presently "
        "named as defendants. Matt Hutto's message used a Class A Recruiting "
        "address while stating it was sent on behalf of Swift Transportation "
        "Co. of Arizona LLC by Tenstreet, LLC.",
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
        "exceeds $35,000, exclusive of interest and costs. No specific "
        "personal-injury or punitive-damages amount is pleaded.",
    ),
    (
        "PARA",
        "18. This Court has personal jurisdiction over Swift because Swift "
        "recruited Plaintiff, a California resident, for work; caused "
        "consumer reports to be procured about a California resident; sent "
        "the pre-adverse and post-adverse communications to Plaintiff in "
        "California; and is, on information and belief, qualified to do "
        "business in California.",
    ),
    (
        "PARA",
        "19. Venue is proper in the County of San Joaquin under Code of Civil "
        "Procedure sections 395 and 395.5 because Plaintiff resides here, he "
        "received the recruiting, screening, and adverse-action "
        "communications here, and the liability and injury arose here.",
    ),
    (
        "PARA",
        "20. Plaintiff has not pleaded a federal claim. This Complaint is a "
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
        "22. The cause of action accrued, if at all, when Swift used registry "
        "information for purposes relating to Plaintiff's employment — that "
        "is, on the date of the employment decision, not on the date of "
        "application, and not on the date Plaintiff first registered under "
        "section 290.",
    ),
    (
        "PARA",
        "23. Swift's written post-adverse letter is dated October 5, 2023, "
        "at 5:09 a.m. Swift Recruiting emailed that letter the same day. "
        "Three years from October 5, 2023, is October 5, 2026. Swift "
        "Recruiting emailed a password-protected pre-adverse letter on "
        "September 26, 2023. Three years from that earlier date is September "
        "26, 2026. This Complaint is prepared for execution on September 8, "
        "2026, inside both dates. [PLAINTIFF MUST NOT DELAY PAST SEPTEMBER "
        "26, 2026 IF HE TREATS THE PRE-ADVERSE LETTER AS ACCRUAL.]",
    ),
    (
        "PARA",
        "24. Plaintiff does not concede that Code of Civil Procedure section "
        "335.1 or section 340, subdivision (a), supplies the limitations period "
        "for the section 290.46(j) count. He does not plead a Tameny or "
        "personal-injury count. A two-year clock from September 26 or "
        "October 5, 2023, would have closed in 2025. He has not pleaded the "
        "Fair Credit Reporting Act; the two-year FCRA discovery clock from "
        "those same 2023 letters would likewise have closed.",
    ),
    ("HEADER", "V.\nCOMMON FACTUAL ALLEGATIONS"),
    ("SUBHEAD", "A. The Swift Application"),
    (
        "PARA",
        "25. On Friday, September 22, 2023, at 3:02 p.m., Robin Kaufman, "
        "identifying herself as a Swift Transportation Driver Recruiter, "
        "emailed Plaintiff that she had received his information and asked "
        "him to complete the full application. The message was sent on "
        "behalf of Swift Transportation Co. of Arizona LLC by Tenstreet, LLC, "
        "120 W. 3rd Street, Tulsa, Oklahoma 74103. Her stated direct line was "
        "623-907-7414 and her address robin_kaufman@swifttrans.com.",
    ),
    (
        "PARA",
        "26. That same evening, at 10:03 p.m., Matt Hutto, also identifying "
        "himself as a Swift Driver Recruiter, emailed that he was trying to "
        "reach Plaintiff at the number Plaintiff had provided, asked him to "
        "complete the full driver application, and gave 803-564-3092 as a "
        "return number. The message used Mhutto@classarecruitinginc.com and "
        "was likewise sent on behalf of Swift Transportation Co. of Arizona "
        "LLC by Tenstreet, LLC.",
    ),
    (
        "PARA",
        "27. On information and belief, the application was for commercial "
        "driver or other safety-sensitive work requiring a commercial driver's "
        "license. The file does not contain the completed application, a "
        "written offer, a job title, or a rate of pay. "
        "[PLAINTIFF MUST CONFIRM THE ROLE, TERMINAL, AND WHETHER ANY OFFER "
        "WAS MADE BEFORE EXECUTION.]",
    ),
    ("SUBHEAD", "B. The September 25, 2023 Screen"),
    (
        "PARA",
        "28. On Monday, September 25, 2023, at 11:54 a.m., Tenstreet notified "
        "Plaintiff that a DriverIQ employment background document ordered in "
        "connection with Swift was available in Driver Pulse.",
    ),
    (
        "PARA",
        "29. Four minutes later, at 11:58 a.m., the FMCSA Office of Safety "
        "Programs emailed Plaintiff that SWIFT TRANSPORTATION CO OF ARIZONA "
        "LLC (USDOT# 54283) had requested access to his FMCSA Drug and "
        "Alcohol Clearinghouse record. The email warned that refusal would "
        "prohibit him from operating a commercial motor vehicle or performing "
        "other safety-sensitive functions for Swift.",
    ),
    (
        "PARA",
        "30. At 1:20 p.m. the same day, Tenstreet notified Plaintiff that his "
        "FMCSA Clearinghouse result ordered by Swift Transportation Co. of "
        "Arizona LLC was available for review. The decrypted pre-adverse "
        "packet includes a Clearinghouse result of Driver Not Prohibited, "
        "with no open violations.",
    ),
    (
        "PARA",
        "31. The Clearinghouse query is alleged as proof that Swift was then "
        "treating Plaintiff as a prospective commercial-driver hire and was "
        "running federally required safety screens. It is not alleged to be "
        "a Penal Code section 290.46 disclosure. Clearinghouse records "
        "concern drug and alcohol program violations, not Megan's Law.",
    ),
    ("SUBHEAD", "C. The Pre-Adverse and Post-Adverse Letters"),
    (
        "PARA",
        "32. On Tuesday, September 26, 2023, at 3:09 a.m., Swift Recruiting "
        "(recruitadmin@swifttrans.com) emailed Plaintiff a message titled "
        "'Swift Transportation - FCRA,' addressed to Brendan Ngehsi Ngwa "
        "Nforbi, stating that an important communication was attached as "
        "Pre_Adverse_Action_Letter_76326281-1916808-encrypted.pdf and that "
        "the password was the last four digits of his Social Security number.",
    ),
    (
        "PARA",
        "33. The pre-adverse attachment has been decrypted. It is a composite "
        "screening packet, not a blank cover letter. It includes completed "
        "criminal-file components returning Clear, an NSOPW component that "
        "remained Processing on every snapshot, a Clearinghouse result of "
        "Driver Not Prohibited, an MVR, PSP inspection history, and CDLIS "
        "license-identity information. Plaintiff does not republish "
        "identifiers from that packet in this pleading. He alleges the "
        "adjudication results as known facts.",
    ),
    (
        "PARA",
        "34. On Thursday, October 5, 2023, at 3:09 a.m., Swift Recruiting "
        "emailed Plaintiff a second 'Swift Transportation - FCRA' message, "
        "this time attaching Post_Adverse_Action_Letter_76326281-1916809_em.pdf.",
    ),
    (
        "PARA",
        "35. The enclosed letter is on Swift Transportation Co. of Arizona LLC "
        "letterhead, dated October 5, 2023, 5:09 a.m., and addressed to "
        "Brendan Ngehsi Nforbi at 1455 Cat Tail Drive, Stockton, California "
        "95204. It states that offers of employment at Swift are contingent "
        "upon successful completion of a background check, and that the "
        "letter 'serves as notification that we have decided not to employ "
        "you or have decided to take other adverse action based in whole or "
        "in part on a consumer report received from a consumer reporting "
        "agency.'",
    ),
    (
        "PARA",
        "36. The letter states that Asurint (Cleveland, Ohio), Tenstreet "
        "(Tulsa, Oklahoma), DriverIQ (Tulsa, Oklahoma; disputes at Cisive), "
        "FMCSA-DOT, and The Work Number / Equifax Workforce Solutions "
        "'provided us with consumer reports which, in whole or in part, "
        "influenced our employment decision.' It states those agencies "
        "played no part in the decision other than providing the reports.",
    ),
    (
        "PARA",
        "37. The October 5 letter says a copy of the consumer report and a "
        "Summary of Rights were attached. The decrypted September 26 packet "
        "is the report-side paper in Plaintiff's files. It does not contain "
        "a completed NSOPW result, a California Sex Offender Registry source "
        "line, or a separate later Asurint, Tenstreet, or DriverIQ printout "
        "showing a registry hit. Civil Code sections 1786.10 and 1786.22 "
        "entitle Plaintiff to inspect the files those agencies maintain on "
        "him. Plaintiff has not yet served those inspection requests. He will.",
    ),
    (
        "PARA",
        "38. The California disclosure in that packet states that Swift may "
        "order a consumer report or investigative consumer report including "
        "'federal criminal history, state criminal history, [and] public "
        "court records,' and names the same agencies. Criminal-history and "
        "court-record searches are not this claim. This claim is the use of "
        "information disclosed pursuant to Penal Code section 290.46.",
    ),
    ("SUBHEAD", "D. Facts Supporting the Registry-Use Inference"),
    (
        "PARA",
        "39. Plaintiff is a person as to whom information is disclosed on the "
        "California Megan's Law website. That website, and the statute that "
        "created it, warn that the information may not be used for employment.",
    ),
    (
        "PARA",
        "40. Swift is a national motor carrier. On information and belief, it "
        "maintains written background-screening policies for driver applicants, "
        "contracts with the agencies named in its October 5 letter, and "
        "adjudicates hits through a centralized process rather than by ad hoc "
        "decision of a single recruiter.",
    ),
    (
        "PARA",
        "41. On information and belief, the ordinary Swift driver screen in "
        "2023 included a search, or caused a vendor to search, sex-offender "
        "registry or Department of Justice public-notification sources, "
        "including sources that republish or are derived from California "
        "Penal Code section 290.46 disclosures.",
    ),
    (
        "PARA",
        "42. The July 2024 First Advantage / UPS report is alleged for three "
        "limited purposes: it shows that Plaintiff's registry status was "
        "commercially retrievable for employment screening; it shows that at "
        "least one national CRA treated a California-registry source as an "
        "employment-eligibility bar for this Plaintiff; and it identifies the "
        "kind of record Swift's vendors would have been able to return. "
        "Plaintiff does not allege that First Advantage was Swift's vendor, "
        "and does not allege that UPS sent its report to Swift.",
    ),
    (
        "PARA",
        "43. The NSOPW component was still Processing. A search that never "
        "completed is not a completed 'no record' result. It is also not a "
        "completed printed hit. Plaintiff is informed and believes, and on "
        "that basis alleges, that Swift or a DOE obtained, displayed, "
        "scored, or was informed of preliminary information from that "
        "in-process NSOPW component citing a sex-offender registry — "
        "including information disclosed pursuant to Penal Code section "
        "290.46 or a derivative national compilation whose source of record "
        "was the California registry — and used that preliminary information "
        "in whole or in part in the October 5, 2023 decision.",
    ),
    (
        "PARA",
        "44. The basis for paragraph 43 is the combination of: Swift ordered "
        "an NSOPW sex-offender-website search; that component remained "
        "Processing on every snapshot in the packet sent with the "
        "pre-adverse notice; Swift then denied employment based in whole or "
        "in part on consumer reports; the completed criminal, Clearinghouse, "
        "and MVR components that are in the packet do not themselves "
        "explain a registry-based denial; Plaintiff was then listed on the "
        "California Megan's Law website; commercial screeners had already "
        "shown they could match this Plaintiff to the California registry; "
        "and the interim NSOPW return, adjudication notes, and "
        "decision-maker communications are exclusively in Defendants' "
        "possession.",
    ),
    (
        "PARA",
        "45. Swift admitted in writing that consumer reports caused the "
        "denial. It took that action while a sex-offender-website component "
        "remained Processing. It did not, in the October 5 letter, identify "
        "the specific item that caused the denial or supply a completed "
        "NSOPW result. Civil Code section 1786.40 required advice that an "
        "investigative consumer report had been obtained and the agency's "
        "name and address at denial. The letter names agencies. It does "
        "not advise that an investigative consumer report containing an "
        "incomplete NSOPW had been obtained, and it does not supply a "
        "complete copy of every component. The ICRAA and UCL counts rest "
        "on that notice and completeness failure even if the preliminary-"
        "registry-use inference later fails.",
    ),
    (
        "PARA",
        "46. Alternative explanations — a failed Clearinghouse or drug-and-"
        "alcohol result, a driving-record or crash disqualification, a "
        "lawful criminal-history adjudication under a statute that actually "
        "authorizes the use, a CDL defect, or a withdrawal of the application "
        "— can be tested against a discrete set of records. Plaintiff will "
        "seek the application file, the Asurint, Tenstreet, and DriverIQ "
        "reports, the Clearinghouse and PSP results, adjudication notes, and "
        "communications of the decision-maker.",
    ),
    (
        "PARA",
        "47. Lerma v. Amazon.com Services, LLC, C.D. Cal. No. 8:22-cv-01727, "
        "Dkt. 36, dismissed a Megan's Law count after the employer's report "
        "was in the record and showed ordinary court records and a completed "
        "national sex-offender search returning no record. This packet is "
        "not that report. The NSOPW component never completed. A demurrer "
        "may take the printed snapshots as what Plaintiff has pleaded them "
        "to be. It cannot convert an incomplete NSOPW into Lerma's completed "
        "no-record search, and it cannot decide — without the adjudication "
        "log — whether Swift used preliminary registry information from that "
        "in-process component. Defendants may not obtain a pleading-stage "
        "dismissal by withholding the interim NSOPW return and the "
        "decision-maker file. If production shows a completed NSOPW "
        "returning no record and no preliminary registry use, the Penal "
        "Code count will stand or fall on that file — after production, "
        "not by assuming it now.",
    ),
    (
        "PARA",
        "48. The use was not to protect a person at risk within the meaning of "
        "section 290.46(j)(1). A general commercial-driver assignment is not, "
        "without more, the narrow authorization that subdivision (j)(1) "
        "describes. FMCSA authorization to query the Clearinghouse or PSP is "
        "not authorization to use Megan's Law website information. Swift has "
        "the burden of proving any other statutory authorization as a defense.",
    ),
    ("SUBHEAD", "E. Knowledge, Concealment, and Harm"),
    (
        "PARA",
        "49. Swift knew or should have known that employment use of Megan's "
        "Law information is prohibited. The registry website displays that "
        "warning. Swift is a sophisticated interstate carrier with dedicated "
        "compliance and screening functions. On information and belief, its "
        "vendor contracts and adjudication guides address or should address "
        "California registry restrictions.",
    ),
    (
        "PARA",
        "50. On information and belief, Swift did not identify the registry, "
        "or any other specific ground, as the basis for the decision. The "
        "October 5 letter names agencies, not hits. That omission deprived "
        "Plaintiff of a meaningful opportunity to inspect the source, dispute "
        "a mismatch, and invoke the statutory remedies before the decision "
        "became final.",
    ),
    (
        "PARA",
        "51. As a result of the decision, Plaintiff lost the Swift employment "
        "opportunity, including the wages and benefits of that position, "
        "according to proof and subject to mitigation. He also suffered "
        "emotional distress, humiliation, and anxiety from an unexplained "
        "denial he is informed and believes rested on a status the Legislature "
        "has forbidden employers to use. [PLAINTIFF MUST CONFIRM WHETHER ANY "
        "WAGES WERE EARNED AND ANY REPLACEMENT WORK BEFORE EXECUTION.]",
    ),
    (
        "PARA",
        "52. Plaintiff has sought and continues to seek replacement employment "
        "and does not claim a guaranteed lifetime expectancy from an unaccepted "
        "driver application. Economic damages will be limited to losses proven "
        "with reasonable certainty and without double recovery against other "
        "dockets that arise from different employers and different decisions.",
    ),
    ("HEADER", "VI.\nFIRST CAUSE OF ACTION"),
    (
        "SUBHEAD",
        "Unauthorized Employment Use of Registry Information\n"
        "Penal Code section 290.46(j) — Against All Defendants\n"
        "(Pleaded on Information and Belief — Preliminary NSOPW / Registry Use)",
    ),
    (
        "PARA",
        "53. Plaintiff realleges paragraphs 1 through 52, except allegations "
        "expressly pleaded in the alternative are incorporated only to the "
        "extent consistent with this cause.",
    ),
    (
        "PARA",
        "54. Penal Code section 290.46(j)(1) authorizes use of information "
        "disclosed under that section only to protect a person at risk, except "
        "as otherwise authorized by law. Section 290.46(j)(2)(E) prohibits use "
        "of that information for purposes relating to employment unless another "
        "law authorizes the use.",
    ),
    (
        "PARA",
        "55. Section 290.46(j)(4)(A) makes the user liable for the actual "
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
        "56. On information and belief, Swift, and such DOE Defendants as "
        "ordered, furnished, scored, or acted on the report, used "
        "preliminary information from the still-Processing NSOPW component "
        "citing a sex-offender registry — including information disclosed "
        "pursuant to section 290.46 concerning Plaintiff — in whole or in "
        "part in the employment decision. Plaintiff does not allege that "
        "the printed snapshots contain a completed NSOPW hit or the words "
        "'SOURCE OF RECORD: CALIFORNIA SEX OFFENDER REGISTRY.' The use "
        "alleged is the use of preliminary registry information from that "
        "in-process component.",
    ),
    (
        "PARA",
        "57. The use related directly to employment: it concerned the Swift "
        "driver application and the October 5, 2023 decision not to employ "
        "Plaintiff. The use was not authorized by section 290.46(j)(1) or by "
        "any other provision of law applicable to that application. "
        "Defendants knew or should have known that employment use was "
        "prohibited. The use was a substantial factor in the decision and "
        "caused the loss and injury alleged.",
    ),
    (
        "PARA",
        "58. Plaintiff seeks the remedies authorized by section 290.46(j)(4)(A) "
        "and preventive relief under subdivision (j)(4)(B) to restrain any "
        "pattern or practice of employment use of Megan's Law information in "
        "Swift's California recruiting and hiring.",
    ),
    ("HEADER", "VII.\nSECOND CAUSE OF ACTION"),
    (
        "SUBHEAD",
        "California Investigative Consumer Reporting Agencies Act\n"
        "Civil Code sections 1786.40 and 1786.50 — Against Swift and User DOES\n"
        "(Load-Bearing Count)",
    ),
    (
        "PARA",
        "59. Plaintiff realleges paragraphs 1 through 52 and 56 through 57 to "
        "the extent consistent with this cause.",
    ),
    (
        "PARA",
        "60. On information and belief, one or more of the agencies Swift "
        "named assembled or evaluated information concerning Plaintiff's "
        "character, general reputation, personal characteristics, or mode of "
        "living for employment purposes at Swift's request, and Swift was the "
        "user of that information before the October 5, 2023 decision.",
    ),
    (
        "PARA",
        "61. Civil Code section 1786.40(a) required Swift, under circumstances "
        "in which employment was denied and an investigative consumer report "
        "had been obtained, to advise Plaintiff of that fact and supply the "
        "agency's name and address. Swift's October 5 letter names agencies. "
        "It does not advise that an investigative consumer report containing "
        "an incomplete NSOPW component had been obtained. It does not "
        "identify which component caused the denial.",
    ),
    (
        "PARA",
        "62. The decrypted packet is not a complete investigative consumer "
        "report. NSOPW remained Processing. Plaintiff was denied while that "
        "component was unfinished. Civil Code sections 1786.10 and 1786.22 "
        "entitle him to inspect the files Asurint, Tenstreet, DriverIQ, and "
        "any other ICRA maintains on him. He has not yet served those "
        "requests. He will.",
    ),
    (
        "PARA",
        "63. This ICRAA count does not depend on proving Penal Code section "
        "290.46(j). A notice or completeness failure under Civil Code "
        "section 1786.40 is independently actionable if an investigative "
        "consumer report was obtained and employment was denied without the "
        "required advice and a complete source. That count can reach "
        "discovery even if the section 290.46(j) count later fails.",
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
        "amendment if production shows a timely FCRA claim and a notice or "
        "copy defect that the 2023 letters did not cure. He also reserves "
        "amendment under Civil Code section 1786.16 if production shows Swift "
        "procured an investigative report before the required standalone "
        "disclosure and written authorization.",
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
        "67. Defendants engaged in unlawful practices by violating Civil Code "
        "section 1786.40 and, if proven, Penal Code section 290.46(j). They "
        "engaged in unfair practices by taking "
        "adverse action on consumer reports while a sex-offender-website "
        "component remained Processing, naming agencies without identifying "
        "the item that caused the denial, and withholding a complete "
        "investigative-consumer-report file.",
    ),
    (
        "PARA",
        "68. Plaintiff suffered injury in fact and lost money or property "
        "through the lost Swift employment opportunity and other economic "
        "losses to be proven. He does not seek future unearned wages as UCL "
        "restitution. He seeks restitution only of money or property in which "
        "he had a vested interest and that Defendants acquired or caused him "
        "to lose through the challenged practices.",
    ),
    (
        "PARA",
        "69. Legal damages are not an adequate remedy for Defendants' "
        "retention, use, and dissemination of registry-derived screening data "
        "or their ongoing employment-screening practices. Plaintiff seeks an "
        "injunction requiring Defendants to cease prohibited employment use of "
        "California registry information in California recruiting; preserve "
        "and disclose the source and audit trail of Plaintiff's screening; "
        "and correct or segregate unlawfully used data, together with "
        "restitution and declaratory relief ancillary to the injunction under "
        "Business and Professions Code section 17203.",
    ),
    ("HEADER", "IX.\nPRESERVATION OF EVIDENCE"),
    (
        "PARA",
        "70. Defendants are on notice to preserve Plaintiff's complete Swift "
        "and Tenstreet application file; recruiter communications of Kaufman "
        "and Hutto; the Asurint, Tenstreet, DriverIQ, Clearinghouse, PSP, and "
        "Equifax / Work Number orders, reports, component searches, "
        "adjudication, access, and cancellation logs; the decrypted September "
        "26, 2023 pre-adverse packet; and policies governing Megan's Law, "
        "FCRA, ICRAA, and driver adjudication in 2023.",
    ),
    (
        "PARA",
        "71. Relevant electronically stored information includes applicant-"
        "tracking and Driver Pulse audit fields, event timestamps, reason "
        "codes, report-view logs, emails, chats, SMS, and data-retention "
        "records from September 1, 2023 through December 31, 2023, and any "
        "later date on which the employment decision was recorded or revisited.",
    ),
    (
        "PARA",
        "72. The July 2024 First Advantage/UPS report is relevant to "
        "retrievability and matching methodology. It is not a substitute for "
        "Swift's own file.",
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
        CAPTION_LEFT, CAPTION_RIGHT, caption_size=8.2, tight_lh=10.5, boxed=True
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
