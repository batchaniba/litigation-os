#!/usr/bin/env node
// ==========================================================
// Short public PDF taps → long Content-Disposition filenames.
//
// Catalog: internal/public/short-links.json
// Writes:  vercel.json
//          internal/public/_redirects
//          internal/public/_headers
//          internal/public/_routes.json
//          internal/public/{slug}/index.html
//
// vercel.json is COMMITTED (it carries git.deploymentEnabled, which Vercel
// must read from the repo at push time); the Pages files are committed so
// `npm run sync:short-links -- --check` can fail on drift, and Vite copies
// them from internal/public/ into dist/. Slug landings are gitignored and
// rebuilt by prebuild. The pre-commit hook re-runs this script when the
// catalog changes.
//
// One source of truth: do not hand-maintain a second redirect catalog.
//
// Usage:
//   npm run sync:short-links
//   npm run sync:short-links -- --check
// ==========================================================
import fs from "node:fs";
import path from "node:path";
import { fileURLToPath } from "node:url";
import { loadManifest, manifestByPath, skipDiskDocs } from "./lib/document-store.mjs";
import {
  buildPagesHeaders,
  buildPagesRedirects,
  buildPagesRoutesJson,
  buildVercelJson,
} from "./lib/spa-host.mjs";

const __dirname = path.dirname(fileURLToPath(import.meta.url));
const REPO_ROOT = path.resolve(__dirname, "../..");
const CATALOG = path.join(REPO_ROOT, "internal/public/short-links.json");
const VERCEL = path.join(REPO_ROOT, "vercel.json");
const PAGES_REDIRECTS = path.join(REPO_ROOT, "internal/public/_redirects");
const PAGES_HEADERS = path.join(REPO_ROOT, "internal/public/_headers");
const PAGES_ROUTES = path.join(REPO_ROOT, "internal/public/_routes.json");
const PUBLIC_ROOT = path.join(REPO_ROOT, "internal/public");
const checkOnly = process.argv.includes("--check");

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

if (!fs.existsSync(CATALOG)) {
  console.error(`Missing ${path.relative(process.cwd(), CATALOG)}`);
  process.exit(1);
}

const catalog = JSON.parse(fs.readFileSync(CATALOG, "utf8"));
const links = catalog.links;
// Hosted builds never have the 660 MB documents tree. Vercel already sets
// PORTFOLIO_SKIP_DISK_DOCS; Pages injects CF_PAGES=1. Treat either as skip
// so prebuild does not require the PDFs that live on R2 / origin/documents.
const skipDisk =
  skipDiskDocs() || Boolean(process.env.CF_PAGES) || Boolean(process.env.VERCEL);
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

const outputs = [
  { file: VERCEL, body: `${JSON.stringify(buildVercelJson(links), null, 2)}\n` },
  { file: PAGES_REDIRECTS, body: buildPagesRedirects(links) },
  { file: PAGES_HEADERS, body: buildPagesHeaders(links) },
  { file: PAGES_ROUTES, body: `${JSON.stringify(buildPagesRoutesJson(), null, 2)}\n` },
];
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
  for (const { file, body } of outputs) {
    if (differs(file, body)) stale.push(path.relative(process.cwd(), file));
  }
  for (const { file, body } of htmlFiles) {
    if (differs(file, body)) stale.push(path.relative(process.cwd(), file));
  }
  if (stale.length) {
    console.error(`Short-link outputs stale (${stale.join(", ")}) — run npm run sync:short-links`);
    process.exit(1);
  }
  console.log(`OK — ${links.length} short link(s) in sync (Vercel + Pages).`);
  process.exit(0);
}

for (const { file, body } of outputs) {
  fs.writeFileSync(file, body);
}
for (const { file, body } of htmlFiles) {
  fs.mkdirSync(path.dirname(file), { recursive: true });
  fs.writeFileSync(file, body);
}
console.log(
  `Wrote ${path.relative(process.cwd(), VERCEL)}, Pages _redirects/_headers/_routes.json, and ${htmlFiles.length} landing page(s) (${links.length} short link(s)).`,
);
