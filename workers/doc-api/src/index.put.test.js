import { describe, expect, it } from "vitest";
import worker from "./index.mjs";
import { sha256Hex } from "./auth.mjs";

const SHA = "f0b75325e925aa441cab1aaa109faaba19cb07287f95998f70b6816dad0024fd";
const pdfBytes = new Uint8Array([0x25, 0x50, 0x44, 0x46]);

// Env stub: rw API key, R2 put spy, D1 run recorder.
async function envWith() {
  const r2puts = [];
  const d1runs = [];
  const env = {
    API_KEYS: JSON.stringify({
      [await sha256Hex("secret")]: { name: "cursor", scope: "rw" },
    }),
    DOCS: {
      put: async (key, bytes, opts) => {
        r2puts.push({ key, bytes, opts });
        return { etag: '"e"' };
      },
    },
    DB: {
      prepare: (sql) => {
        const st = { sql, params: [] };
        const c = {
          bind(...p) {
            st.params = p;
            return c;
          },
          async run() {
            d1runs.push({ sql: st.sql, params: st.params });
            return { meta: { changes: 1 } };
          },
          async first() {
            return null;
          },
          async all() {
            return { results: [] };
          },
        };
        return c;
      },
    },
  };
  return { env, r2puts, d1runs };
}

const putReq = (query, body = pdfBytes) =>
  new Request(`https://example.test/doc/${SHA}${query}`, {
    method: "PUT",
    headers: {
      authorization: "Bearer secret",
      "content-type": "application/pdf",
    },
    body,
  });

describe("PUT /doc/<sha256> requires ?path=", () => {
  it("returns 400 when ?path= is missing, before touching R2 or D1", async () => {
    const { env, r2puts, d1runs } = await envWith();
    const res = await worker.fetch(putReq("?verify=false"), env);
    expect(res.status).toBe(400);
    const body = await res.json();
    expect(body.error).toMatch(/path query param is required/);
    // No bytes may be written when validation fails: a missing path used to
    // 500 after the R2 put, orphaning the object.
    expect(r2puts).toHaveLength(0);
    expect(d1runs).toHaveLength(0);
  });

  it("stores bytes, manifest row, and audit row when ?path= is present", async () => {
    const { env, r2puts, d1runs } = await envWith();
    const res = await worker.fetch(putReq("?verify=false&path=/verify/probe.pdf"), env);
    expect(res.status).toBe(201);
    const body = await res.json();
    expect(body.ok).toBe(true);
    expect(body.row.path).toBe("/verify/probe.pdf");
    expect(r2puts).toHaveLength(1);
    // D1 writes: documents upsert + audit insert.
    expect(d1runs.length).toBeGreaterThanOrEqual(2);
  });
});

describe("DELETE /doc/<sha256> is gone", () => {
  it("answers 405 even with an rw token and confirm=1, and touches nothing", async () => {
    const { env, r2puts, d1runs } = await envWith();
    let r2deletes = 0;
    env.DOCS.delete = async () => {
      r2deletes += 1;
    };
    const res = await worker.fetch(
      new Request(`https://example.test/doc/${SHA}?confirm=1`, {
        method: "DELETE",
        headers: { authorization: "Bearer secret" },
      }),
      env,
    );
    expect(res.status).toBe(405);
    expect(r2deletes).toBe(0);
    expect(r2puts).toEqual([]);
    expect(d1runs.filter((r) => /DELETE/i.test(r.sql))).toEqual([]);
  });
});
