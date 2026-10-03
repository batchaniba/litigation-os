# Proposition ledger — first engine increment

Private reasoning connects assertions to record passages, authorities, adverse sources, objections, and proof gaps. No public SPA, Worker, docket, clock, or case fact is changed.

## Operations

`npm run q getPropositionLedger 28` reads `internal/private/propositions/28.json`. Missing ledgers return found:false; unknown matters and mismatched ledger identities fail. The same operation is available through the laptop stdio MCP server.

`npm run q auditPropositions -- --propositions '[...]'` audits a supplied array without writing it. The laptop MCP exposes auditPropositions with the same input.

A private ledger has version:1, matter:<number>, and propositions:[...]. This first increment deliberately has no write operation or automatically populated legal conclusions. Create a ledger only after reviewing its sources.

## Proposition contract

Required: id, statement, factual_status, sources, proof_gaps, objections.

factual_status: allegation | user_report | inference | supported | disputed | judicial_finding.
An inference should include inference_reason. These labels are assertions by the author, not facts certified by this engine.

Each source requires id, type (record | authority), role (supports | opposes | context), locator, pinpoint, and quote. retrieved_at is optional YYYY-MM-DD. Locator is an identifier or path; this audit does not fetch it.

A reviewed source includes review:{reviewer, reviewed_at, reason, relationship}. Relationship is supports | opposes | context | unclear. Record review also records foundation_checked:true; authority review records proposition_fit:true, jurisdiction_fit:true, posture_fit:true, treatment_checked:true. A judicial finding requires a supporting record review with judicial_finding:true.

An objection has statement, response (optional), response_source_ids:[...]. Referenced IDs must exist in that proposition. proof_gaps is an array of nonempty descriptions.

## Output and limits

The audit preserves inputs and adds issues and review_status (needs_review | checks_complete), plus aggregate counts. Adverse sources remain a review flag even when reviewed. Missing supporting record and authority are separately flagged; a purely factual assertion may legitimately have no authority, and that flag is a review prompt rather than a legal defect.

Retrieving a real citation does not count as reviewing its application. checks_complete means the recorded checks are complete: it is not a probability, a truth finding, or permission to file. Quotes, source versions, reviewer attestations, admissibility and substantive conclusions are not independently verified yet.

## Validation

Run `npm run gate` before opening a PR or merging. The dependency-free audit received synthetic smoke checks in the implementation session; Vitest, CLI/MCP integration and the full repository gate still require a Node checkout.

## Source passage verification

Run `npm run q verifyPropositionLedger 28` to check a private ledger, or call verifyPropositionSources through CLI/laptop MCP with a propositions array. These reads never update source reviews, facts, clocks or public data.

Add text_path to each source, pointing to a .txt extraction under internal/public/documents/ or internal/private/source-text/. Existing document sidecars can be used; CourtListener/Westlaw exports can be stored in the private source-text directory. No credential or remote-fetch integration is introduced.

Optional text_sha256 pins the exact extraction bytes. The result returns the current hash for review and later pinning. An unpinned extraction is flagged; a different pinned hash refuses quotation verification. This digest is not the PDF manifest digest. Connecting extraction identity to original documents remains unverified and is always flagged.

Optional page is a positive, 1-based extraction page separated by form-feed characters. An unpaginated extraction cannot verify a supplied page number. A free-text pinpoint remains descriptive: it is not automatically mapped to reporter, docket or Bates pagination.

Matching is case-sensitive and normalizes Unicode NFC and whitespace only. Omissions, bracketed substitutions, OCR mistakes and line-wrap hyphenation do not silently pass. The result includes every match and nearby context. Source paths cannot escape the two extraction directories, including via file symlinks.

Each source returns a substantive review packet with the assertion, claimed relationship, passage context and questions about scope, qualifications, authority posture or record foundation. This is a prepared review task, not an automated legal judgment. The existing reviewer fields remain explicit and are not filled by a quotation match.

Example source fields:

```json
{
  "id": "example-source",
  "type": "authority",
  "role": "supports",
  "locator": "Your verified authority identifier",
  "pinpoint": "Your reporter page",
  "quote": "An exact quotation from the authority",
  "text_path": "internal/private/source-text/example.txt"
}
```

Six pure passage tests were executed in the implementation session. The Node filesystem adapter, CLI/MCP integration, lint and full gate require a checkout with Node and dependencies.

Five adapter tests also passed with mocked filesystem and hash dependencies in the implementation session. Real Node hashing/filesystem behavior and the Vitest runner remain unexecuted here.
