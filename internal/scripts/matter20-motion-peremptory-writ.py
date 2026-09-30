#!/usr/bin/env python3
"""Matter 20 — Motion for Peremptory Writ of Mandate on the First Cause of
Action, with supporting declaration, [proposed] judgment and writ, and the
attachment to Petitioner's CM-110 for the October 28, 2026 CMC.

Alameda Super. Ct. No. 26CV191136, Dept. 25 (Hon. Jenna M. Whitman).

The August 29, 2026 order overruled the demurrer to Count 1 because the
qualifying-crime question is factual: if the Court credits Petitioner's
account (no odor, no impairment, officers' report false), it "could
reasonably find probable cause for arrest was lacking, which could support a
finding that the CHP abused its discretion." This motion asks for that
merits determination on the record CHP already had, and for a writ
commanding certification — with remand for reconsideration as the
alternative.

Hearing reserved: January 8, 2027, 9:00 a.m., Dept. 25, Reservation ID
958052306492. Renders UNSIGNED; Petitioner signs, then attach the CRS
receipt as the motion's last page.
Every authority is flagged for citation-verify before filing.

  python3 internal/scripts/matter20-motion-peremptory-writ.py

FILED_STATUS: False.
"""
from __future__ import annotations

import os
import sys
from pathlib import Path

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, SCRIPT_DIR)
sys.path.insert(0, os.path.join(SCRIPT_DIR, "lib"))

from pleading_paper import CONTENT_LEFT, COURT_LINE1, PleadingPaper  # noqa: E402

FILED_STATUS = False

# Reserved Sep. 29, 2026 (CRS "Motion for Writ of Mandate"). CCP § 1005(b):
# 16 court days' notice, plus 2 court days for electronic service
# (CCP § 1010.6) -> file and serve by Friday, December 11, 2026.
# Attach the CRS receipt as the last page of the motion.
RESERVATION_ID = "958052306492"
HEARING_DATE = "January 8, 2027"
HEARING_TIME = "9:00 a.m."
EXEC_DATE = "October ___, 2026"
EXEC_PLACE = "Stockton, California"

COURT_LINE2 = "COUNTY OF ALAMEDA"
SIG_LINE = "___________________________________"
REPO_ROOT = Path(SCRIPT_DIR).parents[1]
OUT = REPO_ROOT / "internal" / "public" / "documents" / "matter-20"

CAPTION_LEFT = [
    ("BRENDAN NGEHSI NEWANFORBI,", True, False),
    ("", False, False),
    ("                          Petitioner,", False, False),
    ("", False, False),
    ("       v.", False, False),
    ("", False, False),
    ("CALIFORNIA HIGHWAY PATROL;", True, False),
    ("G. SERRATO, in his official capacity", True, False),
    ("as Captain and Commander of the CHP", True, False),
    ("Dublin Area; and DOES 1 through 10,", True, False),
    ("inclusive,", True, False),
    ("", False, False),
    ("                          Respondents.", False, False),
]


def caption_right(title: list[str], hearing: bool = True) -> list[tuple[str, bool, bool]]:
    rows = [("Case No. 26CV191136", False, False), ("", False, False)]
    rows += [(t, True, False) for t in title]
    rows.append(("", False, False))
    if hearing:
        rows += [
            (f"Date:  {HEARING_DATE}", False, False),
            (f"Time:  {HEARING_TIME}", False, False),
            ("Dept.: 25", False, False),
            (f"Reservation ID: {RESERVATION_ID}", False, False),
        ]
    rows += [
        ("Hon. Jenna M. Whitman", False, False),
        ("Action Filed: May 29, 2026", False, False),
    ]
    return rows


# ---------------------------------------------------------------- content
# Blocks: ("h", centered bold) ("sh", left bold) ("p", paragraph)
# ("q", indented quotation) ("n", numbered/unindented paragraph) ("b",)

NOTICE_AND_MPA: list[tuple] = [
    ("h", "NOTICE OF MOTION AND MOTION"),
    ("b",),
    ("n", "TO RESPONDENTS AND THEIR COUNSEL OF RECORD:"),
    ("b",),
    ("p", f"PLEASE TAKE NOTICE that on {HEARING_DATE}, at {HEARING_TIME}, or as soon "
          "thereafter as the matter may be heard, in Department 25 of the Alameda County "
          "Superior Court, Rene C. Davidson Courthouse, 1225 Fallon Street, Oakland, "
          "California, Petitioner Brendan Ngehsi Newanforbi will and hereby does move for "
          "judgment granting a peremptory writ of mandate on the First Cause of Action of "
          "the Petition for Writ of Mandate."),
    ("p", "The motion seeks a writ commanding Respondent California Highway Patrol "
          "(\"CHP\") to set aside its April 20, 2026 denial and, within 30 days of service "
          "of the writ, to complete, sign, and deliver to Petitioner the Form I-918, "
          "Supplement B, U Nonimmigrant Status Certification he requested on April 9, 2026. "
          "In the alternative, Petitioner seeks a writ commanding CHP to set aside the "
          "denial and to reconsider the request within 30 days in conformity with the "
          "Court's findings, and to file a return to the writ within 45 days."),
    ("p", "The motion is made under Code of Civil Procedure sections 1085, 1086, and 1094 "
          "and Penal Code section 679.10, on the grounds that the record before CHP when it "
          "denied certification shows that Petitioner was the victim of qualifying criminal "
          "activity and has been helpful, that CHP's contrary conclusion is unsupported by "
          "that record, and that CHP therefore abused its discretion and failed to perform "
          "the duty section 679.10, subdivision (g)(1) imposes."),
    ("p", "The motion is based on this notice, the following memorandum of points and "
          "authorities, the concurrently filed Declaration of Brendan Ngehsi Newanforbi, "
          "the Petition and its Exhibits 1 through 14, the Notice of Lodging of the "
          "November 1, 2024 CHP dashcam recording filed September 8, 2026, the Court's "
          "August 29, 2026 Order, the files and records of this action, and any argument "
          "presented at the hearing."),
    ("b",),
    ("h", "MEMORANDUM OF POINTS AND AUTHORITIES"),
    ("b",),
    ("sh", "I.  INTRODUCTION"),
    ("p", "The Court has already framed the question this motion asks it to decide. In "
          "overruling CHP's demurrer to the First Cause of Action, the Court held that if it "
          "credits Petitioner's showing \"that neither he nor his vehicle smelled of "
          "alcohol, that he showed no signs of impairment in talking with the officers or in "
          "performing the physical field sobriety tests he agreed to perform, and that the "
          "arresting officers lied about it in their police report, it could reasonably find "
          "probable cause for arrest was lacking, which could support a finding that the CHP "
          "abused its discretion in refusing to certify Petitioners Form I-918.\" (Order "
          "Sustaining Demurrer In Part, Aug. 29, 2026 (\"Order\"), at p. 4.)"),
    ("p", "That showing does not depend on Petitioner's word. It rests on CHP's own "
          "records, every one of which was before the certifying official on April 20, "
          "2026: CHP's 62-minute dashcam recording, CHP's arrest-investigation report, and "
          "CHP's Penal Code section 851.6 certificate releasing Petitioner because there "
          "were \"insufficient grounds for making a criminal complaint.\" The recording does "
          "not contain what the report says it saw. CHP's denial letter does not mention "
          "any of those records. On this record, the only lawful conclusion is that "
          "Petitioner was the victim of qualifying criminal activity, and section 679.10, "
          "subdivision (g)(1) then provides that CHP \"shall certify.\""),
    ("sh", "II.  STATEMENT OF FACTS"),
    ("sh", "A.  The November 1, 2024 detention."),
    ("p", "Shortly before 1:00 a.m. on November 1, 2024, CHP officers found Petitioner "
          "asleep in a parked, engine-off rental vehicle on the shoulder of eastbound "
          "Interstate 580 in Livermore, where he had pulled over to rest on his way home "
          "to Stockton. (Pet. ¶ 34; Pet. Ex. 5; Newanforbi Decl. ¶¶ 3-4.) He told the "
          "officers he had not been drinking. (Pet. Ex. 5 at p. 3.) An empty can was found "
          "in the vehicle; Petitioner denied drinking from it. (Pet. Ex. 5 at pp. 4-6; Pet. "
          "¶ 47.) He performed the field sobriety tests the officers administered. (Pet. "
          "Ex. 5 at pp. 8-9.) The officer then asked him to take a preliminary alcohol "
          "screening test, told him he was not required to take it, and told him that "
          "whether to arrest was within the officer's discretion; Petitioner declined, and "
          "was handcuffed and arrested. (Pet. Ex. 5 at p. 10; Order at p. 3.) His blood was "
          "drawn under a warrant, he was booked, and he was held until November 5, 2024. "
          "(Pet. ¶¶ 38-42; Newanforbi Decl. ¶ 6.)"),
    ("sh", "B.  CHP's report asserts what CHP's recording does not show."),
    ("p", "CHP's arrest-investigation report states that Petitioner exhibited a \"strong "
          "distinct odor of an alcoholic beverage,\" \"slurred\" speech, and a \"very "
          "confused and disoriented\" demeanor, and that a beverage was present. (Pet. "
          "Ex. 6.) CHP's own dashcam recording of the entire encounter contains none of "
          "that. No officer mentions an odor of alcohol on Petitioner's breath or person at "
          "any point in the recording; when an officer examined the only liquid found in "
          "the vehicle, he identified it aloud as urine, not an alcoholic beverage; and "
          "Petitioner's recorded speech is clear and responsive throughout. (Pet. Ex. 5; "
          "Notice of Lodging, Sept. 8, 2026; Newanforbi Decl. ¶¶ 7-10.) Petitioner's "
          "April 9, 2026 request identified each of these contradictions by dashcam "
          "timestamp. (Pet. Ex. 3.)"),
    ("sh", "C.  CHP released Petitioner for insufficient grounds, and no charge was filed."),
    ("p", "Four days after the arrest, CHP issued a certificate under Penal Code sections "
          "849, subdivision (b)(1) and 851.6 describing the event as \"a detention only, "
          "not an arrest,\" because there were \"insufficient grounds for making a criminal "
          "complaint.\" (Pet. Ex. 7.) No accusatory pleading was ever filed. (Pet. ¶ 42; "
          "Newanforbi Decl. ¶ 11.)"),
    ("sh", "D.  The request and the denial."),
    ("p", "On April 9, 2026, Petitioner submitted Form I-918, Supplement B to CHP with a "
          "supporting memorandum, the dashcam transcript, the arrest report, and the "
          "section 851.6 certificate. (Pet. ¶¶ 55-58, Exs. 2-8.) Petitioner had already "
          "filed a citizen complaint and a POST complaint about the incident and provided "
          "CHP the dashcam transcript. (Pet. ¶¶ 7, 87; Newanforbi Decl. ¶ 12.) Eleven "
          "days later, CHP denied the request in a letter stating only that the incident "
          "\"does not meet the standard of qualifying criminal activity\" under section "
          "679.10 or 8 U.S.C. section 1101(a)(15)(U)(iii). (Pet. Ex. 1.) The letter does "
          "not mention the recording, the report, or the certificate, and does not assert "
          "any failure to cooperate. (Ibid.; Order at p. 4.)"),
    ("sh", "III.  LEGAL STANDARD"),
    ("p", "A writ of mandate may issue \"to compel the performance of an act which the "
          "law specially enjoins\" where there is no plain, speedy, and adequate remedy in "
          "the ordinary course of law. (Code Civ. Proc., §§ 1085, subd. (a), 1086.) "
          "Mandate will not control how an agency exercises discretion, but it lies to "
          "correct an abuse of discretion and to compel the agency to exercise its "
          "judgment under the governing legal standards. (Common Cause v. Board of "
          "Supervisors (1989) 49 Cal.3d 432, 442.) The Court has held that the First Cause "
          "of Action is reviewable on that basis and that its resolution turns on "
          "contested facts to be decided at the hearing on the merits. (Order at pp. 3-4.)"),
    ("p", "Section 679.10, subdivision (g)(1) provides that, upon the victim's request, "
          "a certifying official \"shall certify victim helpfulness on the Form I-918 "
          "Supplement B certification, when the victim was a victim of a qualifying "
          "criminal activity and has been helpful, is being helpful, or is likely to be "
          "helpful to the detection or investigation or prosecution of that qualifying "
          "criminal activity.\" (Order at p. 1 [quoting statute].) \"Shall\" is mandatory. "
          "(Gov. Code, § 14.) Qualifying criminal activity includes \"unlawful criminal "
          "restraint; false imprisonment; ... obstruction of justice; perjury,\" and \"any "
          "similar activity in violation of Federal, State, or local criminal law.\" "
          "(8 U.S.C. § 1101(a)(15)(U)(iii).)"),
    ("sh", "IV.  ARGUMENT"),
    ("sh", "A.  The record establishes that probable cause was lacking."),
    ("p", "Probable cause exists when the facts known to the arresting officer would "
          "persuade someone of reasonable caution that the person arrested committed a "
          "crime. (People v. Thompson (2006) 38 Cal.4th 811, 818; Order at p. 3.) The "
          "question is what the officers actually observed. Here, CHP's contemporaneous "
          "recording of the entire encounter is the best evidence of that, and it records "
          "none of the indicia on which the report relies: no odor of alcohol, no slurred "
          "speech, no confusion or disorientation, and no alcoholic beverage—the only "
          "liquid examined was identified on the recording as urine. (Pet. Ex. 5; "
          "Newanforbi Decl. ¶¶ 7-10.)"),
    ("p", "What remains does not supply probable cause. Petitioner was lawfully parked "
          "and asleep with the engine off; resting on a freeway shoulder is what a tired "
          "driver is supposed to do. An empty container, with no odor and no observed "
          "impairment, says nothing about whether Petitioner had consumed alcohol, and he "
          "told the officers he had not. And the preliminary alcohol screening test was, "
          "as the officer told Petitioner on the recording, optional. (Pet. Ex. 5 at p. 10; "
          "Order at p. 3.) Declining a test the officer described as voluntary, after "
          "performing the field sobriety tests with no recorded sign of impairment, cannot "
          "convert an unsupported hunch into probable cause. The Court has already "
          "recognized that on these facts a finder of fact \"could reasonably find "
          "probable cause for arrest was lacking.\" (Order at p. 4, citing People v. "
          "Wolterman (1992) 11 Cal.App.4th Supp. 15, 18, and Espinoza v. Shiomoto (2017) "
          "10 Cal.App.5th 85, 101-102.)"),
    ("p", "CHP's own post-arrest conduct confirms the point. Within four days CHP "
          "certified that the event was \"a detention only, not an arrest\" because there "
          "were \"insufficient grounds for making a criminal complaint,\" and no charge was "
          "ever filed. (Pet. Ex. 7.) Petitioner does not contend that the certificate is an "
          "adjudication of probable cause. It is CHP's own contemporaneous determination "
          "that the arrest was not supported, and CHP's denial letter does not "
          "acknowledge it. [If the WAR913372 blood result is produced in response to "
          "Request for Production No. __ (due October 20, 2026), add: \"The blood drawn "
          "that night under warrant WAR913372 showed a blood-alcohol concentration of "
          "____. (Newanforbi Decl. ¶ __, Ex. __.)\"]"),
    ("sh", "B.  An arrest without probable cause, documented by a false report, is "
           "qualifying criminal activity."),
    ("p", "Handcuffing and jailing a person for four days without lawful authority is "
          "the \"unlawful violation of the personal liberty of another\" that defines false "
          "imprisonment (Pen. Code, § 236), and an officer who arrests a person without "
          "lawful authority commits a crime (Pen. Code, § 146). A peace officer who files a "
          "report knowing it contains false statements likewise commits a crime. (Pen. "
          "Code, § 118.1.) False imprisonment and unlawful criminal restraint are "
          "enumerated qualifying crimes, and a knowingly false report used to justify a "
          "detention is at minimum \"similar activity\" to the enumerated crimes of "
          "perjury and obstruction of justice. (8 U.S.C. § 1101(a)(15)(U)(iii).) Section "
          "679.10 does not require that the perpetrator have been charged, prosecuted, or "
          "convicted. (Pen. Code, § 679.10, subd. (k).)"),
    ("sh", "C.  Petitioner has been helpful, and CHP has never said otherwise."),
    ("p", "Petitioner reported the incident through a citizen complaint and a POST "
          "complaint, gave CHP a verbatim transcript of its own recording keyed by "
          "timestamp to each contradiction in its report, and has never refused a request "
          "for information or assistance. (Pet. ¶¶ 7, 87; Pet. Ex. 3; Newanforbi Decl. "
          "¶ 12.) CHP did not deny certification for lack of helpfulness; as the Court "
          "found, the denial rested on \"a wholly independent reason.\" (Order at p. 4.) "
          "The helpfulness element is satisfied on this record, and CHP cannot supply a "
          "new ground for the denial now."),
    ("sh", "D.  CHP abused its discretion, and the remedy is a writ commanding "
           "certification."),
    ("p", "An agency abuses its discretion when its decision is unsupported by the "
          "evidence before it. CHP's denial is contradicted by every record CHP itself "
          "generated, and it does not engage with any of them. Because the record admits "
          "only one conclusion—that Petitioner was the victim of qualifying criminal "
          "activity and has been helpful—section 679.10, subdivision (g)(1) leaves CHP "
          "nothing to weigh: the statute provides that the certifying official \"shall "
          "certify.\" The appropriate writ therefore commands CHP to set aside the April "
          "20, 2026 denial and to complete, sign, and deliver the certification within 30 "
          "days. (Code Civ. Proc., § 1085.)"),
    ("p", "In the alternative, if the Court concludes that CHP must make the "
          "determination in the first instance, Petitioner requests a writ setting aside "
          "the denial and commanding CHP to reconsider the request within 30 days in "
          "conformity with the Court's findings on the record, and to file a return within "
          "45 days so that the Court retains the ability to enforce compliance."),
    ("sh", "E.  Petitioner has no adequate alternative remedy."),
    ("p", "Section 679.10 provides no administrative appeal, and federal immigration "
          "authorities cannot compel a state agency to certify. (Pet. ¶ 77.) Without the "
          "certification, Petitioner cannot pursue a U-visa petition. A writ is the only "
          "remedy. (Code Civ. Proc., § 1086.)"),
    ("sh", "V.  CONCLUSION"),
    ("p", "Petitioner respectfully requests that the Court grant the motion, enter "
          "judgment on the First Cause of Action, and issue a peremptory writ of mandate "
          "commanding CHP to set aside its April 20, 2026 denial and to complete, sign, and "
          "deliver Form I-918, Supplement B within 30 days of service of the writ, or, in "
          "the alternative, to reconsider the request within 30 days in conformity with "
          "the Court's findings and file a return within 45 days."),
]

DECLARATION: list[tuple] = [
    ("n", "I, Brendan Ngehsi Newanforbi, declare:"),
    ("p", "1. I am the Petitioner in this action. I have personal knowledge of the facts "
          "stated in this declaration and, if called as a witness, could and would testify "
          "competently to them."),
    ("p", "2. The exhibits to the Petition referred to in the accompanying memorandum are "
          "true and correct copies of the documents they purport to be. Exhibit 1 is CHP's "
          "April 20, 2026 denial letter; Exhibits 2 and 3 are my April 9, 2026 request and "
          "supporting memorandum; Exhibit 5 is a transcript of CHP's November 1, 2024 "
          "dashcam recording that I prepared and that accurately reflects the recording; "
          "Exhibit 6 is CHP's arrest-investigation report; and Exhibit 7 is CHP's Penal "
          "Code section 851.6 certificate. The recording itself was lodged with the Court "
          "on September 8, 2026."),
    ("p", "3. Shortly before 1:00 a.m. on November 1, 2024, I was driving a rental vehicle "
          "home to Stockton. Because I was tired, I pulled onto the shoulder of eastbound "
          "Interstate 580 in Livermore, turned the engine off, and went to sleep."),
    ("p", "4. I had not consumed alcohol that night, and I told the officers so."),
    ("p", "5. I performed the field sobriety tests the officers administered. The officer "
          "told me that the preliminary alcohol screening test was not required. I "
          "declined it. I was then handcuffed and arrested."),
    ("p", "6. My blood was drawn at the officers' direction under a warrant. I was booked "
          "and held in custody until November 5, 2024."),
    ("p", "7. I have listened to the full dashcam recording. At no point does any officer "
          "state that he smells alcohol on my breath or person."),
    ("p", "8. On the recording, when an officer examined the only liquid found in the "
          "vehicle, he identified it aloud as urine."),
    ("p", "9. My speech on the recording is clear and responsive. I was not confused or "
          "disoriented, and the recording does not show that I was."),
    ("p", "10. CHP's report states that I had a strong odor of an alcoholic beverage, "
          "slurred speech, and a confused and disoriented demeanor, and that a beverage "
          "was present. Those statements are not true, and the recording does not support "
          "them."),
    ("p", "11. On November 5, 2024, CHP gave me the certificate attached to the Petition as "
          "Exhibit 7. No criminal charge was ever filed against me arising from the "
          "November 1, 2024 incident."),
    ("p", "12. Before I requested certification, I filed a citizen complaint with CHP and a "
          "complaint with POST about the incident, and I provided CHP a transcript of its "
          "recording identifying each contradiction by timestamp. No one from CHP or any "
          "other agency has ever asked me for information or assistance that I refused or "
          "failed to provide."),
    ("p", "I declare under penalty of perjury under the laws of the State of California "
          "that the foregoing is true and correct."),
]

PROPOSED_JUDGMENT: list[tuple] = [
    ("p", "The motion of Petitioner Brendan Ngehsi Newanforbi for a peremptory writ of "
          f"mandate on the First Cause of Action came on for hearing on {HEARING_DATE} in "
          "Department 25 of this Court, the Honorable Jenna M. Whitman presiding. Having "
          "considered the papers, the record, and the arguments presented, and good cause "
          "appearing,"),
    ("n", "IT IS ORDERED, ADJUDGED, AND DECREED:"),
    ("p", "1. The motion is GRANTED. Judgment is entered for Petitioner on the First Cause "
          "of Action."),
    ("p", "2. A peremptory writ of mandate shall issue commanding Respondent California "
          "Highway Patrol to set aside its April 20, 2026 denial of Petitioner's request "
          "for certification and, within 30 days after service of the writ, to complete, "
          "sign, and deliver to Petitioner Form I-918, Supplement B, U Nonimmigrant Status "
          "Certification, as requested on April 9, 2026.  [ALTERNATIVE: ...to reconsider "
          "Petitioner's April 9, 2026 request within 30 days after service of the writ in "
          "conformity with this Court's findings.]"),
    ("p", "3. Respondent shall file a return to the writ within 45 days after service of "
          "the writ. The Court retains jurisdiction until the return is filed and approved."),
    ("p", "4. Petitioner shall recover his costs as allowed by law."),
]

PROPOSED_WRIT: list[tuple] = [
    ("n", "TO RESPONDENT CALIFORNIA HIGHWAY PATROL:"),
    ("p", "Judgment having been entered in this action ordering that a peremptory writ of "
          "mandate issue,"),
    ("p", "YOU ARE COMMANDED, within 30 days after service of this writ, to set aside your "
          "April 20, 2026 denial of Petitioner Brendan Ngehsi Newanforbi's request for "
          "certification, and to complete, sign, and deliver to Petitioner Form I-918, "
          "Supplement B, U Nonimmigrant Status Certification, as requested on April 9, 2026."),
    ("p", "YOU ARE FURTHER COMMANDED to file with this Court, within 45 days after service "
          "of this writ, a return setting forth what you have done to comply."),
]

CMC_ATTACHMENT: list[tuple] = [
    ("p", "Petitioner submits this attachment to his Case Management Statement (CM-110) "
          "for the October 28, 2026 conference."),
    ("sh", "1.  Status of the pleadings."),
    ("p", "By Order of August 29, 2026, the Court overruled CHP's demurrer to the First "
          "Cause of Action (writ of mandate, Pen. Code, § 679.10), sustained it without "
          "leave as to the Second and Third Causes of Action, and sustained it with leave "
          "as to the Fourth. Petitioner did not amend and proceeds on the First Cause of "
          "Action alone. Respondents Dutra and Paul were dismissed by stipulation. "
          "[Confirm and state: CHP filed its answer on ________ / CHP has not filed an "
          "answer.]"),
    ("sh", "2.  Nature of the remaining proceeding."),
    ("p", "The First Cause of Action is a petition for writ of mandate to be decided by "
          "the Court on a noticed motion. No jury is available or requested, and no trial "
          "date is needed."),
    ("sh", "3.  Request to set the writ hearing and briefing schedule."),
    ("p", "Petitioner requests that the Court set the hearing on his Motion for Peremptory "
          f"Writ of Mandate on the First Cause of Action, reserved for {HEARING_DATE}, at "
          f"{HEARING_TIME} (Reservation ID {RESERVATION_ID}), or an earlier date if available, with CHP's opposition and Petitioner's reply due as provided by "
          "Code of Civil Procedure section 1005, subdivision (b), unless the Court orders "
          "otherwise."),
    ("sh", "4.  Discovery."),
    ("p", "Petitioner served Request for Production of Documents, Set One, on CHP on "
          "September 16, 2026, seeking the blood-draw warrant packet and toxicology result "
          "and CHP's file on the certification request. Responses are due October 20, 2026. "
          "Petitioner does not anticipate further discovery and does not ask that the "
          "hearing await it."),
    ("sh", "5.  Alternative dispute resolution."),
    ("p", "The dispute concerns whether CHP must execute a statutory certification. "
          "Petitioner is willing to discuss resolution with CHP but does not believe "
          "formal ADR would advance the case."),
]


# ---------------------------------------------------------------- render
def _header(d: PleadingPaper) -> None:
    c = d.c
    y0 = d._line_y(0)
    lines = [
        ("BRENDAN NGEHSI NEWANFORBI", "Times-Bold"),
        ("Petitioner In Pro Per", "Times-Roman"),
        ("1455 Cat Tail Drive", "Times-Roman"),
        ("Stockton, CA 95204", "Times-Roman"),
        ("Telephone: (209) 801-4442", "Times-Roman"),
        ("E-mail: bnn.cdl@gmail.com", "Times-Roman"),
    ]
    for i, (t, fn) in enumerate(lines):
        c.setFont(fn, 12)
        c.drawString(CONTENT_LEFT, y0 - i * 15, t)
    d.current_line = 4
    d.blank_line()
    d.write_line(COURT_LINE1, bold=True, center=True)
    d.write_line(COURT_LINE2, bold=True, center=True)
    d.blank_line()


def _render_blocks(d: PleadingPaper, blocks: list[tuple]) -> None:
    for blk in blocks:
        kind = blk[0]
        if kind == "b":
            d.blank_line()
        elif kind == "h":
            d.write_line(blk[1], bold=True, center=True)
        elif kind == "sh":
            d.ensure_space(3)
            d.write_wrapped(blk[1], bold=True, first_indent=0)
        elif kind == "n":
            d.write_wrapped(blk[1], first_indent=0)
        elif kind == "q":
            d.write_wrapped(blk[1], indent=36, first_indent=0)
        else:
            d.write_wrapped(blk[1])
        if kind in ("p", "n", "q"):
            d.blank_line()


def _sign(d: PleadingPaper, declaration: bool = False) -> None:
    d.ensure_space(7)
    if declaration:
        d.write_line(f"Executed on {EXEC_DATE}, at {EXEC_PLACE}.")
    else:
        d.write_line(f"Dated: {EXEC_DATE}")
    d.blank_line()
    d.blank_line()
    d.write_line(SIG_LINE, right=True, right_margin_offset=20)
    d.write_line("BRENDAN NGEHSI NEWANFORBI", bold=True, right=True, right_margin_offset=20)
    d.write_line("Petitioner, In Pro Per", right=True, right_margin_offset=20)


def _judge_sign(d: PleadingPaper) -> None:
    d.ensure_space(6)
    d.write_line("Dated: ____________________")
    d.blank_line()
    d.write_line(SIG_LINE, right=True, right_margin_offset=20)
    d.write_line("HON. JENNA M. WHITMAN", bold=True, right=True, right_margin_offset=20)
    d.write_line("Judge of the Superior Court", right=True, right_margin_offset=20)


def build(path: Path, footer: str, title: list[str], blocks: list[tuple], *,
          hearing: bool = True, sign: str = "party") -> Path:
    path.parent.mkdir(parents=True, exist_ok=True)
    d = PleadingPaper(str(path), doc_title_footer=footer)
    _header(d)
    d.draw_caption_block(CAPTION_LEFT, caption_right(title, hearing), caption_size=10,
                         tight_lh=13, boxed=True)
    d.blank_line()
    _render_blocks(d, blocks)
    if sign == "party":
        _sign(d)
    elif sign == "declarant":
        _sign(d, declaration=True)
    elif sign == "judge":
        _judge_sign(d)
    elif sign == "clerk":
        d.ensure_space(6)
        d.write_line("Dated: ____________________")
        d.blank_line()
        d.write_line("CLERK OF THE SUPERIOR COURT", right=True, right_margin_offset=20)
        d.blank_line()
        d.write_line("By: ____________________, Deputy", right=True, right_margin_offset=20)
    d.save()
    return path


def build_docx(path: Path, title: str, blocks: list[tuple]) -> Path:
    from docx import Document
    from docx.enum.text import WD_ALIGN_PARAGRAPH
    from docx.shared import Pt
    import re

    doc = Document()
    st = doc.styles["Normal"]
    st.font.name = "Times New Roman"
    st.font.size = Pt(12)
    p = doc.add_paragraph()
    p.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p.add_run(title).bold = True
    for blk in blocks:
        if blk[0] == "b":
            continue
        text = re.sub(r"<<(?:b|i|bi):([^>]*)>>", r"\1", blk[1])
        para = doc.add_paragraph()
        run = para.add_run(text)
        if blk[0] in ("h", "sh"):
            run.bold = True
        if blk[0] == "h":
            para.alignment = WD_ALIGN_PARAGRAPH.CENTER
        para.paragraph_format.line_spacing = 2.0 if blk[0] == "p" else 1.0
        if blk[0] == "p":
            para.paragraph_format.first_line_indent = Pt(36)
    doc.save(str(path))
    return path


def main() -> None:
    tag = "DRAFT, Sep 30 2026"
    docs = [
        ("Motion for Peremptory Writ of Mandate - Count 1 - Notice, MPA",
         "MOTION FOR PEREMPTORY WRIT — NEWANFORBI v. CHP, 26CV191136",
         ["NOTICE OF MOTION AND MOTION", "FOR PEREMPTORY WRIT OF",
          "MANDATE (FIRST CAUSE OF", "ACTION); MEMORANDUM OF",
          "POINTS AND AUTHORITIES", "[Code Civ. Proc., §§ 1085, 1094]"],
         NOTICE_AND_MPA, True, "party"),
        ("Declaration of Petitioner ISO Motion for Peremptory Writ",
         "DECLARATION ISO MOTION FOR WRIT — NEWANFORBI v. CHP, 26CV191136",
         ["DECLARATION OF BRENDAN", "NGEHSI NEWANFORBI IN", "SUPPORT OF MOTION FOR",
          "PEREMPTORY WRIT OF MANDATE"],
         DECLARATION, True, "declarant"),
        ("[Proposed] Judgment Granting Peremptory Writ of Mandate",
         "[PROPOSED] JUDGMENT — NEWANFORBI v. CHP, 26CV191136",
         ["[PROPOSED] JUDGMENT GRANTING", "PEREMPTORY WRIT OF MANDATE"],
         PROPOSED_JUDGMENT, True, "judge"),
        ("[Proposed] Peremptory Writ of Mandate",
         "[PROPOSED] PEREMPTORY WRIT — NEWANFORBI v. CHP, 26CV191136",
         ["[PROPOSED] PEREMPTORY WRIT", "OF MANDATE"],
         PROPOSED_WRIT, False, "clerk"),
        ("Attachment to Case Management Statement CM-110 (Oct 28 2026 CMC)",
         "CMC STATEMENT ATTACHMENT — NEWANFORBI v. CHP, 26CV191136",
         ["ATTACHMENT TO PETITIONER'S", "CASE MANAGEMENT STATEMENT", "",
          "CMC: October 28, 2026, 4:00 p.m."],
         CMC_ATTACHMENT, False, "party"),
    ]
    for name, footer, title, blocks, hearing, sign in docs:
        pdf = OUT / f"{name} ({tag}).pdf"
        build(pdf, footer, title, blocks, hearing=hearing, sign=sign)
        build_docx(OUT / f"{name} ({tag}).docx", " ".join(t for t in title if t), blocks)
        print(f"Wrote {pdf}")


if __name__ == "__main__":
    main()
