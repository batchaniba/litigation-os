"""Cross-Matter Risk Index.

Reads the existing CONSISTENCY_AUDIT.md plus every archived PDF to build:
  1. A structured contradiction index (the 22 findings with matter refs and severity).
  2. A related-matter graph keyed by shared defendants / clusters / fact patterns.
  3. Active-matter exposure: which archived matters share a fact pattern or
     defendant with an active matter, and any archived text that names an
     active-matter case number or defendant.

Outputs:
  internal/docs/cross_matter_risk_index.json
  internal/docs/CROSS_MATTER_RISK_INDEX.md
"""
import json
import os
import re
import sys
import unicodedata
from collections import defaultdict

_REPO = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..", ".."))
DOCS = os.path.join(_REPO, "internal", "public", "documents")
MATTERS = os.path.join(_REPO, "internal", "src", "data", "matters")
CACHE = os.environ.get("PDF_AUDIT_CACHE", os.path.join(_REPO, ".cache", "pdf-audit"))


def norm(s):
    s = unicodedata.normalize("NFKD", s or "")
    return re.sub(r"\s+", " ", s).strip()


def load_records():
    records = {}
    for name in os.listdir(MATTERS):
        if re.match(r"\d{2}\.json$", name):
            data = json.load(open(os.path.join(MATTERS, name)))
            records[data["number"]] = data
    return records


def parse_audit_markdown(path):
    """Extract the numbered findings from CONSISTENCY_AUDIT.md into structured records."""
    text = open(path).read()
    findings = []
    # Split into severity sections first
    sections = re.split(r"\n### (HIGH|MEDIUM|LOW) severity\n", text)
    current_sev = None
    for part in sections:
        if part in ("HIGH", "MEDIUM", "LOW"):
            current_sev = part.lower()
            continue
        if current_sev is None:
            continue
        # Find all **N. markers in this section and slice the text between them.
        markers = list(re.finditer(r"\n\*\*(\d+)\.\s?", part))
        for i, m in enumerate(markers):
            num = int(m.group(1))
            start = m.start()
            end = markers[i + 1].start() if i + 1 < len(markers) else len(part)
            block = part[start:end]
            # first line is the title / matter list
            first = block.split("\n", 1)[0]
            body = block[len(first):].strip()
            # strip markdown bold markers from title
            title = re.sub(r"\*\*", "", first).strip()
            # drop the leading number from title
            title = re.sub(r"^\d+\.\\s*", "", title)
            matter_nums = [int(n) for n in re.findall(r"\b\d{1,2}\b", first + " " + body)]
            findings.append(
                {
                    "id": num,
                    "title": norm(title) or f"Finding {num}",
                    "severity": current_sev,
                    "matters": matter_nums,
                    "body": norm(body),
                    "type": "sworn_contradiction" if num <= 13 else "recordkeeping",
                }
            )
    findings.sort(key=lambda x: x["id"])
    return findings


def related_matters(records):
    """Build a graph of related matters by shared cluster and shared defendants."""
    graph = defaultdict(lambda: {"shared_defendants": [], "shared_cluster": [], "shared_fact_group": []})

    # clusters
    clusters = defaultdict(list)
    for n, r in records.items():
        clusters[r.get("cluster")].append(n)
    for members in clusters.values():
        for a in members:
            for b in members:
                if a != b and b not in graph[a]["shared_cluster"]:
                    graph[a]["shared_cluster"].append(b)

    # defendants: extract last names / entity short tokens
    def tokens(defs):
        out = set()
        for chunk in re.split(r";|\band\b", defs or ""):
            chunk = chunk.strip(" .,")
            # prefer capitalized words that look like proper names
            for w in re.findall(r"[A-Z][a-zA-Z\-']{2,}", chunk):
                if w.lower() not in ("state", "california", "county", "city",
                                     "officer", "sergeant", "deputy", "individual",
                                     "capacity", "official", "does", "inc", "llc",
                                     "corporation", "company", "services", "department",
                                     "program", "united", "district", "court", "superior"):
                    out.add(w)
        return out

    for n, r in records.items():
        r["_def_tokens"] = tokens(r.get("defendants", ""))

    for a, ra in records.items():
        for b, rb in records.items():
            if a >= b:
                continue
            common = ra["_def_tokens"] & rb["_def_tokens"]
            if common:
                graph[a]["shared_defendants"].append({"matter": b, "names": sorted(common)})
                graph[b]["shared_defendants"].append({"matter": a, "names": sorted(common)})

    return {k: dict(v) for k, v in graph.items()}


def archived_cross_refs(records, active_numbers):
    """Scan archived PDFs for mentions of active-matter case numbers / defendants."""
    signals = []
    case_nos = {}
    for n, r in records.items():
        cn = norm(r.get("case_no", ""))
        if cn and cn.lower() not in ("n/a", "not yet assigned", "pending"):
            case_nos[n] = re.sub(r"[^A-Z0-9]", "", cn.upper())

    # Curated watch terms per active matter.  These are the distinctive proper
    # names / short entity names that indicate a real cross-reference, not
    # generic legal words like "Director" or "Service".
    active_tokens = {
        1: {"Candelaria", "Highway Patrol", "CHP"},
        2: {"Serrato", "Duryee", "CHP", "Highway Patrol"},
        7: {"Candelaria", "Centerline", "CHP", "Highway Patrol"},
        12: {"Diamond", "Freightliner", "BMW", "South Bay"},
        19: {"Macomber", "CDCR", "Board of Parole"},
        20: {"Serrato", "Duryee", "Candelaria", "CHP", "U-visa", "U visa", "Certification"},
        24: {"Serrato", "Duryee", "CHP", "U-visa", "U visa", "Certification"},
        25: {"FedEx", "Federal Express", "First Advantage"},
        26: {"UPS", "United Parcel", "First Advantage"},
        27: {"Randstad", "Macy"},
        28: {"HOPE", "Palacios", "Noguchi", "CASOMB"},
        29: {"DFEH", "Fair Employment", "Housing"},
    }

    for n, r in records.items():
        if r.get("lifecycle") == "active":
            continue
        folder = os.path.join(DOCS, f"matter-{n:02d}")
        if not os.path.isdir(folder):
            continue
        for root, _, files in os.walk(folder):
            for f in files:
                if not f.lower().endswith(".pdf"):
                    continue
                full = os.path.join(root, f)
                key = hashlib.sha1(full.encode()).hexdigest()[:16] if 'hashlib' in dir() else None
                if not key:
                    import hashlib
                    key = hashlib.sha1(full.encode()).hexdigest()[:16]
                cache = os.path.join(CACHE, key + ".json")
                if not os.path.exists(cache):
                    continue
                body = json.load(open(cache))
                text = norm(" ".join(body.get("pages") or [])).upper()
                if len(text) < 120:
                    continue

                # active case number mentions
                for an, acn in case_nos.items():
                    if an in active_numbers and acn and acn in text:
                        signals.append(
                            {
                                "matter": n,
                                "file": f,
                                "type": "active_case_number",
                                "target_matter": an,
                                "detail": f"archived matter {n:02d} filing '{f}' mentions active matter {an:02d} case number",
                            }
                        )

                # active defendant name mentions
                for an, toks in active_tokens.items():
                    hits = [t for t in toks if re.search(r"\b" + re.escape(t.upper()) + r"\b", text)]
                    if hits:
                        signals.append(
                            {
                                "matter": n,
                                "file": f,
                                "type": "active_defendant_name",
                                "target_matter": an,
                                "detail": f"archived matter {n:02d} filing '{f}' names active matter {an:02d} defendant(s): {', '.join(hits)}",
                            }
                        )
    return signals


def main():
    records = load_records()
    active = sorted([n for n, r in records.items() if r.get("lifecycle") == "active"])
    archived = sorted([n for n, r in records.items() if r.get("lifecycle") != "active"])

    audit_path = os.path.join(_REPO, "internal", "docs", "CONSISTENCY_AUDIT.md")
    findings = parse_audit_markdown(audit_path) if os.path.exists(audit_path) else []

    graph = related_matters(records)

    # active exposure: active matters that share facts with archived matters
    exposure = {}
    for n in active:
        rel = graph.get(n, {})
        exposed = set()
        for e in rel.get("shared_cluster", []):
            exposed.add(e)
        for e in rel.get("shared_defendants", []):
            exposed.add(e["matter"])
        # also from audit findings
        for f in findings:
            if n in f["matters"]:
                exposed.update(f["matters"])
        exposed.discard(n)
        exposure[n] = sorted(exposed)

    signals = archived_cross_refs(records, active)

    # aggregate active risk score
    active_risk = {}
    for n in active:
        score = 0
        for f in findings:
            if n in f["matters"]:
                score += {"high": 3, "medium": 2, "low": 1}[f["severity"]]
        score += len([s for s in signals if s.get("target_matter") == n])
        active_risk[n] = score

    out = {
        "generated_for": "cross-matter-risk-index",
        "active_matters": active,
        "archived_matters": archived,
        "contradiction_findings": findings,
        "related_matters": graph,
        "active_exposure": exposure,
        "archived_to_active_signals": signals,
        "active_risk_score": active_risk,
    }

    json.dump(out, open(os.path.join(_REPO, "internal", "docs", "cross_matter_risk_index.json"), "w"), indent=1)

    # Markdown report
    lines = [
        "# Cross-Matter Risk Index",
        "",
        "Generated from `CONSISTENCY_AUDIT.md`, matter JSON records, and a full-text scan of archived PDFs.",
        "",
        "## Summary",
        "",
        f"- Active matters scanned: {len(active)}",
        f"- Archived matters scanned: {len(archived)}",
        f"- Contradiction findings indexed: {len(findings)}",
        f"- Archived→active cross-reference signals: {len(signals)}",
        "",
        "## Active matter risk scores",
        "",
        "| Matter | Score | Exposed to archived matters |",
        "|---|---|---|",
    ]
    for n in sorted(active_risk, key=lambda x: -active_risk[x]):
        rel = ", ".join(f"{m:02d}" for m in exposure.get(n, []))
        lines.append(f"| Matter {n:02d} | {active_risk[n]} | {rel} |")

    lines += [
        "",
        "## Contradiction findings",
        "",
    ]
    for f in findings:
        lines.append(f"### #{f['id']} — {f['title']} ({f['severity']})")
        lines.append(f"- Matters: {', '.join(f'Matter {m:02d}' for m in f['matters'])}")
        lines.append(f"- Type: {f['type']}")
        lines.append("")
        lines.append(f["body"])
        lines.append("")

    if signals:
        lines += [
            "",
            "## Archived → active cross-reference signals",
            "",
            "| Archived matter | File | Signal type | Active matter | Detail |",
            "|---|---|---|---|---|",
        ]
        for s in signals:
            lines.append(
                f"| {s['matter']:02d} | {s['file']} | {s['type']} | {s['target_matter']:02d} | {s['detail']} |"
            )
    else:
        lines += ["", "## Archived → active cross-reference signals", "", "No archived filings mention active-matter case numbers or defendants."]

    open(os.path.join(_REPO, "internal", "docs", "CROSS_MATTER_RISK_INDEX.md"), "w").write("\n".join(lines))
    print(f"indexed {len(findings)} findings, {len(signals)} cross-reference signals")
    print(f"wrote cross_matter_risk_index.json and CROSS_MATTER_RISK_INDEX.md")


if __name__ == "__main__":
    main()
