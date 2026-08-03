#!/usr/bin/env python3
"""Fill Matter 22 CIV-110 Request for Dismissal and CM-200 Notice of Settlement.

Execution / signature date: August 3, 2026 (per plaintiff).
Settlement date on CM-200: July 14, 2026 (DocuSign countersignature).
"""

from __future__ import annotations

from pathlib import Path

import fitz
from pypdf import PdfReader, PdfWriter
from pypdf.generic import NameObject

from signature_stamp import SIGNATURE_PATH, SIGNATURE_ASPECT

ROOT = Path(__file__).resolve().parents[2]
UPLOADS = Path("/home/ubuntu/.cursor/projects/workspace/uploads")
OUT_DIR = ROOT / "internal/public/documents/matter-22"

CIV_SRC = UPLOADS / "civ110_3_c8f8.pdf"
CM_SRC = UPLOADS / "cm200_9995.pdf"

CIV_OUT = OUT_DIR / (
    "CIV-110 Request for Dismissal - Entire Action With Prejudice "
    "(Pilot, Executed Aug 3 2026).pdf"
)
CM_OUT = OUT_DIR / (
    "CM-200 Notice of Settlement of Entire Case "
    "(Pilot, Executed Aug 3 2026).pdf"
)

CASE = "STK-CV-UWT-2026-0007649"
PLAINTIFF = "BRENDAN NGEHSI NEWANFORBI"
DEFENDANT = "PILOT TRAVEL CENTERS LLC"
NAME = "Brendan Ngehsi Newanforbi"
STREET = "1455 Cat Tail Drive"
CITY = "Stockton"
STATE = "CA"
ZIP = "95204"
PHONE = "(209) 801-4442"
EMAIL = "bnn.cdl@gmail.com"
ATTY_FOR = "Plaintiff in pro per"

COURT_COUNTY = "SAN JOAQUIN"
COURT_STREET = "180 E Weber Avenue"
COURT_MAIL = "180 E Weber Avenue"
COURT_CITYZIP = "Stockton, CA 95202"
COURT_BRANCH = "Stockton Courthouse"

EXEC_DATE = "August 3, 2026"
SETTLE_DATE = "July 14, 2026"
FILED_DATE = "May 29, 2026"


def fill_pdf(src: Path, out: Path, fields: dict) -> None:
    reader = PdfReader(str(src))
    writer = PdfWriter()
    writer.append(reader)
    writer.update_page_form_field_values(None, fields)
    try:
        writer.set_need_appearances_writer(True)
    except Exception:
        pass
    out.parent.mkdir(parents=True, exist_ok=True)
    with out.open("wb") as fh:
        writer.write(fh)


def stamp_signature(path: Path, page_index: int, x0: float, x1: float, y_line: float) -> None:
    doc = fitz.open(str(path))
    page = doc[page_index]
    width = x1 - x0
    height = width * SIGNATURE_ASPECT
    rect = fitz.Rect(x0, y_line - height, x1, y_line)
    page.insert_image(rect, filename=SIGNATURE_PATH, keep_proportion=True)
    doc.saveIncr()
    doc.close()


def civ_fields() -> dict:
    P = "CIV-110[0].Page1[0]"
    P2 = "CIV-110[0].Page2[0]"
    return {
        f"{P}.p1Caption[0].CaptionSub[0].CaseNumber[0].CaseNumber[0]": CASE,
        f"{P}.p1Caption[0].AttyPartyInfo[0].Name[0]": NAME,
        f"{P}.p1Caption[0].AttyPartyInfo[0].Street[0]": STREET,
        f"{P}.p1Caption[0].AttyPartyInfo[0].City[0]": CITY,
        f"{P}.p1Caption[0].AttyPartyInfo[0].State[0]": STATE,
        f"{P}.p1Caption[0].AttyPartyInfo[0].Zip[0]": ZIP,
        f"{P}.p1Caption[0].AttyPartyInfo[0].Phone[0]": PHONE,
        f"{P}.p1Caption[0].AttyPartyInfo[0].Email[0]": EMAIL,
        f"{P}.p1Caption[0].AttyPartyInfo[0].AttyFor[0]": ATTY_FOR,
        f"{P}.p1Caption[0].CourtInfo[0].CrtCounty[0]": COURT_COUNTY,
        f"{P}.p1Caption[0].CourtInfo[0].CrtStreet[0]": COURT_STREET,
        f"{P}.p1Caption[0].CourtInfo[0].CrtMailingAdd[0]": COURT_MAIL,
        f"{P}.p1Caption[0].CourtInfo[0].CrtCityZip[0]": COURT_CITYZIP,
        f"{P}.p1Caption[0].CourtInfo[0].CrtBranch[0]": COURT_BRANCH,
        f"{P}.p1Caption[0].TitlePartyName[0].Party1[0]": PLAINTIFF,
        f"{P}.p1Caption[0].TitlePartyName[0].Party2[0]": DEFENDANT,
        # 1a(1) with prejudice; 1b(1) complaint; 1b(5) entire action
        f"{P}.List1[0].li1a[0].List1[0].li1a1[0].RB1Choices[0]": NameObject("/1"),
        f"{P}.List1[0].LI1b[0].li1b[0].li1b1[0].RB3Choices1[0]": NameObject("/1"),
        f"{P}.List1[0].LI1b[0].li1b[0].li1b5[0].RB2Choices[0]": NameObject("/1"),
        # Item 2 — court DID waive fees
        f"{P}.List2[0].DateTimeField1[0]": EXEC_DATE,
        f"{P}.List2[0].CheckBox2D[0]": NameObject("/1"),
        f"{P}.List2[0].Sig1Name[0]": NAME,
        f"{P}.List2[0].CheckBox2A[1]": NameObject("/2"),
        f"{P}.List2[0].RB2Choice2[0]": NameObject("/Yes"),
        # Page 2 — fee-waiver recovery declaration ($35k settlement)
        f"{P2}.PxCaption[0].TitlePartyName[0].Party1[0]": PLAINTIFF,
        f"{P2}.PxCaption[0].TitlePartyName[0].Party2[0]": DEFENDANT,
        f"{P2}.PxCaption[0].CaseNumber[0].CaseNumber[0]": CASE,
        f"{P2}.Item1[0].FillText109[0]": NAME,
        f"{P2}.List2[0].li2c[0].CBCourtFee[0]": NameObject("/3"),
        # Item 3 No — waived fees not yet repaid; enclose money order before flipping to Yes
        f"{P2}.Item3[0].Yes[0]": NameObject("/2"),
        f"{P2}.PoP[0].DateTimeField1[0]": EXEC_DATE,
        f"{P2}.PoP[0].YourName2[0]": NAME,
        f"{P2}.PoP[0].CheckBox4A[0]": NameObject("/2"),
    }


def cm_fields() -> dict:
    P = "CM-200[0].Page1[0]"
    P2 = "CM-200[0].Page2[0]"
    atty_block = (
        f"{NAME}\n"
        f"{STREET}\n"
        f"{CITY}, {STATE} {ZIP}"
    )
    return {
        f"{P}.P1Caption[0].CaseNumber[0].CaseNumber[0]": CASE,
        f"{P}.P1Caption[0].AttyPartyInfo[0].Add1[0]": atty_block,
        f"{P}.P1Caption[0].AttyPartyInfo[0].Phone[0]": PHONE,
        f"{P}.P1Caption[0].AttyPartyInfo[0].Email[0]": EMAIL,
        f"{P}.P1Caption[0].AttyPartyInfo[0].AttyFor[0]": ATTY_FOR,
        f"{P}.P1Caption[0].CourtInfo[0].CrtCounty[0]": COURT_COUNTY,
        f"{P}.P1Caption[0].CourtInfo[0].CrtStreet[0]": COURT_STREET,
        f"{P}.P1Caption[0].CourtInfo[0].CrtMailingAdd[0]": COURT_MAIL,
        f"{P}.P1Caption[0].CourtInfo[0].CrtCityZip[0]": COURT_CITYZIP,
        f"{P}.P1Caption[0].CourtInfo[0].CrtBranch[0]": COURT_BRANCH,
        f"{P}.P1Caption[0].TitlePartyName[0].Party1[0]": PLAINTIFF,
        f"{P}.P1Caption[0].TitlePartyName[0].Party2[0]": DEFENDANT,
        # 1a Unconditional; settlement date; filed date; no trial date
        f"{P}.List[0].List1[0].Lia[0].conditional[0]": NameObject("/1"),
        f"{P}.List[0].List1[0].Lia[0].DateField1[0]": SETTLE_DATE,
        f"{P}.List[0].List2[0].item2[0].DateField3[0]": FILED_DATE,
        f"{P}.List[0].List4[0].Lia[0].Ch4[0]": NameObject("/2"),
        f"{P}.PoPDec[0].SigDate[0]": EXEC_DATE,
        f"{P}.PoPDec[0].PrintName[0]": NAME,
        f"{P}.PoPDec[0].ch10[1]": NameObject("/2"),
        # Page 2 caption only — POS left blank (party cannot self-serve)
        f"{P2}.PxCaption[0].TitlePartyName[0].Party1[0]": PLAINTIFF,
        f"{P2}.PxCaption[0].TitlePartyName[0].Party2[0]": DEFENDANT,
        f"{P2}.PxCaption[0].CaseNumber[0].CaseNumber[0]": CASE,
    }


def main() -> None:
    fill_pdf(CIV_SRC, CIV_OUT, civ_fields())
    fill_pdf(CM_SRC, CM_OUT, cm_fields())

    # Signature stamps on the signature lines (not the typed-name fields).
    # CIV-110 p1 item 2 (~y 468); CIV-110 p2 declaration (~y 368); CM-200 p1 (~y 702)
    stamp_signature(CIV_OUT, 0, 330, 540, 468)
    stamp_signature(CIV_OUT, 1, 330, 540, 368)
    stamp_signature(CM_OUT, 0, 330, 540, 702)

    print(f"Wrote {CIV_OUT.name}")
    print(f"Wrote {CM_OUT.name}")


if __name__ == "__main__":
    main()
