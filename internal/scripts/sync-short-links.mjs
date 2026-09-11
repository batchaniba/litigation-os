#!/usr/bin/env node
// ==========================================================
// Short public PDF taps → long Content-Disposition filenames.
//
// Catalog: internal/public/short-links.json
// Writes:  vercel.json  and  internal/public/{slug}/index.html
//
// Usage:
//   npm run sync:short-links
//   npm run sync:short-links -- --check
// ==========================================================
import fs from "node:fs";
import path from "node:path";
import { fileURLToPath } from "node:url";
import { loadManifest, manifestByPath, skipDiskDocs } from "./lib/document-store.mjs";
import { vercelSpaRewrites } from "./lib/documents-branch.mjs";

const __dirname = path.dirname(fileURLToPath(import.meta.url));
const REPO_ROOT = path.resolve(__dirname, "../..");
const CATALOG = path.join(REPO_ROOT, "internal/public/short-links.json");
const VERCEL = path.join(REPO_ROOT, "vercel.json");
const PUBLIC_ROOT = path.join(REPO_ROOT, "internal/public");
const checkOnly = process.argv.includes("--check");

function contentDisposition(downloadName) {
  const quoted = downloadName.replace(/\\/g, "\\\\").replace(/"/g, '\\"');
  const encoded = encodeURIComponent(downloadName).replace(
    /[()]/g,
    (ch) => `%${ch.charCodeAt(0).toString(16).toUpperCase()}`,
  );
  return `attachment; filename="${quoted}"; filename*=UTF-8''${encoded}`;
}

function landingHtml(link) {
  const href = `../${link.slug}.pdf`;
  const title = link.title || link.downloadName;
  return `<!doctype html>
<html lang="en">
  <head>
    <meta charset="utf-8" />
    <meta name="viewport" content="width=device-width, initial-scale=1" />
    <title>${escapeHtml(title)}</title>
    <meta http-equiv="refresh" content="0;url=${href}" />
    <script>
      location.replace(${JSON.stringify(href)});
    </script>
  </head>
  <body>
    <p>
      <a href="${href}" download="${escapeHtml(link.downloadName)}"
        >Download ${escapeHtml(link.downloadName)}</a
      >
    </p>
  </body>
</html>
`;
}

function escapeHtml(value) {
  return String(value)
    .replaceAll("&", "&amp;")
    .replaceAll("<", "&lt;")
    .replaceAll(">", "&gt;")
    .replaceAll('"', "&quot;");
}

function buildVercelJson(links) {
  const redirects = [];
  const headers = [];
  for (const link of links) {
    const dest = `/${link.slug}.pdf`;
    redirects.push({ source: `/${link.slug}`, destination: dest, permanent: false });
    redirects.push({ source: `/${link.slug}/`, destination: dest, permanent: false });
    headers.push({
      source: dest,
      headers: [{ key: "Content-Disposition", value: contentDisposition(link.downloadName) }],
    });
  }
  return {
    redirects,
    headers,
    rewrites: vercelSpaRewrites(),
  };
}

if (!fs.existsSync(CATALOG)) {
  console.error(`Missing ${path.relative(process.cwd(), CATALOG)}`);
  process.exit(1);
}

const catalog = JSON.parse(fs.readFileSync(CATALOG, "utf8"));
const links = catalog.links;
const skipDisk = skipDiskDocs();
const documentManifestByPath = manifestByPath(loadManifest());
if (!Array.isArray(links) || links.length === 0) {
  console.error("short-links.json must have a non-empty links array");
  process.exit(1);
}

const slugRe = /^[a-z0-9]+(?:-[a-z0-9]+)*$/;
const seen = new Set();
for (const link of links) {
  if (!link?.slug || !slugRe.test(link.slug)) {
    console.error(`Invalid short-link slug: ${JSON.stringify(link?.slug)}`);
    process.exit(1);
  }
  if (seen.has(link.slug)) {
    console.error(`Duplicate short-link slug: ${link.slug}`);
    process.exit(1);
  }
  seen.add(link.slug);
  if (!link.source || !link.downloadName) {
    console.error(`short-link "${link.slug}" needs source and downloadName`);
    process.exit(1);
  }
  if (!link.downloadName.endsWith(".pdf")) {
    console.error(`short-link "${link.slug}" downloadName must end in .pdf`);
    process.exit(1);
  }
  const pdfPath = path.join(PUBLIC_ROOT, `${link.slug}.pdf`);
  if (!fs.existsSync(pdfPath)) {
    console.error(`Missing ${path.relative(process.cwd(), pdfPath)} — generator must copy the packet to this slug`);
    process.exit(1);
  }
  const sourcePath = path.join(PUBLIC_ROOT, link.source.replace(/^\//, ""));
  if (skipDisk && String(link.source).startsWith("/documents/")) {
    if (!documentManifestByPath.has(link.source)) {
      console.error(`Missing catalog source in document manifest: ${link.source}`);
      process.exit(1);
    }
  } else if (!fs.existsSync(sourcePath)) {
    console.error(`Missing catalog source ${path.relative(process.cwd(), sourcePath)}`);
    process.exit(1);
  }
}

const vercelPayload = `${JSON.stringify(buildVercelJson(links), null, 2)}\n`;
const htmlFiles = links.map((link) => ({
  file: path.join(PUBLIC_ROOT, link.slug, "index.html"),
  body: landingHtml(link),
}));

function differs(file, body) {
  if (!fs.existsSync(file)) return true;
  return fs.readFileSync(file, "utf8") !== body;
}

if (checkOnly) {
  const stale = [];
  if (!fs.existsSync(VERCEL) || fs.readFileSync(VERCEL, "utf8") !== vercelPayload) {
    stale.push("vercel.json");
  }
  for (const { file, body } of htmlFiles) {
    if (differs(file, body)) stale.push(path.relative(process.cwd(), file));
  }
  if (stale.length) {
    console.error(`Short-link outputs stale (${stale.join(", ")}) — run npm run sync:short-links`);
    process.exit(1);
  }
  console.log(`OK — ${links.length} short link(s) in sync.`);
  process.exit(0);
}

fs.writeFileSync(VERCEL, vercelPayload);
for (const { file, body } of htmlFiles) {
  fs.mkdirSync(path.dirname(file), { recursive: true });
  fs.writeFileSync(file, body);
}
console.log(
  `Wrote ${path.relative(process.cwd(), VERCEL)} and ${htmlFiles.length} landing page(s) (${links.length} short link(s)).`,
);
