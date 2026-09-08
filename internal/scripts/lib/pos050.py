"""Judicial Council POS-050/EFS-050 (Rev. Feb. 1, 2017) fill helper.

Canonical blank: ``internal/public/documents/_form-library/pos050-blank-template.pdf``

Alameda rejected a federal four-sided-border Proof of Service on the
Matter 20 dashcam lodging (Sep. 8, 2026) for CRC 2.111 / JCC format.
This is the optional electronic-service form the clerk pointed to
(https://courts.ca.gov/forms-rules/court-forms). Text is drawn onto the
printed lines, not left in LiveCycle appearance streams.

    from pos050 import ProofOfElectronicService, fill_pos050
"""
from __future__ import annotations

import shutil
import sys
from dataclasses import dataclass, field
from pathlib import Path

import pymupdf

_SCRIPTS = Path(__file__).resolve().parent.parent
if str(_SCRIPTS) not in sys.path:
    sys.path.insert(0, str(_SCRIPTS))

from signature_stamp import SIGNATURE_NATIVE_PX, SIGNATURE_PATH  # noqa: E402

REPO_ROOT = Path(__file__).resolve().parents[3]
TEMPLATE_PATH = REPO_ROOT / "internal/public/documents/_form-library/pos050-blank-template.pdf"
MIN_TEMPLATE_BYTES = 10_000

# Right-hand "(SIGNATURE OF DECLARANT)" rule on POS-050 page 1.
SIG_LINE_Y = 694.2
SIG_X0 = 400.0
SIG_WIDTH = 155.0


@dataclass
class ProofOfElectronicService:
    """Values for one POS-050. Leave a string empty to skip that line."""

    name: str
    street: str
    city: str
    state: str
    zip_code: str
    phone: str
    email: str
    attorney_for: str
    county: str
    court_street: str
    court_mailing: str
    court_city_zip: str
    court_branch: str
    petitioner: str
    respondent: str
    case_number: str
    judicial_officer: str
    department: str
    residence_address: str
    server_e_address: str
    document_titles: list[str] = field(default_factory=list)
    person_served: str = ""
    on_behalf_of: str = ""
    person_e_address: str = ""
    service_date: str = ""
    signature_date: str = ""
    printed_name: str = ""
    stamp_signature: bool = True
    firm_name: str = ""
    fax: str = ""
    bar_no: str = ""


def require_template(path: Path | None = None) -> Path:
    template = path or TEMPLATE_PATH
    if not template.is_file():
        raise SystemExit(f"Missing template: {template}")
    size = template.stat().st_size
    if size < MIN_TEMPLATE_BYTES:
        raise SystemExit(f"Template looks like an LFS pointer ({size} bytes): {template}")
    return template


def _whiteout(page: pymupdf.Page, rect: pymupdf.Rect) -> None:
    page.draw_rect(rect, color=(1, 1, 1), fill=(1, 1, 1), width=0)


def _write_at(page: pymupdf.Page, x: float, baseline: float, text: str, fontsize: float) -> None:
    page.insert_text(
        (x, baseline),
        text,
        fontsize=fontsize,
        fontname="helv",
        color=(0, 0, 0),
    )


def _write_on_line(
    page: pymupdf.Page,
    rect: pymupdf.Rect,
    text: str,
    fontsize: float = 8.0,
    *,
    baseline_inset: float = 1.6,
    x_inset: float = 1.2,
) -> None:
    if not text:
        return
    width = pymupdf.get_text_length(text, fontname="helv", fontsize=fontsize)
    max_w = max(rect.width - x_inset - 1.0, 8)
    if width > max_w:
        fontsize = max(6.0, fontsize * (max_w / width))
    baseline = rect.y1 - baseline_inset
    if baseline - fontsize < rect.y0 - 0.4:
        baseline = rect.y0 + fontsize * 0.9
    _write_at(page, rect.x0 + x_inset, baseline, text, fontsize)


def _wrap(text: str, max_width: float, fontsize: float) -> list[str]:
    words = text.split()
    if not words:
        return []
    lines: list[str] = []
    current = words[0]
    for word in words[1:]:
        trial = f"{current} {word}"
        if pymupdf.get_text_length(trial, fontname="helv", fontsize=fontsize) <= max_width:
            current = trial
        else:
            lines.append(current)
            current = word
    lines.append(current)
    return lines


def _write_stack(
    page: pymupdf.Page,
    rect: pymupdf.Rect,
    lines: list[str],
    fontsize: float = 7.5,
) -> None:
    usable = [ln for ln in lines if ln]
    if not usable:
        return
    lead = fontsize + 1.4
    total_h = lead * (len(usable) - 1) + fontsize
    y = rect.y0 + max((rect.height - total_h) / 2, 0.4) + fontsize
    for ln in usable:
        _write_at(page, rect.x0 + 1.2, y, ln, fontsize)
        y += lead


def _widget_map(page: pymupdf.Page) -> dict[str, pymupdf.Rect]:
    found: dict[str, pymupdf.Rect] = {}
    for w in page.widgets() or []:
        name = w.field_name or ""
        found[name.split(".")[-1]] = pymupdf.Rect(w.rect)
    return found


def _drop_widgets(page: pymupdf.Page) -> None:
    for w in list(page.widgets() or []):
        page.delete_widget(w)


def _stamp_on_rule(page: pymupdf.Page, x0: float, y_rule: float, width: float) -> None:
    sw, sh = SIGNATURE_NATIVE_PX
    height = width * (sh / sw)
    # Sit the ink on the rule; do not punch through the label under it.
    bottom = y_rule + 1.5
    rect = pymupdf.Rect(x0, bottom - height, x0 + width, bottom)
    page.insert_image(rect, filename=SIGNATURE_PATH, keep_proportion=False)


def fill_pos050(
    out: Path | str,
    fields: ProofOfElectronicService,
    *,
    template: Path | None = None,
) -> Path:
    """Draw ``fields`` onto a copy of the blank POS-050 and write ``out``."""
    blank = require_template(template)
    out_path = Path(out)
    out_path.parent.mkdir(parents=True, exist_ok=True)
    shutil.copy2(blank, out_path)
    doc = pymupdf.open(str(out_path))
    page = doc[0]
    box = _widget_map(page)

    def line(suffix: str, text: str, fontsize: float = 8.0, **kwargs) -> None:
        if suffix in box and text:
            _write_on_line(page, box[suffix], text, fontsize, **kwargs)

    line("AttyName_ft[0]", fields.name)
    line("AttyBarNo_dc[0]", fields.bar_no)
    line("AttyFirm_ft[0]", fields.firm_name)
    line("AttyStreet_ft[0]", fields.street)
    line("AttyCity_ft[0]", fields.city)
    line("AttyState_ft[0]", fields.state)
    line("AttyZip_ft[0]", fields.zip_code)
    line("Phone_ft[0]", fields.phone)
    line("Fax_ft[0]", fields.fax)
    line("Email_ft[0]", fields.email)
    line("AttyFor_ft[0]", fields.attorney_for)

    line("CrtCounty_ft[0]", fields.county)
    line("Street_ft[0]", fields.court_street)
    line("MailingAdd_ft[0]", fields.court_mailing)
    line("CityZip_ft[0]", fields.court_city_zip)
    line("Branch_ft[0]", fields.court_branch, fontsize=7.5)

    line("Party1_ft[0]", fields.petitioner)
    line("Party2_ft[0]", fields.respondent)
    line("CaseNumber_ft[0]", fields.case_number)
    line("JudOfcr_ft[0]", fields.judicial_officer)
    line("Dept_ft[0]", fields.department)

    line("FillText18[0]", fields.residence_address)
    line("FillText19[0]", fields.server_e_address)

    if "FillText20[0]" in box and fields.document_titles:
        titles = [t.strip() for t in fields.document_titles if t.strip()]
        wrapped: list[str] = []
        max_w = box["FillText20[0]"].width - 4.0
        for title in titles:
            wrapped.extend(_wrap(title, max_w, 7.4))
        _write_stack(page, box["FillText20[0]"], wrapped, fontsize=7.4)

    line("FillText27[0]", fields.person_served, fontsize=7.5)
    line("FillText21[0]", fields.on_behalf_of, fontsize=7.5)
    line("FillText22[0]", fields.person_e_address)
    line("FillText23[0]", fields.service_date, fontsize=7.5)
    line("FillText25[0]", fields.signature_date, fontsize=7.5)
    line("FillText26[0]", fields.printed_name or fields.name)

    if fields.stamp_signature:
        if not Path(SIGNATURE_PATH).is_file():
            raise SystemExit(f"Missing signature: {SIGNATURE_PATH}")
        _stamp_on_rule(page, SIG_X0, SIG_LINE_Y, SIG_WIDTH)

    # JC "sign here" pointer on the signature rule.
    _whiteout(page, pymupdf.Rect(328.5, 674.5, 341.0, 695.5))
    # Adobe Print / Save / Clear chrome is not part of the filed form.
    _whiteout(page, pymupdf.Rect(0.0, 756.0, 612.0, 792.0))
    _drop_widgets(page)

    tmp = out_path.with_suffix(out_path.suffix + ".tmp")
    doc.save(str(tmp), garbage=4, deflate=True)
    doc.close()
    tmp.replace(out_path)
    return out_path
