import { describe, expect, it } from "vitest";
import worker from "./index.mjs";

const SHA = "f0b75325e925aa441cab1aaa109faaba19cb07287f95998f70b6816dad0024fd";
const pdfKey = `sha256/${SHA.slice(0, 2)}/${SHA.slice(2)}.pdf`;
const pdfBytes = new Uint8Array([0x25, 0x50, 0x44, 0x46, 0x2d, 0x31, 0x2e, 0x37]);
const DOC_PATH = "/documents/matter-24/First Amended Complaint (Doc 10, Filed Jul 15 2026).pdf";

// documents_by_path row marking SHA as part of the public projection (the stub
// answers every query with the same rows).
const PUBLIC = [{ sha256: SHA, ok: 1 }];

function envWith({ index, d1, apiKeys } = {}) {
  return {
    ...(apiKeys ? { API_KEYS: apiKeys, PUBLIC_READ: "true" } : {}),
    DOCS: {
      async get(key) {
        if (key === "index/path-to-sha256.json") {
          if (!index) return null;
          return { json: async () => index, httpEtag: '"i"', size: 2 };
        }
        if (key === pdfKey) {
          return { body: pdfBytes, httpEtag: '"p"', size: pdfBytes.length };
        }
        return null;
      },
    },
    DB: d1
      ? {
          prepare() {
            return {
              bind() {
                return { all: async () => ({ results: d1 }) };
              },
            };
          },
        }
      : undefined,
  };
}

describe("GET /documents/<path>", () => {
  it("serves PDF bytes from the path index and does not mark the path immutable", async () => {
    const res = await worker.fetch(
      new Request(`https://example.test${DOC_PATH}`),
      envWith({ index: { [DOC_PATH]: SHA }, d1: PUBLIC }),
    );
    expect(res.status).toBe(200);
    expect(res.headers.get("content-type")).toBe("application/pdf");
    expect(res.headers.get("cache-control")).toBe("public, max-age=60");
    expect(res.headers.get("cache-control")).not.toMatch(/immutable/);
    expect(res.headers.get("content-disposition")).toContain("First Amended Complaint");
  });

  it("falls back to D1 when the path index is missing", async () => {
    const res = await worker.fetch(
      new Request(`https://example.test${DOC_PATH}`),
      envWith({ d1: [{ sha256: SHA }] }),
    );
    expect(res.status).toBe(200);
  });

  it("returns JSON 404 with the court path when neither index nor D1 has it", async () => {
    const res = await worker.fetch(
      new Request(`https://example.test${DOC_PATH}`),
      envWith({}),
    );
    expect(res.status).toBe(404);
    const body = await res.json();
    expect(body.error).toBe("not_found");
    expect(body.path).toBe(DOC_PATH);
  });

  it("hash URLs stay immutable", async () => {
    const res = await worker.fetch(
      new Request(`https://example.test/doc/${SHA}`),
      envWith({ d1: PUBLIC }),
    );
    expect(res.status).toBe(200);
    expect(res.headers.get("cache-control")).toMatch(/immutable/);
  });
});

describe("unregistered hashes 404 for anonymous callers so /doc is not an R2 listing", () => {
  // Path index resolves the path, but D1 does not hold the hash.
  const missingEnv = (extra = {}) => envWith({ index: { [DOC_PATH]: SHA }, d1: [], ...extra });

  it.each([`/doc/${SHA}`, `/doc/${SHA}/meta`, DOC_PATH])("404s %s without a token", async (route) => {
    const res = await worker.fetch(new Request(`https://example.test${route}`), missingEnv());
    expect(res.status).toBe(404);
    expect((await res.json()).error).toBe("not_found");
  });

  it("serves the same unregistered hash to a valid read token", async () => {
    const { sha256Hex } = await import("./auth.mjs");
    const apiKeys = JSON.stringify({ [await sha256Hex("tok")]: { name: "phone", scope: "r" } });
    const res = await worker.fetch(
      new Request(`https://example.test/doc/${SHA}`, { headers: { authorization: "Bearer tok" } }),
      missingEnv({ apiKeys }),
    );
    expect(res.status).toBe(200);
  });

  it("fails closed with no D1 binding", async () => {
    const res = await worker.fetch(new Request(`https://example.test/doc/${SHA}`), envWith({}));
    expect(res.status).toBe(404);
  });
});

const OPEN = "c".repeat(64);
const PRIV = "9c6b98a0ccf500f2894028f6b50f5e6538d4561c8f4681e9dca45858e8e2e7cc";
const OPEN_PATH = "/documents/matter-12/Meet and Confer.pdf";
const PRIV_PATH =
  "/documents/matter-05/hope-discovery/HOPE_000001-031_Professional_Liability_Policy.pdf";

function r2Key(sha) {
  return `sha256/${sha.slice(0, 2)}/${sha.slice(2)}.pdf`;
}

function envCatalog({ apiKeys } = {}) {
  const tables = {
    documents_by_path: [{ sha256: SHA, path: DOC_PATH, size: 1, matter_number: 24 }],
    documents: [
      { sha256: SHA, path: DOC_PATH, size: 1, matter_number: 24 },
      { sha256: OPEN, path: OPEN_PATH, size: 1, matter_number: 12 },
      { sha256: PRIV, path: PRIV_PATH, size: 1, matter_number: 5 },
    ],
  };
  return {
    ...(apiKeys ? { API_KEYS: apiKeys, PUBLIC_READ: "true" } : {}),
    DOCS: {
      async get(key) {
        if (key === "index/path-to-sha256.json") {
          return { json: async () => ({ [DOC_PATH]: SHA }), httpEtag: '"i"', size: 2 };
        }
        if (key === r2Key(SHA) || key === r2Key(OPEN) || key === r2Key(PRIV)) {
          return { body: pdfBytes, httpEtag: '"p"', size: pdfBytes.length };
        }
        return null;
      },
      async head(key) {
        const obj = await this.get(key);
        return obj ? { size: obj.size, httpEtag: obj.httpEtag } : null;
      },
    },
    DB: {
      prepare(sql) {
        const stmt = {
          p: [],
          bind(...p) {
            stmt.p = p;
            return stmt;
          },
          async all() {
            const table = /FROM\s+(\w+)/i.exec(sql)?.[1];
            let rows = tables[table] ?? [];
            if (/WHERE sha256 = \?/.test(sql)) rows = rows.filter((r) => r.sha256 === stmt.p[0]);
            if (/WHERE path = \?/.test(sql)) rows = rows.filter((r) => r.path === stmt.p[0]);
            return { results: rows };
          },
        };
        return stmt;
      },
    },
  };
}

describe("GET /doc stays open except the 14-path denylist", () => {
  it("does not 401 an anonymous GET /doc of a public hash", async () => {
    const res = await worker.fetch(new Request(`https://example.test/doc/${SHA}`), envCatalog());
    expect(res.status).toBe(200);
  });

  it("serves an assistant-registered public file that is not in documents_by_path", async () => {
    const res = await worker.fetch(new Request(`https://example.test/doc/${OPEN}`), envCatalog());
    expect(res.status).toBe(200);
  });

  it.each([`/doc/${PRIV}`, `/doc/${PRIV}/meta`, PRIV_PATH])(
    "404s denylist %s without a token",
    async (route) => {
      const res = await worker.fetch(new Request(`https://example.test${route}`), envCatalog());
      expect(res.status).toBe(404);
      expect((await res.json()).error).toBe("not_found");
    },
  );

  it("serves the denylist hash to a valid read token", async () => {
    const { sha256Hex } = await import("./auth.mjs");
    const apiKeys = JSON.stringify({ [await sha256Hex("tok")]: { name: "phone", scope: "r" } });
    const res = await worker.fetch(
      new Request(`https://example.test/doc/${PRIV}`, { headers: { authorization: "Bearer tok" } }),
      envCatalog({ apiKeys }),
    );
    expect(res.status).toBe(200);
  });
});
