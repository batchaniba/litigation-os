# -*- coding: utf-8 -*-
#!/usr/bin/env python3
"""
Matter 32 -- Plaintiff's Opposition to Defendants' Motion to Dismiss FAC and
Motion to Strike (ECF 22), on portfolio pleading paper, with the universal
signature affixed.

  python3 internal/scripts/matter32-opposition-mtd-pleading.py

DRAFT v2 (Oct. 27, 2026). Not filed or served. Pins listed in
internal/private/research/matter-32/11-opposition-filing-draft/REVIEW-NOTES.md
must clear Westlaw before filing.

Drafting boundary: the brief argues only from ECF 5 (the FAC). It does not
attach or describe the dashcam video, the transcript, the warrant affidavit,
the CHP 202 / DS-367, or the toxicology report, and it does not discuss the
sequence of the E.D. Cal. and Alameda dismissals.
"""

from __future__ import annotations

import os
import re
import sys
from pathlib import Path

SCRIPT_DIR = Path(__file__).resolve().parent
sys.path.insert(0, str(SCRIPT_DIR / "lib"))
sys.path.insert(0, str(SCRIPT_DIR))

from pleading_paper import (  # noqa: E402
    CONTENT_LEFT, CONTENT_RIGHT, CONTENT_WIDTH, PleadingPaper,
)
from signature_stamp import SIGNATURE_PATH, SIGNATURE_NATIVE_PX  # noqa: E402

REPO_ROOT = SCRIPT_DIR.parent.parent
OUT_DIR = REPO_ROOT / "internal" / "private" / "research" / "matter-32" / "11-opposition-filing-draft"
OUT_PATHS = [OUT_DIR / "Opposition to MTD (ECF 22) - Pleading Paper - DRAFT v2 (Oct 27 2026).pdf"]
TEXT_OUT = OUT_DIR / "opposition-text-draft-v2.md"
SCRATCH_DIR = Path(
    "/tmp/claude-0/-home-user-interactive-litigation-portfolio/"
    "5d8752f5-0059-5673-9c7e-bba513c7c835/scratchpad"
)

# Docket name in this action is "Brendan Ngwa Nforbi" (FAC ¶ 35 ties it to
# "Brendan Ngehsi Newanforbi"). Change here if the caption name is conformed.
PLAINTIFF_NAME = "BRENDAN NGWA NFORBI"
SIGN_DATE = "November ___, 2026"

DOC_TITLE_FOOTER = (
    "PL.'S OPP. TO MOT. TO DISMISS FAC AND STRIKE -- NFORBI v. MEZA-GONZALEZ "
    "(No. 4:26-cv-08271-ASK) -- DRAFT v2, NOT FILED"
)
COURT_LINE1 = "UNITED STATES DISTRICT COURT"
COURT_LINE2 = "NORTHERN DISTRICT OF CALIFORNIA"

SIG_IMG_W_PX, SIG_IMG_H_PX = SIGNATURE_NATIVE_PX
SIG_WIDTH = 235
SIG_RIGHT_OFFSET = 28
SIG_HEIGHT_SCALE = 1.25

ATTORNEY_BLOCK = [
    (PLAINTIFF_NAME, "Times-Bold", 12),
    ("Plaintiff, In Pro Per", "Times-Roman", 12),
    ("1455 Cat Tail Drive", "Times-Roman", 12),
    ("Stockton, CA 95204", "Times-Roman", 12),
    ("Telephone: (209) 801-4442", "Times-Roman", 12),
    ("E-mail: bnn.cdl@gmail.com", "Times-Roman", 12),
]

CAPTION_LEFT = [
    (PLAINTIFF_NAME + ",", True, False),
    ("", False, False),
    ("                          Plaintiff,", False, False),
    ("", False, False),
    ("       v.", False, False),
    ("", False, False),
    ("SANTIAGO MEZA-GONZALEZ (CHP Badge", True, False),
    ("#023295), in his individual capacity;", True, False),
    ("JOSE MELANO (CHP Badge #023054), in", True, False),
    ("his individual capacity; and DOES 1", True, False),
    ("through 10, inclusive,", True, False),
    ("", False, False),
    ("                          Defendants.", False, False),
    ("", False, False),
]

CAPTION_RIGHT = [
    ("Case No. 4:26-cv-08271-ASK", False, False),
    ("", False, False),
    ("PLAINTIFF'S OPPOSITION TO", True, False),
    ("DEFENDANTS' MOTION TO DISMISS", True, False),
    ("FIRST AMENDED COMPLAINT AND", True, False),
    ("MOTION TO STRIKE (ECF 22)", True, False),
    ("", False, False),
    ("Date: December 9, 2026", False, False),
    ("Time: 1:30 p.m.", False, False),
    ("Courtroom: 4", False, False),
    ("Judge: Hon. Ajay S. Krishnan", False, False),
    ("(as noticed; reassignment pending)", False, False),
]

HEARING_LINE = (
    "Hearing as noticed by Defendants: December 9, 2026, at 1:30 p.m., Courtroom 4, "
    "1301 Clay Street, Oakland, before the Honorable Ajay S. Krishnan. Defendants have "
    "declined magistrate-judge jurisdiction (ECF 23), and the hearing may be reset upon "
    "reassignment."
)

# ----------------------------------------------------------------------------
# Authorities: (category, display, regex that finds it in body text)
# ----------------------------------------------------------------------------
AUTHORITIES = [
    ("Cases", "Akhtar v. Mesa, 698 F.3d 1202 (9th Cir. 2012)", r"Akhtar"),
    ("Cases", "Arizona v. Hicks, 480 U.S. 321 (1987)", r"Hicks"),
    ("Cases", "Ashcroft v. Iqbal, 556 U.S. 662 (2009)", r"Iqbal"),
    ("Cases", "Bell Atlantic Corp. v. Twombly, 550 U.S. 544 (2007)", r"Twombly"),
    ("Cases", "Bostock v. Clayton County, 590 U.S. 644 (2020)", r"Bostock"),
    ("Cases", "Brigham City v. Stuart, 547 U.S. 398 (2006)", r"Brigham City"),
    ("Cases", "Caldwell v. City & County of San Francisco, 889 F.3d 1105 (9th Cir. 2018)", r"Caldwell"),
    ("Cases", "Chism v. Washington State, 661 F.3d 380 (9th Cir. 2011)", r"Chism"),
    ("Cases", "Costanich v. Department of Social & Health Services, 627 F.3d 1101 (9th Cir. 2010)", r"Costanich"),
    ("Cases", "Devenpeck v. Alford, 543 U.S. 146 (2004)", r"Devenpeck"),
    ("Cases", "District of Columbia v. Wesby, 583 U.S. 48 (2018)", r"Wesby"),
    ("Cases", "Galbraith v. County of Santa Clara, 307 F.3d 1119 (9th Cir. 2002)", r"Galbraith"),
    ("Cases", "Garity v. APWU National Labor Organization, 828 F.3d 848 (9th Cir. 2016)", r"Garity"),
    ("Cases", "Grier v. Finjan Holdings, Inc., No. 21-16702 (9th Cir. Jan. 20, 2023)", r"Grier"),
    ("Cases", "Hebbe v. Pliler, 627 F.3d 338 (9th Cir. 2010)", r"Hebbe"),
    ("Cases", "Hopkins v. Bonvicino, 573 F.3d 752 (9th Cir. 2009)", r"Hopkins"),
    ("Cases", "Kay v. Ehrler, 499 U.S. 432 (1991)", r"Kay v\. Ehrler"),
    ("Cases", "Keates v. Koile, 883 F.3d 1228 (9th Cir. 2018)", r"Keates"),
    ("Cases", "Khoja v. Orexigen Therapeutics, Inc., 899 F.3d 988 (9th Cir. 2018)", r"Khoja"),
    ("Cases", "Knowles v. Iowa, 525 U.S. 113 (1998)", r"Knowles"),
    ("Cases", "Liston v. County of Riverside, 120 F.3d 965 (9th Cir. 1997)", r"Liston"),
    ("Cases", "Lopez v. Smith, 203 F.3d 1122 (9th Cir. 2000) (en banc)", r"Lopez v\. Smith"),
    ("Cases", "Michigan v. Fisher, 558 U.S. 45 (2009) (per curiam)", r"Fisher"),
    ("Cases", "Mincey v. Arizona, 437 U.S. 385 (1978)", r"Mincey"),
    ("Cases", "Nieves v. Bartlett, 587 U.S. 391 (2019)", r"Nieves"),
    ("Cases", "Smith v. Wade, 461 U.S. 30 (1983)", r"Smith v\. Wade"),
    ("Cases", "Starr v. Baca, 652 F.3d 1202 (9th Cir. 2011)", r"Starr"),
    ("Cases", "United States v. Jones, 565 U.S. 400 (2012)", r"United States v\. Jones"),
    ("Cases", "United States v. Lopez, 482 F.3d 1067 (9th Cir. 2007)", r"United States v\. Lopez|Lopez, 482"),
    ("Cases", "United States v. Ngumezi, 980 F.3d 1285 (9th Cir. 2020)", r"Ngumezi"),
    ("Cases", "United States v. Prescott, 581 F.2d 1343 (9th Cir. 1978)", r"Prescott"),
    ("Cases", "United States v. Rodgers, 656 F.3d 1023 (9th Cir. 2011)", r"Rodgers"),
    ("Cases", "United States v. Snipe, 515 F.3d 947 (9th Cir. 2008)", r"Snipe"),
    ("Cases", "United States v. Stanert, 762 F.2d 775 (9th Cir. 1985)", r"Stanert"),
    ("Cases", "Whittlestone, Inc. v. Handi-Craft Co., 618 F.3d 970 (9th Cir. 2010)", r"Whittlestone"),
    ("Cases", "Zamani v. Carnes, 491 F.3d 990 (9th Cir. 2007)", r"Zamani"),
    ("Statutes and Rules", "42 U.S.C. § 1983", r"§ 1983|section 1983"),
    ("Statutes and Rules", "42 U.S.C. § 1988", r"§ 1988"),
    ("Statutes and Rules", "Cal. Veh. Code § 21718", r"21718"),
    ("Statutes and Rules", "Cal. Veh. Code § 23612", r"23612"),
    ("Statutes and Rules", "Fed. R. Civ. P. 12(b)(6)", r"12\(b\)\(6\)"),
    ("Statutes and Rules", "Fed. R. Civ. P. 12(f)", r"12\(f\)"),
    ("Statutes and Rules", "Fed. R. Civ. P. 15(a)(2)", r"15\(a\)\(2\)"),
]

CASE_ITALICS = sorted(
    [
        "Akhtar v. Mesa", "Arizona v. Hicks", "Ashcroft v. Iqbal", "Bostock v. Clayton County",
        "Brigham City v. Stuart", "Caldwell v. City & County of San Francisco",
        "Chism v. Washington State", "Costanich v. Dep't of Soc. & Health Servs.",
        "Devenpeck v. Alford", "District of Columbia v. Wesby",
        "Galbraith v. County of Santa Clara", "Garity v. APWU Nat'l Lab. Org.",
        "Grier v. Finjan Holdings, Inc.", "Hebbe v. Pliler", "Hopkins v. Bonvicino",
        "Kay v. Ehrler", "Keates v. Koile", "Khoja v. Orexigen Therapeutics, Inc.",
        "Knowles v. Iowa", "Liston v. County of Riverside", "Lopez v. Smith",
        "Michigan v. Fisher", "Mincey v. Arizona", "Nieves v. Bartlett", "Smith v. Wade",
        "Starr v. Baca", "United States v. Jones", "United States v. Lopez",
        "United States v. Ngumezi", "United States v. Prescott", "United States v. Rodgers",
        "United States v. Snipe", "United States v. Stanert",
        "Whittlestone, Inc. v. Handi-Craft Co.", "Zamani v. Carnes",
        "Bell Atlantic Corp. v. Twombly", "Bureerong v. Uvawas", "Wilkerson v. Butler",
        "Newanforbi v. Serrato",
        "Akhtar", "Hicks", "Iqbal", "Twombly", "Brigham City", "Caldwell", "Chism",
        "Costanich", "Devenpeck", "Wesby", "Galbraith", "Grier", "Hebbe", "Hopkins",
        "Keates", "Khoja", "Knowles", "Fisher", "Mincey", "Nieves", "Starr", "Lopez",
        "Ngumezi", "Prescott", "Snipe", "Whittlestone", "Zamani", "Bostock",
        "Id.", "id.", "See", "see", "See also", "a fortiori",
    ],
    key=len, reverse=True,
)


def italicize_cases(text: str) -> str:
    out = text
    for name in CASE_ITALICS:
        pattern = re.compile(r"(?<![A-Za-z<:])" + re.escape(name) + r"(?![A-Za-z])")
        parts = re.split(r"(<<[bi]{1,2}:[^>]+>>)", out)
        rebuilt = []
        for part in parts:
            if part.startswith("<<"):
                rebuilt.append(part)
            else:
                rebuilt.append(pattern.sub(f"<<i:{name}>>", part))
        out = "".join(rebuilt)
    return out


H, S, S2, P, L = "HEADER", "SUBHEAD", "SUBSUB", "PARA", "LIST"

CONTENT = [
    (H, "MEMORANDUM OF POINTS AND AUTHORITIES"),
    (H, "I. INTRODUCTION"),
    (P, "Defendants ask the Court to dismiss, with prejudice, a First Amended Complaint (\"FAC\") that describes a roadside encounter minute by minute using timestamps from the officers' own dashcam. They do not show that the FAC's facts, accepted as true, fail to state a claim. Instead, they replace those facts with their own. They call Plaintiff \"unconscious\" where the FAC alleges he was resting after pulling off the road. They treat contested entries in Defendant Meza-Gonzalez's reports as established. They offer a \"simple explanation\" for discrepancies the FAC alleges. And they treat the FAC's silence about field sobriety results as an admission of results the FAC never pleads. Rule 12(b)(6) permits none of that."),
    (P, "The motion also misstates the governing law. It never addresses United States v. Ngumezi, 980 F.3d 1285 (9th Cir. 2020), which holds that an officer who opens a car door and leans inside conducts a search that requires probable cause or another particularized justification. That is the conduct alleged in Count IV. Defendants defend the entry with an emergency-aid theory that no pleaded fact supports, and with a parking-infraction theory that would not authorize a vehicle search even if an infraction were established. And they invoke Rule 12(f) to strike punitive damages, a use the Ninth Circuit has squarely rejected. Whittlestone, Inc. v. Handi-Craft Co., 618 F.3d 970, 974-75 (9th Cir. 2010)."),
    (P, "Plaintiff opposes the motion as to Counts I, III, IV, and V and as to the punitive-damages request. To narrow the issues, Plaintiff does not oppose dismissal of Counts II and VI without prejudice and with leave to amend, and he confirms that he does not seek attorney's fees for his own work as a self-represented litigant. If the Court finds any other claim deficient, Plaintiff requests leave to amend and identifies below the specific amendments he would make."),

    (H, "II. STATEMENT OF ISSUES TO BE DECIDED"),
    (P, "1. Whether Counts IV and V state Fourth Amendment claims where the FAC alleges that Defendant Melano opened a closed passenger door, entered the vehicle, and seized and examined a cup, without a warrant, consent, or any objectively observable emergency."),
    (P, "2. Whether Count III states a claim for arrest without probable cause where Defendants' contrary theory depends on facts the FAC does not plead and on report entries the FAC specifically disputes."),
    (P, "3. Whether Count I states a judicial-deception claim, and whether materiality can be decided against Plaintiff when the warrant application is not before the Court."),
    (P, "4. Whether qualified immunity supports dismissal at the pleading stage on Defendants' generalized showing."),
    (P, "5. Whether Rule 12(f) authorizes striking a request for punitive damages."),
    (P, "6. Whether any dismissal should be with leave to amend."),

    (H, "III. FACTS ALLEGED IN THE FAC"),
    (P, "On the night of October 31 to November 1, 2024, Plaintiff, a Class A commercial driver, became fatigued while driving east on Interstate 580. He left the travel lanes, parked on the right shoulder near the Isabel Avenue exit in Livermore, and rested in the driver's seat. FAC ¶¶ 1, 7, 11-12. No officer saw him drive. Id. ¶ 11."),
    (P, "At 00:54:36, the dashcam of a California Highway Patrol car occupied by Defendants Meza-Gonzalez and Melano began recording as the patrol car stopped behind Plaintiff's car. Id. ¶ 13. Before approaching, Melano remarked, \"It's a rental. Huh.\" Id. ¶ 14. The officers walked up and shined flashlights through the windows. Id. Melano said, \"It wasn't here earlier when we passed by,\" and then, referring to a cup visible through a window, \"I think it's booze.\" Id. ¶¶ 14-15. Melano formed that hypothesis before either officer had spoken to Plaintiff or observed anything about his condition. Id. ¶ 15."),
    (P, "At 00:56:43, Melano opened the front passenger door. Id. ¶ 16. Plaintiff had not consented, and there was no warrant. Id. The car was intact and undamaged; there was no smoke, fire, or crash debris; and Plaintiff was in a normal resting posture. Id. ¶ 56. No emergency was articulated on the recording. Id. ¶¶ 16, 56."),
    (P, "Between 00:58:49 and 00:59:07, Melano reached into the car, removed the cup from the console area, smelled it, and announced: \"Is it water? No this is piss. This is pee.\" Id. ¶¶ 17, 60. The officers did not end the encounter. Id. ¶ 19. They ordered Plaintiff out onto uneven ground and administered field sobriety exercises; Melano acknowledged on the recording that the ground was unsuitable and declined to administer certain balance exercises for that reason. Id. Throughout, Plaintiff spoke coherently. He spelled his surname, discussed the mechanical design of the rental car, explained commercial-driver fatigue protocols, and correctly identified his location as Livermore. Id. ¶ 20."),
    (P, "At 01:10:54, Meza-Gonzalez told Plaintiff that the preliminary alcohol screening (\"PAS\") test was voluntary: \"You're not required to do this.\" Id. ¶ 21. Nine seconds later he added: \"If you choose to not consent to it, then it'll be up to my discretion whether I put you under arrest for DUI or not.\" Id. ¶ 22. Plaintiff declined. Id. ¶ 23. Meza-Gonzalez arrested him seconds later, with no new observation in between. Id. ¶ 24."),
    (P, "Meza-Gonzalez then executed sworn documents that were used to obtain a warrant for a compelled blood draw. Id. ¶¶ 25, 29, 40. The FAC alleges that those documents described Plaintiff's speech as \"slurred\" and described him as \"very confused and disoriented,\" descriptions the FAC alleges the recording contradicts. Id. ¶ 26(b)-(c). It alleges that the documents omitted that the suspected alcohol had been identified as urine, that certain exercises were not administered because of the ground, that the PAS had been described as voluntary, and that no officer had seen Plaintiff drive. Id. ¶¶ 27, 30. Plaintiff's blood was drawn by force under the warrant, and he was booked into Santa Rita Jail. Id. ¶¶ 29, 31. Four days later, CHP issued a Penal Code section 851.6 certificate describing the event as \"a detention only, not an arrest.\" Id. ¶ 32. The District Attorney filed no charges. Id. ¶ 34."),

    (H, "IV. LEGAL STANDARD"),
    (P, "A complaint survives Rule 12(b)(6) if it pleads \"factual content that allows the court to draw the reasonable inference that the defendant is liable for the misconduct alleged.\" Ashcroft v. Iqbal, 556 U.S. 662, 678 (2009). The Court accepts well-pleaded facts as true and draws reasonable inferences in the plaintiff's favor. Id.; Bell Atlantic Corp. v. Twombly, 550 U.S. 544, 555-56 (2007). When the defendant and the plaintiff each advance a plausible explanation, the complaint survives. Starr v. Baca, 652 F.3d 1202, 1216 (9th Cir. 2011). A self-represented plaintiff's pleading is construed liberally. Hebbe v. Pliler, 627 F.3d 338, 342 (9th Cir. 2010)."),
    (P, "Defendants attached no exhibit and requested no judicial notice. Even when a document is incorporated by reference, \"it is improper to assume the truth of an incorporated document if such assumptions only serve to dispute facts stated in a well-pleaded complaint.\" Khoja v. Orexigen Therapeutics, Inc., 899 F.3d 988, 1003 (9th Cir. 2018). And when specific facts alleged in a complaint contradict specific facts recited in a document that is not legally operative, \"the conflict is resolved in the plaintiff's favor.\" Grier v. Finjan Holdings, Inc., No. 21-16702, slip op. at 7-8 n.1 (9th Cir. Jan. 20, 2023) (citing Khoja, 899 F.3d at 1003). A police report is not a legally operative document."),

    (H, "V. ARGUMENT"),
    (S, "A. The Motion Rests on Facts the FAC Does Not Plead and on Inferences Drawn Against Plaintiff."),
    (P, "The motion's method is to recast the FAC. Four examples illustrate the problem."),
    (L, "Defendants describe Plaintiff as \"unconscious.\" Mot. 2:8, 3:13, 8:8. The FAC alleges that he was resting in the driver's seat, in a normal resting posture, after pulling off the road because he was tired. FAC ¶¶ 11, 16, 56."),
    (L, "Defendants offer \"[t]he simple explanation\" and \"[a]nother possibility\" for discrepancies between Meza-Gonzalez's sworn statements and the recording. Mot. 6:4-11. Choosing between competing explanations is fact-finding. Starr, 652 F.3d at 1216."),
    (L, "Defendants rely on \"slurred speech and other signs of intoxication\" as established facts. Mot. 10:1-3, 10:13. Those are the report entries the FAC alleges the recording contradicts. FAC ¶¶ 20, 26(b)-(c). Accepting them as true would use a disputed document to defeat the pleading, which Khoja forbids. 899 F.3d at 1003."),
    (L, "Defendants call the FAC \"conspicuously silent\" about field sobriety results and treat that silence as though it established adverse results. Mot. 6:27-28; see id. at 10:21-24. A complaint need not plead the defendant's evidence, and the absence of an allegation is not an admission."),
    (P, "Defendants also misattribute the FAC's facts. The motion states that \"Officer Gonzalez determines that the cup in Plaintiff's vehicle is filled not with booze, but with urine.\" Mot. 10:4-5. The FAC alleges that Melano made that identification. FAC ¶ 17. These are not technicalities. Each one converts a disputed or misread fact into a premise for dismissal."),

    (S, "B. Count IV States a Claim for Unlawful Warrantless Entry."),
    (S2, "1. Opening the passenger door was a search."),
    (P, "Officers who lack \"probable cause or any other particularized justification, such as a reasonable belief that the driver poses a danger,\" may not \"open the door to a vehicle and lean inside.\" United States v. Ngumezi, 980 F.3d 1285, 1288-89 (9th Cir. 2020). The physical intrusion is what matters. In Ngumezi, the officer \"entered the interior space of the vehicle when he leaned in across the plane of the door,\" and \"that physical intrusion is constitutionally significant.\" Id. at 1289. In most circumstances, \"probable cause is necessary to conduct a warrantless search of a vehicle.\" Id. (quoting United States v. Rodgers, 656 F.3d 1023, 1024 (9th Cir. 2011))."),
    (P, "The FAC alleges that search. Melano opened the closed passenger door of Plaintiff's car without a warrant or consent, FAC ¶¶ 16, 56, and entered the interior, where he removed and examined the cup, id. ¶¶ 55, 60. The motion does not cite Ngumezi, even though the FAC relies on it. Id. ¶¶ 55-57, 61-62. Defendants must therefore establish an exception to the warrant requirement from the face of the FAC. They cannot."),
    (S2, "2. The FAC pleads no objective basis for emergency aid."),
    (P, "The emergency-aid exception permits a warrantless entry only when officers have \"an objectively reasonable basis for believing\" that a person inside needs immediate aid. Brigham City v. Stuart, 547 U.S. 398, 406 (2006); Michigan v. Fisher, 558 U.S. 45, 47 (2009) (per curiam). In this circuit, the government must show both (1) an objectively reasonable basis, considering the totality of the circumstances, for concluding that there was an immediate need to protect others or themselves from serious harm, and (2) that the scope and manner of the search were reasonable to meet that need. United States v. Snipe, 515 F.3d 947, 951-52 (9th Cir. 2008). The exception is narrow, and it derives from the community-caretaking function rather than from the investigation of crime. Hopkins v. Bonvicino, 573 F.3d 752, 763 (9th Cir. 2009)."),
    (P, "Defendants rely on Mincey v. Arizona, 437 U.S. 385 (1978), which they describe as a holding of \"[t]he Ninth Circuit.\" Mot. 7:27-28. Mincey is a Supreme Court decision that rejected a warrantless search of a homicide scene. It states the general emergency principle, but it supplies no fact that would make Plaintiff's situation an emergency."),
    (P, "The FAC alleges facts that negate an emergency. The car was intact, with no damage, smoke, fire, or debris, and Plaintiff was in a normal resting posture. FAC ¶ 56. He had pulled off the road because he was tired. Id. ¶¶ 11-12. Every remark the officers made before the entry concerned the car or their suspicion of a crime: \"It's a rental,\" \"It wasn't here earlier,\" \"I think it's booze.\" Id. ¶¶ 14-15, 56. None describes a sign of injury, illness, or distress. Under Fisher the test is objective, and Plaintiff does not rest on the officers' motives. But what officers say they are observing is strong evidence of the objective facts available to them, and those facts disclosed no emergency."),
    (P, "Defendants' only response is that the officers \"could not have known\" that no emergency existed \"before opening the door.\" Mot. 8:9-10. That inverts the test. The question is whether objective facts gave the officers a reasonable basis to believe aid was immediately needed, not whether opening the door could dispel uncertainty. Every driver resting in a parked car presents some uncertainty. That does not make every parked car an emergency."),
    (P, "The motion also ignores Snipe's second requirement: the scope and manner of the intrusion must be reasonable to meet the asserted need. Opening a passenger door and entering the interior is not the only, or the least intrusive, way to check on a resting driver. Whether the officers' conduct fit any welfare concern is a factual question that cannot be resolved against Plaintiff on the pleadings."),
    (S2, "3. A suspected parking infraction does not authorize a vehicle search."),
    (P, "Defendants argue in the alternative that, if there was no emergency, Plaintiff's stop violated Vehicle Code section 21718, giving the officers grounds \"to investigate a crime.\" Mot. 8:14-23. The argument fails twice. First, section 21718(a)(1) permits stopping on a freeway \"[w]hen necessary to avoid injury or damage to persons or property.\" The FAC alleges that Plaintiff left the travel lanes because he was fatigued, consistent with commercial-driver safety principles. FAC ¶¶ 11-12. On the pleadings, the exception is at least plausibly alleged. Second, even a completed infraction does not authorize a search of the vehicle. Knowles v. Iowa, 525 U.S. 113, 117-19 (1998). Devenpeck v. Alford, 543 U.S. 146 (2004), on which Defendants rely, addresses whether probable cause for some offense supports an arrest. Id. at 152-53. It creates no power to enter a car to investigate a parking infraction."),
    (S2, "4. An officer's guess about a cup is not probable cause."),
    (P, "Finally, Defendants contend that Melano's remark, \"I think it's booze,\" supplied probable cause. Mot. 8:24-9:2. The FAC alleges that Melano formed that hypothesis about a cup seen through the window \"before any contact with Plaintiff and before any observation of his condition.\" FAC ¶ 15. An officer may seize an item in plain view only if he has probable cause to believe it is contraband or evidence. Arizona v. Hicks, 480 U.S. 321, 326-27 (1987). Defendants' own motion concedes that the officers \"did not discover the cup in Plaintiff's vehicle contained urine until they searched Plaintiff's vehicle.\" Mot. 8:28-9:2. That concession confirms that the cup's contents were not apparent from outside, and that the search, not the view, produced the information. At a minimum, whether a guess about an unidentified cup amounted to probable cause is a fact-dependent question that cannot be resolved against Plaintiff on a motion to dismiss."),

    (S, "C. Count V States a Claim for the Seizure and Search of the Cup."),
    (P, "Count V challenges conduct beyond opening the door. Melano reached inside, removed the cup from the console, smelled it, and examined its contents while Meza-Gonzalez directed Plaintiff's attention and movements. FAC ¶¶ 17, 60. A physical intrusion combined with an attempt to find something or to obtain information is a search. Ngumezi, 980 F.3d at 1289 (citing United States v. Jones, 565 U.S. 400, 408 n.5 (2012)). Removing the cup was also a seizure of Plaintiff's property, which required probable cause. Hicks, 480 U.S. at 326-27. Because Count IV plausibly alleges that the entry was unjustified, Count V's allegations that the officers then seized and examined an item inside the car state a claim for the same reasons."),
    (P, "The FAC further alleges that once Melano identified the liquid as urine, the basis for any suspicion arising from the cup was gone, yet the officers continued the warrantless search and the detention. FAC ¶¶ 18, 61. Evidence that may support probable cause can be vitiated by countervailing evidence, and officers may not disregard substantial countervailing indicators. United States v. Lopez, 482 F.3d 1067, 1073-74 (9th Cir. 2007). The FAC plausibly alleges that is what occurred here."),

    (S, "D. Count III States a Claim for Arrest Without Probable Cause."),
    (P, "Probable cause to arrest exists when the facts known to the officer would lead a prudent person to believe that the suspect has committed an offense. Devenpeck, 543 U.S. at 152. The Court considers the totality of the circumstances. District of Columbia v. Wesby, 583 U.S. 48, 60-61 (2018). On a motion to dismiss, the totality is the one the complaint pleads."),
    (P, "The FAC pleads the facts known at the moment of arrest, between 01:11:15 and 01:11:33. Plaintiff had been resting in a parked car. The only suspected \"beverage\" had been identified as urine. He had spoken coherently and identified his location. No officer had seen him drive. Certain field exercises were not administered because the ground was unsuitable. And he had just declined a test the arresting officer had described as voluntary. FAC ¶¶ 11, 17-24, 50. Those facts do not compel a finding of probable cause. They plausibly negate it."),
    (P, "Defendants' contrary argument depends on facts outside the FAC. They rely on \"slurred speech and other signs of intoxication,\" Mot. 10:1-3, which are the report entries the FAC disputes, FAC ¶¶ 20, 26(b)-(c). And they rely on the FAC's silence about field-exercise results. Mot. 6:27-28, 10:21-24. Neither is a pleaded fact. What remains is that Plaintiff \"was asleep in a vehicle parked on the side of the freeway with a cup of urine next to him.\" Mot. 10:19-20. That describes a tired driver who stopped driving. Even Defendants retreat from it, arguing only that \"[a]t the very least\" those facts supported asking for field sobriety tests. Id. at 10:20-21. Grounds to investigate are not probable cause to arrest."),
    (P, "The sequence of the arrest reinforces the claim. Meza-Gonzalez told Plaintiff the PAS test was voluntary, then said that refusing it would leave the arrest to his \"discretion,\" and arrested Plaintiff seconds after he declined. FAC ¶¶ 21-24. California law makes the PAS an investigative tool that the driver may decline, Cal. Veh. Code § 23612(h)-(i), and a refusal to consent to a search is privileged conduct that cannot be treated as evidence of wrongdoing. United States v. Prescott, 581 F.2d 1343, 1351 (9th Cir. 1978). The FAC plausibly alleges that the decisive event before the arrest was not any new evidence of impairment, but Plaintiff's exercise of a right the officer had just confirmed. FAC ¶¶ 24, 50."),
    (P, "The FAC also pleads each officer's role. Meza-Gonzalez made the arrest, and Melano conducted the entry, the cup search, and the field exercises and took part in the joint investigation through the arrest. FAC ¶ 53. The motion does not challenge either officer's personal participation, and an argument raised for the first time in reply need not be considered. Zamani v. Carnes, 491 F.3d 990, 997 (9th Cir. 2007)."),

    (S, "E. Count I States a Judicial-Deception Claim."),
    (P, "A judicial-deception claim requires facts showing that the defendant deliberately or recklessly made false statements or omissions that were material to the finding of probable cause. Galbraith v. County of Santa Clara, 307 F.3d 1119, 1126 (9th Cir. 2002). Galbraith rejected any heightened pleading requirement for such claims. Id. at 1125-26."),
    (P, "The FAC meets that standard. It identifies the affiant (Meza-Gonzalez), the sworn documents, the warrant they supported, and the compelled blood draw that followed. FAC ¶¶ 25, 29, 38-42. It identifies specific descriptions, namely that Plaintiff's speech was \"slurred\" and that he \"seemed very confused and disoriented,\" and alleges the facts on the recording that contradict them: extended coherent conversation, spelling his surname, discussing the car's mechanics, correctly identifying his location, and reading distant signs. Id. ¶¶ 20, 26(b)-(c). And it identifies material omissions: that the suspected alcohol had been identified as urine, that certain exercises were not administered because of the ground, that the PAS had been described as voluntary, and that no officer saw Plaintiff drive. Id. ¶ 27."),
    (P, "Recklessness is plausibly alleged because each challenged statement and omission concerned facts within Meza-Gonzalez's personal knowledge; he was present for the encounter he described. FAC ¶¶ 41, 46. The Ninth Circuit has called that circumstance \"[t]he most commonsense evidence that the officers acted with at least a reckless disregard for the truth.\" Chism v. Washington State, 661 F.3d 380, 388 (9th Cir. 2011). Whether an officer acted deliberately or recklessly is a question of fact. Id. (citing Liston v. County of Riverside, 120 F.3d 965, 974 (9th Cir. 1997))."),
    (P, "Defendants' materiality argument cannot be decided on this record. Materiality asks whether the warrant application, \"once corrected and supplemented,\" would have provided a substantial basis for probable cause. Id. at 389 (quoting United States v. Stanert, 762 F.2d 775, 782 (9th Cir. 1985)). That inquiry requires the application itself, and Defendants have not placed it before the Court. Their argument instead keeps the disputed entries and relies on field-exercise results the FAC does not plead. Mot. 6:24-28. Materiality cannot be decided against Plaintiff on that basis. If the Court concludes that the FAC should identify the warrant application and its specific statements more precisely, the remedy is leave to amend, which Plaintiff requests in Part V.H."),

    (S, "F. Plaintiff Does Not Oppose Dismissal of Counts II and VI With Leave to Amend."),
    (P, "To focus the issues, Plaintiff does not oppose dismissal of Count II (deliberate fabrication of evidence) and Count VI (First Amendment retaliation), provided that the dismissal is without prejudice and with leave to amend. Plaintiff notes two errors in the motion so that they do not shape any amended pleading."),
    (P, "First, Defendants read Caldwell v. City & County of San Francisco, 889 F.3d 1105 (9th Cir. 2018), as making a criminal charge a prerequisite to a fabrication claim. Mot. 7:8-17. Caldwell holds that being charged is sufficient to show a deprivation of liberty. 889 F.3d at 1115. It does not hold that a charge is necessary, and the Ninth Circuit has recognized deliberate-fabrication claims arising outside criminal prosecutions where a protected liberty or property interest is lost. Costanich v. Dep't of Soc. & Health Servs., 627 F.3d 1101, 1108 (9th Cir. 2010). Second, the motion analyzes retaliation under Bostock v. Clayton County, 590 U.S. 644 (2020), a Title VII decision, Mot. 11:9-19, rather than the framework that governs retaliatory-arrest claims, Nieves v. Bartlett, 587 U.S. 391, 402 (2019)."),

    (S, "G. Qualified Immunity Does Not Warrant Dismissal on This Record."),
    (P, "The motion's qualified-immunity argument addresses only whether there was probable cause to search and arrest. Mot. 12-13. It does not separately analyze the door entry, the seizure of the cup, or judicial deception. Qualified immunity is assessed on the facts alleged in the complaint, and dismissal on that ground at the pleading stage is proper only if the complaint fails to allege a violation of clearly established law. Keates v. Koile, 883 F.3d 1228, 1234-35 (9th Cir. 2018)."),
    (P, "Count IV. Ngumezi was decided in 2020, four years before this encounter. It held that opening a car door and entering the interior is a search requiring probable cause or another particularized justification. 980 F.3d at 1288-89. The requirement of an objectively reasonable basis before an emergency-aid entry was settled long before that. Brigham City, 547 U.S. at 406; Snipe, 515 F.3d at 951-52; Hopkins, 573 F.3d at 763. Whether any objective emergency existed depends on facts the FAC pleads against Defendants. Qualified immunity cannot be decided by substituting \"unconscious\" for the FAC's allegations."),
    (P, "Count V. The same authorities, and the settled rule that a plain-view seizure requires probable cause, Hicks, 480 U.S. at 326-27, clearly established the right as to the cup."),
    (P, "Count III. The right to be free from arrest without probable cause is clearly established. Whether officers reasonably but mistakenly believed probable cause existed depends on which observations are credited, and the motion's argument credits the disputed ones. That question cannot be resolved against Plaintiff on the pleadings."),
    (P, "Count I. The Ninth Circuit has \"consistently applied the rule that summary judgment on the ground of qualified immunity is not appropriate once a plaintiff has made out a judicial deception claim.\" Chism, 661 F.3d at 393. If immunity is unavailable at summary judgment once such a claim is made out, dismissal is not appropriate where the FAC plausibly alleges one."),

    (S, "H. The Prior Litigation Does Not Make Amendment Futile."),
    (P, "Leave to amend should be freely given when justice so requires. Fed. R. Civ. P. 15(a)(2). A pro se complaint should not be dismissed without leave to amend unless it is absolutely clear that its deficiencies cannot be cured, and the plaintiff must first be told what the deficiencies are. Akhtar v. Mesa, 698 F.3d 1202, 1212 (9th Cir. 2012); Lopez v. Smith, 203 F.3d 1122, 1130-31 (9th Cir. 2000) (en banc). Defendants acknowledge that rule. Mot. 13:23-25 (citing Garity v. APWU Nat'l Lab. Org., 828 F.3d 848, 854 (9th Cir. 2016))."),
    (P, "Defendants' futility argument rests on the history of other cases, not on any defect that amendment could not cure. Mot. 14:1-21. No court has adjudicated these claims on the merits. The Eastern District ruling the motion cites was a magistrate judge's recommendation, not a judgment, and it was issued on April 20, 2026, not in 2025 as the motion states. Mot. 14:8. The Alameda County action ended without any ruling on the merits. Newanforbi v. Serrato, No. 3:26-cv-05953-CRB, involves a different defendant and a different claim; and in that related action, this Court found on screening that a complaint resting on an overlapping factual record stated a claim. FAC ¶ 35. This is Plaintiff's first amendment in this case, made as of right. Nothing in this history shows that the specific amendments below would be futile."),
    (P, "If the Court finds any claim deficient, Plaintiff requests leave to file a second amended complaint within 28 days. He would make the following amendments:"),
    (L, "Door sequence. Plead the entry using the timestamps on the recording, including the officers' knocking, Melano's instruction to \"[o]pen the window,\" and his opening of the passenger door seconds later, so that the allegations state precisely what Plaintiff was doing when the door was opened."),
    (L, "Warrant application. Identify the warrant application by date and time, quote the specific statements challenged in it, identify the omitted facts, and set out the corrected application."),
    (L, "Form wording. Correct paragraphs 2, 26(d), and 28, which describe a \"Beverage Present: Yes\" entry. The form fields at issue refer to an odor of an alcoholic beverage, not to a container. Plaintiff will plead the forms' actual wording and will not rely on that characterization."),
    (L, "Search chronology. Plead the door opening, the removal and examination of the cup, and any later search as separate acts, each with the facts known at that moment and each Defendant's role."),
    (L, "Arrest chronology. Plead the PAS advisement, the conditional statement, the refusal, the arrest command, and the handcuffing with their exact times."),
    (L, "Counts II and VI. Re-plead Count II only if Plaintiff can allege a specific fabricated statement and its use to cause a particular deprivation, and re-plead Count VI only with protected expression and facts satisfying Nieves."),
    (L, "Fees. Remove the request for attorney's fees for Plaintiff's own work."),

    (S, "I. Rule 12(f) Does Not Authorize Striking the Punitive-Damages Request."),
    (P, "\"We therefore hold that Rule 12(f) does not authorize district courts to strike claims for damages on the ground that such claims are precluded as a matter of law.\" Whittlestone, 618 F.3d at 974-75. Defendants' authorities are district-court decisions that predate Whittlestone. Mot. 14:26-15:2 (citing Bureerong v. Uvawas, 922 F. Supp. 1450 (C.D. Cal. 1996), and Wilkerson v. Butler, 229 F.R.D. 166 (E.D. Cal. 2005))."),
    (P, "Punitive damages are available under section 1983 when a defendant's conduct involves \"reckless or callous indifference to the federally protected rights of others.\" Smith v. Wade, 461 U.S. 30, 56 (1983). The FAC alleges that Melano entered a car without any articulated justification while voicing investigative suspicions, FAC ¶¶ 14-16, 56, and that Meza-Gonzalez swore to descriptions contradicted by events he personally witnessed, id. ¶¶ 26(b)-(c), 41, 46. Those allegations plausibly support punitive damages. Whether Plaintiff can prove the required state of mind is a question for a later stage."),
    (P, "Plaintiff confirms that he does not seek attorney's fees under 42 U.S.C. § 1988 for his own work as a self-represented litigant. See Kay v. Ehrler, 499 U.S. 432, 437-38 (1991). He preserves his request for taxable costs, FAC Prayer ¶ C, and for fees for any counsel who may later appear."),

    (H, "VI. CONCLUSION"),
    (P, "The Court should deny the motion to dismiss as to Counts I, III, IV, and V; dismiss Counts II and VI without prejudice and with leave to amend; deny the motion to strike the punitive-damages request; and note Plaintiff's withdrawal of any request for attorney's fees for his own work. If the Court finds any other claim deficient, Plaintiff requests 28 days' leave to file a second amended complaint consistent with Part V.H."),
]


def signature_block() -> str:
    return (
        f"Dated: {SIGN_DATE}\n"
        "\n"
        "Respectfully submitted,\n"
        "___________________________________\n"
        f"{PLAINTIFF_NAME}\n"
        "Plaintiff, In Pro Per"
    )


CERT_LINES = [
    "I am the Plaintiff in this action. On " + SIGN_DATE + ", I served the foregoing PLAINTIFF'S "
    "OPPOSITION TO DEFENDANTS' MOTION TO DISMISS FIRST AMENDED COMPLAINT AND MOTION TO STRIKE "
    "on counsel for Defendants Santiago Meza-Gonzalez and Jose Melano, addressed as follows:",
    "Haiyang A. Li, Deputy Attorney General, Office of the Attorney General, 300 South Spring "
    "Street, Suite 1702, Los Angeles, CA 90013-1230; Haiyang.Li@doj.ca.gov",
    "by the following method: [ ] the Court's CM/ECF system; [ ] first-class U.S. Mail, postage "
    "prepaid, deposited at ____________________, California.",
    "I declare under penalty of perjury under the laws of the United States that the foregoing is "
    "true and correct.",
]


def is_toc_entry(ctype: str, text: str):
    if ctype == H:
        return ("roman", text)
    if ctype == S:
        return ("letter", text)
    return None


def toc_row(d, label: str, page_str: str, bold: bool = False, indent: float = 0,
            num_reserve: float = 30) -> None:
    c = d.c
    fn = "Times-Bold" if bold else "Times-Roman"
    size = 12
    left_x = CONTENT_LEFT + indent
    right_x = CONTENT_RIGHT - 8
    avail = CONTENT_WIDTH - indent - num_reserve - 6
    words = label.split(" ")
    lines, cur = [], ""
    for w in words:
        t = (cur + " " + w).strip()
        if c.stringWidth(t, fn, size) > avail and cur:
            lines.append(cur)
            cur = w
        else:
            cur = t
    if cur:
        lines.append(cur)
    for i, ln in enumerate(lines):
        d._ensure_line()
        y = d._line_y(d.current_line)
        c.setFont(fn, size)
        c.drawString(left_x, y, ln)
        if i == len(lines) - 1:
            c.setFont("Times-Roman", size)
            c.drawRightString(right_x, y, page_str)
            label_end = left_x + c.stringWidth(ln, fn, size) + 4
            num_w = c.stringWidth(page_str, "Times-Roman", size)
            leader_end = right_x - num_w - 4
            if leader_end > label_end:
                dw = c.stringWidth(". ", "Times-Roman", size)
                ndots = max(0, int((leader_end - label_end) / dw))
                c.drawString(label_end, y, ". " * ndots)
        d.current_line += 1


def fmt_pages(pages: set) -> str:
    if not pages:
        return "0"
    ps = sorted(pages)
    if len(ps) > 5:
        return "passim"
    return ", ".join(str(p) for p in ps)


def render(out_path: Path, toc_pages: dict, toa_pages: dict,
           capture: dict | None = None, cites: dict | None = None) -> int:
    out_path.parent.mkdir(parents=True, exist_ok=True)
    d = PleadingPaper(str(out_path), doc_title_footer=DOC_TITLE_FOOTER)
    c = d.c
    atty_y = d._line_y(0)
    for i, (text, font, size) in enumerate(ATTORNEY_BLOCK):
        c.setFont(font, size)
        c.drawString(CONTENT_LEFT, atty_y - i * 15, text)
    d.current_line = 4
    d.blank_line()
    d.write_line(COURT_LINE1, bold=True, center=True)
    d.write_line(COURT_LINE2, bold=True, center=True)
    d.blank_line()
    d.draw_caption_block(CAPTION_LEFT, CAPTION_RIGHT, caption_size=10, tight_lh=13, boxed=True)
    d.blank_line()
    d.write_wrapped(HEARING_LINE, first_indent=0)

    # Table of contents
    d.start_new_page()
    d.write_line("TABLE OF CONTENTS", bold=True, center=True)
    d.blank_line()
    for ctype, text in CONTENT:
        te = is_toc_entry(ctype, text)
        if not te:
            continue
        level, label = te
        toc_row(d, label, str(toc_pages.get(label, "0")), bold=(level == "roman"),
                indent=(0 if level == "roman" else 18))

    # Table of authorities
    d.start_new_page()
    d.write_line("TABLE OF AUTHORITIES", bold=True, center=True)
    d.blank_line()
    current_cat = None
    for cat, display, _pat in AUTHORITIES:
        if cat != current_cat:
            if current_cat is not None:
                d.blank_line()
            d.write_line(cat, bold=True)
            current_cat = cat
        toc_row(d, display, fmt_pages(toa_pages.get(display, set())))

    # Body
    d.start_new_page()
    body_first_page = d.page_num
    for c_type, text in CONTENT:
        if c_type == H:
            d.ensure_space(4)
            if capture is not None:
                capture[text] = d.page_num
            d.write_line(text, bold=True, center=True)
            d.blank_line()
        elif c_type in (S, S2):
            d.ensure_space(6)
            if capture is not None and c_type == S:
                capture[text] = d.page_num
            d.write_wrapped(f"<<b:{text}>>", first_indent=0, indent=(0 if c_type == S else 18))
        elif c_type in (P, L):
            start = d.page_num
            if c_type == P:
                d.write_wrapped(italicize_cases(text), first_indent=36)
            else:
                d.write_wrapped("- " + italicize_cases(text), indent=36, first_indent=0)
            end = d.page_num
            if cites is not None:
                for _cat, display, pat in AUTHORITIES:
                    if re.search(pat, text):
                        cites.setdefault(display, set()).update(range(start, end + 1))

    d.blank_line()
    d.ensure_space(10)
    for line in signature_block().split("\n"):
        if line.startswith("_") and os.path.isfile(SIGNATURE_PATH):
            d.draw_signature_image(
                SIGNATURE_PATH, SIG_IMG_W_PX, SIG_IMG_H_PX, line,
                width=SIG_WIDTH, right_margin_offset=SIG_RIGHT_OFFSET,
                height_scale=SIG_HEIGHT_SCALE,
            )
        d.write_line(line, right=True, right_margin_offset=SIG_RIGHT_OFFSET)
    body_last_page = d.page_num

    # Certificate of service
    d.start_new_page()
    d.write_line("CERTIFICATE OF SERVICE", bold=True, center=True)
    d.blank_line()
    for para in CERT_LINES:
        d.write_wrapped(para, first_indent=36)
    d.blank_line()
    for line in signature_block().split("\n"):
        if line.startswith("_") and os.path.isfile(SIGNATURE_PATH):
            d.draw_signature_image(
                SIGNATURE_PATH, SIG_IMG_W_PX, SIG_IMG_H_PX, line,
                width=SIG_WIDTH, right_margin_offset=SIG_RIGHT_OFFSET,
                height_scale=SIG_HEIGHT_SCALE,
            )
        if line.startswith("Respectfully"):
            continue
        d.write_line(line, right=True, right_margin_offset=SIG_RIGHT_OFFSET)

    d.save()
    print(f"Wrote {out_path} ({out_path.stat().st_size} bytes, {d.page_num} pages; "
          f"memorandum pp. {body_first_page}-{body_last_page} = "
          f"{body_last_page - body_first_page + 1} pages)")
    return d.page_num


def write_text_copy() -> None:
    lines = [f"# Opposition to ECF 22 - text of DRAFT v2 (generated from {Path(__file__).name})", ""]
    for ctype, text in CONTENT:
        if ctype == H:
            lines += [f"## {text}", ""]
        elif ctype == S:
            lines += [f"### {text}", ""]
        elif ctype == S2:
            lines += [f"#### {text}", ""]
        elif ctype == L:
            lines += [f"- {text}", ""]
        else:
            lines += [text, ""]
    lines += [f"Dated: {SIGN_DATE}", "", "[signature image]", PLAINTIFF_NAME, "Plaintiff, In Pro Per", ""]
    TEXT_OUT.write_text("\n".join(lines), encoding="utf-8")
    print(f"Wrote {TEXT_OUT}")


def main() -> None:
    if not Path(SIGNATURE_PATH).is_file():
        raise SystemExit(f"Missing universal signature: {SIGNATURE_PATH}")
    SCRATCH_DIR.mkdir(parents=True, exist_ok=True)
    capture: dict = {}
    cites: dict = {}
    tmp = SCRATCH_DIR / "_m32_pass1.pdf"
    render(tmp, {}, {}, capture=capture, cites=cites)
    tmp.unlink(missing_ok=True)
    for out in OUT_PATHS:
        render(out, capture, cites)
    write_text_copy()
    print("NOTE: DRAFT. Not filed or served. Clear REVIEW-NOTES.md before filing.")


if __name__ == "__main__":
    main()
