#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Matter 40 — N.D. Cal. case-opening papers for Ngwa Nforbi v. Uber.

Builds, dated and signed:

  1. JS-CAND 44 Civil Cover Sheet (pro se form, Rev. 04-2025);
  2. Consent or Declination to Magistrate Judge Jurisdiction — CONSENT;
  3. Plaintiff's Civil L.R. 3-15 Certification of Conflicts and Interested
     Entities or Persons;
  4. AO 440 Summons in a Civil Action (proposed, for issuance) — one each
     for Uber Technologies, Inc., TaskUs Holdings, Inc., TaskUs USA, LLC;
  5. AO 240 IFP application (short form), with --ao240 — mirrors the Serrato
     application answer for answer at Plaintiff's direction;
  6. Complete Filing Packet — cover sheet, complaint, IFP, consent, 3-15,
     summonses, in that order.

The complaint itself is matter40-uber-complaint.py (run it first).

Cover-sheet name order follows the JS-CAND 44 instruction (Last, First).
Nature of Suit 480 (Consumer Credit) is the JS-44 code for FCRA claims.
Division: San Jose — the complaint pleads Santa Clara County under Civil
L.R. 3-2(c), (e).

    python3 internal/scripts/matter40-ndcal-filing-packet.py \\
        --js-cand /path/to/JS-CAND-44_fillable_04-2025.pdf \\
        --ao240 /path/to/ao240.pdf
"""

from __future__ import annotations

import argparse
import sys
from pathlib import Path

SCRIPT_DIR = Path(__file__).resolve().parent
sys.path.insert(0, str(SCRIPT_DIR / "lib"))
sys.path.insert(0, str(SCRIPT_DIR))

import fitz  # noqa: E402

from pleading_paper import CONTENT_LEFT, PleadingPaper  # noqa: E402
from signature_stamp import (  # noqa: E402
    SIGNATURE_NATIVE_PX,
    SIGNATURE_PATH,
    stamp_on_pdf_line,
)

ROOT = SCRIPT_DIR.parents[1]
FORMS = ROOT / "internal/public/documents/_form-library"
OUT_DIR = ROOT / "internal/public/documents/matter-40"

EXEC_DATE = "September 23, 2026"
EXEC_DATE_NUM = "09/23/2026"
TAG = "(N.D. Cal.) (Sep 23 2026)"

PLAINTIFF_CAPS = "BRENDAN NGWA NFORBI"
PLAINTIFF_MIXED = "Brendan Ngwa Nforbi"
PLAINTIFF_LAST_FIRST = "Ngwa Nforbi, Brendan"
ADDRESS_LINES = ["1455 Cat Tail Drive", "Stockton, CA 95204", "(209) 801-4442"]
DEFENDANTS_SHORT = "UBER TECHNOLOGIES, INC., et al."
DEFENDANTS_FULL = (
    "UBER TECHNOLOGIES, INC.; TASKUS HOLDINGS, INC.; "
    "TASKUS USA, LLC; and DOES 1 through 20, inclusive"
)

# Service addresses are the California agents for service of process (CA SOS:
# Uber Technologies, Inc. No. 3318029; TaskUs Holdings, Inc. No. 3828721;
# TaskUs USA, LLC No. 201729810166 -- all C T Corporation System, Glendale).
# Confirm each on bizfile before the clerk issues the summonses.
SUMMONS_TARGETS = [
    {
        "slug": "Uber Technologies Inc",
        "address": [
            "Uber Technologies, Inc.",
            "c/o C T Corporation System, Registered Agent",
            "330 N. Brand Blvd., Suite 700",
            "Glendale, CA 91203",
        ],
    },
    {
        "slug": "TaskUs Holdings Inc",
        "address": [
            "TaskUs Holdings, Inc.",
            "c/o C T Corporation System, Registered Agent",
            "330 N. Brand Blvd., Suite 700",
            "Glendale, CA 91203",
        ],
    },
    {
        "slug": "TaskUs USA LLC",
        "address": [
            "TaskUs USA, LLC",
            "c/o C T Corporation System, Registered Agent",
            "330 N. Brand Blvd., Suite 700",
            "Glendale, CA 91203",
        ],
    },
]

SIG_LINE = "___________________________________"


def _out(name: str) -> Path:
    OUT_DIR.mkdir(parents=True, exist_ok=True)
    return OUT_DIR / f"{name} - Ngwa Nforbi v Uber Technologies Inc {TAG}.pdf"


def _set(w, value, size: float | None = None) -> None:
    if size is not None:
        w.text_fontsize = size
    w.field_value = value
    w.update()


# ---------------------------------------------------------------- JS-CAND 44
def build_cover_sheet(src: Path) -> Path:
    out = _out("Civil Cover Sheet JS-CAND 44")
    doc = fitz.open(src)
    page = doc[0]
    text = {
        "Plaintiff": (PLAINTIFF_LAST_FIRST, 10),
        "County_of_Residence_P1": ("San Joaquin", 9),
        "Plaintiff's Attorney(s)": (
            "Ngwa Nforbi, Brendan (pro se), 1455 Cat Tail Drive, "
            "Stockton, CA 95204; (209) 801-4442",
            8,
        ),
        "Defendant": (
            "Uber Technologies, Inc.; TaskUs Holdings, Inc.; "
            "TaskUs USA, LLC; Does 1-20",
            8.5,
        ),
        "County_of_Residence_of_D1": ("San Francisco", 9),
        "Defendant's Attorney(s) (If Known)": ("Unknown", 9),
        "Cause of Action": (
            "15 U.S.C. § 1681b(b)(2)(A), (b)(3)(A) (Fair Credit Reporting Act)",
            7.5,
        ),
        "Description of case": (
            "FCRA employment-screening disclosure / pre-adverse-action violations",
            6.5,
        ),
        "Related Case Information": ("None", 9),
        "Today's Date": (EXEC_DATE_NUM, 9),
        "Signature of Attorney of Record": ("", None),
        "Demand": ("", None),
    }
    radios = {
        "Group4": "Choice2",   # II. Federal Question
        "Group5": "Choice54",  # IV. 480 Consumer Credit (FCRA)
        "Group3": "1",         # IX. San Jose
    }
    checks = {"V.Origin": "1", "Jury demand": "1"}
    sig_rect = None
    for w in page.widgets():
        name = w.field_name
        if name in text:
            value, size = text[name]
            _set(w, value, size)
            if name == "Signature of Attorney of Record":
                sig_rect = fitz.Rect(w.rect)
        elif name in radios:
            if w.on_state() == radios[name]:
                w.field_value = w.on_state()
                w.update()
        elif name in checks:
            if str(w.on_state()) == checks[name]:
                w.field_value = w.on_state()
                w.update()
    for w in list(page.widgets()):
        if w.field_name.startswith("Button."):
            page.delete_widget(w)
    doc.bake(annots=True, widgets=True)
    if sig_rect is None:
        raise SystemExit("JS-CAND 44: signature field not found")
    stamp_on_pdf_line(
        page, sig_rect.x0 + 40, sig_rect.x0 + 150, sig_rect.y1 - 1, whiteout=False
    )
    doc.save(out, garbage=4, deflate=True)
    doc.close()
    return out


# ------------------------------------------------------- Magistrate consent
DATE_BASELINE = 566.4
PROSE_BASELINE = 631.8
CONSENT_SIG_LINE = (350.0, 520.0, 596.4)


def build_consent() -> Path:
    out = _out("Consent to Magistrate Judge Jurisdiction")
    doc = fitz.open(FORMS / "ndcal-mj-consent-declination-blank-template.pdf")
    page = doc[0]
    for w in page.widgets():
        name = w.field_name
        if name == "Plaintiff Name(s)":
            w.text_fontname = "tiro"
            _set(w, PLAINTIFF_CAPS, 9)
        elif name == "Defendant Name(s)":
            w.text_fontname = "tiro"
            _set(w, DEFENDANTS_SHORT, 9)
        elif name == "Case number":
            _set(w, "", None)
        elif name == "Consent to Magistrate Judge Jurisdiction":
            w.field_value = w.on_state()
            w.update()
        elif name == "Decline Magistrate Judge Jurisdiction":
            w.field_value = "Off"
            w.update()
        elif name in {"DATE", "YEAR", "NAME", "ProSe", "sig"}:
            _set(w, "", None)
    for w in list(page.widgets()):
        if w.field_name == "Reset Form":
            page.delete_widget(w)
    doc.bake(annots=True, widgets=True)
    date_part, _, year = EXEC_DATE.rpartition(",")
    for text, x, y, size in [
        (date_part.strip(), 116.0, DATE_BASELINE, 10),
        (year.strip()[-2:], 228.5, DATE_BASELINE, 10),
        (PLAINTIFF_MIXED, 348.0, DATE_BASELINE, 9),
        ("PRO SE", 348.0, PROSE_BASELINE, 10),
    ]:
        page.insert_text(fitz.Point(x, y), text, fontsize=size, fontname="tiro")
    stamp_on_pdf_line(page, *CONSENT_SIG_LINE, whiteout=False)
    doc.save(out, garbage=4, deflate=True)
    doc.close()
    return out


# ------------------------------------------------ Civil L.R. 3-15 certificate
def build_certification() -> Path:
    out = _out("Certification of Conflicts and Interested Entities or Persons")
    d = PleadingPaper(
        str(out),
        doc_title_footer=(
            "PLAINTIFF'S CIVIL L.R. 3-15 CERTIFICATION -- "
            "NGWA NFORBI v. UBER TECHNOLOGIES, INC., ET AL."
        ),
    )
    c = d.c
    top = d._line_y(0)
    for i, (txt, font) in enumerate(
        [(PLAINTIFF_CAPS, "Times-Bold"), ("Plaintiff, In Propria Persona", "Times-Roman")]
        + [(line, "Times-Roman") for line in ["1455 Cat Tail Drive", "Stockton, California 95204",
                                               "Telephone: (209) 801-4442",
                                               "E-mail: bnn.cdl@gmail.com"]]
    ):
        c.setFont(font, 12)
        c.drawString(CONTENT_LEFT, top - i * 15, txt)
    d.current_line = 4
    d.blank_line()
    d.write_line("UNITED STATES DISTRICT COURT", bold=True, center=True)
    d.write_line("NORTHERN DISTRICT OF CALIFORNIA", bold=True, center=True)
    d.blank_line()
    d.draw_caption_block(
        [
            ("BRENDAN NGWA NFORBI,", True, False),
            ("", False, False),
            ("                          Plaintiff,", False, False),
            ("", False, False),
            ("       v.", False, False),
            ("", False, False),
            ("UBER TECHNOLOGIES, INC.; TASKUS", True, False),
            ("HOLDINGS, INC.; TASKUS USA, LLC;", True, False),
            ("and DOES 1 through 20, inclusive,", True, False),
            ("", False, False),
            ("                          Defendants.", False, False),
        ],
        [
            ("Case No. _________________", False, False),
            ("", False, False),
            ("PLAINTIFF'S CERTIFICATION OF", True, False),
            ("CONFLICTS AND INTERESTED", True, False),
            ("ENTITIES OR PERSONS", True, False),
            ("", False, False),
            ("[Civil L.R. 3-15]", False, True),
        ],
        caption_size=9.0,
        tight_lh=11.0,
        boxed=True,
    )
    d.blank_line()
    d.write_wrapped(
        "Pursuant to Civil L.R. 3-15, the undersigned certifies that as of this "
        "date, there is no conflict or interest (other than the named parties) "
        "to report.",
        first_indent=36,
    )
    d.blank_line()
    d.write_wrapped(
        "Plaintiff is a natural person appearing in propria persona. He has no "
        "parent corporation, no publicly held corporation owns any interest in "
        "him, and no person or entity is funding the prosecution of this action "
        "or has a financial interest in its outcome. This action is not in "
        "federal court on the basis of diversity of citizenship under 28 U.S.C. "
        "§ 1332(a).",
        first_indent=36,
    )
    d.blank_line()
    d.ensure_space(9)
    d.write_line(f"Dated: {EXEC_DATE}")
    d.write_line("Respectfully submitted,", right=True, right_margin_offset=20)
    d.draw_signature_image(
        SIGNATURE_PATH, SIGNATURE_NATIVE_PX[0], SIGNATURE_NATIVE_PX[1], SIG_LINE
    )
    d.write_line(SIG_LINE, right=True, right_margin_offset=20)
    d.write_line(PLAINTIFF_CAPS, right=True, right_margin_offset=20)
    d.write_line("Plaintiff, In Propria Persona", right=True, right_margin_offset=20)
    d.save()
    return out


# ------------------------------------------------------------- AO 440 summons
def build_summons(target: dict) -> Path:
    out = _out(f"Summons AO 440 - {target['slug']}")
    doc = fitz.open(FORMS / "ao440-blank-template.pdf")
    values = {
        "Dist.Info": ("        Northern District of California", None),
        "Plaintiff": (PLAINTIFF_CAPS, 10),
        "Defendant": (
            "UBER TECHNOLOGIES, INC.; TASKUS HOLDINGS, INC.; "
            "TASKUS USA, LLC; and DOES 1 through 20, inclusive",
            9,
        ),
        "Defendant address": ("\n".join(target["address"]), 10),
        "Plaintiff address": (
            "\n".join([PLAINTIFF_MIXED, "Plaintiff, In Propria Persona"] + ADDRESS_LINES),
            9,
        ),
    }
    for page in doc:
        for w in page.widgets():
            if page.number == 0 and w.field_name in values:
                value, size = values[w.field_name]
                _set(w, value, size)
        for w in list(page.widgets()):
            if w.field_name.startswith("Button."):
                page.delete_widget(w)
    doc.save(out, garbage=4, deflate=True)
    doc.close()
    return out


# ------------------------------------------------ AO 240 IFP (short form)
# Mirrors the Serrato application (Matter 24, ECF No. 2, granted ECF No. 5,
# Jun 29 2026) answer for answer, at Plaintiff's direction.
IFP_CASH = "105.00"


def build_ifp(src: Path) -> Path:
    out = _out("IFP Application AO 240")
    doc = fitz.open(src)
    text = {
        "Plaintiff": (PLAINTIFF_CAPS, 10),
        "Defendant": (DEFENDANTS_SHORT, 10),
        "Case_Num": ("", None),
        "Location held": ("N/A", 10),
        "Employer's name and address": ("N/A", 10),
        "Gross pay amount": ("N/A", 10),
        "Take-home pay amount": ("N/A", 10),
        "Specify pay period": ("N/A", 10),
        "Amount and source of other income": ("N/A", 10),
        "Amount of money in cash/checking/savings": (IFP_CASH, 10),
        "Value of property owned": ("None.", 10),
        "Monthly expenses": ("None.", 10),
        "Dependents, and how much paid for support": ("None.", 10),
        "Other financial debts or obligations": ("None.", 10),
        "Date2": (EXEC_DATE_NUM, 10),
        "Applicant'sSignature": ("", None),
        "Applican'tsNameTitle": (PLAINTIFF_MIXED, 10),
    }
    sig_rect = None
    for page in doc:
        for w in page.widgets():
            name = w.field_name
            if name == "District Information":
                w.field_value = "        Northern District of California"
                w.update()
            elif name in text:
                value, size = text[name]
                _set(w, value, size)
                if name == "Applicant'sSignature":
                    sig_rect = (page.number, fitz.Rect(w.rect))
            elif name.startswith("Check Box"):
                # Questions 3(a)-(f): every answer "No".
                w.field_value = w.on_state() if w.on_state() == "No" else "Off"
                w.update()
        for w in list(page.widgets()):
            if w.field_name.startswith("Button."):
                page.delete_widget(w)
    doc.bake(annots=True, widgets=True)
    if sig_rect is None:
        raise SystemExit("AO 240: signature field not found")
    pno, r = sig_rect
    stamp_on_pdf_line(doc[pno], r.x0 + 30, r.x0 + 170, r.y1 - 1, whiteout=False)
    doc.save(out, garbage=4, deflate=True)
    doc.close()
    return out


def main() -> None:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--js-cand", required=True, help="Blank JS-CAND 44 fillable PDF")
    ap.add_argument("--ao240", help="Blank AO 240 fillable PDF")
    args = ap.parse_args()
    outs = [
        build_cover_sheet(Path(args.js_cand)),
        build_consent(),
        build_certification(),
        *[build_summons(t) for t in SUMMONS_TARGETS],
    ]
    if args.ao240:
        outs.append(build_ifp(Path(args.ao240)))
    complaint = OUT_DIR / (
        "Complaint - Ngwa Nforbi v Uber Technologies Inc (N.D. Cal.)"
        " (Sep 23 2026).pdf"
    )
    if complaint.is_file():
        # cover sheet, complaint, [IFP], consent, 3-15, summonses
        order = [outs[0], complaint] + outs[6:7] + outs[1:6]
        packet = fitz.open()
        for part in order:
            with fitz.open(part) as src:
                packet.insert_pdf(src)
        pk = _out("Complete Filing Packet")
        packet.save(pk, garbage=4, deflate=True)
        packet.close()
        outs.append(pk)
    for o in outs:
        print(f"Generated: {o}")


if __name__ == "__main__":
    main()
