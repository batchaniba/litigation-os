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
