import { describe, expect, it } from "vitest";
import {
  deleteMatter,
  patchMatter,
  putDocBytes,
  upsertDocumentRow,
  upsertMatter,
} from "./writes.mjs";

// Minimal D1 stub: records run() writes and answers first() via firstImpl.
function d1Stub(firstImpl) {
  const runs = [];
  const batches = [];
  function chain(sql) {
    const st = { sql, params: [] };
    const c = {
      __st: st,
      bind(...p) {
        st.params = p;
        return c;
      },
      async run() {
        runs.push({ sql: st.sql, params: st.params });
        return { meta: { changes: 1 } };
      },
      async first() {
        return firstImpl ? firstImpl(st.sql, st.params) : null;
      },
      async all() {
        return { results: [] };
      },
    };
    return c;
  }
  const DB = {
    prepare: (sql) => chain(sql),
    async batch(list) {
      batches.push(list.map((c) => ({ sql: c.__st.sql, params: c.__st.params })));
      return list.map(() => ({}));
    },
  };
  return { DB, runs, batches };
}

function r2Stub() {
  const puts = [];
  const dels = [];
  return {
    DOCS: {
      async put(k, v) {
        puts.push({ k, size: v.byteLength ?? v.length });
      },
      async delete(k) {
        dels.push(k);
      },
    },
    puts,
    dels,
  };
}

const SHA_A = "a".repeat(64);

describe("writes: matters", () => {
  it("upsertMatter INSERTs with ON CONFLICT and binds the number first", async () => {
    const { DB, runs } = d1Stub();
    const out = await upsertMatter({ DB }, { number: 27, status_label: "x", lifecycle: "active" });
    expect(out.number).toBe(27);
    expect(runs).toHaveLength(1);
    expect(runs[0].sql).toMatch(/INSERT INTO matters/);
    expect(runs[0].sql).toMatch(/ON CONFLICT\(number\) DO UPDATE/);
    expect(runs[0].params[0]).toBe(27);
  });

  it("upsertMatter rejects an unknown field", async () => {
    const { DB } = d1Stub();
    await expect(upsertMatter({ DB }, { number: 1, bogus: 1 })).rejects.toMatchObject({ status: 400 });
  });

  it("upsertMatter rejects a bad lifecycle and bad date", async () => {
    const { DB } = d1Stub();
    await expect(upsertMatter({ DB }, { number: 1, lifecycle: "zzz" })).rejects.toMatchObject({ status: 400 });
    await expect(upsertMatter({ DB }, { number: 1, next_clock_date: "2026/01/01" })).rejects.toMatchObject({ status: 400 });
  });

  it("patchMatter 404s when the matter is unknown", async () => {
    const { DB } = d1Stub(() => null); // SELECT returns nothing
    await expect(patchMatter({ DB }, 99, { status_label: "y" })).rejects.toMatchObject({ status: 404 });
  });

  it("patchMatter updates only the provided columns", async () => {
    const { DB, runs } = d1Stub((sql) => (/WHERE number = \?/.test(sql) ? { number: 27 } : null));
    const out = await patchMatter({ DB }, 27, { status_label: "$25k final demand" });
    expect(out).toMatchObject({ number: 27, updated: ["status_label"] });
    const update = runs.find((r) => /UPDATE matters SET/.test(r.sql));
    expect(update.sql).toMatch(/status_label = \?/);
    expect(update.params).toEqual(["$25k final demand", 27]);
  });

  it("patchMatter rejects an empty patch", async () => {
    const { DB } = d1Stub(() => ({ number: 27 }));
    await expect(patchMatter({ DB }, 27, {})).rejects.toMatchObject({ status: 400 });
  });
});

describe("writes: deleteMatter", () => {
  const counts = (docs, clocks) => (sql) => {
    if (/FROM matters WHERE number/.test(sql)) return { number: 27 };
    if (/FROM documents/.test(sql)) return { c: docs };
    if (/FROM clocks/.test(sql)) return { c: clocks };
    return null;
  };

  it("refuses a non-empty matter without cascade (409)", async () => {
    const { DB } = d1Stub(counts(3, 1));
    await expect(deleteMatter({ DB }, 27)).rejects.toMatchObject({ status: 409 });
  });

  it("cascades when asked, batching the child deletes", async () => {
    const { DB, batches } = d1Stub(counts(3, 1));
    const out = await deleteMatter({ DB }, 27, { cascade: true });
    expect(out).toMatchObject({ deleted: true, cascade: true, removed_documents: 3, removed_clocks: 1 });
    expect(batches[0]).toHaveLength(3); // matters + clocks + documents
  });

  it("deletes an empty matter without cascade", async () => {
    const { DB, batches } = d1Stub(counts(0, 0));
    await expect(deleteMatter({ DB }, 27)).resolves.toMatchObject({ deleted: true });
    expect(batches[0]).toHaveLength(1);
  });
});

describe("writes: documents", () => {
  it("upsertDocumentRow INSERTs with ON CONFLICT(sha256)", async () => {
    const { DB, runs } = d1Stub();
    await upsertDocumentRow({ DB }, { sha256: SHA_A, matter_number: 26, path: "/documents/matter-26/x.pdf", size: 10 });
    expect(runs[0].sql).toMatch(/INSERT INTO documents/);
    expect(runs[0].sql).toMatch(/ON CONFLICT\(sha256\)/);
    expect(runs[0].params).toEqual([SHA_A, 26, "/documents/matter-26/x.pdf", 10]);
  });

  it("putDocBytes rejects a sha256 that does not match the bytes", async () => {
    const { DOCS } = r2Stub();
    const bytes = new TextEncoder().encode("hello");
    await expect(putDocBytes({ DOCS }, SHA_A, bytes)).rejects.toMatchObject({ status: 400 });
  });

  it("putDocBytes stores when the hash matches (verify) ", async () => {
    const bytes = new TextEncoder().encode("hello world");
    const digest = await crypto.subtle.digest("SHA-256", bytes);
    const sha = [...new Uint8Array(digest)].map((b) => b.toString(16).padStart(2, "0")).join("");
    const { DOCS, puts } = r2Stub();
    const out = await putDocBytes({ DOCS }, sha, bytes);
    expect(out).toMatchObject({ sha256: sha, size: bytes.byteLength });
    expect(puts[0].k).toBe(`sha256/${sha.slice(0, 2)}/${sha.slice(2)}.pdf`);
  });

  it("putDocBytes with verify=false skips the hash check", async () => {
    const { DOCS, puts } = r2Stub();
    const bytes = new TextEncoder().encode("mismatch");
    await expect(putDocBytes({ DOCS }, SHA_A, bytes, { verify: false })).resolves.toMatchObject({ sha256: SHA_A });
    expect(puts).toHaveLength(1);
  });

  it("putDocBytes rejects an empty body", async () => {
    const { DOCS } = r2Stub();
    await expect(putDocBytes({ DOCS }, SHA_A, new Uint8Array(0), { verify: false })).rejects.toMatchObject({ status: 400 });
  });
});
