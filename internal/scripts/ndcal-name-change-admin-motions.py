#!/usr/bin/env python3
"""N.D. Cal. Civil L.R. 7-11 administrative motions to swap Plaintiff's
docket name to Brendan Ngwa Nforbi (first Brendan; last Ngwa Nforbi).

These are Plaintiff's requests — not Civil L.R. 7-12 stipulations.
Live posture as of September 11, 2026:

- Matter 33: McMahon revision accepted 1:29 p.m. Sep. 10. Do not file
  this 7-11 while that authorization is live.
- Matter 24 / 32: Li will not stipulate; will not oppose if the paper
  makes clear Nforbi and Newanforbi are the same person. Recite that.
  His 32 statement is not an appearance and not acceptance of service.
- Matter 28: Martinez will review a quieter stipulation; he does not
  intend to oppose a motion. File this 7-11 only if he declines the
  revised counterpart.
- Matter 29: Amazon is agreeable if both name forms are confirmed.
  Accurate asked for that confirmation and a government ID. Do not
  send an ID. Do not recite non-opposition until it is on the email
  record after the confirmation.

  python3 internal/scripts/ndcal-name-change-admin-motions.py

Dated September 14, 2026 except Matter 24 (Serrato), which is the
September 15, 2026 packet after Dkt. 29 reassignment to Judge Breyer
(3:26-cv-05953-CRB) and Dkt. 30's November 20, 2026 MTD hearing.
Signed. Do not treat as filed.

  python3 internal/scripts/ndcal-name-change-admin-motions.py --matter 24
"""
from __future__ import annotations

import argparse
import re
import sys
from dataclasses import dataclass, field
from pathlib import Path

SCRIPT_DIR = Path(__file__).resolve().parent
sys.path.insert(0, str(SCRIPT_DIR))
sys.path.insert(0, str(SCRIPT_DIR / "lib"))

from exhibit_cover import write_exhibit_cover  # noqa: E402
from pdf_packet import assemble  # noqa: E402
from pleading_paper import CONTENT_LEFT, CONTENT_RIGHT, PleadingPaper  # noqa: E402
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
# The full requested name stays roman. Other docket-name literals are
# bolded by _mark_name_tokens when the body is written.
BOLD_NAME = NEW_NAME
BOLD_NAME_CAPS = NEW_NAME_CAPS
FIRST_LAST_GLOSS = (
    f"first name {FIRST_NAME}, last name {LAST_NAME}"
)
SIG_LINE = "________________________________________"
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
    # If set, this docket recorded last name as a single token (Nforbi)
    # and the ask is to change that field to Ngwa Nforbi to match PACER.
    last_name_on_docket: str = ""
    # If set (24/28), change this middle+last token to Ngwa Nforbi.
    # Leave empty on Amazon — that packet stays on the generic ask.
    from_name_token: str = ""
    division: str = ""
    exec_date: str = ""
    signed_at: str = ""
    mail_from: str = ""
    judge_title: str = "United States Magistrate Judge"
    preserve_numbered: bool = False
    federal_jurat: bool = False
    user_draft: bool = False
    extra_short_slugs: dict[str, str] = field(default_factory=dict)

    @property
    def file_tag(self) -> str:
        docket = self.case_no.replace(":", "-")
        return f"{self.file_short} (N.D. Cal. {docket})"

    @property
    def dated(self) -> str:
        return self.exec_date or EXEC_DATE

    @property
    def place(self) -> str:
        return self.signed_at or "Milpitas, California"

    @property
    def pos_place(self) -> str:
        return self.mail_from or MAIL_FROM


CASES: list[NameCase] = [
    NameCase(
        matter=24,
        slug="serrato",
        out_dir=DOCS / "matter-24",
        case_no="3:26-cv-05953-CRB",
        judge="Hon. Charles R. Breyer",
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
            "Haiyang Allen Li, Deputy Attorney General",
            "Office of the Attorney General",
            "300 South Spring Street, Suite 1702",
            "Los Angeles, CA 90013-1230",
            "Haiyang.Li@doj.ca.gov",
            "Attorney for Defendant Captain G. Serrato",
        ],
        conferral_decl=(
            "Pursuant to Civil L.R. 7-11(a), I conferred with Deputy Attorney "
            "General Haiyang Allen Li, counsel of record for Defendant "
            "Captain G. Serrato. On September 10, 2026, Mr. Li stated that "
            "he does not believe a formal stipulation is required and that "
            "Defendant will not oppose an administrative motion so long as "
            'the paper makes clear that "Nforbi" and "Newanforbi" are the '
            "same person. This declaration and the accompanying motion "
            "expressly make that recital. Counsel did not execute a Civil "
            "L.R. 7-12 stipulation, which is why this motion is filed under "
            "Civil L.R. 7-11 with this explanatory declaration."
        ),
        motion_conferral=(
            "Pursuant to Civil L.R. 7-11(a), Plaintiff conferred with Deputy "
            "Attorney General Haiyang Allen Li, counsel of record for "
            "Defendant Captain G. Serrato. Mr. Li stated that Defendant does "
            "not believe a formal stipulation is required and will not "
            "oppose an administrative motion so long as the paper makes "
            'clear that "Nforbi" and "Newanforbi" are the same person. '
            "Section III above and the accompanying declaration explicitly "
            "make that confirmation. Counsel did not execute a Civil L.R. "
            "7-12 stipulation; the accompanying declaration explains why a "
            "stipulation was not obtained and satisfies Civil L.R. 7-11(a)."
        ),
        preserve=[
            "The November 20, 2026 hearing on Defendant's Motion to Dismiss "
            "(Dkt. 18, reset by Clerk's Notice Dkt. 30 to 10:00 a.m. Zoom "
            "before Judge Breyer);",
            "Defendant's pending Motion to Dismiss (Dkt. 18) and Plaintiff's "
            "filed Opposition (Dkt. 20);",
            "The continued initial Case Management Conference (continued by "
            "Dkt. 25 to fourteen days after the final order on Dkt. 18); and",
            "The Rule 26(a)(1) disclosures, Joint Case Management Statement, "
            "and ADR certification dates reset by Dkt. 25 to run from that "
            "continued conference.",
        ],
        unopposed=True,
        short_slug="name-24",
        file_short="Serrato",
        email_to=["Haiyang.Li@doj.ca.gov"],
        caption_short="NEWANFORBI v. SERRATO",
        from_name_token="Ngehsi Newanforbi",
        division="SAN FRANCISCO DIVISION",
        exec_date="September 15, 2026",
        signed_at="Stockton, California",
        mail_from="Stockton, California",
        judge_title="United States District Judge",
        preserve_numbered=True,
        federal_jurat=True,
        user_draft=True,
        extra_short_slugs={
            "motion": "name-24-motion",
            "decl": "name-24-decl",
            "order": "name-24-order",
        },
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
            "Lawrence & Broghammer, counsel for Defendants. On September "
            "11, 2026 Mr. Martinez wrote that he does not intend to oppose "
            "a request that the Clerk identify Plaintiff as "
            f"{NEW_NAME}, and that he would review a revised stipulation. "
            "A revised counterpart was sent. No Civil L.R. 7-12 "
            "stipulation was executed. That is why this motion is not "
            "accompanied by a stipulation. This motion and this "
            "declaration make clear that the two name forms are one person."
        ),
        motion_conferral=(
            "Plaintiff conferred with Blaze Van Dine and Eric Martinez. "
            "Mr. Martinez stated he does not intend to oppose this request. "
            "A revised stipulation was offered. None was executed. Section "
            "II and the accompanying declaration make clear that the two "
            "name forms are one person. The accompanying declaration "
            "satisfies Civil L.R. 7-11(a)."
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
            "You said you do not intend to oppose. I am not asking you to "
            "sign. This motion is the fallback if the revised stipulation "
            "does not go on file.\n"
        ),
        caption_short="NEWANFORBI v. SMITH",
        from_name_token="Ngehsi Newanforbi",
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
            "Amazon.com Services, LLC, and John Drury and Jasmine J. "
            "Stanzick, counsel for Accurate Background LLC. On September "
            "11, 2026 Mr. Frederick wrote that Amazon is agreeable if I "
            "confirm that both name forms are names I use. Mr. Drury asked "
            "for that confirmation and for a government ID. I am confirming "
            "the names. I am not circulating a government ID. "
            "No Civil L.R. 7-12 stipulation has been executed. That is "
            "why this motion is not accompanied by a stipulation. Civil "
            "L.R. 7-11(b) gives them four days after filing to oppose or "
            "support."
        ),
        motion_conferral=(
            "Plaintiff conferred with counsel for Amazon.com Services, LLC, "
            "and Accurate Background LLC. Amazon stated it is agreeable if "
            "both name forms are confirmed as names Plaintiff uses. "
            "Accurate asked for that confirmation and for a government ID. "
            "The names are being confirmed. A government ID is not being circulated. "
            "A Civil L.R. 7-12 stipulation has not been executed. The "
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
        footer="ADMIN. MOTION TO CONFORM PLAINTIFF'S NAME -- NGWA NFORBI v. MEZA-GONZALEZ",
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
            "(Dkt. 13). On September 10, 2026 he wrote that he does not "
            "represent Officer Melano or Officer Meza-Gonzalez in this "
            "action, that neither has been properly served as he sees it, "
            "that he does not believe a stipulation is required, and that "
            "he will not oppose a motion so long as the paper makes clear "
            'that "Nforbi" and "Newanforbi" are the same person. This '
            "motion and this declaration do that. He has not filed a "
            "notice of appearance in this action. His statement is "
            "non-opposition to this caption request. It is not a notice of "
            "appearance and not acceptance of service. A Civil L.R. 7-12 "
            "stipulation could not be obtained because he is not counsel of "
            "record here and did not agree to stipulate. Officer Melano has "
            "been served."
        ),
        motion_conferral=(
            "Plaintiff conferred with Deputy Attorney General Haiyang A. Li. "
            "He stated he will not oppose this request so long as the paper "
            'makes clear that "Nforbi" and "Newanforbi" are the same person. '
            "He has not appeared in this action and states he does not "
            "represent either officer here. His statement is non-opposition "
            "to this caption request — not an appearance and not acceptance "
            "of service. Dkt. 13 remains pending. A Civil L.R. 7-12 "
            "stipulation could not be obtained. The accompanying declaration "
            "satisfies Civil L.R. 7-11(a)."
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
        caption_short="NGWA NFORBI v. MEZA-GONZALEZ",
        last_name_on_docket="Nforbi",
    ),
    NameCase(
        matter=33,
        slug="candelaria",
        out_dir=DOCS / "matter-33/ndcal",
        case_no="3:26-cv-08272-LJC",
        judge="Hon. Lisa J. Cisneros",
        footer="ADMIN. MOTION TO CONFORM PLAINTIFF'S NAME -- NGWA NFORBI v. CANDELARIA",
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
            "Answer, and identified Fiel Dizon Tigno as PACER lead. On "
            "September 10, 2026 Mr. McMahon returned a revised stipulation. "
            "I accepted that named file the same afternoon and authorized "
            "counsel to file it. As of the date of this declaration that "
            "paper has not appeared on the docket. This motion is the "
            "fallback. It does not withdraw the September 10 authorization "
            "to file that named revised file. Civil L.R. 7-11(b) gives "
            "counsel four days after filing to oppose or support."
        ),
        motion_conferral=(
            "Plaintiff conferred with counsel for Defendants. Counsel sent "
            "a revised stipulation on September 10, 2026. Plaintiff "
            "accepted that named file. It has not yet appeared on the "
            "docket. This motion is the fallback if that paper is not "
            "filed. The accompanying declaration satisfies Civil L.R. "
            "7-11(a). Counsel may file a Civil L.R. 7-11(b) response "
            "within four days."
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
            "The September 10 authorization to file your revised "
            "stipulation remains. This motion is only the fallback if that "
            "paper does not go on file. Civil L.R. 7-11(b) gives you four "
            "days after filing to oppose or support.\n"
        ),
        caption_short="NGWA NFORBI v. CANDELARIA",
        last_name_on_docket="Nforbi",
    ),
]


def _header(d: PleadingPaper, case: NameCase | None = None) -> None:
    atty_y = d._line_y(0)
    for i, (txt, fn, sz) in enumerate(ATTY):
        d.c.setFont(fn, sz)
        d.c.drawString(CONTENT_LEFT, atty_y - i * 14, txt)
    d.current_line = 4
    d.blank_line()
    d.write_line("UNITED STATES DISTRICT COURT", bold=True, center=True)
    d.write_line("NORTHERN DISTRICT OF CALIFORNIA", bold=True, center=True)
    if case and case.division:
        d.write_line(case.division, bold=True, center=True)
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
    d.ensure_space(10)
    if declaration:
        if case.federal_jurat:
            _body(
                d,
                "I declare under penalty of perjury under the laws of the "
                "United States of America that the foregoing is true and "
                f"correct. Executed on {case.dated}, at {case.place}.",
                first_indent=0,
            )
        else:
            d.write_line("I declare under penalty of perjury that the foregoing")
            d.write_line(f"is true and correct. Signed on {case.dated},")
            d.write_line(f"at {case.place}.")
    else:
        d.write_line(f"Dated: {case.dated}")
        d.blank_line()
        d.write_line("Respectfully submitted,", right=True, right_margin_offset=20)
    d.blank_line()
    d.blank_line()
    d.draw_signature_image(
        SIGNATURE_PATH,
        SIGNATURE_NATIVE_PX[0],
        SIGNATURE_NATIVE_PX[1],
        SIG_LINE,
        width=215,
        x_offset=15,
        height_scale=1.2,
    )
    d.write_line(SIG_LINE, right=True, right_margin_offset=20)
    d.write_line(NEW_NAME_CAPS, bold=True, right=True, right_margin_offset=20)
    role = (
        "Declarant / Plaintiff in Propria Persona"
        if declaration and case.user_draft
        else "Plaintiff, In Propria Persona"
    )
    d.write_line(role, right=True, right_margin_offset=20)
    _write_right_markup(
        d,
        f"(presently on this docket as {case.current_docket_name})",
        size=10,
        right_margin_offset=20,
    )


def _write_right_markup(
    d: PleadingPaper,
    text: str,
    *,
    size: int = 10,
    right_margin_offset: int = 20,
) -> None:
    """Right-align a line that may contain <<b:…>> markers."""
    segs = d._parse_segments(_mark_name_tokens(text))

    def font_for(style: str) -> str:
        return "Times-Bold" if style == "b" else "Times-Roman"

    total = sum(d.c.stringWidth(part, font_for(style), size) for part, style in segs)
    d._ensure_line()
    y = d._line_y(d.current_line)
    x = CONTENT_RIGHT - right_margin_offset - total
    for part, style in segs:
        font = font_for(style)
        d.c.setFont(font, size)
        d.c.drawString(x, y, part)
        x += d.c.stringWidth(part, font, size)
    d.current_line += 1


def _mark_name_tokens(text: str) -> str:
    """Bold Ngwa Nforbi, Nforbi, and Ngehsi Newanforbi throughout.

    Those words stay roman only inside the full requested name
    Brendan Ngwa Nforbi / BRENDAN NGWA NFORBI. The letters inside
    Newanforbi are not a match for Nforbi.
    """
    held: list[str] = []

    def stash(value: str) -> str:
        held.append(value)
        return f"\x00{len(held) - 1}\x00"

    text = re.sub(r"<<[a-z]+:[^>]*>>", lambda m: stash(m.group(0)), text)
    for literal in ("Brendan Ngwa Nforbi", "BRENDAN NGWA NFORBI"):
        text = text.replace(literal, stash(literal))
    for old, marked in (
        ("Ngehsi Newanforbi", "<<b:Ngehsi Newanforbi>>"),
        ("NGEHSI NEWANFORBI", "<<b:NGEHSI NEWANFORBI>>"),
        ("Ngwa Nforbi", "<<b:Ngwa Nforbi>>"),
        ("NGWA NFORBI", "<<b:NGWA NFORBI>>"),
    ):
        text = text.replace(old, stash(marked))
    text = re.sub(r"\bNforbi\b", "<<b:Nforbi>>", text)
    text = re.sub(r"\bNFORBI\b", "<<b:NFORBI>>", text)
    return re.sub(r"\x00(\d+)\x00", lambda m: held[int(m.group(1))], text)


def _body(d: PleadingPaper, text: str, **kwargs) -> None:
    kwargs.setdefault("first_indent", 0)
    PleadingPaper.write_wrapped(d, _mark_name_tokens(text), **kwargs)


def _aka_clause() -> str:
    """The other docket forms; no leading Brendan on Newanforbi."""
    return "Ngwa Nforbi and as Nforbi and as Ngehsi Newanforbi"


def _same_person_line() -> str:
    """Requested name plus every other docket form."""
    return f"{BOLD_NAME} is the same natural person as {_aka_clause()}."


def _pacer_name_ask(case: NameCase) -> str:
    """Case-specific PACER-match ask. Amazon stays on the generic paragraph."""
    if case.last_name_on_docket:
        return (
            f" This docket currently records last name as the single word "
            f"{case.last_name_on_docket}. The ask is that the Clerk change "
            f"that last-name field from {case.last_name_on_docket} to "
            f"{LAST_NAME} so it matches Plaintiff's PACER account (login "
            f"bngwanforbi). First name is {FIRST_NAME}."
        )
    if case.from_name_token:
        return (
            f" This docket currently records the name as "
            f"{case.current_docket_name}. The ask is that the Clerk change "
            f"{case.from_name_token} to {LAST_NAME} so it matches "
            f"Plaintiff's PACER account (login bngwanforbi). First name "
            f"remains {FIRST_NAME}."
        )
    return ""


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
        f"{case.file_tag} ({case.dated}).pdf"
    )


def _decl_path(case: NameCase) -> Path:
    return case.out_dir / (
        f"Declaration ISO Administrative Motion - Conform Plaintiff's Name - "
        f"{case.file_tag} ({case.dated}).pdf"
    )


def _order_path(case: NameCase) -> Path:
    return case.out_dir / (
        f"Proposed Order - Conform Plaintiff's Name - "
        f"{case.file_tag} ({case.dated}).pdf"
    )


def _pos_path(case: NameCase) -> Path:
    return case.out_dir / (
        f"Proof of Service - Name Conform Administrative Motion - "
        f"{case.file_tag} ({case.dated}).pdf"
    )


def _packet_path(case: NameCase) -> Path:
    return case.out_dir / (
        f"Name Conform Administrative Motion Packet - "
        f"{case.file_tag} ({case.dated}).pdf"
    )


def _cover_path(case: NameCase) -> Path:
    return case.out_dir / (
        f"Exhibit A Cover - ECF Help Desk - {case.file_tag} ({case.dated}).pdf"
    )


def _email_path(case: NameCase) -> Path:
    return case.out_dir / f"EMAIL_DRAFT_Name_Conform_Admin_Motion_{case.slug}.txt"


def build_motion(case: NameCase) -> Path:
    if case.user_draft:
        return _build_motion_user(case)
    path = _motion_path(case)
    path.parent.mkdir(parents=True, exist_ok=True)
    d = PleadingPaper(str(path), doc_title_footer=case.footer)
    _header(d, case)
    _caption(d, case, _caption_title())
    d.write_line(_motion_title(), bold=True, center=True)
    d.write_line("PLAINTIFF'S NAME ON THE DOCKET", bold=True, center=True)
    d.blank_line()
    _body(d,
        f"TO THE COURT AND TO {case.defendants_short.upper()}, THROUGH COUNSEL:",
        first_indent=0,
    )
    d.blank_line()
    _body(d,
        f"Plaintiff {BOLD_NAME}, appearing in propria persona and presently "
        f"identified on this docket as {case.current_docket_name}, moves under "
        "Civil Local Rule 7-11 for an order conforming the docket name. This "
        "is Plaintiff's request. It is not a Civil L.R. 7-12 stipulation.",
        first_indent=0,
    )
    d.blank_line()
    d.ensure_space(10)
    d.write_line("I.", bold=True, center=True)
    d.write_line("THE ECF HELP DESK CANNOT LINK THE ACCOUNT", bold=True, center=True)
    d.write_line("UNTIL THE DOCKET MATCHES", bold=True, center=True)
    d.blank_line()
    _body(d,
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
    _body(d,
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
    d.write_line("II.", bold=True, center=True)
    d.write_line("RELIEF REQUESTED", bold=True, center=True)
    d.blank_line()
    _body(d,
        f"The Clerk shall amend the docket, the short title, the CM/ECF "
        f"party record, and the caption of this action so that Plaintiff is "
        f"identified as {BOLD_NAME} — {FIRST_LAST_GLOSS} — matching "
        f"Plaintiff's existing PACER account (login "
        f"bngwanforbi). This is a clean swap of the party name."
        f"{_pacer_name_ask(case)} Subsequent "
        f"papers shall use that caption.",
        first_indent=0,
    )
    d.blank_line()
    d.ensure_space(3)
    d.write_line("III.", bold=True, center=True)
    d.write_line("THE TWO NAMES ARE ONE PERSON", bold=True, center=True)
    d.blank_line()
    _body(d,
        f"{_same_person_line()} The names are one person. This motion does not "
        "add, drop, or substitute any party. It is not an amendment of any "
        "claim, defense, or operative pleading. It is not a Fed. R. Civ. P. "
        "25 substitution.",
        first_indent=0,
    )
    d.blank_line()
    d.ensure_space(3)
    d.write_line("IV.", bold=True, center=True)
    d.write_line("CIVIL L.R. 7-11", bold=True, center=True)
    d.blank_line()
    _body(d,
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
    _body(d,
        "All prior filings, proofs of service, acceptances of service, "
        "orders, and related-case determinations remain effective as to the "
        "same person. No party need be re-served. <<b:No other date or "
        "deadline in this action is modified.>> This motion is not a stay "
        "of discovery. Expressly unchanged, without limitation: "
        f"{'; '.join(case.preserve)}.",
        first_indent=0,
    )
    d.blank_line()
    _body(d,
        "Nothing in this motion is a waiver of any claim, defense, "
        "objection, or right except the identity of Plaintiff as the same "
        "natural person and the docket name requested in Section II.",
        first_indent=0,
    )
    d.blank_line()
    _body(d,
        "A declaration, Exhibit A, and a proposed order accompany this motion.",
        first_indent=0,
    )
    d.blank_line()
    _sign_for(d, case)
    d.save()
    return path


def build_declaration(case: NameCase) -> Path:
    if case.user_draft:
        return _build_declaration_user(case)
    path = _decl_path(case)
    d = PleadingPaper(
        str(path),
        doc_title_footer=f"DECLARATION ISO ADMIN. MOTION -- {case.case_no}",
    )
    _header(d, case)
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
    _body(d,
        f"I, {BOLD_NAME_CAPS}, declare as follows:",
        first_indent=0,
    )
    d.blank_line()
    _body(d,
        "1.  I am the Plaintiff in this action. I am over eighteen. I make "
        "this declaration from personal knowledge in support of Plaintiff's "
        "Civil L.R. 7-11 administrative motion to conform the Plaintiff "
        "name on this docket. If called, I could and would testify "
        "competently to these facts.",
        first_indent=0,
    )
    d.blank_line()
    _body(d,
        "2.  My PACER login is bngwanforbi. On September 1, 2026 I asked "
        "the CAND ECF Help Desk to link that account to this action and to "
        "my other N.D. Cal. actions. The Help Desk replied the same day "
        "that it cannot link an action to that account until the docket "
        "reflects the name on the account, and that a name change requires "
        "a request to the Court. A true copy of that reply is Exhibit A.",
        first_indent=0,
    )
    d.blank_line()
    _body(d,
        "3.  I recently learned that this District permits pro se "
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
    _body(d,
        f"4.  I, {BOLD_NAME}, am the same natural person as "
        f"{_aka_clause()}."
        f"{_pacer_name_ask(case)} I am not asking the "
        "Court to add, drop, or substitute any party.",
        first_indent=0,
    )
    d.blank_line()
    _body(d,
        f"5.  {case.conferral_decl}",
        first_indent=0,
    )
    d.blank_line()
    _body(d,
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
    if case.user_draft:
        return _build_order_user(case)
    path = _order_path(case)
    d = PleadingPaper(
        str(path),
        doc_title_footer=f"[PROPOSED] ORDER CONFORMING PLAINTIFF'S NAME -- {case.case_no}",
    )
    _header(d, case)
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
    _body(d,
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
    _body(d,
        f"1.  The Clerk shall amend the docket, the short title, the "
        f"CM/ECF party record, and the caption of this action so that "
        f"Plaintiff is identified as {BOLD_NAME} ({FIRST_LAST_GLOSS}), "
        f"matching PACER login bngwanforbi."
        f"{_pacer_name_ask(case)} "
        f"Subsequent papers shall use that caption.",
        first_indent=0,
    )
    d.blank_line()
    _body(d,
        f"2.  {_same_person_line()} "
        f"{BOLD_NAME} is the same natural person previously identified "
        f"on this docket as {case.current_docket_name}. "
        "This Order does not add, drop, or substitute any party and does "
        "not amend any claim or defense.",
        first_indent=0,
    )
    d.blank_line()
    _body(d,
        "3.  All prior filings, service, acceptances of service, and orders "
        "remain effective. No party need be re-served by reason of this Order.",
        first_indent=0,
    )
    d.blank_line()
    _body(d,
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
    d.write_line(case.judge_title)
    d.save()
    return path


FIRST_LAST_COLON = f"first name: {FIRST_NAME}; last name: {LAST_NAME}"


def _build_motion_user(case: NameCase) -> Path:
    path = _motion_path(case)
    path.parent.mkdir(parents=True, exist_ok=True)
    d = PleadingPaper(str(path), doc_title_footer=case.footer)
    _header(d, case)
    _caption(d, case, _caption_title())
    d.write_line(_motion_title(), bold=True, center=True)
    d.write_line("PLAINTIFF'S NAME ON THE DOCKET", bold=True, center=True)
    d.blank_line()
    _body(
        d,
        f"TO THE COURT AND TO {case.defendants_short.upper()}, THROUGH COUNSEL:",
        first_indent=0,
    )
    d.blank_line()
    _body(
        d,
        f"Plaintiff {BOLD_NAME}, appearing in propria persona and presently "
        f"identified on this docket as {case.current_docket_name}, moves under "
        "Civil Local Rule 7-11 for an administrative order conforming his name "
        "on the docket, the short title, and the CM/ECF party record. This is "
        "Plaintiff's request; it is not a Civil L.R. 7-12 stipulation.",
        first_indent=0,
    )
    d.blank_line()
    d.ensure_space(10)
    d.write_line("I.", bold=True, center=True)
    d.write_line("THE ECF HELP DESK CANNOT LINK THE PACER ACCOUNT", bold=True, center=True)
    d.write_line("UNTIL THE DOCKET MATCHES", bold=True, center=True)
    d.blank_line()
    _body(
        d,
        "On September 1, 2026, the Northern District of California ECF Help "
        "Desk advised Plaintiff that it cannot link this action to PACER login "
        "bngwanforbi until the docket reflects the name on the account, and "
        "that conforming a name on the docket requires a request to the Court. "
        "A true and correct copy of that written guidance is attached as "
        "Exhibit A. Upon the Clerk updating the party name on the docket, "
        "Plaintiff will request that the Help Desk link that login for pro se "
        "e-filing. This motion does not itself activate e-filing.",
        first_indent=0,
    )
    d.blank_line()
    _body(
        d,
        "Good cause exists to conform the docket name so the login can be "
        "linked. E-filing will eliminate the delay inherent in mailing papers "
        "to the Clerk and to counsel; will ensure that filings appear on the "
        "docket on the day they are filed rather than days later; will allow "
        "defense counsel of record to receive immediate electronic service via "
        "NEF; and will avoid the transit, weekend, and holiday lag associated "
        "with paper mail.",
        first_indent=0,
    )
    d.blank_line()
    d.ensure_space(3)
    d.write_line("II.", bold=True, center=True)
    d.write_line("RELIEF REQUESTED", bold=True, center=True)
    d.blank_line()
    _body(
        d,
        f"Plaintiff requests that the Clerk be directed to amend the docket, "
        f"the short title, the CM/ECF party record, and the caption of this "
        f"action so that Plaintiff is identified as {BOLD_NAME} "
        f"({FIRST_LAST_COLON}), matching Plaintiff's existing PACER account "
        f"(login: bngwanforbi).",
        first_indent=0,
    )
    d.blank_line()
    _body(
        d,
        f"This docket currently records Plaintiff's name as "
        f"{case.current_docket_name}. The request is that the Clerk conform "
        f"the middle and last name token from {case.from_name_token} to "
        f"{LAST_NAME} to match PACER login bngwanforbi, while the first name "
        f"remains {FIRST_NAME}. Subsequent papers shall bear that conformed "
        f"caption.",
        first_indent=0,
    )
    d.blank_line()
    d.ensure_space(3)
    d.write_line("III.", bold=True, center=True)
    d.write_line("THE TWO NAMES ARE ONE PERSON", bold=True, center=True)
    d.blank_line()
    _body(
        d,
        f"{BOLD_NAME} is the same natural person previously and alternatively "
        f"identified on this docket and related records as "
        f"{case.current_docket_name}, {case.from_name_token}, and {LAST_NAME}.",
        first_indent=0,
    )
    d.blank_line()
    _body(
        d,
        "The two name forms belong to one and the same person. This motion "
        "does not add, drop, or substitute any party. It is not a substitution "
        "of parties under Federal Rule of Civil Procedure 25. It does not "
        "alter, amend, or modify any claim, cause of action, theory of "
        "liability, prayer for relief, or defense.",
        first_indent=0,
    )
    d.blank_line()
    d.ensure_space(3)
    d.write_line("IV.", bold=True, center=True)
    d.write_line("CIVIL L.R. 7-11", bold=True, center=True)
    d.blank_line()
    _body(
        d,
        "Conforming a pro se party's docket name to allow an official PACER "
        "e-filing account to be linked is a miscellaneous administrative "
        "matter appropriate for resolution under Civil Local Rule 7-11. A "
        "35-day noticed motion under Civil L.R. 7-2 is unnecessary.",
        first_indent=0,
    )
    d.blank_line()
    _body(d, case.motion_conferral, first_indent=0)
    d.blank_line()
    d.ensure_space(3)
    d.write_line("V.", bold=True, center=True)
    d.write_line("NOTHING ELSE MOVES", bold=True, center=True)
    d.blank_line()
    _body(
        d,
        "All prior filings, summonses, proofs of service, appearances, "
        "orders, and related-case determinations remain fully effective as to "
        "the same person. No party need be re-served by reason of this "
        "administrative change.",
        first_indent=0,
    )
    d.blank_line()
    _body(
        d,
        "<<b:No other date, hearing, or deadline in this action is modified.>> "
        "Expressly unchanged, without limitation:",
        first_indent=0,
    )
    d.blank_line()
    for i, item in enumerate(case.preserve, 1):
        _body(d, f"{i}.  {item}", first_indent=0, indent=12)
        d.blank_line()
    _body(
        d,
        "A declaration in support, Exhibit A, and a proposed order accompany "
        "this motion.",
        first_indent=0,
    )
    d.blank_line()
    _sign_for(d, case)
    d.save()
    return path


def _build_declaration_user(case: NameCase) -> Path:
    path = _decl_path(case)
    d = PleadingPaper(
        str(path),
        doc_title_footer=f"DECLARATION ISO ADMIN. MOTION -- {case.case_no}",
    )
    _header(d, case)
    _caption(
        d,
        case,
        [
            "DECLARATION OF BRENDAN",
            "NGWA NFORBI ISO",
            "ADMINISTRATIVE MOTION",
            "TO CONFORM PLAINTIFF'S NAME",
        ],
    )
    d.write_line("DECLARATION OF BRENDAN NGWA NFORBI", bold=True, center=True)
    d.write_line("IN SUPPORT OF ADMINISTRATIVE MOTION", bold=True, center=True)
    d.write_line("TO CONFORM PLAINTIFF'S NAME", bold=True, center=True)
    d.blank_line()
    _body(d, f"I, {BOLD_NAME_CAPS}, declare as follows:", first_indent=0)
    d.blank_line()
    _body(
        d,
        "1.  I am the Plaintiff in this action. I am over the age of eighteen "
        "and competent to make this declaration. I have personal knowledge of "
        "the facts set forth herein, and if called as a witness, I could and "
        "would testify competently thereto. I make this declaration in support "
        "of Plaintiff's Civil L.R. 7-11 Administrative Motion to Conform "
        "Plaintiff's Name on the Docket.",
        first_indent=0,
    )
    d.blank_line()
    _body(
        d,
        "2.  My PACER login is bngwanforbi. On September 1, 2026, I contacted "
        "the Northern District of California ECF Help Desk to request that my "
        "PACER login be linked to this action and my other pending actions in "
        "this District. The ECF Help Desk replied the same day, informing me "
        "that the Clerk's Office cannot link an action to that PACER account "
        "until the docket reflects the name on the account, and that updating "
        "or conforming a docket name requires a request to the Court. A true "
        "and correct copy of that September 1, 2026 email communication from "
        "the ECF Help Desk is attached hereto as Exhibit A.",
        first_indent=0,
    )
    d.blank_line()
    _body(
        d,
        "3.  Until the docket name is conformed to match my PACER account, I "
        "am required to serve and file all papers via paper mail. Postal "
        "service introduces substantial delay, including mailing transit times, "
        "holiday and weekend transit lag, and the risk of late delivery. "
        "Conforming the docket name will enable the ECF Help Desk to link "
        "PACER login bngwanforbi, permitting immediate electronic filing and "
        "electronic service on counsel of record via the Court's CM/ECF "
        "system.",
        first_indent=0,
    )
    d.blank_line()
    _body(
        d,
        f"4.  I, {BOLD_NAME}, am the exact same natural person as "
        f"{case.current_docket_name}, {case.from_name_token}, and {LAST_NAME}. "
        f"This docket currently records my name as {case.current_docket_name}. "
        f"I request that the Clerk conform the middle and last name tokens to "
        f"{LAST_NAME} so that the party name reads {BOLD_NAME} "
        f"({FIRST_LAST_COLON}), exactly matching PACER login bngwanforbi. I "
        f"am not asking to add, drop, or substitute any party, nor to alter "
        f"any claim or defense.",
        first_indent=0,
    )
    d.blank_line()
    _body(d, f"5.  {case.conferral_decl}", first_indent=0)
    d.blank_line()
    _body(
        d,
        "6.  I am not asking the Court to modify, continue, or vacate any "
        "scheduled hearing, conference, briefing schedule, pending motion, or "
        "discovery deadline. Following the Clerk's entry conforming the party "
        "name, I will request that the ECF Help Desk link PACER account "
        "bngwanforbi for pro se e-filing.",
        first_indent=0,
    )
    d.blank_line()
    _sign_for(d, case, declaration=True)
    d.save()
    return path


def _build_order_user(case: NameCase) -> Path:
    path = _order_path(case)
    d = PleadingPaper(
        str(path),
        doc_title_footer=f"[PROPOSED] ORDER CONFORMING PLAINTIFF'S NAME -- {case.case_no}",
    )
    _header(d, case)
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
    _body(
        d,
        "The Court has considered Plaintiff's Civil Local Rule 7-11 "
        "Administrative Motion to Conform Plaintiff's Name on the Docket, the "
        f"supporting Declaration of {BOLD_NAME}, and Exhibit A attached "
        "thereto. Good cause appearing—including ensuring that the docket name "
        "matches Plaintiff's existing PACER account (login bngwanforbi) so "
        "that the ECF Help Desk may link the account for pro se electronic "
        "filing, thereby eliminating transit delay and facilitating prompt "
        "service—",
        first_indent=0,
    )
    d.blank_line()
    d.write_line("IT IS HEREBY ORDERED THAT:", bold=True)
    d.blank_line()
    _body(
        d,
        f"1.  The Clerk shall amend the docket, the short title, the CM/ECF "
        f"party record, and the caption of this action so that Plaintiff is "
        f"identified as {BOLD_NAME_CAPS} ({FIRST_LAST_COLON}), matching PACER "
        f"login bngwanforbi. All subsequent filings in this action shall bear "
        f"that conformed caption.",
        first_indent=0,
    )
    d.blank_line()
    _body(
        d,
        f"2.  {BOLD_NAME} is the same natural person previously identified on "
        f"this docket as {case.current_docket_name}. This Order does not add, "
        f"drop, or substitute any party, does not constitute a substitution "
        f"under Federal Rule of Civil Procedure 25, and does not amend or "
        f"alter any claim or defense.",
        first_indent=0,
    )
    d.blank_line()
    _body(
        d,
        "3.  All prior filings, summonses, proofs of service, appearances, "
        "orders, and related-case determinations remain in full force and "
        "effect. No party need be re-served by reason of this Order.",
        first_indent=0,
    )
    d.blank_line()
    _body(
        d,
        "4.  No hearing date, conference, briefing schedule, pending motion, "
        "or discovery deadline is modified by this Order.",
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
    d.write_line(case.judge.upper())
    d.write_line(case.judge_title)
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
        "Name; Declaration; Exhibit A; [Proposed] Order"
    )
    build_proof_of_service(
        path,
        ProofOfServiceFields(
            plaintiff_line=case.current_docket_name.upper(),
            plaintiff_role="Plaintiff",
            defendant_lines=case.defendant_pos_lines,
            defendant_role="Defendant",
            case_number=case.case_no,
            service_date=case.dated,
            document_title=title,
            mailing_location=case.pos_place,
            recipients=case.pos_recipients,
            server_name=NEW_NAME,
            stamp_signature=True,
            district_line=DISTRICT_NDCAL,
            by_email=True,
            signature_on_second_page=False,
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
    if case.last_name_on_docket:
        docket_ask = (
            "This docket lists last name as " + case.last_name_on_docket
            + ". The ask is to change that last name to " + LAST_NAME
            + " to match PACER login bngwanforbi.\n"
        )
    elif case.from_name_token:
        docket_ask = (
            "This docket lists the name as " + case.current_docket_name
            + ". The ask is to change " + case.from_name_token
            + " to " + LAST_NAME + " to match PACER login bngwanforbi.\n"
        )
    else:
        docket_ask = ""
    body = f"""To: {to}
Subject: {subject}

Counsel:

I am filing a Civil L.R. 7-11 administrative motion asking the Court
to conform the Plaintiff name on this docket to {NEW_NAME}
(first name Brendan; last name Ngwa Nforbi).
{docket_ask}
This is a request to the Court. It is not a stipulation.

{posture}
{("" if not case.email_extra else chr(10) + case.email_extra)}
The two name forms are one person. No deadline, hearing, or pending
motion moves. Conforming the name lets the Help Desk link the account
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
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--matter",
        type=int,
        action="append",
        dest="matters",
        help="Generate only these matter numbers (repeatable).",
    )
    args = parser.parse_args()
    selected = [c for c in CASES if not args.matters or c.matter in args.matters]
    if not selected:
        raise SystemExit(f"No matching matters for {args.matters}")
    if not Path(SIGNATURE_PATH).is_file():
        raise SystemExit(f"Missing signature image: {SIGNATURE_PATH}")
    if not HELP_DESK.is_file():
        raise SystemExit(f"Missing Help Desk exhibit: {HELP_DESK}")
    for case in selected:
        motion = build_motion(case)
        decl = build_declaration(case)
        cover = build_exhibit_cover(case)
        order = build_order(case)
        pos = build_pos(case)
        packet = _packet_path(case)
        assemble([motion, decl, cover, HELP_DESK, order, pos], packet)
        email = build_email(case)
        short = publish_short_link(packet, case.short_slug)
        extras = []
        for kind, slug in case.extra_short_slugs.items():
            src = {"motion": motion, "decl": decl, "order": order}[kind]
            extras.append(publish_short_link(src, slug))
        print(f"M{case.matter} {case.slug} unopposed={case.unopposed}:")
        print(f"  {motion}")
        print(f"  {decl}")
        print(f"  {order}")
        print(f"  {pos}")
        print(f"  {packet}")
        print(f"  {email}")
        print(f"  {short}")
        for extra in extras:
            print(f"  {extra}")


if __name__ == "__main__":
    main()
