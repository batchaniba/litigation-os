"""Mechanical source preservation, PDF checks and local-only rendered review sheets."""
from pathlib import Path
import json
import subprocess
import hashlib
import numpy as np
import pymupdf as fitz
from PIL import Image, ImageDraw

HERE = Path(__file__).resolve().parent
ROOT = HERE.parent
LOCAL_QA = Path("/home/user/workspace/matter20-review-qa")
LOCAL_QA.mkdir(exist_ok=True)
verification = json.loads((HERE / "generation-verification.json").read_text())
baseline = fitz.open(ROOT / "10-working-motion/Newanforbi_26CV191136_Working_Motion_Packet_Federal_Order_Revision.pdf")
packet = fitz.open(HERE / "Matter-20-Revised-Moving-Papers-Review-Compilation.pdf")
memo_pages = verification["memo_total_pages"]
targets = {1: 0, 2: 1, 3: 2, 16: 3 + memo_pages, 17: 4 + memo_pages,
           18: 5 + memo_pages, 19: 6 + memo_pages, 29: 7 + memo_pages,
           30: 8 + memo_pages, 31: 9 + memo_pages}
changes = {change["source_page"]: change for change in verification["neutral_title_corrections"]}
preservation = []
for source_page, output_index in targets.items():
    original, output = baseline[source_page - 1], packet[output_index]
    a, b = original.get_pixmap(alpha=False), output.get_pixmap(alpha=False)
    aa = np.frombuffer(a.samples, np.uint8).reshape(a.height, a.width, 3)
    bb = np.frombuffer(b.samples, np.uint8).reshape(b.height, b.width, 3)
    difference = np.any(aa != bb, axis=2)
    if source_page in changes:
        x0, y0, x1, y1 = changes[source_page]["bbox"]
        difference[max(0, int(y0)-3):int(y1)+4, max(0, int(x0)-3):int(x1)+4] = False
        assert not difference.any(), f"Unrelated visual change on source page {source_page}"
        assert changes[source_page]["after"] in output.get_text(), source_page
        status = "unchanged outside declared title-correction line"
    else:
        assert a.samples == b.samples, f"Unchanged page failed pixel comparison: {source_page}"
        status = "pixel-identical"
    preservation.append({"source_page": source_page, "compilation_page": output_index + 1, "status": status})

all_outputs = sorted(HERE.glob("*.pdf"))
syntax = {}
images = []
for path in all_outputs:
    result = subprocess.run(["qpdf", "--check", str(path)], text=True, capture_output=True)
    assert result.returncode == 0, result.stdout + result.stderr
    doc = fitz.open(path)
    syntax[path.name] = {"qpdf_check": "passed", "pages": len(doc)}
    for index, page in enumerate(doc):
        assert abs(page.rect.width - 612) < .01 and abs(page.rect.height - 792) < .01
        assert "\ufffd" not in page.get_text(), (path.name, index + 1)
        if "Compilation" not in path.name:
            for block in page.get_text("dict")["blocks"]:
                for line in block.get("lines", []):
                    for span in line["spans"]:
                        assert span["bbox"][2] <= 577, (path.name, index + 1, span["text"])
        # Review all newly generated pages; compilation's unchanged pages are
        # validated pixel-for-pixel and the three corrected lines are inspected.
        pix = page.get_pixmap(matrix=fitz.Matrix(1.1, 1.1), alpha=False)
        if "Compilation" in path.name:
            if index not in [targets[n] for n in changes]:
                continue
        image = Image.frombytes("RGB", [pix.width, pix.height], pix.samples)
        images.append((path.name + " / PDF " + str(index + 1), image))
sheet_paths = []
for offset in range(0, len(images), 4):
    batch = images[offset:offset+4]
    w, h = max(i.width for _, i in batch), max(i.height for _, i in batch)
    sheet = Image.new("RGB", (w*2 + 30, (h+32)*2 + 15), "#dddddd")
    draw = ImageDraw.Draw(sheet)
    for index, (label, image) in enumerate(batch):
        x, y = 10 + (index % 2) * (w+10), 8 + (index // 2) * (h+32)
        draw.text((x, y), label, fill="black")
        sheet.paste(image, (x, y+22))
    dest = LOCAL_QA / f"review-sheet-{offset//4+1:02}.png"
    sheet.save(dest)
    sheet_paths.append(str(dest))

memo = fitz.open(HERE / "Matter-20-Revised-Writ-Memorandum.pdf")
memo_text = "\n".join(page.get_text() for page in memo)
for literal in ("1455 Cat Tail Drive", "26CV191136", "958052306492",
                "January 8, 2027", "Jenna M. Whitman", "0.073", "0.004"):
    assert literal in memo_text, literal
assert "Verified Answer" not in memo_text
assert len(memo) == verification["memo_total_pages"]
report = {"syntax_and_page_boxes": syntax,
          "source_page_preservation": preservation,
          "all_output_pages_rendered": True,
          "local_review_sheets": sheet_paths,
          "warning": "Mechanical checks do not establish admissibility, current docket status or filing readiness."}
(HERE / "quality-verification.json").write_text(json.dumps(report, indent=2) + "\n")
print(json.dumps(report, indent=2))
