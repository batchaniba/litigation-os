#!/usr/bin/env python3
"""Matter 20 — Notice of Lodging of the November 1, 2024 CHP dashcam.

Alameda Super. Ct. No. 26CV191136, Dept. 25 (Hon. Jenna M. Whitman).

Department 25's covering clerk authorized lodging video by USB or a cloud
drive (September 4, 2026). Petitioner emailed the Camera 1 Google Drive
link to dept25@alameda.courts.ca.gov (cc DAG Ing) on September 8, 2026.
This paper is the eCourt Notice of Lodging, a separate-page authenticating
declaration, and the portfolio four-sided-border Proof of Service. The
portal will not accept the 2.5 GB file; the link is the lodging.

  python3 internal/scripts/matter20-notice-of-lodging-dashcam.py

FILED_STATUS: False until e-filed and served.
"""
from __future__ import annotations

import os
import sys
from pathlib import Path

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, SCRIPT_DIR)
sys.path.insert(0, os.path.join(SCRIPT_DIR, "lib"))

from pdf_packet import assemble  # noqa: E402
from pleading_paper import (  # noqa: E402
    CONTENT_LEFT,
    COURT_LINE1,
    PleadingPaper,
)
from proof_of_service import ProofOfServiceFields, build_proof_of_service  # noqa: E402
from signature_stamp import SIGNATURE_NATIVE_PX, SIGNATURE_PATH  # noqa: E402

SIGNATURE_IMG = SIGNATURE_PATH
SIG_IMG_W_PX, SIG_IMG_H_PX = SIGNATURE_NATIVE_PX

FILED_STATUS = False

EXEC_DATE = "September 8, 2026"
EXEC_PLACE = "Milpitas, California"
CMC_DATE = "October 28, 2026"
CMC_TIME = "4:00 p.m."

DRIVE_URL = (
    "https://drive.google.com/file/d/1xFrRh4CuyQ4vjQ8-zAKxCDOspuNagI69/view"
)

DOC_TITLE_FOOTER = (
    "NOTICE OF LODGING — CHP DASHCAM (EX. 5 SOURCE) — "
    "NEWANFORBI v. CHP, ET AL."
)
COURT_LINE2 = "COUNTY OF ALAMEDA"
PAPER_TITLE = (
    "NOTICE OF LODGING OF NOVEMBER 1, 2024 CHP DASHCAM "
    "RECORDING (PETITION EXHIBIT 5 SOURCE); DECLARATION OF PETITIONER"
)

REPO_ROOT = os.path.abspath(os.path.join(SCRIPT_DIR, "..", ".."))
MATTER20 = Path(REPO_ROOT) / "internal" / "public" / "documents" / "matter-20"
OUTPUT_PATH = MATTER20 / (
    "Notice of Lodging - Nov 1 2024 CHP Dashcam Exhibit 5 Source (Sep 8 2026).pdf"
)
POS_PATH = MATTER20 / (
    "Proof of Service - Notice of Lodging Nov 1 2024 CHP Dashcam (Sep 8 2026).pdf"
)

SIG_LINE = "___________________________________"


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


def _caption(d: PleadingPaper, right_title_lines: list[tuple[str, bool, bool]]) -> None:
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
    right = [
        ("Case No. 26CV191136", False, False),
        ("", False, False),
        *right_title_lines,
        ("", False, False),
        (f"CMC:  {CMC_DATE}", False, False),
        (f"Time:  {CMC_TIME}", False, False),
        ("Assigned for All Purposes to:", False, False),
        ("Hon. Jenna M. Whitman, Dept. 25", False, False),
        ("", False, False),
        ("Action Filed: May 29, 2026", False, False),
        ("Trial Date:   Not set", False, False),
    ]
    d.draw_caption_block(left, right, caption_size=10, tight_lh=13, boxed=True)
    d.blank_line()


def _sign(d: PleadingPaper, executed_line: str) -> None:
    """Stamp with air above the line so the loops do not hit the date line."""
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
    d.write_line("BRENDAN NGEHSI NEWANFORBI", bold=True, right=True, right_margin_offset=20)
    d.write_line("Petitioner, In Pro Per", right=True, right_margin_offset=20)


def _notice_right() -> list[tuple[str, bool, bool]]:
    return [
        ("NOTICE OF LODGING OF", True, False),
        ("NOVEMBER 1, 2024 CHP", True, False),
        ("DASHCAM RECORDING", True, False),
        ("(PETITION EXHIBIT 5 SOURCE)", True, False),
    ]


def _declaration_right() -> list[tuple[str, bool, bool]]:
    return [
        ("DECLARATION OF PETITIONER", True, False),
        ("ISO NOTICE OF LODGING OF", True, False),
        ("NOVEMBER 1, 2024 CHP", True, False),
        ("DASHCAM RECORDING", True, False),
    ]


def build_notice_and_declaration(path: Path) -> Path:
    path.parent.mkdir(parents=True, exist_ok=True)
    d = PleadingPaper(str(path), doc_title_footer=DOC_TITLE_FOOTER)
    _header(d)
    _caption(d, _notice_right())

    d.write_line("NOTICE OF LODGING", bold=True, center=True)
    d.blank_line()

    d.write_wrapped("TO ALL PARTIES AND THEIR COUNSEL OF RECORD:", first_indent=0)
    d.blank_line()

    d.write_wrapped(
        "PLEASE TAKE NOTICE that Petitioner Brendan Ngehsi Newanforbi, "
        "appearing in propria persona, hereby lodges with Department 25 the "
        "November 1, 2024 California Highway Patrol dashcam recording "
        "identified below. Lodging is by cloud link, as the covering "
        "courtroom clerk for Department 25 authorized on September 4, 2026 "
        "(USB or a cloud drive). Petitioner is not requesting a ruling or a "
        "proposed order."
    )
    d.blank_line()

    d.write_wrapped(
        f"The recording is the source from which the transcript attached to "
        f"the Verified Petition as Exhibit 5 was prepared. It is lodged for "
        f"surviving Count 1 and for the case management conference on "
        f"{CMC_DATE}, at {CMC_TIME}, in Department 25."
    )
    d.blank_line()

    d.write_wrapped("The lodged file is:", first_indent=36)
    d.write_wrapped(
        "Camera 1 — CHP_Cam1.MP4 (approximately 2.5 gigabytes).",
        indent=36,
        first_indent=0,
    )
    d.write_wrapped(
        "CHP Case RJ68845; CAD 241101GG0064; November 1, 2024; "
        "times 00:54:36–01:57:10.",
        indent=36,
        first_indent=0,
    )
    d.write_wrapped(
        f"View link (anyone with the link can view; no Google account "
        f"required): {DRIVE_URL}",
        indent=36,
        first_indent=0,
    )
    d.blank_line()

    d.write_wrapped(
        "The video file is not attached to this e-filing. The eCourt portal "
        "cannot accept a file of this size. That is why Department 25 "
        "authorized a cloud link."
    )
    d.blank_line()

    d.write_wrapped(
        f"On {EXEC_DATE}, Petitioner emailed the same link to "
        "dept25@alameda.courts.ca.gov, with a copy to Deputy Attorney "
        "General Vanessa K. Ing, counsel for Respondents."
    )
    d.blank_line()
    _sign(d, f"Signed on {EXEC_DATE}, at {EXEC_PLACE}.")

    d.start_new_page()
    _header(d)
    _caption(d, _declaration_right())

    d.write_line("DECLARATION OF PETITIONER", bold=True, center=True)
    d.blank_line()
    d.write_wrapped("I, Brendan Ngehsi Newanforbi, declare:", first_indent=0)
    d.blank_line()

    d.write_wrapped(
        "1. I am the Petitioner in this action, appearing in propria persona. "
        "I have personal knowledge of the facts stated in this declaration, "
        "and if called as a witness I could and would testify competently to "
        "them."
    )
    d.blank_line()

    d.write_wrapped(
        "2. The file at the Google Drive link stated in the accompanying "
        "Notice of Lodging is the November 1, 2024 California Highway Patrol "
        "dashcam recording of the encounter in CHP Case RJ68845 / CAD "
        "241101GG0064. The burned-in clock on the recording begins at "
        "00:54:36 and the encounter window pleaded in the Petition runs "
        "through 01:57:10. I have not altered the video."
    )
    d.blank_line()

    d.write_wrapped(
        "3. Petition Exhibit 5 is a transcript prepared from this recording. "
        "I am lodging the recording so the Court has the source file, not "
        "only the transcript."
    )
    d.blank_line()

    d.write_wrapped(
        f"4. On {EXEC_DATE}, I created a view-only sharing link (anyone with "
        "the link can view; no Google account required) and emailed that "
        "link to Department 25 at dept25@alameda.courts.ca.gov, with a copy "
        "to Vanessa.Ing@doj.ca.gov, as the covering courtroom clerk "
        "authorized on September 4, 2026."
    )
    d.blank_line()

    d.write_wrapped(
        "5. I am not requesting a ruling or a proposed order by this lodging."
    )
    d.blank_line()

    d.write_wrapped(
        "I declare under penalty of perjury under the laws of the State of "
        "California that the foregoing is true and correct."
    )
    d.blank_line()
    _sign(d, f"Signed on {EXEC_DATE}, at {EXEC_PLACE}.")
    d.save()
    return path


def lodging_pos_fields() -> ProofOfServiceFields:
    return ProofOfServiceFields(
        plaintiff_line="BRENDAN NGEHSI NEWANFORBI",
        plaintiff_role="Petitioner",
        defendant_lines=[
            "CALIFORNIA HIGHWAY PATROL;",
            "G. SERRATO; and DOES 1-10",
        ],
        defendant_role="Respondents",
        case_number="26CV191136",
        title="PROOF OF SERVICE",
        service_date=EXEC_DATE,
        document_title=PAPER_TITLE,
        mailing_location=EXEC_PLACE,
        recipients=[
            "Vanessa K. Ing, Deputy Attorney General",
            "Vanessa.Ing@doj.ca.gov",
            "Office of the Attorney General",
            "455 Golden Gate Avenue, Suite 11000",
            "San Francisco, CA 94102-7004",
            "Attorneys for Respondents California Highway Patrol and G. Serrato",
        ],
        server_name="Brendan Ngehsi Newanforbi",
        stamp_signature=True,
        court_line=COURT_LINE1,
        district_line=COURT_LINE2,
        by_email=True,
        signature_on_second_page=True,
    )


def build_pos(path: Path) -> Path:
    return build_proof_of_service(path, lodging_pos_fields())


def main() -> None:
    if not os.path.isfile(SIGNATURE_IMG):
        raise SystemExit(f"Missing universal signature: {SIGNATURE_IMG}")
    MATTER20.mkdir(parents=True, exist_ok=True)
    front = Path("/tmp/matter20-lodging-front.pdf")
    build_notice_and_declaration(front)
    build_pos(POS_PATH)
    assemble([front, POS_PATH], OUTPUT_PATH)
    print(f"SUCCESS! Generated: {OUTPUT_PATH}")
    print(f"SUCCESS! Generated: {POS_PATH}")
    if not FILED_STATUS:
        print("NOTE: FILED_STATUS is False -- not yet e-filed/served.")


if __name__ == "__main__":
    main()
