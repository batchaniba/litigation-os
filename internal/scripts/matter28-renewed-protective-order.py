#!/usr/bin/env python3
"""Generate corrected renewed Protective Order drafts for Matter 28.

The July 16, 2026 Motion for Protective Order was denied without prejudice
(Doc 7, Jul. 23, 2026). Citation audit Round 3 found two bad cites in that
package:

  - Dunford v. Rovi Corp., 2015 WL 13752958 — NOT_FOUND
  - Condit v. Dunne quote — MISCITED (the "fruits of one litigation"
    sentence is from Foltz, 331 F.3d at 1131)

This script does not alter the filed historical PDFs. It writes renewed
drafts under matter-28/ with corrected authority, the assigned case number,
and a short renewal predicate. The declaration is unchanged (no bad cites).

Outputs:
  internal/public/documents/matter-28/
    Renewed Motion Protective Order NDCA (cite-corrected draft).pdf
    Proposed Protective Order NDCA (cite-corrected draft).pdf
"""

from __future__ import annotations

import os
import sys
from pathlib import Path

SCRIPT_DIR = Path(__file__).resolve().parent
sys.path.insert(0, str(SCRIPT_DIR / "lib"))

try:
    import reportlab  # noqa: F401
except ImportError:
    os.system(f"{sys.executable} -m pip install reportlab -q")

import pymupdf

from pleading_paper import PleadingPaper

ROOT = SCRIPT_DIR.parents[1]
OUT_DIR = ROOT / "internal/public/documents/matter-28"

MOTION_OUT = OUT_DIR / "Renewed Motion Protective Order NDCA (cite-corrected draft).pdf"
PROPOSED_OUT = OUT_DIR / "Proposed Protective Order NDCA (cite-corrected draft).pdf"
PROPOSED_SRC = OUT_DIR / "Proposed Protective Order NDCA.pdf"

CASE_NO = "3:26-cv-07504"
JUDGE = "Hon. Lisa J. Cisneros"
FOOTER_MOTION = "RENEWED MOTION FOR PROTECTIVE ORDER — NEWANFORBI v. SMITH, ET AL."
FOOTER_PROPOSED = "[PROPOSED] PROTECTIVE ORDER RE: CONFIDENTIAL INFORMATION"

# Corrected cross-use authority — Foltz already cited in the original for good cause;
# it is also the true source of the "fruits of one litigation" sentence.
FOLTZ_CROSS_USE = (
    "With respect to the use of discovery materials obtained in related litigation, "
    "this Circuit \"strongly favors access to discovery materials to meet the needs of "
    "parties engaged in collateral litigation.\" Foltz v. State Farm Mut. Auto. Ins. Co., "
    "331 F.3d 1122, 1131 (9th Cir. 2003). \"Allowing the fruits of one litigation to "
    "facilitate preparation in other cases advances the interests of judicial economy by "
    "avoiding the wasteful duplication of discovery.\" Id. (citing Beckman Indus., Inc. v. "
    "Int'l Ins. Co., 966 F.2d 470, 475 (9th Cir. 1992)). Courts routinely permit such use "
    "where the materials are relevant and the producing party's legitimate confidentiality "
    "interests are preserved under an equivalent protective order."
)

FOLTZ_ARG_B = (
    "Federal courts strongly favor avoiding such duplication. In Foltz, 331 F.3d at 1131, "
    "the Ninth Circuit held that \"[a]llowing the fruits of one litigation to facilitate "
    "preparation in other cases advances the interests of judicial economy by avoiding the "
    "wasteful duplication of discovery.\" The burden falls on the party opposing cross-use "
    "to demonstrate \"good cause\" for the restriction — not on the party seeking to use "
    "relevant materials that have already been produced under protective order."
)


def _caption_left():
    return [
        ("BRENDAN NGEHSI NEWANFORBI,", False, False),
        ("", False, False),
        ("               Plaintiff,", False, False),
        ("", False, False),
        ("       v.", False, False),
        ("", False, False),
        ("SHANNON SMITH, LCSW, Chief", False, False),
        ("Executive Officer and Founder of", False, False),
        ("HOPE Program, an individual; and", False, False),
        ("HOPE PSYCHOTHERAPY, INC., d/b/a", False, False),
        ("HOPE PROGRAM, a California", False, False),
        ("corporation,", False, False),
        ("", False, False),
        ("               Defendants.", False, False),
    ]


def _write_party_header(d: PleadingPaper):
    d.write_line("BRENDAN NGEHSI NEWANFORBI", bold=True, size=11)
    d.write_line("Plaintiff In Pro Per", size=11)
    d.write_line("1455 Cat Tail Drive", size=11)
    d.write_line("Stockton, CA 95204", size=11)
    d.write_line("Tel: (209) 801-4442", size=11)
    d.write_line("E-mail: bnn.cdl@gmail.com", size=11)
    d.blank_line()
    d.write_line("UNITED STATES DISTRICT COURT", bold=True, center=True, size=11)
    d.write_line("NORTHERN DISTRICT OF CALIFORNIA", bold=True, center=True, size=11)
    d.blank_line()


def build_motion(path: Path) -> None:
    d = PleadingPaper(str(path), doc_title_footer=FOOTER_MOTION)
    _write_party_header(d)

    right = [
        (f"Case No.: {CASE_NO}", True, False),
        ("", False, False),
        ("NOTICE OF MOTION AND", True, False),
        ("RENEWED MOTION FOR", True, False),
        ("PROTECTIVE ORDER RE:", True, False),
        ("CONFIDENTIAL INFORMATION;", True, False),
        ("MEMORANDUM OF POINTS AND", True, False),
        ("AUTHORITIES", True, False),
        ("", False, False),
        ("[Fed. R. Civ. P. 26(c)(1)]", False, False),
        ("", False, False),
        (f"Judge: {JUDGE}", False, False),
        ("Hearing Date: _______________", False, False),
        ("Hearing Time: _______________", False, False),
    ]
    d.draw_caption_block(_caption_left(), right, caption_size=9, tight_lh=12)
    d.blank_line()

    d.write_line("NOTICE OF MOTION AND RENEWED MOTION FOR PROTECTIVE ORDER",
                 bold=True, center=True, size=11)
    d.blank_line()
    d.write_line("TO ALL PARTIES AND THEIR COUNSEL OF RECORD:", bold=True)
    d.write_wrapped(
        "PLEASE TAKE NOTICE that Plaintiff BRENDAN NGEHSI NEWANFORBI, appearing "
        "in propria persona, hereby renews his motion pursuant to Federal Rule of Civil "
        f"Procedure 26(c)(1) in Case No. {CASE_NO} for entry of a Protective Order Re: "
        "Confidential Information to govern discovery in this action and to authorize the "
        "retention and use of confidential discovery materials previously produced in the "
        "related, now-disposed state-court action Newanforbi v. Palacios et al., San Joaquin "
        "County Superior Court, Case No. STK-CV-UF-2026-0001032 (the \"State Action\")."
    )
    d.write_wrapped(
        "This Renewed Motion replaces the Motion for Protective Order filed July 16, 2026, "
        "which the Court denied without prejudice on July 23, 2026 (Doc 7). The citation "
        "authorities in Sections III and IV.B of that motion have been corrected: the "
        "cross-use proposition is grounded exclusively in Foltz v. State Farm Mut. Auto. "
        "Ins. Co., 331 F.3d 1122 (9th Cir. 2003), and two authorities that do not support "
        "the proposition previously attributed to them have been removed."
    )
    d.write_wrapped(
        "This Motion is made on the grounds that: (1) good cause exists under Rule 26(c)(1) "
        "to protect confidential clinical records, personnel files, proprietary treatment "
        "protocols, and privacy-protected information that will be produced or have already "
        "been produced in litigation arising from the same nucleus of operative fact; "
        "(2) federal courts strongly favor allowing the use of discovery materials obtained "
        "in related litigation to avoid wasteful duplication of discovery; and (3) the "
        "Proposed Protective Order will protect the legitimate confidentiality interests of "
        "all parties while permitting the efficient prosecution of this action."
    )
    d.write_wrapped(
        "This Motion is based on this Notice, the accompanying Memorandum of Points and "
        "Authorities, the Declaration of Brendan Ngehsi Newanforbi previously filed with "
        "the July 16, 2026 motion (and re-lodged herewith by reference), the [Proposed] "
        "Protective Order Re: Confidential Information filed herewith (cite-corrected), "
        "the pleadings and papers on file in this action, and such oral argument as the "
        "Court may permit."
    )
    d.write_wrapped(
        "Pursuant to Federal Rule of Civil Procedure 26(c)(1), Plaintiff certifies that he "
        "will meet and confer with Defendants' counsel regarding any modifications to the "
        "Proposed Protective Order promptly upon Defendants' appearance. Courtesy copies "
        "of this Renewed Motion are being served on counsel who appeared for HOPE in the "
        "State Action."
    )

    d.ensure_space(3)
    d.write_line("MEMORANDUM OF POINTS AND AUTHORITIES", bold=True, center=True)
    d.blank_line()
    d.write_line("I.  INTRODUCTION", bold=True)
    d.write_wrapped(
        "This action arises from substantially the same nucleus of operative fact as the "
        "now-disposed State Action, in which the parties conducted extensive discovery "
        "involving highly sensitive materials — including clinical treatment records, "
        "proprietary treatment protocols, personnel files, and counseling materials "
        "protected by the constitutional right to privacy. A Stipulated Protective Order "
        "governed that discovery. (Newanforbi Decl. ¶¶ 3-4.)"
    )
    d.write_wrapped(
        "Plaintiff moves for a Protective Order that accomplishes two objectives: "
        "(1) establishing a framework to govern future discovery in this action, and "
        "(2) authorizing the retention and use of the state-court discovery materials under "
        "equivalent protections. The July 23, 2026 denial without prejudice expressly left "
        "this path open; this Renewed Motion supplies corrected authority and updated "
        "procedural context."
    )

    d.write_line("II.  PROCEDURAL BACKGROUND", bold=True)
    d.write_line("A.  The State Action and State-Court Protective Order", bold=True)
    d.write_wrapped(
        "On February 10, 2026, Plaintiff filed a complaint in the San Joaquin County "
        "Superior Court against Katie Palacios and HOPE Psychotherapy, Inc. (\"HOPE\"), "
        "asserting claims arising from HOPE's blanket retention policy in its "
        "CDCR-contracted sex offender treatment program. (Newanforbi Decl. ¶ 2.) During "
        "discovery, Defendants produced 542 pages of documents, including HOPE's Clinical "
        "Operational Manual, employee personnel records, clinical practice guidelines, "
        "collateral notes, email communications, and insurance policy information. "
        "(Newanforbi Decl. ¶ 5.)"
    )
    d.write_wrapped(
        "On or about June 17, 2026, the San Joaquin County Superior Court entered a "
        "Stipulated Protective Order agreed to by both parties. (Newanforbi Decl. ¶¶ 3-4, "
        "Ex. A.) The State PO authorized use of Confidential Information in the State "
        "Action and in the related federal action Newanforbi v. Derrick et al., Case No. "
        "2:26-cv-00004-DJC-JDP (E.D. Cal.), but did not authorize use in any other "
        "proceeding. Section VIII of the State PO requires each party to return or destroy "
        "Confidential Information within sixty days after the conclusion of the State "
        "Action or the Derrick action, whichever is later — with \"conclusion\" tied to "
        "final judgment, settlement, or consent decree plus appeal time. "
        "(Newanforbi Decl. ¶ 6; State PO § VIII.)"
    )
    d.write_line("B.  Disposition of the State Action and This Action", bold=True)
    d.write_wrapped(
        "On July 15, 2026, the San Joaquin County Superior Court sustained Defendants' "
        "demurrer without leave to amend on exhaustion grounds. Plaintiff then filed this "
        f"action (Case No. {CASE_NO}) under 42 U.S.C. § 1983, 18 U.S.C. § 1962, California "
        "Civil Code § 52.1, and common law, arising from the same blanket retention "
        "policy, false reports to CDCR, and retaliatory conduct. This action names "
        "Shannon Smith, LCSW, CEO and Founder of HOPE, as lead defendant — a party who "
        "was not named in the State Action."
    )
    d.write_wrapped(
        "On July 23, 2026, this Court denied the original Protective Order motion without "
        "prejudice (Doc 7), questioning its authority to alter the State PO's "
        "return-or-destroy deadline and noting that the Eastern District Derrick action "
        "then still had a motion to dismiss under submission. Subsequent developments — "
        "including the July 24, 2026 Eastern District ruling and Plaintiff's July 30, 2026 "
        "Notice of Payment and Filing of State Court Decision (Doc 9) — supply the "
        "updated record for renewal."
    )

    d.write_line("III.  LEGAL STANDARD", bold=True)
    d.write_wrapped(
        "Federal Rule of Civil Procedure 26(c)(1) provides that \"[t]he court may, for "
        "good cause, issue an order to protect a party or person from annoyance, "
        "embarrassment, oppression, or undue burden or expense.\" The party seeking the "
        "protective order bears the burden of demonstrating good cause. Phillips ex rel. "
        "Estates of Byrd v. General Motors Corp., 307 F.3d 1206, 1210-11 (9th Cir. 2002). "
        "Good cause exists when \"specific prejudice or harm will result\" from the "
        "absence of a protective order. Foltz v. State Farm Mut. Auto. Ins. Co., 331 F.3d "
        "1122, 1130 (9th Cir. 2003)."
    )
    d.write_wrapped(FOLTZ_CROSS_USE)

    d.write_line("IV.  ARGUMENT", bold=True)
    d.write_line("A.  Good Cause Exists for Entry of a Protective Order", bold=True)
    d.write_wrapped(
        "The discovery materials at issue include clinical treatment records, counseling "
        "notes, information pertaining to sexual matters, psychological assessments, "
        "personnel files, proprietary treatment protocols, and insurance policy "
        "information. These categories of information are routinely afforded protection "
        "by courts. (Newanforbi Decl. ¶ 5.) Defendants themselves recognized the "
        "sensitivity of these materials by insisting on a protective order as a "
        "precondition to production in the State Action. (Newanforbi Decl. ¶ 3.)"
    )
    d.write_wrapped(
        "The Proposed Protective Order replicates, in all material respects, the "
        "protections that Defendants negotiated and agreed to in the State Action. "
        "Defendants will suffer no prejudice from its entry because the identical "
        "categories of information will be subject to the identical restrictions on "
        "disclosure. Indeed, Defendants' own prior conduct in stipulating to the State "
        "PO constitutes a concession that these protections are both necessary and "
        "sufficient."
    )
    d.write_line("B.  The Court Should Authorize Retention and Use of State-Court Materials",
                 bold=True)
    d.write_wrapped(
        "The 542 pages of documents produced in the State Action are directly relevant "
        "to — and in many instances essential for — the claims asserted in this action. "
        "The State Action and this action arise from the same blanket retention policy, "
        "the same Clinical Operational Manual, the same false reports to CDCR, the same "
        "retaliatory conduct, and the same institutional practices. Requiring Plaintiff "
        "to return or destroy these materials and then re-propound the identical "
        "discovery requests would impose unnecessary burden on all parties and the Court."
    )
    d.write_wrapped(FOLTZ_ARG_B)
    d.write_wrapped(
        "Here, there is no legitimate basis to prohibit cross-use. The materials are "
        "relevant. The parties are substantially overlapping. The Proposed Protective "
        "Order provides equivalent or greater protection than the State PO. And the "
        "State PO, by its own terms, does not authorize use of Confidential Information "
        "in this action — which is why an order of this Court is needed."
    )
    d.write_line("C.  The State PO's Return-or-Destroy Obligation Should Be Addressed",
                 bold=True)
    d.write_wrapped(
        "Section VIII of the State PO ties the sixty-day return-or-destroy obligation to "
        "the conclusion of the State Action or the Derrick action, whichever is later, "
        "and defines conclusion by reference to final judgment, settlement, or consent "
        "decree plus appeal time. The Proposed Protective Order addresses the "
        "interaction of that obligation with this action by staying return-or-destroy "
        "during the pendency of this case, provided that Plaintiff continues to treat "
        "the materials in accordance with the Order's confidentiality provisions. "
        "(Proposed Order § II.B.) This is the most efficient resolution for all parties "
        "and avoids the absurd result of destroying materials essential to this action "
        "only to re-propound the same discovery from the same defendants."
    )
    d.write_line("D.  Plaintiff Has Acted in Good Faith and Transparency", bold=True)
    d.write_wrapped(
        "Plaintiff has not attached any state-court discovery documents as exhibits to "
        "the Complaint, has not disclosed the contents of any documents designated as "
        "Confidential, and has referenced only facts — not documents — in the "
        "Complaint's factual allegations. Rather than attempting to use the materials "
        "without authorization and risk a sanctions dispute, Plaintiff puts the issue "
        "before the Court and asks for an orderly resolution."
    )

    d.write_line("V.  CONCLUSION", bold=True)
    d.write_wrapped(
        "For the foregoing reasons, Plaintiff respectfully requests that the Court grant "
        "this Renewed Motion and enter the [Proposed] Protective Order Re: Confidential "
        "Information, which will: (1) govern the use and disclosure of confidential "
        "discovery materials in this action; (2) authorize the retention and use of "
        "materials previously produced in the State Action, subject to equivalent "
        "protections; (3) stay the return-or-destroy obligation under the State PO during "
        "the pendency of this action; and (4) deem the state-court discovery materials "
        "produced in this action upon entry of the Order."
    )
    d.blank_line()
    d.write_line("Dated: August 9, 2026")
    d.blank_line()
    d.write_line("Respectfully submitted,", right=True, right_margin_offset=20)
    d.blank_line()
    d.write_line("___________________________________", right=True, right_margin_offset=20)
    d.write_line("BRENDAN NGEHSI NEWANFORBI", right=True, right_margin_offset=20)
    d.write_line("Plaintiff, In Pro Per", right=True, right_margin_offset=20)

    d.ensure_space(8)
    d.write_line("CERTIFICATE OF SERVICE", bold=True, center=True)
    d.blank_line()
    d.write_wrapped(
        "I, BRENDAN NGEHSI NEWANFORBI, declare under penalty of perjury under the laws "
        "of the United States of America that on August 9, 2026, I caused a true and "
        "correct copy of the foregoing RENEWED MOTION FOR PROTECTIVE ORDER RE: "
        "CONFIDENTIAL INFORMATION, together with the [Proposed] Protective Order Re: "
        "Confidential Information (cite-corrected draft), to be served upon the following "
        "by United States first-class mail, postage prepaid, and additionally by email:"
    )
    d.write_wrapped(
        "Defendant SHANNON SMITH (individually): c/o HOPE Psychotherapy, Inc., "
        "1245 B Street, Hayward, CA 94541"
    )
    d.write_wrapped(
        "Defendant HOPE PSYCHOTHERAPY, INC.: c/o Shannon Smith, CEO, "
        "1245 B Street, Hayward, CA 94541"
    )
    d.write_wrapped(
        "Counsel of Record (courtesy copy): Blaze Van Dine, Esq., "
        "SIMS, LAWRENCE & BROGHAMMER, 1478 Stone Point Drive, Suite 450, "
        "Roseville, CA 95661; Email: blaze@sims-law.net; SLB-eservice@sims-law.net"
    )
    d.blank_line()
    d.write_line("Executed on August 9, 2026, at Stockton, California.")
    d.blank_line()
    d.write_line("___________________________________", right=True, right_margin_offset=20)
    d.write_line("BRENDAN NGEHSI NEWANFORBI", right=True, right_margin_offset=20)
    d.write_line("Plaintiff, In Pro Per", right=True, right_margin_offset=20)
    d.save()


def build_proposed_order(path: Path) -> None:
    """Copy the filed proposed order and replace only the bad WHEREAS cites.

    The Condit/Dunford parenthetical wraps across two body lines on page 2.
    Redact those two lines in full and rewrite them with Foltz only, so no
    orphaned fragments remain.
    """
    doc = pymupdf.open(PROPOSED_SRC)
    page = doc[1]  # page 2 (0-indexed) holds the Condit/Dunford WHEREAS

    if not page.search_for("Condit v. Dunne") or not page.search_for("Dunford v. Rovi"):
        raise SystemExit("Could not locate Condit/Dunford cites on proposed-order page 2")

    # Exact body-line boxes from the filed PDF (word coords, Times ~11 pt).
    # Line A: "obtained in related litigation … (see Condit v. Dunne, 225"
    # Line B: "F.R.D. 100, 105 … 2015)),"
    line_a = pymupdf.Rect(104.0, 277.5, 580.0, 296.5)
    line_b = pymupdf.Rect(104.0, 301.5, 580.0, 320.5)
    page.add_redact_annot(line_a, fill=(1, 1, 1))
    page.add_redact_annot(line_b, fill=(1, 1, 1))
    page.apply_redactions()

    replacement = (
        "obtained in related litigation to avoid wasteful duplication of discovery (see\n"
        "Foltz v. State Farm Mut. Auto. Ins. Co., 331 F.3d 1122, 1131 (9th Cir. 2003)),"
    )
    # Single textbox covering both cleared lines; leading preserves left margin.
    combined = pymupdf.Rect(104.0, 277.5, 580.0, 320.5)
    rc = page.insert_textbox(
        combined,
        replacement,
        fontname="times-roman",
        fontsize=11,
        align=pymupdf.TEXT_ALIGN_LEFT,
    )
    if rc < 0:
        raise SystemExit(f"Foltz replacement did not fit proposed-order page 2 (rc={rc})")

    # Caption case number / judge blanks on page 1 (underscores are separate words).
    # insert_textbox often returns <0 on these narrow caption rows — use insert_text.
    page0 = doc[0]
    case_hits = page0.search_for("Case No.")
    blank_hits = page0.search_for("_______________")
    for ch in case_hits:
        if ch.y0 < 260:
            for bh in blank_hits:
                if abs(bh.y0 - ch.y0) < 5 and bh.x0 > ch.x0:
                    union = pymupdf.Rect(ch.x0, ch.y0 - 1, ch.x0 + 200, bh.y1 + 1)
                    page0.add_redact_annot(union, fill=(1, 1, 1))
                    page0.apply_redactions()
                    page0.insert_text(
                        (ch.x0, ch.y1 - 1),
                        f"Case No. {CASE_NO}",
                        fontname="times-bold",
                        fontsize=10,
                    )
                    break
            break
    for jh in page0.search_for("Judge:"):
        if jh.y0 < 340:
            for bh in page0.search_for("_______________"):
                if abs(bh.y0 - jh.y0) < 5 and bh.x0 > jh.x0:
                    union = pymupdf.Rect(jh.x0, jh.y0 - 1, jh.x0 + 220, bh.y1 + 1)
                    page0.add_redact_annot(union, fill=(1, 1, 1))
                    page0.apply_redactions()
                    page0.insert_text(
                        (jh.x0, jh.y1 - 1),
                        f"Judge: {JUDGE}",
                        fontname="times-roman",
                        fontsize=10,
                    )
                    break
            break

    doc.save(path)
    doc.close()


def verify_outputs() -> None:
    forbidden = [
        "Dunford",
        "Condit v. Dunne",
        "Condit",
        "2015 WL 13752958",
        "S.D.N.Y. 2004",
        "Rovi",
    ]
    for path in (MOTION_OUT, PROPOSED_OUT):
        doc = pymupdf.open(path)
        text = "\n".join(p.get_text() for p in doc)
        doc.close()
        for bad in forbidden:
            if bad in text:
                raise SystemExit(f"FAILED: {path.name} still contains {bad!r}")
        if "Foltz" not in text:
            raise SystemExit(f"FAILED: {path.name} missing Foltz")
        if "331 F.3d" not in text:
            raise SystemExit(f"FAILED: {path.name} missing Foltz reporter pin")
        if path == PROPOSED_OUT and CASE_NO not in text:
            raise SystemExit(f"FAILED: {path.name} missing case number {CASE_NO}")
        if path == PROPOSED_OUT and "Cisneros" not in text:
            raise SystemExit(f"FAILED: {path.name} missing judge name")
        print(f"OK {path.name}: no bad cites; Foltz present; {path.stat().st_size} bytes")


def main() -> None:
    OUT_DIR.mkdir(parents=True, exist_ok=True)
    build_motion(MOTION_OUT)
    build_proposed_order(PROPOSED_OUT)
    verify_outputs()
    print(f"Wrote:\n  {MOTION_OUT}\n  {PROPOSED_OUT}")


if __name__ == "__main__":
    main()
