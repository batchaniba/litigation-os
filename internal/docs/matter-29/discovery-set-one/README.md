# Matter 29 — First Discovery Package (Amazon / Accurate)

**N.D. Cal. 4:26-cv-09249-ASK · Magistrate Judge Ajay S. Krishnan**

**STATUS: WORKING DRAFTS DATED OCTOBER 20, 2026 WITH SIGNATURE IMAGE AFFIXED — NONE FILED, DELIVERED, OR SERVED BY THIS PR.**

## Packet contents

| Document | Type | Count | Timing |
|---|---|---:|---|
| 00_README_Deployment_and_Checklist.md | Deployment checklist | — | Review before service |
| 01_Amazon_RFP_Set_One.md | Rule 34 requests | 18 | May be delivered early under Rule 26(d)(2) |
| 02_Accurate_RFP_Set_One.md | Rule 34 requests | 20 | Same |
| 03_Amazon_Interrogatories_Set_One.md | Rule 33 | 8 | At or after actual Rule 26(f) conference |
| 04_Accurate_Interrogatories_Set_One.md | Rule 33 | 9 | Same |
| 05_Amazon_RFA_Set_One.md | Rule 36 | 8 | At or after actual Rule 26(f) conference |
| 06_Accurate_RFA_Set_One.md | Rule 36 | 8 | Same |
| 07_Rule_26f_ESI_Proposal.md | Conference discussion proposal | — | Not binding |
| 08_Amazon_30b6_Draft_HOLD.md | Deposition outline | — | Do not serve before refinement |
| 09_Accurate_30b6_Draft_HOLD.md | Deposition outline | — | Do not serve before refinement |
| 10_Amazon_Service_Record.md | Record template | — | Complete upon delivery/service |
| 11_Accurate_Service_Record.md | Record template | — | Same |
| 12_Cover_Email_Templates_NOT_SENT.txt | Communications drafts | — | Never automatically send |

**Total:** 38 RFPs, 17 interrogatories, 16 RFAs = **71 requests**.

These Markdown files preserve the full wording of the 71 discovery requests and companion working templates in an editable, diff-friendly form. **Rendered Word/PDF drafts are included in this PR** under [`generated/`](generated/) along with three combined PDFs and a downloadable ZIP archive, built by [`build_matter29_discovery_packet.py`](../../../scripts/build_matter29_discovery_packet.py):

- **Word (.docx):** pleading paper for Microsoft Word — Times New Roman 12 pt, exact 24-pt lines, 28 line numbers in a header-anchored text box, header rule lines, named "Pleading …" styles, inline signature image, no macros, tracked changes, or comments; author Brendan Ngehsi Newanforbi.
- **PDF:** each DOCX is read back and rendered through the portfolio pleading-paper formatter (`internal/scripts/lib/pleading_paper.py`, the engine behind `pleading-paper-formatter-script.py`), with the Civil L.R. 3-4 first page (party block at line 1, court title from line 8, caption, case number, document title) and the title/case-number footer.
- **Proofs of service:** the portfolio federal POS template (`internal/scripts/lib/proof_of_service.py`) is appended to each discovery set; `10_`/`11_` PDFs collect them per defendant. RFP proofs are dated and signed October 20, 2026; interrogatory and RFA proofs stay undated and unsigned. Verify the generated layout, caption, dates, signature image placement, and authorized service method before use.

## Deployment protocol

1. Confirm live docket, caption, any name-conform order, and any superseding discovery restrictions.
2. **Each discovery set is signed under Rule 26(g)** with Plaintiff's portfolio signature image above the typed name "Brendan Ngehsi Newanforbi" (matching the caption) and dated October 20, 2026.
3. Rule 26(d)(2) permits **early delivery** of Rule 34 requests more than 21 days after service, but they are **deemed served at the first actual Rule 26(f) conference**. Record delivery and deemed service distinctly.
4. Interrogatories and requests for admission do not use Rule 26(d)(2)'s early Rule 34 delivery mechanism. Serve when permitted by Rule 26(d), an agreement, or court order.
5. Discuss ESI scope, native production, time zones, privilege, sensitive identifiers, protective order, and report crosswalk at Rule 26(f).
6. Confirm email service authorization; informal email exchanges and ECF filing notices are not substitutes for valid service of unfiled discovery. Keep proof of transmission.
7. Send PDF versions with editable Word courtesy copies under Magistrate Judge Krishnan's standing order. Discovery requests ordinarily are **served, not filed**.
8. After responses: compare Amazon status/decision logs with Accurate report transmission/access logs; confer about missing records before considering a discovery letter or Rule 30(b)(6) deposition.

## Planning dates (not confirmation of a conference)

- **Oct. 20, 2026:** Signature date; internal target to deliver the two early Rule 34 sets (21 days before the Nov. 10 target).
- **Nov. 10:** Portfolio's Rule 26(f) and ADR target; **actual conference date not yet confirmed**.
- **Nov. 18:** Amazon partial motion hearing (Claims 5–7).
- **Nov. 24:** Portfolio lists initial disclosures and joint CMC statement.
- **Dec. 1:** Initial case-management conference.
- **Dec. 10:** Illustrative Rule 34 response date **only if** the first Rule 26(f) conference occurs Nov. 10 and no altered deadline applies.

## Highest-value records

Amazon: ATS/shift change history, reason codes, first access to screening findings, intake records, adverse-action workflows.

Accurate: report versions, furnishing/access logs, alias provenance, Santa Clara retrieval history, Oct. 13 package review, and source records for the recorded conviction answer.

## Repository notes

- Do not merge as evidence of service, delivery, admission, or executed signing.
- No opposing counsel controls or affixes Plaintiff's signature. The build script affixes Plaintiff's own signature image (`internal/assets/signature/brendan-newanforbi-signature.png`) to every `[[SIGNATURE]]` marker in the Markdown sources.
- Preserve existing pleadings, standing orders, dates, and counsel research without changing them in this PR.
- The source documents are sensitive litigation materials in a private repository. Reassess before any public export.

## Generated packet

- [Full DOCX/PDF ZIP](generated/Matter_29_Complete_Discovery_Packet_DOCX_PDF.zip)
- [Complete combined PDF](generated/Matter_29_Complete_Discovery_Packet.pdf)
- [Amazon combined PDF](generated/Matter_29_Amazon_Discovery_Combined.pdf)
- [Accurate combined PDF](generated/Matter_29_Accurate_Discovery_Combined.pdf)

Render with `python internal/scripts/build_matter29_discovery_packet.py` after installing `python-docx`, `pypdf`, and LibreOffice. Requires `python-docx`, `pypdf`, `reportlab`; LibreOffice renders only the internal 00 checklist.
