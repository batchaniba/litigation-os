import { describe, expect, it } from "vitest";
import worker from "./index.mjs";

const SHA = "f0b75325e925aa441cab1aaa109faaba19cb07287f95998f70b6816dad0024fd";
const pdfKey = `sha256/${SHA.slice(0, 2)}/${SHA.slice(2)}.pdf`;
const pdfBytes = new Uint8Array([0x25, 0x50, 0x44, 0x46, 0x2d, 0x31, 0x2e, 0x37]);
const DOC_PATH = "/documents/matter-24/First Amended Complaint (Doc 10, Filed Jul 15 2026).pdf";

function envWith({ index, d1 } = {}) {
  return {
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
      envWith({ index: { [DOC_PATH]: SHA } }),
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

  it("hash URLs stay immutable", async () => {
    const res = await worker.fetch(
      new Request(`https://example.test/doc/${SHA}`),
      envWith({}),
    );
    expect(res.status).toBe(200);
    expect(res.headers.get("cache-control")).toMatch(/immutable/);
  });
});
