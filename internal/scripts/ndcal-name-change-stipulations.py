#!/usr/bin/env python3
"""N.D. Cal. Civil L.R. 7-12 name-conform counterparts.

Live posture as of September 11, 2026 — do not lean on counsel:

- Matter 33 (McMahon): Plaintiff accepted their REVISED file at 1:29 p.m.
  on September 10. Do not send a new counterpart. Do not file a 7-11
  while that authorization is live. Wait for the conformed copy.
- Matter 24 (Li): will not stipulate; will not oppose a motion if
  "Nforbi" and "Newanforbi" are the same person. Take the non-opposition.
  File the 7-11. Do not ask him to sign.
- Matter 32 (Li): same, plus he does not appear and does not accept
  service. Do not put him on a signature block that looks like an
  appearance.
- Matter 29 Amazon (Frederick): agreeable if Plaintiff confirms both
  name forms are names he uses. Confirm that. Plaintiff drafts.
- Matter 29 Accurate (Drury / Stanzick): asked for the same confirmation
  and a government ID. Confirm the names. Do not send an ID.
- Matter 28 (Martinez): will review a quieter revision (background;
  drop the date laundry list). Use the quiet Matter 28 terms. Do not
  narrate "aliases" as a stipulated fact about the events of the suit.

Same-person clean swap. No deadline moves. No aka in the caption. The
body and proposed order recites that the two name forms are one person.

  python3 internal/scripts/ndcal-name-change-stipulations.py

Plaintiff-executed counterparts. Counsel signature lines are blank.
Do not file until the named counsel signs. Amazon / Accurate have not
agreed on the record — send the counterpart; do not represent their
consent. Do not authorize anyone to affix Plaintiff's /s/ except on
one named final file after Plaintiff reads it.
"""
from __future__ import annotations

import sys
from dataclasses import dataclass, field
from pathlib import Path

SCRIPT_DIR = Path(__file__).resolve().parent
sys.path.insert(0, str(SCRIPT_DIR))
sys.path.insert(0, str(SCRIPT_DIR / "lib"))

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
SIG_LINE = "___________________________________"

ATTY = [
    (NEW_NAME_CAPS, "Times-Bold", 12),
    ("Plaintiff, In Propria Persona", "Times-Roman", 12),
    ("1455 Cat Tail Drive", "Times-Roman", 12),
    ("Stockton, CA 95204", "Times-Roman", 12),
    ("Telephone: (209) 801-4442", "Times-Roman", 12),
    ("E-mail: bnn.cdl@gmail.com", "Times-Roman", 12),
]


@dataclass
class CounselSig:
    name: str
    firm_or_title: str
    for_party: str


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
    counsel_sigs: list[CounselSig]
    pos_recipients: list[str]
    pos_by_email: bool
    counsel_stated: str
    preserve: list[str]
    agreed_on_record: bool
    extra_right: list[tuple[str, bool, bool]] = field(default_factory=list)
    email_extra: str = ""
    short_slug: str = ""
    quiet: bool = False


CASES: list[NameCase] = [
    NameCase(
        matter=24,
        slug="serrato",
        out_dir=DOCS / "matter-24",
        case_no="4:26-cv-05953-ASK",
        judge="Hon. Ajay S. Krishnan",
        footer="STIPULATION TO CONFORM PLAINTIFF'S NAME -- NEWANFORBI v. SERRATO",
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
        counsel_sigs=[
            CounselSig(
                "HAIYANG A. LI",
                "Deputy Attorney General",
                "Attorney for Defendant Captain G. Serrato",
            ),
        ],
        pos_recipients=[
            "Haiyang A. Li, Deputy Attorney General",
            "Office of the Attorney General",
            "300 South Spring Street, Suite 1702",
            "Los Angeles, CA 90013-1230",
            "Haiyang.Li@doj.ca.gov",
            "Attorney for Defendant Captain G. Serrato",
        ],
        pos_by_email=True,
        counsel_stated=(
            "Deputy Attorney General Haiyang A. Li stated on September 10, "
            "2026 that he does not believe a stipulation is required and "
            "that Defendant will not oppose a motion so long as the paper "
            'makes clear that "Nforbi" and "Newanforbi" are the same '
            "person. This counterpart is not for his signature. The "
            "operative vehicle in this action is the Civil L.R. 7-11 "
            "motion."
        ),
        preserve=[
            "the continued initial case management conference (Dkt. 25)",
            "the September 30, 2026 hearing on Defendant's motion to dismiss "
            "(Dkt. 18 / Dkt. 21)",
            "Defendant's pending motion (Dkt. 18) and Plaintiff's opposition",
        ],
        agreed_on_record=False,
        short_slug="name-24",
    ),
    NameCase(
        matter=28,
        slug="smith",
        out_dir=DOCS / "matter-28",
        case_no="3:26-cv-07504-LJC",
        judge="Hon. Lisa J. Cisneros",
        footer="STIPULATION TO CONFORM PLAINTIFF'S NAME -- NEWANFORBI v. SMITH",
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
        counsel_sigs=[
            CounselSig(
                "BLAZE VAN DINE",
                "Sims, Lawrence & Broghammer",
                "Attorneys for Defendants Shannon Smith, LCSW, "
                "and HOPE Psychotherapy, Inc.",
            ),
            CounselSig(
                "ERIC MARTINEZ",
                "Sims, Lawrence & Broghammer",
                "Attorneys for Defendants Shannon Smith, LCSW, "
                "and HOPE Psychotherapy, Inc.",
            ),
        ],
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
        pos_by_email=True,
        counsel_stated=(
            "Eric T. Martinez wrote on September 11, 2026 that he does not "
            "intend to oppose a request that the Clerk identify Plaintiff "
            f"as {NEW_NAME}, and that he will review a revised stipulation "
            "that explains why the two name forms appear and why the "
            "correction is needed. Paragraph 1 does that. This paper does "
            "not recite a date-by-date calendar."
        ),
        preserve=[],
        agreed_on_record=False,
        email_extra=(
            "This is the quieter revision you asked for on September 11: "
            "short background on the two name forms and the PACER / Help "
            "Desk reason; no date-by-date list. The paper asks only that "
            "the Clerk identify me as Brendan Ngwa Nforbi. I am the same "
            "person as Brendan Ngehsi Newanforbi. If you want a change, "
            "send a redline.\n"
        ),
        short_slug="name-28",
        quiet=True,
    ),
    NameCase(
        matter=29,
        slug="amazon",
        out_dir=DOCS / "matter-29",
        case_no="4:26-cv-09249-ASK",
        judge="Hon. Ajay S. Krishnan",
        footer="STIPULATION TO CONFORM PLAINTIFF'S NAME -- NEWANFORBI v. AMAZON",
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
        counsel_sigs=[
            CounselSig(
                "ANDREW P. FREDERICK (SBN 284832)",
                "Morgan, Lewis & Bockius LLP",
                "Attorneys for Defendant Amazon.com Services, LLC",
            ),
            CounselSig(
                "JASMINE J. STANZICK (SBN 354704)",
                "Seyfarth Shaw LLP",
                "Attorneys for Defendant Accurate Background LLC",
            ),
        ],
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
        pos_by_email=True,
        counsel_stated=(
            "Andrew P. Frederick wrote on September 11, 2026 that Amazon "
            "is agreeable if Plaintiff confirms that both name forms are "
            "names he uses and goes by. John Drury wrote the same morning "
            "asking for that confirmation and for a government ID. This "
            "counterpart is sent for their signatures after that "
            "confirmation. It is not a stipulation until both signature "
            "blocks are signed. Plaintiff is not circulating a government "
            "ID with this paper."
        ),
        preserve=[
            "both Defendants' September 22, 2026 deadlines to answer or "
            "otherwise respond (Dkts. 6 and 7)",
            "both Defendants' September 22, 2026 magistrate-consent clocks "
            "(Dkts. 6 and 7)",
            "the December 1, 2026 initial case management conference",
        ],
        agreed_on_record=False,
        short_slug="name-29",
    ),
    NameCase(
        matter=32,
        slug="meza",
        out_dir=DOCS / "matter-32/ndcal",
        case_no="4:26-cv-08271-ASK",
        judge="Hon. Ajay S. Krishnan",
        footer="STIPULATION TO CONFORM PLAINTIFF'S NAME -- NFORBI v. MEZA-GONZALEZ",
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
        counsel_sigs=[
            CounselSig(
                "HAIYANG A. LI",
                "Deputy Attorney General",
                "Non-opposition; anticipated / related CHP counsel "
                "(Serrato 4:26-cv-05953-ASK)",
            ),
        ],
        pos_recipients=[
            "Haiyang A. Li, Deputy Attorney General",
            "Office of the Attorney General",
            "300 South Spring Street, Suite 1702",
            "Los Angeles, CA 90013-1230",
            "Haiyang.Li@doj.ca.gov",
            "Related Serrato counsel; Dkt. 13 accept-service motion pending",
        ],
        pos_by_email=True,
        counsel_stated=(
            "Deputy Attorney General Haiyang A. Li stated he will not oppose "
            "a clean name change identifying Plaintiff as "
            f"{NEW_NAME}. He is counsel of record for Captain Serrato in the "
            "related action and is the attorney named in Plaintiff's pending "
            "Civil L.R. 7-11 motion that he accept service for Officer "
            "Meza-Gonzalez (Dkt. 13). Officer Melano has been served. Li has "
            "not filed a notice of appearance in this action. His signature "
            "is non-opposition, not an appearance and not acceptance of "
            "service."
        ),
        preserve=[
            "Plaintiff's pending administrative motion that DAG Li accept "
            "service for Officer Meza-Gonzalez (Dkt. 13)",
            "any case-management date the Court sets after the August 24, "
            "2026 related-case reassignment",
            "Plaintiff's obligation to file the Rule 4(l) return for "
            "Officer Meza-Gonzalez",
        ],
        agreed_on_record=True,
        extra_right=[("Related: 4:26-cv-05953-ASK", False, False)],
        short_slug="name-32",
    ),
    NameCase(
        matter=33,
        slug="candelaria",
        out_dir=DOCS / "matter-33/ndcal",
        case_no="3:26-cv-08272-LJC",
        judge="Hon. Lisa J. Cisneros",
        footer="STIPULATION TO CONFORM PLAINTIFF'S NAME -- NFORBI v. CANDELARIA",
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
        counsel_sigs=[
            CounselSig(
                "FIEL DIZON TIGNO",
                "Supervising Deputy Attorney General",
                "Attorneys for Defendants Diana Candelaria and Steve Gordon",
            ),
            CounselSig(
                "WILLIAM J. McMAHON (SBN 178588)",
                "Deputy Attorney General",
                "Attorneys for Defendants Diana Candelaria and Steve Gordon",
            ),
        ],
        pos_recipients=[
            "Fiel Dizon Tigno, Supervising Deputy Attorney General",
            "William J. McMahon, Deputy Attorney General",
            "Office of the Attorney General, California Department of Justice",
            "1515 Clay Street, 20th Floor, P.O. Box 70550",
            "Oakland, CA 94612-0550",
            "fiel.tigno@doj.ca.gov",
            "Attorneys for Defendants Diana Candelaria and Steve Gordon",
        ],
        pos_by_email=True,
        counsel_stated=(
            "William J. McMahon returned a REVISED stipulation on "
            "September 10, 2026. Plaintiff accepted that named file at "
            "1:29 p.m. the same day and authorized counsel to file that "
            "file only. This generator is not a substitute for that "
            "accepted revision. Do not send this counterpart. Do not file "
            "a 7-11 while that authorization is live."
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
        agreed_on_record=True,
        email_extra=(
            "Your September 10 revision's deadline list is in this "
            "counterpart (September 22 magistrate consent; October 22 ADR / "
            "Rule 26(f); November 5 disclosures and JCMS; November 12 CMC; "
            "Dkt. 11). Fiel Dizon Tigno is on the signature block as PACER "
            "lead. The September 10 authorization to file the then-attached "
            "file does not extend to this file or to your markup. Please "
            "sign this counterpart, or send a redline. I will authorize one "
            "named final file in a separate writing after I read it.\n"
        ),
        short_slug="name-33",
    ),
]


def _header(d: PleadingPaper) -> None:
    c = d.c
    atty_y = d._line_y(0)
    for i, (txt, fn, sz) in enumerate(ATTY):
        c.setFont(fn, sz)
        c.drawString(CONTENT_LEFT, atty_y - i * 14, txt)
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
            ("[Civil L.R. 7-12]", False, False),
            ("", False, False),
            (f"Judge: {case.judge}", False, False),
            *case.extra_right,
        ]
    )
    d.draw_caption_block(case.caption_left, right, caption_size=10, tight_lh=13, boxed=True)
    d.blank_line()


def _stip_path(case: NameCase) -> Path:
    tag = "" if case.agreed_on_record else " (Plaintiff Counterpart — not yet agreed)"
    return case.out_dir / (
        f"Stipulation and Proposed Order - Conform Plaintiff's Name "
        f"to Brendan Ngwa Nforbi{tag} ({EXEC_DATE}).pdf"
    )


def _order_path(case: NameCase) -> Path:
    return case.out_dir / (
        f"Proposed Order - Conform Plaintiff's Name to Brendan Ngwa Nforbi "
        f"({EXEC_DATE}).pdf"
    )


def _pos_path(case: NameCase) -> Path:
    return case.out_dir / (
        f"Proof of Service - Name Conform Stipulation ({EXEC_DATE}).pdf"
    )


def _packet_path(case: NameCase) -> Path:
    tag = "" if case.agreed_on_record else " (not yet agreed)"
    return case.out_dir / (
        f"Name Conform Packet - Brendan Ngwa Nforbi{tag} ({EXEC_DATE}).pdf"
    )


def _email_path(case: NameCase) -> Path:
    return case.out_dir / (
        f"EMAIL_DRAFT_Name_Conform_Stipulation_{case.slug}.txt"
    )


def build_stipulation(case: NameCase) -> Path:
    path = _stip_path(case)
    path.parent.mkdir(parents=True, exist_ok=True)
    d = PleadingPaper(str(path), doc_title_footer=case.footer)
    _header(d)
    _caption(
        d,
        case,
        [
            "STIPULATION AND REQUEST FOR",
            "ORDER CONFORMING PLAINTIFF'S",
            "NAME ON THE DOCKET",
        ],
    )
    d.write_line("STIPULATION AND REQUEST FOR ORDER", bold=True, center=True)
    d.write_line("CONFORMING PLAINTIFF'S NAME", bold=True, center=True)
    d.blank_line()
    d.write_wrapped(
        f"Plaintiff {NEW_NAME}, appearing in propria persona and presently "
        f"identified on this docket as {case.current_docket_name}, and "
        f"{case.defendants_short}, through the counsel named below, "
        "stipulate and jointly request as follows:",
        first_indent=0,
    )
    d.blank_line()
    if case.quiet:
        d.write_wrapped(
            f"1.  Plaintiff has appeared in this District under more than "
            f"one name form. {NEW_NAME} and {case.current_docket_name} "
            "refer to the same natural person — the Plaintiff in this "
            "action. Plaintiff's existing PACER account (login "
            "bngwanforbi) records his first name as Brendan and his last "
            "name as Ngwa Nforbi. On September 1, 2026, the CAND ECF Help "
            "Desk advised that it cannot link this action to that account "
            "until the docket reflects the name on the account. That is "
            "the reason for this request.",
            first_indent=0,
        )
        d.blank_line()
        d.write_wrapped(
            f"2.  The Clerk shall amend the docket, the short title, the "
            f"CM/ECF party record, and the caption of this action so that "
            f"Plaintiff is identified as <<b:{NEW_NAME}>> — first name "
            f"Brendan, last name Ngwa Nforbi. Subsequent papers shall use "
            f"that caption.",
            first_indent=0,
        )
        d.blank_line()
        d.write_wrapped(
            "3.  This stipulation does not add, drop, or substitute any "
            "party. It is not an amendment of any claim, defense, or "
            "operative pleading. It is not a Fed. R. Civ. P. 25 "
            "substitution.",
            first_indent=0,
        )
        d.blank_line()
        d.write_wrapped(
            "4.  All prior filings, proofs of service, acceptances of "
            "service, and orders remain effective as to the same person. "
            "No party need be re-served by reason of this caption change.",
            first_indent=0,
        )
        d.blank_line()
        d.write_wrapped(
            "5.  This request is limited to the docket name. It does not "
            "seek any other relief.",
            first_indent=0,
        )
        d.blank_line()
        d.write_wrapped(
            "6.  Nothing in this stipulation is a waiver of any claim, "
            "defense, objection, or right, except the identity of "
            "Plaintiff as the same natural person and the docket name "
            "requested in paragraph 2.",
            first_indent=0,
        )
    else:
        d.write_wrapped(
            f"1.  The Clerk shall amend the docket, the short title, the "
            f"CM/ECF party record, and the caption of this action so that "
            f"Plaintiff is identified as <<b:{NEW_NAME}>> — first name "
            f"Brendan, last name Ngwa Nforbi — matching Plaintiff's existing "
            f"PACER account (login bngwanforbi). This is a clean swap of the "
            f"party name. Subsequent papers shall use that caption.",
            first_indent=0,
        )
        d.blank_line()
        d.write_wrapped(
            f"2.  {NEW_NAME} is the same natural person as "
            f"{case.current_docket_name}"
            + (
                " and as Brendan Ngehsi Newanforbi"
                if case.current_docket_name != "Brendan Ngehsi Newanforbi"
                else " and as Ngwa Nforbi"
            )
            + ". The names are one person. This stipulation does not add, drop, "
            "or substitute any party. It is not an amendment of any claim, "
            "defense, or operative pleading. It is not a Fed. R. Civ. P. 25 "
            "substitution. On September 1, 2026 the CAND ECF Help Desk advised "
            "that it cannot link this action to that PACER account until the "
            "docket reflects the name on the account.",
            first_indent=0,
        )
        d.blank_line()
        d.write_wrapped(
            "3.  " + case.counsel_stated,
            first_indent=0,
        )
        d.blank_line()
        d.write_wrapped(
            "4.  All prior filings, proofs of service, acceptances of service, "
            "orders, and related-case determinations remain effective as to the "
            "same person. No party need be re-served by reason of this caption "
            "change.",
            first_indent=0,
        )
        d.blank_line()
        if case.preserve:
            preserved = "; ".join(case.preserve)
            d.write_wrapped(
                "5.  <<b:No other date or deadline in this action is modified.>> "
                "This stipulation is not a stay of discovery and does not stay or "
                "defer any party's discovery obligations. Expressly unchanged, "
                f"without limitation: {preserved}.",
                first_indent=0,
            )
        else:
            d.write_wrapped(
                "5.  This request is limited to the docket name. It does not "
                "seek any other relief.",
                first_indent=0,
            )
        d.blank_line()
        d.write_wrapped(
            "6.  Nothing in this stipulation is a waiver of any claim, defense, "
            "objection, or right. No party concedes any issue other than the "
            "identity of Plaintiff as the same natural person and the docket "
            "name requested in paragraph 1. No party is authorized to affix "
            "Plaintiff's signature or to file this paper with Plaintiff's "
            "electronic signature except on the exact final file Plaintiff "
            "authorizes in a separate writing.",
            first_indent=0,
        )
    d.blank_line()
    d.write_wrapped(
        "7.  After the Clerk updates the party name, Plaintiff may ask the "
        "ECF Help Desk to link PACER login bngwanforbi to this action for "
        "pro se e-filing. This stipulation does not itself activate e-filing.",
        first_indent=0,
    )
    if not case.agreed_on_record:
        d.blank_line()
        d.write_wrapped(
            "8.  This is Plaintiff's executed counterpart only. Defendants "
            "have not signed. It is not a Civil L.R. 7-12 stipulation until "
            "every signature block below is signed.",
            first_indent=0,
        )
    d.blank_line()
    d.write_line("IT IS SO STIPULATED.", bold=True, center=True)
    d.blank_line()
    _plaintiff_sign_fixed(d, case.current_docket_name)
    for sig in case.counsel_sigs:
        d.blank_line()
        _counsel_block(d, sig)
    d.blank_line()
    d.ensure_space(4)
    d.write_line("PURSUANT TO STIPULATION, IT IS SO ORDERED.", bold=True)
    d.blank_line()
    d.write_line("Dated: ________________     ________________________________")
    d.write_line(f"                            {case.judge}")
    d.write_line("                            United States Magistrate Judge")
    d.save()
    return path


def _plaintiff_sign_fixed(d: PleadingPaper, current: str) -> None:
    d.ensure_space(8)
    d.write_line(f"Dated: {EXEC_DATE}")
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
    d.write_line(NEW_NAME_CAPS, bold=True, right=True, right_margin_offset=20)
    d.write_line("Plaintiff, In Propria Persona", right=True, right_margin_offset=20)
    d.write_line(
        f"(presently on this docket as {current})",
        right=True,
        right_margin_offset=20,
        size=10,
    )


def _counsel_block(d: PleadingPaper, sig: CounselSig) -> None:
    d.ensure_space(8)
    d.write_line("Dated: ________________")
    d.blank_line()
    d.write_line(SIG_LINE, right=True, right_margin_offset=20)
    d.write_line(sig.name, bold=True, right=True, right_margin_offset=20)
    d.write_line(sig.firm_or_title, right=True, right_margin_offset=20)
    for chunk in _right_chunks(sig.for_party, 42):
        d.write_line(chunk, right=True, right_margin_offset=20)


def _right_chunks(text: str, width: int) -> list[str]:
    words = text.split()
    lines: list[str] = []
    cur = ""
    for w in words:
        trial = f"{cur} {w}".strip()
        if len(trial) > width and cur:
            lines.append(cur)
            cur = w
        else:
            cur = trial
    if cur:
        lines.append(cur)
    return lines


def build_proposed_order(case: NameCase) -> Path:
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
    d.write_wrapped(
        "The Court has considered the parties' Civil L.R. 7-12 stipulation "
        "and request to conform Plaintiff's name on the docket. Good cause "
        "appearing, IT IS ORDERED that:",
        first_indent=0,
    )
    d.blank_line()
    d.write_wrapped(
        f"1.  The Clerk shall amend the docket, the short title, the "
        f"CM/ECF party record, and the caption of this action so that "
        f"Plaintiff is identified as <<b:{NEW_NAME}>> (first name Brendan; "
        f"last name Ngwa Nforbi), matching PACER login bngwanforbi. "
        f"Subsequent papers shall use that caption.",
        first_indent=0,
    )
    d.blank_line()
    d.write_wrapped(
        f"2.  {NEW_NAME} is the same natural person previously identified "
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
        "4.  This Order grants no other relief."
        if case.quiet
        else (
            "4.  No deadline, hearing, conference, pending motion, or discovery "
            "obligation is modified."
        ),
        first_indent=0,
    )
    d.blank_line()
    d.write_line("IT IS SO ORDERED.", bold=True)
    d.blank_line()
    d.blank_line()
    d.write_line("Dated: ________________     ________________________________")
    d.write_line(f"                            {case.judge}")
    d.write_line("                            United States Magistrate Judge")
    d.save()
    return path


def build_pos(case: NameCase) -> Path:
    path = _pos_path(case)
    title = (
        "Stipulation and Request for Order Conforming Plaintiff's Name "
        f"on the Docket; [Proposed] Order ({EXEC_DATE})"
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
            by_email=case.pos_by_email,
            signature_on_second_page=True,
        ),
    )
    return path


def build_email(case: NameCase) -> Path:
    path = _email_path(case)
    to_lines = [ln for ln in case.pos_recipients if "@" in ln]
    if case.matter == 33:
        to_lines = [
            "fiel.tigno@doj.ca.gov",
            "William.McMahon@doj.ca.gov",
        ]
    to = "; ".join(to_lines) if to_lines else "[counsel]"
    subject = (
        f"{case.case_no} — stipulation to conform Plaintiff's name to "
        f"{NEW_NAME} (clean swap; same person)"
    )
    amazon_warn = ""
    if not case.agreed_on_record:
        amazon_warn = (
            "\nThis is a draft counterpart only. I am not representing that "
            "Amazon or Accurate has agreed. Please review and, if you will "
            "stipulate, sign and return the exact PDF. Civil L.R. 7-12 "
            "requires every affected party's counsel.\n"
        )
    li_32 = ""
    if case.matter == 32:
        li_32 = (
            "\nYour signature is requested as non-opposition. It is not a "
            "notice of appearance and not acceptance of service on Officer "
            "Meza-Gonzalez. Dkt. 13 remains pending.\n"
        )
    if case.quiet:
        body = f"""To: {to}
Subject: Re: {case.case_no} — docket name correction

Counsel:

Attached is a revised stipulation and proposed order asking the Clerk
to identify me as {NEW_NAME}. I am the same person as
{case.current_docket_name}.

The revision adds a short explanation of the two name forms and the
PACER / ECF Help Desk reason, and it drops the date-by-date list. The
paper asks only for the docket name.

I have signed the enclosed counterpart. If it works, please add
counsel's signature and file that file. If you want a change, send a
redline and I will look at it.
{("" if not case.email_extra else chr(10) + case.email_extra)}
Thank you,
{NEW_NAME}
(209) 801-4442
bnn.cdl@gmail.com
"""
    else:
        body = f"""To: {to}
Subject: {subject}

Counsel:

Please find attached a Civil L.R. 7-12 stipulation and [proposed] order
to conform the Plaintiff name on this docket to {NEW_NAME}
(first name Brendan; last name Ngwa Nforbi).

This is a clean caption swap. Paragraph 2 states that the two name
forms are one person. It does not add or substitute a party, does not
amend any claim, and does not move any deadline, hearing, or pending
motion.

I have signed the attached counterpart. Please sign the same PDF (or
confirm in writing that I may file the attached file with your /s/ on
that exact version only). I will file after your signature is on it.
I do not authorize anyone to apply my electronic signature except on
one named final file that I have read.
{amazon_warn}{li_32}{("" if not case.email_extra else case.email_extra + chr(10))}
After the Clerk updates the party name I will ask the ECF Help Desk
to link PACER login bngwanforbi for pro se e-filing. The stipulation
does not itself turn e-filing on.

Thank you,
{NEW_NAME}
(209) 801-4442
bnn.cdl@gmail.com
"""
    path.write_text(body)
    return path


def build_docx(case: NameCase, pdf_path: Path) -> Path:
    """Word counterpart for counsel e-sign workflows. Same terms."""
    try:
        from docx import Document
        from docx.enum.text import WD_ALIGN_PARAGRAPH, WD_LINE_SPACING
        from docx.oxml.ns import qn
        from docx.shared import Inches, Pt
    except ImportError:
        import os

        os.system(f"{sys.executable} -m pip install -q python-docx")
        from docx import Document
        from docx.enum.text import WD_ALIGN_PARAGRAPH, WD_LINE_SPACING
        from docx.oxml.ns import qn
        from docx.shared import Inches, Pt

    path = pdf_path.with_suffix(".docx")
    font_name = "Times New Roman"
    size = Pt(12)
    sig_width = Inches(220 / 72)
    from signature_stamp import SIGNATURE_ASPECT  # noqa: E402

    sig_height = Inches((220 / 72) * SIGNATURE_ASPECT)

    def set_run(run, *, bold=False, run_size=size):
        run.font.name = font_name
        run._element.rPr.rFonts.set(qn("w:eastAsia"), font_name)
        run.font.size = run_size
        run.bold = bold

    def add_para(document, text="", *, bold=False, center=False, right=False, double=False):
        p = document.add_paragraph()
        pf = p.paragraph_format
        pf.space_before = Pt(0)
        pf.space_after = Pt(0)
        if double:
            pf.line_spacing_rule = WD_LINE_SPACING.DOUBLE
        else:
            pf.line_spacing = 1.0
            pf.line_spacing_rule = WD_LINE_SPACING.SINGLE
        if center:
            p.alignment = WD_ALIGN_PARAGRAPH.CENTER
        elif right:
            p.alignment = WD_ALIGN_PARAGRAPH.RIGHT
        if text:
            run = p.add_run(text)
            set_run(run, bold=bold)
        return p

    doc = Document()
    section = doc.sections[0]
    section.page_width = Inches(8.5)
    section.page_height = Inches(11)
    section.left_margin = Inches(1.0)
    section.right_margin = Inches(1.0)
    section.top_margin = Inches(1.0)
    section.bottom_margin = Inches(1.0)
    fp = section.footer.paragraphs[0]
    fp.alignment = WD_ALIGN_PARAGRAPH.CENTER
    run = fp.add_run(f"Case No. {case.case_no}  —  NAME CONFORM STIPULATION")
    set_run(run, run_size=Pt(9))

    for line, fn, _sz in ATTY:
        add_para(doc, line, bold=("Bold" in fn))
    add_para(doc, "")
    add_para(doc, "UNITED STATES DISTRICT COURT", bold=True, center=True)
    add_para(doc, "NORTHERN DISTRICT OF CALIFORNIA", bold=True, center=True)
    add_para(doc, "")
    add_para(doc, f"Case No. {case.case_no}", bold=True)
    add_para(doc, f"Judge: {case.judge}")
    add_para(doc, "")
    add_para(doc, "STIPULATION AND REQUEST FOR ORDER", bold=True, center=True)
    add_para(doc, "CONFORMING PLAINTIFF'S NAME", bold=True, center=True)
    add_para(doc, "")
    add_para(
        doc,
        f"Plaintiff {NEW_NAME}, appearing in propria persona and presently "
        f"identified on this docket as {case.current_docket_name}, and "
        f"{case.defendants_short}, through the counsel named below, "
        "stipulate and jointly request as follows:",
        double=True,
    )
    aka_other = (
        " and as Brendan Ngehsi Newanforbi"
        if case.current_docket_name != "Brendan Ngehsi Newanforbi"
        else " and as Ngwa Nforbi"
    )
    paras = [
        f"1.  The Clerk shall amend the docket, the short title, the "
        f"CM/ECF party record, and the caption of this action so that "
        f"Plaintiff is identified as {NEW_NAME} — first name Brendan, last "
        f"name Ngwa Nforbi — matching Plaintiff's existing PACER account "
        f"(login bngwanforbi). This is a clean swap of the party name. "
        f"Subsequent papers shall use that caption.",
        f"2.  {NEW_NAME} is the same natural person as "
        f"{case.current_docket_name}{aka_other}. The names are one person. "
        f"This stipulation does not add, drop, or substitute any party. It "
        f"is not an amendment of any claim, defense, or operative pleading. "
        f"It is not a Fed. R. Civ. P. 25 substitution. On September 1, 2026 "
        f"the CAND ECF Help Desk advised that it cannot link this action to "
        f"that PACER account until the docket reflects the name on the "
        f"account.",
        f"3.  {case.counsel_stated}",
        "4.  All prior filings, proofs of service, acceptances of service, "
        "orders, and related-case determinations remain effective as to the "
        "same person. No party need be re-served by reason of this caption "
        "change.",
        "5.  No other date or deadline in this action is modified. This "
        "stipulation is not a stay of discovery and does not stay or defer "
        "any party's discovery obligations. Expressly unchanged, without "
        f"limitation: {'; '.join(case.preserve)}.",
        "6.  Nothing in this stipulation is a waiver of any claim, defense, "
        "objection, or right. No party concedes any issue other than the "
        "identity of Plaintiff as the same natural person and the docket "
        "name requested in paragraph 1. No party is authorized to affix "
        "Plaintiff's signature or to file this paper with Plaintiff's "
        "electronic signature except on the exact final file Plaintiff "
        "authorizes in a separate writing.",
        "7.  After the Clerk updates the party name, Plaintiff may ask the "
        "ECF Help Desk to link PACER login bngwanforbi to this action for "
        "pro se e-filing. This stipulation does not itself activate e-filing.",
    ]
    if not case.agreed_on_record:
        paras.append(
            "8.  This is Plaintiff's executed counterpart only. Defendants "
            "have not signed. It is not a Civil L.R. 7-12 stipulation until "
            "every signature block below is signed."
        )
    for text in paras:
        add_para(doc, text, double=True)
    add_para(doc, "")
    add_para(doc, "IT IS SO STIPULATED.", bold=True, center=True)
    add_para(doc, "")
    add_para(doc, f"Dated: {EXEC_DATE}")
    add_para(doc, "")
    add_para(doc, "")
    sig_p = add_para(doc, "", right=True)
    run = sig_p.add_run()
    run.add_picture(SIGNATURE_PATH, width=sig_width, height=sig_height)
    add_para(doc, SIG_LINE, right=True)
    add_para(doc, NEW_NAME_CAPS, bold=True, right=True)
    add_para(doc, "Plaintiff, In Propria Persona", right=True)
    add_para(doc, f"(presently on this docket as {case.current_docket_name})", right=True)
    for sig in case.counsel_sigs:
        add_para(doc, "")
        add_para(doc, "Dated: ________________")
        add_para(doc, SIG_LINE, right=True)
        add_para(doc, sig.name, bold=True, right=True)
        add_para(doc, sig.firm_or_title, right=True)
        add_para(doc, sig.for_party, right=True)
    add_para(doc, "")
    add_para(doc, "PURSUANT TO STIPULATION, IT IS SO ORDERED.", bold=True)
    add_para(doc, "")
    add_para(doc, f"Dated: ________________     {case.judge}")
    add_para(doc, "                            United States Magistrate Judge")
    doc.save(str(path))
    return path


def main() -> None:
    if not Path(SIGNATURE_PATH).is_file():
        raise SystemExit(f"Missing signature image: {SIGNATURE_PATH}")
    for case in CASES:
        stip = build_stipulation(case)
        order = build_proposed_order(case)
        pos = build_pos(case)
        packet = _packet_path(case)
        assemble([stip, order, pos], packet)
        docx = build_docx(case, stip)
        email = build_email(case)
        short = publish_short_link(stip, case.short_slug) if case.short_slug else None
        print(f"M{case.matter} {case.slug}:")
        print(f"  {stip}")
        print(f"  {order}")
        print(f"  {pos}")
        print(f"  {packet}")
        print(f"  {docx}")
        print(f"  {email}")
        if short:
            print(f"  /{case.short_slug}.pdf")


if __name__ == "__main__":
    main()
