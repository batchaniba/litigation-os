import { describe, expect, it } from "vitest";
import { handleMcp } from "./mcp.mjs";
import { sha256Hex } from "./auth.mjs";

const PUB = "a".repeat(64);
const OPEN = "c".repeat(64); // assistant-registered; public unless denylisted
const PRIV = "9c6b98a0ccf500f2894028f6b50f5e6538d4561c8f4681e9dca45858e8e2e7cc"; // D1 HOPE_000001
const PRIV_PATH =
  "/documents/matter-05/hope-discovery/HOPE_000001-031_Professional_Liability_Policy.pdf";

function env(extra = {}) {
  const tables = {
    documents_by_path: [
      { sha256: PUB, path: "/documents/matter-12/Filed Complaint.pdf", size: 1, matter_number: 12 },
    ],
    documents: [
      { sha256: PUB, path: "/documents/matter-12/Filed Complaint.pdf", size: 1, matter_number: 12 },
      { sha256: OPEN, path: "/documents/matter-12/Meet and Confer.pdf", size: 1, matter_number: 12 },
      { sha256: PRIV, path: PRIV_PATH, size: 1, matter_number: 5 },
    ],
    matters: [
      { number: 12, caption: "v. Diamond", lifecycle: "active" },
      { number: 5, caption: "v. Palacios", lifecycle: "active" },
    ],
    clocks: [],
  };
  return {
    DB: {
      prepare(sql) {
        const stmt = {
          bind(...p) {
            stmt.p = p;
            return stmt;
          },
          async all() {
            const table = /FROM\s+(\w+)/i.exec(sql)?.[1];
            if (!(table in tables)) throw new Error(`no such table: ${table}`);
            let rows = tables[table] ?? [];
            if (/WHERE sha256 = \?/.test(sql)) rows = rows.filter((r) => r.sha256 === stmt.p[0]);
            if (/WHERE matter_number = \?/.test(sql))
              rows = rows.filter((r) => r.matter_number === stmt.p[0]);
            if (/LIKE \?/.test(sql)) {
              const like = String(stmt.p[0] ?? "").replaceAll("%", "");
              rows = rows.filter(
                (r) =>
                  String(r.path ?? "").includes(like) ||
                  String(tables.matters.find((m) => m.number === r.matter_number)?.caption ?? "").includes(
                    like,
                  ),
              );
            }
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

describe("mcp reads: public catalog minus the 14-path denylist", () => {
  it("anonymous getMatterDocs includes assistant-registered public files", async () => {
    const docs = await text(await handleMcp(rpc("getMatterDocs", { n: 12 }), env()));
    expect(docs).toContain("Filed Complaint");
    expect(docs).toContain("Meet and Confer");
  });

  it("anonymous callers never see the HOPE_000 / CC-auth denylist", async () => {
    const listed = await text(await handleMcp(rpc("listDocuments", { matter: 5 }), env()));
    expect(listed).not.toContain("HOPE_000001");
    expect(listed).not.toContain(PRIV);
    const found = await text(await handleMcp(rpc("searchDocuments", { query: "hope-discovery" }), env()));
    expect(found).not.toContain(PRIV_PATH);
    expect(await text(await handleMcp(rpc("fetchDocument", { sha256: PRIV }), env()))).toMatch(/not_found/);
    expect(await text(await handleMcp(rpc("readDocumentText", { sha256: PRIV }), env()))).toMatch(/not_found/);
  });

  it("anonymous fetchDocument serves a public hash", async () => {
    expect(await text(await handleMcp(rpc("fetchDocument", { sha256: PUB }), env()))).not.toMatch(/not_found/);
    expect(await text(await handleMcp(rpc("fetchDocument", { sha256: OPEN }), env()))).not.toMatch(/not_found/);
  });

  it("a valid token sees the denylist too", async () => {
    const keys = JSON.stringify({ [await sha256Hex("tok")]: { name: "phone", scope: "r" } });
    const e = env({ API_KEYS: keys, PUBLIC_READ: "true" });
    expect(await text(await handleMcp(rpc("list_documents", { matter: 5 }, "tok"), e))).toContain(
      "HOPE_000001",
    );
  });

  it("snake_case aliases resolve", async () => {
    const listed = await text(await handleMcp(rpc("list_matters", {}), env()));
    expect(listed).toContain("v. Diamond");
  });
});
