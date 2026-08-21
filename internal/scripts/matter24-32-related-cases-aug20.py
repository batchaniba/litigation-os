#!/usr/bin/env python3
# ==========================================================
# FILING 1 -- Matter 24 (Newanforbi v. Serrato, 4:26-cv-05953-ASK)
#   Administrative Motion to Consider Whether Cases Should Be Related
#   Declaration ISO (Civil L.R. 7-11)
#   [Proposed] Order
#
# FILING 2 -- Matter 32 (Nforbi v. Meza-Gonzalez, 3:26-cv-08271-PHK)
#   Notice of Filing of Administrative Motion (Civil L.R. 3-12(b))
#   Exhibit A (cover + copies of Filing 1 papers)
#
# Execution date: August 20, 2026
# FILED_STATUS: False until actually e-filed via CM/ECF.
#
# Fact corrections vs. the unsigned Aug. 20 root drafts:
#   - Serrato service is USMS personal service Aug. 5, 2026 (USM-285
#     Doc. 15), not July 13 certified mail.
#   - Meza-Gonzalez Dkt. 1 (complaint) is the court pleading of record;
#     both officers were personally served Aug. 14, 2026. The unsigned
#     Aug. 12 FAC has not been lodged.
# ==========================================================
from __future__ import annotations

import sys
from pathlib import Path

SCRIPT_DIR = Path(__file__).resolve().parent
sys.path.insert(0, str(SCRIPT_DIR))
sys.path.insert(0, str(SCRIPT_DIR / "lib"))
from pleading_paper import PleadingPaper  # noqa: E402
from signature_stamp import SIGNATURE_NATIVE_PX, SIGNATURE_PATH  # noqa: E402

try:
    import pymupdf as fitz
except ImportError:  # pragma: no cover
    import fitz  # type: ignore

FILED_STATUS = False
EXEC_DATE = "August 20, 2026"

ROOT = SCRIPT_DIR.parents[1]
M24 = ROOT / "internal/public/documents/matter-24"
M32 = ROOT / "internal/public/documents/matter-32/ndcal"

MOTION_PATH = M24 / (
    "Administrative Motion to Consider Whether Cases Should Be Related "
    "(Aug 20 2026).pdf"
)
DECL_PATH = M24 / (
    "Declaration ISO Administrative Motion to Consider Whether Cases "
    "Should Be Related (Aug 20 2026).pdf"
)
ORDER_PATH = M24 / (
    "Proposed Order Granting Administrative Motion to Consider Whether "
    "Cases Should Be Related (Aug 20 2026).pdf"
)
NOTICE_PATH = M32 / (
    "Notice of Filing of Administrative Motion to Consider Whether Cases "
    "Should Be Related (Aug 20 2026).pdf"
)
EXHIBIT_A_PATH = M32 / (
    "Exhibit A - Administrative Motion Packet from Serrato "
    "4-26-cv-05953-ASK (Aug 20 2026).pdf"
)
COVER_PATH = M32 / (
    "Exhibit A Cover Page - Administrative Motion Packet (Aug 20 2026).pdf"
)

SIG_LINE = "___________________________________"


def _require_signature() -> None:
    if not Path(SIGNATURE_PATH).is_file():
        raise SystemExit(f"Missing universal signature: {SIGNATURE_PATH}")


def _party_block(d: PleadingPaper, name: str, title: str = "Plaintiff, In Pro Per") -> None:
    d.write_attorney_block([
        (name, True),
        title,
        "1455 Cat Tail Drive",
        "Stockton, CA 95204",
        "Telephone: (209) 801-4442",
        "E-mail: bnn.cdl@gmail.com",
    ])


def _sign(d: PleadingPaper, name: str, title: str = "Plaintiff, In Pro Per") -> None:
    d.ensure_space(6)
    d.write_line(f"Dated: {EXEC_DATE}")
    d.write_line("Respectfully submitted,", italic=True)
    d.blank_line()
    d.draw_signature_image(
        SIGNATURE_PATH, SIGNATURE_NATIVE_PX[0], SIGNATURE_NATIVE_PX[1], SIG_LINE
    )
    d.write_line(SIG_LINE, right=True, right_margin_offset=20)
    d.write_line(name, bold=True, right=True, right_margin_offset=20)
    d.write_line(title, right=True, right_margin_offset=20)


def _serrato_caption_left() -> list[tuple[str, bool, bool]]:
    return [
        ("BRENDAN NGEHSI NEWANFORBI,", True, False),
        ("", False, False),
        ("                          Plaintiff,", False, False),
        ("", False, False),
        ("       v.", False, False),
        ("", False, False),
        ("CAPTAIN G. SERRATO, in his individual", False, False),
        ("and official capacities as Commander,", False, False),
        ("Dublin Area, California Highway Patrol,", False, False),
        ("", False, False),
        ("                          Defendant.", False, False),
    ]


def _nforbi_caption_left() -> list[tuple[str, bool, bool]]:
    return [
        ("BRENDAN NGWA NFORBI,", True, False),
        ("", False, False),
        ("                          Plaintiff,", False, False),
        ("", False, False),
        ("       v.", False, False),
        ("", False, False),
        ("SANTIAGO MEZA-GONZALEZ", False, False),
        ("(CHP Badge #023295), in his individual", False, False),
        ("capacity; JOSE MELANO (CHP Badge", False, False),
        ("#023054), in his individual capacity;", False, False),
        ("and DOES 1 through 10, inclusive,", False, False),
        ("", False, False),
        ("                          Defendants.", False, False),
    ]


def build_motion() -> Path:
    d = PleadingPaper(
        str(MOTION_PATH),
        doc_title_footer=(
            "ADMIN. MOTION TO CONSIDER WHETHER CASES SHOULD BE RELATED "
            "-- NEWANFORBI v. SERRATO"
        ),
    )
    _party_block(d, "BRENDAN NGEHSI NEWANFORBI")
    d.write_line("UNITED STATES DISTRICT COURT", bold=True, center=True)
    d.write_line("NORTHERN DISTRICT OF CALIFORNIA", bold=True, center=True)

    right = [
        ("Case No. 4:26-cv-05953-ASK", True, False),
        ("", False, False),
        ("ADMINISTRATIVE MOTION TO", True, False),
        ("CONSIDER WHETHER CASES", True, False),
        ("SHOULD BE RELATED", True, False),
        ("", False, False),
        ("(Civil L.R. 3-12 and 7-11)", False, False),
    ]
    d.draw_caption_block(_serrato_caption_left(), right, caption_size=10, tight_lh=11, boxed=True)
    d.blank_line()

    d.write_wrapped(
        "TO THE HONORABLE AJAY S. KRISHNAN, UNITED STATES MAGISTRATE JUDGE:",
        bold=True,
        first_indent=0,
    )
    d.blank_line()
    d.write_wrapped(
        "Pursuant to Civil Local Rules 3-12 and 7-11, Plaintiff Brendan Ngehsi "
        "Newanforbi, appearing in propria persona, respectfully submits this "
        "Administrative Motion requesting that the Court determine whether the "
        "following two actions are related:"
    )
    d.blank_line()
    d.write_wrapped(
        "1.  <<i:Newanforbi v. Serrato>>, No. 4:26-cv-05953-ASK (the instant "
        "action), assigned to Magistrate Judge Ajay S. Krishnan; and",
        first_indent=0,
    )
    d.blank_line()
    d.write_wrapped(
        "2.  <<i:Nforbi v. Meza-Gonzalez et al.>>, No. 3:26-cv-08271-PHK, "
        "assigned to Magistrate Judge Peter H. Kang.",
        first_indent=0,
    )
    d.blank_line()
    d.write_wrapped(
        "Plaintiff is the same individual in both actions, appearing under "
        "different name variants. The two cases arise from the same nucleus of "
        "operative facts and satisfy both prongs of Civil L.R. 3-12(a)."
    )
    d.blank_line()

    d.ensure_space(4)
    d.write_line("I.", bold=True, center=True)
    d.write_line("STATEMENT OF RELATIONSHIP UNDER CIVIL L.R. 3-12(a)", bold=True, center=True)
    d.blank_line()
    d.write_line("A.  The Actions Concern Substantially the Same Transaction or Event", bold=True)
    d.blank_line()
    d.write_wrapped(
        "Both actions arise from a single encounter on November 1, 2024, on "
        "Interstate 580 East in Livermore, Alameda County, California. During "
        "that encounter, California Highway Patrol Officers Santiago "
        "Meza-Gonzalez (Badge #023295) and Jose Melano (Badge #023054) "
        "conducted a traffic stop of Plaintiff, arrested him, and obtained an "
        "involuntary blood draw through a search warrant. Plaintiff alleges "
        "that the officers fabricated material statements in a sworn CHP "
        "report to justify the arrest and procure the blood-draw warrant."
    )
    d.blank_line()
    d.write_wrapped(
        "The instant action, <<i:Newanforbi v. Serrato>>, challenges the "
        "subsequent denial of Plaintiff's Form I-918, Supplement B "
        "certification request by Captain G. Serrato, Commander of the CHP "
        "Dublin Area. Serrato's denial rests on his characterization of the "
        "November 1 incident. This Court's June 29, 2026 screening order "
        "(Dkt. No. 5) expressly recounted Plaintiff's allegations that CHP "
        "officers subjected him to a false arrest, fabricated material "
        "statements in a sworn report, and forced an involuntary blood draw "
        "through a warrant procured by those fabrications."
    )
    d.blank_line()
    d.write_wrapped(
        "The related action, <<i:Nforbi v. Meza-Gonzalez>>, asserts six causes "
        "of action under 42 U.S.C. § 1983 directly against Officers "
        "Meza-Gonzalez and Melano for their conduct during that same "
        "encounter, including claims for judicial deception, fabrication of "
        "evidence, unlawful arrest, unlawful entry, unlawful search, and First "
        "Amendment retaliation. The complaint in that action was docketed on "
        "August 10, 2026 as Dkt. 1 and remains the court pleading of record. "
        "Both officers were personally served on August 14, 2026."
    )
    d.blank_line()
    d.write_wrapped(
        "The factual nucleus is identical. Both actions require adjudication "
        "of substantially overlapping facts concerning: the November 1, 2024 "
        "encounter between Plaintiff and Officers Meza-Gonzalez and Melano; "
        "the contents and accuracy of the CHP dashcam recording that captured "
        "the entire two-hour encounter; the officers' observations, conduct, "
        "and representations during the encounter; the accuracy of the "
        "officers' subsequent sworn statements in the CHP report; the "
        "circumstances of Plaintiff's arrest; and the warrant application and "
        "resulting involuntary blood draw."
    )
    d.blank_line()
    d.write_wrapped("The first element of Civil L.R. 3-12(a) is satisfied.")
    d.blank_line()

    d.ensure_space(4)
    d.write_line(
        "B.  Separate Adjudication Risks Duplicative Labor and Inconsistent Results",
        bold=True,
    )
    d.blank_line()
    d.write_wrapped(
        "If these actions proceed before different judges, each will "
        "independently examine the same evidentiary record, including the "
        "same CHP dashcam footage, the same CHP report, and the same warrant "
        "materials. This will produce unduly burdensome duplication of "
        "judicial labor."
    )
    d.blank_line()
    d.write_wrapped(
        "More critically, separate adjudication risks inconsistent factual "
        "findings concerning the officers' conduct on November 1, 2024, the "
        "accuracy of their sworn representations, and the lawfulness of the "
        "arrest and blood draw. For example, a determination in one action "
        "that the officers' sworn statements were truthful could directly "
        "conflict with a determination in the other action that those same "
        "statements were fabricated."
    )
    d.blank_line()
    d.write_wrapped(
        "This Court has already familiarized itself with this factual "
        "nucleus. In its June 29, 2026 screening order, the Court reviewed "
        "Plaintiff's detailed allegations concerning the officers' conduct, "
        "the fabricated report, and the warrant-based blood draw, and "
        "concluded that the complaint states a claim sufficient to satisfy "
        "§ 1915 review. Reassignment of the related action to this Court "
        "would promote judicial economy by consolidating before a single "
        "judge both federal actions arising from the same set of events."
    )
    d.blank_line()
    d.write_wrapped(
        "The second element of Civil L.R. 3-12(a) is therefore satisfied."
    )
    d.blank_line()

    d.ensure_space(4)
    d.write_line("II.", bold=True, center=True)
    d.write_line("COMPLIANCE WITH CIVIL L.R. 7-11", bold=True, center=True)
    d.blank_line()
    d.write_wrapped(
        "Civil L.R. 7-11(a) requires that an administrative motion be "
        "accompanied by a proposed order and either a stipulation under Civil "
        "L.R. 7-12 or a declaration explaining why a stipulation could not be "
        "obtained. A Declaration of Plaintiff is filed concurrently herewith, "
        "explaining that no defendant has appeared in either action, making "
        "stipulation impossible at this time. A Proposed Order is also "
        "submitted concurrently."
    )
    d.blank_line()

    d.ensure_space(4)
    d.write_line("III.", bold=True, center=True)
    d.write_line("CONCLUSION", bold=True, center=True)
    d.blank_line()
    d.write_wrapped(
        "For the foregoing reasons, Plaintiff respectfully requests that the "
        "Court find <<i:Newanforbi v. Serrato>>, No. 4:26-cv-05953-ASK, and "
        "<<i:Nforbi v. Meza-Gonzalez et al.>>, No. 3:26-cv-08271-PHK, to be "
        "related under Civil L.R. 3-12(a) and direct the Clerk to reassign "
        "the higher-numbered action to this Court pursuant to Civil L.R. "
        "3-12(f)(3)."
    )
    d.blank_line()
    d.write_wrapped(
        "Pursuant to Civil L.R. 3-12(b), a copy of this motion has been filed "
        "in <<i:Nforbi v. Meza-Gonzalez et al.>>, No. 3:26-cv-08271-PHK, "
        "using the \"Notice (Other)\" ECF event."
    )
    _sign(d, "BRENDAN NGEHSI NEWANFORBI")
    d.save()
    return MOTION_PATH


def build_declaration() -> Path:
    d = PleadingPaper(
        str(DECL_PATH),
        doc_title_footer="DECLARATION ISO ADMIN. MOTION -- NEWANFORBI v. SERRATO",
    )
    _party_block(d, "BRENDAN NGEHSI NEWANFORBI")
    d.write_line("UNITED STATES DISTRICT COURT", bold=True, center=True)
    d.write_line("NORTHERN DISTRICT OF CALIFORNIA", bold=True, center=True)

    right = [
        ("Case No. 4:26-cv-05953-ASK", True, False),
        ("", False, False),
        ("DECLARATION OF BRENDAN", True, False),
        ("NGEHSI NEWANFORBI IN SUPPORT", True, False),
        ("OF ADMINISTRATIVE MOTION TO", True, False),
        ("CONSIDER WHETHER CASES", True, False),
        ("SHOULD BE RELATED", True, False),
        ("", False, False),
        ("(Civil L.R. 7-11)", False, False),
    ]
    d.draw_caption_block(_serrato_caption_left(), right, caption_size=10, tight_lh=11, boxed=True)
    d.blank_line()

    d.write_line("DECLARATION OF BRENDAN NGEHSI NEWANFORBI", bold=True, center=True)
    d.blank_line()
    d.write_wrapped("I, Brendan Ngehsi Newanforbi, declare as follows:", first_indent=0)
    d.blank_line()
    d.write_wrapped(
        "1.  I am the Plaintiff in this action, <<i:Newanforbi v. Serrato>>, "
        "No. 4:26-cv-05953-ASK, and in the related action, <<i:Nforbi v. "
        "Meza-Gonzalez et al.>>, No. 3:26-cv-08271-PHK. I appear in propria "
        "persona in both actions.",
        first_indent=0,
    )
    d.blank_line()
    d.write_wrapped(
        "2.  Civil Local Rule 7-11(a) requires that an administrative motion "
        "be accompanied by either a stipulation under Civil L.R. 7-12 or a "
        "declaration explaining why a stipulation could not be obtained.",
        first_indent=0,
    )
    d.blank_line()
    d.write_wrapped(
        "3.  I am unable to obtain a stipulation because no defendant has "
        "appeared in either action:",
        first_indent=0,
    )
    d.blank_line()
    d.write_wrapped(
        "a.  In the instant action, <<i:Newanforbi v. Serrato>>, the United "
        "States Marshals Service personally served Defendant Captain G. "
        "Serrato with process on August 5, 2026, at 10:20 a.m., at the "
        "California Highway Patrol Dublin Area office, 4999 Gleason Drive, "
        "Dublin, California, via Kim Schoonmaker, Office Assistant (USM-285 "
        "Process Receipt and Return, Doc. 15, filed August 6, 2026). "
        "Defendant Serrato's time to answer or otherwise respond runs to "
        "August 26, 2026. As of the date of this Declaration, Defendant "
        "Serrato has not appeared or filed any responsive pleading.",
        first_indent=0,
    )
    d.blank_line()
    d.write_wrapped(
        "b.  In the related action, <<i:Nforbi v. Meza-Gonzalez et al.>>, the "
        "complaint was docketed on August 10, 2026 as Dkt. 1 and remains the "
        "court pleading of record. Both defendants were personally served on "
        "August 14, 2026 -- Officer Meza-Gonzalez via the Stanislaus County "
        "Sheriff at the CHP Modesto Area, and Officer Melano via the "
        "Sacramento County Sheriff at the CHP South Sacramento Area. Their "
        "time to answer or otherwise respond runs to September 4, 2026. As of "
        "the date of this Declaration, neither defendant has appeared or "
        "filed any responsive pleading.",
        first_indent=0,
    )
    d.blank_line()
    d.write_wrapped(
        "4.  Because no defendant has appeared in either action, it is not "
        "possible to obtain a stipulation regarding the relationship of these "
        "cases at this time.",
        first_indent=0,
    )
    d.blank_line()
    d.write_wrapped(
        "I declare under penalty of perjury under the laws of the United "
        "States that the foregoing is true and correct.",
        first_indent=0,
    )
    d.blank_line()
    d.write_line(f"Executed on {EXEC_DATE}, in Milpitas, California.")
    _sign(d, "BRENDAN NGEHSI NEWANFORBI")
    d.save()
    return DECL_PATH


def build_proposed_order() -> Path:
    d = PleadingPaper(
        str(ORDER_PATH),
        doc_title_footer="[PROPOSED] ORDER -- RELATED CASES -- NEWANFORBI v. SERRATO",
    )
    d.write_line("UNITED STATES DISTRICT COURT", bold=True, center=True)
    d.write_line("NORTHERN DISTRICT OF CALIFORNIA", bold=True, center=True)

    right = [
        ("Case No. 4:26-cv-05953-ASK", True, False),
        ("", False, False),
        ("[PROPOSED] ORDER GRANTING", True, False),
        ("ADMINISTRATIVE MOTION TO", True, False),
        ("CONSIDER WHETHER CASES", True, False),
        ("SHOULD BE RELATED", True, False),
        ("", False, False),
        ("(Civil L.R. 3-12)", False, False),
    ]
    d.draw_caption_block(_serrato_caption_left(), right, caption_size=10, tight_lh=11, boxed=True)
    d.blank_line()
    d.write_wrapped(
        "Having considered Plaintiff's Administrative Motion to Consider "
        "Whether Cases Should Be Related, filed pursuant to Civil Local Rules "
        "3-12 and 7-11, and good cause appearing therefor:",
        first_indent=0,
    )
    d.blank_line()
    d.write_wrapped("IT IS HEREBY ORDERED that:", first_indent=0)
    d.blank_line()
    d.write_wrapped(
        "1.  The following actions are related within the meaning of Civil "
        "L.R. 3-12(a):",
        first_indent=0,
    )
    d.blank_line()
    d.write_wrapped(
        "a.  <<i:Newanforbi v. Serrato>>, No. 4:26-cv-05953-ASK; and",
        first_indent=0,
    )
    d.blank_line()
    d.write_wrapped(
        "b.  <<i:Nforbi v. Meza-Gonzalez et al.>>, No. 3:26-cv-08271-PHK.",
        first_indent=0,
    )
    d.blank_line()
    d.write_wrapped(
        "2.  Pursuant to Civil L.R. 3-12(f)(3), the Clerk is directed to "
        "reassign <<i:Nforbi v. Meza-Gonzalez et al.>>, No. 3:26-cv-08271-PHK, "
        "to the undersigned.",
        first_indent=0,
    )
    d.blank_line()
    d.write_wrapped(
        "3.  The case management conference in <<i:Nforbi v. Meza-Gonzalez "
        "et al.>> shall be rescheduled by the undersigned in accordance with "
        "Civil L.R. 3-12(g).",
        first_indent=0,
    )
    d.blank_line()
    d.write_line("IT IS SO ORDERED.")
    d.ensure_space(6)
    d.blank_line()
    d.write_line("Dated: _______________", right=True, right_margin_offset=20)
    d.blank_line()
    d.write_line(SIG_LINE, right=True, right_margin_offset=20)
    d.write_line("HON. AJAY S. KRISHNAN", bold=True, right=True, right_margin_offset=20)
    d.write_line("United States Magistrate Judge", right=True, right_margin_offset=20)
    d.save()
    return ORDER_PATH


def build_notice() -> Path:
    d = PleadingPaper(
        str(NOTICE_PATH),
        doc_title_footer=(
            "NOTICE OF FILING OF ADMIN. MOTION -- "
            "NFORBI v. MEZA-GONZALEZ ET AL."
        ),
    )
    _party_block(d, "BRENDAN NGWA NFORBI")
    d.write_line("UNITED STATES DISTRICT COURT", bold=True, center=True)
    d.write_line("NORTHERN DISTRICT OF CALIFORNIA", bold=True, center=True)

    right = [
        ("Case No. 3:26-cv-08271-PHK", True, False),
        ("", False, False),
        ("NOTICE OF FILING OF", True, False),
        ("ADMINISTRATIVE MOTION TO", True, False),
        ("CONSIDER WHETHER CASES", True, False),
        ("SHOULD BE RELATED", True, False),
        ("", False, False),
        ("(Civil L.R. 3-12(b))", False, False),
    ]
    d.draw_caption_block(_nforbi_caption_left(), right, caption_size=10, tight_lh=11, boxed=True)
    d.blank_line()
    d.write_line(
        "NOTICE OF FILING OF ADMINISTRATIVE MOTION",
        bold=True,
        center=True,
    )
    d.write_line("TO CONSIDER WHETHER CASES SHOULD BE RELATED", bold=True, center=True)
    d.blank_line()
    d.write_wrapped(
        "TO THE CLERK OF THE COURT AND ALL PARTIES:",
        bold=True,
        first_indent=0,
    )
    d.blank_line()
    d.write_wrapped(
        "Pursuant to Civil Local Rule 3-12(b), Plaintiff Brendan Ngwa Nforbi "
        "hereby gives notice that an Administrative Motion to Consider "
        "Whether Cases Should Be Related has been filed in the "
        "lowest-numbered related action:"
    )
    d.blank_line()
    d.write_wrapped(
        "<<i:Newanforbi v. Serrato>>, No. 4:26-cv-05953-ASK (Magistrate "
        "Judge Ajay S. Krishnan).",
        first_indent=0,
    )
    d.blank_line()
    d.write_wrapped(
        "The Administrative Motion requests that the Court determine whether "
        "the instant action, <<i:Nforbi v. Meza-Gonzalez et al.>>, No. "
        "3:26-cv-08271-PHK, is related to <<i:Newanforbi v. Serrato>> under "
        "Civil L.R. 3-12(a) on the grounds that both actions arise from the "
        "same November 1, 2024 encounter between Plaintiff and California "
        "Highway Patrol Officers Santiago Meza-Gonzalez and Jose Melano on "
        "Interstate 580 East in Livermore, Alameda County, California, and "
        "that separate adjudication would risk duplicative examination of the "
        "same evidentiary record and inconsistent factual findings."
    )
    d.blank_line()
    d.write_wrapped(
        "A true and correct copy of the Administrative Motion, together with "
        "the accompanying Declaration and Proposed Order filed in "
        "<<i:Newanforbi v. Serrato>>, No. 4:26-cv-05953-ASK, is attached "
        "hereto as Exhibit A."
    )
    _sign(d, "BRENDAN NGWA NFORBI")
    d.save()
    return NOTICE_PATH


def build_exhibit_a_cover() -> Path:
    d = PleadingPaper(
        str(COVER_PATH),
        doc_title_footer="EXHIBIT A -- NFORBI v. MEZA-GONZALEZ ET AL.",
    )
    d.blank_line()
    d.blank_line()
    d.write_line("EXHIBIT A", bold=True, center=True)
    d.blank_line()
    d.write_wrapped(
        "Administrative Motion to Consider Whether Cases Should Be Related "
        "Pursuant to Civil L.R. 3-12, with Accompanying Declaration and "
        "Proposed Order, Filed in <<i:Newanforbi v. Serrato>>, No. "
        "4:26-cv-05953-ASK",
        first_indent=0,
    )
    d.save()
    return COVER_PATH


def merge_exhibit_a(cover: Path, motion: Path, declaration: Path, order: Path) -> Path:
    out = fitz.open()
    for path in (cover, motion, declaration, order):
        src = fitz.open(path)
        out.insert_pdf(src)
        src.close()
    EXHIBIT_A_PATH.parent.mkdir(parents=True, exist_ok=True)
    out.save(str(EXHIBIT_A_PATH))
    out.close()
    return EXHIBIT_A_PATH


def build() -> list[Path]:
    _require_signature()
    M24.mkdir(parents=True, exist_ok=True)
    M32.mkdir(parents=True, exist_ok=True)
    motion = build_motion()
    declaration = build_declaration()
    order = build_proposed_order()
    notice = build_notice()
    cover = build_exhibit_a_cover()
    exhibit_a = merge_exhibit_a(cover, motion, declaration, order)
    # Cover is absorbed into Exhibit A; do not leave a standalone extra PDF.
    if cover.exists() and cover != exhibit_a:
        cover.unlink()
    return [motion, declaration, order, notice, exhibit_a]


if __name__ == "__main__":
    written = build()
    print(f"FILED_STATUS={FILED_STATUS}; execution date={EXEC_DATE}")
    for path in written:
        print(f"Wrote {path}")
