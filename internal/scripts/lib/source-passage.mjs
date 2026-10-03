// Exact textual verification is separate from legal proposition review.
export function verifySourcePassage({ quote, text, page } = {}) {
  if (typeof quote !== "string" || !quote.trim()) throw new Error("quote must be nonempty");
  if (typeof text !== "string") throw new Error("source text must be a string");
  if (page !== undefined && (!Number.isSafeInteger(page) || page < 1))
    throw new Error("page must be a positive integer");
  const pages = text.split("\f");
  // A single unpaginated extraction cannot establish a PDF page number.
  if (page !== undefined && pages.length === 1)
    return { status: "page_unverifiable", matches: [] };
  const normalize = (s) => s.normalize("NFC").replace(/\s+/gu, " ").trim();
  const needle = normalize(quote);
  const matches = [];
  for (let i = 0; i < pages.length; i++) {
    if (page !== undefined && i + 1 !== page) continue;
    const haystack = normalize(pages[i]);
    let from = 0;
    for (;;) {
      const offset = haystack.indexOf(needle, from);
      if (offset < 0) break;
      matches.push({
        extraction_page: pages.length > 1 ? i + 1 : null,
        offset,
        context: haystack.slice(Math.max(0, offset - 240), offset + needle.length + 240),
      });
      from = offset + needle.length;
    }
  }
  return {
    status: matches.length ? "matched" : "not_found",
    mode: "case_sensitive_whitespace_normalized",
    page_verified: page !== undefined && matches.length > 0,
    matches,
  };
}

export function passageReviewPacket(proposition, source, verification) {
  return {
    proposition_id: proposition.id,
    statement: proposition.statement,
    source_id: source.id,
    claimed_relationship: source.role,
    locator: source.locator,
    pinpoint: source.pinpoint,
    quotation: source.quote,
    verification,
    relationship_status: "requires_substantive_review",
    questions: [
      "Does the passage address this exact proposition, rather than a nearby issue?",
      "What limitations or exceptions appear in the surrounding text?",
      ...(source.type === "authority" ? [
        "Is this a holding, dicta, a party argument, or a quotation of another authority?",
        "Do jurisdiction, procedural posture, material facts and subsequent treatment fit?",
      ] : [
        "Who made the statement, with what personal knowledge and evidentiary foundation?",
        "Is this an allegation, testimony, admission, or judicial finding?",
      ]),
    ],
  };
}
