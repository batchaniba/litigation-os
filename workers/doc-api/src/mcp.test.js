import { describe, expect, it } from "vitest";
import worker from "./index.mjs";
import { TOOLS } from "./mcp.mjs";

const SHA = "f0b75325e925aa441cab1aaa109faaba19cb07287f95998f70b6816dad0024fd";
const DOC_PATH = "/documents/matter-24/First Amended Complaint (Doc 10, Filed Jul 15 2026).pdf";
const pdfKey = `sha256/${SHA.slice(0, 2)}/${SHA.slice(2)}.pdf`;

const MATTERS = [
  {
    number: 24,
    caption: "Newanforbi v. Serrato",
    case_no: "3:26-cv-05953-CRB",
    court: "USDC N.D. Cal.",
    phase: "mtd_briefing",
    lifecycle: "active",
    status_label: "MTD",
    judge: "Hon. Charles R. Breyer",
    next_clock_title: "Email appearance names",
    next_clock_date: "2026-11-16",
  },
  {
    number: 40,
    caption: "Brendan Ngwa Nforbi v. TaskUs / Uber",
    case_no: null,
    court: null,
    phase: "pre_filing",
    lifecycle: "pre_filing",
    status_label: "pre-filing",
    judge: null,
    next_clock_title: "Drug-test schedule expires",
    next_clock_date: "2026-09-17",
  },
];
const DOCUMENTS = [
  { sha256: SHA, path: DOC_PATH, size: 10944702, matter_number: 24 },
];
const CLOCKS = [
  { matter_number: 24, title: "Email appearance names", date: "2026-11-16", kind: "deadline" },
];

function filterLike(value, needle) {
  const n = String(needle ?? "").replaceAll("%", "").toLowerCase();
  if (!n) return true;
  return String(value ?? "").toLowerCase().includes(n);
}

function envWith({ index = { [DOC_PATH]: SHA }, d1 = true, head = true } = {}) {
  return {
    DOCS: {
      async get(key) {
        if (key === "index/path-to-sha256.json") {
          if (!index) return null;
          return { json: async () => index };
        }
        return null;
      },
      async head(key) {
        if (head && key === pdfKey) return { size: 10944702, httpEtag: '"p"' };
        return null;
      },
    },
    DB: d1
      ? {
          prepare(sql) {
            const s = String(sql);
            return {
              bind(...params) {
                return {
                  all: async () => ({ results: dispatch(s, params) }),
                };
              },
            };
          },
        }
      : undefined,
  };
}

function dispatch(sql, params) {
  if (/FROM documents d/i.test(sql)) {
    const matterFilter = /d\.matter_number = \?/.test(sql) ? Number(params[0]) : null;
    const needle = matterFilter !== null ? params[1] : params[0];
    return DOCUMENTS.filter((d) => {
      if (matterFilter !== null && d.matter_number !== matterFilter) return false;
      const caption = MATTERS.find((m) => m.number === d.matter_number)?.caption;
      return filterLike(d.path, needle) || filterLike(caption, needle);
    }).map((d) => ({
      ...d,
      caption: MATTERS.find((m) => m.number === d.matter_number)?.caption ?? null,
    }));
  }
  if (/FROM documents WHERE sha256/i.test(sql)) {
    const sha = String(params[0] ?? "").toLowerCase();
    return DOCUMENTS.filter((d) => d.sha256 === sha).map(({ path, size }) => ({ path, size }));
  }
  if (/FROM documents WHERE path/i.test(sql)) {
    return DOCUMENTS.filter((d) => d.path === params[0]).map(({ sha256 }) => ({ sha256 }));
  }
  if (/FROM documents WHERE matter_number/i.test(sql)) {
    return DOCUMENTS.filter((d) => d.matter_number === params[0]).map(({ sha256, path, size }) => ({
      sha256,
      path,
      size,
    }));
  }
  if (/FROM clocks c JOIN/i.test(sql)) {
    return CLOCKS.map((c) => {
      const m = MATTERS.find((row) => row.number === c.matter_number);
      return {
        number: c.matter_number,
        title: c.title,
        date: c.date,
        kind: c.kind,
        caption: m?.caption,
        lifecycle: m?.lifecycle,
      };
    });
  }
  if (/FROM clocks WHERE matter_number/i.test(sql)) {
    return CLOCKS.filter((c) => c.matter_number === params[0]).map(({ title, date, kind }) => ({
      title,
      date,
      kind,
    }));
  }
  if (/FROM matters WHERE number/i.test(sql)) {
    return MATTERS.filter((m) => m.number === params[0]);
  }
  if (/FROM matters ORDER BY number/i.test(sql)) return MATTERS;
  if (/FROM matters/i.test(sql)) {
    return MATTERS.map((m) => ({
      number: m.number,
      caption: m.caption,
      lifecycle: m.lifecycle,
      next_clock_title: m.next_clock_title,
      next_clock_date: m.next_clock_date,
    }));
  }
  return [];
}

async function rpc(method, params = {}, env = envWith(), id = 1) {
  const res = await worker.fetch(
    new Request("https://example.test/mcp", {
      method: "POST",
      headers: { "content-type": "application/json" },
      body: JSON.stringify({ jsonrpc: "2.0", id, method, params }),
    }),
    env,
  );
  const body = await res.json();
  return { status: res.status, body, cors: res.headers.get("access-control-allow-origin") };
}

describe("POST /mcp", () => {
  it("initializes and lists the document-store tools", async () => {
    const init = await rpc("initialize", {
      protocolVersion: "2025-03-26",
      capabilities: {},
      clientInfo: { name: "t", version: "0" },
    });
    expect(init.status).toBe(200);
    expect(init.cors).toBe("*");
    expect(init.body.result.protocolVersion).toBe("2025-03-26");
    expect(init.body.result.serverInfo.name).toBe("litigation-doc-api");

    const listed = await rpc("tools/list");
    const names = listed.body.result.tools.map((t) => t.name);
    expect(names).toEqual(TOOLS.map((t) => t.name));
    expect(names).toContain("search_documents");
    expect(names).toContain("fetch_document");
  });

  it("search_documents matches path substrings against D1", async () => {
    const { body } = await rpc("tools/call", {
      name: "search_documents",
      arguments: { query: "Serrato", limit: 10 },
    });
    const data = JSON.parse(body.result.content[0].text);
    expect(data.count).toBe(1);
    expect(data.documents[0].sha256).toBe(SHA);
    expect(data.documents[0].path).toContain("First Amended Complaint");
  });

  it("fetch_document returns public URLs instead of PDF bytes", async () => {
    const { body } = await rpc("tools/call", {
      name: "fetch_document",
      arguments: { path: DOC_PATH },
    });
    const data = JSON.parse(body.result.content[0].text);
    expect(data.sha256).toBe(SHA);
    expect(data.in_r2).toBe(true);
    expect(data.url).toBe(`https://example.test/doc/${SHA}`);
    expect(data.documents_url).toBe(`https://example.test${DOC_PATH}`);
    expect(data.size).toBe(10944702);
  });

  it("get_matter and get_fuse_board read D1", async () => {
    const matter = await rpc("tools/call", { name: "get_matter", arguments: { n: 24 } });
    const row = JSON.parse(matter.body.result.content[0].text);
    expect(row.caption).toMatch(/Serrato/);
    expect(row.document_count).toBe(1);

    const board = await rpc("tools/call", { name: "get_fuse_board", arguments: {} });
    const fuse = JSON.parse(board.body.result.content[0].text);
    expect(fuse.parked.some((m) => m.number === 40)).toBe(true);
  });

  it("marks missing required arguments as JSON-RPC invalid params", async () => {
    const { body } = await rpc("tools/call", { name: "search_documents", arguments: {} });
    expect(body.error.code).toBe(-32602);
  });

  it("returns isError when D1 is unbound", async () => {
    const { body } = await rpc(
      "tools/call",
      { name: "list_matters", arguments: {} },
      envWith({ d1: false }),
    );
    expect(body.result.isError).toBe(true);
    expect(body.result.content[0].text).toMatch(/d1_not_provisioned/);
  });

  it("GET /mcp is discovery JSON and OPTIONS is CORS preflight", async () => {
    const get = await worker.fetch(new Request("https://example.test/mcp"), envWith());
    expect(get.status).toBe(200);
    const info = await get.json();
    expect(info.endpoint).toBe("/mcp");
    expect(info.tools).toContain("search_documents");

    const opt = await worker.fetch(
      new Request("https://example.test/mcp", { method: "OPTIONS" }),
      envWith(),
    );
    expect(opt.status).toBe(204);
    expect(opt.headers.get("access-control-allow-origin")).toBe("*");
  });

  it("does not open POST on other routes", async () => {
    const res = await worker.fetch(
      new Request("https://example.test/health", { method: "POST" }),
      envWith(),
    );
    expect(res.status).toBe(405);
  });
});

describe("GET /health", () => {
  it("advertises the MCP path", async () => {
    const res = await worker.fetch(new Request("https://example.test/health"), envWith());
    expect(res.status).toBe(200);
    expect(await res.json()).toEqual({
      ok: true,
      bucket: "litigation-documents",
      mcp: "/mcp",
    });
  });
});
