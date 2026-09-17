import { describe, expect, it } from "vitest";
import { handleMcp } from "./mcp.mjs";
import { sha256Hex } from "./auth.mjs";

// D1 stub: SELECT ... WHERE number returns a matter; run() writes are recorded.
function d1Stub() {
  const runs = [];
  function chain(sql) {
    const st = { sql, params: [] };
    const c = {
      bind(...p) {
        st.params = p;
        return c;
      },
      async run() {
        runs.push({ sql: st.sql, params: st.params });
        return { meta: { changes: 1 } };
      },
      async first() {
        return /FROM matters WHERE number/.test(st.sql) ? { number: 27 } : null;
      },
      async all() {
        return { results: [] };
      },
    };
    return c;
  }
  return { DB: { prepare: (sql) => chain(sql) }, runs };
}

const call = (name, args) => ({
  jsonrpc: "2.0",
  id: 1,
  method: "tools/call",
  params: { name, arguments: args },
});

const post = (body, token) =>
  new Request("https://x/mcp", {
    method: "POST",
    headers: {
      "content-type": "application/json",
      ...(token ? { authorization: `Bearer ${token}` } : {}),
    },
    body: JSON.stringify(body),
  });

async function keys(token, scope = "rw") {
  return JSON.stringify({ [await sha256Hex(token)]: { name: "cursor", scope } });
}

describe("mcp write gate", () => {
  it("refuses a write tool when API_KEYS is not configured", async () => {
    const { DB } = d1Stub();
    const res = await handleMcp(post(call("updateMatter", { n: 27, status_label: "x" })), { DB });
    const j = await res.json();
    expect(j.error.code).toBe(-32003);
    expect(j.error.message).toMatch(/API_KEYS/);
  });

  it("refuses a write tool without an rw token", async () => {
    const { DB } = d1Stub();
    const env = { DB, API_KEYS: await keys("secret", "r") };
    const res = await handleMcp(post(call("updateMatter", { n: 27, status_label: "x" }), "secret"), env);
    const j = await res.json();
    expect(j.error.code).toBe(-32003);
    expect(j.error.message).toMatch(/rw scope/);
  });

  it("allows an rw token, applies the write, and records an audit row", async () => {
    const { DB, runs } = d1Stub();
    const env = { DB, API_KEYS: await keys("secret", "rw") };
    const res = await handleMcp(post(call("updateMatter", { n: 27, status_label: "$25k final demand" }), "secret"), env);
    const j = await res.json();
    expect(j.error).toBeUndefined();
    const payload = JSON.parse(j.result.content[0].text);
    expect(payload).toMatchObject({ number: 27, updated: ["status_label"] });
    expect(runs.some((r) => /UPDATE matters SET/.test(r.sql))).toBe(true);
    expect(runs.some((r) => /INSERT INTO audit/.test(r.sql))).toBe(true);
  });

  it("still serves reads with no token when unconfigured", async () => {
    const { DB } = d1Stub();
    const res = await handleMcp(post(call("listMatters", {})), { DB });
    const j = await res.json();
    expect(j.error).toBeUndefined();
    expect(JSON.parse(j.result.content[0].text)).toEqual([]);
  });

  it("locks reads when API_KEYS is set and no token is sent", async () => {
    const { DB } = d1Stub();
    const env = { DB, API_KEYS: await keys("secret", "rw") };
    const res = await handleMcp(post(call("listMatters", {})), env);
    const j = await res.json();
    expect(j.error.code).toBe(-32003);
  });
});
