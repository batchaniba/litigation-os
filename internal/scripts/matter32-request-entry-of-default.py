#!/usr/bin/env python3
"""Matter 32 — Request for Clerk's Entry of Default (Rule 55(a)).

Nforbi v. Meza-Gonzalez et al., N.D. Cal. No. 4:26-cv-08271-ASK.

Keyed to the September 18, 2026 ECF docket report:
  Melano — Dkt. 12: served 8/14/2026, answer due 9/4/2026
  Meza   — Dkt. 16: served 8/27/2026, answer due 9/17/2026

This is entry of default only (Rule 55(a)). It is not a motion for default
judgment (Rule 55(b)). Dkt. 13 remains pending and is not withdrawn.

    python3 internal/scripts/matter32-request-entry-of-default.py
    python3 internal/scripts/matter32-request-entry-of-default.py \\
        --date "September 18, 2026" --mailed-from "San Jose, California"

POS is valid only if mailed that day from the stated city. Not filed until
presented to the clerk.
"""

from __future__ import annotations

import argparse
import sys
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
from short_link import publish_short_link  # noqa: E402
from signature_stamp import SIGNATURE_NATIVE_PX, SIGNATURE_PATH  # noqa: E402

ROOT = SCRIPT_DIR.parents[1]
OUT_DIR = ROOT / "internal/public/documents/matter-32/ndcal"

DEFAULT_DATE = "September 18, 2026"
DEFAULT_MAILED_FROM = "San Jose, California"
SHORT_LINK_SLUG = "meza-clerk-default"

CASE_NO = "4:26-cv-08271-ASK"
JUDGE = "Hon. Ajay S. Krishnan"
RELATED = "3:26-cv-05953-CRB"

PLAINTIFF_BLOCK = [
    ("BRENDAN NGWA NFORBI", "Times-Bold", 12),
    ("Plaintiff, In Propria Persona", "Times-Roman", 12),
    ("1455 Cat Tail Drive", "Times-Roman", 12),
    ("Stockton, CA 95204", "Times-Roman", 12),
    ("Telephone: (209) 801-4442", "Times-Roman", 12),
    ("E-mail: bnn.cdl@gmail.com", "Times-Roman", 12),
]

COURT_LINE1 = "UNITED STATES DISTRICT COURT"
COURT_LINE2 = "NORTHERN DISTRICT OF CALIFORNIA"

CAPTION_LEFT = [
    ("BRENDAN NGWA NFORBI,", True, False),
    ("", False, False),
    ("                          Plaintiff,", False, False),
    ("", False, False),
    ("       v.", False, False),
    ("", False, False),
    ("SANTIAGO MEZA-GONZALEZ", True, False),
    ("(CHP #023295); JOSE MELANO", True, False),
    ("(CHP #023054); and DOES 1-10,", True, False),
    ("", False, False),
    ("                          Defendants.", False, False),
]

SIGNOFF_NAME = "BRENDAN NGWA NFORBI"
SIGNOFF_ROLE = "Plaintiff, In Propria Persona"
SIG_LINE = "___________________________________"

REQ_FOOTER = (
    "REQUEST FOR ENTRY OF DEFAULT -- "
    "NFORBI v. MEZA-GONZALEZ ET AL."
)
DECL_FOOTER = (
    "DECLARATION ISO REQUEST FOR ENTRY OF DEFAULT -- "
    "NFORBI v. MEZA-GONZALEZ ET AL."
)
ENTRY_FOOTER = (
    "[PROPOSED] CLERK'S ENTRY OF DEFAULT -- "
    "NFORBI v. MEZA-GONZALEZ ET AL."
)

LI_BLOCK = [
    "Haiyang A. Li, Deputy Attorney General",
    "Office of the Attorney General",
    "300 South Spring Street, Suite 1702",
    "Los Angeles, CA 90013-1230",
    "Haiyang.Li@doj.ca.gov",
    "Counsel for Captain G. Serrato in the related action;",
    "prior counsel for Meza-Gonzalez and Melano on this incident",
]

MELANO_BLOCK = [
    "Jose Melano, CHP #023054",
    "California Highway Patrol, South Sacramento Area",
    "6 Massie Court",
    "Sacramento, CA 95823",
    "Defendant (Dkt. 12 — answer due September 4, 2026)",
]

MEZA_BLOCK = [
    "Santiago Meza-Gonzalez, CHP #023295",
    "California Highway Patrol, Modesto Area",
    "4030 Kiernan Avenue",
    "Modesto, CA 95356",
    "Defendant (Dkt. 16 — answer due September 17, 2026)",
]


def _caption_right(title_lines: list[str]) -> list[tuple[str, bool, bool]]:
    rows: list[tuple[str, bool, bool]] = [
        (f"Case No. {CASE_NO}", True, False),
        ("", False, False),
    ]
    for line in title_lines:
        rows.append((line, True, False))
    rows.extend(
        [
            ("", False, False),
            ("Fed. R. Civ. P. 55(a)", False, False),
            ("", False, False),
            (f"Judge: {JUDGE}", False, False),
            (f"Related: {RELATED}", False, False),
        ]
    )
    return rows


REQ_CAPTION_RIGHT = _caption_right(
    [
        "PLAINTIFF'S REQUEST FOR",
        "CLERK'S ENTRY OF DEFAULT",
        "AS TO DEFENDANTS",
        "MEZA-GONZALEZ AND MELANO",
    ]
)

DECL_CAPTION_RIGHT = _caption_right(
    [
        "DECLARATION OF BRENDAN",
        "NGWA NFORBI IN SUPPORT OF",
        "REQUEST FOR CLERK'S ENTRY",
        "OF DEFAULT",
    ]
)

ENTRY_CAPTION_RIGHT = _caption_right(
    [
        "[PROPOSED] CLERK'S ENTRY",
        "OF DEFAULT AS TO",
        "DEFENDANTS MEZA-GONZALEZ",
        "AND MELANO",
    ]
)


REQ_CONTENT = [
    ("PARA",
     "TO THE CLERK OF COURT AND TO DEFENDANTS SANTIAGO MEZA-GONZALEZ AND "
     "JOSE MELANO:"),

    ("PARA",
     "Plaintiff BRENDAN NGWA NFORBI, appearing in propria persona, requests "
     "that the Clerk enter the defaults of Defendants Santiago Meza-Gonzalez "
     "and Jose Melano under Federal Rule of Civil Procedure 55(a). The facts "
     "are in the accompanying declaration."),

    ("HEADER", "I.\nTHE RECORD ON THE DOCKET"),

    ("PARA",
     "The operative pleading is the First Amended Complaint filed August 17, "
     "2026 (Dkt. 5). The Clerk issued summonses as to both defendants on "
     "August 10, 2026 (Dkt. 3)."),

    ("PARA",
     "As to Defendant Jose Melano, Document 12 is a summons returned "
     "executed. The docket entry states that Melano was served on August 14, "
     "2026, and that his answer was due September 4, 2026."),

    ("PARA",
     "As to Defendant Santiago Meza-Gonzalez, Document 16 is a summons "
     "returned executed. The docket entry states that Meza-Gonzalez was "
     "served on August 27, 2026, and that his answer was due September 17, "
     "2026."),

    ("HEADER", "II.\nFAILURE TO PLEAD OR OTHERWISE DEFEND"),

    ("PARA",
     "As of the date of this request, neither Melano nor Meza-Gonzalez has "
     "filed an answer, a Rule 12 motion, or any other paper pleading or "
     "defending against the First Amended Complaint. Neither defendant has "
     "appeared. No attorney has appeared for either defendant on this docket."),

    ("PARA",
     "Plaintiff's Civil L.R. 7-11 administrative motion directing Deputy "
     "Attorney General Haiyang A. Li to accept service for Meza-Gonzalez "
     "(Dkt. 13) remains pending. This request does not withdraw Document 13. "
     "It seeks Rule 55(a) entry of default on the answer-due dates the Clerk "
     "has already entered on Documents 12 and 16."),

    ("HEADER", "III.\nRELIEF REQUESTED"),

    ("PARA",
     "Plaintiff requests that the Clerk enter the defaults of Santiago "
     "Meza-Gonzalez and Jose Melano under Rule 55(a). This is not a request "
     "for default judgment under Rule 55(b). A proposed Clerk's Entry of "
     "Default accompanies this request."),
]


DECL_CONTENT = [
    ("PARA",
     "I, BRENDAN NGWA NFORBI, declare as follows:"),

    ("LIST_ITEM",
     "1.  I am the Plaintiff in this action. I am over eighteen years of age. "
     "I make this declaration from my personal knowledge in support of "
     "Plaintiff's Request for Clerk's Entry of Default as to Defendants "
     "Santiago Meza-Gonzalez and Jose Melano. If called, I could and would "
     "testify competently to these facts."),

    ("LIST_ITEM",
     "2.  This action is Nforbi v. Meza-Gonzalez et al., No. 4:26-cv-08271-ASK "
     "(N.D. Cal.), related to Newanforbi v. Serrato, No. 3:26-cv-05953-CRB. "
     "The operative pleading is the First Amended Complaint (Dkt. 5)."),

    ("LIST_ITEM",
     "3.  On August 31, 2026, the Clerk entered Document 12: Summons Returned "
     "Executed as to Jose Melano. Document 12 states that Melano was served "
     "on August 14, 2026, and that his answer was due September 4, 2026. The "
     "underlying AO 440 return (also filed as Dkt. 5-1) shows service by "
     "Clifford Black of C&P Process Server on Officer Reed at California "
     "Highway Patrol, South Sacramento Area, 6 Massie Court, Sacramento, "
     "California 95823, on August 14, 2026. Officer Reed is designated by "
     "law to accept service of process on behalf of the California Highway "
     "Patrol at that station."),

    ("LIST_ITEM",
     "4.  On September 14, 2026, the Clerk entered Document 16: Summons "
     "Returned Executed as to Santiago Meza-Gonzalez. Document 16 states "
     "that Meza-Gonzalez was served on August 27, 2026, and that his answer "
     "was due September 17, 2026. Document 16 attaches the Declaration of "
     "Service and Declaration of Reasonable Diligence of Daniel Fischer "
     "(Run With It order 15645547), reflecting substituted delivery at "
     "California Highway Patrol, Modesto Area, 4030 Kiernan Avenue, Modesto, "
     "California 95356, on August 27, 2026, after attempts on August 25 and "
     "August 26, 2026."),

    ("LIST_ITEM",
     "5.  I reviewed the PACER / CM/ECF docket for this action on September "
     "18, 2026. As of that review, and as of the date of this declaration, "
     "neither Melano nor Meza-Gonzalez has filed an answer, a motion under "
     "Rule 12, a notice of appearance, or any other paper pleading or "
     "otherwise defending against the First Amended Complaint. No counsel "
     "has appeared for either defendant on this docket."),

    ("LIST_ITEM",
     "6.  The time for Melano to plead or otherwise defend, as stated on "
     "Document 12 (September 4, 2026), has expired. The time for "
     "Meza-Gonzalez to plead or otherwise defend, as stated on Document 16 "
     "(September 17, 2026), has expired."),

    ("LIST_ITEM",
     "7.  To my knowledge, neither Melano nor Meza-Gonzalez is an infant or "
     "an incompetent person."),

    ("LIST_ITEM",
     "8.  To my knowledge after reasonable investigation of the record in "
     "this action and in the related civil matters arising from the same "
     "November 1, 2024 incident, neither Melano nor Meza-Gonzalez is in "
     "military service within the meaning of the Servicemembers Civil Relief "
     "Act, 50 U.S.C. §§ 3901–4043. Both are California Highway Patrol "
     "officers sued in their individual capacities."),

    ("LIST_ITEM",
     "9.  Document 13 (Plaintiff's administrative motion directing Deputy "
     "Attorney General Haiyang A. Li to accept service for Meza-Gonzalez) "
     "remains pending. I am not withdrawing Document 13. This request seeks "
     "entry of default under Rule 55(a) based on the answer-due dates the "
     "Clerk has entered on Documents 12 and 16."),

    ("LIST_ITEM",
     "10. I am requesting entry of default only. I am not requesting default "
     "judgment by this paper."),

    ("PARA",
     "I declare under penalty of perjury under the laws of the United States "
     "of America that the foregoing is true and correct."),
]


ENTRY_CONTENT = [
    ("PARA",
     "It appearing from the record and from the Declaration of Brendan Ngwa "
     "Nforbi that Defendants Santiago Meza-Gonzalez and Jose Melano have "
     "been served with process; that the time within which each was required "
     "to plead or otherwise defend has expired; and that each has failed to "
     "plead or otherwise defend as provided by the Federal Rules of Civil "
     "Procedure:"),

    ("PARA",
     "NOW, THEREFORE, the defaults of Defendants Santiago Meza-Gonzalez and "
     "Jose Melano are hereby ENTERED pursuant to Federal Rule of Civil "
     "Procedure 55(a)."),
]


def _header_block(d: PleadingPaper, right_caption: list) -> None:
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
        CAPTION_LEFT, right_caption, caption_size=9, tight_lh=12, boxed=True
    )
    d.blank_line()


def _render_body(d: PleadingPaper, content: list[tuple[str, str]]) -> None:
    for kind, text in content:
        if kind == "HEADER":
            lines = text.split("\n")
            d.ensure_space(len(lines) + 2)
            for line in lines:
                d.write_line(line, bold=True, center=True)
            d.blank_line()
        elif kind == "PARA":
            d.write_wrapped(text, first_indent=36)
            d.blank_line()
        elif kind == "LIST_ITEM":
            d.write_wrapped(text, indent=18, first_indent=0)
            d.blank_line()
        else:
            raise ValueError(f"unknown content kind {kind!r}")


def _signature(d: PleadingPaper, exec_date: str, *, place: str | None = None) -> None:
    d.ensure_space(10)
    if place:
        d.write_line(f"Executed on {exec_date}, at {place}.")
    else:
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
    d.write_line(SIGNOFF_NAME, right=True, right_margin_offset=20)
    d.write_line(SIGNOFF_ROLE, right=True, right_margin_offset=20)


def _pos_fields(exec_date: str, mailed_from: str) -> ProofOfServiceFields:
    recipients: list[str] = []
    recipients.extend(LI_BLOCK)
    recipients.append("")
    recipients.extend(MELANO_BLOCK)
    recipients.append("")
    recipients.extend(MEZA_BLOCK)
    return ProofOfServiceFields(
        plaintiff_line="BRENDAN NGWA NFORBI",
        plaintiff_role="Plaintiff",
        defendant_lines=[
            "SANTIAGO MEZA-GONZALEZ; JOSE MELANO;",
            "and DOES 1-10",
        ],
        defendant_role="Defendants",
        case_number=CASE_NO,
        district_line=DISTRICT_NDCAL,
        title="PROOF OF SERVICE",
        service_date=exec_date,
        document_title=(
            "Plaintiff's Request for Clerk's Entry of Default as to "
            "Defendants Meza-Gonzalez and Melano; Declaration; "
            "[Proposed] Clerk's Entry of Default"
        ),
        mailing_location=mailed_from,
        recipients=recipients,
        server_name="Brendan Ngwa Nforbi",
        stamp_signature=True,
        signature_on_second_page=True,
    )


def paths_for(exec_date: str) -> dict[str, Path]:
    short = "Sep 18 2026" if exec_date == DEFAULT_DATE else exec_date
    return {
        "request": OUT_DIR / (
            f"Request for Clerk Entry of Default - Meza-Gonzalez and Melano "
            f"(N.D. Cal. 4-26-cv-08271-ASK) ({short}).pdf"
        ),
        "declaration": OUT_DIR / (
            f"Declaration ISO Request for Clerk Entry of Default - "
            f"Meza-Gonzalez and Melano (N.D. Cal. 4-26-cv-08271-ASK) ({short}).pdf"
        ),
        "entry": OUT_DIR / (
            f"Proposed Clerk Entry of Default - Meza-Gonzalez and Melano "
            f"(N.D. Cal. 4-26-cv-08271-ASK) ({short}).pdf"
        ),
        "pos": OUT_DIR / (
            f"Proof of Service - Request for Clerk Entry of Default "
            f"(Meza Melano) ({short}).pdf"
        ),
        "packet": OUT_DIR / (
            f"Request for Clerk Entry of Default Packet - Meza-Gonzalez and "
            f"Melano (N.D. Cal. 4-26-cv-08271-ASK) ({short}).pdf"
        ),
        "instructions": OUT_DIR / (
            f"FILING_INSTRUCTIONS_Clerk_Entry_of_Default_Meza_Melano "
            f"({short}).txt"
        ),
        "email": OUT_DIR / (
            f"EMAIL_DRAFT_Li_Clerk_Entry_of_Default_Meza_Melano ({short}).txt"
        ),
    }


def build_request(out: Path, exec_date: str) -> Path:
    out.parent.mkdir(parents=True, exist_ok=True)
    d = PleadingPaper(str(out), doc_title_footer=REQ_FOOTER)
    _header_block(d, REQ_CAPTION_RIGHT)
    _render_body(d, REQ_CONTENT)
    _signature(d, exec_date)
    d.save()
    return out


def build_declaration(out: Path, exec_date: str, mailed_from: str) -> Path:
    out.parent.mkdir(parents=True, exist_ok=True)
    d = PleadingPaper(str(out), doc_title_footer=DECL_FOOTER)
    _header_block(d, DECL_CAPTION_RIGHT)
    _render_body(d, DECL_CONTENT)
    _signature(d, exec_date, place=mailed_from)
    d.save()
    return out


def build_proposed_entry(out: Path, exec_date: str) -> Path:
    out.parent.mkdir(parents=True, exist_ok=True)
    d = PleadingPaper(str(out), doc_title_footer=ENTRY_FOOTER)
    _header_block(d, ENTRY_CAPTION_RIGHT)
    _render_body(d, ENTRY_CONTENT)
    d.ensure_space(8)
    d.write_line(f"Dated: _______________, 2026")
    d.blank_line()
    d.blank_line()
    d.write_line("___________________________________________")
    d.write_line("Clerk, United States District Court")
    d.write_line("Northern District of California")
    d.save()
    return out


def build_pos(out: Path, exec_date: str, mailed_from: str) -> Path:
    if not Path(SIGNATURE_PATH).is_file():
        raise SystemExit(f"Missing universal signature: {SIGNATURE_PATH}")
    out.parent.mkdir(parents=True, exist_ok=True)
    return build_proof_of_service(out, _pos_fields(exec_date, mailed_from))


def write_instructions(out: Path, exec_date: str, mailed_from: str) -> Path:
    out.parent.mkdir(parents=True, exist_ok=True)
    text = f"""PLAINTIFF COPY — DO NOT FILE — DO NOT MAIL THIS SHEET TO DEFENDANTS
Nforbi v. Meza-Gonzalez et al., 4:26-cv-08271-ASK
Papers dated {exec_date}. City of mailing: {mailed_from}.

WHAT THIS IS
  Rule 55(a) request for the Clerk to ENTER DEFAULT as to Melano and Meza.
  Not a Rule 55(b) motion for default judgment. Damages stay for later.

FILE WITH THE CLERK (San Jose / Oakland as applicable)
  1. Request for Clerk's Entry of Default
  2. Declaration of Brendan Ngwa Nforbi
  3. [Proposed] Clerk's Entry of Default
  4. Proof of Service

SERVE THE SAME DAY (first-class mail)
  Li (Spring Street + email courtesy)
  Melano @ CHP South Sacramento
  Meza @ CHP Modesto
  Use the POS. Send Li the covering email. No GitHub. No repo URL.

DOCKET ANCHORS (Sep. 18, 2026 ECF)
  Melano — Dkt. 12: served 8/14/2026, answer due 9/4/2026 (clean)
  Meza   — Dkt. 16: served 8/27/2026, answer due 9/17/2026 (ECF face)

LEAVE ON FILE
  Dkt. 13 (Li accept-service admin motion). Do not withdraw it.
  Sep. 17 § 415.20(b) mailing papers — still file those if not filed;
  they strengthen Meza service even if the Clerk enters on Dkt. 16.

IF THE CLERK ENTERS ONLY AS TO MELANO
  That is still a win. Re-present Meza after the § 415.20 mailing is on
  the docket, or after Dkt. 13 is granted.

DO NOT
  Do not ask for default judgment in this packet.
  Do not put a GitHub or portfolio URL in the email or the filing.
"""
    out.write_text(text)
    return out


def write_email(out: Path, exec_date: str) -> Path:
    out.parent.mkdir(parents=True, exist_ok=True)
    text = f"""To: Haiyang.Li@doj.ca.gov
Subject: Nforbi v. Meza-Gonzalez, 4:26-cv-08271-ASK — Request for Clerk's Entry of Default (Rule 55(a))

Counsel:

I am filing a Request for Clerk's Entry of Default under Federal Rule of Civil Procedure 55(a) as to Officers Jose Melano and Santiago Meza-Gonzalez.

Document 12 states Melano was served August 14, 2026, with an answer due September 4, 2026. Document 16 states Meza-Gonzalez was served August 27, 2026, with an answer due September 17, 2026. Neither has appeared or responded on this docket.

This is entry of default only. It is not a motion for default judgment. Document 13 remains pending and is not withdrawn.

The request, supporting declaration, proposed Clerk's entry, and proof of service are attached and are being filed.

Thank you,
Brendan Ngwa Nforbi
Plaintiff, In Propria Persona
"""
    out.write_text(text)
    return out


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--date", default=DEFAULT_DATE)
    parser.add_argument("--mailed-from", default=DEFAULT_MAILED_FROM)
    args = parser.parse_args()

    if not Path(SIGNATURE_PATH).is_file():
        raise SystemExit(f"Missing universal signature: {SIGNATURE_PATH}")

    outs = paths_for(args.date)
    build_request(outs["request"], args.date)
    build_declaration(outs["declaration"], args.date, args.mailed_from)
    build_proposed_entry(outs["entry"], args.date)
    build_pos(outs["pos"], args.date, args.mailed_from)
    write_instructions(outs["instructions"], args.date, args.mailed_from)
    write_email(outs["email"], args.date)
    n = assemble(
        [
            outs["request"],
            outs["declaration"],
            outs["entry"],
            outs["pos"],
        ],
        outs["packet"],
    )
    publish_short_link(outs["packet"], SHORT_LINK_SLUG)
    print(f"request:      {outs['request']}")
    print(f"declaration:  {outs['declaration']}")
    print(f"entry:        {outs['entry']}")
    print(f"pos:          {outs['pos']}")
    print(f"packet:       {outs['packet']} ({n} pp.)")
    print(f"instructions: {outs['instructions']}")
    print(f"email:        {outs['email']}")
    print(f"short link:   /{SHORT_LINK_SLUG}")
    print(
        f"FILED_STATUS=False; execution date={args.date}; "
        f"mailed from={args.mailed_from}"
    )


if __name__ == "__main__":
    main()
