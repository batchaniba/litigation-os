import { beforeEach, describe, expect, it, vi } from "vitest";
const state = vi.hoisted(() => ({ files: new Map(), escapes: false }));
vi.mock("./root.mjs", () => ({ REPO_ROOT: "/portfolio-test" }));
vi.mock("node:fs", () => ({ default: {
  existsSync: (p) => state.files.has(p),
  realpathSync: (p) => state.escapes && p.endsWith(".txt") ? "/outside/source.txt" : p,
  readFileSync: (p) => Buffer.from(state.files.get(p)),
} }));
import { createHash } from "node:crypto";
import { verifyPropositionSources } from "./proposition-sources.mjs";

const file = "/portfolio-test/internal/private/source-text/example.txt";
function input(extra = {}) {
  return { propositions: [{
    id: "p", statement: "Synthetic claim", factual_status: "allegation",
    proof_gaps: [], objections: [], sources: [{
      id: "s", type: "authority", role: "supports", locator: "synthetic",
      pinpoint: "1", quote: "Motion denied", text_path: "internal/private/source-text/example.txt", ...extra,
    }],
  }] };
}
const verification = (r) => r.propositions[0].source_reviews[0].verification;
describe("private extraction adapter", () => {
  beforeEach(() => { state.files.clear(); state.escapes = false; });
  it("checks quotation and pins extraction bytes separately from document identity", () => {
    state.files.set(file, "Motion denied");
    const hash = createHash("sha256").update("Motion denied").digest("hex");
    const result = verifyPropositionSources(input({ text_sha256: hash }));
    expect(verification(result).status).toBe("matched");
    expect(verification(result).version_pinned).toBe(true);
    expect(result.propositions[0].issues).toContainEqual({ code: "source_document_identity_unverified", source: "s" });
  });
  it("refuses a changed extraction", () => {
    state.files.set(file, "Motion denied");
    expect(verification(verifyPropositionSources(input({ text_sha256: "0".repeat(64) }))).status)
      .toBe("source_version_mismatch");
  });
  it("reports unavailable text without pretending the quote is wrong", () => {
    expect(verification(verifyPropositionSources(input())).status).toBe("source_text_unavailable");
  });
  it("rejects traversal and symlink escapes", () => {
    expect(() => verifyPropositionSources(input({ text_path: "../../secret.txt" }))).toThrow("source-text");
    state.files.set(file, "Motion denied");
    state.escapes = true;
    expect(() => verifyPropositionSources(input())).toThrow("symlink");
  });
  it("rejects malformed content hashes even when extraction is missing", () => {
    expect(() => verifyPropositionSources(input({ text_sha256: "invalid" }))).toThrow("64 hex");
  });
});
