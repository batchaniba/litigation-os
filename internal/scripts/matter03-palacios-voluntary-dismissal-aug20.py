#!/usr/bin/env python3
# ==========================================================
# FILING 3 -- Matter 3 (Newanforbi v. Derrick, 2:26-cv-00004-DJC-JDP)
# NOTICE OF VOLUNTARY DISMISSAL OF DEFENDANT KATIE PALACIOS
# Fed. R. Civ. P. 41(a)(1)(A)(i)
#
# Execution date: August 20, 2026
# FILED_STATUS: False until actually e-filed via CM/ECF.
#
# This is the remaining-defendant dismissal in Matter 3 after the
# July 22, 2026 Rule 41(a)(1)(A)(i) dismissal of Derrick and Noguchi.
# It is not a Matter 5 paper (Newanforbi v. Palacios, San Joaquin, already
# dismissed July 15, 2026).
# ==========================================================
from __future__ import annotations

import sys
from pathlib import Path

SCRIPT_DIR = Path(__file__).resolve().parent
sys.path.insert(0, str(SCRIPT_DIR))
sys.path.insert(0, str(SCRIPT_DIR / "lib"))
from pleading_paper import PleadingPaper  # noqa: E402
from signature_stamp import SIGNATURE_NATIVE_PX, SIGNATURE_PATH  # noqa: E402

FILED_STATUS = False
EXEC_DATE = "August 20, 2026"

ROOT = SCRIPT_DIR.parents[1]
OUT = (
    ROOT
    / "internal/public/documents/matter-03"
    / "Notice of Voluntary Dismissal of Defendant Katie Palacios (Aug 20 2026).pdf"
)

SIG_LINE = "___________________________________"


def build() -> Path:
    if not Path(SIGNATURE_PATH).is_file():
        raise SystemExit(f"Missing universal signature: {SIGNATURE_PATH}")
    OUT.parent.mkdir(parents=True, exist_ok=True)

    d = PleadingPaper(
        str(OUT),
        doc_title_footer=(
            "NOTICE OF VOLUNTARY DISMISSAL -- NEWANFORBI v. DERRICK, ET AL. "
            "(2:26-cv-00004-DJC-JDP)"
        ),
    )
    d.write_attorney_block([
        ("BRENDAN NGEHSI NEWANFORBI", True),
        "Plaintiff, Pro Se",
        "1455 Cat Tail Drive",
        "Stockton, CA 95204",
        "E-mail: bnn.cdl@gmail.com",
    ])

    d.write_line("UNITED STATES DISTRICT COURT", bold=True, center=True)
    d.write_line("FOR THE EASTERN DISTRICT OF CALIFORNIA", bold=True, center=True)
    d.write_line("SACRAMENTO DIVISION", bold=True, center=True)

    left = [
        ("BRENDAN NGEHSI NEWANFORBI,", True, False),
        ("", False, False),
        ("                          Plaintiff,", False, False),
        ("", False, False),
        ("       v.", False, False),
        ("", False, False),
        ("DERRICK, et al.,", False, False),
        ("", False, False),
        ("                          Defendants.", False, False),
    ]
    right = [
        ("Case No.: 2:26-cv-00004-DJC-JDP", True, False),
        ("(PS)", True, False),
        ("", False, False),
        ("PLAINTIFF'S NOTICE OF", True, False),
        ("VOLUNTARY DISMISSAL OF", True, False),
        ("DEFENDANT KATIE PALACIOS", True, False),
        ("PURSUANT TO FED. R. CIV. P.", True, False),
        ("41(a)(1)(A)(i)", True, False),
        ("", False, False),
        ("Judge: Hon. Daniel J. Calabretta", False, False),
        ("Mag. Judge: Hon. Jeremy D.", False, False),
        ("Peterson", False, False),
        ("Action Filed: January 5, 2026", False, False),
        ("FAC Filed: January 12, 2026", False, False),
    ]
    d.draw_caption_block(left, right, caption_size=10, tight_lh=11, boxed=True)
    d.blank_line()

    d.write_line("PLAINTIFF'S NOTICE OF VOLUNTARY DISMISSAL", bold=True, center=True)
    d.write_line("OF DEFENDANT KATIE PALACIOS PURSUANT TO", bold=True, center=True)
    d.write_line("FED. R. CIV. P. 41(a)(1)(A)(i)", bold=True, center=True)
    d.blank_line()
    d.write_wrapped(
        "TO THE CLERK OF THE COURT, ALL PARTIES, AND THEIR COUNSEL OF RECORD:",
        bold=True,
        first_indent=0,
    )
    d.blank_line()
    d.write_wrapped(
        "PLEASE TAKE NOTICE that, pursuant to Federal Rule of Civil Procedure "
        "41(a)(1)(A)(i), Plaintiff BRENDAN NGEHSI NEWANFORBI, appearing pro se, "
        "hereby voluntarily dismisses all claims against Defendant KATIE "
        "PALACIOS in the above-captioned action, without prejudice."
    )
    d.blank_line()
    d.write_wrapped(
        "In light of the Court's August 13, 2026 Order to Show Cause (ECF No. "
        "33), Plaintiff has elected not to continue prosecution of this action "
        "and instead voluntarily dismisses the remaining defendant."
    )
    d.blank_line()
    d.write_wrapped(
        "Plaintiff is entitled to dismiss claims against Defendant Palacios as "
        "a matter of right because Defendant Palacios has not served either an "
        "answer or a motion for summary judgment. (Fed. R. Civ. P. "
        "41(a)(1)(A)(i).) The Clerk of Court is respectfully requested to "
        "terminate Defendant Katie Palacios from this action."
    )
    d.blank_line()
    d.write_wrapped(
        "Plaintiff respectfully thanks the Court for its careful attention to "
        "this matter and for the opportunity to be heard."
    )

    d.ensure_space(8)
    d.blank_line()
    d.write_line(f"Dated: {EXEC_DATE}")
    d.write_line("Respectfully submitted,", italic=True)
    d.blank_line()
    d.draw_signature_image(
        SIGNATURE_PATH, SIGNATURE_NATIVE_PX[0], SIGNATURE_NATIVE_PX[1], SIG_LINE
    )
    d.write_line(SIG_LINE, right=True, right_margin_offset=20)
    d.write_line("BRENDAN NGEHSI NEWANFORBI", bold=True, right=True, right_margin_offset=20)
    d.write_line("Plaintiff, Pro Se", right=True, right_margin_offset=20)
    d.write_line("1455 Cat Tail Drive", right=True, right_margin_offset=20)
    d.write_line("Stockton, CA 95204", right=True, right_margin_offset=20)
    d.write_line("E-mail: bnn.cdl@gmail.com", right=True, right_margin_offset=20)
    d.save()
    return OUT


if __name__ == "__main__":
    path = build()
    print(f"Wrote {path}")
    print(f"FILED_STATUS={FILED_STATUS}; execution date={EXEC_DATE}")
