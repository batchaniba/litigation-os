import { describe, expect, it, vi } from "vitest";
import {
  PAGES_DEV_HOST,
  PAGES_HEADER_LINE_LIMIT,
  PAGES_PROJECT_NAME,
  PAGES_SPA_FALLBACK,
  buildPagesHeaders,
  buildPagesRedirects,
  buildPagesRoutesJson,
  buildVercelJson,
  contentDisposition,
} from "./spa-host.mjs";
import { DOCUMENTS_ORIGIN, DOCUMENTS_WORKER_ORIGIN } from "./documents-origin.mjs";
import { vercelSpaRewrites } from "./documents-branch.mjs";
import { documentsProxyUrl, proxyDocumentsRequest } from "./pages-documents-proxy.mjs";

const sampleLinks = [
  {
    slug: "fedex-consent",
    downloadName: "Consent (E.D. Cal. 2-26-cv-02881).pdf",
  },
  {
    slug: "ups-opp",
    downloadName: "Dkt 10 - Opposition to UPS Rule 12(b)(6).pdf",
  },
];

describe("Pages project naming", () => {
  it("keeps the Vercel project slug on pages.dev", () => {
    expect(PAGES_PROJECT_NAME).toBe("interactive-litigation-portfolio");
    expect(PAGES_DEV_HOST).toBe("interactive-litigation-portfolio.pages.dev");
  });
});

describe("buildVercelJson", () => {
  it("still disables git deployments and rewrites /documents to the Worker", () => {
    const json = buildVercelJson(sampleLinks);
    expect(json.git).toEqual({ deploymentEnabled: false });
    expect(json.rewrites).toEqual(vercelSpaRewrites());
    expect(json.rewrites[0].destination).toBe(`${DOCUMENTS_ORIGIN}/:path*`);
    expect(json.redirects).toEqual([
      { source: "/fedex-consent", destination: "/fedex-consent.pdf", permanent: false },
      { source: "/fedex-consent/", destination: "/fedex-consent.pdf", permanent: false },
      { source: "/ups-opp", destination: "/ups-opp.pdf", permanent: false },
      { source: "/ups-opp/", destination: "/ups-opp.pdf", permanent: false },
    ]);
    expect(json.headers[0].source).toBe("/fedex-consent.pdf");
    expect(json.headers[0].headers[0].value).toBe(
      contentDisposition(sampleLinks[0].downloadName),
    );
  });
});

describe("buildPagesRedirects", () => {
  it("emits static slug 302s then the SPA fallback, and never 200-proxies workers.dev", () => {
    const text = buildPagesRedirects(sampleLinks);
    expect(text).toContain("/fedex-consent /fedex-consent.pdf 302");
    expect(text).toContain("/fedex-consent/ /fedex-consent.pdf 302");
    expect(text).toContain("/ups-opp /ups-opp.pdf 302");
    expect(text.trimEnd().endsWith(PAGES_SPA_FALLBACK)).toBe(true);
    const spaIndex = text.lastIndexOf(PAGES_SPA_FALLBACK);
    const lastStatic = text.lastIndexOf("/ups-opp/");
    expect(lastStatic).toBeGreaterThan(-1);
    expect(spaIndex).toBeGreaterThan(lastStatic);

    expect(text).not.toMatch(/workers\.dev.*\s200\b/);
    const rules = text.split("\n").filter((line) => line && !line.startsWith("#"));
    expect(rules.some((line) => line.startsWith("/documents"))).toBe(false);
  });
});

describe("buildPagesHeaders", () => {
  it("sets Content-Disposition on slug PDFs and noindexes *.pages.dev", () => {
    const text = buildPagesHeaders(sampleLinks);
    expect(text).toContain(`https://${PAGES_DEV_HOST}/*`);
    expect(text).toContain("X-Robots-Tag: noindex");
    expect(text).toContain("/fedex-consent.pdf");
    expect(text).toContain(contentDisposition(sampleLinks[0].downloadName));
    for (const line of text.split("\n")) {
      expect(line.length).toBeLessThanOrEqual(PAGES_HEADER_LINE_LIMIT);
    }
  });

  it("throws when a header line would exceed the Pages 2,000-character budget", () => {
    const downloadName = `${"A".repeat(PAGES_HEADER_LINE_LIMIT)}.pdf`;
    expect(() =>
      buildPagesHeaders([{ slug: "too-long", downloadName }]),
    ).toThrow(/exceeds 2000 chars/);
  });
});

describe("buildPagesRoutesJson", () => {
  it("invokes Functions only for /documents/*", () => {
    expect(buildPagesRoutesJson()).toEqual({
      version: 1,
      include: ["/documents/*"],
      exclude: [],
    });
  });
});

describe("documents Pages proxy", () => {
  const encoded =
    "https://interactive-litigation-portfolio.pages.dev/documents/matter-26/Dkt%2010%20-%2012%28b%29.pdf?download=1";

  it("preserves encoded path and query on the Worker origin", () => {
    const target = documentsProxyUrl(encoded);
    expect(target.origin).toBe(DOCUMENTS_WORKER_ORIGIN);
    expect(target.pathname).toBe("/documents/matter-26/Dkt%2010%20-%2012%28b%29.pdf");
    expect(target.search).toBe("?download=1");
  });

  it("rejects non-documents paths", () => {
    expect(() => documentsProxyUrl("https://example.com/fedex-consent.pdf")).toThrow(
      /\/documents/,
    );
  });

  it("fetches the Worker with the incoming method", async () => {
    const fetchImpl = vi.fn(async () => new Response("pdf", { status: 200 }));
    const request = new Request(encoded, { method: "GET" });
    const response = await proxyDocumentsRequest(request, fetchImpl);
    expect(response.status).toBe(200);
    expect(await response.text()).toBe("pdf");
    expect(fetchImpl).toHaveBeenCalledOnce();
    const forwarded = fetchImpl.mock.calls[0][0];
    expect(forwarded).toBeInstanceOf(Request);
    expect(new URL(forwarded.url).origin).toBe(DOCUMENTS_WORKER_ORIGIN);
    expect(forwarded.method).toBe("GET");
  });
});

describe("Pages Function entry", () => {
  it("exports onRequest that uses the documents proxy", async () => {
    const { onRequest } = await import("../../../functions/documents/[[path]].js");
    const fetchImpl = vi.fn(async () => new Response("ok", { status: 200 }));
    const originalFetch = globalThis.fetch;
    globalThis.fetch = fetchImpl;
    try {
      const response = await onRequest({
        request: new Request(
          "https://interactive-litigation-portfolio.pages.dev/documents/matter-05/a.pdf",
        ),
      });
      expect(response.status).toBe(200);
      expect(fetchImpl.mock.calls[0][0]).toBeInstanceOf(Request);
      expect(String(fetchImpl.mock.calls[0][0].url)).toContain(
        "litigation-doc-api.ss8sxswwkt.workers.dev/documents/matter-05/a.pdf",
      );
    } finally {
      globalThis.fetch = originalFetch;
    }
  });
});
