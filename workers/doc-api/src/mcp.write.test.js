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
    // HTTP-level auth challenge (MCP / RFC 9728): OAuth-capable clients use
    // the WWW-Authenticate header to discover the authorization server.
    expect(res.status).toBe(401);
    expect(res.headers.get("www-authenticate")).toMatch(
      /Bearer resource_metadata=".*\/\.well-known\/oauth-protected-resource"/,
    );
    const j = await res.json();
    expect(j.error).toBe("unauthorized");
  });

  it("challenges an anonymous write with HTTP 401 + WWW-Authenticate", async () => {
    const { DB } = d1Stub();
    const env = { DB, API_KEYS: await keys("secret", "rw") };
    const res = await handleMcp(post(call("addClock", { matter_number: 27, title: "x" })), env);
    expect(res.status).toBe(401);
    const wah = res.headers.get("www-authenticate");
    expect(wah).toBe('Bearer resource_metadata="https://x/.well-known/oauth-protected-resource"');
    const j = await res.json();
    expect(j.error).toBe("unauthorized");
    expect(j.error_description).toMatch(/oauth-protected-resource/);
  });

  it("challenges a batch containing a write, but not a pure read batch", async () => {
    const { DB } = d1Stub();
    const env = { DB, API_KEYS: await keys("secret", "rw") };
    const mixed = await handleMcp(
      post([
        { jsonrpc: "2.0", id: 1, method: "tools/list", params: {} },
        call("addClock", { matter_number: 27, title: "x" }),
      ]),
      env,
    );
    expect(mixed.status).toBe(401);
    const readsOnly = await handleMcp(post([{ jsonrpc: "2.0", id: 1, method: "tools/list", params: {} }]), env);
    expect(readsOnly.status).toBe(200);
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

describe("mcp uploadDocument", () => {
  // R2 stub: records puts (key, byte size, content type).
  function r2Stub() {
    const puts = [];
    const DOCS = {
      async put(key, buf, opts) {
        puts.push({ key, size: buf.byteLength, contentType: opts?.httpMetadata?.contentType });
      },
      async head() {
        return null;
      },
      async delete() {},
    };
    return { DOCS, puts };
  }

  const helloB64 = Buffer.from("hello world").toString("base64");
  const helloSha = "b94d27b9934d3e08a52e52d7da7dabfac484efe37a5380ee9088f7ace2efcde9";

  it("uploads bytes, registers the manifest row, and returns the sha256 + URL", async () => {
    const { DB, runs } = d1Stub();
    const { DOCS, puts } = r2Stub();
    const env = { DB, DOCS, API_KEYS: await keys("secret", "rw") };
    const res = await handleMcp(
      post(
        call("uploadDocument", {
          content_base64: helloB64,
          path: "/documents/matter-27/_test-upload.txt",
          matter_number: 27,
          content_type: "text/plain",
        }),
        "secret",
      ),
      env,
    );
    const j = await res.json();
    expect(j.error).toBeUndefined();
    const payload = JSON.parse(j.result.content[0].text);
    expect(payload).toMatchObject({
      ok: true,
      sha256: helloSha,
      size: 11,
      matter_number: 27,
      path: "/documents/matter-27/_test-upload.txt",
    });
    expect(payload.url).toBe(`https://x/doc/${helloSha}`);
    expect(puts).toHaveLength(1);
    expect(puts[0].key).toBe(`sha256/${helloSha.slice(0, 2)}/${helloSha.slice(2)}.pdf`);
    expect(puts[0].contentType).toBe("text/plain");
    expect(runs.some((r) => /INSERT INTO documents/.test(r.sql))).toBe(true);
  });

  it("redacts the base64 payload from the audit row", async () => {
    const { DB, runs } = d1Stub();
    const { DOCS } = r2Stub();
    const env = { DB, DOCS, API_KEYS: await keys("secret", "rw") };
    const res = await handleMcp(
      post(call("uploadDocument", { content_base64: helloB64, path: "/x.pdf" }), "secret"),
      env,
    );
    const j = await res.json();
    expect(j.error).toBeUndefined();
    const audit = runs.find((r) => /INSERT INTO audit/.test(r.sql));
    expect(audit).toBeDefined();
    const detail = JSON.stringify(audit.params);
    expect(detail).not.toContain(helloB64);
    expect(detail).toContain("[redacted");
  });

  it("refuses without an rw token", async () => {
    const { DB } = d1Stub();
    const { DOCS } = r2Stub();
    const env = { DB, DOCS, API_KEYS: await keys("secret", "r") };
    const res = await handleMcp(
      post(call("uploadDocument", { content_base64: helloB64, path: "/x.pdf" }), "secret"),
      env,
    );
    // HTTP 401 + WWW-Authenticate challenge (not a bare JSON-RPC error), so
    // OAuth-only clients can discover the authorization server and sign in.
    expect(res.status).toBe(401);
    expect(res.headers.get("www-authenticate")).toContain("Bearer resource_metadata=");
    const j = await res.json();
    expect(j.error).toBe("unauthorized");
  });

  it("rejects invalid and empty base64", async () => {
    const { DB, runs } = d1Stub();
    const { DOCS, puts } = r2Stub();
    const env = { DB, DOCS, API_KEYS: await keys("secret", "rw") };
    for (const bad of ["!!!not-base64!!!", ""]) {
      const res = await handleMcp(
        post(call("uploadDocument", { content_base64: bad, path: "/x.pdf" }), "secret"),
        env,
      );
      const j = await res.json();
      expect(j.error.code).toBe(-32602);
    }
    expect(puts).toHaveLength(0);
    expect(runs.some((r) => /INSERT INTO documents/.test(r.sql))).toBe(false);
  });
});

describe("mcp exposes no delete tools", () => {
  it("lists no delete* tool even to an rw token", async () => {
    const { DB } = d1Stub();
    const env = { DB, API_KEYS: await keys("secret", "rw") };
    const res = await handleMcp(post({ jsonrpc: "2.0", id: 1, method: "tools/list", params: {} }, "secret"), env);
    const names = (await res.json()).result.tools.map((t) => t.name);
    expect(names).toContain("uploadDocument");
    expect(names.filter((n) => /^delete/i.test(n))).toEqual([]);
  });

  it.each(["deleteDocument", "deleteMatter", "deleteClock"])("rejects %s as an unknown tool", async (name) => {
    const { DB } = d1Stub();
    const env = { DB, API_KEYS: await keys("secret", "rw") };
    const res = await handleMcp(
      post(call(name, { sha256: "a".repeat(64), n: 27, matter_number: 27, title: "x", confirm: true }), "secret"),
      env,
    );
    const j = await res.json();
    expect(j.error?.message ?? j.result?.content?.[0]?.text ?? "").toMatch(/unknown tool/);
  });
});
