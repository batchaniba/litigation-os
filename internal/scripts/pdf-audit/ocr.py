"""OCR fallback for the scanned/image-only PDFs among the Tier 1 selection."""
import os as _os
_REPO = _os.path.abspath(_os.path.join(_os.path.dirname(__file__), "..", "..", ".."))
_CACHE_DIR = _os.environ.get("PDF_AUDIT_CACHE", _os.path.join(_REPO, ".cache", "pdf-audit"))
_os.makedirs(_CACHE_DIR, exist_ok=True)
import json, os
import pypdfium2 as pdfium
import pytesseract

CACHE = _CACHE_DIR
MAX_PAGES = 6
index = json.load(open(_os.path.join(_CACHE_DIR, "index.json")))

targets = []
for m, recs in index.items():
    for r in recs:
        if r["chars"] < 200:
            targets.append((m, r))

for m, r in targets:
    cache_file = os.path.join(CACHE, r["cache"] + ".json")
    rec = json.load(open(cache_file))
    if rec.get("ocr"):
        continue
    pdf = pdfium.PdfDocument(rec["path"])
    pages = []
    for i in range(min(len(pdf), MAX_PAGES)):
        bitmap = pdf[i].render(scale=2.2)
        pages.append(pytesseract.image_to_string(bitmap.to_pil()))
    rec["pages"] = pages
    rec["ocr"] = True
    rec["chars"] = sum(len(p) for p in pages)
    json.dump(rec, open(cache_file, "w"))
    r["chars"] = rec["chars"]
    r["ocr"] = True
    print(f"matter {m:>2}  OCR {rec['chars']:>6} chars  {os.path.basename(rec['path'])[:70]}")

json.dump(index, open(_os.path.join(_CACHE_DIR, "index.json"), "w"), indent=1)
print("done", len(targets), "targets")
