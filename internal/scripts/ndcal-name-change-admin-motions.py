#!/usr/bin/env python3
"""N.D. Cal. Civil L.R. 7-11 administrative motions to swap Plaintiff's
docket name to Brendan Ngwa Nforbi (first Brendan; last Ngwa Nforbi).

These are Plaintiff's requests — not Civil L.R. 7-12 stipulations.
Counsel who have signaled they will not oppose once the request is
made: Haiyang A. Li (24, 32); Blaze Van Dine and Eric Martinez (28).
Do not recite non-opposition for Amazon / Accurate (29) or Tigno /
McMahon (33). A 7-11 still lies in those two actions; the declaration
says a stipulation could not be obtained and does not invent consent.

  python3 internal/scripts/ndcal-name-change-admin-motions.py

Dated September 14, 2026. Signed. Do not treat as filed.
"""
from __future__ import annotations

import sys
from dataclasses import dataclass, field
from pathlib import Path

SCRIPT_DIR = Path(__file__).resolve().parent
sys.path.insert(0, str(SCRIPT_DIR))
sys.path.insert(0, str(SCRIPT_DIR / "lib"))

from exhibit_cover import write_exhibit_cover  # noqa: E402
from pdf_packet import assemble  # noqa: E402
from pleading_paper import CONTENT_LEFT, PleadingPaper  # noqa: E402
from proof_of_service import (  # noqa: E402
    DISTRICT_NDCAL,
    ProofOfServiceFields,
    build_proof_of_service,
)
from short_link import publish_short_link  # noqa: E402
from signature_stamp import SIGNATURE_NATIVE_PX, SIGNATURE_PATH  # noqa: E402

ROOT = SCRIPT_DIR.parent
DOCS = ROOT / "public/documents"
EXEC_DATE = "September 14, 2026"
MAIL_FROM = "San Jose, California"
NEW_NAME = "Brendan Ngwa Nforbi"
NEW_NAME_CAPS = "BRENDAN NGWA NFORBI"
FIRST_NAME = "Brendan"
LAST_NAME = "Ngwa Nforbi"
BOLD_FIRST = f"<<b:{FIRST_NAME}>>"
BOLD_LAST = f"<<b:{LAST_NAME}>>"
BOLD_NAME = f"{BOLD_FIRST} {BOLD_LAST}"
BOLD_NAME_CAPS = "<<b:BRENDAN>> <<b:NGWA NFORBI>>"
FIRST_LAST_GLOSS = (
    f"first name {BOLD_FIRST}, last name {BOLD_LAST}"
)
SIG_LINE = "___________________________________"
HELP_DESK = (
    DOCS
    / "matter-28"
    / (
        "Gmail - Re Pro se e-filing one account two name forms - "
        "CAND ECF Help Desk (Received Sep 1 2026).pdf"
    )
)

ATTY = [
    (NEW_NAME_CAPS, "Times-Bold", 12),
    ("Plaintiff, In Propria Persona", "Times-Roman", 12),
    ("1455 Cat Tail Drive", "Times-Roman", 12),
    ("Stockton, CA 95204", "Times-Roman", 12),
    ("Telephone: (209) 801-4442", "Times-Roman", 12),
    ("E-mail: bnn.cdl@gmail.com", "Times-Roman", 12),
]


@dataclass
class NameCase:
    matter: int
    slug: str
    out_dir: Path
    case_no: str
    judge: str
    footer: str
    current_docket_name: str
    caption_left: list[tuple[str, bool, bool]]
    defendant_pos_lines: list[str]
    defendants_short: str
    pos_recipients: list[str]
    conferral_decl: str
    motion_conferral: str
    preserve: list[str]
    unopposed: bool
    short_slug: str
    file_short: str
    extra_right: list[tuple[str, bool, bool]] = field(default_factory=list)
    email_to: list[str] = field(default_factory=list)
    email_extra: str = ""
    caption_short: str = ""

    @property
    def file_tag(self) -> str:
        docket = self.case_no.replace(":", "-")
        return f"{self.file_short} (N.D. Cal. {docket})"


CASES: list[NameCase] = [
    NameCase(
        matter=24,
        slug="serrato",
        out_dir=DOCS / "matter-24",
        case_no="4:26-cv-05953-ASK",
        judge="Hon. Ajay S. Krishnan",
        footer="ADMIN. MOTION TO CONFORM PLAINTIFF'S NAME -- NEWANFORBI v. SERRATO",
        current_docket_name="Brendan Ngehsi Newanforbi",
        caption_left=[
            ("BRENDAN NGEHSI NEWANFORBI,", True, False),
            ("", False, False),
            ("                          Plaintiff,", False, False),
            ("", False, False),
            ("       v.", False, False),
            ("", False, False),
            ("CAPTAIN G. SERRATO; and", True, False),
            ("DOES 1-10, inclusive,", True, False),
            ("", False, False),
            ("                          Defendants.", False, False),
        ],
        defendant_pos_lines=["CAPTAIN G. SERRATO"],
        defendants_short="Captain G. Serrato",
        pos_recipients=[
            "Haiyang A. Li, Deputy Attorney General",
            "Office of the Attorney General",
            "300 South Spring Street, Suite 1702",
            "Los Angeles, CA 90013-1230",
            "Haiyang.Li@doj.ca.gov",
            "Attorney for Defendant Captain G. Serrato",
        ],
        conferral_decl=(
            "I conferred with Deputy Attorney General Haiyang A. Li, counsel "
            "of record for Defendant Captain G. Serrato. He stated that "
            "Defendant will not oppose a request that the Clerk identify "
            f"Plaintiff as {BOLD_NAME}. He did not agree to enter a Civil "
            "L.R. 7-12 stipulation. That is why this motion is not "
            "accompanied by a stipulation."
        ),
        motion_conferral=(
            "Plaintiff conferred with Deputy Attorney General Haiyang A. Li. "
            "He stated Defendant will not oppose this request. He did not "
            "agree to a Civil L.R. 7-12 stipulation. The accompanying "
            "declaration satisfies Civil L.R. 7-11(a)."
        ),
        preserve=[
            "the continued initial case management conference (Dkt. 25: "
            "fourteen days after the final order on Defendant's motion to "
            "dismiss)",
            "the September 30, 2026 hearing on Defendant's motion to dismiss "
            "(Dkt. 18 / Dkt. 21)",
            "the Rule 26(a)(1), Joint CMC Statement, and ADR-certification "
            "dates reset by Dkt. 25 to run from that continued conference",
            "Defendant's pending motion (Dkt. 18) and Plaintiff's opposition",
        ],
        unopposed=True,
        short_slug="name-24",
        file_short="Serrato",
        email_to=["Haiyang.Li@doj.ca.gov"],
        caption_short="NEWANFORBI v. SERRATO",
    ),
    NameCase(
        matter=28,
        slug="smith",
        out_dir=DOCS / "matter-28",
        case_no="3:26-cv-07504-LJC",
        judge="Hon. Lisa J. Cisneros",
        footer="ADMIN. MOTION TO CONFORM PLAINTIFF'S NAME -- NEWANFORBI v. SMITH",
        current_docket_name="Brendan Ngehsi Newanforbi",
        caption_left=[
            ("BRENDAN NGEHSI NEWANFORBI,", True, False),
            ("", False, False),
            ("                          Plaintiff,", False, False),
            ("", False, False),
            ("       v.", False, False),
            ("", False, False),
            ("SHANNON SMITH, LCSW;", True, False),
            ("HOPE PSYCHOTHERAPY, INC.; and", True, False),
            ("DOES 1-10, inclusive,", True, False),
            ("", False, False),
            ("                          Defendants.", False, False),
        ],
        defendant_pos_lines=[
            "SHANNON SMITH, LCSW;",
            "HOPE PSYCHOTHERAPY, INC.",
        ],
        defendants_short="Shannon Smith, LCSW, and HOPE Psychotherapy, Inc.",
        pos_recipients=[
            "Blaze Van Dine, Esq.",
            "Eric T. Martinez, Esq.",
            "SIMS, LAWRENCE & BROGHAMMER",
            "1478 Stone Point Drive, Suite 450",
            "Roseville, CA 95661",
            "blaze@sims-law.net",
            "emartinez@sims-law.net",
            "slb-eservice@sims-law.net",
            "Counsel for Shannon Smith, LCSW, and HOPE Psychotherapy, Inc.",
        ],
        conferral_decl=(
            "I conferred with Blaze Van Dine and Eric Martinez of Sims, "
            "Lawrence & Broghammer, counsel for Defendants. They stated "
            "Defendants will not oppose a request that the Clerk identify "
            f"Plaintiff as {BOLD_NAME} so long as the paper makes clear that "
            "the two name forms are one person. This motion and this "
            "declaration do that. They did not agree to enter a Civil L.R. "
            "7-12 stipulation. That is why this motion is not accompanied "
            "by a stipulation."
        ),
        motion_conferral=(
            "Plaintiff conferred with Blaze Van Dine and Eric Martinez. "
            "They stated Defendants will not oppose this request if the "
            "paper makes clear that the two name forms are one person. "
            "Section II and the accompanying declaration do that. They did "
            "not agree to a Civil L.R. 7-12 stipulation. The accompanying "
            "declaration satisfies Civil L.R. 7-11(a)."
        ),
        preserve=[
            "Defendants' September 21, 2026 deadline to answer or otherwise "
            "respond (from the August 31, 2026 accepted service)",
            "the October 15, 2026 joint case management statement",
            "the October 22, 2026 initial case management conference",
        ],
        unopposed=True,
        short_slug="name-28",
        file_short="Smith",
        email_to=[
            "blaze@sims-law.net",
            "emartinez@sims-law.net",
            "slb-eservice@sims-law.net",
        ],
        email_extra=(
            "This is the request we discussed September 10: same person as "
            "Brendan Ngehsi Newanforbi; PACER login bngwanforbi; September 21, "
            "October 15, and October 22 stay put. I am not asking you to "
            "stipulate or to sign.\n"
        ),
        caption_short="NEWANFORBI v. SMITH",
    ),
    NameCase(
        matter=29,
        slug="amazon",
        out_dir=DOCS / "matter-29",
        case_no="4:26-cv-09249-ASK",
        judge="Hon. Ajay S. Krishnan",
        footer="ADMIN. MOTION TO CONFORM PLAINTIFF'S NAME -- NEWANFORBI v. AMAZON",
        current_docket_name="Brendan Ngehsi Newanforbi",
        caption_left=[
            ("BRENDAN NGEHSI NEWANFORBI,", True, False),
            ("", False, False),
            ("                          Plaintiff,", False, False),
            ("", False, False),
            ("       v.", False, False),
            ("", False, False),
            ("AMAZON.COM SERVICES, LLC;", True, False),
            ("ACCURATE BACKGROUND LLC; and", True, False),
            ("DOES 1-10, inclusive,", True, False),
            ("", False, False),
            ("                          Defendants.", False, False),
        ],
        defendant_pos_lines=[
            "AMAZON.COM SERVICES, LLC;",
            "ACCURATE BACKGROUND LLC",
        ],
        defendants_short="Amazon.com Services, LLC, and Accurate Background LLC",
        pos_recipients=[
            "Andrew P. Frederick",
            "Morgan, Lewis & Bockius LLP",
            "1400 Page Mill Road",
            "Palo Alto, CA 94304",
            "andrew.frederick@morganlewis.com",
            "Attorneys for Amazon.com Services, LLC",
            "",
            "Jasmine J. Stanzick",
            "Seyfarth Shaw LLP",
            "2029 Century Park East, Suite 3500",
            "Los Angeles, CA 90067-3021",
            "jstanzick@seyfarth.com",
            "Attorneys for Accurate Background LLC",
        ],
        conferral_decl=(
            "I have communicated with Andrew P. Frederick, counsel for "
            "Amazon.com Services, LLC, and Jasmine J. Stanzick, counsel for "
            "Accurate Background LLC. Neither has stated that Defendants "
            "will not oppose this request. Neither has agreed to a Civil "
            "L.R. 7-12 stipulation. That is why this motion is not "
            "accompanied by a stipulation. Civil L.R. 7-11(b) gives them "
            "four days after filing to oppose or support."
        ),
        motion_conferral=(
            "Plaintiff has not obtained a statement of non-opposition from "
            "counsel for Amazon.com Services, LLC, or Accurate Background "
            "LLC. A Civil L.R. 7-12 stipulation could not be obtained. The "
            "accompanying declaration satisfies Civil L.R. 7-11(a). Counsel "
            "may file a Civil L.R. 7-11(b) response within four days."
        ),
        preserve=[
            "both Defendants' September 22, 2026 deadlines to answer or "
            "otherwise respond (Dkts. 6 and 7)",
            "both Defendants' September 22, 2026 magistrate-consent clocks "
            "(Dkts. 6 and 7)",
            "the December 1, 2026 initial case management conference",
        ],
        unopposed=False,
        short_slug="name-29",
        file_short="Amazon",
        email_to=[
            "andrew.frederick@morganlewis.com",
            "jstanzick@seyfarth.com",
        ],
        email_extra=(
            "I am not representing that Amazon or Accurate has agreed or "
            "will not oppose. Civil L.R. 7-11(b) gives you four days after "
            "filing to oppose or support. If you will state non-opposition "
            "in writing before I file, I will recite it.\n"
        ),
        caption_short="NEWANFORBI v. AMAZON",
    ),
    NameCase(
        matter=32,
        slug="meza",
        out_dir=DOCS / "matter-32/ndcal",
        case_no="4:26-cv-08271-ASK",
        judge="Hon. Ajay S. Krishnan",
        footer="ADMIN. MOTION TO CONFORM PLAINTIFF'S NAME -- NFORBI v. MEZA-GONZALEZ",
        current_docket_name="Ngwa Nforbi",
        caption_left=[
            ("NGWA NFORBI,", True, False),
            ("", False, False),
            ("                          Plaintiff,", False, False),
            ("", False, False),
            ("       v.", False, False),
            ("", False, False),
            ("SANTIAGO MEZA-GONZALEZ;", True, False),
            ("JOSE MELANO; and", True, False),
            ("DOES 1-10, inclusive,", True, False),
            ("", False, False),
            ("                          Defendants.", False, False),
        ],
        defendant_pos_lines=[
            "SANTIAGO MEZA-GONZALEZ;",
            "JOSE MELANO",
        ],
        defendants_short="Santiago Meza-Gonzalez and Jose Melano",
        pos_recipients=[
            "Haiyang A. Li, Deputy Attorney General",
            "Office of the Attorney General",
            "300 South Spring Street, Suite 1702",
            "Los Angeles, CA 90013-1230",
            "Haiyang.Li@doj.ca.gov",
            "Related Serrato counsel; Dkt. 13 accept-service motion pending",
        ],
        conferral_decl=(
            "I conferred with Deputy Attorney General Haiyang A. Li. He is "
            "counsel of record for Captain Serrato in the related action "
            "and is the attorney named in Plaintiff's pending Civil L.R. "
            "7-11 motion that he accept service for Officer Meza-Gonzalez "
            "(Dkt. 13). He stated he will not oppose a request that the "
            f"Clerk identify Plaintiff as {BOLD_NAME}. He has not filed a "
            "notice of appearance in this action. His statement is "
            "non-opposition to this caption request. It is not a notice of "
            "appearance and not acceptance of service. A Civil L.R. 7-12 "
            "stipulation could not be obtained because he is not counsel of "
            "record here and did not agree to stipulate. Officer Melano has "
            "been served."
        ),
        motion_conferral=(
            "Plaintiff conferred with Deputy Attorney General Haiyang A. Li. "
            "He stated he will not oppose this request. He has not appeared "
            "in this action. His statement is non-opposition to this "
            "caption request — not an appearance and not acceptance of "
            "service. Dkt. 13 remains pending. A Civil L.R. 7-12 stipulation "
            "could not be obtained. The accompanying declaration satisfies "
            "Civil L.R. 7-11(a)."
        ),
        preserve=[
            "Plaintiff's pending administrative motion that DAG Li accept "
            "service for Officer Meza-Gonzalez (Dkt. 13)",
            "any case-management date the Court sets after the August 24, "
            "2026 related-case reassignment",
            "Plaintiff's obligation to file the Rule 4(l) return for "
            "Officer Meza-Gonzalez",
        ],
        unopposed=True,
        short_slug="name-32",
        file_short="Meza-Gonzalez",
        extra_right=[("Related: 4:26-cv-05953-ASK", False, False)],
        email_to=["Haiyang.Li@doj.ca.gov"],
        email_extra=(
            "Your statement is recited as non-opposition to this caption "
            "request only. It is not a notice of appearance and not "
            "acceptance of service on Officer Meza-Gonzalez. Dkt. 13 "
            "remains pending.\n"
        ),
        caption_short="NFORBI v. MEZA-GONZALEZ",
    ),
    NameCase(
        matter=33,
        slug="candelaria",
        out_dir=DOCS / "matter-33/ndcal",
        case_no="3:26-cv-08272-LJC",
        judge="Hon. Lisa J. Cisneros",
        footer="ADMIN. MOTION TO CONFORM PLAINTIFF'S NAME -- NFORBI v. CANDELARIA",
        current_docket_name="Ngwa Nforbi",
        caption_left=[
            ("NGWA NFORBI,", True, False),
            ("", False, False),
            ("                          Plaintiff,", False, False),
            ("", False, False),
            ("       v.", False, False),
            ("", False, False),
            ("DIANA CANDELARIA;", True, False),
            ("STEVE GORDON; and", True, False),
            ("DOES 1-10, inclusive,", True, False),
            ("", False, False),
            ("                          Defendants.", False, False),
        ],
        defendant_pos_lines=[
            "DIANA CANDELARIA;",
            "STEVE GORDON",
        ],
        defendants_short="Diana Candelaria and Steve Gordon",
        pos_recipients=[
            "Fiel Dizon Tigno, Supervising Deputy Attorney General",
            "William J. McMahon, Deputy Attorney General",
            "Office of the Attorney General, California Department of Justice",
            "1515 Clay Street, 20th Floor, P.O. Box 70550",
            "Oakland, CA 94612-0550",
            "fiel.tigno@doj.ca.gov",
            "William.McMahon@doj.ca.gov",
            "Attorneys for Defendants Diana Candelaria and Steve Gordon",
        ],
        conferral_decl=(
            "I conferred with William J. McMahon, who signed the Dkt. 11 "
            "Answer, and identified Fiel Dizon Tigno as PACER lead. Counsel "
            "discussed a stipulation. No Civil L.R. 7-12 stipulation was "
            "executed. Counsel have not stated that they will not oppose "
            "this administrative request. That is why this motion is not "
            "accompanied by a stipulation. Civil L.R. 7-11(b) gives them "
            "four days after filing to oppose or support."
        ),
        motion_conferral=(
            "Plaintiff conferred with counsel for Defendants. A stipulation "
            "was discussed. None was executed. Counsel have not stated that "
            "they will not oppose this request. The accompanying declaration "
            "satisfies Civil L.R. 7-11(a). Counsel may file a Civil L.R. "
            "7-11(b) response within four days."
        ),
        preserve=[
            "Defendants' September 22, 2026 deadline to consent or decline "
            "magistrate-judge jurisdiction (Dkt. 12)",
            "the October 22, 2026 ADR certification and Rule 26(f) conference",
            "the November 5, 2026 initial-disclosure and Joint Case Management "
            "Statement deadline",
            "the November 12, 2026 initial case management conference",
            "the Dkt. 11 Answer and any challenge to it",
            "the identification of Dkt. 6 as the operative First Amended "
            "Complaint",
        ],
        unopposed=False,
        short_slug="name-33",
        file_short="Candelaria",
        email_to=["fiel.tigno@doj.ca.gov", "William.McMahon@doj.ca.gov"],
        email_extra=(
            "I am not representing that you have stipulated or that you "
            "will not oppose. The September 10 authorization to file the "
            "then-attached stipulation does not apply to this motion. Civil "
            "L.R. 7-11(b) gives you four days after filing to oppose or "
            "support. If you will state non-opposition in writing before I "
            "file, I will recite it.\n"
        ),
        caption_short="NFORBI v. CANDELARIA",
    ),
]


def _header(d: PleadingPaper) -> None:
    atty_y = d._line_y(0)
    for i, (txt, fn, sz) in enumerate(ATTY):
        d.c.setFont(fn, sz)
        d.c.drawString(CONTENT_LEFT, atty_y - i * 14, txt)
    d.current_line = 4
    d.blank_line()
    d.write_line("UNITED STATES DISTRICT COURT", bold=True, center=True)
    d.write_line("NORTHERN DISTRICT OF CALIFORNIA", bold=True, center=True)
    d.blank_line()


def _caption(d: PleadingPaper, case: NameCase, right_title: list[str]) -> None:
    right = [
        (f"Case No. {case.case_no}", False, False),
        ("", False, False),
    ]
    for line in right_title:
        right.append((line, True, False))
    right.extend(
        [
            ("[Civil L.R. 7-11]", False, False),
            ("", False, False),
            (f"Judge: {case.judge}", False, False),
            *case.extra_right,
        ]
    )
    d.draw_caption_block(case.caption_left, right, caption_size=10, tight_lh=13, boxed=True)
    d.blank_line()


def _sign_for(d: PleadingPaper, case: NameCase, *, declaration: bool = False) -> None:
    d.ensure_space(8)
    if declaration:
        d.write_line("I declare under penalty of perjury that the foregoing")
        d.write_line(f"is true and correct. Executed on {EXEC_DATE},")
        d.write_line("at Stockton, California.")
    else:
        d.write_line(f"Dated: {EXEC_DATE}")
        d.blank_line()
        d.write_line("Respectfully submitted,", right=True, right_margin_offset=20)
    d.blank_line()
    d.draw_signature_image(
        SIGNATURE_PATH,
        SIGNATURE_NATIVE_PX[0],
        SIGNATURE_NATIVE_PX[1],
        SIG_LINE,
        width=185,
        x_offset=15,
        height_scale=1.0,
    )
    d.write_line(SIG_LINE, right=True, right_margin_offset=20)
    d.write_line(NEW_NAME_CAPS, bold=True, right=True, right_margin_offset=20)
    d.write_line("Plaintiff, In Propria Persona", right=True, right_margin_offset=20)
    d.write_line(
        f"(presently on this docket as {case.current_docket_name})",
        right=True,
        right_margin_offset=20,
        size=10,
    )


def _aka_other(case: NameCase) -> str:
    if case.current_docket_name != "Brendan Ngehsi Newanforbi":
        return " and as Brendan Ngehsi Newanforbi"
    return " and as Ngwa Nforbi"


def _motion_title() -> str:
    return "ADMINISTRATIVE MOTION TO CONFORM"


def _caption_title() -> list[str]:
    return [
        "ADMIN. MOTION",
        "TO CONFORM",
        "PLAINTIFF'S NAME",
        "ON THE DOCKET",
    ]


def _motion_path(case: NameCase) -> Path:
    return case.out_dir / (
        f"Administrative Motion - Conform Plaintiff's Name - "
        f"{case.file_tag} ({EXEC_DATE}).pdf"
    )


def _decl_path(case: NameCase) -> Path:
    return case.out_dir / (
        f"Declaration ISO Administrative Motion - Conform Plaintiff's Name - "
        f"{case.file_tag} ({EXEC_DATE}).pdf"
    )


def _order_path(case: NameCase) -> Path:
    return case.out_dir / (
        f"Proposed Order - Conform Plaintiff's Name - "
        f"{case.file_tag} ({EXEC_DATE}).pdf"
    )


def _pos_path(case: NameCase) -> Path:
    return case.out_dir / (
        f"Proof of Service - Name Conform Administrative Motion - "
        f"{case.file_tag} ({EXEC_DATE}).pdf"
    )


def _packet_path(case: NameCase) -> Path:
    return case.out_dir / (
        f"Name Conform Administrative Motion Packet - "
        f"{case.file_tag} ({EXEC_DATE}).pdf"
    )


def _cover_path(case: NameCase) -> Path:
    return case.out_dir / (
        f"Exhibit A Cover - ECF Help Desk - {case.file_tag} ({EXEC_DATE}).pdf"
    )


def _email_path(case: NameCase) -> Path:
    return case.out_dir / f"EMAIL_DRAFT_Name_Conform_Admin_Motion_{case.slug}.txt"


def build_motion(case: NameCase) -> Path:
    path = _motion_path(case)
    path.parent.mkdir(parents=True, exist_ok=True)
    d = PleadingPaper(str(path), doc_title_footer=case.footer)
    _header(d)
    _caption(d, case, _caption_title())
    d.write_line(_motion_title(), bold=True, center=True)
    d.write_line("PLAINTIFF'S NAME ON THE DOCKET", bold=True, center=True)
    d.blank_line()
    d.write_wrapped(
        f"TO THE COURT AND TO {case.defendants_short.upper()}, THROUGH COUNSEL:",
        first_indent=0,
    )
    d.blank_line()
    d.write_wrapped(
        f"Plaintiff {BOLD_NAME}, appearing in propria persona and presently "
        f"identified on this docket as {case.current_docket_name}, moves under "
        "Civil Local Rule 7-11 for an order conforming the docket name. This "
        "is Plaintiff's request. It is not a Civil L.R. 7-12 stipulation.",
        first_indent=0,
    )
    d.blank_line()
    d.ensure_space(3)
    d.write_line("I.", bold=True, center=True)
    d.write_line("RELIEF REQUESTED", bold=True, center=True)
    d.blank_line()
    d.write_wrapped(
        f"The Clerk shall amend the docket, the short title, the CM/ECF "
        f"party record, and the caption of this action so that Plaintiff is "
        f"identified as {BOLD_NAME} — {FIRST_LAST_GLOSS} — matching "
        f"Plaintiff's existing PACER account (login "
        f"bngwanforbi). This is a clean swap of the party name. Subsequent "
        f"papers shall use that caption.",
        first_indent=0,
    )
    d.blank_line()
    d.ensure_space(3)
    d.write_line("II.", bold=True, center=True)
    d.write_line("THE TWO NAMES ARE ONE PERSON", bold=True, center=True)
    d.blank_line()
    d.write_wrapped(
        f"{BOLD_NAME} is the same natural person as {case.current_docket_name}"
        f"{_aka_other(case)}. The names are one person. This motion does not "
        "add, drop, or substitute any party. It is not an amendment of any "
        "claim, defense, or operative pleading. It is not a Fed. R. Civ. P. "
        "25 substitution.",
        first_indent=0,
    )
    d.blank_line()
    d.ensure_space(3)
    d.write_line("III.", bold=True, center=True)
    d.write_line("THE ECF HELP DESK CANNOT LINK THE ACCOUNT", bold=True, center=True)
    d.write_line("UNTIL THE DOCKET MATCHES", bold=True, center=True)
    d.blank_line()
    d.write_wrapped(
        "On September 1, 2026 the CAND ECF Help Desk advised that it cannot "
        "link this action to PACER login bngwanforbi until the docket "
        "reflects the name on the account, and that a name change requires "
        "a request to the Court. Exhibit A is that reply. After the Clerk "
        "updates the party name, Plaintiff will ask the Help Desk to link "
        "that login for pro se e-filing. This motion does not itself "
        "activate e-filing.",
        first_indent=0,
    )
    d.blank_line()
    d.write_wrapped(
        "Plaintiff recently learned that this District permits pro se "
        "litigants to e-file. Good cause exists to conform the docket name "
        "so that login can be linked. Among other things, e-filing will "
        "prevent the delay inherent in mailing papers to the Clerk and to "
        "counsel, wherever those papers are sent from; it will put each "
        "paper on the docket the "
        "day it is filed rather than days later in the mail; it will let "
        "counsel of record receive service the same day; and it will let "
        "Plaintiff prosecute these five open N.D. Cal. actions on one "
        "account instead of mailing five copies of every paper. Mailing "
        "also carries weekend and holiday lag and the risk that a paper "
        "reaches the Clerk after the date it was sent.",
        first_indent=0,
    )
    d.blank_line()
    d.ensure_space(3)
    d.write_line("IV.", bold=True, center=True)
    d.write_line("CIVIL L.R. 7-11", bold=True, center=True)
    d.blank_line()
    d.write_wrapped(
        "Conforming a pro se party's docket name so one PACER account can "
        "be linked is a miscellaneous administrative matter. A 35-day "
        "noticed motion is unnecessary. Civil L.R. 7-11(a) requires a "
        "proposed order and either a Civil L.R. 7-12 stipulation or a "
        "declaration explaining why a stipulation could not be obtained. "
        f"{case.motion_conferral}",
        first_indent=0,
    )
    d.blank_line()
    d.ensure_space(3)
    d.write_line("V.", bold=True, center=True)
    d.write_line("NOTHING ELSE MOVES", bold=True, center=True)
    d.blank_line()
    d.write_wrapped(
        "All prior filings, proofs of service, acceptances of service, "
        "orders, and related-case determinations remain effective as to the "
        "same person. No party need be re-served. <<b:No other date or "
        "deadline in this action is modified.>> This motion is not a stay "
        "of discovery. Expressly unchanged, without limitation: "
        f"{'; '.join(case.preserve)}.",
        first_indent=0,
    )
    d.blank_line()
    d.write_wrapped(
        "Nothing in this motion is a waiver of any claim, defense, "
        "objection, or right except the identity of Plaintiff as the same "
        "natural person and the docket name requested in Section I.",
        first_indent=0,
    )
    d.blank_line()
    d.write_wrapped(
        "A declaration, Exhibit A, and a proposed order accompany this motion.",
        first_indent=0,
    )
    d.blank_line()
    _sign_for(d, case)
    d.save()
    return path


def build_declaration(case: NameCase) -> Path:
    path = _decl_path(case)
    d = PleadingPaper(
        str(path),
        doc_title_footer=f"DECLARATION ISO ADMIN. MOTION -- {case.case_no}",
    )
    _header(d)
    _caption(
        d,
        case,
        [
            "DECLARATION OF BRENDAN",
            "NGWA NFORBI ISO",
            "ADMINISTRATIVE MOTION",
        ],
    )
    d.write_line("DECLARATION OF BRENDAN NGWA NFORBI", bold=True, center=True)
    d.blank_line()
    d.write_wrapped(
        f"I, {BOLD_NAME_CAPS}, declare as follows:",
        first_indent=0,
    )
    d.blank_line()
    d.write_wrapped(
        "1.  I am the Plaintiff in this action. I am over eighteen. I make "
        "this declaration from personal knowledge in support of Plaintiff's "
        "Civil L.R. 7-11 administrative motion to conform the Plaintiff "
        "name on this docket. If called, I could and would testify "
        "competently to these facts.",
        first_indent=0,
    )
    d.blank_line()
    d.write_wrapped(
        f"2.  I am the same natural person as {case.current_docket_name}"
        f"{_aka_other(case)}. The names are one person. I am not asking the "
        "Court to add, drop, or substitute any party.",
        first_indent=0,
    )
    d.blank_line()
    d.write_wrapped(
        "3.  My PACER login is bngwanforbi. On September 1, 2026 I asked "
        "the CAND ECF Help Desk to link that account to this action and to "
        "my other N.D. Cal. actions. The Help Desk replied the same day "
        "that it cannot link an action to that account until the docket "
        "reflects the name on the account, and that a name change requires "
        "a request to the Court. A true copy of that reply is Exhibit A.",
        first_indent=0,
    )
    d.blank_line()
    d.write_wrapped(
        f"4.  {case.conferral_decl}",
        first_indent=0,
    )
    d.blank_line()
    d.write_wrapped(
        "5.  I recently learned that this District permits pro se "
        "litigants to e-file. That is why I asked the ECF Help Desk on "
        "September 1, 2026 to link PACER login bngwanforbi. Until the "
        "docket name matches, I must mail papers. Mailing introduces "
        "delay wherever the papers are sent from: transit time to the "
        "Clerk and to counsel, weekend and holiday lag, and the risk that "
        "a paper reaches the "
        "Clerk or counsel after the date I sent it. I have five open "
        "actions in this District. Conforming the name so I can e-file "
        "will avoid that delay, let the Clerk and counsel receive papers "
        "the same day, and let me use one PACER account instead of "
        "mailing each paper five times.",
        first_indent=0,
    )
    d.blank_line()
    d.write_wrapped(
        "6.  I am not asking the Court to move any deadline, hearing, "
        "conference, pending motion, or discovery obligation. After the "
        "Clerk updates the party name I will ask the ECF Help Desk to link "
        "PACER login bngwanforbi for pro se e-filing.",
        first_indent=0,
    )
    d.blank_line()
    _sign_for(d, case, declaration=True)
    d.save()
    return path


def build_order(case: NameCase) -> Path:
    path = _order_path(case)
    d = PleadingPaper(
        str(path),
        doc_title_footer=f"[PROPOSED] ORDER CONFORMING PLAINTIFF'S NAME -- {case.case_no}",
    )
    _header(d)
    _caption(
        d,
        case,
        [
            "[PROPOSED] ORDER CONFORMING",
            "PLAINTIFF'S NAME ON THE DOCKET",
        ],
    )
    d.write_line("[PROPOSED] ORDER", bold=True, center=True)
    d.blank_line()
    considered = "Plaintiff's Civil L.R. 7-11 administrative motion"
    d.write_wrapped(
        f"The Court has considered {considered} to conform Plaintiff's "
        "name on the docket, the supporting declaration, and Exhibit A. "
        "Good cause appearing — including so that the docket will match "
        "PACER login bngwanforbi, the ECF Help Desk may link that account "
        "for pro se e-filing, and Plaintiff may file and serve without the "
        "delay inherent in mailing papers to the Clerk and to counsel — "
        "IT IS ORDERED that:",
        first_indent=0,
    )
    d.blank_line()
    d.write_wrapped(
        f"1.  The Clerk shall amend the docket, the short title, the "
        f"CM/ECF party record, and the caption of this action so that "
        f"Plaintiff is identified as {BOLD_NAME} ({FIRST_LAST_GLOSS}), "
        f"matching PACER login bngwanforbi. "
        f"Subsequent papers shall use that caption.",
        first_indent=0,
    )
    d.blank_line()
    d.write_wrapped(
        f"2.  {BOLD_NAME} is the same natural person previously identified "
        f"on this docket as {case.current_docket_name}. This Order does not "
        "add, drop, or substitute any party and does not amend any claim "
        "or defense.",
        first_indent=0,
    )
    d.blank_line()
    d.write_wrapped(
        "3.  All prior filings, service, acceptances of service, and orders "
        "remain effective. No party need be re-served by reason of this Order.",
        first_indent=0,
    )
    d.blank_line()
    d.write_wrapped(
        "4.  No deadline, hearing, conference, pending motion, or discovery "
        "obligation is modified.",
        first_indent=0,
    )
    d.blank_line()
    d.ensure_space(9)
    d.write_line("IT IS SO ORDERED.", bold=True)
    d.blank_line()
    d.blank_line()
    d.write_line("Dated: ________________")
    d.blank_line()
    d.blank_line()
    d.blank_line()
    d.write_line(SIG_LINE)
    d.write_line(case.judge)
    d.write_line("United States Magistrate Judge")
    d.save()
    return path


def build_exhibit_cover(case: NameCase) -> Path:
    path = _cover_path(case)
    write_exhibit_cover(
        path,
        court="UNITED STATES DISTRICT COURT",
        court_line2="NORTHERN DISTRICT OF CALIFORNIA",
        caption=case.caption_short or case.footer,
        case_no=f"Case No. {case.case_no}",
        exhibit="A",
        title="CAND ECF Help Desk reply (September 1, 2026)",
        details=[
            "Cannot link PACER login bngwanforbi until the docket",
            "reflects the name on the account; name change requires",
            "a request to the Court.",
        ],
        footer=f"Admin. motion to conform Plaintiff's name — {case.case_no}",
    )
    return path


def build_pos(case: NameCase) -> Path:
    path = _pos_path(case)
    title = (
        "Civil L.R. 7-11 Administrative Motion to Conform Plaintiff's "
        f"Name on the Docket; Declaration; Exhibit A; [Proposed] Order ({EXEC_DATE})"
    )
    build_proof_of_service(
        path,
        ProofOfServiceFields(
            plaintiff_line=case.current_docket_name.upper(),
            plaintiff_role="Plaintiff",
            defendant_lines=case.defendant_pos_lines,
            defendant_role="Defendant",
            case_number=case.case_no,
            service_date=EXEC_DATE,
            document_title=title,
            mailing_location=MAIL_FROM,
            recipients=case.pos_recipients,
            server_name=NEW_NAME,
            stamp_signature=True,
            district_line=DISTRICT_NDCAL,
            by_email=True,
            signature_on_second_page=True,
        ),
    )
    return path


def build_email(case: NameCase) -> Path:
    path = _email_path(case)
    to = "; ".join(case.email_to) if case.email_to else "[counsel]"
    subject = (
        f"{case.case_no} — Civil L.R. 7-11 administrative motion to conform "
        f"Plaintiff's name to {NEW_NAME}"
    )
    if case.unopposed:
        posture = (
            "You stated you will not oppose this request once made. I am "
            "not asking you to stipulate or to sign. The attached paper is "
            "Plaintiff's Civil L.R. 7-11 motion, declaration, Exhibit A "
            "(the September 1 ECF Help Desk reply), proposed order, and "
            "proof of service."
        )
    else:
        posture = (
            "I have not treated you as having stipulated or as having "
            "stated non-opposition. The attached paper is Plaintiff's "
            "Civil L.R. 7-11 motion. Civil L.R. 7-11(b) gives you four "
            "days after filing to oppose or support."
        )
    body = f"""To: {to}
Subject: {subject}

Counsel:

I am filing a Civil L.R. 7-11 administrative motion asking the Court
to conform the Plaintiff name on this docket to {NEW_NAME}
(first name Brendan; last name Ngwa Nforbi).

This is a request to the Court. It is not a stipulation.

{posture}
{("" if not case.email_extra else chr(10) + case.email_extra)}
The two name forms are one person. No deadline, hearing, or pending
motion moves. I recently learned this District permits pro se
e-filing; conforming the name lets the Help Desk link the account
and avoids the delay of mailing papers.

After the Clerk updates the party name I will ask the ECF Help Desk
to link PACER login bngwanforbi for pro se e-filing.

Thank you,
{NEW_NAME}
(209) 801-4442
bnn.cdl@gmail.com
"""
    path.write_text(body)
    return path


def main() -> None:
    if not Path(SIGNATURE_PATH).is_file():
        raise SystemExit(f"Missing signature image: {SIGNATURE_PATH}")
    if not HELP_DESK.is_file():
        raise SystemExit(f"Missing Help Desk exhibit: {HELP_DESK}")
    for case in CASES:
        motion = build_motion(case)
        decl = build_declaration(case)
        cover = build_exhibit_cover(case)
        order = build_order(case)
        pos = build_pos(case)
        packet = _packet_path(case)
        assemble([motion, decl, cover, HELP_DESK, order, pos], packet)
        email = build_email(case)
        short = publish_short_link(packet, case.short_slug)
        print(f"M{case.matter} {case.slug} unopposed={case.unopposed}:")
        print(f"  {motion}")
        print(f"  {decl}")
        print(f"  {order}")
        print(f"  {pos}")
        print(f"  {packet}")
        print(f"  {email}")
        print(f"  {short}")


if __name__ == "__main__":
    main()
