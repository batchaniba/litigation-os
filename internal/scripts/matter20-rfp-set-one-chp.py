#!/usr/bin/env python3
"""Matter 20 — Petitioner's Request for Production of Documents, Set One,
to Respondent California Highway Patrol.

Alameda Super. Ct. No. 26CV191136, Dept. 25 (Hon. Jenna M. Whitman).

Count 1 survived the August 29, 2026 order: whether the November 1, 2024
incident involved qualifying criminal activity because probable cause for
DUI was lacking. This demand is that paper ask — warrant packet WAR913372,
blood / toxicology, and the April 2026 certification file. It is not a
deposition notice, not a Pitchess demand, and not a Matter 32 damages set.

Discovery in a writ is served, not e-filed. CRC 3.250. Do not send
Department 25 a copy.

  python3 internal/scripts/matter20-rfp-set-one-chp.py

FILED_STATUS: False until served on DAG Ing. Do not treat as filed.
"""
from __future__ import annotations

import os
import sys
from pathlib import Path

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, SCRIPT_DIR)
sys.path.insert(0, os.path.join(SCRIPT_DIR, "lib"))

from pleading_paper import (  # noqa: E402
    CONTENT_LEFT,
    COURT_LINE1,
    PleadingPaper,
)
from signature_stamp import SIGNATURE_NATIVE_PX, SIGNATURE_PATH  # noqa: E402
import pymupdf  # noqa: E402

SIGNATURE_IMG = SIGNATURE_PATH
SIG_IMG_W_PX, SIG_IMG_H_PX = SIGNATURE_NATIVE_PX

FILED_STATUS = False

EXEC_DATE = "September 16, 2026"
EXEC_PLACE = "Stockton, California"
CMC_DATE = "October 28, 2026"
CMC_TIME = "4:00 p.m."
# CCP § 2031.260 (30 days) from Sep. 16, computed under CCP § 12, plus
# two court days under CCP § 1010.6 for electronic service: Tuesday,
# October 20, 2026. Indigenous Peoples' Day is October 12.
RESPONSE_DATE = "October 20, 2026"
PRODUCTION_DATE = "October 20, 2026"

COURT_LINE2 = "COUNTY OF ALAMEDA"
DOC_TITLE_FOOTER = (
    "RFP SET ONE (CHP) — NEWANFORBI v. CHP, ET AL., 26CV191136"
)
SIG_LINE = "___________________________________"

REPO_ROOT = os.path.abspath(os.path.join(SCRIPT_DIR, "..", ".."))
MATTER20 = Path(REPO_ROOT) / "internal" / "public" / "documents" / "matter-20"
RFP_PATH = MATTER20 / (
    "Request for Production of Documents Set One - CHP (Sep 16 2026).pdf"
)
POS_PATH = MATTER20 / (
    "Proof of Electronic Service - RFP Set One CHP (Sep 16 2026).pdf"
)
EMAIL_PATH = MATTER20 / "EMAIL_DRAFT_Ing_RFP_Set_One_CHP.txt"
PACKET_PATH = MATTER20 / (
    "Request for Production of Documents Set One - CHP with POS "
    "(Sep 16 2026).pdf"
)

COVER_EMAIL = f"""To: Vanessa.Ing@doj.ca.gov
Cc: Mark.Beckington@doj.ca.gov
Subject: Newanforbi v. California Highway Patrol et al., No. 26CV191136 — Petitioner's Request for Production of Documents, Set One

Attach:
- Request for Production of Documents Set One - CHP (Sep 16 2026).pdf
- Proof of Electronic Service - RFP Set One CHP (Sep 16 2026).pdf

---

Ms. Ing:

Please find enclosed Petitioner's Request for Production of Documents, Set One, directed to Respondent California Highway Patrol, together with proof of electronic service.

The Demand is limited to surviving Count 1. It seeks the WAR913372 warrant packet, the November 1, 2024 blood-draw chain of custody and toxicology, and the file of the April 9, 2026 U-visa certification request and April 20, 2026 denial. Electronic production to bnn.cdl@gmail.com is requested. Written responses and production are due as stated in the Demand. If this Demand is served today, written responses and production are due {RESPONSE_DATE}.

This is a discovery demand. It is not being filed with the Court.

Thank you,

Brendan Ngwa Nforbi
Plaintiff, In Propria Persona

---
Note to self (do not send this footer):
Draft of {EXEC_DATE}. NOT YET TRANSMITTED.
- Attach the two PDFs named above. Do not paste the Demand into the email body. Do not send the combined "with POS" packet as a substitute for the two attachments.
- The proof is a party-signed CCP § 1013b certificate. Do not substitute Judicial Council POS-050; that form recites the server is not a party.
- Do not e-file the Demand or proof of service. CRC 3.250. The September 8 lodging POS was rejected at the portal; do not repeat that.
- Do not cc Department 25.
- Cc Mark.Beckington@doj.ca.gov because he was on Ms. Ing's September 10 thread. To: Vanessa.Ing@doj.ca.gov is the service address. That address is on the proof.
- If you send after September 16, regenerate so the Demand signature date, response date, and proof-of-service date match the actual send date.
- Do not mention Matter 32, Franks, qualified immunity, punitive damages, or depositions in the email.
- Do not notice Meza or Melano with this send. Documents first.
- Do not convert Count 4 into a damages prayer to "open" this discovery. Count 1 already supports it.
- If a lab sheet is already in hand, attach it to the Matter 32 FAC and lodge it here; do not wait on this Demand for a document you have.
"""


def _header(d: PleadingPaper) -> None:
    c = d.c
    atty_y = d._line_y(0)
    atty_lh = 15
    atty_lines = [
        ("BRENDAN NGEHSI NEWANFORBI", "Times-Bold", 12),
        ("Petitioner In Pro Per", "Times-Roman", 12),
        ("1455 Cat Tail Drive", "Times-Roman", 12),
        ("Stockton, CA 95204", "Times-Roman", 12),
        ("Telephone: (209) 801-4442", "Times-Roman", 12),
        ("E-mail: bnn.cdl@gmail.com", "Times-Roman", 12),
    ]
    for i, (txt, fn, sz) in enumerate(atty_lines):
        c.setFont(fn, sz)
        c.drawString(CONTENT_LEFT, atty_y - i * atty_lh, txt)
    d.current_line = 4
    d.blank_line()
    d.write_line(COURT_LINE1, bold=True, center=True)
    d.write_line(COURT_LINE2, bold=True, center=True)
    d.blank_line()


def _caption(d: PleadingPaper, *, proof: bool = False) -> None:
    left = [
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
    if proof:
        title = [
            ("PROOF OF ELECTRONIC SERVICE", True, False),
            ("[Code Civ. Proc. § 1013b]", False, False),
        ]
    else:
        title = [
            ("PETITIONER'S REQUEST FOR", True, False),
            ("PRODUCTION OF DOCUMENTS,", True, False),
            ("SET ONE, TO RESPONDENT", True, False),
            ("CALIFORNIA HIGHWAY PATROL", True, False),
        ]
    right = [
        ("Case No. 26CV191136", False, False),
        ("", False, False),
        *title,
        ("", False, False),
        (f"CMC:  {CMC_DATE}", False, False),
        (f"Time:  {CMC_TIME}", False, False),
        ("Assigned for All Purposes to:", False, False),
        ("Hon. Jenna M. Whitman, Dept. 25", False, False),
        ("", False, False),
        ("Action Filed: May 29, 2026", False, False),
        ("Trial Date:   Not set", False, False),
        ("", False, False),
        ("[Discovery — not for filing]", False, True),
    ]
    d.draw_caption_block(left, right, caption_size=10, tight_lh=13, boxed=True)
    d.blank_line()


def _sign(d: PleadingPaper, executed_line: str) -> None:
    d.ensure_space(11)
    d.write_line(executed_line)
    d.blank_line()
    d.blank_line()
    d.draw_signature_image(
        SIGNATURE_IMG,
        SIG_IMG_W_PX,
        SIG_IMG_H_PX,
        SIG_LINE,
        width=165,
        x_offset=15,
    )
    d.write_line(SIG_LINE, right=True, right_margin_offset=20)
    d.blank_line()
    d.write_line(
        "BRENDAN NGEHSI NEWANFORBI",
        bold=True,
        right=True,
        right_margin_offset=20,
    )
    d.write_line("Petitioner, In Pro Per", right=True, right_margin_offset=20)


def _heading(d: PleadingPaper, text: str) -> None:
    d.ensure_space(3)
    d.write_line(text, bold=True, center=True)
    d.blank_line()


def _para(d: PleadingPaper, text: str, first_indent: int = 36) -> None:
    d.write_wrapped(text, first_indent=first_indent)
    d.blank_line()


def _request(d: PleadingPaper, number: int, text: str) -> None:
    d.ensure_space(4)
    d.write_wrapped(f"<<b:REQUEST NO. {number}.>>  {text}", first_indent=0)
    d.blank_line()


def build_rfp(path: Path) -> Path:
    path.parent.mkdir(parents=True, exist_ok=True)
    d = PleadingPaper(str(path), doc_title_footer=DOC_TITLE_FOOTER)
    _header(d)
    _caption(d)

    d.write_line("PETITIONER'S REQUEST FOR PRODUCTION OF", bold=True, center=True)
    d.write_line("DOCUMENTS, SET ONE, TO RESPONDENT", bold=True, center=True)
    d.write_line("CALIFORNIA HIGHWAY PATROL", bold=True, center=True)
    d.blank_line()

    _para(
        d,
        "TO RESPONDENT CALIFORNIA HIGHWAY PATROL AND TO ITS ATTORNEY "
        "OF RECORD:",
        first_indent=0,
    )
    _para(
        d,
        "Petitioner Brendan Ngehsi Newanforbi, appearing in propria persona, "
        "demands that Respondent California Highway Patrol produce the "
        "DOCUMENTS described below for inspection and copying pursuant to "
        "Code of Civil Procedure sections 2016.010, 2016.020, 2017.010, and "
        "2031.010 et seq.",
    )
    _para(
        d,
        "This is a special proceeding of a civil nature. Code of Civil "
        "Procedure section 2016.020, subdivision (a), defines \"action\" to "
        "include a civil action and a special proceeding of a civil nature. "
        "The Civil Discovery Act therefore applies. Respondent California "
        "Highway Patrol appeared in this proceeding. More than ten days have "
        "passed since that appearance. Code Civ. Proc. § 2031.020(b).",
    )
    _para(
        d,
        "The Demand is directed to surviving Count 1 of the Verified Petition "
        "for Writ of Mandate, as framed by the Court's August 29, 2026 Order "
        "Sustaining Demurrer in Part, with Leave to Amend (notice of entry "
        "August 31, 2026): whether the November 1, 2024 incident involved "
        "qualifying criminal activity in light of the claimed absence of "
        "probable cause for driving under the influence. Count 1 challenges "
        "an informal, five-sentence certification denial dated April 20, "
        "2026. That denial was not the product of a formal evidentiary "
        "hearing under Code of Civil Procedure section 1094.5.",
    )
    _para(
        d,
        "Petitioner seeks the paper that proves or kills that decision: what "
        "was shown to Judge A. Sekany to obtain blood-draw warrant WAR913372; "
        "the blood-draw and laboratory record; and the file Respondent "
        "considered, reviewed, possessed, or had available when Captain G. "
        "Serrato denied Form I-918 Supplement B certification on April 20, "
        "2026.",
    )

    _heading(d, "I.  DEFINITIONS")

    _para(
        d,
        "1.  \"YOU,\" \"YOUR,\" and \"RESPONDENT\" mean Respondent California "
        "Highway Patrol, including the Dublin Area office, Headquarters, and "
        "all officers, employees, agents, and representatives, including "
        "without limitation Officer Santiago Meza-Gonzalez (Badge 023295), "
        "Officer Jose Melano (Badge 023054), Captain G. Serrato, Lieutenant "
        "Gary Paul, Sergeant Eric Dutra, and phlebotomist Aziza Ghaleb, and "
        "anyone else acting on YOUR behalf.",
        first_indent=0,
    )
    _para(
        d,
        "2.  \"PETITIONER\" means Brendan Ngehsi Newanforbi, also identified "
        "in YOUR records as Brendan Ngwa Nforbi, driver license F7953179.",
        first_indent=0,
    )
    _para(
        d,
        "3.  \"INCIDENT\" means the November 1, 2024 encounter on Interstate "
        "580 East, Livermore, California, CHP Case No. RJ68845, CAD No. "
        "241101GG0064, including the stop, detention, arrest, transport, "
        "blood draw, and booking under CAR913358.",
        first_indent=0,
    )
    _para(
        d,
        "4.  \"WARRANT\" means search warrant WAR913372, presented to and "
        "signed by Judge A. Sekany on or about November 1, 2024, at "
        "approximately 2:34 a.m., authorizing a blood draw from PETITIONER.",
        first_indent=0,
    )
    _para(
        d,
        "5.  \"CERTIFICATION REQUEST\" means PETITIONER's April 9, 2026 "
        "request that YOU certify Form I-918 Supplement B under Penal Code "
        "section 679.10, including the pre-completed form and supporting "
        "memorandum and exhibits.",
        first_indent=0,
    )
    _para(
        d,
        "6.  \"DENIAL\" means the April 20, 2026 letter from Captain G. "
        "Serrato denying the CERTIFICATION REQUEST, File No. "
        "390.18437.17620.26-050, and every draft, routing, and enclosure.",
        first_indent=0,
    )
    _para(
        d,
        "7.  \"DOCUMENT\" and \"DOCUMENTS\" mean any writing as defined in "
        "Evidence Code section 250, including electronically stored "
        "information: paper, PDF, email, CAD and MDC records, text or chat "
        "messages, photographs, audio, video, laboratory printouts, chain-of-"
        "custody forms, warrant-system entries, and any other record, "
        "whether original, copy, draft, or metadata-bearing native file.",
        first_indent=0,
    )
    _para(
        d,
        "8.  \"COMMUNICATION\" means any DOCUMENT that records, transmits, or "
        "reflects information exchanged between two or more persons, "
        "including email, memorandum, CAD notes, MDC messages, text, letter, "
        "and recorded conversation.",
        first_indent=0,
    )
    _para(
        d,
        "9.  \"POSSESSION, CUSTODY, OR CONTROL\" means DOCUMENTS in YOUR "
        "actual possession or custody, or that YOU have a legal right to "
        "obtain on demand. It does not include a record merely because YOU "
        "might be able to request a copy from an independent custodian. If "
        "the Alameda County Superior Court, the Department of Justice, Bureau "
        "of Forensic Services, or another independent custodian exclusively "
        "holds a responsive DOCUMENT, state that fact and IDENTIFY the "
        "custodian.",
        first_indent=0,
    )
    _para(
        d,
        "10.  \"IDENTIFY,\" when used as to a DOCUMENT not produced, means "
        "state the title or description, date, author, recipient, present "
        "custodian, last known address of that custodian, and the reason the "
        "DOCUMENT is not in YOUR POSSESSION, CUSTODY, OR CONTROL.",
        first_indent=0,
    )

    _heading(d, "II.  INSTRUCTIONS")

    _para(
        d,
        "A.  Time of production.  Serve a written response and produce the "
        "DOCUMENTS within the time required by Code of Civil Procedure "
        "sections 2031.260 and 1010.6. If this Demand is electronically "
        f"served on {EXEC_DATE}, written responses and production are due "
        f"{RESPONSE_DATE}. If service occurs later, the statutory deadline "
        "controls.",
        first_indent=0,
    )
    _para(
        d,
        "B.  Place and manner.  Produce electronically to "
        "bnn.cdl@gmail.com, in searchable PDF, or in native format for ESI "
        "that is not reasonably converted to PDF. Bates-stamp each page. If "
        "YOU elect physical production, the place of inspection is 1455 Cat "
        "Tail Drive, Stockton, California 95204, between 10:00 a.m. and "
        f"4:00 p.m. on {PRODUCTION_DATE}. Related activity: copying, "
        "scanning, and photographing. Code Civ. Proc. § 2031.030(c).",
        first_indent=0,
    )
    _para(
        d,
        "C.  Response format.  For each request, respond as Code of Civil "
        "Procedure sections 2031.210 through 2031.280 require: produce; "
        "state an inability to comply under section 2031.230; or object "
        "with specificity under section 2031.240. An inability-to-comply "
        "response must state whether the item never existed, was lost, "
        "misplaced, stolen, or destroyed, or has never been, or is no "
        "longer, in YOUR POSSESSION, CUSTODY, OR CONTROL, and must IDENTIFY "
        "the person or entity believed to have the DOCUMENT, including the "
        "Alameda County Superior Court, the Department of Justice, Bureau of "
        "Forensic Services, or any other laboratory or prosecutor.",
        first_indent=0,
    )
    _para(
        d,
        "D.  Privilege.  If YOU withhold any DOCUMENT based on privilege or "
        "work product, comply with Code of Civil Procedure section 2031.240 "
        "and provide sufficient factual information to evaluate the claim, "
        "including a privilege log if necessary. Produce all reasonably "
        "segregable non-privileged portions. If Evidence Code section 1040 "
        "is asserted, state the basis for the claim with sufficient "
        "specificity to permit evaluation.",
        first_indent=0,
    )
    _para(
        d,
        "E.  Sealed warrant materials.  If any portion of the WARRANT file "
        "is sealed, so state, IDENTIFY the sealing order by court, date, "
        "and case or warrant number, produce every unsealed portion, and "
        "produce the sealing order itself.",
        first_indent=0,
    )
    _para(
        d,
        "F.  Documents already served.  If a DOCUMENT was previously served "
        "in this proceeding (including the November 1, 2024 dashcam lodging "
        "of September 8, 2026), YOU may IDENTIFY it by date of service and "
        "description rather than re-produce it, unless the copy previously "
        "served was incomplete, redacted, or not the original-quality file.",
        first_indent=0,
    )
    _para(
        d,
        "G.  Scope and Pitchess carveout.  These requests reach DOCUMENTS in "
        "YOUR POSSESSION, CUSTODY, OR CONTROL. They do not seek peace-officer "
        "personnel records, citizen-complaint investigation files, or other "
        "records subject to Evidence Code sections 1043 through 1045; "
        "training histories; or DOCUMENTS concerning unrelated stops. To the "
        "extent a responsive record is withheld as Pitchess material, state "
        "that basis without disclosing protected contents. This Set One does "
        "not notice any deposition.",
        first_indent=0,
    )
    _para(
        d,
        "H.  Protective order.  If YOU contend a responsive, non-privileged "
        "DOCUMENT requires confidentiality protection, identify the claimed "
        "basis and meet and confer promptly regarding an appropriate "
        "protective order. Nothing in this instruction requires disclosure "
        "of privileged or statutorily protected material.",
        first_indent=0,
    )

    _heading(d, "III.  REQUESTS FOR PRODUCTION")

    _request(
        d,
        1,
        "The complete search-warrant package for WAR913372, including: "
        "(a) the application; (b) the affidavit and any supplemental "
        "affidavit or statement; (c) all attachments, exhibits, and "
        "incorporated writings; (d) every electronic-warrant submission, "
        "transmittal, confirmation, or system record (including any Alameda "
        "County e-warrant or WAR-system entry); (e) the warrant signed by "
        "Judge A. Sekany on or about November 1, 2024, at approximately "
        "2:34 a.m.; (f) the return; (g) the inventory; and (h) any sealing, "
        "unsealing, or access order concerning the warrant or affidavit.",
    )
    _request(
        d,
        2,
        "Every DOCUMENT reflecting the factual showing made to Judge A. "
        "Sekany to obtain the WARRANT, including any draft affidavit, "
        "officer declaration, CHP Form 202, DS-367, CAD printout, "
        "photograph, dashcam still, or other writing presented, transmitted, "
        "read, or summarized to the magistrate, and any note of what was "
        "said to the magistrate that is not already contained in the "
        "package produced in response to Request No. 1.",
    )
    _request(
        d,
        3,
        "Every chain-of-custody DOCUMENT for the blood vials drawn from "
        "PETITIONER on November 1, 2024, in connection with the INCIDENT "
        "and the WARRANT, including collection forms, kit identifiers, "
        "vial labels, seals, storage logs, and the identity of the person "
        "who drew the blood (including Aziza Ghaleb, if that person drew "
        "the blood) and of every person who thereafter took custody of "
        "either vial.",
    )
    _request(
        d,
        4,
        "Every DOCUMENT reflecting the submission or transmittal of "
        "PETITIONER's blood samples from the INCIDENT to the California "
        "Department of Justice, Bureau of Forensic Services, or any other "
        "laboratory, including the sample identifier, laboratory request, "
        "shipping or courier record, and any acknowledgment of receipt.",
    )
    _request(
        d,
        5,
        "The complete toxicology, blood-alcohol, and forensic laboratory "
        "file for PETITIONER's November 1, 2024 blood samples, including "
        "every preliminary, amended, supplemental, and final report, "
        "printout, chromatogram, analyst notes, and result of 0.00 or any "
        "other value, whether or not a numerical BAC is reported.",
    )
    _request(
        d,
        6,
        "Every DOCUMENT showing the date YOU received any laboratory result "
        "described in Request No. 5, and the identity of each person who "
        "received, reviewed, routed, or was informed of that result, "
        "including any DOCUMENT showing whether the result was in YOUR "
        "POSSESSION, CUSTODY, OR CONTROL on or before April 20, 2026.",
    )
    _request(
        d,
        7,
        "Non-privileged operational COMMUNICATIONS from November 1, 2024 "
        "through April 20, 2026 concerning: (a) the WARRANT; (b) the blood "
        "draw from PETITIONER and laboratory testing of that blood; (c) the "
        "transmittal, receipt, routing, or review of any laboratory result; "
        "(d) whether to refer criminal charges arising from the INCIDENT; "
        "or (e) the CERTIFICATION REQUEST or DENIAL. This request includes "
        "responsive communications with the Alameda County District "
        "Attorney's Office, the Department of Justice or laboratory, and CHP "
        "personnel. It excludes attorney-client communications, attorney work "
        "product, communications created solely for this litigation, and "
        "communications about unrelated investigations.",
    )
    _request(
        d,
        8,
        "The non-Pitchess certification-decision file that Captain G. "
        "Serrato or YOU considered, reviewed, or actually had available when "
        "evaluating the CERTIFICATION REQUEST and issuing the DENIAL, "
        "including: (a) the April 9, 2026 request and attachments; (b) the "
        "April 10, 2026 communication from Lieutenant Gary Paul; (c) the "
        "April 20, 2026 DENIAL and drafts; (d) CHP Form 202, DS-367, the "
        "November 5, 2024 Detention Certificate, and dashcam or transcript, "
        "to the extent reviewed or actually available and not already "
        "produced in complete form; and (e) any non-privileged note, routing "
        "slip, checklist, or legal guidance used in the certification "
        "evaluation. This request expressly excludes peace-officer personnel "
        "records, citizen-complaint investigation files, and other records "
        "subject to Evidence Code sections 1043 through 1045.",
    )

    _heading(d, "IV.  RESERVATION")

    _para(
        d,
        "Petitioner reserves the right to serve additional discovery, "
        "including further document demands and, if warranted, nonparty "
        "deposition or business-records subpoenas under Code of Civil "
        "Procedure section 2020.010 et seq. This Set One does not waive "
        "that right. It does not notice any deposition.",
    )

    d.write_respectfully_submitted()
    _sign(d, f"Dated: {EXEC_DATE}")
    d.save()
    return path


def build_pos(path: Path) -> Path:
    """Build a party-signed proof of electronic service under CCP § 1013b.

    POS-050 is not used because its printed declaration states the server is
    not a party to the action. Petitioner is a party and may electronically
    serve discovery, so this proof states the true facts without that
    inapplicable preprinted representation.
    """
    path.parent.mkdir(parents=True, exist_ok=True)
    d = PleadingPaper(str(path), doc_title_footer=(
        "PROOF OF ELECTRONIC SERVICE — RFP SET ONE (CHP) — "
        "NEWANFORBI v. CHP, ET AL., 26CV191136"
    ))
    _header(d)
    _caption(d, proof=True)
    d.write_line("PROOF OF ELECTRONIC SERVICE", bold=True, center=True)
    d.write_line("[Code Civ. Proc. § 1013b]", center=True)
    d.blank_line()
    _para(
        d,
        "I, Brendan Ngehsi Newanforbi, declare:",
        first_indent=0,
    )
    _para(
        d,
        "1.  I am over the age of 18 years and am the Petitioner in this "
        "action. I am a party. My electronic service address is "
        "bnn.cdl@gmail.com. My mailing address is 1455 Cat Tail Drive, "
        "Stockton, California 95204.",
        first_indent=0,
    )
    _para(
        d,
        f"2.  On {EXEC_DATE}, I electronically served the following "
        "document:",
        first_indent=0,
    )
    _para(
        d,
        "Petitioner's Request for Production of Documents, Set One, to "
        "Respondent California Highway Patrol",
        first_indent=36,
    )
    _para(
        d,
        "by transmitting a true copy by electronic mail from "
        "bnn.cdl@gmail.com to Vanessa K. Ing, Deputy Attorney General, "
        "counsel of record for Respondent California Highway Patrol, at "
        "Vanessa.Ing@doj.ca.gov.",
        first_indent=0,
    )
    _para(
        d,
        "3.  I transmitted a courtesy copy of the same document to "
        "Mark.Beckington@doj.ca.gov. Mr. Beckington is not the addressee of "
        "service.",
        first_indent=0,
    )
    _para(
        d,
        "4.  I did not receive, within a reasonable time after the "
        "transmission, any electronic message or other indication that the "
        "transmission was unsuccessful.",
        first_indent=0,
    )
    _para(
        d,
        "5.  I declare under penalty of perjury under the laws of the State "
        f"of California that the foregoing is true and correct. Executed on "
        f"{EXEC_DATE}, at {EXEC_PLACE}.",
        first_indent=0,
    )
    _sign(d, f"Dated: {EXEC_DATE}")
    d.save()
    return path


def build_email(path: Path) -> Path:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(COVER_EMAIL, encoding="utf-8")
    return path


def build_packet(rfp: Path, pos: Path, dest: Path) -> Path:
    dest.parent.mkdir(parents=True, exist_ok=True)
    out = pymupdf.open()
    for src_path in (rfp, pos):
        src = pymupdf.open(src_path)
        out.insert_pdf(src)
        src.close()
    out.save(dest)
    out.close()
    return dest


def main() -> None:
    if not os.path.isfile(SIGNATURE_IMG):
        raise SystemExit(f"Missing universal signature: {SIGNATURE_IMG}")
    MATTER20.mkdir(parents=True, exist_ok=True)
    build_rfp(RFP_PATH)
    build_pos(POS_PATH)
    build_email(EMAIL_PATH)
    build_packet(RFP_PATH, POS_PATH, PACKET_PATH)
    print(f"SUCCESS! Generated: {RFP_PATH}")
    print(f"SUCCESS! Generated: {POS_PATH}")
    print(f"SUCCESS! Generated: {EMAIL_PATH}")
    print(f"SUCCESS! Generated: {PACKET_PATH}")
    if not FILED_STATUS:
        print("NOTE: FILED_STATUS is False -- not yet served. Do not e-file.")


if __name__ == "__main__":
    main()
