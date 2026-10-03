// Laptop-only source extraction adapter. No remote URLs or credentials.
import fs from "node:fs";
import path from "node:path";
import { createHash } from "node:crypto";
import { REPO_ROOT } from "./root.mjs";
import { auditPropositions } from "./proposition-audit.mjs";
import { verifySourcePassage, passageReviewPacket } from "./source-passage.mjs";

const inside = (root, file) => file.startsWith(root + path.sep);

function readExtraction(source) {
  if (source.text_sha256 !== undefined &&
      (typeof source.text_sha256 !== "string" || !/^[a-f0-9]{64}$/i.test(source.text_sha256)))
    throw new Error("text_sha256 must be 64 hex characters");
  if (typeof source.text_path !== "string" || !source.text_path.endsWith(".txt"))
    return { status: "source_text_unavailable", matches: [] };
  const allowed = ["internal/public/documents", "internal/private/source-text"];
  const file = path.resolve(REPO_ROOT, source.text_path);
  const dir = allowed.find((rel) => inside(path.resolve(REPO_ROOT, rel), file));
  if (!dir) throw new Error("text_path must be under a source-text directory");
  if (!fs.existsSync(file)) return { status: "source_text_unavailable", matches: [] };
  const realRoot = fs.realpathSync(path.resolve(REPO_ROOT, dir));
  const realFile = fs.realpathSync(file);
  if (!inside(realRoot, realFile)) throw new Error("source symlink escapes source-text directory");
  const bytes = fs.readFileSync(realFile);
  const digest = createHash("sha256").update(bytes).digest("hex");
  if (source.text_sha256 && source.text_sha256.toLowerCase() !== digest)
    return { status: "source_version_mismatch", text_sha256: digest, version_pinned: true, matches: [] };
  const result = verifySourcePassage({ quote: source.quote, text: bytes.toString("utf8"), page: source.page });
  return { ...result, text_path: source.text_path, text_sha256: digest,
    version_pinned: Boolean(source.text_sha256),
    identity_status: "extraction_only_document_identity_not_verified" };
}

export function verifyPropositionSources({ propositions } = {}) {
  const audit = auditPropositions({ propositions });
  const results = audit.propositions.map((p) => {
    const packets = p.sources.map((s) => passageReviewPacket(p, s, readExtraction(s)));
    const issues = [...p.issues];
    for (const packet of packets) {
      if (packet.verification.status !== "matched")
        issues.push({ code: "quotation_" + packet.verification.status, source: packet.source_id });
      if (!packet.verification.version_pinned)
        issues.push({ code: "source_version_unpinned", source: packet.source_id });
      issues.push({ code: "source_document_identity_unverified", source: packet.source_id });
    }
    return { ...p, issues, review_status: issues.length ? "needs_review" : "checks_complete", source_reviews: packets };
  });
  return {
    ...audit, propositions: results,
    summary: { total: results.length, needs_review: results.filter((p) => p.issues.length).length,
      checks_complete: results.filter((p) => !p.issues.length).length },
    limitation: "Matches establish quotation presence in an extraction, not document authenticity, legal support or admissibility. Extraction pages are not reporter or Bates pages. Substantive review remains explicit.",
  };
}
