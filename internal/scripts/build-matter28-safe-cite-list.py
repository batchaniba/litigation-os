#!/usr/bin/env python3
"""Build Matter 28 safe-cite / do-not-use list keyed to research PDF pages.

Reads citation_audit.json (Matter 28 entries) and scans each research PDF page
for case-name / reporter hits. Writes:

  internal/docs/MATTER_28_SAFE_CITE_LIST.md

Buckets:
  SAFE          — VERIFIED, load-bearing as characterized
  CAUTION       — VERIFIED but vacated, adverse, or must-distinguish
  DO_NOT_USE    — MISCITED / MISCHARACTERIZED / NOT_FOUND
"""

from __future__ import annotations

import json
import re
from collections import defaultdict
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
AUDIT_PATH = ROOT / "docs/citation_audit.json"
RESEARCH_DIR = ROOT / "public/documents/matter-28/research"
OUT_PATH = ROOT / "docs/MATTER_28_SAFE_CITE_LIST.md"

# Verified cites that still need a briefing guardrail.
CAUTION_NAMES = {
    "Filarsky v. Delia",  # distinguish: private attorney briefly retained by city
    "United States v. Sanchez-Gomez",  # vacated by SCOTUS
    "Minneci v. Pollard",  # adverse Bivens / private-prison context
    "Luca v. Administration of Offender Services Bureau",  # adverse unpublished
    "Estate of Esche v. Bunuel-Jordana",  # real but jurisdictional — also MISCHARACTERIZED
}

# Preferred Theory A / Theory B lead string for the header.
THEORY_A_LEAD = (
    "Richardson v. McKnight; Halvorsen v. Baird; Clement v. City of Glendale; "
    "Ace Beverage Co. v. Lockheed Info. Mgmt. Servs.; Danielson v. Inslee "
    "(distinguish Filarsky v. Delia; cite Estate of Esche only for its reasoning, "
    "not as a QI-threshold holding)"
)
THEORY_B_LEAD = (
    "Neal v. Shimoda + Morrissey v. Brewer / Vitek v. Jones / Foucha v. Louisiana "
    "+ United States v. Williams / Weber / Cope "
    "(drop Jessie, Chubb, Collins, Grants Pass; fix Johnson reporter; "
    "do not claim Chavez reversed on QI; soften Edmo)"
)

DO_NOT_USE_STATUS = {"MISCITED", "MISCHARACTERIZED", "NOT_FOUND"}


def _needles(entry: dict) -> list[str]:
    name = entry.get("case_name") or ""
    cite = entry.get("citation") or ""
    out: list[str] = []
    if name:
        out.append(name)
        first = name.split(" v.")[0].split(",")[0].strip()
        if len(first) >= 5:
            out.append(first)
    for pat in (
        r"(\d+\s+F\.(?:3d|4th|2d|Supp\.\s*2d?)\s+\d+)",
        r"(\d+\s+U\.S\.\s+\d+)",
        r"(\d+\s+M\.J\.\s+\d+)",
        r"(WL\s+\d+)",
        r"(No\.\s+\d+-\d+)",
    ):
        m = re.search(pat, cite)
        if m:
            out.append(m.group(1))
    # Deduplicate preserving order
    seen = set()
    uniq = []
    for n in out:
        if n not in seen:
            seen.add(n)
            uniq.append(n)
    return uniq


def page_mentions(text: str, entry: dict) -> bool:
    compact = re.sub(r"\s+", " ", text)
    compact_ns = compact.replace(" ", "")
    for n in _needles(entry):
        if n in compact or n.replace(" ", "") in compact_ns:
            return True
    return False


def bucket_for(entry: dict) -> str:
    status = entry.get("status") or ""
    name = entry.get("case_name") or ""
    if status in DO_NOT_USE_STATUS:
        return "DO_NOT_USE"
    if status == "VERIFIED" and name in CAUTION_NAMES:
        return "CAUTION"
    if status == "VERIFIED":
        return "SAFE"
    return "CAUTION"


def action_for(entry: dict) -> str:
    status = entry["status"]
    name = entry["case_name"]
    cite = entry["citation"]
    note = (entry.get("notes") or "").strip()
    if name.startswith("Dunford"):
        return "DROP — no such case; use Foltz, 331 F.3d at 1131"
    if name.startswith("Condit"):
        return "DROP quote attribution — re-pin to Foltz, 331 F.3d at 1131"
    if name.startswith("United States v. Jessie"):
        return "DROP — CAAF case; wrong proposition for SOTP blanket policies"
    if name.startswith("Chubb"):
        return "DROP — wrong court and wrong proposition"
    if name.startswith("Collins"):
        return "DROP — citation does not exist at 81 F.3d 167"
    if name.startswith("Johnson v. City of Grants Pass"):
        return "DROP for due-process / 'illusory procedures' proposition"
    if name.startswith("United States v. Johnson"):
        return "FIX reporter — use 697 F.3d 1249 / 2012 WL 5328597 (not WL 5279672)"
    if name.startswith("Tsao") and "98 F.3d" in cite:
        return "FIX — print as 698 F.3d 1128 (not 98 F.3d)"
    if name.startswith("Chavez"):
        return "DO NOT claim QI-denial reversal — Ninth Circuit affirmed dismissal"
    if name.startswith("Edmo"):
        return "SOFTEN — individualized deliberate-indifference holding, not per se blanket ban"
    if name.startswith("Estate of Esche"):
        return "REASONING only — holding is jurisdictional, not QI threshold"
    if name.startswith("Filarsky"):
        return "DISTINGUISH — briefly retained private counsel for a city, not private CDCR vendor CEO"
    if "Sanchez-Gomez" in name:
        return "FLAG vacated — do not treat as binding clearly-established law"
    if name.startswith("Minneci"):
        return "ADVERSE context — Bivens / private prison; use only if distinguishing"
    if name.startswith("Luca"):
        return "ADVERSE unpublished — expect opponent to cite; do not lead with it"
    return note.split(".")[0] + "." if note else status


def short_fix(entry: dict) -> str:
    return (
        f"**{entry['case_name']}**, {entry['citation']} — "
        f"[{entry['status']}] {action_for(entry)}"
    )


def main() -> None:
    import pymupdf

    audit = json.loads(AUDIT_PATH.read_text())
    m28 = [c for c in audit["citations"] if c.get("matter") == 28]
    research_pdfs = sorted(RESEARCH_DIR.glob("*.pdf"))

    lines: list[str] = []
    lines.append("# Matter 28 — Safe Cite List / Do-Not-Use List (page-keyed)")
    lines.append("")
    lines.append(
        "Opposition-prep research only. Generated from Round 2–3 `citation_audit.json` "
        "hits mapped onto each PDF page. Filed protective-order package is covered "
        "separately at the bottom (cite-corrected renewed drafts strip *Dunford* / "
        "re-pin the Condit quote to *Foltz*)."
    )
    lines.append("")
    lines.append("| Bucket | Meaning |")
    lines.append("| --- | --- |")
    lines.append("| **SAFE** | VERIFIED; okay to brief as characterized |")
    lines.append(
        "| **CAUTION** | Real, but distinguish, fix form, or do not treat as binding |"
    )
    lines.append(
        "| **DO NOT USE** | MISCITED / MISCHARACTERIZED / NOT_FOUND — remove before filing |"
    )
    lines.append("")
    lines.append("### Briefing leads (after cleanup)")
    lines.append("")
    lines.append(f"- **Theory A (no QI / threshold):** {THEORY_A_LEAD}")
    lines.append(f"- **Theory B (clearly established):** {THEORY_B_LEAD}")
    lines.append("")

    # Global do-not-use cheat sheet
    lines.append("## Global do-not-use cheat sheet")
    lines.append("")
    lines.append("| Authority | Status | Fix |")
    lines.append("| --- | --- | --- |")
    seen_bad = set()
    for e in m28:
        if e["status"] not in DO_NOT_USE_STATUS:
            continue
        key = (e["case_name"], e["citation"])
        if key in seen_bad:
            continue
        seen_bad.add(key)
        # short fix
        lines.append(
            f"| {e['case_name']}, {e['citation']} | {e['status']} | {action_for(e)} |"
        )
    lines.append("")

    for pdf in research_pdfs:
        rel = f"matter-28/research/{pdf.name}"
        doc_entries = [
            e
            for e in m28
            if (e.get("document") or "").endswith(pdf.name)
            or e.get("document") == rel
        ]
        d = pymupdf.open(pdf)
        lines.append(f"## `{pdf.name}` ({len(d)} pages)")
        lines.append("")
        if doc_entries:
            lines.append(
                f"_Audit rows attributed to this file: {len(doc_entries)}. "
                "Page rows below also surface Matter 28 research authorities "
                "that appear on the page even if primarily audited under another memo._"
            )
        else:
            lines.append(
                "_No dedicated audit rows for this file; pages matched against "
                "the Matter 28 research authority set._"
            )
        lines.append("")

        for i, page in enumerate(d):
            text = page.get_text()
            hits = []
            for e in m28:
                edoc = e.get("document") or ""
                if "research/" not in edoc and "Motion Protective" not in edoc:
                    # complaint-only rows stay out unless they hit
                    if not page_mentions(text, e):
                        continue
                if page_mentions(text, e):
                    hits.append(e)
            # Prefer research hits; drop complaint-only noise
            hits = [
                e
                for e in hits
                if "research/" in (e.get("document") or "")
                or "Motion Protective" in (e.get("document") or "")
            ]
            # Deduplicate by case_name + status bucket preference
            # For Tsao: if page has 98 F.3d keep MISCITED row; if 698 keep VERIFIED
            by_name: dict[str, list] = defaultdict(list)
            for e in hits:
                by_name[e["case_name"]].append(e)
            uniq = []
            for name, group in by_name.items():
                if name.startswith("Tsao"):
                    if "98 F.3d" in text and any("98 F.3d" in g["citation"] for g in group):
                        uniq.extend([g for g in group if "98 F.3d" in g["citation"]])
                    elif any("698 F.3d" in g["citation"] for g in group):
                        uniq.extend([g for g in group if "698 F.3d" in g["citation"]][:1])
                    else:
                        uniq.append(group[0])
                else:
                    # one row per case_name — prefer DO_NOT_USE over SAFE if both
                    group_sorted = sorted(
                        group,
                        key=lambda g: (
                            0 if g["status"] in DO_NOT_USE_STATUS else 1,
                            g["citation"],
                        ),
                    )
                    uniq.append(group_sorted[0])

            safe = [e for e in uniq if bucket_for(e) == "SAFE"]
            caution = [e for e in uniq if bucket_for(e) == "CAUTION"]
            bad = [e for e in uniq if bucket_for(e) == "DO_NOT_USE"]

            lines.append(f"### Page {i + 1}")
            if not uniq:
                lines.append("_No audited Matter 28 authorities detected on this page._")
                lines.append("")
                continue
            if safe:
                lines.append("**SAFE**")
                for e in sorted(safe, key=lambda x: x["case_name"]):
                    lines.append(
                        f"- {e['case_name']}, {e['citation']}"
                    )
            if caution:
                lines.append("**CAUTION**")
                for e in sorted(caution, key=lambda x: x["case_name"]):
                    lines.append(f"- {short_fix(e)}")
            if bad:
                lines.append("**DO NOT USE**")
                for e in sorted(bad, key=lambda x: x["case_name"]):
                    lines.append(f"- {short_fix(e)}")
            lines.append("")
        d.close()

    # Protective order section
    lines.append("## Filed protective-order package (not research, but cite-critical)")
    lines.append("")
    lines.append(
        "The July 16, 2026 motion / proposed order (denied without prejudice, Doc 7) "
        "contained two bad cites. **Do not reuse the filed PDFs' authority block.** "
        "Renewed cite-corrected drafts live at:"
    )
    lines.append("")
    lines.append(
        "- `matter-28/Renewed Motion Protective Order NDCA (cite-corrected draft).pdf`"
    )
    lines.append(
        "- `matter-28/Proposed Protective Order NDCA (cite-corrected draft).pdf`"
    )
    lines.append("")
    lines.append("| Authority (as filed) | Status | Action |")
    lines.append("| --- | --- | --- |")
    lines.append(
        "| Dunford v. Rovi Corp., 2015 WL 13752958 | NOT_FOUND | DROP |"
    )
    lines.append(
        "| Condit v. Dunne, 225 F.R.D. 100, 105 (quote) | MISCITED | Re-attribute quote to Foltz, 331 F.3d at 1131 |"
    )
    lines.append(
        "| Foltz v. State Farm Mut. Auto. Ins. Co., 331 F.3d 1122 | VERIFIED | KEEP — sole cross-use authority |"
    )
    lines.append(
        "| Phillips ex rel. Estates of Byrd v. General Motors Corp., 307 F.3d 1206 | VERIFIED | KEEP — good-cause burden |"
    )
    lines.append("")
    lines.append(
        f"*Generated by `internal/scripts/build-matter28-safe-cite-list.py`. "
        f"Source audit date: {audit.get('analysisDate', 'n/a')}.*"
    )
    lines.append("")

    OUT_PATH.write_text("\n".join(lines), encoding="utf-8")
    print(f"Wrote {OUT_PATH} ({OUT_PATH.stat().st_size} bytes)")


if __name__ == "__main__":
    main()
