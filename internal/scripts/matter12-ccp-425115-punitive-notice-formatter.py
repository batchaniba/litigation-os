# ==========================================================
# NGWA NFORBI v. DIAMOND TRUCK SALES, INC. ET AL.
# (STK-CV-UF-2026-0001094)
# NOTICE OF AMOUNT OF PUNITIVE DAMAGES SOUGHT
# (Code Civ. Proc. § 425.115)
#
# One notice per defendant (Diamond / Alpine). Serve before default
# is taken if punitive damages will be requested in the default judgment.
# ==========================================================
import os
import sys

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(SCRIPT_DIR, "lib"))
from pleading_paper import (  # noqa: E402
    PleadingPaper,
    CONTENT_LEFT,
    COURT_LINE1,
)

SIGNATURE_IMG = os.path.join(SCRIPT_DIR, "assets", "newanforbi-pen-signature.png")
SIG_IMG_W_PX, SIG_IMG_H_PX = 369, 101

REPO_ROOT = os.path.abspath(os.path.join(SCRIPT_DIR, "..", ".."))
OUT_DIR = os.path.join(REPO_ROOT, "internal", "public", "documents", "matter-12")

COURT_LINE2 = "COUNTY OF SAN JOAQUIN"
CASE_NO = "STK-CV-UF-2026-0001094"
EXEC_DATE = "August 3, 2026"
PUNITIVE_AMOUNT = "$25,000.00"
PLAINTIFF = "Brendan Ngwa Nforbi"

DEFENDANTS = [
    {
        "short": "Diamond",
        "full": "DIAMOND TRUCK SALES, INC., a California corporation",
        "filename": (
            "1094 Notice of Amount of Punitive Damages Sought "
            "(CCP 425.115) - Diamond Truck Sales (Aug 3 2026).pdf"
        ),
        "footer": (
            "NOTICE OF PUNITIVE DAMAGES (CCP § 425.115) — "
            "NGWA NFORBI v. DIAMOND TRUCK SALES, ET AL."
        ),
    },
    {
        "short": "Alpine",
        "full": (
            "ALPINE TRUCK SALES, INC., a California corporation "
            "(sued individually and as the successor in interest, "
            "mere continuation, and/or alter ego of Diamond Truck Sales, Inc.)"
        ),
        "filename": (
            "1094 Notice of Amount of Punitive Damages Sought "
            "(CCP 425.115) - Alpine Truck Sales (Aug 3 2026).pdf"
        ),
        "footer": (
            "NOTICE OF PUNITIVE DAMAGES (CCP § 425.115) — "
            "NGWA NFORBI v. ALPINE TRUCK SALES, ET AL."
        ),
    },
]


def build_notice(defendant: dict) -> str:
    out_path = os.path.join(OUT_DIR, defendant["filename"])
    d = PleadingPaper(out_path, doc_title_footer=defendant["footer"])
    c = d.c

    # Attorney / party block
    atty_y = d._line_y(0)
    atty_lh = 15
    atty_lines = [
        ("BRENDAN NGWA NFORBI", "Times-Bold", 12),
        ("Plaintiff In Pro Per", "Times-Roman", 12),
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

    left = [
        ("BRENDAN NGWA NFORBI,", True, False),
        ("", False, False),
        ("                          Plaintiff,", False, False),
        ("", False, False),
        ("       v.", False, False),
        ("", False, False),
        ("DIAMOND TRUCK SALES, INC.,", True, False),
        ("a California corporation;", True, False),
        ("ALPINE TRUCK SALES, INC.,", True, False),
        ("a California corporation; and", True, False),
        ("DOES 1 through 20, inclusive,", True, False),
        ("", False, False),
        ("                          Defendants.", False, False),
    ]
    right = [
        (f"Case No. {CASE_NO}", False, False),
        ("", False, False),
        ("NOTICE OF AMOUNT OF", True, False),
        ("PUNITIVE DAMAGES SOUGHT", True, False),
        ("", False, False),
        ("(Code Civ. Proc. § 425.115;", False, False),
        ("Civ. Code § 3294)", False, False),
        ("", False, False),
        ("TO BE SERVED ON:", False, False),
        (f"{defendant['short']} Truck Sales, Inc.", True, False),
        ("", False, False),
        ("Assigned to:", False, False),
        ("Hon. Robert T. Waters, Dept. 11B", False, False),
        ("Prove-Up / CMC: August 12, 2026", False, False),
        ("Action Filed: February 13, 2026", False, False),
    ]
    d.draw_caption_block(left, right, caption_size=10, tight_lh=13, boxed=True)
    d.blank_line()

    d.write_line("NOTICE OF AMOUNT OF PUNITIVE DAMAGES SOUGHT", bold=True, center=True)
    d.write_line("(Code of Civil Procedure section 425.115)", bold=True, center=True)
    d.blank_line()

    d.write_wrapped(
        f"TO DEFENDANT {defendant['full']}:",
        first_indent=0,
    )
    d.blank_line()

    # Statutory notice text (CCP § 425.115(b))
    d.write_line("NOTICE TO DEFENDANT:", bold=True, center=True)
    d.blank_line()
    d.write_wrapped(
        f"{PLAINTIFF} reserves the right to seek {PUNITIVE_AMOUNT} in punitive "
        f"damages when {PLAINTIFF} seeks a judgment in the suit filed against you.",
        first_indent=36,
    )
    d.blank_line()

    d.write_wrapped(
        "This Notice is served pursuant to Code of Civil Procedure section 425.115 "
        "to preserve Plaintiff's right to seek punitive damages under Civil Code "
        "section 3294 in connection with any default judgment, court judgment after "
        "default, or other judgment in this action. The amount stated above is the "
        "amount of punitive damages Plaintiff presently seeks against you; if you "
        "appear in the action, Plaintiff shall not be limited to that amount. "
        "(Code Civ. Proc., § 425.115, subds. (b)-(c).)",
        first_indent=36,
    )
    d.blank_line()

    d.write_wrapped(
        "This Notice is directed to you alone. A separate Notice under section "
        "425.115 is being served on each named defendant against whom Plaintiff "
        "seeks punitive damages.",
        first_indent=36,
    )
    d.blank_line()

    d.write_wrapped(
        "PLEASE TAKE FURTHER NOTICE that a Case Management Conference / default "
        "prove-up hearing in this action is set for August 12, 2026, at 8:30 a.m., "
        "in Department 11B of the Superior Court of California, County of San "
        "Joaquin, before the Honorable Robert T. Waters.",
        first_indent=36,
    )
    d.blank_line()
    d.blank_line()

    d.write_line(f"Dated: {EXEC_DATE}", bold=False)
    d.blank_line()
    d.write_line("Respectfully submitted,", right=True, right_margin_offset=20)
    d.blank_line()

    sig_line = "___________________________________"
    if os.path.isfile(SIGNATURE_IMG):
        d.draw_signature_image(
            SIGNATURE_IMG, SIG_IMG_W_PX, SIG_IMG_H_PX, sig_line
        )
    d.write_line(sig_line, right=True, right_margin_offset=20)
    d.write_line("BRENDAN NGWA NFORBI", right=True, right_margin_offset=20)
    d.write_line("Plaintiff, In Pro Per", right=True, right_margin_offset=20)

    d.save()
    print(f"Generated: {out_path}")
    return out_path


def main():
    os.makedirs(OUT_DIR, exist_ok=True)
    paths = [build_notice(d) for d in DEFENDANTS]
    print(f"Done — {len(paths)} notices (execution date {EXEC_DATE}).")
    print("Serve each notice on the named defendant before default is taken;")
    print("file proof of service. Plaintiff cannot serve these papers personally.")


if __name__ == "__main__":
    main()
