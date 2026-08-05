# PDF-Grounded Source Audit — Tier 1 (Active Matters)

Every claim below was checked against the filed PDFs in `internal/public/documents/`,
not against other prose in this repository. Machine-readable findings:
[`pdf_source_audit.json`](./pdf_source_audit.json).

## Scope

| Item | Value |
| --- | --- |
| Matters audited | 12 active: 1, 2, 7, 12, 19, 20, 24, 25, 26, 27, 28, 29 |
| PDFs read in full | 61 (record-setting filings: complaints, summonses, orders, dispositive motions) |
| PDFs requiring OCR | 16 (scanned/flattened filings) |
| Fields cross-checked | case caption, case number, court/division, judge, named defendants, causes of action |
| Total PDFs in repo | 529 (Tier 2 = all ~335 active-matter documents; Tier 3 = full repo) |

Extraction is cached per file, so Tier 2/3 re-runs only pay for files not yet read.

## Result on core fields

**Zero factual discrepancies** between the matter records and the filed documents on
caption, court, case number, named defendants, or causes of action. Every documented
`documents[].path` resolves to a file on disk.

## Findings (5, all "unverified" — record not contradicted)

| Matter | Field | Record | In the PDFs |
| --- | --- | --- | --- |
| 7 | judge | Hon. Dena M. Coggins | not named in any Tier 1 filing |
| 19 | case number | C2604791 | not printed in the habeas petition |
| 19 | judge | Hon. Robert Hawk | not named in any Tier 1 filing |
| 24 | judge | Hon. Ajay S. Krishnan | not named in any Tier 1 filing |
| 28 | judge | Hon. Lisa J. Cisneros | not named in any Tier 1 filing |

These are the expected shape of a post-filing assignment: the court assigns the number
and the judge *after* the initiating document is prepared, so the initiating document
cannot carry them. They are flagged as unverified-by-source, not as errors, and they
resolve the moment a notice of case assignment lands in the matter folder.

A sixth candidate — a causes-of-action count mismatch in matter 28 — was checked and
**dismissed as a false positive**: the sentence the count came from describes the
Stockton matter, not matter 28.

## Corrections applied in this change

1. **Misfiled filing recovered (matters 27 / 29).** `matter-29/FW001 Newanforbi v
   Randstad.pdf` is a fee-waiver request whose form caption reads *Newanforbi v.
   Randstad US, LLC et al.* (Alameda Superior Court, 1225 Fallon Street). Filename
   alone was not treated as proof — the caption was read out of the PDF's form
   fields. Moved into `matter-27/` under a descriptive name and referenced in
   matter 27's record.
2. **15 byte-identical duplicates removed (matter 12).** The `001`–`020` numbered set
   was a SHA-1-identical second copy of the `1094 …` set the record already cites.
   Duplicate copies split a citation trail across two paths for the same filing; the
   cited copy was kept and the shadow copies deleted.
3. **9 real filings linked into the record.** Documents that existed on disk but were
   reachable from no matter page: matter 1 (lawsuit cover sheet, return of service),
   matter 12 (CIV-100 default request, clerk's notice to filing party, two POS-010s,
   CM-110 statement, sheriff-service packet), matter 29 (Amazon Simple Hire Checklist
   screenshot of the revoked training shift).

## Regression guard

`internal/scripts/validate-portfolio.mjs` now **fails** when two byte-identical files
sit in the same matter folder, so a duplicate copy can no longer be reintroduced
quietly. Path existence and orphan-file reporting were already enforced there.

## Reproducing

```bash
python internal/scripts/pdf-audit/extract.py   # select + extract Tier 1 PDFs (cached)
python internal/scripts/pdf-audit/ocr.py       # OCR fallback for scanned pages
python internal/scripts/pdf-audit/audit.py     # cross-check -> internal/docs/pdf_source_audit.json
```

Requires `pdfplumber`, `pypdfium2`, and `pytesseract`. Cache location defaults to
`.cache/pdf-audit/`, overridable with `PDF_AUDIT_CACHE`.

## Remaining, in leverage order

1. **Tier 2** — read all ~335 active-matter documents; the cache makes this incremental.
2. **Assignment notices** — clear the 5 unverified fields as soon as the notices are filed.
3. **Tier 3** — extend to the 194 archived-matter documents.
4. **Orphans** — 62 files on disk are still unreferenced (mostly `matter-29/lerma-v-amazon/`
   comparator-case dockets, which are reference material rather than this portfolio's filings).
