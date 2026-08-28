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
# taken, and file proof of service.
#
# AMOUNTS (revised Aug. 7, 2026). The original Aug. 4, 2026 batch
# carried a flat $25,000.00 placeholder copied from Matter 12
# (Diamond/Alpine) — a ~$53.7K fraud case against a small dealership,
# with no analytical relationship to these defendants. Two problems
# with that figure drove this revision:
#
#   1. In these four matters the Pen. Code § 290.46(j)(4)(A) remedy is
#      itself "actual damages or $25,000, whichever is greater" — a
#      COMPENSATORY figure. Noticing punitive damages at the identical
#      $25,000 puts the same number on both sides of the ledger and
#      invites a prove-up court to read the punitive request as
#      duplicative of the statutory penalty.
#   2. Section 425.115 caps punitive damages recoverable ON DEFAULT and
#      cannot be raised once default is entered, so an under-set figure
#      is a permanent ceiling in the only scenario the document exists
#      for. It imposes no cap at all if the defendant appears.
#
# Each amount below is now set per defendant, anchored to that matter's
# modeled compensatory exposure (internal/src/data/damages.js) at a
# ratio inside the single-digit due-process bound of State Farm v.
# Campbell (2003) 538 U.S. 408 and Simon v. San Paolo U.S. Holding Co.
# (2005) 35 Cal.4th 1159.
#
# AMENDED vs. ORIGINAL. Matters 25, 26, and 27 were already served with
# (or had already routed to the Sheriff) the Aug. 4, 2026 $25,000
# notice, so those four defendants receive an AMENDED notice that
# expressly supersedes the earlier one. Matter 29 (Amazon / Accurate
# Background) had no notice served, so those two are original notices
# at the revised amount.
#
# An amended statement raising the amount must itself be served before
# default is entered; recovery on default is limited to the amount
# stated in the statement in effect at that time.
# ==========================================================
import os
import sys

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, SCRIPT_DIR)
sys.path.insert(0, os.path.join(SCRIPT_DIR, "lib"))
from pleading_paper import (  # noqa: E402
    PleadingPaper,
    CONTENT_LEFT,
    COURT_LINE1,
)

from signature_stamp import SIGNATURE_NATIVE_PX, SIGNATURE_PATH  # noqa: E402

SIGNATURE_IMG = SIGNATURE_PATH
SIG_IMG_W_PX, SIG_IMG_H_PX = SIGNATURE_NATIVE_PX

REPO_ROOT = os.path.abspath(os.path.join(SCRIPT_DIR, "..", ".."))
DOCS_ROOT = os.path.join(REPO_ROOT, "internal", "public", "documents")

EXEC_DATE = "August 7, 2026"
PLAINTIFF = "Brendan Ngehsi Newanforbi"

# The superseded first batch — quoted verbatim in each amended notice so the
# record shows exactly which statement is being replaced and by what.
PRIOR_NOTICE_DATE = "August 4, 2026"
PRIOR_AMOUNT = "$25,000.00"

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
        "cmc_line": "CMC: Jan. 14, 2027, 8:45 a.m.",
        "cmc_date": "January 14, 2027, at 8:45 a.m.",
        "dept": "Department 10B",
        "county_full": "County of San Joaquin",
        "filed_line": "Action Filed: July 15, 2026",
        "defendants": [
            {
                "short": "Federal Express",
                "full": "FEDERAL EXPRESS CORPORATION",
                # 3:1 against ~$80K modeled moderate compensatory (Matter 25
                # moderate total ~$95K, less the fee component).
                "amount": "$250,000.00",
                "amended": True,
                "filename": "Amended Notice of Amount of Punitive Damages Sought (CCP 425.115) - Federal Express Corporation (Aug 7 2026).pdf",
                "footer": "AMENDED NOTICE OF PUNITIVE DAMAGES (CCP § 425.115) — NEWANFORBI v. FEDERAL EXPRESS CORPORATION",
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
        "cmc_line": "CMC: Jan. 13, 2027, 8:30 a.m.",
        "cmc_date": "January 13, 2027, at 8:30 a.m.",
        "dept": "Department 11B",
        "county_full": "County of San Joaquin",
        "filed_line": "Action Filed: July 15, 2026",
        "defendants": [
            {
                "short": "UPS",
                "full": "UNITED PARCEL SERVICE, INC.",
                # Held parallel to Matter 25 — near-identical claims, same
                # posture, same modeled range (~$85K moderate).
                "amount": "$250,000.00",
                "amended": True,
                "filename": "Amended Notice of Amount of Punitive Damages Sought (CCP 425.115) - United Parcel Service Inc (Aug 7 2026).pdf",
                "footer": "AMENDED NOTICE OF PUNITIVE DAMAGES (CCP § 425.115) — NEWANFORBI v. UNITED PARCEL SERVICE, INC.",
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
        "cmc_line": "CMC: Dec. 17, 2026, 3:00 p.m.",
        "cmc_date": "December 17, 2026, at 3:00 p.m.",
        "dept": "Department 20",
        "county_full": "County of Alameda",
        "filed_line": "Action Filed: July 20, 2026",
        "defendants": [
            {
                "short": "Randstad",
                "full": "RANDSTAD US, LLC, a Delaware limited liability company",
                # ~2:1 against ~$237K modeled moderate compensatory (back pay
                # $97K + front pay $65K + emotional distress $50K + $25K
                # statutory). The old $25,000 sat below even this matter's
                # CONSERVATIVE modeled punitive figure of $50,000.
                "amount": "$500,000.00",
                "amended": True,
                "filename": "Amended Notice of Amount of Punitive Damages Sought (CCP 425.115) - Randstad US LLC (Aug 7 2026).pdf",
                "footer": "AMENDED NOTICE OF PUNITIVE DAMAGES (CCP § 425.115) — NEWANFORBI v. RANDSTAD US, LLC, ET AL.",
            },
            {
                "short": "RK Logistics",
                "full": "THE RK LOGISTICS GROUP, INC., a California corporation",
                # Same figure as Randstad: each § 425.115 statement is an
                # independent per-defendant cap, and RK configured the
                # screening criteria that produced the adverse decision.
                "amount": "$500,000.00",
                "amended": True,
                "filename": "Amended Notice of Amount of Punitive Damages Sought (CCP 425.115) - RK Logistics Group Inc (Aug 7 2026).pdf",
                "footer": "AMENDED NOTICE OF PUNITIVE DAMAGES (CCP § 425.115) — NEWANFORBI v. RANDSTAD US, LLC, ET AL.",
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
        "cmc_line": "CMC: Jan. 6, 2027, 10:00 a.m.",
        "cmc_date": "January 6, 2027, at 10:00 a.m.",
        "dept": "Department 520 (Hayward Hall of Justice)",
        "county_full": "County of Alameda",
        "filed_line": "Action Filed: July 28, 2026",
        "defendants": [
            {
                "short": "Amazon",
                "full": "AMAZON.COM SERVICES, LLC, a Delaware limited liability company",
                # ~4:1 against ~$60K modeled moderate compensatory. Higher
                # ratio than Matters 25/26 because the compensatory base is
                # small (seasonal part-time position) while the willfulness
                # showing and the defendant's ability to pay are the strongest
                # in this group. NOT amended — no notice was served here.
                "amount": "$250,000.00",
                "amended": False,
                "filename": "Notice of Amount of Punitive Damages Sought (CCP 425.115) - Amazon.com Services LLC (Aug 7 2026).pdf",
                "footer": "NOTICE OF PUNITIVE DAMAGES (CCP § 425.115) — NEWANFORBI v. AMAZON.COM SERVICES, LLC, ET AL.",
            },
            {
                "short": "Accurate Background",
                "full": "ACCURATE BACKGROUND LLC",
                # Set below Amazon's: Accurate Background's exposure here is
                # the narrower consumer-reporting-agency role (ICRAA / FCRA),
                # and its financial condition is materially harder to prove up
                # than a public company's — Adams v. Murakami (1991) 54 Cal.3d
                # 105 puts that burden on Plaintiff.
                "amount": "$100,000.00",
                "amended": False,
                "filename": "Notice of Amount of Punitive Damages Sought (CCP 425.115) - Accurate Background LLC (Aug 7 2026).pdf",
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

    amended = defendant["amended"]
    title_lines = (
        [("AMENDED NOTICE OF AMOUNT", True, False), ("OF PUNITIVE DAMAGES SOUGHT", True, False)]
        if amended
        else [("NOTICE OF AMOUNT OF", True, False), ("PUNITIVE DAMAGES SOUGHT", True, False)]
    )
    right = [
        (f"Case No. {matter['case_no']}", False, False),
        ("", False, False),
        *title_lines,
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

    heading = "NOTICE OF AMOUNT OF PUNITIVE DAMAGES SOUGHT"
    if amended:
        heading = "AMENDED " + heading
    d.write_line(heading, bold=True, center=True)
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
        f"{PLAINTIFF} reserves the right to seek {defendant['amount']} in punitive "
        f"damages when {PLAINTIFF} seeks a judgment in the suit filed against you.",
        first_indent=36,
    )
    d.blank_line()

    notice_word = "Amended Notice" if amended else "Notice"
    d.write_wrapped(
        f"This {notice_word} is served pursuant to Code of Civil Procedure section "
        "425.115 to preserve Plaintiff's right to seek punitive damages under Civil "
        "Code section 3294 in connection with any default judgment, court judgment "
        "after default, or other judgment in this action. The amount stated above is "
        "the amount of punitive damages Plaintiff presently seeks against you; if you "
        "appear in the action, Plaintiff shall not be limited to that amount. "
        "(Code Civ. Proc., § 425.115, subds. (b)-(c).)",
        first_indent=36,
    )
    d.blank_line()

    if amended:
        d.write_wrapped(
            f"This Amended Notice supersedes and replaces in full the Notice of Amount "
            f"of Punitive Damages Sought previously served on you in this action, dated "
            f"{PRIOR_NOTICE_DATE}, which stated the amount of {PRIOR_AMOUNT}. The amount "
            f"stated above — {defendant['amount']} — is the amount of punitive damages "
            f"Plaintiff now seeks against you, and it replaces the amount stated in that "
            f"earlier Notice for all purposes. No default has been entered against you "
            f"as of the date of this Amended Notice, and this Amended Notice is served "
            f"before any default is taken.",
            first_indent=36,
        )
        d.blank_line()

    if len(matter["defendants"]) > 1:
        d.write_wrapped(
            f"This {notice_word} is directed to you alone. A separate {notice_word} "
            "under section 425.115 is being served on each other named defendant "
            "against whom Plaintiff seeks punitive damages in this action.",
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

    # Keep the whole closing block on one page: Dated line, "Respectfully
    # submitted," the signature line, and the two name lines under it. Without
    # this the two-defendant Matter 27 notices broke after the signature line
    # and orphaned "BRENDAN NGEHSI NEWANFORBI / Plaintiff, In Pro Per" onto a
    # page of their own, separated from the line they sign.
    d.ensure_space(8)

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
    amended = sum(len([x for x in m["defendants"] if x["amended"]]) for m in MATTERS)
    print(f"Done — {len(paths)} notices ({amended} amended), execution date {EXEC_DATE}.")
    print("Serve each notice PERSONALLY on its named defendant before default is")
    print("taken (CCP 425.115(f)(2) -- certified mail is unavailable until the")
    print("defendant has made a general appearance); file proof of service.")
    print("Plaintiff cannot serve these papers personally -- use the Sheriff or")
    print("a registered process server, same as the underlying summons/complaint.")
    print("The four AMENDED notices raise the amount above the Aug. 4, 2026")
    print("statement; recovery on default is limited to the amount in the")
    print("statement in effect when default is entered, so each amended notice")
    print("must be served before default is taken to have any effect.")


if __name__ == "__main__":
    main()
