# Matter 29 First Amended Complaint draft

Private review draft only. Not filed, served, or a representation that leave to amend has been granted. Only the execution date is blank. The original complaint's name, contact block, party descriptions, and DOES 1-10 caption are preserved; the court and case number use the current federal action.

Files:
- `First_Amended_Complaint.md`: complete editable source, including the canonical signature-image reference.
- `First_Amended_Complaint.docx`: editable 28-line pleading paper with the existing signature stamp image.
- `First_Amended_Complaint.pdf`: 28-line pleading-paper PDF.
- `build_fac.py`: reproducible document-specific adapter.
- `REVIEW-NOTES.md`: reconciliation, source map, factual filing gates, and statutory verification note.

Formatter used: `internal/scripts/build_matter29_discovery_packet.py` (existing Word pleading-paper styles, numbered header, caption, signature and DOCX-to-PDF functions), and `internal/scripts/lib/pleading_paper.py` (unchanged shared ReportLab engine). The adapter imports selected functions directly from the former script's AST so its unrelated discovery/proof-of-service jobs cannot run. The existing `internal/scripts/pleading-paper-formatter-script.py` was also located and inspected; it is a filing-specific PDF script, not the Word exporter.

Signature asset: `internal/assets/signature/brendan-newanforbi-signature.png` (existing canonical photographed loops stamp). No typed electronic signature substitution. Rebuild with `python3 internal/private/research/matter-29-discovery/fac-draft/build_fac.py` using python-docx, Pillow and ReportLab. The PDF and Word contain the same complaint text; pagination may differ between renderers.

No exhibits, service certificate, leave motion, docket entry, public inventory entry, R2 publication, new PR, or merge is included. Filing requires Rule 15 consent or leave and review of the actual ruling/schedule then in effect.

Validation: all 18 PDF pages and all 17 Word-rendered pages visually inspected; all PDF pages have numbers 1-28; all 70 numbered paragraphs are present; Word body matches the source; signature image confirmed. The adapter embeds available Nimbus Times-compatible fonts to prevent PDF substitution artifacts without changing the shared engine.
