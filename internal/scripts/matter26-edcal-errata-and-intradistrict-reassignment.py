#!/usr/bin/env python3
"""Matter 26 — Notice of Errata Correcting Misnomer and Request for
Intradistrict Reassignment to the Sacramento Division.

Newanforbi v. United Parcel Service, Inc., USDC E.D. Cal. No. 1:26-at-03195
(removed Aug. 20, 2026 from San Joaquin Sup. Ct. No. STK-CV-UWT-2026-0009113).

Two corrections, both cheap and both better made before a judge is assigned:

  1. Defendant's Notice of Removal captions Plaintiff "BRENDAN NGWANFORBI"
     and repeats the misspelling at paragraph 4, while its own declaration
     and Rule 7.1 statement caption the action correctly. The Rule 7.1
     statement then recites the misspelling as an "also known as." Plaintiff appears
     in this action as BRENDAN NGEHSI NEWANFORBI only; the notice claims no other
     name variant.
  2. The removal was filed under a "1:" number -- the Fresno Division. San
     Joaquin County is a Sacramento Division county under E.D. Cal. L.R.
     120(d), and 28 U.S.C. 1441(a) allows removal only to the division
     embracing the place where the state action was pending.

Rendered on the shared California pleading-paper engine and signed with the
portfolio universal signature.

    python3 internal/scripts/matter26-edcal-errata-and-intradistrict-reassignment.py \
        [--date "August 21, 2026"] [OUT_PDF]
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
    / "Notice of Errata and Request for Intradistrict Reassignment (E.D. Cal. 1-26-at-03195) (Aug 21 2026).pdf"
)

DEFAULT_EXEC_DATE = "August 21, 2026"
FOOTER = (
    "PLAINTIFF'S NOTICE OF ERRATA AND REQUEST FOR INTRADISTRICT REASSIGNMENT "
    "-- NEWANFORBI v. UNITED PARCEL SERVICE, INC."
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
    ("PLAINTIFF'S NOTICE OF ERRATA", True, False),
    ("CORRECTING MISNOMER, AND", True, False),
    ("REQUEST FOR INTRADISTRICT", True, False),
    ("REASSIGNMENT TO THE", True, False),
    ("SACRAMENTO DIVISION", True, False),
    ("", False, False),
    ("(E.D. Cal. L.R. 120(d), (f);", False, False),
    ("28 U.S.C. 1441(a))", False, False),
    ("", False, False),
    ("Removed: August 20, 2026 from the", False, False),
    ("Superior Court of the State of", False, False),
    ("California for the County of San", False, False),
    ("Joaquin, Case No. STK-CV-UWT-", False, False),
    ("2026-0009113", False, False),
    ("", False, False),
    ("[No hearing requested]", False, True),
]

CONTENT = [
    ("PARA",
     "TO THE HONORABLE COURT, AND TO DEFENDANT UNITED PARCEL SERVICE, INC. AND ITS "
     "ATTORNEYS OF RECORD:"),
    ("PARA",
     "Plaintiff BRENDAN NGEHSI NEWANFORBI, appearing in propria persona, respectfully "
     "submits this notice for two limited purposes: to correct the spelling of his name "
     "on the caption of this removed action, and to request that the action be reassigned "
     "to the Sacramento Division of this Court, which is the division that embraces the "
     "county in which the action was pending. Both corrections are administrative, neither "
     "requires a hearing, and both are better made now, before a district judge or "
     "magistrate judge is assigned and before any scheduling order issues."),

    ("HEADER", "I.\nTHE CAPTION MISSTATES PLAINTIFF'S NAME"),
    ("PARA",
     "1. Plaintiff's true and correct name is BRENDAN NGEHSI NEWANFORBI. That is the name "
     "under which this action was filed in the Superior Court of the State of California "
     "for the County of San Joaquin on July 15, 2026, Case No. STK-CV-UWT-2026-0009113, and "
     "it is the name that appears on the Summons, on the Complaint, and on every paper "
     "served on Defendant in that action."),
    ("PARA",
     "2. Defendant's Notice of Removal spells Plaintiff's surname \"NGWANFORBI\" in its "
     "caption and repeats that spelling at paragraph 4. The same removal package spells the "
     "name correctly elsewhere: both the Declaration of Ashley Felsing (Doc. 1-2) and the "
     "Notice of Interested Parties and Corporate Disclosure Statement (Doc. 1-3) caption "
     "this action \"BRENDAN NGEHSI NEWANFORBI.\""),
    ("PARA",
     "3. Paragraph 5(a) of the Notice of Interested Parties goes further and describes "
     "Plaintiff as \"Brendan Ngehsi Newanforbi, also known as Brendan Ngwanforbi.\" That is "
     "not correct. \"Ngwanforbi\" is a typographical error, not an alias. Plaintiff has not "
     "appeared in this action, or in the state-court action from which it was removed, under "
     "any name other than BRENDAN NGEHSI NEWANFORBI, and respectfully asks that the docket "
     "in this Court not carry an alias that does not exist."),
    ("PARA",
     "4. On removal, this Court takes the action as it stood in the state court, and the "
     "caption is the caption of the state-court action. The docket in this Court should "
     "therefore identify Plaintiff as BRENDAN NGEHSI NEWANFORBI. Plaintiff raises the point "
     "now so that the misspelling does not carry forward into this Court's orders, its "
     "records, and the public docket, and so that filings in this action can be matched to "
     "the state-court record from which they came."),

    ("HEADER", "II.\nTHIS ACTION BELONGS IN THE SACRAMENTO DIVISION"),
    ("PARA",
     "5. Defendant removed this action on August 20, 2026. The Notice of Removal was filed "
     "under Case No. 1:26-at-03195. The \"1:\" prefix designates the Fresno Division of this "
     "Court."),
    ("PARA",
     "6. The action arose in, and was pending in, San Joaquin County. A defendant may remove "
     "only to \"the district court of the United States for the district and division "
     "embracing the place where such action is pending.\" 28 U.S.C. 1441(a)."),
    ("PARA",
     "7. Under this Court's Local Rule 120(d), civil actions arising in San Joaquin County "
     "are to be commenced in the United States District Court sitting in Sacramento. San "
     "Joaquin County is not among the counties assigned to the Fresno Division. The division "
     "embracing the place where this action was pending is therefore Sacramento."),
    ("PARA",
     "8. Defendant does not appear to contend otherwise. Paragraph 37 of the Notice of "
     "Removal states that \"Plaintiff's Complaint was filed in the Superior Court of the "
     "County of San Joaquin\" and that \"This Court is part of the division in which the "
     "Superior Court action is pending,\" citing 28 U.S.C. 84(b) and 1446(a). That is the "
     "correct standard. Applying it to San Joaquin County yields the Sacramento Division. "
     "This request asks for nothing more than the assignment Defendant's own papers describe."),
    ("PARA",
     "9. Local Rule 120(f) provides for transfer where an action has not been commenced in "
     "the proper court in accordance with Rule 120, on the motion of any party, on "
     "stipulation, or for other good cause. Good cause is plain here and the correction "
     "costs the Court and the parties almost nothing: no district judge or magistrate judge "
     "has been assigned, no scheduling order has issued, no motion has been noticed, and "
     "nothing has been briefed. To the extent the Court prefers that this request be "
     "presented as a noticed motion or by stipulation, Plaintiff will promptly file one, and "
     "will first ask Defendant whether it will stipulate."),
    ("PARA",
     "10. Reassignment also serves the convenience of the parties and of any witnesses. "
     "Plaintiff resides in Stockton, in San Joaquin County -- a fact on which Defendant "
     "itself relies to establish diversity of citizenship. See Notice of Removal, paragraphs "
     "15-16; Felsing Decl., paragraph 6. The employment application at issue, the "
     "adverse-action correspondence, and the entire state-court record originate in or "
     "around San Joaquin County. Sacramento is roughly fifty miles from Stockton; Fresno is "
     "roughly one hundred thirty."),

    ("HEADER", "III.\nRELIEF REQUESTED"),
    ("PARA", "11. Plaintiff respectfully requests that the Court:"),
    ("LIST_ITEM",
     "(a) direct the Clerk of Court to correct the caption of this action so that Plaintiff "
     "is named as BRENDAN NGEHSI NEWANFORBI;"),
    ("LIST_ITEM",
     "(b) reassign this action to the Sacramento Division of this Court under Local Rule "
     "120(f), and direct that it be renumbered accordingly; and"),
    ("LIST_ITEM",
     "(c) grant such other and further relief as the Court deems just and proper."),
    ("PARA",
     "12. RESERVATION OF RIGHTS. This notice is submitted for the two limited purposes "
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


def _certificate_of_service(d, exec_date: str) -> None:
    d.start_new_page()
    d.write_line("CERTIFICATE OF SERVICE", bold=True, center=True)
    d.blank_line()
    d.write_wrapped(
        "I am the Plaintiff in this action and am over the age of eighteen years. My address "
        "is 1455 Cat Tail Drive, Stockton, California 95204. On "
        f"{exec_date}, I served the foregoing NOTICE OF ERRATA AND REQUEST FOR "
        "INTRADISTRICT REASSIGNMENT by placing a true and correct copy in a sealed envelope, "
        "with first-class postage fully prepaid, and depositing it with the United States "
        "Postal Service at Stockton, California, addressed as follows:",
        first_indent=36,
    )
    d.blank_line()
    for line in SERVICE_ADDRESSEES:
        d.write_line(line, indent=54)
    d.blank_line()
    d.write_wrapped(
        "I declare under penalty of perjury under the laws of the United States of America "
        f"that the foregoing is true and correct. Executed on {exec_date}, at Stockton, "
        "California.",
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


def build(out: Path, exec_date: str) -> Path:
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
    _certificate_of_service(d, exec_date)
    d.save()
    return out


def main() -> None:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("out", nargs="?", default=str(DEFAULT_OUT))
    ap.add_argument("--date", default=DEFAULT_EXEC_DATE,
                    help="Execution / service date printed on the filing")
    args = ap.parse_args()
    path = build(Path(args.out).resolve(), args.date)
    print(f"Generated: {path}")


if __name__ == "__main__":
    main()
