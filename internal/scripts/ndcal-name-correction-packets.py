#!/usr/bin/env python3
"""N.D. Cal. name-correction packets — one docket name form for e-filing.

Plaintiff holds one PACER account (bngwanforbi; first name "Brendan", last
name "Ngwa Nforbi") but appears on five N.D. Cal. dockets under two name
forms. The CAND ECF Help Desk wrote on September 1, 2026 that it cannot
merge the accounts because "the case has to reflect what is listed on the
complaint," and that the fix is to ask each court to change the name on the
docket first, then request the merge.

This builds, per case: a Civil L.R. 7-11 administrative motion to correct
the docket name, a supporting declaration under 28 U.S.C. section 1746, a
proposed order, a proof of service, a combined packet, and a meet-and-confer
email draft for L.R. 7-11(a).

Nothing here changes a claim, a party, or a deadline. It is a docket-caption
correction so the plaintiff can e-file.

  python3 internal/scripts/ndcal-name-correction-packets.py

VERIFY BEFORE FILING (see VERIFY.txt written alongside the packets):
  * the exact party-name string on each docket (PACER party tab), and
  * the current case-number initials for 3:26-cv-08271, which the
    August 24, 2026 related-case order reassigned from Kang to Krishnan.
"""
from __future__ import annotations

import sys
from dataclasses import dataclass, field
from pathlib import Path

import fitz

SCRIPT_DIR = Path(__file__).resolve().parent
sys.path.insert(0, str(SCRIPT_DIR))
sys.path.insert(0, str(SCRIPT_DIR / "lib"))

from pdf_packet import assemble  # noqa: E402
from pleading_paper import CONTENT_LEFT, PleadingPaper  # noqa: E402
from proof_of_service import (  # noqa: E402
    ProofOfServiceFields,
    build_proof_of_service,
)
from signature_stamp import SIGNATURE_ASPECT, SIGNATURE_PATH  # noqa: E402

ROOT = SCRIPT_DIR.parent
EXEC_DATE = "September 9, 2026"
SERVICE_PLACE = "Stockton, California"

TARGET_NAME = "BRENDAN NGWA NFORBI"
TARGET_NAME_TC = "Brendan Ngwa Nforbi"
PACER_LOGIN = "bngwanforbi"
HELPDESK_DATE = "September 1, 2026"

ADDRESS = [
    "1455 Cat Tail Drive",
    "Stockton, CA 95204",
    "Telephone: (209) 801-4442",
    "E-mail: bnn.cdl@gmail.com",
]


@dataclass
class Case:
    matter: int
    case_no: str
    division: str
    judge: str
    short: str
    docket_name: str          # party name as it currently appears on the docket
    left_caption: list[str]   # defendant block lines, after the plaintiff rows
    recipients: list[str] = field(default_factory=list)
    emails: list[str] = field(default_factory=list)
    counsel_salutation: str = "Counsel"
    verify_note: str = ""

    @property
    def needs_change(self) -> bool:
        return self.docket_name != TARGET_NAME_TC

    @property
    def slug(self) -> str:
        return self.case_no.split("-cv-")[1].split("-")[0]


CASES = [
    Case(
        matter=24,
        case_no="4:26-cv-05953-ASK",
        division="OAKLAND DIVISION",
        judge="Hon. Ajay S. Krishnan",
        short="NFORBI v. SERRATO",
        docket_name="Brendan Ngehsi Newanforbi",
        left_caption=[
            "CAPTAIN G. SERRATO, in his",
            "individual and official capacities",
            "as Commander, Dublin Area,",
            "California Highway Patrol,",
        ],
        recipients=[
            "Haiyang A. Li, Deputy Attorney General",
            "Office of the Attorney General",
            "[COMPLETE BEFORE FILING — DAG Li's street address]",
            "Attorney for Defendant G. Serrato",
        ],
        emails=["Haiyang.Li@doj.ca.gov", "Andy.Marquez@doj.ca.gov"],
        counsel_salutation="Mr. Li",
    ),
    Case(
        matter=28,
        case_no="3:26-cv-07504-LJC",
        division="SAN FRANCISCO DIVISION",
        judge="Hon. Lisa J. Cisneros",
        short="NFORBI v. SMITH, ET AL.",
        docket_name="Brendan Ngehsi Newanforbi",
        left_caption=[
            "SHANNON SMITH, LCSW, individually",
            "and as Chief Executive Officer;",
            "HOPE PSYCHOTHERAPY, INC., d/b/a",
            "HOPE PROGRAM; and DOES 1-10,",
        ],
        verify_note="Confirm defense counsel of record before service.",
    ),
    Case(
        matter=29,
        case_no="3:26-cv-09249-ASK",
        division="SAN FRANCISCO DIVISION",
        judge="Hon. Ajay S. Krishnan",
        short="NFORBI v. AMAZON.COM SERVICES, LLC",
        docket_name="Brendan Ngehsi Newanforbi",
        left_caption=[
            "AMAZON.COM SERVICES, LLC;",
            "ACCURATE BACKGROUND, LLC;",
            "and DOES 1-10,",
        ],
        verify_note="Confirm counsel e-mail for Amazon and Accurate before service.",
    ),
    Case(
        matter=32,
        case_no="3:26-cv-08271-PHK",
        division="SAN FRANCISCO DIVISION",
        judge="Hon. Ajay S. Krishnan",
        short="NFORBI v. MEZA-GONZALEZ, ET AL.",
        docket_name="Nforbi",
        left_caption=[
            "SANTIAGO MEZA-GONZALEZ,",
            "individually; JOSE MELANO,",
            "individually; and DOES 1-10,",
        ],
        recipients=[
            "Haiyang A. Li, Deputy Attorney General",
            "Office of the Attorney General",
            "[COMPLETE BEFORE FILING — DAG Li's street address]",
            "Attorney for Defendants Meza-Gonzalez and Melano",
        ],
        emails=["Haiyang.Li@doj.ca.gov"],
        counsel_salutation="Mr. Li",
        verify_note=(
            "Case-number initials: the August 24, 2026 related-case order "
            "reassigned this action from Magistrate Judge Kang to Magistrate "
            "Judge Krishnan. Confirm the current initials on PACER and update "
            "the caption before filing."
        ),
    ),
    Case(
        matter=33,
        case_no="3:26-cv-08272-LJC",
        division="SAN FRANCISCO DIVISION",
        judge="Hon. Lisa J. Cisneros",
        short="NFORBI v. CANDELARIA, ET AL.",
        docket_name="Nforbi",
        left_caption=[
            "DIANA CANDELARIA, individually;",
            "STEVE GORDON, Director, California",
            "Department of Motor Vehicles, in his",
            "official capacity; and DOES 1-10,",
        ],
        verify_note="Confirm defense counsel of record before service.",
    ),
]

OUTDIR = ROOT / "public/documents/_ndcal-name-correction"


# ----------------------------------------------------------------- helpers
def _header(d: PleadingPaper, case: Case) -> None:
    c = d.c
    atty_y = d._line_y(0)
    lines = [(TARGET_NAME, "Times-Bold", 12)]
    if case.needs_change:
        lines.append((f"(docketed as {case.docket_name})", "Times-Italic", 11))
    lines.append(("Plaintiff, In Pro Per", "Times-Roman", 12))
    lines += [(t, "Times-Roman", 12) for t in ADDRESS]
    for i, (txt, fn, sz) in enumerate(lines):
        c.setFont(fn, sz)
        c.drawString(CONTENT_LEFT, atty_y - i * 14, txt)
    d.current_line = 5
    d.blank_line()
    d.write_line("UNITED STATES DISTRICT COURT", bold=True, center=True)
    d.write_line("NORTHERN DISTRICT OF CALIFORNIA", bold=True, center=True)
    d.write_line(case.division, bold=True, center=True)
    d.blank_line()


def _caption(d: PleadingPaper, case: Case, right_title: list[str]) -> None:
    left = [(f"{TARGET_NAME},", True, False), ("", False, False),
            ("                          Plaintiff,", False, False),
            ("", False, False), ("       v.", False, False),
            ("", False, False)]
    left += [(t, True, False) for t in case.left_caption]
    left += [("", False, False), ("                          Defendants.", False, False)]
    right = [(f"Case No. {case.case_no}", False, False), ("", False, False)]
    right += [(t, True, False) for t in right_title]
    right += [
        ("[Civil L.R. 7-11]", True, False),
        ("", False, False),
        (f"Judge: {case.judge}", False, False),
    ]
    d.draw_caption_block(left, right, caption_size=10, tight_lh=13, boxed=True)
    d.blank_line()


def _sign_block(d: PleadingPaper, case: Case) -> None:
    d.ensure_space(8)
    d.write_line(f"Dated: {EXEC_DATE}")
    d.write_line("Respectfully submitted,", italic=True)
    d.blank_line()
    d.write_line("___________________________________")
    d.write_line(TARGET_NAME, bold=True)
    if case.needs_change:
        d.write_line(f"(docketed as {case.docket_name})", italic=True, size=11)
    d.write_line("Plaintiff, In Pro Per")


def _stamp_sig(path: Path) -> None:
    doc = fitz.open(str(path))
    page = line = None
    for candidate in doc:
        hits = candidate.search_for("_______________________________")
        if hits:
            page, line = candidate, hits[-1]
            break
    if page is None:
        doc.close()
        return
    width = 135.0
    height = width * SIGNATURE_ASPECT
    y1 = line.y1 - 2.0
    rect = fitz.Rect(line.x0, y1 - height, line.x0 + width, y1)
    page.insert_image(rect, filename=SIGNATURE_PATH, keep_proportion=True)
    tmp = path.with_name(path.stem + ".signed.pdf")
    doc.save(tmp, garbage=4, deflate=True, incremental=False)
    doc.close()
    tmp.replace(path)


# ------------------------------------------------------------------ motion
def build_motion(path: Path, case: Case) -> None:
    d = PleadingPaper(str(path), doc_title_footer=f"ADMIN. MOTION TO CORRECT NAME -- {case.short}")
    _header(d, case)
    _caption(d, case, ["ADMINISTRATIVE MOTION", "TO CORRECT PLAINTIFF'S", "NAME ON THE DOCKET"])
    d.write_line("ADMINISTRATIVE MOTION TO CORRECT", bold=True, center=True)
    d.write_line("PLAINTIFF'S NAME ON THE DOCKET", bold=True, center=True)
    d.blank_line()
    d.write_wrapped("TO THE COURT, ALL PARTIES, AND THEIR COUNSEL OF RECORD:", first_indent=0)
    d.blank_line()
    d.write_wrapped(
        f"Plaintiff, appearing in propria persona, respectfully moves this Court "
        f"under Civil Local Rule 7-11 for an order correcting the docket to state "
        f"Plaintiff's name as \"{TARGET_NAME_TC},\" and directing the Clerk to "
        f"conform the CM/ECF party record accordingly. Plaintiff currently appears "
        f"on this docket as \"{case.docket_name}.\"",
        first_indent=0,
    )
    d.blank_line()
    d.write_line("I.  RELIEF REQUESTED AND WHY IT IS ADMINISTRATIVE", bold=True)
    d.blank_line()
    d.write_wrapped(
        "This motion asks only that the docket reflect a single, consistent form "
        "of Plaintiff's name. It does not add, drop, or substitute a party. It "
        "does not amend any claim, alter any allegation, or move any deadline. "
        "No party's rights or defenses are affected. Relief of this kind is "
        "administrative within the meaning of Civil Local Rule 7-11 and falls "
        "within the Court's inherent authority to manage its own docket.",
    )
    d.blank_line()
    d.write_wrapped(
        "Because no party is substituted, Federal Rule of Civil Procedure 25 is "
        "not implicated. Plaintiff is the same natural person before and after "
        "the requested correction.",
    )
    d.blank_line()
    d.write_line("II.  GROUNDS", bold=True)
    d.blank_line()
    d.write_wrapped(
        f"Plaintiff is one person who has been identified on court records under "
        f"two forms of the same name: \"Brendan Ngehsi Newanforbi\" and "
        f"\"{TARGET_NAME_TC}.\" Both forms appear across five actions now pending "
        f"in this District. Plaintiff maintains a single PACER account under the "
        f"login {PACER_LOGIN}, in which his first name is recorded as \"Brendan\" "
        f"and his last name as \"Ngwa Nforbi.\"",
    )
    d.blank_line()
    d.write_wrapped(
        f"On {HELPDESK_DATE}, Plaintiff asked the Court's ECF Help Desk to link "
        f"all five actions to that single account so that he could electronically "
        f"file. The Help Desk responded that it is \"unable to merge the two name "
        f"into one account since the case has to reflect what is listed on the "
        f"complaint,\" that \"[o]n each complaint, the name is different,\" and "
        f"that if Plaintiff \"wish[es] to change the names on the cases,\" he "
        f"\"may submit a request to the court to do so,\" after which the cases "
        f"may be merged into one e-filing account. That correspondence is "
        f"attached to the accompanying declaration as Exhibit A. This motion is "
        f"that request.",
    )
    d.blank_line()
    d.write_wrapped(
        "The practical consequence of the mismatch is concrete. Plaintiff is "
        "presently unable to electronically file in this action and must submit "
        "filings in paper or by mail, which delays the Court's receipt of his "
        "papers, increases his costs as an indigent pro se litigant, and creates "
        "avoidable risk of a filing arriving after a deadline. A single docket "
        "name form resolves it.",
    )
    d.blank_line()
    d.write_wrapped(
        "Consistency across the docket also serves the Court and the parties. "
        "Five related or coordinated actions currently identify the same "
        "plaintiff two different ways, which invites confusion in indexing, "
        "related-case administration, and service.",
    )
    d.blank_line()
    d.write_line("III.  CIVIL L.R. 7-11(a) STATEMENT", bold=True)
    d.blank_line()
    d.write_wrapped(
        "Civil Local Rule 7-11(a) requires that an administrative motion be "
        "accompanied by a stipulation or by a declaration explaining why a "
        "stipulation could not be obtained. Plaintiff's declaration, filed "
        "herewith, addresses that requirement.",
    )
    d.blank_line()
    d.write_line("IV.  ALTERNATIVE RELIEF", bold=True)
    d.blank_line()
    d.write_wrapped(
        "Should the Court conclude that the operative pleading's caption must be "
        "conformed rather than corrected clerically, Plaintiff requests, in the "
        "alternative, leave under Federal Rule of Civil Procedure 15(a)(2) to "
        "file a caption-only amended pleading under Rule 10(a) that changes "
        "nothing but the form of Plaintiff's name. Plaintiff does not seek to "
        "alter any allegation, claim, or party, and asks that any such amendment "
        "relate back and leave all existing deadlines undisturbed.",
    )
    d.blank_line()
    d.write_line("V.  CONCLUSION", bold=True)
    d.blank_line()
    d.write_wrapped(
        f"Plaintiff respectfully requests that the Court correct the docket to "
        f"state his name as \"{TARGET_NAME_TC}\" and direct the Clerk to conform "
        f"the CM/ECF party record.",
    )
    _sign_block(d, case)
    d.save()
    _stamp_sig(path)


# ------------------------------------------------------------- declaration
def build_declaration(path: Path, case: Case) -> None:
    d = PleadingPaper(str(path), doc_title_footer=f"DECLARATION ISO NAME CORRECTION -- {case.short}")
    _header(d, case)
    _caption(d, case, ["DECLARATION OF PLAINTIFF", "IN SUPPORT OF ADMINISTRATIVE", "MOTION TO CORRECT NAME"])
    d.write_line("DECLARATION OF PLAINTIFF", bold=True, center=True)
    d.blank_line()
    d.write_wrapped(f"I, {TARGET_NAME_TC}, declare:", first_indent=0)
    d.blank_line()
    items = [
        "I am the Plaintiff in this action and appear in propria persona. I have "
        "personal knowledge of the facts stated below and, if called as a witness, "
        "could and would testify competently to them.",

        f"I am one person. I have been identified on court records under two forms "
        f"of my name: \"Brendan Ngehsi Newanforbi\" and \"{TARGET_NAME_TC}.\" Both "
        f"refer to me. Neither is an alias adopted to obscure my identity, and I "
        f"have not used the variance to gain any advantage in this or any other "
        f"proceeding.",

        f"On this docket I am currently identified as \"{case.docket_name}.\"",

        f"I maintain a single PACER account under the login {PACER_LOGIN}. In that "
        f"account my first name is recorded as \"Brendan\" and my last name as "
        f"\"Ngwa Nforbi.\" My e-mail of record is bnn.cdl@gmail.com and my "
        f"telephone number is (209) 801-4442.",

        f"On {HELPDESK_DATE}, I wrote to the Court's ECF Help Desk asking that all "
        f"five of my pending actions in this District be linked to that single "
        f"account. The Help Desk replied the same day that it could not merge the "
        f"accounts because the case must reflect the name listed on the complaint, "
        f"and that I could submit a request to the court to change the names on the "
        f"cases, after which the cases could be merged into one e-filing account. "
        f"A true and correct copy of that exchange is attached as Exhibit A.",

        "Because of the mismatch, I cannot electronically file in this action. I "
        "must file in paper or by mail. I am indigent, have proceeded under fee "
        "waivers, and am presently without stable housing. Paper filing costs me "
        "postage and travel I can ill afford and delays the Court's receipt of my "
        "papers.",

        "I do not seek by this motion to change any claim, any allegation, any "
        "party, or any deadline. I ask only that the docket state one form of my "
        "name so that I may e-file.",
    ]
    if case.recipients:
        items.append(
            "Before filing, I wrote to counsel of record to ask whether they would "
            "stipulate to this correction. I have set out below what came of that "
            "request. [COMPLETE BEFORE FILING: state the date of the request and "
            "whether counsel stipulated, declined, or did not respond.]"
        )
    else:
        items.append(
            "[COMPLETE BEFORE FILING: state whether counsel of record has appeared "
            "and, if so, the date you asked for a stipulation and the response. If "
            "no defendant has appeared, say so — that is itself a sufficient "
            "explanation under Civil L.R. 7-11(a).]"
        )
    for i, text in enumerate(items, 1):
        d.ensure_space(4)
        d.write_wrapped(f"{i}.  {text}")
        d.blank_line()
    d.ensure_space(6)
    d.write_wrapped(
        "I declare under penalty of perjury under the laws of the United States "
        "of America that the foregoing is true and correct. Executed on "
        f"{EXEC_DATE}, at {SERVICE_PLACE}. (28 U.S.C. § 1746.)",
        first_indent=0,
    )
    _sign_block(d, case)
    d.save()
    _stamp_sig(path)


# ------------------------------------------------------------------- order
def build_order(path: Path, case: Case) -> None:
    d = PleadingPaper(str(path), doc_title_footer=f"[PROPOSED] ORDER -- {case.short}")
    _header(d, case)
    _caption(d, case, ["[PROPOSED] ORDER CORRECTING", "PLAINTIFF'S NAME ON THE", "DOCKET"])
    d.write_line("[PROPOSED] ORDER", bold=True, center=True)
    d.blank_line()
    d.write_wrapped(
        "Plaintiff's Administrative Motion to Correct Plaintiff's Name on the "
        "Docket came before the Court under Civil Local Rule 7-11. Having "
        "considered the motion and the supporting declaration, and good cause "
        "appearing, the Court ORDERS as follows:",
        first_indent=0,
    )
    d.blank_line()
    d.write_wrapped(
        f"1.  The motion is GRANTED. Plaintiff's name on the docket in this "
        f"action shall be stated as \"{TARGET_NAME_TC}.\"",
        first_indent=0,
    )
    d.blank_line()
    d.write_wrapped(
        "2.  The Clerk is directed to conform the CM/ECF party record in this "
        "action accordingly.",
        first_indent=0,
    )
    d.blank_line()
    d.write_wrapped(
        "3.  This order corrects the form of Plaintiff's name only. It effects no "
        "substitution of parties, no amendment of any claim or allegation, and no "
        "change to any deadline previously set in this action.",
        first_indent=0,
    )
    d.blank_line()
    d.blank_line()
    d.write_line("IT IS SO ORDERED.")
    d.blank_line()
    d.blank_line()
    d.write_line("Dated: ______________________")
    d.blank_line()
    d.blank_line()
    d.write_line("                                    ___________________________________")
    d.write_line(f"                                    {case.judge}")
    d.write_line("                                    United States Magistrate Judge")
    d.save()


# --------------------------------------------------------------------- POS
def build_pos(path: Path, case: Case) -> Path:
    recipients = case.recipients or [
        "[COMPLETE BEFORE FILING — name, firm, and street address of each",
        "counsel of record. Serve by U.S. Mail under Fed. R. Civ. P. 5(b)(2)(C).",
        "Do not serve by e-mail unless counsel has given written consent under",
        "Fed. R. Civ. P. 5(b)(2)(E).]",
    ]
    fields = ProofOfServiceFields(
        plaintiff_line=TARGET_NAME_TC,
        defendant_lines=[l.rstrip(",") for l in case.left_caption],
        case_number=case.case_no,
        service_date=EXEC_DATE,
        document_title=(
            "ADMINISTRATIVE MOTION TO CORRECT PLAINTIFF'S NAME ON THE DOCKET; "
            "DECLARATION OF PLAINTIFF; [PROPOSED] ORDER"
        ),
        mailing_location=SERVICE_PLACE,
        recipients=recipients,
        server_name=TARGET_NAME_TC,
        stamp_signature=True,
    )
    return build_proof_of_service(path, fields)


# ------------------------------------------------------------ m&c e-mail
def build_email(path: Path, case: Case) -> None:
    to = "; ".join(case.emails) or "[counsel of record]"
    body = f"""To: {to}
Subject: {case.case_no} — request to stipulate to a docket name correction (Civil L.R. 7-11(a))

Dear {case.counsel_salutation},

I write under Civil Local Rule 7-11(a) before filing an administrative
motion, to ask whether you will stipulate.

I am one person. This docket identifies me as "{case.docket_name}." My PACER
account ({PACER_LOGIN}) records my first name as "Brendan" and my last name
as "Ngwa Nforbi." Because the two do not match, the CAND ECF Help Desk
advised me on {HELPDESK_DATE} that it cannot link this case to my account,
and that the fix is to ask the Court to correct the name on the docket first.

The result is that I cannot e-file in this case and must file on paper.

I intend to ask the Court to state my name on the docket as
"{TARGET_NAME_TC}." The request changes nothing else: no party is added,
dropped, or substituted; no claim or allegation is amended; no deadline
moves. Rule 25 is not implicated, because I am the same person before and
after.

Would you stipulate? If so, I will prepare a short stipulation and proposed
order for your signature. If you would rather I proceed by motion, or if you
oppose, please tell me so I can state your position accurately in my
Rule 7-11(a) declaration.

Thank you.

{TARGET_NAME_TC}
Plaintiff, In Pro Per
1455 Cat Tail Drive, Stockton, CA 95204
(209) 801-4442 | bnn.cdl@gmail.com
"""
    path.write_text(body, encoding="utf-8")


# -------------------------------------------------------------------- main
def main() -> None:
    OUTDIR.mkdir(parents=True, exist_ok=True)
    verify: list[str] = [
        "VERIFY BEFORE FILING — N.D. Cal. name-correction packets",
        f"Generated {EXEC_DATE}. Target docket name: {TARGET_NAME_TC}",
        "",
        "1. Pull the exact party-name string from the PACER party tab in each",
        "   case. The strings below came from the portfolio record, not from",
        "   PACER. If a docket reads 'Nforbi' rather than 'Ngwa Nforbi', it does",
        "   NOT already match the ECF account and still needs a motion.",
        "",
        "2. Attach the September 1, 2026 ECF Help Desk e-mail as Exhibit A to",
        "   each declaration before filing.",
        "",
        "3. Complete the bracketed Civil L.R. 7-11(a) paragraph in each",
        "   declaration after you hear back from counsel.",
        "",
        "4. SERVICE. The proof of service is written for U.S. Mail under",
        "   Fed. R. Civ. P. 5(b)(2)(C), which is always valid. Fill in each",
        "   counsel's STREET address. Do NOT switch it to e-mail service",
        "   unless that counsel has given written consent under Rule",
        "   5(b)(2)(E) — an e-mail address on a signature block is not",
        "   consent. The meet-and-confer drafts are correspondence, not",
        "   service, so e-mail is fine for those.",
        "",
    ]
    made = 0
    for case in CASES:
        stem = f"{case.slug}-matter-{case.matter}"
        motion = OUTDIR / f"{stem} - Admin Motion to Correct Name (Sep 9 2026).pdf"
        decl = OUTDIR / f"{stem} - Declaration ISO Name Correction (Sep 9 2026).pdf"
        order = OUTDIR / f"{stem} - Proposed Order Correcting Name (Sep 9 2026).pdf"
        pos = OUTDIR / f"{stem} - Proof of Service (Sep 9 2026).pdf"
        packet = OUTDIR / f"{stem} - NAME CORRECTION PACKET (Sep 9 2026).pdf"
        email = OUTDIR / f"{stem} - EMAIL_DRAFT_meet_and_confer.txt"

        build_motion(motion, case)
        build_declaration(decl, case)
        build_order(order, case)
        build_pos(pos, case)
        build_email(email, case)
        pages = assemble([motion, decl, order, pos], packet)
        made += 1
        print(f"  [{case.case_no}] matter {case.matter} — packet {pages} pp. "
              f"(docket name now: {case.docket_name})")

        verify.append(f"{case.case_no}  (matter {case.matter})")
        verify.append(f"    docket name per portfolio : {case.docket_name}")
        verify.append(f"    needs change             : {'YES' if case.needs_change else 'verify'}")
        if case.verify_note:
            verify.append(f"    NOTE                     : {case.verify_note}")
        if not case.recipients:
            verify.append("    NOTE                     : recipients blank — fill POS and e-mail.")
        verify.append("")

    (OUTDIR / "VERIFY.txt").write_text("\n".join(verify), encoding="utf-8")
    print(f"\n{made} packets + VERIFY.txt -> {OUTDIR.relative_to(ROOT.parent)}")


if __name__ == "__main__":
    main()
