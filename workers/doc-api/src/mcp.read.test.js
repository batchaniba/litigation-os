import { describe, expect, it } from "vitest";
import { handleMcp } from "./mcp.mjs";
import { sha256Hex } from "./auth.mjs";

const PUB = "a".repeat(64);
const PRIV = "b".repeat(64);

// D1 stub that answers by table: documents_by_path is the seeded public
// projection, documents also holds an assistant-registered private row.
function env(extra = {}) {
  const tables = {
    documents_by_path: [{ sha256: PUB, path: "/documents/matter-12/Filed Complaint.pdf", size: 1, matter_number: 12 }],
    documents: [
      { sha256: PUB, path: "/documents/matter-12/Filed Complaint.pdf", size: 1, matter_number: 12 },
      { sha256: PRIV, path: "/documents/matter-12/CC Auth.pdf", size: 1, matter_number: 12 },
    ],
    matters: [{ number: 12, caption: "v. Diamond", lifecycle: "active" }],
    clocks: [],
  };
  return {
    DB: {
      prepare(sql) {
        const table = /FROM\s+(\w+)/i.exec(sql)[1];
        const stmt = {
          bind(...p) {
            stmt.p = p;
            return stmt;
          },
          async all() {
            let rows = tables[table] ?? [];
            if (/WHERE sha256 = \?/.test(sql)) rows = rows.filter((r) => r.sha256 === stmt.p[0]);
            return { results: rows };
          },
        };
        return stmt;
      },
    },
    DOCS: { head: async () => ({ size: 1, httpEtag: '"e"' }) },
    ...extra,
  };
}

const rpc = (name, args, token) =>
  new Request("https://x/mcp", {
    method: "POST",
    headers: { "content-type": "application/json", ...(token ? { authorization: `Bearer ${token}` } : {}) },
    body: JSON.stringify({ jsonrpc: "2.0", id: 1, method: "tools/call", params: { name, arguments: args } }),
  });

const text = async (res) => JSON.stringify(await res.json());

describe("mcp reads without a token use the filing-safe projection", () => {
  it("getMatterDocs and searchDocuments omit unpublished rows", async () => {
    const docs = await text(await handleMcp(rpc("getMatterDocs", { n: 12 }), env()));
    expect(docs).toContain("Filed Complaint");
    expect(docs).not.toContain("CC Auth");
    const found = await text(await handleMcp(rpc("searchDocuments", { query: "matter-12" }), env()));
    expect(found).not.toContain("CC Auth");
  });

  it("fetchDocument and readDocumentText refuse an unpublished hash", async () => {
    expect(await text(await handleMcp(rpc("fetchDocument", { sha256: PRIV }), env()))).toMatch(/not_found/);
    expect(await text(await handleMcp(rpc("readDocumentText", { sha256: PRIV }), env()))).toMatch(/not_found/);
    expect(await text(await handleMcp(rpc("fetchDocument", { sha256: PUB }), env()))).not.toMatch(/not_found/);
  });

  it("a valid token sees everything", async () => {
    const keys = JSON.stringify({ [await sha256Hex("tok")]: { name: "phone", scope: "r" } });
    const e = env({ API_KEYS: keys, PUBLIC_READ: "true" });
    expect(await text(await handleMcp(rpc("getMatterDocs", { n: 12 }, "tok"), e))).toContain("CC Auth");
  });
});
