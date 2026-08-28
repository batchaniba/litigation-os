"""Judicial Council SER-001 (Rev. Jan 1, 2026) fill helper.

Canonical blank: ``internal/public/documents/_form-library/ser001-blank-template.pdf``

Matter scripts import ``FIELDS`` (AcroForm names), ``fill_ser001``, and the
checkbox constants rather than copy-pasting the field map and pypdf write loop.
Optional page-4 signature uses ``signature_stamp.stamp_ser001_signature``.
"""
from __future__ import annotations

import sys
from pathlib import Path

from pypdf import PdfReader, PdfWriter
from pypdf.generic import NameObject

_SCRIPTS = Path(__file__).resolve().parent.parent
if str(_SCRIPTS) not in sys.path:
    sys.path.insert(0, str(_SCRIPTS))

from signature_stamp import stamp_ser001_signature  # noqa: E402

REPO_ROOT = Path(__file__).resolve().parents[3]
TEMPLATE_PATH = REPO_ROOT / "internal/public/documents/_form-library/ser001-blank-template.pdf"
MIN_TEMPLATE_BYTES = 10_000

# AcroForm checkbox export values on this revision of SER-001.
CB_PERSON = NameObject("/1")  # item 3a person; description/safety "no"
CB_ENTITY = NameObject("/2")  # item 3b entity/business; alt-service no; other-info yes
CB_HEARING = NameObject("/3")  # item 5c hearing yes; item 5d deadline yes

# Fully-qualified AcroForm names (Judicial Council SER-001 Rev. Jan 1, 2026).
FIELDS = {
    "case1": "SER-001[0].Page1[0].CaptionRight[0].CaseNo[0].CaseNumber[0]",
    "county": "SER-001[0].Page1[0].List1[0].Li1[0].NameofCounty[0]",
    "yourname": "SER-001[0].Page1[0].List2[0].Li2a[0].Yourname[0]",
    "casename": "SER-001[0].Page1[0].List2[0].Li2c[0].TextField[0]",
    "address": "SER-001[0].Page1[0].List2[0].Li2d[0].address\\.2d[0]",
    "city": "SER-001[0].Page1[0].List2[0].Li2d[0].city\\.2d[0]",
    "state": "SER-001[0].Page1[0].List2[0].Li2d[0].state\\.2d[0]",
    "zip": "SER-001[0].Page1[0].List2[0].Li2d[0].zip\\.2d[0]",
    "phone": "SER-001[0].Page1[0].List2[0].Li2d[0].telephone\\.2d[0]",
    "email": "SER-001[0].Page1[0].List2[0].Li2d[0].email\\.2d[0]",
    "serve_person": "SER-001[0].Page2[0].List3[0].Li3a[0].servePerson[0]",
    "person_name": "SER-001[0].Page2[0].List3[0].Li3a[0].Li3aList[0].Li3a1[0].personName[0]",
    "nicknames": "SER-001[0].Page2[0].List3[0].Li3a[0].Li3aList[0].Li3a1[0].nicknames[0]",
    "desc_no": "SER-001[0].Page2[0].List3[0].Li3a[0].Li3aList[0].Li3a3[0].Description[0]",
    "safety_no": "SER-001[0].Page2[0].List3[0].Li3a[0].Li3aList[0].Li3a4[0].SafetyAccessibility[0]",
    "serve_entity": "SER-001[0].Page2[0].List3[0].Li3b[0].servePerson[0]",
    "entity_name": "SER-001[0].Page2[0].List3[0].Li3b[0].Li3bList[0].Li3b1[0].NameType[0]",
    "entity_person": "SER-001[0].Page2[0].List3[0].Li3b[0].Li3bList[0].Li3b2[0].nameofperson[0]",
    "entity_agent": "SER-001[0].Page2[0].List3[0].Li3b[0].Li3bList[0].Li3b3[0].nameofagent[0]",
    "case2": "SER-001[0].Page2[0].PxCaption[0].CaseNumber[0]",
    "addr": "SER-001[0].Page3[0].List4[0].Li4[0].Address[0]",
    "addr_city": "SER-001[0].Page3[0].List4[0].Li4[0].City[0]",
    "addr_state": "SER-001[0].Page3[0].List4[0].Li4[0].State[0]",
    "addr_zip": "SER-001[0].Page3[0].List4[0].Li4[0].Zip[0]",
    "business": "SER-001[0].Page3[0].List4[0].Li4[0].addDef[1]",
    "serve_time": "SER-001[0].Page3[0].List4[0].Li4[0].serveTime[0]",
    "gate": "SER-001[0].Page3[0].List4[0].Li4[0].gateCode[0]",
    "type_papers": "SER-001[0].Page3[0].List5[0].Li5a[0].typePapers[0]",
    "list_forms": "SER-001[0].Page3[0].List5[0].Li5b[0].listForms[0]",
    "hearing_yes": "SER-001[0].Page3[0].List5[0].Li5c[0].Hearing[2]",
    "hearing_date": "SER-001[0].Page3[0].List5[0].Li5c[0].hearingDate[0]",
    "case3": "SER-001[0].Page3[0].PxCaption[0].CaseNumber[0]",
    "deadline_yes": "SER-001[0].Page4[0].List5Continued[0].Li5d[0].deadline[2]",
    "deadline_date": "SER-001[0].Page4[0].List5Continued[0].Li5d[0].deadlineDate[0]",
    "alt_no": "SER-001[0].Page4[0].List5Continued[0].Li5e[0].altService[1]",
    "oth_yes": "SER-001[0].Page4[0].List5Continued[0].Li5f[0].othInfo[1]",
    "oth_text": "SER-001[0].Page4[0].List5Continued[0].Li5f[0].TextField[0]",
    "case4": "SER-001[0].Page4[0].PxCaption[0].CaseNumber[0]",
    "sig_date": "SER-001[0].Page4[0].sig[0].SigDate[0]",
    "type_name": "SER-001[0].Page4[0].sig[0].typeName[0]",
    "case5": "SER-001[0].Page5[0].PxCaption[0].CaseNumber[0]",
}
F = FIELDS


def require_template(path: Path | None = None) -> Path:
    """Return the blank SER-001, or exit if missing / Git-LFS pointer."""
    template = path or TEMPLATE_PATH
    if not template.is_file():
        raise SystemExit(f"Missing template: {template}")
    size = template.stat().st_size
    if size < MIN_TEMPLATE_BYTES:
        raise SystemExit(f"Template looks like an LFS pointer ({size} bytes): {template}")
    return template


def filled_values(path: Path | str) -> dict[str, object]:
    """AcroForm values that are actually filled (not empty / Off)."""
    fields = PdfReader(str(path)).get_fields() or {}
    return {
        k: v.get("/V")
        for k, v in fields.items()
        if v.get("/V") not in (None, "", NameObject("/Off"), "/Off")
    }


def fill_ser001(
    out: Path | str,
    fields: dict[str, object],
    *,
    stamp_signature: bool = False,
    template: Path | None = None,
) -> Path:
    """Fill ``fields`` onto a copy of the blank SER-001 and write ``out``."""
    blank = require_template(template)
    out_path = Path(out)
    out_path.parent.mkdir(parents=True, exist_ok=True)
    reader = PdfReader(str(blank))
    writer = PdfWriter()
    writer.append(reader)
    writer.update_page_form_field_values(None, fields)
    if writer.get_fields():
        try:
            writer.set_need_appearances_writer(True)
        except Exception:
            pass
    with open(out_path, "wb") as fh:
        writer.write(fh)
    if stamp_signature:
        stamp_ser001_signature(out_path)
    return out_path
