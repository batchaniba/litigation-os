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
// Clock status is open | set | contingent | vacated | satisfied
// (internal/scripts/lib/clock-status.mjs). overdue is derived, never seeded.

import fs from "node:fs";
import { execFileSync } from "node:child_process";
import path from "node:path";
import { fileURLToPath } from "node:url";
import { listMatterSources } from "../../internal/scripts/lib/matter-layout.mjs";
import {
  REPO_ROOT,
  loadPhoneTapPaths,
  publishMatterFromDir,
} from "../../internal/scripts/lib/publish-matter.mjs";
import { isClosedClockStatus } from "../../internal/scripts/lib/clock-status.mjs";
import { isPrivateDocument } from "../../internal/scripts/lib/private-documents.mjs";

const readJSON = (p) => JSON.parse(fs.readFileSync(p, "utf8"));
const lit = (v) =>
  v === null || v === undefined
    ? "NULL"
    : typeof v === "number" && Number.isFinite(v)
      ? String(v)
      : `'${String(v).replace(/'/g, "''")}'`;

const nextOpenClock = (clocks) => {
  const open = (clocks ?? []).filter(
    (c) => c && c.date && !isClosedClockStatus(c.status),
  );
  open.sort(
    (a, b) => String(a.date).localeCompare(String(b.date)) || String(a.title ?? "").localeCompare(String(b.title ?? "")),
  );
  return open[0] ?? null;
};

// Which commit the projection was built from. "-dirty" when tracked matter or
// manifest files differ from HEAD, so a seed from uncommitted data is visible.
export function sourceCommit(repoRoot = REPO_ROOT) {
  try {
    const sha = execFileSync("git", ["rev-parse", "HEAD"], { cwd: repoRoot, encoding: "utf8" }).trim();
    const dirty = execFileSync(
      "git",
      ["status", "--porcelain", "--", "internal/src/data/matters", "internal/src/data/documents/manifest.json"],
      { cwd: repoRoot, encoding: "utf8" },
    ).trim();
    return dirty ? `${sha}-dirty` : sha;
  } catch {
    return "unknown";
  }
}

/**
 * The exact rows D1 should hold: the filing-safe publish projection of every
 * split matter. Shared by buildSeedSql (writes D1) and audit-mirror (diffs
 * live D1 against it), so the two cannot disagree about what "correct" is.
 */
export function buildProjection({ repoRoot = REPO_ROOT } = {}) {
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

  const matters = [];
  const clocks = [];
  const documents = [];
  for (const published of publishedMatters) {
    const n = published.number;
    const nc = nextOpenClock(published.clocks);
    matters.push({
      number: n,
      caption: published.caption ?? null,
      case_no: published.case_no ?? null,
      court: published.court ?? null,
      phase: published.phase ?? null,
      status_label: published.status_label ?? null,
      judge: published.judge ?? null,
      next_clock_title: nc?.title ?? null,
      next_clock_date: nc?.date ?? null,
      lifecycle: published.lifecycle ?? null,
    });
    for (const c of published.clocks ?? []) {
      if (!c || !c.date) continue;
      clocks.push({
        matter_number: n,
        title: c.title ?? null,
        date: c.date,
        kind: c.kind ?? null,
        status: c.status ?? "open",
      });
    }
    for (const doc of published.documents ?? []) {
      const sha = shaByPath.get(doc.path);
      if (!sha) continue;
      if (isPrivateDocument({ path: doc.path, sha256: sha })) continue;
      documents.push({ path: doc.path, sha256: sha, matter_number: n, size: sizeByPath.get(doc.path) ?? null });
    }
  }
  return { matters, clocks, documents };
}

export function buildSeedSql({
  repoRoot = REPO_ROOT,
  commit = sourceCommit(repoRoot),
  seededAt = new Date().toISOString(),
} = {}) {
  const { matters, clocks, documents } = buildProjection({ repoRoot });

  const out = [];
  out.push("-- D1 seed — filing-safe publish projection. Idempotent; replaces every row.");
  // One line each: POST /admin/reseed applies INSERT / DELETE / CREATE TABLE IF NOT EXISTS lines.
  out.push("CREATE TABLE IF NOT EXISTS meta (key TEXT PRIMARY KEY, value TEXT);");
  out.push("DELETE FROM meta;");
  out.push("DELETE FROM clocks;");
  out.push("DELETE FROM documents_by_path;");
  out.push("DELETE FROM documents;");
  // Matters too: without this a matter removed from the repo (or a write-test
  // row) survived every reseed.
  out.push("DELETE FROM matters;");

  for (const m of matters) {
    out.push(
      `INSERT OR REPLACE INTO matters (number, caption, case_no, court, phase, status_label, judge, next_clock_title, next_clock_date, lifecycle) VALUES (` +
        [
          m.number,
          lit(m.caption),
          lit(m.case_no),
          lit(m.court),
          lit(m.phase),
          lit(m.status_label),
          lit(m.judge),
          lit(m.next_clock_title),
          lit(m.next_clock_date),
          lit(m.lifecycle),
        ].join(", ") +
        `);`,
    );
  }
  for (const c of clocks) {
    out.push(
      `INSERT INTO clocks (matter_number, title, date, kind, status) VALUES (${c.matter_number}, ${lit(c.title)}, ${lit(c.date)}, ${lit(c.kind)}, ${lit(c.status)});`,
    );
  }
  for (const d of documents) {
    out.push(
      `INSERT OR REPLACE INTO documents_by_path (path, sha256, matter_number, size) VALUES (` +
        [lit(d.path), lit(d.sha256), d.matter_number, lit(d.size)].join(", ") +
        `);`,
    );
    out.push(
      `INSERT OR REPLACE INTO documents (sha256, matter_number, path, size) VALUES (` +
        [lit(d.sha256), d.matter_number, lit(d.path), lit(d.size)].join(", ") +
        `);`,
    );
  }
  out.push(`INSERT INTO meta (key, value) VALUES ('source_commit', ${lit(commit)});`);
  out.push(`INSERT INTO meta (key, value) VALUES ('seeded_at', ${lit(seededAt)});`);

  return out.join("\n");
}

const isMain =
  process.argv[1] && path.resolve(process.argv[1]) === fileURLToPath(import.meta.url);
if (isMain) {
  console.log(buildSeedSql({ repoRoot: REPO_ROOT }));
}
