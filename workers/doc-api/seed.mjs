#!/usr/bin/env node
// Seed the D1 tables from the same publish projection the SPA uses.
// Emits idempotent INSERT statements to stdout — pipe to a file, then apply
// on the laptop:
//
//   node seed.mjs > seed.sql
//   wrangler d1 execute litigation-portfolio --remote --file=schema.sql
//   wrangler d1 execute litigation-portfolio --remote --file=seed.sql
//
// Public Worker / MCP reads stay open, but only this filing-safe subset lands
// in D1. The laptop graph (npm run q / npm run mcp) is not this file.

import fs from "node:fs";
import path from "node:path";
import { fileURLToPath } from "node:url";
import { listMatterSources } from "../../internal/scripts/lib/matter-layout.mjs";
import {
  REPO_ROOT,
  loadPhoneTapPaths,
  publishMatterFromDir,
} from "../../internal/scripts/lib/publish-matter.mjs";

const CLOSED_CLOCK = new Set(["satisfied", "retired", "cancelled", "canceled", "vacated"]);

const readJSON = (p) => JSON.parse(fs.readFileSync(p, "utf8"));
const lit = (v) =>
  v === null || v === undefined
    ? "NULL"
    : typeof v === "number" && Number.isFinite(v)
      ? String(v)
      : `'${String(v).replace(/'/g, "''")}'`;

const nextOpenClock = (clocks) => {
  const open = (clocks ?? []).filter(
    (c) => c && c.date && !CLOSED_CLOCK.has(String(c.status ?? "open").toLowerCase()),
  );
  open.sort(
    (a, b) => String(a.date).localeCompare(String(b.date)) || String(a.title ?? "").localeCompare(String(b.title ?? "")),
  );
  return open[0] ?? null;
};

export function buildSeedSql({ repoRoot = REPO_ROOT } = {}) {
  const mattersDir = path.join(repoRoot, "internal/src/data/matters");
  const manifest = readJSON(path.join(repoRoot, "internal/src/data/documents/manifest.json"));
  const shaByPath = new Map();
  const sizeByPath = new Map();
  for (const f of manifest.files ?? []) {
    if (!f || !f.sha256 || !f.path) continue;
    const sha = String(f.sha256).toLowerCase();
    shaByPath.set(f.path, sha);
    if (f.size != null) sizeByPath.set(f.path, f.size);
  }

  const phoneTapPaths = loadPhoneTapPaths(repoRoot);
  const sources = listMatterSources(mattersDir).filter((source) => source.layout === "split");
  const publishedMatters = sources.map((source) => publishMatterFromDir(source.dir, { phoneTapPaths }));

  const out = [];
  out.push("-- D1 seed — filing-safe publish projection. Idempotent.");
  out.push("DELETE FROM clocks;");
  out.push("DELETE FROM documents_by_path;");
  out.push("DELETE FROM documents;");

  for (const published of publishedMatters) {
    const n = published.number;
    const nc = nextOpenClock(published.clocks);
    out.push(
      `INSERT OR REPLACE INTO matters (number, caption, case_no, court, phase, status_label, judge, next_clock_title, next_clock_date, lifecycle) VALUES (` +
        [
          n,
          lit(published.caption),
          lit(published.case_no),
          lit(published.court),
          lit(published.phase),
          lit(published.status_label),
          lit(published.judge),
          lit(nc?.title ?? null),
          lit(nc?.date ?? null),
          lit(published.lifecycle),
        ].join(", ") +
        `);`,
    );

    for (const c of published.clocks ?? []) {
      if (!c || !c.date) continue;
      out.push(
        `INSERT INTO clocks (matter_number, title, date, kind, status) VALUES (${n}, ${lit(c.title)}, ${lit(c.date)}, ${lit(c.kind ?? null)}, ${lit(c.status ?? "open")});`,
      );
    }

    for (const doc of published.documents ?? []) {
      const sha = shaByPath.get(doc.path);
      if (!sha) continue;
      const mm = n;
      const size = sizeByPath.get(doc.path) ?? null;
      out.push(
        `INSERT OR REPLACE INTO documents_by_path (path, sha256, matter_number, size) VALUES (` +
          [lit(doc.path), lit(sha), mm, lit(size)].join(", ") +
          `);`,
      );
      out.push(
        `INSERT OR REPLACE INTO documents (sha256, matter_number, path, size) VALUES (` +
          [lit(sha), mm, lit(doc.path), lit(size)].join(", ") +
          `);`,
      );
    }
  }

  return out.join("\n");
}

const isMain =
  process.argv[1] && path.resolve(process.argv[1]) === fileURLToPath(import.meta.url);
if (isMain) {
  console.log(buildSeedSql({ repoRoot: REPO_ROOT }));
}
