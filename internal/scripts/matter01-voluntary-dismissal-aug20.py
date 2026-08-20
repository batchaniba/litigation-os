#!/usr/bin/env python3
# ==========================================================
# FILING 4 -- Matter 1 (Newanforbi v. CHP et al., 2:25-cv-01460-DC-CSK)
# NOTICE OF VOLUNTARY DISMISSAL WITHOUT PREJUDICE
# Fed. R. Civ. P. 41(a)(1)(A)(i)
#
# Execution / service date: August 20, 2026
# FILED_STATUS: False until actually e-filed via CM/ECF.
#
# Redates the Aug. 11, 2026 draft (unsigned; portfolio recorded an
# Aug. 15 e-filing of that draft -- confirm the E.D. Cal. docket before
# treating this Aug. 20 paper as a second filing). Signed with the
# portfolio universal signature on the notice and the certificate of
# service. Claims against Meza-Gonzalez and Melano are live in Matter 32
# (N.D. Cal. No. 3:26-cv-08271-PHK, docketed Aug. 10, 2026).
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
    / "internal/public/documents/matter-32/from-01"
    / "Notice of Voluntary Dismissal Without Prejudice (Aug 20 2026).pdf"
)

SIG_LINE = "___________________________________"
FOOTER = (
    "NOTICE OF VOLUNTARY DISMISSAL W/O PREJUDICE -- "
    "NEWANFORBI v. STATE OF CALIFORNIA ET AL. (2:25-cv-01460-DC-CSK)"
)


def _sign(d: PleadingPaper, extra_lines: list[str] | None = None) -> None:
    d.ensure_space(8 if extra_lines else 6)
    d.write_line(f"Dated: {EXEC_DATE}")
    d.write_line("Respectfully submitted,", italic=True)
    d.blank_line()
    d.draw_signature_image(
        SIGNATURE_PATH, SIGNATURE_NATIVE_PX[0], SIGNATURE_NATIVE_PX[1], SIG_LINE
    )
    d.write_line(SIG_LINE, right=True, right_margin_offset=20)
    d.write_line("BRENDAN NGEHSI NEWANFORBI", bold=True, right=True, right_margin_offset=20)
    d.write_line("Plaintiff, In Pro Per", right=True, right_margin_offset=20)
    for line in extra_lines or []:
        d.write_line(line, right=True, right_margin_offset=20)


def _sign_cos(d: PleadingPaper) -> None:
    d.ensure_space(6)
    d.write_line(f"Executed on {EXEC_DATE}, at Milpitas, California.")
    d.blank_line()
    d.draw_signature_image(
        SIGNATURE_PATH, SIGNATURE_NATIVE_PX[0], SIGNATURE_NATIVE_PX[1], SIG_LINE
    )
    d.write_line(SIG_LINE, right=True, right_margin_offset=20)
    d.write_line("BRENDAN NGEHSI NEWANFORBI", bold=True, right=True, right_margin_offset=20)
    d.write_line("Plaintiff, In Pro Per", right=True, right_margin_offset=20)


def build() -> Path:
    if not Path(SIGNATURE_PATH).is_file():
        raise SystemExit(f"Missing universal signature: {SIGNATURE_PATH}")
    OUT.parent.mkdir(parents=True, exist_ok=True)

    d = PleadingPaper(str(OUT), doc_title_footer=FOOTER)
    d.write_line("BRENDAN NGEHSI NEWANFORBI", bold=True)
    d.write_line("Plaintiff, In Pro Per")
    d.write_line("1455 Cat Tail Drive, Stockton, CA 95204")
    d.write_line("Tel: (209) 801-4442  E-mail: bnn.cdl@gmail.com")

    d.write_line("UNITED STATES DISTRICT COURT", bold=True, center=True)
    d.write_line("FOR THE EASTERN DISTRICT OF CALIFORNIA", bold=True, center=True)

    left = [
        ("BRENDAN NGEHSI NEWANFORBI,", True, False),
        ("", False, False),
        ("                          Plaintiff,", False, False),
        ("", False, False),
        ("       v.", False, False),
        ("", False, False),
        ("STATE OF CALIFORNIA; CALIFORNIA", False, False),
        ("HIGHWAY PATROL; OFFICER SANTIAGO", False, False),
        ("MEZA-GONZALEZ (#023295); OFFICER", False, False),
        ("MELANO (#023054),", False, False),
        ("", False, False),
        ("                          Defendants.", False, False),
    ]
    right = [
        ("Case No. 2:25-cv-01460-DC-CSK", True, False),
        ("", False, False),
        ("NOTICE OF VOLUNTARY", True, False),
        ("DISMISSAL WITHOUT PREJUDICE", True, False),
        ("[Fed. R. Civ. P. 41(a)(1)(A)(i)]", False, False),
        ("", False, False),
        ("Judge: Hon. Dena M. Coggins", False, False),
        ("Mag. Judge: Hon. Chi Soo Kim", False, False),
        ("", False, False),
        ("Complaint Filed: May 27, 2025", False, False),
    ]
    d.draw_caption_block(left, right, caption_size=10, tight_lh=11, boxed=True)
    d.blank_line()

    d.write_wrapped(
        "TO THE CLERK OF THE COURT, ALL PARTIES, AND THEIR COUNSEL OF RECORD:",
        bold=True,
        first_indent=0,
    )
    d.blank_line()
    d.write_wrapped(
        "PLEASE TAKE NOTICE that, pursuant to Rule 41(a)(1)(A)(i) of the Federal "
        "Rules of Civil Procedure, Plaintiff BRENDAN NGEHSI NEWANFORBI, appearing "
        "in propria persona, hereby voluntarily dismisses the above-captioned "
        "action in its entirety, without prejudice, as to all Defendants, "
        "including Defendants STATE OF CALIFORNIA; CALIFORNIA HIGHWAY PATROL; "
        "OFFICER SANTIAGO MEZA-GONZALEZ (#023295); and OFFICER MELANO (#023054)."
    )
    d.blank_line()
    d.write_wrapped(
        "Plaintiff is entitled to dismiss this action as a matter of right "
        "because no Defendant has served either an answer or a motion for "
        "summary judgment. (Fed. R. Civ. P. 41(a)(1)(A)(i).) The only "
        "dispositive motion served by any Defendant in this action is "
        "Defendants' Motion to Dismiss under Rule 12(b)(6) (filed December 10, "
        "2025), which is neither an answer nor a motion for summary judgment "
        "within the meaning of Rule 41(a)(1)(A)(i). (See <<i:Hamilton v. "
        "Shearson-Lehman American Express, Inc.>>, 813 F.2d 1532, 1534-35 "
        "(9th Cir. 1987) [right to dismiss under Rule 41(a)(1) is absolute "
        "until the defendant serves an answer or motion for summary judgment]; "
        "<<i:Concha v. London>>, 62 F.3d 1493, 1506 (9th Cir. 1995) [Rule "
        "12(b)(6) motion does not terminate the plaintiff's absolute right to "
        "dismiss under Rule 41(a)(1)].) The Magistrate Judge's April 20, 2026 "
        "Findings and Recommendations recommending dismissal, Plaintiff's "
        "April 21, 2026 Objections thereto, and Plaintiff's July 7, 2026 "
        "Notice of Supplemental Authority likewise do not constitute an answer "
        "or a motion for summary judgment."
    )
    d.blank_line()
    d.write_wrapped(
        "Plaintiff has refiled the claims against Officers Meza-Gonzalez and "
        "Melano in the United States District Court for the Northern District "
        "of California, <<i:Nforbi v. Meza-Gonzalez et al.>>, No. "
        "3:26-cv-08271-PHK (docketed August 10, 2026)."
    )
    d.blank_line()
    d.write_wrapped(
        "Because this is the first voluntary dismissal by Plaintiff of any "
        "action based on or including the claims asserted in this action, the "
        "dismissal is <<b:without prejudice>> and does not operate as an "
        "adjudication on the merits. (Fed. R. Civ. P. 41(a)(1)(B).) No court "
        "order is required to effect this dismissal. (See <<i:Commercial Space "
        "Mgmt. Co. v. Boeing Co.>>, 193 F.3d 1074, 1077-78 (9th Cir. 1999) "
        "[Rule 41(a)(1) notice of dismissal is self-executing and terminates "
        "the action automatically upon filing].) The Clerk of the Court is "
        "respectfully requested to close the file. Each party shall bear its "
        "own costs and attorneys' fees, if any."
    )

    _sign(
        d,
        extra_lines=[
            "1455 Cat Tail Drive, Stockton, CA 95204",
            "(209) 801-4442  bnn.cdl@gmail.com",
        ],
    )

    d.start_new_page()
    d.write_line("CERTIFICATE OF SERVICE", bold=True, center=True, underline=True)
    d.blank_line()
    d.write_wrapped(
        f"I, BRENDAN NGEHSI NEWANFORBI, declare under penalty of perjury under "
        f"the laws of the United States of America that on {EXEC_DATE}, I "
        f"caused a true and correct copy of the foregoing <<b:NOTICE OF "
        f"VOLUNTARY DISMISSAL WITHOUT PREJUDICE>> to be filed with the Clerk "
        f"of the Court through the Court's CM/ECF system, which will provide "
        f"electronic notice to all counsel of record registered through "
        f"CM/ECF, and, to the extent required, to be served by United States "
        f"first-class mail, postage prepaid, and/or by electronic mail, upon "
        f"the following:",
        first_indent=0,
    )
    d.blank_line()
    d.write_line("Counsel for Defendants:", bold=True)
    d.write_line("Haiyang A. Li, Deputy Attorney General")
    d.write_line("Office of the Attorney General / Department of Justice")
    d.write_line("300 South Spring Street, Suite 1702, Los Angeles, CA 90013")
    d.write_line("Haiyang.Li@doj.ca.gov")
    d.write_line("cc: Adriana Zagal, Legal Secretary -- Adriana.Zagal@doj.ca.gov")
    d.blank_line()
    _sign_cos(d)
    d.save()
    return OUT


if __name__ == "__main__":
    path = build()
    print(f"Wrote {path}")
    print(f"FILED_STATUS={FILED_STATUS}; execution date={EXEC_DATE}")
