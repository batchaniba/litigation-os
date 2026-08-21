#!/usr/bin/env python3
"""Matter 26 — AMENDED Notice Regarding Caption, and Request for Intradistrict
Reassignment to the Sacramento Division.

Newanforbi v. United Parcel Service, Inc., USDC E.D. Cal. No. 1:26-at-03195.

Supersedes matter26-edcal-errata-and-intradistrict-reassignment.py (executed
and mailed Aug. 20, 2026). Paragraph 3 of that notice stated that
"Ngwanforbi" is a typographical error rather than an alias and that Plaintiff
had appeared under no other name. That statement was wrong: Ngwanforbi is a
name Plaintiff has used, and Defendant's Rule 7.1 also-known-as recital is
accurate. This amended notice withdraws the statement at the first
opportunity and drops the a.k.a. objection entirely.

The relief sought is unchanged, because it never depended on that paragraph.
The caption of a removed action is the caption of the state-court action from
which it was removed; this action was filed and served as BRENDAN NGEHSI
NEWANFORBI, so that is what the docket should read, whether or not other
names exist. Part II now rests on that ground alone.

Rendered on the shared California pleading-paper engine and signed with the
portfolio universal signature.

    python3 internal/scripts/matter26-edcal-amended-notice-caption-and-reassignment.py \
        [--date "August 21, 2026"] [--mailed-from "San Jose, California"] [OUT_PDF]
"""

from __future__ import annotations

import argparse
import sys
from pathlib import Path

SCRIPT_DIR = Path(__file__).resolve().parent
sys.path.insert(0, str(SCRIPT_DIR / "lib"))
sys.path.insert(0, str(SCRIPT_DIR))
from pleading_paper import CONTENT_LEFT, PleadingPaper  # noqa: E402
from signature_stamp import SIGNATURE_NATIVE_PX, SIGNATURE_PATH  # noqa: E402

ROOT = SCRIPT_DIR.parents[1]
DEFAULT_OUT = (
    ROOT
    / "internal/public/documents/matter-26"
    / "Amended Notice Regarding Caption and Request for Intradistrict Reassignment (E.D. Cal. 1-26-at-03195) (Aug 21 2026).pdf"
)

DEFAULT_EXEC_DATE = "August 21, 2026"
DEFAULT_MAILED_FROM = "San Jose, California"
FOOTER = (
    "PLAINTIFF'S AMENDED NOTICE REGARDING CAPTION AND REQUEST FOR INTRADISTRICT "
    "REASSIGNMENT -- NEWANFORBI v. UNITED PARCEL SERVICE, INC."
)

PLAINTIFF_BLOCK = [
    ("BRENDAN NGEHSI NEWANFORBI", "Times-Bold", 12),
    ("Plaintiff, In Propria Persona", "Times-Roman", 12),
    ("1455 Cat Tail Drive", "Times-Roman", 12),
    ("Stockton, CA 95204", "Times-Roman", 12),
    ("Telephone: (209) 801-4442", "Times-Roman", 12),
    ("E-mail: bnn.cdl@gmail.com", "Times-Roman", 12),
]

COURT_LINE1 = "UNITED STATES DISTRICT COURT"
COURT_LINE2 = "EASTERN DISTRICT OF CALIFORNIA"

CAPTION_LEFT = [
    ("BRENDAN NGEHSI NEWANFORBI,", True, False),
    ("", False, False),
    ("                          Plaintiff,", False, False),
    ("", False, False),
    ("       v.", False, False),
    ("", False, False),
    ("UNITED PARCEL SERVICE, INC.; and", True, False),
    ("DOES 1 through 10, inclusive,", True, False),
    ("", False, False),
    ("                          Defendants.", False, False),
]

CAPTION_RIGHT = [
    ("Case No. 1:26-at-03195", False, False),
    ("", False, False),
    ("PLAINTIFF'S AMENDED NOTICE", True, False),
    ("REGARDING CAPTION, AND", True, False),
    ("REQUEST FOR INTRADISTRICT", True, False),
    ("REASSIGNMENT TO THE", True, False),
    ("SACRAMENTO DIVISION", True, False),
    ("", False, False),
    ("(E.D. Cal. L.R. 120(d), (f);", False, False),
    ("28 U.S.C. 1441(a))", False, False),
    ("", False, False),
    ("Supersedes Plaintiff's Notice of", False, True),
    ("Errata executed August 20, 2026", False, True),
    ("", False, False),
    ("[No hearing requested]", False, True),
]

CONTENT = [
    ("PARA",
     "TO THE HONORABLE COURT, AND TO DEFENDANT UNITED PARCEL SERVICE, INC. AND ITS "
     "ATTORNEYS OF RECORD:"),
    ("PARA",
     "Plaintiff BRENDAN NGEHSI NEWANFORBI, appearing in propria persona, submits this "
     "Amended Notice, which supersedes in its entirety Plaintiff's Notice of Errata "
     "Correcting Misnomer, and Request for Intradistrict Reassignment to the Sacramento "
     "Division, executed and mailed to the Clerk on August 20, 2026. It is submitted to "
     "withdraw one statement in that notice at the first opportunity, and otherwise seeks "
     "the same two administrative corrections, neither of which requires a hearing."),

    ("HEADER", "I.\nCORRECTION TO THE AUGUST 20, 2026 NOTICE"),
    ("PARA",
     "1. Paragraph 3 of the August 20, 2026 notice stated that \"Ngwanforbi\" is a "
     "typographical error rather than an alias, and that Plaintiff had not appeared under "
     "any name other than BRENDAN NGEHSI NEWANFORBI. That statement was incorrect. "
     "Plaintiff has used the name Brendan Ngwanforbi, and Defendant's Notice of Interested "
     "Parties and Corporate Disclosure Statement (Doc. 1-3) is accurate insofar as it "
     "identifies that name as an also-known-as. Plaintiff withdraws paragraph 3 in full, "
     "withdraws any objection to Defendant's also-known-as recital, and regrets the error."),
    ("PARA",
     "2. The withdrawal does not affect the relief Plaintiff seeks. As set out in Part II "
     "below, the request that the docket name Plaintiff as BRENDAN NGEHSI NEWANFORBI rests "
     "on the caption of the action that was removed, not on whether other names exist."),

    ("HEADER", "II.\nTHE DOCKET SHOULD CARRY THE CAPTION OF THE ACTION REMOVED"),
    ("PARA",
     "3. This action was filed in the Superior Court of the State of California for the "
     "County of San Joaquin on July 15, 2026, Case No. STK-CV-UWT-2026-0009113, under the "
     "name BRENDAN NGEHSI NEWANFORBI. That is the name on the Summons, on the Complaint, "
     "and on every paper served on Defendant in that action."),
    ("PARA",
     "4. On removal, this Court takes the action as it stood in the state court, and the "
     "caption of the removed action is the caption of the state-court action. Defendant's "
     "removal package does not carry that caption consistently. The Notice of Removal "
     "captions the action \"BRENDAN NGWANFORBI\" and repeats that spelling at paragraph 4, "
     "while the Declaration of Ashley Felsing (Doc. 1-2) and the Notice of Interested "
     "Parties (Doc. 1-3) both caption it \"BRENDAN NGEHSI NEWANFORBI.\""),
    ("PARA",
     "5. Plaintiff respectfully requests that the docket in this Court carry the caption of "
     "the action that was removed -- BRENDAN NGEHSI NEWANFORBI -- which is also the name "
     "under which Plaintiff appears in this Court. Plaintiff raises the point now so that "
     "the two captions do not diverge as the case proceeds, and so that filings here can be "
     "matched to the state-court record from which they came."),

    ("HEADER", "III.\nTHIS ACTION BELONGS IN THE SACRAMENTO DIVISION"),
    ("PARA",
     "6. Defendant removed this action on August 20, 2026. The Notice of Removal was filed "
     "under Case No. 1:26-at-03195. The \"1:\" prefix designates the Fresno Division of this "
     "Court."),
    ("PARA",
     "7. The action arose in, and was pending in, San Joaquin County. A defendant may remove "
     "only to \"the district court of the United States for the district and division "
     "embracing the place where such action is pending.\" 28 U.S.C. 1441(a)."),
    ("PARA",
     "8. Under this Court's Local Rule 120(d), civil actions arising in San Joaquin County "
     "are to be commenced in the United States District Court sitting in Sacramento. San "
     "Joaquin County is not among the counties assigned to the Fresno Division. The division "
     "embracing the place where this action was pending is therefore Sacramento."),
    ("PARA",
     "9. Defendant does not appear to contend otherwise. Paragraph 37 of the Notice of "
     "Removal states that \"Plaintiff's Complaint was filed in the Superior Court of the "
     "County of San Joaquin\" and that \"This Court is part of the division in which the "
     "Superior Court action is pending,\" citing 28 U.S.C. 84(b) and 1446(a). That is the "
     "correct standard. Applying it to San Joaquin County yields the Sacramento Division. "
     "This request asks for nothing more than the assignment Defendant's own papers describe."),
    ("PARA",
     "10. Local Rule 120(f) provides for transfer where an action has not been commenced in "
     "the proper court in accordance with Rule 120, on the motion of any party, on "
     "stipulation, or for other good cause. Good cause is plain here and the correction "
     "costs the Court and the parties almost nothing: no district judge or magistrate judge "
     "has been assigned, no scheduling order has issued, no motion has been noticed, and "
     "nothing has been briefed. To the extent the Court prefers that this request be "
     "presented as a noticed motion or by stipulation, Plaintiff will promptly file one, and "
     "will first ask Defendant whether it will stipulate."),
    ("PARA",
     "11. Reassignment also serves the convenience of the parties and of any witnesses. "
     "This action arose in San Joaquin County: the Complaint was filed there, the Superior "
     "Court in which the action was pending sits there, and the state-court record now "
     "before this Court originates there. Sacramento County adjoins San Joaquin County; "
     "Fresno lies roughly one hundred thirty miles to the south. Defendant identifies no "
     "connection between this action and any county assigned to the Fresno Division, and "
     "none appears on the face of its removal papers."),

    ("HEADER", "IV.\nRELIEF REQUESTED"),
    ("PARA", "12. Plaintiff respectfully requests that the Court:"),
    ("LIST_ITEM",
     "(a) direct the Clerk of Court to carry the caption of the removed action, naming "
     "Plaintiff as BRENDAN NGEHSI NEWANFORBI;"),
    ("LIST_ITEM",
     "(b) reassign this action to the Sacramento Division of this Court under Local Rule "
     "120(f), and direct that it be renumbered accordingly; and"),
    ("LIST_ITEM",
     "(c) grant such other and further relief as the Court deems just and proper."),
    ("PARA",
     "13. RESERVATION OF RIGHTS. This Amended Notice is submitted for the limited purposes "
     "stated above. Nothing in it is, or should be construed as, a waiver of any right, "
     "objection, or defense available to Plaintiff. Plaintiff expressly reserves all "
     "objections to this Court's subject-matter jurisdiction, which under 28 U.S.C. 1447(c) "
     "may be raised at any time before final judgment, and takes no position here on the "
     "responsive pleading that Defendant must file under Federal Rule of Civil Procedure "
     "81(c)(2)."),
]

SIGNOFF_NAME = "BRENDAN NGEHSI NEWANFORBI"
SIGNOFF_ROLE = "Plaintiff, In Propria Persona"
SIG_LINE = "___________________________________"

SERVICE_ADDRESSEES = [
    "Vanessa W. Mott, Esq. (SBN 184606)",
    "Alyssa R. Daskas, Esq. (SBN 359379)",
    "MARTENSON, HASBROUCK & SIMON LLP",
    "600 Anton Boulevard, Suite 1250",
    "Costa Mesa, CA 92626",
    "vmott@martensonlaw.com",
    "adaskas@martensonlaw.com",
    "Attorneys for Defendant United Parcel Service, Inc.",
]


def _signature(d, exec_date: str) -> None:
    d.ensure_space(9)
    d.write_line(f"Dated: {exec_date}")
    d.blank_line()
    d.write_line("Respectfully submitted,", right=True, right_margin_offset=20)
    d.blank_line()
    d.draw_signature_image(
        SIGNATURE_PATH, SIGNATURE_NATIVE_PX[0], SIGNATURE_NATIVE_PX[1], SIG_LINE
    )
    d.write_line(SIG_LINE, right=True, right_margin_offset=20)
    d.write_line(SIGNOFF_NAME, right=True, right_margin_offset=20)
    d.write_line(SIGNOFF_ROLE, right=True, right_margin_offset=20)


def _certificate_of_service(d, exec_date: str, mailed_from: str) -> None:
    d.start_new_page()
    d.write_line("CERTIFICATE OF SERVICE", bold=True, center=True)
    d.blank_line()
    d.write_wrapped(
        "I am the Plaintiff in this action and am over the age of eighteen years. On "
        f"{exec_date}, I served the foregoing AMENDED NOTICE REGARDING CAPTION, AND "
        "REQUEST FOR INTRADISTRICT REASSIGNMENT by placing a true and correct copy in a "
        "sealed envelope, with first-class postage fully prepaid, and depositing it with the "
        f"United States Postal Service at {mailed_from}, addressed as follows:",
        first_indent=36,
    )
    d.blank_line()
    for line in SERVICE_ADDRESSEES:
        d.write_line(line, indent=54)
    d.blank_line()
    d.write_wrapped(
        "I declare under penalty of perjury under the laws of the United States of America "
        f"that the foregoing is true and correct. Executed on {exec_date}, at "
        f"{mailed_from}.",
        first_indent=36,
    )
    d.ensure_space(6)
    d.blank_line()
    d.draw_signature_image(
        SIGNATURE_PATH, SIGNATURE_NATIVE_PX[0], SIGNATURE_NATIVE_PX[1], SIG_LINE
    )
    d.write_line(SIG_LINE, right=True, right_margin_offset=20)
    d.write_line(SIGNOFF_NAME, right=True, right_margin_offset=20)
    d.write_line(SIGNOFF_ROLE, right=True, right_margin_offset=20)


def build(out: Path, exec_date: str, mailed_from: str) -> Path:
    if not Path(SIGNATURE_PATH).is_file():
        raise SystemExit(f"Missing universal signature: {SIGNATURE_PATH}")
    out.parent.mkdir(parents=True, exist_ok=True)
    d = PleadingPaper(str(out), doc_title_footer=FOOTER)
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

    d.draw_caption_block(CAPTION_LEFT, CAPTION_RIGHT, caption_size=10,
                         tight_lh=13, boxed=True)
    d.blank_line()

    for kind, text in CONTENT:
        if kind == "HEADER":
            lines = text.split("\n")
            d.ensure_space(len(lines) + 3)
            for line in lines:
                d.write_line(line, bold=True, center=True)
            d.blank_line()
        elif kind == "PARA":
            d.write_wrapped(text, first_indent=36)
            d.blank_line()
        elif kind == "LIST_ITEM":
            d.write_wrapped(text, indent=36, first_indent=0)
            d.blank_line()
        else:
            raise ValueError(f"unknown content kind {kind!r}")

    _signature(d, exec_date)
    _certificate_of_service(d, exec_date, mailed_from)
    d.save()
    return out


def main() -> None:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("out", nargs="?", default=str(DEFAULT_OUT))
    ap.add_argument("--date", default=DEFAULT_EXEC_DATE)
    ap.add_argument("--mailed-from", default=DEFAULT_MAILED_FROM)
    args = ap.parse_args()
    print(f"Generated: {build(Path(args.out).resolve(), args.date, args.mailed_from)}")


if __name__ == "__main__":
    main()
