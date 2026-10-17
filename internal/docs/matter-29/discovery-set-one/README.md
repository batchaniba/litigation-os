# Matter 29 — First Discovery Package (Amazon / Accurate)

**N.D. Cal. 4:26-cv-09249-ASK · Hon. Ajay S. Krishnan**

**STATUS: WORKING DRAFTS — NONE FILED, DELIVERED, SIGNED, OR SERVED BY THIS PR.**

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

These Markdown files preserve the full wording of the 71 discovery requests and companion working templates in an editable, diff-friendly form. **Rendered Word/PDF drafts are included in this PR** under [`generated/`](generated/) along with three combined PDFs and a downloadable ZIP archive. They were regenerated from the tracked Markdown source by [`build_matter29_discovery_packet.py`](../../../scripts/build_matter29_discovery_packet.py) and are not byte-for-byte copies of the earlier conversation renders. Verify the generated layout, caption, dates, blank signature fields, and authorized service method before use.

## Deployment protocol

1. Confirm live docket, caption, any name-conform order, and any superseding discovery restrictions.
2. **Sign each intended discovery set under Rule 26(g)** before actual service. The caption retains the docket plaintiff name; the signature block uses "Brendan Ngwa Nforbi" as requested.
3. Rule 26(d)(2) permits **early delivery** of Rule 34 requests more than 21 days after service, but they are **deemed served at the first actual Rule 26(f) conference**. Record delivery and deemed service distinctly.
4. Interrogatories and requests for admission do not use Rule 26(d)(2)'s early Rule 34 delivery mechanism. Serve when permitted by Rule 26(d), an agreement, or court order.
5. Discuss ESI scope, native production, time zones, privilege, sensitive identifiers, protective order, and report crosswalk at Rule 26(f).
6. Confirm email service authorization; informal email exchanges and ECF filing notices are not substitutes for valid service of unfiled discovery. Keep proof of transmission.
7. Send PDF versions with editable Word courtesy copies under Judge Krishnan's standing order. Discovery requests ordinarily are **served, not filed**.
8. After responses: compare Amazon status/decision logs with Accurate report transmission/access logs; confer about missing records before considering a discovery letter or Rule 30(b)(6) deposition.

## Planning dates (not confirmation of a conference)

- **Nov. 3, 2026:** Internal target to deliver the two early Rule 34 sets.
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
- No opposing counsel controls or affixes Plaintiff's signature; leave signature lines blank until Plaintiff reviews final files.
- Preserve existing pleadings, standing orders, dates, and counsel research without changing them in this PR.
- The source documents are sensitive litigation materials in a private repository. Reassess before any public export.

## Generated packet

- [Full DOCX/PDF ZIP](generated/Matter_29_Complete_Discovery_Packet_DOCX_PDF.zip)
- [Complete combined PDF](generated/Matter_29_Complete_Discovery_Packet.pdf)
- [Amazon combined PDF](generated/Matter_29_Amazon_Discovery_Combined.pdf)
- [Accurate combined PDF](generated/Matter_29_Accurate_Discovery_Combined.pdf)

Render with `python internal/scripts/build_matter29_discovery_packet.py` after installing `python-docx`, `pypdf`, and LibreOffice. GitHub Actions on the temporary PR branch generated and committed the existing files.
