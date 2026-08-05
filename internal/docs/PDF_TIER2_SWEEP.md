# Tier 2 PDF Sweep — Active Matters

Every filing in the 12 active matters was read from the PDF itself: **281 documents** (46 required OCR). Text is cached under `.cache/pdf-audit`, so re-runs are incremental.

Reproduce with:

```bash
python internal/scripts/pdf-audit/tier2.py extract
python internal/scripts/pdf-audit/tier2.py audit
```

## Summary

| Check | Findings | Meaning |
| --- | --- | --- |
| link | 0 | every `documents[]` path in every active matter resolves to a real file |
| misfiled | 1 | filing whose text carries only another matter's case number |
| unreadable | 1 | no text layer and OCR produced nothing |
| mislabeled | 4 | filename claims a document type the text does not support |
| duplicate | 0 | byte-identical copies inside one matter folder (Tier 1 already cleared matter 12) |
| orphan | 8 | files in a matter folder that nothing references (6 are `.gitkeep`/subfolders) |
| deadline | 119 | hearing/trial dates printed in filings with no matching timeline entry |

## Findings that need a decision

- **Misfiled (matter 24)** — `Complaint.pdf`: text carries only another matter's case number: matter 01 (2:25-cv-01460-DC-CSK); matter 02 (26CV168913). Needs confirmation of which matter this complaint belongs to before it is moved.
- **Unreadable (matter 01)** — `01_Lawsuit_Cover_Sheet.pdf`: no usable text after extraction and OCR; content cannot be verified. A re-scan of the original is required for verification.
- **Naming (matter 01)** — `Opposition for Motion to Dismiss.pdf`: filename says 'opposition' but the text has no matching marker.
- **Naming (matter 07)** — `Notice of Supplemental Authority - Serrato Order - ELECTRONICALLY FILE`: filename says 'order' but the text has no matching marker.
- **Naming (matter 12)** — `Gmail - USPS eReceipt - Default Judgment Packet with SASE Postage (Aug`: filename says 'judgment' but the text has no matching marker.
- **Naming (matter 25)** — `Newanforbi v FedEx - Complete Filing Packet (Summons, Complaint, Notic`: filename says 'summons' but the text has no matching marker.

## Orphaned files

- matter 01: `.gitkeep`
- matter 02: `.gitkeep`
- matter 07: `.gitkeep`
- matter 12: `.gitkeep`
- matter 12: `1094 POS010 Proof of Service of Summons (Blank Form).pdf`
- matter 20: `.gitkeep`
- matter 28: `HOPE Discovery (Matter 5)`
- matter 29: `lerma-v-amazon`

## Deadline coverage

The sweep found dated hearing/trial references in the filings that the timeline does not carry, by matter: 01 (1), 02 (3), 12 (30), 20 (48), 25 (6), 26 (6), 27 (10), 28 (1), 29 (14).

This check is deliberately broad — it fires on any dated hearing reference in any filing, including dates that were later continued, dates belonging to a related action quoted in a brief, and service/packet paperwork that restates a date. It is a review queue, not a defect list. Full detail with the source filename per hit is in `pdf_tier2_audit.json`.

## What Tier 2 confirmed

- No broken document links anywhere in the active portfolio.
- No duplicate filings remaining after the Tier 1 cleanup.
- Every active matter's case number, court, and lead parties appear in its own filings, except the one misfiled complaint above.
