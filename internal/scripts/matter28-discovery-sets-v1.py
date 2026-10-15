#!/usr/bin/env python3
"""Matter 28 -- Discovery sets v1 (ROGs / RFAs / RFPs to HOPE and to Smith), rendered to
markdown (with internal notes appendix) and to pleading-paper PDF (service text only).

Newanforbi v. Smith, N.D. Cal. No. 3:26-cv-07504-LJC. Assumes all claims survive Dkt 15 except
fraud and RICO. Nothing here is served: signature lines print blank; pass --stamp-signature only at
service time (Rule 26(g) certification is the Plaintiff's). HOLD sets carry a HOLD footer.

    python3 internal/scripts/matter28-discovery-sets-v1.py [--stamp-signature] [--date "..."]
"""
from __future__ import annotations
import argparse, sys, tempfile
from pathlib import Path

SCRIPT_DIR = Path(__file__).resolve().parent
sys.path.insert(0, str(SCRIPT_DIR / "lib")); sys.path.insert(0, str(SCRIPT_DIR))
from pleading_paper import CONTENT_LEFT, PleadingPaper  # noqa: E402
from pdf_packet import assemble  # noqa: E402
from proof_of_service import DISTRICT_NDCAL, ProofOfServiceFields, build_proof_of_service  # noqa: E402
from signature_stamp import SIGNATURE_NATIVE_PX, SIGNATURE_PATH  # noqa: E402
import matter28_sets_v1_data as D  # noqa: E402

ROOT = SCRIPT_DIR.parents[1]
OUT = ROOT / "internal/docs/matter-28/discovery-workspace/drafts/sets-v1"
CASE_NO = "3:26-cv-07504-LJC"
ATTY = [("BRENDAN NGEHSI NEWANFORBI", "Times-Bold", 12), ("Plaintiff, In Propria Persona", "Times-Roman", 12),
        ("1455 Cat Tail Drive", "Times-Roman", 12), ("Stockton, CA 95204", "Times-Roman", 12),
        ("Telephone: (209) 801-4442", "Times-Roman", 12), ("E-mail: bnn.cdl@gmail.com", "Times-Roman", 12)]
LEFT = [("BRENDAN NGEHSI NEWANFORBI,", True, False), ("", 0, 0), ("                          Plaintiff,", 0, 0),
        ("", 0, 0), ("       v.", 0, 0), ("", 0, 0),
        ("SHANNON SMITH, LCSW, Chief", True, False), ("Executive Officer and Founder of", True, False),
        ("HOPE Program, an individual; and", True, False), ("HOPE PSYCHOTHERAPY, INC.,", True, False),
        ("d/b/a HOPE PROGRAM, a California", True, False), ("corporation,", True, False), ("", 0, 0),
        ("                          Defendants.", 0, 0)]
RECIPIENTS = [
    "Cynthia G. Lawrence, Esq. \u2014 cynthia@sims-law.net",
    "Blaze Van Dine, Esq. \u2014 blaze@sims-law.net",
    "Eric T. Martinez, Esq. \u2014 emartinez@sims-law.net",
    "Sims, Lawrence & Broghammer (e-service) \u2014 slb-eservice@sims-law.net",
    "", "Attorneys for Defendants Shannon Smith, LCSW, and",
    "HOPE Psychotherapy, Inc. (d/b/a HOPE Program)", "",
    "Service by electronic means under Fed. R. Civ. P. 5(b)(2)(E),",
    "pursuant to the written consent of counsel for Defendants."]

KIND = {"ROG": ("INTERROGATORY", "INTERROGATORIES", "Fed. R. Civ. P. 26, 33", D.INSTR_ROG),
        "RFA": ("REQUEST FOR ADMISSION", "REQUESTS FOR ADMISSION", "Fed. R. Civ. P. 26, 36", D.INSTR_RFA),
        "RFP": ("REQUEST FOR PRODUCTION", "REQUESTS FOR PRODUCTION OF DOCUMENTS", "Fed. R. Civ. P. 26, 34", D.INSTR_RFP)}
SETWORD = {1: "FIRST", 2: "SECOND"}


def sets():
    """Yield (filename stem, kind, party, set_no, hold, sections[(heading|None, [(text, tags, note)])])."""
    def rows(items, notes=None, fmt=lambda x: x):
        out = []
        for i, it in enumerate(items, 1):
            if isinstance(it, dict):
                out.append((it["t"], it.get("c", []), it.get("note")))
            else:
                out.append((it[0], it[1] if isinstance(it[1], list) else [], (notes or {}).get(i) if notes else None))
        return out
    yield ("01 HOPE - Interrogatories Set One", "ROG", D.HOPE, 1, False, [(None, rows(D.HOPE_ROGS))])
    yield ("02 HOPE - RFAs Set One", "RFA", D.HOPE, 1, False, [(None, rows(D.HOPE_RFA1, D.HOPE_RFA1_NOTES))])
    h2 = [(t, ["AUTH" if i <= 3 else "HOLD"], f"Bates basis: HOPE_{b}" + (" -- " + D.HOPE_RFA2_NOTES[i] if i in D.HOPE_RFA2_NOTES else ""))
          for i, (t, b) in enumerate(D.HOPE_RFA2_HOLD, 1)]
    yield ("03 HOPE - RFAs Set Two (HOLD pending PO fix)", "RFA", D.HOPE, 2, True, [(None, h2)])
    yield ("04 HOPE - RFPs Set One", "RFP", D.HOPE, 1, False, [(h, rows(items)) for h, items in D.HOPE_RFP])
    yield ("05 SMITH - Interrogatories Set One", "ROG", D.SMITH, 1, False, [(None, rows(D.SMITH_ROGS))])
    sr = rows(D.SMITH_RFA, D.SMITH_RFA_NOTES)
    yield ("06 SMITH - RFAs Set One", "RFA", D.SMITH, 1, False,
           [(None, [r for i, r in enumerate(sr, 1) if i not in D.SMITH_RFA_HOLD_IDX])])
    yield ("07 SMITH - RFAs Set Two (HOLD pending PO fix)", "RFA", D.SMITH, 2, True,
           [(None, [r for i, r in enumerate(sr, 1) if i in D.SMITH_RFA_HOLD_IDX])])
    yield ("08 SMITH - RFPs Set One", "RFP", D.SMITH, 1, False, [(h, rows(items)) for h, items in D.SMITH_RFP])


def title_lines(kind, party, n):
    return [f"PLAINTIFF'S {SETWORD[n]} SET OF {KIND[kind][1]}", f"TO DEFENDANT {D.PARTY_NAME[party]}"]


def preamble(kind, party):
    who = D.PARTY_NAME[party].title().replace("Lcsw", "LCSW").replace("Hope", "HOPE").replace("D/B/A", "d/b/a").replace("Inc.", "Inc.")
    verb = {"ROG": "answer each interrogatory below separately and fully, in writing and under oath",
            "RFA": "admit, in writing and under Rule 36, the truth of each matter below",
            "RFP": "produce the documents described below for inspection and copying"}[kind]
    return (f"TO DEFENDANT {D.PARTY_NAME[party]} AND {'ITS' if party == D.HOPE else 'HER'} ATTORNEYS OF RECORD:",
            f"Under Federal Rules of Civil Procedure 26 and {KIND[kind][2].split(', ')[-1]}, Plaintiff Brendan Ngehsi Newanforbi requests that Defendant {who} {verb}, and serve a written response on Plaintiff within thirty (30) days after service.")


def defs_for(party):
    d = list(D.DEFS_COMMON)
    d.insert(0, ('"YOU" and "YOUR"', "Defendant HOPE as defined below." if party == D.HOPE else "Defendant Shannon Smith, LCSW, and anyone acting on her behalf."))
    return d


# ------------------------------------------------------------------ markdown
def write_md(stem, kind, party, n, hold, sections):
    label, plural, rule, instr = KIND[kind]
    L = []
    if hold:
        L += ["> **HOLD -- NOT FOR SERVICE.** Depends on HOPE San Joaquin production (HOPE_000001-542). Serve only after the protective-order fix (re-production or stipulated prior-production paragraph). Bates cites appear here and are fine in this private workspace only.", ""]
    L += ["UNITED STATES DISTRICT COURT -- NORTHERN DISTRICT OF CALIFORNIA", "",
          "BRENDAN NGEHSI NEWANFORBI, Plaintiff, v. SHANNON SMITH, LCSW, et al., Defendants.", "",
          f"Case No. {CASE_NO} -- Hon. Lisa J. Cisneros", "",
          f"# {' '.join(title_lines(kind, party, n))}", "",
          f"Propounding party: Plaintiff Brendan Ngehsi Newanforbi. Responding party: Defendant {D.PARTY_NAME[party]}. Set No.: {n}. ({rule})", ""]
    a, b = preamble(kind, party); L += [a, "", b, "", "## INSTRUCTIONS", ""]
    L += [f"{i}. {t}" for i, t in enumerate(instr, 1)] + ["", "## DEFINITIONS", ""]
    L += [f"- {k} means {v}" for k, v in defs_for(party)] + ["", f"## {plural}", ""]
    num = 0; notes = []
    for head, items in sections:
        if head: L += [f"### {head}", ""]
        for text, tags, note in items:
            num += 1
            L += [f"**{label} NO. {num}:** {text}", ""]
            notes.append((num, tags, note))
    L += ["Dated: ____________________, 2026", "",
          "Respectfully submitted,", "", "[signature image placed at service]", "",
          "______________________________", "BRENDAN NGEHSI NEWANFORBI", "Plaintiff, In Propria Persona", "",
          "[Proof of service attached at service -- electronic service on SLB per written consent.]", "",
          "---", "", "## INTERNAL NOTES -- STRIP BEFORE SERVICE (not in the PDF)", "",
          "| No. | Claim / issue tags | Note |", "|---|---|---|"]
    L += [f"| {k} | {', '.join(t)} | {(nt or '').replace('|', '/')} |" for k, t, nt in notes]
    (OUT / f"{stem}.md").write_text("\n".join(L) + "\n")
    return num


# ------------------------------------------------------------------ pdf
def right_block(kind, party, n):
    rows = [(f"Case No. {CASE_NO}", 0, 0), ("", 0, 0)]
    rows += [(t, True, False) for t in [f"PLAINTIFF'S {SETWORD[n]} SET OF", *wrap_caption(KIND[kind][1]), "TO DEFENDANT", *wrap_caption(D.PARTY_NAME[party])]]
    rows += [("", 0, 0), (f"Set No.: {n}  ({KIND[kind][2]})", 0, 0), ("", 0, 0), ("Judge: Hon. Lisa J. Cisneros", 0, 0)]
    return rows


def wrap_caption(s, w=30):
    out, cur = [], ""
    for word in s.split():
        if len(cur) + len(word) + 1 > w: out.append(cur); cur = word
        else: cur = (cur + " " + word).strip()
    return out + [cur]


def write_pdf(stem, kind, party, n, hold, sections, args, tmp):
    label, plural, rule, instr = KIND[kind]
    short = {"ROG": "INTERROGATORIES", "RFA": "REQUESTS FOR ADMISSION", "RFP": "REQUESTS FOR PRODUCTION"}[kind]
    foot = f"PL.'S {SETWORD[n]} SET OF {short} TO {'HOPE' if party == D.HOPE else 'SMITH'} -- NEWANFORBI v. SMITH, No. {CASE_NO}" + (" -- HOLD, NOT FOR SERVICE" if hold else "")
    body = tmp / f"{stem}.body.pdf"
    d = PleadingPaper(str(body), doc_title_footer=foot)
    y = d._line_y(0)
    for i, (t, f, s) in enumerate(ATTY):
        d.c.setFont(f, s); d.c.drawString(CONTENT_LEFT, y - i * 15, t)
    d.current_line = 4; d.blank_line()
    d.write_line("UNITED STATES DISTRICT COURT", bold=True, center=True)
    d.write_line("NORTHERN DISTRICT OF CALIFORNIA", bold=True, center=True); d.blank_line()
    d.draw_caption_block(LEFT, right_block(kind, party, n), caption_size=10, tight_lh=13, boxed=True); d.blank_line()
    for t in title_lines(kind, party, n): d.write_line(t, bold=True, center=True)
    d.blank_line()
    a, b = preamble(kind, party)
    d.write_wrapped(a, first_indent=0); d.blank_line(); d.write_wrapped(b, first_indent=36); d.blank_line()

    def heading(t):
        d.ensure_space(4); d.write_line(t, bold=True, center=True); d.blank_line()
    heading("INSTRUCTIONS")
    for i, t in enumerate(instr, 1): d.write_wrapped(f"{i}. {t}", first_indent=0); d.blank_line()
    heading("DEFINITIONS")
    for k, v in defs_for(party): d.write_wrapped(f"{k} means {v}", first_indent=0); d.blank_line()
    heading(plural)
    num = 0
    for head, items in sections:
        if head: d.ensure_space(4); d.write_line(head, bold=True); d.blank_line()
        for text, _t, _n in items:
            num += 1
            d.ensure_space(3); d.write_line(f"{label} NO. {num}:", bold=True)
            d.write_wrapped(text, first_indent=36); d.blank_line()
    d.ensure_space(11)
    d.write_line(f"Dated: {args.date}" if args.date else "Dated: ____________________, 2026"); d.blank_line()
    d.write_respectfully_submitted(right_margin_offset=28)
    sig = "___________________________________"
    if args.stamp_signature and not hold:
        w, h = SIGNATURE_NATIVE_PX
        d.draw_signature_image(SIGNATURE_PATH, w, h, sig, width=210, right_margin_offset=28)
    else:
        d.blank_line(); d.blank_line()
    for ln in (sig, "BRENDAN NGEHSI NEWANFORBI", "Plaintiff, In Propria Persona"):
        d.write_line(ln, right=True, right_margin_offset=28)
    d.save()
    parts = [body]
    if not hold:
        pos = tmp / f"{stem}.pos.pdf"
        build_proof_of_service(pos, ProofOfServiceFields(
            plaintiff_line="BRENDAN NGEHSI NEWANFORBI", plaintiff_role="Plaintiff",
            defendant_lines=["SHANNON SMITH, LCSW;", "HOPE PSYCHOTHERAPY, INC."], defendant_role="Defendants",
            case_number=CASE_NO, title="PROOF OF SERVICE", service_date=args.date or "",
            document_title=f"PLAINTIFF'S {SETWORD[n]} SET OF {plural} TO DEFENDANT {D.PARTY_NAME[party]}",
            recipients=RECIPIENTS, server_name="Brendan Ngehsi Newanforbi",
            stamp_signature=bool(args.stamp_signature), district_line=DISTRICT_NDCAL, by_email=True,
            signature_on_second_page=True))
        parts.append(pos)
    (OUT / "pdf").mkdir(parents=True, exist_ok=True)
    final = OUT / "pdf" / f"{stem}.pdf"
    assemble(parts, final)
    return final


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--date", default="")
    ap.add_argument("--stamp-signature", action="store_true")
    args = ap.parse_args()
    OUT.mkdir(parents=True, exist_ok=True)
    with tempfile.TemporaryDirectory() as t:
        for stem, kind, party, n, hold, sections in sets():
            cnt = write_md(stem, kind, party, n, hold, sections)
            f = write_pdf(stem, kind, party, n, hold, sections, args, Path(t))
            print(f"{stem}: {cnt} items -> {f.relative_to(ROOT)}")


if __name__ == "__main__":
    main()
