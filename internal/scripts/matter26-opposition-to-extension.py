#!/usr/bin/env python3
"""Matter 26 -- Opposition to UPS's ECF No. 11 extension motion.

HISTORICAL generator — when they caption consent he did not give, the
locked posture is opposition, not a late signature on their paper. See
.claude/skills/stipulation-defense/SKILL.md. Portfolio-wide.


Newanforbi v. United Parcel Service, Inc., USDC E.D. Cal. No. 2:26-cv-02847-DAD-CKD.
Hearing on the underlying Rule 12(b)(6) motion: October 7, 2026, 10:00 a.m.,
Courtroom 24 (CKD), Magistrate Judge Carolyn K. Delaney (civil L&M by Zoom).
ECF No. 7 / the October 5 Drozd setting were vacated (ECF No. 8). The live
motion is ECF No. 9.

Opposes Dkt. 11 (filed Sep. 4, 2026), captioned a "Consent Motion" although
paragraph 4 admits Plaintiff does not consent. Live reply clock is E.D. Cal.
L.R. 230(d): ten days after Dkt. 10 (filed Aug. 28) is Monday, Sep. 7 (Labor
Day), rolled to Tuesday, Sep. 8 under Fed. R. Civ. P. 6(a)(1)(C). Do not flip
that clock unless the Court enters an order.

Drozd Standing Order I.E: do not file a proposed order with this paper unless
the Court asks. L.R. 233(b) caps an opposition to administrative relief at five
pages; keep the brief inside that limit even though UPS did not label Dkt. 11
as a motion for administrative relief.

    python3 internal/scripts/matter26-opposition-to-extension.py \\
        [--date "September 4, 2026"] [--mailed-from "San Jose, California"]
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
    DISTRICT_EDCAL,
    ProofOfServiceFields,
    build_proof_of_service,
)
from short_link import publish_short_link  # noqa: E402
from signature_stamp import SIGNATURE_NATIVE_PX, SIGNATURE_PATH  # noqa: E402

ROOT = SCRIPT_DIR.parents[1]
DEFAULT_OUT = (
    ROOT
    / "internal/public/documents/matter-26"
    / "Opposition to UPS Consent Motion for Extension of Time to File Reply (Sep 4 2026).pdf"
)
DEFAULT_POS_OUT = (
    ROOT
    / "internal/public/documents/matter-26"
    / "Proof of Service - Opposition to UPS Consent Motion for Extension (Sep 4 2026).pdf"
)

DEFAULT_EXEC_DATE = "September 4, 2026"
DEFAULT_MAILED_FROM = "San Jose, California"
SHORT_LINK_SLUG = "ups-ext-opp"
FOOTER = (
    "PLAINTIFF'S OPPOSITION TO MOTION FOR EXTENSION -- "
    "NEWANFORBI v. UNITED PARCEL SERVICE, INC."
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
    ("Case No. 2:26-cv-02847-DAD-CKD", False, False),
    ("", False, False),
    ("PLAINTIFF'S OPPOSITION TO", True, False),
    ("DEFENDANT UNITED PARCEL", True, False),
    ("SERVICE, INC.'S MOTION FOR", True, False),
    ("EXTENSION OF TIME TO FILE", True, False),
    ("REPLY (ECF No. 11)", True, False),
    ("", False, False),
    ("Hearing (ECF No. 9): Oct. 7, 2026", False, False),
    ("Time: 10:00 a.m.", False, False),
    ("Courtroom: 24 (CKD) (Zoom)", False, False),
    ("Judge: Hon. Carolyn K. Delaney", False, False),
    ("", False, False),
    ("Action filed: July 15, 2026", False, False),
    ("Removed: August 20, 2026", False, False),
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
    "",
    "AND TO (address of record on the docket):",
    "Vanessa W. Mott, Esq.",
    "MARTENSON, HASBROUCK & SIMON LLP",
    "5800 Armada Drive, Suite 101",
    "Carlsbad, CA 92008",
    "Attorneys for Defendant United Parcel Service, Inc.",
]


CONTENT = [
    ("PARA",
     "TO THE HONORABLE COURT, AND TO DEFENDANT UNITED PARCEL SERVICE, INC. AND ITS "
     "ATTORNEYS OF RECORD:"),

    ("PARA",
     "Plaintiff BRENDAN NGEHSI NEWANFORBI, appearing in propria persona, opposes "
     "Defendant United Parcel Service, Inc.'s (\"UPS\") motion for an extension of time "
     "to file a reply in support of its Rule 12(b)(6) motion (ECF No. 11). The paper is "
     "captioned a \"Consent Motion.\" Paragraph 4 of the same paper states that Plaintiff "
     "does not consent. The live reply deadline under Eastern District Local Rule 230(d) "
     "is Tuesday, September 8, 2026. UPS had ample time to meet that deadline. An "
     "extension would prejudice Plaintiff. The Court should deny the motion."),

    ("HEADER", "I.\nTHE MOTION IS NOT CONSENTED AND IS BROUGHT UNDER THE WRONG RULE"),

    ("PARA",
     "UPS invokes Federal Rule of Civil Procedure 16(b)(4). (ECF No. 11 at 2; id. "
     "\u00b66.) That rule governs modification of a scheduling order. No Rule 16 "
     "scheduling order in this action sets the reply date. The reply is set by Local "
     "Rule 230(d): \"No later than ten (10) days after the opposition was filed, the "
     "moving party may serve and file a reply.\""),

    ("PARA",
     "Plaintiff's opposition is ECF No. 10, filed August 28, 2026, to the live motion "
     "(ECF No. 9). UPS's paragraph 2 cites a September 7 deadline to \"[Doc. 8].\" "
     "ECF No. 8 is the August 27 minute order that vacated the October 5 hearing on "
     "the first notice (ECF No. 7, marked disregarded). It is not a reply deadline. "
     "Ten days after August 28 is Monday, September 7, 2026, which is Labor Day. "
     "Under Federal Rule of Civil Procedure 6(a)(1)(C) the period continues to "
     "Tuesday, September 8, 2026."),

    ("PARA",
     "An opposed request to move that date is governed by Local Rule 144. Local Rule "
     "144(a) allows one initial twenty-eight-day stipulation to answer a complaint or "
     "to respond to written discovery, without Court approval. \"All other extensions "
     "of time must be approved by the Court.\" This is not that stipulation. Local "
     "Rule 144(c) permits an initial ex parte extension only on an affidavit that a "
     "stipulation cannot reasonably be obtained, explaining why and why the extension "
     "is necessary. \"Except for one such initial extension, ex parte applications for "
     "extension of time are not ordinarily granted.\" There is no affidavit. Local "
     "Rule 144(d) required counsel to seek the extension \"as soon as the need for an "
     "extension becomes apparent\" and looks with disfavor on requests brought on the "
     "required filing date. Counsel waited until the last business day before Labor "
     "Day."),

    ("PARA",
     "If the paper is treated as a motion for administrative relief -- Standing Order "
     "IV lists \"requests to extend a response deadline\" and \"requests to alter a "
     "briefing schedule\" -- Local Rule 233(a) requires that label, a proposed order, "
     "and a statement of every affected party's position. UPS labeled the paper a "
     "consent motion, lodged no proposed order, and recited Plaintiff's non-consent "
     "in the same filing. If it is treated as an ex parte application -- a refused "
     "stipulation, filed Friday of a holiday weekend, with no hearing noticed -- "
     "Standing Order III required contact with the courtroom deputy, a statement "
     "whether an opposition will be filed, and an affidavit of need, inability to "
     "obtain a stipulation, and why the request cannot be noticed under Local Rule "
     "230. The motion recites none of those. Plaintiff is filing this opposition the "
     "same day so the Court has his position before the reply clock runs."),

    ("HEADER", "II.\nUPS HAD AMPLE TIME"),

    ("PARA",
     "UPS first noticed the motion for October 5, 2026, before District Judge Drozd. "
     "(ECF No. 7.) The Court vacated that hearing and directed UPS to re-notice "
     "before the assigned magistrate judge. (ECF No. 8.) The live motion is ECF No. "
     "9, noticed for October 7, 2026, at 10:00 a.m. in Courtroom 24 before Magistrate "
     "Judge Delaney. UPS chose that date. The ten-day reply clock was knowable the "
     "day the opposition was filed."),

    ("PARA",
     "Plaintiff filed a twenty-page opposition on August 28, 2026, twelve days before "
     "the Local Rule 230(c) opposition deadline. UPS has had those papers for a week. "
     "It used that week to telephone Plaintiff on September 4 and to ask first for "
     "thirty days, then for fifteen. Plaintiff declined both. Counsel then filed this "
     "paper seeking September 14. A thirty-day extension would have run to October 8, "
     "after the October 7 hearing. That sequence is not diligence. It is a moving "
     "target presented on the last business day before the holiday."),

    ("PARA",
     "The stated cause is \"UPS counsel's personal matters, including but not limited "
     "to non-refundable, pre-planned travel for the upcoming holiday weekend.\" (ECF "
     "No. 11 \u00b67.) Pre-planned, non-refundable travel is known in advance. It was "
     "known when UPS selected the October 7 hearing. It was known when the opposition "
     "arrived on August 28. It does not become good cause on the Friday of the weekend "
     "for which the travel was already booked. The motion gives no travel dates, no "
     "showing that the reply could not be prepared before travel, and no showing that "
     "another lawyer at the firm could file it. \"Including but not limited to\" is not "
     "a showing."),

    ("HEADER", "III.\nAN EXTENSION WOULD PREJUDICE PLAINTIFF"),

    ("PARA",
     "UPS asserts that the request \"will not prejudice Plaintiff because the hearing "
     "for this Motion is presently scheduled for October 5, 2026.\" (ECF No. 11 \u00b68.) "
     "That hearing was vacated. (ECF No. 8.) The live hearing is October 7, 2026, at "
     "10:00 a.m. in Courtroom 24 before Magistrate Judge Delaney. (ECF No. 9.) The "
     "hearing date is not a substitute for a complete, timely briefing set. Plaintiff "
     "is proceeding in propria persona. He prepared on the Local Rule clock. Sliding "
     "the reply a week compresses the time he has to read it, to decide whether Local "
     "Rule 230(m)(1) requires an objection to new reply evidence -- due seven days "
     "after the reply is filed -- and to prepare for oral argument on October 7."),

    ("PARA",
     "If the reply is filed September 14, an objection under Local Rule 230(m)(1) "
     "would be due on or about September 21. Plaintiff is served by mail. UPS served "
     "this motion by mail only, on Friday of a holiday weekend, and listed Plaintiff's "
     "email as bnn.cdla@gmail.com. (ECF No. 11-1.) That is not his address. His "
     "address is bnn.cdl@gmail.com, as it appears on the complaint, on ECF No. 10, "
     "and on every paper he has served in this action. He may not have ECF No. 11 in "
     "hand before the reply deadline. That is prejudice."),

    ("PARA",
     "Federal Rule of Civil Procedure 15(a)(1)(B) still allows one amendment as of "
     "right within twenty-one days after service of a Rule 12(b) motion. UPS served "
     "the motion to dismiss by mail on August 26, 2026. That window "
     "runs through September 16, 2026, and may run through September 19 under Rule "
     "6(d). A reply filed September 14 lands inside that window. Plaintiff is entitled "
     "to decide whether to amend with the reply in hand, or to let the window close, "
     "on a clock that does not move because counsel has pre-planned travel. An "
     "extension forces that choice without the reply, or in a compressed few days "
     "after a late reply arrives by mail. Each version of the ask -- thirty days, "
     "then fifteen, now September 14 -- also resets the hearing-preparation calendar. "
     "Plaintiff should not have to re-plan October 7 every time the request shrinks."),

    ("HEADER", "IV.\nCONCLUSION"),

    ("PARA",
     "The motion is not consented. It cites the wrong rule, misstates the deadline, "
     "and is unsupported by an affidavit. UPS had a week with the opposition and a "
     "hearing date it chose. Pre-planned holiday travel is not good cause presented "
     "on the Friday before Labor Day. An extension would prejudice a pro se plaintiff "
     "preparing for October 7 on the Local Rule clock, served by mail, with a Rule 15 "
     "window still open. The Court should deny ECF No. 11. The reply remains due "
     "September 8, 2026. No proposed order is lodged; Local Rule 233(a)(4) runs "
     "against the moving party."),
]


def opposition_pos_fields(exec_date: str, mailed_from: str) -> ProofOfServiceFields:
    """Fill the portfolio four-sided-border Proof of Service (not pleading paper)."""
    return ProofOfServiceFields(
        plaintiff_line="BRENDAN NGEHSI NEWANFORBI",
        plaintiff_role="Plaintiff",
        defendant_lines=[
            "UNITED PARCEL SERVICE, INC.; and",
            "DOES 1 through 10, inclusive",
        ],
        defendant_role="Defendants",
        case_number="2:26-cv-02847-DAD-CKD",
        district_line=DISTRICT_EDCAL,
        title="PROOF OF SERVICE",
        service_date=exec_date,
        document_title=(
            "Plaintiff's Opposition to Defendant United Parcel Service, Inc.'s "
            "Motion for Extension of Time to File Reply (ECF No. 11)"
        ),
        mailing_location=mailed_from,
        recipients=list(SERVICE_ADDRESSEES),
        server_name="Brendan Ngehsi Newanforbi",
        stamp_signature=True,
    )


def build_opposition_proof_of_service(
    out: Path, exec_date: str, mailed_from: str
) -> Path:
    if not Path(SIGNATURE_PATH).is_file():
        raise SystemExit(f"Missing universal signature: {SIGNATURE_PATH}")
    return build_proof_of_service(out, opposition_pos_fields(exec_date, mailed_from))


def _signature(d: PleadingPaper, exec_date: str) -> None:
    d.ensure_space(10)
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


def _render_body(d: PleadingPaper, content: list[tuple[str, str]]) -> None:
    for kind, text in content:
        if kind == "HEADER":
            lines = text.split("\n")
            d.ensure_space(len(lines) + 3)
            for line in lines:
                d.write_line(line, bold=True, center=True)
            d.blank_line()
        elif kind == "PARA":
            d.write_wrapped(text, first_indent=36)
            d.blank_line()
        else:
            raise ValueError(f"unknown content kind {kind!r}")


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
    d.draw_caption_block(CAPTION_LEFT, right_caption, caption_size=10,
                         tight_lh=13, boxed=True)
    d.blank_line()


def append_pdfs(front: Path, back: Path) -> Path:
    """Write front+back into front (in place). Used to attach the POS."""
    assemble([front, back], front)
    return front


def build_opposition(out: Path, exec_date: str, mailed_from: str) -> Path:
    if not Path(SIGNATURE_PATH).is_file():
        raise SystemExit(f"Missing universal signature: {SIGNATURE_PATH}")
    out.parent.mkdir(parents=True, exist_ok=True)
    d = PleadingPaper(str(out), doc_title_footer=FOOTER)
    _header_block(d, CAPTION_RIGHT)
    _render_body(d, CONTENT)
    _signature(d, exec_date)
    d.save()
    return out


def main() -> None:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("out", nargs="?", default=str(DEFAULT_OUT))
    ap.add_argument("--date", default=DEFAULT_EXEC_DATE,
                    help="Date of actual service, printed on the signature and "
                         "Proof of Service.")
    ap.add_argument("--mailed-from", default=DEFAULT_MAILED_FROM,
                    help="City and state where the service copy is deposited with the "
                         "USPS and where the Proof of Service is executed")
    ap.add_argument("--pos-out", default=str(DEFAULT_POS_OUT),
                    help="Path for the four-sided-border Proof of Service PDF")
    ap.add_argument("--skip-pos", action="store_true")
    args = ap.parse_args()
    path = build_opposition(Path(args.out).resolve(), args.date, args.mailed_from)
    if not args.skip_pos:
        pos = build_opposition_proof_of_service(
            Path(args.pos_out).resolve(), args.date, args.mailed_from
        )
        append_pdfs(path, pos)
        print(f"Generated opposition (POS attached): {path}")
        print(f"Generated proof of service: {pos}")
    else:
        print(f"Generated opposition: {path}")
    short = publish_short_link(path, SHORT_LINK_SLUG)
    print(f"Short link copy: {short}")


if __name__ == "__main__":
    main()
