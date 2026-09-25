# Matter 25 — FedEx first-wave discovery

Prepared for service after the September 25, 2026 Rule 26(f) conference in *Newanforbi v. Federal Express Corporation*, E.D. Cal. No. 2:26-cv-02881-DAD-SCR.

## Package

- 21 interrogatories to Federal Express Corporation
- 28 requests for admission
- 25 requests for production
- Rule 45(a)(4) notice concerning First Advantage Background Services Corp.
- Attachment A containing 12 document requests to First Advantage
- request to the Clerk for issuance of an AO 88B subpoena
- proposed, unsigned AO 88B subpoena
- editable DOCX and service-ready PDF versions

The official blank AO 88B source form is stored at `internal/public/documents/_form-library/AO88B-Subpoena-to-Produce-Documents.pdf`. Regenerate the package with:

```bash
python3 internal/scripts/matter25-fedex-first-wave-discovery.py
```

The generator requires `python-docx` and `pypdf`.

## Discovery design

This wave targets the record needed to test FedEx's September 24 assertion that application misrepresentations independently justified the hiring decision:

1. the exact application question and answer FedEx claims were false;
2. when FedEx first learned of the alleged misrepresentation;
3. every contemporaneous decision reason and decisionmaker;
4. Plaintiff's prior FedEx applications, hires, and comparable answers;
5. the full First Advantage report, source data, adjudication configuration, and access logs;
6. FedEx–First Advantage communications and adverse-action records;
7. the factual bases for FedEx's seventh and eighth affirmative defenses; and
8. the asserted person-at-risk justification under Penal Code section 290.46(j)(1).

## Service sequence

1. Serve the interrogatories, requests for admission, and requests for production only after the Rule 26(f) conference concludes. Do not file ordinary discovery requests unless used for a motion or ordered by the court.
2. Use email only after written consent to electronic service; otherwise use first-class mail. Complete and sign each certificate after actual service.
3. Do not serve the proposed AO 88B on First Advantage. Plaintiff must first obtain a clerk-issued subpoena under Rule 45(a)(3).
4. After issuance, serve defense counsel with the Rule 45(a)(4) notice, an exact copy of the issued subpoena, and Attachment A before serving First Advantage.
5. Have an adult nonparty serve First Advantage and complete the AO 88B proof of service.
6. If issuance or service is delayed, move the October 23, 2026 compliance date to preserve reasonable response time.

The detailed mailing and service checklist is in `00_READ_ME_SERVICE_SEQUENCE.txt`.

## Repository treatment

These are unserved working papers, not docket filings. They live under `internal/docs/` and intentionally do not alter `docket.json`, `documents.json`, the manifest, the registry, clocks, or generated catalogs. Record service and catalog final PDFs only after the actual method and date are known.
