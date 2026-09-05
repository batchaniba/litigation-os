#!/usr/bin/env python3
"""Plaintiff Civil L.R. 3-15 certifications for the five live N.D. Cal. cases.

Uses the May 1, 2026 Civil L.R. 3-15(c)(3) no-conflict / no-interest form.
None of these five actions is in federal court on 28 U.S.C. § 1332(a)
diversity, so (b)(3) / (c)(4)–(5) citizenship recitals are not required.
Plaintiff is a natural person; no parent, no litigation funder.

    python3 internal/scripts/ndcal-3-15-certifications.py \\
        [--date "September 4, 2026"] [--mailed-from "San Jose, California"]
"""

from __future__ import annotations

import argparse
import sys
from dataclasses import dataclass
from pathlib import Path

SCRIPT_DIR = Path(__file__).resolve().parent
sys.path.insert(0, str(SCRIPT_DIR / "lib"))
sys.path.insert(0, str(SCRIPT_DIR))
from pdf_packet import assemble  # noqa: E402
from pleading_paper import CONTENT_LEFT, PleadingPaper  # noqa: E402
from proof_of_service import (  # noqa: E402
    DISTRICT_NDCAL,
    ProofOfServiceFields,
    build_proof_of_service,
)
from signature_stamp import SIGNATURE_NATIVE_PX, SIGNATURE_PATH  # noqa: E402

ROOT = SCRIPT_DIR.parents[1]
DEFAULT_DATE = "September 4, 2026"
DEFAULT_MAILED_FROM = "San Jose, California"

COURT_LINE1 = "UNITED STATES DISTRICT COURT"
COURT_LINE2 = "NORTHERN DISTRICT OF CALIFORNIA"

FORM_CERT = (
    "Pursuant to Civil L.R. 3-15, the undersigned certifies that as of this "
    "date, there is no conflict or interest (other than the named parties) "
    "to report."
)

SIG_LINE = "___________________________________"


@dataclass(frozen=True)
class CertCase:
    matter: int
    slug: str
    out_rel: str
    pos_rel: str
    footer: str
    plaintiff_block_name: str
    plaintiff_caption: str
    plaintiff_pos: str
    server_name: str
    case_no: str
    judge: str
    caption_left: list[tuple[str, bool, bool]]
    defendant_pos_lines: list[str]
    recipients: list[str]
    pos_by_email: bool = False


CASES: list[CertCase] = [
    CertCase(
        matter=24,
        slug="serrato",
        out_rel=(
            "internal/public/documents/matter-24/"
            "Certification of Conflicts Interested Entities and Persons "
            "(Serrato) (Sep 4 2026).pdf"
        ),
        pos_rel=(
            "internal/public/documents/matter-24/"
            "Proof of Service - Certification of Conflicts (Serrato) "
            "(Sep 4 2026).pdf"
        ),
        footer="PLAINTIFF'S CIVIL L.R. 3-15 CERTIFICATION -- NEWANFORBI v. SERRATO",
        plaintiff_block_name="BRENDAN NGEHSI NEWANFORBI",
        plaintiff_caption="BRENDAN NGEHSI NEWANFORBI,",
        plaintiff_pos="BRENDAN NGEHSI NEWANFORBI",
        server_name="Brendan Ngehsi Newanforbi",
        case_no="4:26-cv-05953-ASK",
        judge="Hon. Ajay S. Krishnan",
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
        defendant_pos_lines=[
            "CAPTAIN G. SERRATO; and",
            "DOES 1-10, inclusive",
        ],
        recipients=[
            "Haiyang A. Li, Deputy Attorney General",
            "Office of the Attorney General",
            "300 South Spring Street, Suite 1702",
            "Los Angeles, CA 90013-1230",
            "Haiyang.Li@doj.ca.gov",
            "Attorney for Defendant Captain G. Serrato",
        ],
    ),
    CertCase(
        matter=28,
        slug="smith",
        out_rel=(
            "internal/public/documents/matter-28/"
            "Certification of Conflicts Interested Entities and Persons "
            "(Smith HOPE) (Sep 4 2026).pdf"
        ),
        pos_rel=(
            "internal/public/documents/matter-28/"
            "Proof of Service - Certification of Conflicts (Smith HOPE) "
            "(Sep 4 2026).pdf"
        ),
        footer=(
            "PLAINTIFF'S CIVIL L.R. 3-15 CERTIFICATION -- "
            "NEWANFORBI v. SMITH ET AL."
        ),
        plaintiff_block_name="BRENDAN NGEHSI NEWANFORBI",
        plaintiff_caption="BRENDAN NGEHSI NEWANFORBI,",
        plaintiff_pos="BRENDAN NGEHSI NEWANFORBI",
        server_name="Brendan Ngehsi Newanforbi",
        case_no="3:26-cv-07504-LJC",
        judge="Hon. Lisa J. Cisneros",
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
        recipients=[
            "Blaze Van Dine, Esq.",
            "SIMS, LAWRENCE & BROGHAMMER",
            "1478 Stone Point Drive, Suite 450",
            "Roseville, CA 95661",
            "blaze@sims-law.net",
            "slb-eservice@sims-law.net",
            "Counsel for Shannon Smith, LCSW, and HOPE Psychotherapy, Inc.",
        ],
        pos_by_email=True,
    ),
    CertCase(
        matter=29,
        slug="amazon",
        out_rel=(
            "internal/public/documents/matter-29/"
            "Certification of Conflicts Interested Entities and Persons "
            "(Amazon Accurate) (Sep 4 2026).pdf"
        ),
        pos_rel=(
            "internal/public/documents/matter-29/"
            "Proof of Service - Certification of Conflicts "
            "(Amazon Accurate) (Sep 4 2026).pdf"
        ),
        footer=(
            "PLAINTIFF'S CIVIL L.R. 3-15 CERTIFICATION -- "
            "NEWANFORBI v. AMAZON ET AL."
        ),
        plaintiff_block_name="BRENDAN NGEHSI NEWANFORBI",
        plaintiff_caption="BRENDAN NGEHSI NEWANFORBI,",
        plaintiff_pos="BRENDAN NGEHSI NEWANFORBI",
        server_name="Brendan Ngehsi Newanforbi",
        case_no="4:26-cv-09249-ASK",
        judge="Hon. Ajay S. Krishnan",
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
        recipients=[
            "Andrew P. Frederick, Esq.",
            "MORGAN, LEWIS & BOCKIUS LLP",
            "1400 Page Mill Road",
            "Palo Alto, CA 94304",
            "andrew.frederick@morganlewis.com",
            "Attorney for Amazon.com Services, LLC",
            "",
            "Jasmine J. Stanzick, Esq.",
            "SEYFARTH SHAW LLP",
            "2029 Century Park East, Suite 3500",
            "Los Angeles, CA 90067-3021",
            "jstanzick@seyfarth.com",
            "Attorney for Accurate Background, LLC",
        ],
    ),
    CertCase(
        matter=32,
        slug="meza",
        out_rel=(
            "internal/public/documents/matter-32/ndcal/"
            "Certification of Conflicts Interested Entities and Persons "
            "(Meza Melano) (Sep 4 2026).pdf"
        ),
        pos_rel=(
            "internal/public/documents/matter-32/ndcal/"
            "Proof of Service - Certification of Conflicts "
            "(Meza Melano) (Sep 4 2026).pdf"
        ),
        footer=(
            "PLAINTIFF'S CIVIL L.R. 3-15 CERTIFICATION -- "
            "NFORBI v. MEZA-GONZALEZ ET AL."
        ),
        plaintiff_block_name="BRENDAN NGWA NFORBI",
        plaintiff_caption="BRENDAN NGWA NFORBI,",
        plaintiff_pos="BRENDAN NGWA NFORBI",
        server_name="Brendan Ngwa Nforbi",
        case_no="4:26-cv-08271-ASK",
        judge="Hon. Ajay S. Krishnan",
        caption_left=[
            ("BRENDAN NGWA NFORBI,", True, False),
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
            "JOSE MELANO; and DOES 1-10",
        ],
        recipients=[
            "Jose Melano, CHP #023054",
            "California Highway Patrol, South Sacramento Area",
            "6 Massie Court",
            "Sacramento, CA 95823",
            "",
            "Santiago Meza-Gonzalez, CHP #023295",
            "California Highway Patrol, Modesto Area",
            "4030 Kiernan Avenue",
            "Modesto, CA 95356",
            "(Courtesy; Rule 4 as to Meza remains incomplete)",
            "",
            "Haiyang A. Li, Deputy Attorney General",
            "Office of the Attorney General",
            "300 South Spring Street, Suite 1702",
            "Los Angeles, CA 90013-1230",
            "Haiyang.Li@doj.ca.gov",
            "(Courtesy; counsel in the related Serrato action)",
        ],
    ),
    CertCase(
        matter=33,
        slug="candelaria",
        out_rel=(
            "internal/public/documents/matter-33/ndcal/"
            "Certification of Conflicts Interested Entities and Persons "
            "(Candelaria Gordon) (Sep 4 2026).pdf"
        ),
        pos_rel=(
            "internal/public/documents/matter-33/ndcal/"
            "Proof of Service - Certification of Conflicts "
            "(Candelaria Gordon) (Sep 4 2026).pdf"
        ),
        footer=(
            "PLAINTIFF'S CIVIL L.R. 3-15 CERTIFICATION -- "
            "NFORBI v. CANDELARIA ET AL."
        ),
        plaintiff_block_name="BRENDAN NGWA NFORBI",
        plaintiff_caption="BRENDAN NGWA NFORBI,",
        plaintiff_pos="BRENDAN NGWA NFORBI",
        server_name="Brendan Ngwa Nforbi",
        case_no="3:26-cv-08272-LJC",
        judge="Hon. Lisa J. Cisneros",
        caption_left=[
            ("BRENDAN NGWA NFORBI,", True, False),
            ("", False, False),
            ("                          Plaintiff,", False, False),
            ("", False, False),
            ("       v.", False, False),
            ("", False, False),
            ("DIANA CANDELARIA, individually;", True, False),
            ("STEVE GORDON, officially; and", True, False),
            ("DOES 1-10, inclusive,", True, False),
            ("", False, False),
            ("                          Defendants.", False, False),
        ],
        defendant_pos_lines=[
            "DIANA CANDELARIA, individually;",
            "STEVE GORDON, officially; and DOES 1-10",
        ],
        recipients=[
            "Diana Candelaria, Driver Safety Hearing Officer",
            "California Department of Motor Vehicles",
            "Legal Affairs Division, Mail Station C128",
            "2415 First Avenue",
            "Sacramento, CA 95818",
            "",
            "Steve Gordon, Director",
            "California Department of Motor Vehicles",
            "Legal Affairs Division, Mail Station C128",
            "2415 First Avenue",
            "Sacramento, CA 95818",
        ],
    ),
]


def _plaintiff_block(name: str) -> list[tuple[str, str, int]]:
    return [
        (name, "Times-Bold", 12),
        ("Plaintiff, In Propria Persona", "Times-Roman", 12),
        ("1455 Cat Tail Drive", "Times-Roman", 12),
        ("Stockton, CA 95204", "Times-Roman", 12),
        ("Telephone: (209) 801-4442", "Times-Roman", 12),
        ("E-mail: bnn.cdl@gmail.com", "Times-Roman", 12),
    ]


def _caption_right(case: CertCase) -> list[tuple[str, bool, bool]]:
    return [
        (f"Case No. {case.case_no}", False, False),
        ("", False, False),
        ("PLAINTIFF'S CERTIFICATION OF", True, False),
        ("CONFLICTS, INTERESTED", True, False),
        ("ENTITIES AND PERSONS, AND", True, False),
        ("CITIZENSHIP", True, False),
        ("", False, False),
        ("(Civil L.R. 3-15)", False, False),
        ("", False, False),
        (f"Judge: {case.judge}", False, False),
    ]


def _header(d: PleadingPaper, case: CertCase) -> None:
    c = d.c
    atty_y = d._line_y(0)
    for i, (txt, fn, sz) in enumerate(_plaintiff_block(case.plaintiff_block_name)):
        c.setFont(fn, sz)
        c.drawString(CONTENT_LEFT, atty_y - i * 15, txt)
    d.current_line = 4
    d.blank_line()
    d.write_line(COURT_LINE1, bold=True, center=True)
    d.write_line(COURT_LINE2, bold=True, center=True)
    d.blank_line()
    d.draw_caption_block(case.caption_left, _caption_right(case), caption_size=10,
                         tight_lh=13, boxed=True)
    d.blank_line()


def _body(d: PleadingPaper, case: CertCase, exec_date: str) -> None:
    d.write_wrapped(
        "TO THE COURT AND TO ALL PARTIES AND THEIR ATTORNEYS OF RECORD:",
        first_indent=36,
    )
    d.blank_line()
    d.write_wrapped(
        "Plaintiff, appearing in propria persona, submits this Certification as a "
        "separate document under Civil Local Rule 3-15(a). Plaintiff is a natural "
        "person with no parent corporation and no litigation funder. Plaintiff is not "
        "aware of any conflict, financial or otherwise, that the presiding Judge "
        f"({case.judge}) may have with the parties to this litigation.",
        first_indent=36,
    )
    d.blank_line()
    d.write_wrapped(FORM_CERT, first_indent=36)
    d.blank_line()
    d.write_wrapped(
        "This Court's jurisdiction is not based on 28 U.S.C. § 1332(a). Civil L.R. "
        "3-15(b)(3) therefore does not require a statement of attributed citizenship. "
        "Plaintiff will file a supplemental Certification if any required information "
        "changes.",
        first_indent=36,
    )
    d.blank_line()
    d.write_line(f"Dated: {exec_date}")
    d.blank_line()
    d.write_line("Respectfully submitted,", right=True, right_margin_offset=20)
    d.blank_line()
    d.blank_line()
    d.draw_signature_image(
        SIGNATURE_PATH,
        SIGNATURE_NATIVE_PX[0],
        SIGNATURE_NATIVE_PX[1],
        SIG_LINE,
        width=220,
        x_offset=15,
    )
    d.write_line(SIG_LINE, right=True, right_margin_offset=20)
    d.write_line(case.plaintiff_block_name, right=True, right_margin_offset=20)
    d.write_line("Plaintiff, In Propria Persona", right=True, right_margin_offset=20)


def build_cert(case: CertCase, out: Path, exec_date: str) -> Path:
    if not Path(SIGNATURE_PATH).is_file():
        raise SystemExit(f"Missing universal signature: {SIGNATURE_PATH}")
    out.parent.mkdir(parents=True, exist_ok=True)
    d = PleadingPaper(str(out), doc_title_footer=case.footer)
    _header(d, case)
    _body(d, case, exec_date)
    d.save()
    return out


def build_pos(case: CertCase, out: Path, exec_date: str, mailed_from: str) -> Path:
    fields = ProofOfServiceFields(
        plaintiff_line=case.plaintiff_pos,
        plaintiff_role="Plaintiff",
        defendant_lines=list(case.defendant_pos_lines),
        defendant_role="Defendants",
        case_number=case.case_no,
        district_line=DISTRICT_NDCAL,
        title="PROOF OF SERVICE",
        service_date=exec_date,
        document_title=(
            "Plaintiff's Certification of Conflicts, Interested Entities "
            "and Persons, and Citizenship (Civil L.R. 3-15)"
        ),
        mailing_location="" if case.pos_by_email else mailed_from,
        recipients=list(case.recipients),
        server_name=case.server_name,
        stamp_signature=True,
        by_email=case.pos_by_email,
        signature_on_second_page=len(case.recipients) > 12,
    )
    return build_proof_of_service(out, fields)


def main() -> None:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--date", default=DEFAULT_DATE)
    ap.add_argument("--mailed-from", default=DEFAULT_MAILED_FROM)
    ap.add_argument("--only", choices=[c.slug for c in CASES], action="append")
    args = ap.parse_args()
    chosen = [c for c in CASES if not args.only or c.slug in args.only]
    for case in chosen:
        out = ROOT / case.out_rel
        pos = ROOT / case.pos_rel
        build_cert(case, out, args.date)
        build_pos(case, pos, args.date, args.mailed_from)
        print(f"M{case.matter} {case.case_no}: {out}")


if __name__ == "__main__":
    main()
