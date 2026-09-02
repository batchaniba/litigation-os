#!/usr/bin/env python3
"""Matter 32 — Administrative motion directing DAG Haiyang A. Li to accept
service of process on behalf of Santiago Meza-Gonzalez.

Nforbi v. Meza-Gonzalez et al., N.D. Cal. No. 4:26-cv-08271-ASK,
related to Serrato, 4:26-cv-05953-ASK.

Civil L.R. 7-11 (miscellaneous administrative matter) plus Fed. R. Civ. P.
4(e)(1) / 4(m) and Cal. Code Civ. Proc. § 413.30. Melano is already served
(Dkt. 5-1 / Document 12). Meza-Gonzalez has not been produced at the
Modesto Area duty station. Li has represented these officers on this
incident in E.D. Cal., Alameda Superior Court, and the related Serrato
action before this Court. Exhibits A–C are Diamond-style covers plus the
caption page of each prior Li appearance.

    python3 internal/scripts/matter32-admin-motion-li-accept-service.py \\
        [--date "September 1, 2026"] [--mailed-from "San Jose, California"]

Not filed until actually presented to the clerk. POS is valid only if
mailed that day from the stated city.
"""

from __future__ import annotations

import argparse
import sys
from pathlib import Path

SCRIPT_DIR = Path(__file__).resolve().parent
sys.path.insert(0, str(SCRIPT_DIR / "lib"))
sys.path.insert(0, str(SCRIPT_DIR))
from exhibit_cover import write_exhibit_cover  # noqa: E402
from pdf_packet import append_page, assemble  # noqa: E402
from pleading_paper import CONTENT_LEFT, PleadingPaper  # noqa: E402
from pypdf import PdfWriter
from proof_of_service import (  # noqa: E402
    DISTRICT_NDCAL,
    ProofOfServiceFields,
    build_proof_of_service,
)
from short_link import publish_short_link  # noqa: E402
from signature_stamp import SIGNATURE_NATIVE_PX, SIGNATURE_PATH  # noqa: E402

ROOT = SCRIPT_DIR.parents[1]
DOCS = ROOT / "internal/public/documents"
OUT_DIR = DOCS / "matter-32/ndcal"

# Caption-page sources — first page only. Do not restamp the filed originals.
EXHIBIT_SOURCES = {
    "A": DOCS / "matter-32/from-01/CHP Motion To Dismiss.pdf",
    "B": DOCS / "matter-32/from-02/Opposition to Motion for U-visa certification.pdf",
    "C": DOCS / "matter-24/Defendant Serrato Motion to Dismiss FAC and Strike (Aug 26 2026).pdf",
}

DEFAULT_DATE = "September 1, 2026"
DEFAULT_MAILED_FROM = "San Jose, California"
SHORT_LINK_SLUG = "meza-li-service"

CASE_NO = "4:26-cv-08271-ASK"
JUDGE = "Hon. Ajay S. Krishnan"

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

MOTION_FOOTER = (
    "ADMIN. MOTION — DAG LI TO ACCEPT SERVICE -- "
    "NFORBI v. MEZA-GONZALEZ ET AL."
)
DECL_FOOTER = (
    "DECLARATION ISO ADMIN. MOTION -- "
    "NFORBI v. MEZA-GONZALEZ ET AL."
)
ORDER_FOOTER = (
    "[PROPOSED] ORDER — DAG LI TO ACCEPT SERVICE -- "
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
    "Defendant (summons served August 14, 2026)",
]

MEZA_BLOCK = [
    "Santiago Meza-Gonzalez, CHP #023295",
    "California Highway Patrol, Modesto Area",
    "4030 Kiernan Avenue",
    "Modesto, CA 95356",
    "Defendant (courtesy copy; Rule 4 incomplete)",
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
            ("Civil L.R. 7-11; Fed. R. Civ. P.", False, False),
            ("4(e)(1), 4(m); Cal. Code Civ.", False, False),
            ("Proc. § 413.30", False, False),
            ("", False, False),
            (f"Judge: {JUDGE}", False, False),
            ("Related: 4:26-cv-05953-ASK", False, False),
        ]
    )
    return rows


MOTION_CAPTION_RIGHT = _caption_right(
    [
        "PLAINTIFF'S ADMINISTRATIVE",
        "MOTION — ORDER DIRECTING",
        "DAG HAIYANG A. LI TO ACCEPT",
        "SERVICE FOR MEZA-GONZALEZ",
    ]
)

DECL_CAPTION_RIGHT = _caption_right(
    [
        "DECLARATION OF BRENDAN",
        "NGWA NFORBI ISO",
        "ADMINISTRATIVE MOTION",
    ]
)

ORDER_CAPTION_RIGHT = _caption_right(
    [
        "[PROPOSED] ORDER GRANTING",
        "ADMINISTRATIVE MOTION —",
        "DAG LI TO ACCEPT SERVICE",
    ]
)


MOTION_CONTENT = [
    ("PARA",
     "TO THE COURT, TO DEFENDANT JOSE MELANO, AND TO DEPUTY ATTORNEY GENERAL "
     "HAIYANG A. LI:"),

    ("PARA",
     "Plaintiff BRENDAN NGWA NFORBI, appearing in propria persona, moves under "
     "Civil Local Rule 7-11, Federal Rule of Civil Procedure 4(e)(1) and 4(m), "
     "and California Code of Civil Procedure section 413.30 for an order "
     "directing Deputy Attorney General Haiyang A. Li to accept service of "
     "process on behalf of Defendant Santiago Meza-Gonzalez. The facts are in "
     "the accompanying declaration."),

    ("HEADER", "I.\nTHE SERVICE GAP"),

    ("PARA",
     "Melano has been served. Meza-Gonzalez has not. Both are California Highway "
     "Patrol officers. Both had identifiable duty stations on the summonses this "
     "Court issued August 10, 2026 (Dkt. 3). Process server Clifford Black served "
     "Melano on August 14, 2026, at CHP South Sacramento, 6 Massie Court, through "
     "Officer Reed, who is designated to accept process for the Patrol at that "
     "station. The AO 440 return was filed as Dkt. 5-1 and entered August 31, "
     "2026 as Document 12 after this Court related the case to <<i:Newanforbi v. "
     "Serrato>>, No. 4:26-cv-05953-ASK, and reassigned it as No. 4:26-cv-08271-ASK. "
     "This motion does not touch that service."),

    ("PARA",
     "Meza-Gonzalez has not been produced at CHP Modesto Area, 4030 Kiernan "
     "Avenue — the address on his issued summons and his assigned post. "
     "Plaintiff's August 13 Stanislaus County Sheriff SER-001 produced no Rule "
     "4(l) return. A private process-server packet went to the same station on "
     "August 25. The papers stop at the duty station. The officer is not "
     "produced. This is the second case on this November 1, 2024 incident in "
     "which his service has lagged behind Melano's. In Alameda Superior Court "
     "No. 26CV168913, the State and Melano were served March 25, 2026; "
     "Meza-Gonzalez required a court-ordered extension to May 4, 2026."),

    ("HEADER", "II.\nDAG LI HAS REPRESENTED THESE OFFICERS THROUGHOUT"),

    ("PARA",
     "Haiyang A. Li, Deputy Attorney General, 300 South Spring Street, Suite "
     "1702, Los Angeles, California 90013-1230, Haiyang.Li@doj.ca.gov, has "
     "appeared for Meza-Gonzalez and Melano — and for the State and the Patrol "
     "— in every civil case on this incident."),

    ("LIST_ITEM",
     "1.  <<i:Newanforbi v. State of California / CHP et al.>>, E.D. Cal. No. "
     "2:25-cv-01460-DC-CSK. Li filed the December 10, 2025 Rule 12(b)(6) motion "
     "and the January 5, 2026 reply for the State, CHP, Meza-Gonzalez, and "
     "Melano. Plaintiff served the April 21, 2026 Objections and July 7, 2026 "
     "Notice of Supplemental Authority on him. On April 9, 2026, Li consulted "
     "those same clients on 28 U.S.C. § 636(c) consent. That case was dismissed "
     "without prejudice August 15, 2026, after this action was filed."),

    ("LIST_ITEM",
     "2.  <<i:Newanforbi v. Meza-Gonzalez et al.>>, Alameda Super. Ct. No. "
     "26CV168913. Li noticed a demurrer April 2, 2026; met and conferred April "
     "9; negotiated and filed a stipulated stay April 13–14; and in June 2026 "
     "opposed the U-visa certification motion for the same defendants. That "
     "case was dismissed without prejudice August 15, 2026."),

    ("LIST_ITEM",
     "3.  <<i:Newanforbi v. Serrato>>, N.D. Cal. No. 4:26-cv-05953-ASK. Li is "
     "counsel of record for Captain G. Serrato — these officers' commander — "
     "before this Court, on claims from the same incident. He filed Serrato's "
     "motion to dismiss August 26, 2026 (Dkt. 18). This Court related the "
     "actions August 24, 2026."),

    ("PARA",
     "Li already has actual notice of this lawsuit, already has a lawyer-client "
     "relationship with this officer on this incident, and already appears "
     "before this Court on the related case. The remaining gap is a Rule 4 "
     "return as to the one officer who has not been produced at his station."),

    ("HEADER", "III.\nTHE COURT MAY DIRECT THIS MANNER OF SERVICE"),

    ("PARA",
     "Rule 4(e)(1) permits service by following California law. Section 413.30 "
     "provides that the court \"may direct that summons be served in a manner "
     "which is reasonably calculated to give actual notice to the party to be "
     "served and that proof of such service be made as prescribed by the "
     "court.\" That is the constitutional floor as well. <<i:Mullane v. Central "
     "Hanover Bank & Trust Co.>>, 339 U.S. 306, 314 (1950). The Ninth Circuit "
     "approves alternative service when ordinary methods have not finished the "
     "work, so long as the method is reasonably calculated to give notice. "
     "<<i:Rio Properties, Inc. v. Rio Int'l Interlink>>, 284 F.3d 1007, 1016-17 "
     "(9th Cir. 2002)."),

    ("PARA",
     "Directing Li to accept the summons and the operative First Amended "
     "Complaint, and treating delivery to him at the Spring Street address and "
     "email he uses as counsel for these officers, is reasonably calculated to "
     "give Meza-Gonzalez actual notice. Li has been this officer's lawyer on "
     "this incident since at least December 2025. Plaintiff is not asking the "
     "Court to treat Li as an already-appointed Rule 4(e)(2)(C) agent. Li has "
     "not appeared in <<i:this>> action, because Meza-Gonzalez has not been "
     "served. Plaintiff asks the Court to <<i:direct>> that service be "
     "completed by delivery to the lawyer who has represented this defendant "
     "throughout. That is the least intrusive way to close a gap duty-station "
     "service has not closed."),

    ("PARA",
     "Civil Local Rule 7-11 is the right vehicle. Completing Rule 4 as to one "
     "defendant so the related cases can move on the same calendar is a "
     "miscellaneous administrative matter. A 35-day noticed motion would add a "
     "month of delay the Court can avoid on the papers."),

    ("PARA",
     "A stipulation could not be obtained before filing because Li has not "
     "appeared here. Plaintiff is serving this motion on him concurrently at "
     "the address and email he uses in <<i:Serrato>>, and invites a stipulation "
     "that he will accept service. If he stipulates, the proposed order can "
     "enter as agreed. If he does not, the Court should grant the motion."),

    ("HEADER", "IV.\nRELIEF REQUESTED"),

    ("PARA",
     "Plaintiff requests that the Court: (1) direct that DAG Li is authorized "
     "and ordered to accept service on behalf of Meza-Gonzalez; (2) provide "
     "that Plaintiff's delivery to Li, by email at Haiyang.Li@doj.ca.gov and "
     "first-class mail at 300 South Spring Street, Suite 1702, Los Angeles, "
     "California 90013-1230, of the issued Meza-Gonzalez summons (Dkt. 3), the "
     "operative First Amended Complaint (Dkt. 5), and the CMC/ADR order "
     "(Dkt. 4), constitutes completed service under Rule 4(e)(1) and section "
     "413.30 as of the email date; (3) direct Plaintiff to file a Rule 4(l) "
     "proof of that delivery within seven days; (4) alternatively, authorize "
     "the same delivery as alternative service, or extend Rule 4(m) for good "
     "cause; and (5) confirm that Melano's completed service is unaffected. A "
     "declaration, Exhibits A through C, and a proposed order accompany this "
     "motion."),
]


DECL_CONTENT = [
    ("PARA",
     "I, BRENDAN NGWA NFORBI, declare as follows:"),

    ("LIST_ITEM",
     "1.  I am the Plaintiff in this action. I am over eighteen years of age. "
     "I make this declaration from my personal knowledge in support of "
     "Plaintiff's Administrative Motion for an Order Directing Deputy Attorney "
     "General Haiyang A. Li to Accept Service of Process on Behalf of "
     "Defendant Santiago Meza-Gonzalez. If called, I could and would testify "
     "competently to these facts."),

    ("LIST_ITEM",
     "2.  This action arises from a November 1, 2024 encounter with California "
     "Highway Patrol Officers Santiago Meza-Gonzalez, badge 023295, and Jose "
     "Melano, badge 023054, on Interstate 580 East in Livermore. The operative "
     "pleading is the First Amended Complaint filed August 17, 2026 (Dkt. 5)."),

    ("LIST_ITEM",
     "3.  The Clerk issued summonses for both officers on August 10, 2026 "
     "(Dkt. 3). Meza-Gonzalez's summons is directed to the CHP Modesto Area "
     "duty station, 4030 Kiernan Avenue, Modesto, California 95356. Melano's "
     "summons is directed to CHP South Sacramento Area, 6 Massie Court, "
     "Sacramento, California 95823."),

    ("LIST_ITEM",
     "4.  On August 13, 2026, I submitted a SER-001 request to the Stanislaus "
     "County Sheriff Civil Division asking that office to serve Meza-Gonzalez "
     "at the Modesto Area duty station, and a SER-001 request to the "
     "Sacramento County Sheriff asking that office to serve Melano at South "
     "Sacramento."),

    ("LIST_ITEM",
     "5.  Melano was served on August 14, 2026. Process server Clifford Black, "
     "owner of C&P Process Server, delivered the summons to Officer Reed at "
     "6 Massie Court. The AO 440 return states that Officer Reed is designated "
     "by law to accept service of process on behalf of the California Highway "
     "Patrol at that station. That return was filed August 17, 2026 as Dkt. "
     "5-1. The clerk-stamped original was entered August 31, 2026 as Document "
     "12 after this action was related to <<i:Newanforbi v. Serrato>>, No. "
     "4:26-cv-05953-ASK, and reassigned to this Court as No. 4:26-cv-08271-ASK."),

    ("LIST_ITEM",
     "6.  No Rule 4(l) return has been filed as to Meza-Gonzalez. The "
     "Stanislaus SER-001 did not produce a filed return. On August 25, 2026, I "
     "prepared a private process-server packet for the same Modesto Area duty "
     "station — issued summons, operative First Amended Complaint, notice "
     "identifying that complaint, and the Court's CMC/ADR order. Defendant has "
     "not been produced for personal service at that station. He has not made "
     "himself available there. The duty-station method that completed service "
     "on his partner has not completed service on him."),

    ("LIST_ITEM",
     "7.  I have personal knowledge of the same pattern in the earlier Alameda "
     "Superior Court action, No. 26CV168913. The State of California / CHP and "
     "Melano were served in that case on March 25, 2026. Meza-Gonzalez was "
     "not. I had to apply ex parte for an extension of time to serve him. The "
     "court extended the deadline to May 4, 2026."),

    ("LIST_ITEM",
     "8.  Deputy Attorney General Haiyang A. Li has been the lawyer for these "
     "officers on this incident throughout. In the Eastern District action, No. "
     "2:25-cv-01460-DC-CSK, he filed the December 10, 2025 motion to dismiss "
     "and the January 5, 2026 reply on behalf of the State, CHP, Meza-Gonzalez, "
     "and Melano. I served my April 21, 2026 Objections and July 7, 2026 Notice "
     "of Supplemental Authority on him. On April 9, 2026, I spoke with him by "
     "telephone about the Alameda demurrer; he agreed in principle to a stay "
     "of that case and said he would consult his clients, including these "
     "officers, on magistrate-judge consent in the Eastern District action."),

    ("LIST_ITEM",
     "9.  In the Alameda action he circulated a draft stay stipulation on "
     "April 13, 2026, accepted my counter-draft on April 14, and caused the "
     "stipulation to be filed the same day. In June 2026 he opposed my U-visa "
     "certification motion in that case on behalf of the State, CHP, "
     "Meza-Gonzalez, and Melano."),

    ("LIST_ITEM",
     "10.  In the related action before this Court, <<i:Newanforbi v. "
     "Serrato>>, No. 4:26-cv-05953-ASK, Li is counsel of record for Captain G. "
     "Serrato. He filed the August 26, 2026 motion to dismiss (Dkt. 18). I have "
     "served papers on him in that case at 300 South Spring Street, Suite "
     "1702, Los Angeles, California 90013-1230, and at Haiyang.Li@doj.ca.gov."),

    ("LIST_ITEM",
     "11.  Li has not appeared in this action. I have not been able to obtain "
     "a stipulation from him before filing this motion, because he is not "
     "counsel of record here while Meza-Gonzalez remains unserved. I am "
     "serving this motion on him concurrently at the Spring Street address and "
     "the email address above, and I request that he stipulate to accept "
     "service for Meza-Gonzalez. If he does, I will so advise the Court."),

    ("LIST_ITEM",
     "12.  I am also serving this motion by first-class mail on Melano at the "
     "South Sacramento duty station where he was served, and I am sending a "
     "courtesy copy to Meza-Gonzalez at the Modesto Area duty station."),

    ("LIST_ITEM",
     "13.  I am not asking the Court to disturb Melano's completed service. I "
     "am asking the Court to close the remaining Rule 4 gap by directing the "
     "lawyer who has represented Meza-Gonzalez on this incident to accept the "
     "papers."),

    ("LIST_ITEM",
     "14.  True and correct copies of the caption pages of those filings are "
     "attached as Exhibit A (Eastern District motion to dismiss, December 10, "
     "2025, naming Li as attorney for Meza-Gonzalez and Melano), Exhibit B "
     "(Alameda opposition to the U-visa certification motion, naming Li as "
     "attorney for the same defendants), and Exhibit C (Serrato motion to "
     "dismiss, August 26, 2026, naming Li as counsel of record for Captain "
     "Serrato)."),

    ("PARA",
     "I declare under penalty of perjury under the laws of the United States "
     "of America that the foregoing is true and correct."),
]


ORDER_CONTENT = [
    ("PARA",
     "Plaintiff has moved under Civil Local Rule 7-11, Federal Rule of Civil "
     "Procedure 4(e)(1) and 4(m), and California Code of Civil Procedure "
     "section 413.30 for an order directing Deputy Attorney General Haiyang A. "
     "Li to accept service of process on behalf of Defendant Santiago "
     "Meza-Gonzalez."),

    ("PARA",
     "The Court has considered the motion, the supporting declaration, and the "
     "record. Defendant Jose Melano has been served. The AO 440 return filed "
     "as Dkt. 5-1 and entered as Document 12 establishes service on Melano at "
     "CHP South Sacramento on August 14, 2026. No Rule 4(l) return has been "
     "filed as to Meza-Gonzalez. The record further shows that Deputy Attorney "
     "General Li has represented Meza-Gonzalez and Melano in prior civil "
     "actions arising from the same November 1, 2024 incident, and that he is "
     "counsel of record for Captain G. Serrato in the related action before "
     "this Court, No. 4:26-cv-05953-ASK."),

    ("PARA",
     "Delivery of the summons and operative complaint to the Deputy Attorney "
     "General who has represented this defendant throughout is a manner of "
     "service reasonably calculated to give actual notice. (Fed. R. Civ. P. "
     "4(e)(1); Cal. Code Civ. Proc. § 413.30; <<i:Mullane v. Central Hanover "
     "Bank & Trust Co.>>, 339 U.S. 306, 314 (1950); <<i:Rio Properties, Inc. "
     "v. Rio Int'l Interlink>>, 284 F.3d 1007, 1016-17 (9th Cir. 2002).)"),

    ("PARA",
     "GOOD CAUSE APPEARING, IT IS ORDERED that:"),

    ("LIST_ITEM",
     "1.  Plaintiff's administrative motion is GRANTED."),

    ("LIST_ITEM",
     "2.  Deputy Attorney General Haiyang A. Li is authorized and directed to "
     "accept service of process on behalf of Defendant Santiago Meza-Gonzalez "
     "in this action."),

    ("LIST_ITEM",
     "3.  Plaintiff's delivery to Deputy Attorney General Li, by electronic "
     "mail at Haiyang.Li@doj.ca.gov and by first-class mail at 300 South "
     "Spring Street, Suite 1702, Los Angeles, California 90013-1230, of "
     "(a) the issued summons as to Meza-Gonzalez (Dkt. 3), (b) the operative "
     "First Amended Complaint (Dkt. 5), and (c) the Order Setting Initial Case "
     "Management Conference and ADR Deadlines (Dkt. 4), shall constitute "
     "completed service on Defendant Santiago Meza-Gonzalez under Federal Rule "
     "of Civil Procedure 4(e)(1) and California Code of Civil Procedure "
     "section 413.30 as of the date of the email transmission."),

    ("LIST_ITEM",
     "4.  Plaintiff shall file a proof of that delivery under Federal Rule of "
     "Civil Procedure 4(l) within seven (7) days of the email transmission."),

    ("LIST_ITEM",
     "5.  Completed service on Defendant Jose Melano is unaffected by this "
     "Order."),

    ("PARA", "IT IS SO ORDERED."),
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
    d.draw_caption_block(CAPTION_LEFT, right_caption, caption_size=9,
                         tight_lh=12, boxed=True)
    d.blank_line()


def _render_body(d: PleadingPaper, content: list[tuple[str, str]]) -> None:
    for kind, text in content:
        if kind == "HEADER":
            lines = text.split("\n")
            d.ensure_space(len(lines) + 2)
            for line in lines:
                d.write_line(line, bold=True, center=True)
            d.blank_line()
        elif kind == "SUBHEAD":
            lines = text.split("\n")
            d.ensure_space(len(lines) + 2)
            for line in lines:
                d.write_line(line, bold=True, center=False)
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
            "Plaintiff's Civil L.R. 7-11 Administrative Motion Directing "
            "DAG Haiyang A. Li to Accept Service for Meza-Gonzalez; "
            "Declaration; Exhibits A-C; [Proposed] Order"
        ),
        mailing_location=mailed_from,
        recipients=recipients,
        server_name="Brendan Ngwa Nforbi",
        stamp_signature=True,
        signature_on_second_page=True,
    )


def build_motion(out: Path, exec_date: str) -> Path:
    out.parent.mkdir(parents=True, exist_ok=True)
    d = PleadingPaper(str(out), doc_title_footer=MOTION_FOOTER)
    _header_block(d, MOTION_CAPTION_RIGHT)
    _render_body(d, MOTION_CONTENT)
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


def build_proposed_order(out: Path) -> Path:
    out.parent.mkdir(parents=True, exist_ok=True)
    d = PleadingPaper(str(out), doc_title_footer=ORDER_FOOTER)
    _header_block(d, ORDER_CAPTION_RIGHT)
    _render_body(d, ORDER_CONTENT)
    d.ensure_space(6)
    d.write_line("Dated: _______________, 2026")
    d.blank_line()
    d.blank_line()
    d.write_line("___________________________________________")
    d.write_line("HON. AJAY S. KRISHNAN")
    d.write_line("United States Magistrate Judge")
    d.save()
    return out


def build_pos(out: Path, exec_date: str, mailed_from: str) -> Path:
    if not Path(SIGNATURE_PATH).is_file():
        raise SystemExit(f"Missing universal signature: {SIGNATURE_PATH}")
    out.parent.mkdir(parents=True, exist_ok=True)
    return build_proof_of_service(out, _pos_fields(exec_date, mailed_from))


def paths_for(exec_date: str) -> dict[str, Path]:
    short = "Sep 1 2026" if exec_date == DEFAULT_DATE else exec_date
    return {
        "motion": OUT_DIR / (
            f"Administrative Motion - DAG Li to Accept Service for "
            f"Meza-Gonzalez (N.D. Cal. 4-26-cv-08271-ASK) ({short}).pdf"
        ),
        "declaration": OUT_DIR / (
            f"Declaration ISO Administrative Motion - DAG Li to Accept "
            f"Service (Meza-Gonzalez) ({short}).pdf"
        ),
        "order": OUT_DIR / (
            f"Proposed Order - DAG Li to Accept Service for Meza-Gonzalez "
            f"(N.D. Cal. 4-26-cv-08271-ASK) ({short}).pdf"
        ),
        "pos": OUT_DIR / (
            f"Proof of Service - Administrative Motion DAG Li to Accept "
            f"Service (Meza-Gonzalez) ({short}).pdf"
        ),
        "packet": OUT_DIR / (
            f"Administrative Motion Packet - DAG Li to Accept Service for "
            f"Meza-Gonzalez (N.D. Cal. 4-26-cv-08271-ASK) ({short}).pdf"
        ),
        "ex_a_cover": OUT_DIR / (
            f"Exhibit A Cover - ED Cal MTD Caption Li for Meza-Gonzalez ({short}).pdf"
        ),
        "ex_a_page": OUT_DIR / (
            "Exhibit A - Caption Page - ED Cal MTD Li Appearance (Dec 10 2025).pdf"
        ),
        "ex_b_cover": OUT_DIR / (
            f"Exhibit B Cover - Alameda U-Visa Opposition Caption Li ({short}).pdf"
        ),
        "ex_b_page": OUT_DIR / (
            "Exhibit B - Caption Page - Alameda U-Visa Opposition Li Appearance.pdf"
        ),
        "ex_c_cover": OUT_DIR / (
            f"Exhibit C Cover - Serrato MTD Caption Li Appearance ({short}).pdf"
        ),
        "ex_c_page": OUT_DIR / (
            "Exhibit C - Caption Page - Serrato MTD Li Appearance (Aug 26 2026).pdf"
        ),
    }


EXHIBIT_COVERS = [
    {
        "letter": "A",
        "cover_key": "ex_a_cover",
        "page_key": "ex_a_page",
        "title": "Caption Page — Eastern District Motion to Dismiss",
        "details": [
            "Newanforbi v. State of California / CHP et al.",
            "E.D. Cal. No. 2:25-cv-01460-DC-CSK — filed December 10, 2025",
            "Haiyang A. Li, attorney for Meza-Gonzalez and Melano",
        ],
    },
    {
        "letter": "B",
        "cover_key": "ex_b_cover",
        "page_key": "ex_b_page",
        "title": "Caption Page — Alameda U-Visa Opposition",
        "details": [
            "Newanforbi v. Meza-Gonzalez et al.",
            "Alameda Super. Ct. No. 26CV168913 — June 2026",
            "Haiyang A. Li, attorney for Meza-Gonzalez and Melano",
        ],
    },
    {
        "letter": "C",
        "cover_key": "ex_c_cover",
        "page_key": "ex_c_page",
        "title": "Caption Page — Serrato Motion to Dismiss",
        "details": [
            "Newanforbi v. Serrato",
            "N.D. Cal. No. 4:26-cv-05953-ASK — filed August 26, 2026 (Dkt. 18)",
            "Haiyang A. Li, counsel of record for Captain G. Serrato",
        ],
    },
]


def extract_caption_page(src: Path, dest: Path) -> Path:
    """Write page 1 of ``src`` only. Do not modify the source filing."""
    if not src.is_file():
        raise SystemExit(f"Missing exhibit source: {src}")
    dest.parent.mkdir(parents=True, exist_ok=True)
    writer = PdfWriter()
    append_page(writer, src, 0)
    with dest.open("wb") as fh:
        writer.write(fh)
    return dest


def build_exhibits(outs: dict[str, Path]) -> list[Path]:
    """Diamond-style covers + one caption page each. Returns packet order."""
    pieces: list[Path] = []
    for spec in EXHIBIT_COVERS:
        write_exhibit_cover(
            outs[spec["cover_key"]],
            court="UNITED STATES DISTRICT COURT",
            court_line2="NORTHERN DISTRICT OF CALIFORNIA",
            caption="NFORBI v. MEZA-GONZALEZ ET AL.",
            case_no=f"Case No. {CASE_NO}",
            exhibit=spec["letter"],
            title=spec["title"],
            details=spec["details"],
            footer=(
                "Administrative Motion — DAG Li to Accept Service — "
                f"Nforbi v. Meza-Gonzalez et al. — Exhibit {spec['letter']}"
            ),
        )
        extract_caption_page(EXHIBIT_SOURCES[spec["letter"]], outs[spec["page_key"]])
        pieces.extend([outs[spec["cover_key"]], outs[spec["page_key"]]])
    return pieces


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--date", default=DEFAULT_DATE)
    parser.add_argument("--mailed-from", default=DEFAULT_MAILED_FROM)
    args = parser.parse_args()

    if not Path(SIGNATURE_PATH).is_file():
        raise SystemExit(f"Missing universal signature: {SIGNATURE_PATH}")

    outs = paths_for(args.date)
    build_motion(outs["motion"], args.date)
    build_declaration(outs["declaration"], args.date, args.mailed_from)
    exhibits = build_exhibits(outs)
    build_proposed_order(outs["order"])
    build_pos(outs["pos"], args.date, args.mailed_from)
    n = assemble(
        [
            outs["motion"],
            outs["declaration"],
            *exhibits,
            outs["order"],
            outs["pos"],
        ],
        outs["packet"],
    )
    publish_short_link(outs["packet"], SHORT_LINK_SLUG)
    print(f"motion:       {outs['motion']}")
    print(f"declaration:  {outs['declaration']}")
    for piece in exhibits:
        print(f"exhibit:      {piece}")
    print(f"order:        {outs['order']}")
    print(f"pos:          {outs['pos']}")
    print(f"packet:       {outs['packet']} ({n} pp.)")
    print(f"short link:   /{SHORT_LINK_SLUG}")
    print(f"FILED_STATUS=False; execution date={args.date}; mailed from={args.mailed_from}")


if __name__ == "__main__":
    main()
