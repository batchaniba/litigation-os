# ==========================================================
# NOTICE OF AMOUNT OF PUNITIVE DAMAGES SOUGHT
# (Code Civ. Proc. § 425.115; Civ. Code § 3294)
#
# Six notices, one per served-but-not-yet-answered defendant across
# four matters that plead Civil Code § 3294 punitive damages:
#   Matter 25 — Newanforbi v. Federal Express Corporation
#   Matter 26 — Newanforbi v. United Parcel Service, Inc.
#   Matter 27 — Newanforbi v. Randstad US, LLC, et al.
#   Matter 29 — Newanforbi v. Amazon.com Services, LLC, et al.
#
# Each defendant below was personally served with the summons and
# complaint but NOT with a § 425.115 statement at that time. Serve
# each notice individually on its named defendant, personally
# (§ 425.115(f)(2) — certified mail is not available until the
# defendant has made a general appearance), before any default is
# taken, and file proof of service. The $25,000 punitive figure is
# a placeholder mirroring the amount used in Matter 12 (Diamond/
# Alpine) — confirm or adjust per defendant before serving.
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
DOCS_ROOT = os.path.join(REPO_ROOT, "internal", "public", "documents")

EXEC_DATE = "August 4, 2026"
PUNITIVE_AMOUNT = "$25,000.00"
PLAINTIFF = "Brendan Ngehsi Newanforbi"

PLAINTIFF_BLOCK = [
    ("BRENDAN NGEHSI NEWANFORBI", "Times-Bold", 12),
    ("Plaintiff In Pro Per", "Times-Roman", 12),
    ("1455 Cat Tail Drive", "Times-Roman", 12),
    ("Stockton, CA 95204", "Times-Roman", 12),
    ("Telephone: (209) 801-4442", "Times-Roman", 12),
    ("E-mail: bnn.cdl@gmail.com", "Times-Roman", 12),
]

MATTERS = [
    {
        "matter": 25,
        "case_no": "STK-CV-UWT-2026-0009118",
        "court_line1": COURT_LINE1,
        "court_line2": "COUNTY OF SAN JOAQUIN",
        "caption_case": "Newanforbi v. Federal Express Corporation",
        "party_block_left": [
            ("BRENDAN NGEHSI NEWANFORBI,", True, False),
            ("", False, False),
            ("                          Plaintiff,", False, False),
            ("", False, False),
            ("       v.", False, False),
            ("", False, False),
            ("FEDERAL EXPRESS CORPORATION;", True, False),
            ("and DOES 1 through 10, inclusive,", True, False),
            ("", False, False),
            ("                          Defendants.", False, False),
        ],
        "judge_line": "Hon. Blanca Banuelos, Dept. 10B",
        "cmc_line": "Case Management Conference: January 14, 2027, 8:45 a.m.",
        "cmc_date": "January 14, 2027, at 8:45 a.m.",
        "dept": "Department 10B",
        "county_full": "County of San Joaquin",
        "filed_line": "Action Filed: July 15, 2026",
        "defendants": [
            {
                "short": "Federal Express",
                "full": "FEDERAL EXPRESS CORPORATION",
                "filename": "Notice of Amount of Punitive Damages Sought (CCP 425.115) - Federal Express Corporation (Aug 4 2026).pdf",
                "footer": "NOTICE OF PUNITIVE DAMAGES (CCP § 425.115) — NEWANFORBI v. FEDERAL EXPRESS CORPORATION",
            },
        ],
    },
    {
        "matter": 26,
        "case_no": "STK-CV-UWT-2026-0009113",
        "court_line1": COURT_LINE1,
        "court_line2": "COUNTY OF SAN JOAQUIN",
        "caption_case": "Newanforbi v. United Parcel Service, Inc.",
        "party_block_left": [
            ("BRENDAN NGEHSI NEWANFORBI,", True, False),
            ("", False, False),
            ("                          Plaintiff,", False, False),
            ("", False, False),
            ("       v.", False, False),
            ("", False, False),
            ("UNITED PARCEL SERVICE, INC.;", True, False),
            ("and DOES 1 through 10, inclusive,", True, False),
            ("", False, False),
            ("                          Defendants.", False, False),
        ],
        "judge_line": "Hon. Robert T. Waters, Dept. 11B",
        "cmc_line": "Case Management Conference: January 13, 2027, 8:30 a.m.",
        "cmc_date": "January 13, 2027, at 8:30 a.m.",
        "dept": "Department 11B",
        "county_full": "County of San Joaquin",
        "filed_line": "Action Filed: July 15, 2026",
        "defendants": [
            {
                "short": "UPS",
                "full": "UNITED PARCEL SERVICE, INC.",
                "filename": "Notice of Amount of Punitive Damages Sought (CCP 425.115) - United Parcel Service Inc (Aug 4 2026).pdf",
                "footer": "NOTICE OF PUNITIVE DAMAGES (CCP § 425.115) — NEWANFORBI v. UNITED PARCEL SERVICE, INC.",
            },
        ],
    },
    {
        "matter": 27,
        "case_no": "26CV199902",
        "court_line1": COURT_LINE1,
        "court_line2": "COUNTY OF ALAMEDA",
        "caption_case": "Newanforbi v. Randstad US, LLC, et al.",
        "party_block_left": [
            ("BRENDAN NGEHSI NEWANFORBI,", True, False),
            ("", False, False),
            ("                          Plaintiff,", False, False),
            ("", False, False),
            ("       v.", False, False),
            ("", False, False),
            ("RANDSTAD US, LLC, a Delaware", True, False),
            ("limited liability company; THE RK", True, False),
            ("LOGISTICS GROUP, INC., a California", True, False),
            ("corporation; and DOES 1 through 20,", True, False),
            ("inclusive,", True, False),
            ("", False, False),
            ("                          Defendants.", False, False),
        ],
        "judge_line": "Hon. Karin Schwartz, Dept. 20",
        "cmc_line": "Case Management Conference: December 17, 2026, 3:00 p.m.",
        "cmc_date": "December 17, 2026, at 3:00 p.m.",
        "dept": "Department 20",
        "county_full": "County of Alameda",
        "filed_line": "Action Filed: July 20, 2026",
        "defendants": [
            {
                "short": "Randstad",
                "full": "RANDSTAD US, LLC, a Delaware limited liability company",
                "filename": "Notice of Amount of Punitive Damages Sought (CCP 425.115) - Randstad US LLC (Aug 4 2026).pdf",
                "footer": "NOTICE OF PUNITIVE DAMAGES (CCP § 425.115) — NEWANFORBI v. RANDSTAD US, LLC, ET AL.",
            },
            {
                "short": "RK Logistics",
                "full": "THE RK LOGISTICS GROUP, INC., a California corporation",
                "filename": "Notice of Amount of Punitive Damages Sought (CCP 425.115) - RK Logistics Group Inc (Aug 4 2026).pdf",
                "footer": "NOTICE OF PUNITIVE DAMAGES (CCP § 425.115) — NEWANFORBI v. RANDSTAD US, LLC, ET AL.",
            },
        ],
    },
    {
        "matter": 29,
        "case_no": "26CV201554",
        "court_line1": COURT_LINE1,
        "court_line2": "COUNTY OF ALAMEDA",
        "caption_case": "Newanforbi v. Amazon.com Services, LLC, et al.",
        "party_block_left": [
            ("BRENDAN NGEHSI NEWANFORBI,", True, False),
            ("", False, False),
            ("                          Plaintiff,", False, False),
            ("", False, False),
            ("       v.", False, False),
            ("", False, False),
            ("AMAZON.COM SERVICES, LLC, a", True, False),
            ("Delaware limited liability company;", True, False),
            ("ACCURATE BACKGROUND LLC; and", True, False),
            ("DOES 1 through 10, inclusive,", True, False),
            ("", False, False),
            ("                          Defendants.", False, False),
        ],
        "judge_line": "Hon. Jamilah Jefferson, Dept. 520",
        "cmc_line": "Case Management Conference: January 6, 2027, 10:00 a.m.",
        "cmc_date": "January 6, 2027, at 10:00 a.m.",
        "dept": "Department 520 (Hayward Hall of Justice)",
        "county_full": "County of Alameda",
        "filed_line": "Action Filed: July 28, 2026",
        "defendants": [
            {
                "short": "Amazon",
                "full": "AMAZON.COM SERVICES, LLC, a Delaware limited liability company",
                "filename": "Notice of Amount of Punitive Damages Sought (CCP 425.115) - Amazon.com Services LLC (Aug 4 2026).pdf",
                "footer": "NOTICE OF PUNITIVE DAMAGES (CCP § 425.115) — NEWANFORBI v. AMAZON.COM SERVICES, LLC, ET AL.",
            },
            {
                "short": "Accurate Background",
                "full": "ACCURATE BACKGROUND LLC",
                "filename": "Notice of Amount of Punitive Damages Sought (CCP 425.115) - Accurate Background LLC (Aug 4 2026).pdf",
                "footer": "NOTICE OF PUNITIVE DAMAGES (CCP § 425.115) — NEWANFORBI v. AMAZON.COM SERVICES, LLC, ET AL.",
            },
        ],
    },
]


def build_notice(matter: dict, defendant: dict) -> str:
    out_dir = os.path.join(DOCS_ROOT, f"matter-{matter['matter']:02d}")
    os.makedirs(out_dir, exist_ok=True)
    out_path = os.path.join(out_dir, defendant["filename"])
    d = PleadingPaper(out_path, doc_title_footer=defendant["footer"])
    c = d.c

    # Attorney / party block
    atty_y = d._line_y(0)
    atty_lh = 15
    for i, (txt, fn, sz) in enumerate(PLAINTIFF_BLOCK):
        c.setFont(fn, sz)
        c.drawString(CONTENT_LEFT, atty_y - i * atty_lh, txt)
    d.current_line = 4
    d.blank_line()

    d.write_line(matter["court_line1"], bold=True, center=True)
    d.write_line(matter["court_line2"], bold=True, center=True)
    d.blank_line()

    right = [
        (f"Case No. {matter['case_no']}", False, False),
        ("", False, False),
        ("NOTICE OF AMOUNT OF", True, False),
        ("PUNITIVE DAMAGES SOUGHT", True, False),
        ("", False, False),
        ("(Code Civ. Proc. § 425.115;", False, False),
        ("Civ. Code § 3294)", False, False),
        ("", False, False),
        ("TO BE SERVED ON:", False, False),
        (defendant["short"], True, False),
        ("", False, False),
        ("Assigned to:", False, False),
        (matter["judge_line"], False, False),
        (matter["cmc_line"], False, False),
        (matter["filed_line"], False, False),
    ]
    d.draw_caption_block(matter["party_block_left"], right, caption_size=10, tight_lh=13, boxed=True)
    d.blank_line()

    d.write_line("NOTICE OF AMOUNT OF PUNITIVE DAMAGES SOUGHT", bold=True, center=True)
    d.write_line("(Code of Civil Procedure section 425.115)", bold=True, center=True)
    d.blank_line()

    d.write_wrapped(
        f"TO DEFENDANT {defendant['full']}:",
        first_indent=0,
    )
    d.blank_line()

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

    if len(matter["defendants"]) > 1:
        d.write_wrapped(
            "This Notice is directed to you alone. A separate Notice under section "
            "425.115 is being served on each other named defendant against whom "
            "Plaintiff seeks punitive damages in this action.",
            first_indent=36,
        )
        d.blank_line()

    d.write_wrapped(
        f"PLEASE TAKE FURTHER NOTICE that a Case Management Conference in this "
        f"action is set for {matter['cmc_date']}, in {matter['dept']} of the "
        f"Superior Court of California, {matter['county_full']}, before the "
        f"{'Honorable ' + matter['judge_line'].split(', Dept')[0].replace('Hon. ', '')}.",
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
    d.write_line("BRENDAN NGEHSI NEWANFORBI", right=True, right_margin_offset=20)
    d.write_line("Plaintiff, In Pro Per", right=True, right_margin_offset=20)

    d.save()
    print(f"Generated: {out_path}")
    return out_path


def main():
    paths = []
    for matter in MATTERS:
        for defendant in matter["defendants"]:
            paths.append(build_notice(matter, defendant))
    print(f"Done — {len(paths)} notices (execution date {EXEC_DATE}).")
    print("Serve each notice PERSONALLY on its named defendant before default is")
    print("taken (CCP 425.115(f)(2) -- certified mail is unavailable until the")
    print("defendant has made a general appearance); file proof of service.")
    print("Plaintiff cannot serve these papers personally -- use the Sheriff or")
    print("a registered process server, same as the underlying summons/complaint.")


if __name__ == "__main__":
    main()
