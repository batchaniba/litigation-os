#!/usr/bin/env node
// Backup audit: how many *verified* copies does each manifest document have?
//
// Counts copies by content hash, never by filename or file count:
//   r2        bytes fetched through the doc-api Worker (GET /doc/<sha256>,
//             no keys needed) and re-hashed locally
//   documents blobs anywhere in the `documents` branch history (git), re-hashed.
//             History counts: the branch was emptied on 2026-09-17 but its
//             commits still hold the bytes.
//   main      files tracked on the current checkout (root PDFs, phone-tap
//             slugs), re-hashed
//
// Exit 1 when any manifest hash has fewer than --min-copies verified copies
// (default 2), or when any R2 object is missing or hashes to something else.
//
//   NODE_USE_ENV_PROXY=1 npm run audit:backup                 # full re-hash (~1.1 GB)
//   npm run audit:backup -- --meta-only                       # existence + size only
//   npm run audit:backup -- --out report.json --concurrency 8
//   npm run audit:backup -- --documents-ref origin/documents  # default
import crypto from "node:crypto";
import fs from "node:fs";
import path from "node:path";
import { execFileSync } from "node:child_process";
import { fileURLToPath } from "node:url";

const ROOT = path.resolve(path.dirname(fileURLToPath(import.meta.url)), "../..");
const MANIFEST = path.join(ROOT, "internal/src/data/documents/manifest.json");
const DEFAULT_API = "https://litigation-doc-api.ss8sxswwkt.workers.dev";

const args = process.argv.slice(2);
function opt(name, fallback = null) {
  const hit = args.find((a) => a === name || a.startsWith(`${name}=`));
  if (!hit) return fallback;
  if (hit.includes("=")) return hit.split("=").slice(1).join("=");
  const next = args[args.indexOf(hit) + 1];
  return next && !next.startsWith("--") ? next : true;
}

const API = String(opt("--api", process.env.DOC_API_URL || DEFAULT_API)).replace(/\/+$/, "");
const META_ONLY = Boolean(opt("--meta-only", false));
const MIN_COPIES = Number(opt("--min-copies", 2));
const CONCURRENCY = Math.max(1, Number(opt("--concurrency", 6)));
const DOCUMENTS_REF = String(opt("--documents-ref", "origin/documents"));
const OUT = opt("--out", null);

const sha256 = (buf) => crypto.createHash("sha256").update(buf).digest("hex");

function git(argv, opts = {}) {
  return execFileSync("git", argv, { cwd: ROOT, maxBuffer: 1 << 30, ...opts });
}

/** Manifest entries grouped by content hash. */
export function manifestByHash(manifest) {
  const byHash = new Map();
  for (const f of manifest.files ?? []) {
    if (!f?.sha256) continue;
    const entry = byHash.get(f.sha256) ?? { sha256: f.sha256, size: f.size ?? null, paths: [] };
    entry.paths.push(f.path);
    byHash.set(f.sha256, entry);
  }
  return byHash;
}

/**
 * Hash blobs reachable from a git ref and keep the ones the manifest wants.
 * history=false: only the ref's current tree. history=true: every blob in
 * the ref's history (a deleted file is still recoverable with git).
 */
function gitCopies(ref, wanted, label, { history = false } = {}) {
  let blobs;
  try {
    const listing = history
      ? git(["rev-list", "--objects", ref], { encoding: "utf8" })
      : git(["ls-tree", "-r", ref], { encoding: "utf8" });
    const ids = history
      ? listing.split("\n").map((l) => l.split(" ")[0]).filter(Boolean)
      : listing
          .split("\n")
          .map((l) => /^\d+ blob ([0-9a-f]{40})\t/.exec(l)?.[1])
          .filter(Boolean);
    const types = git(["cat-file", "--batch-check=%(objecttype) %(objectname)"], {
      input: `${ids.join("\n")}\n`,
      encoding: "utf8",
    });
    blobs = types
      .split("\n")
      .filter((l) => l.startsWith("blob "))
      .map((l) => l.slice(5));
  } catch {
    return { available: false, label, hashes: new Map() };
  }
  // One `git cat-file --batch` for all blobs; output is "<id> blob <size>\n<bytes>\n" each.
  const out = git(["cat-file", "--batch"], { input: `${blobs.join("\n")}\n` });
  const hashes = new Map();
  let pos = 0;
  for (const id of blobs) {
    const nl = out.indexOf(10, pos);
    const size = Number(out.subarray(pos, nl).toString("utf8").split(" ")[2]);
    const h = sha256(out.subarray(nl + 1, nl + 1 + size));
    if (wanted.has(h)) hashes.set(h, id);
    pos = nl + 1 + size + 1;
  }
  return { available: true, label, hashes };
}

async function r2Check(entry) {
  const url = `${API}/doc/${entry.sha256}${META_ONLY ? "/meta" : ""}`;
  for (let attempt = 1; ; attempt++) {
    try {
      const res = await fetch(url);
      if (res.status === 404) return { status: "missing" };
      if (!res.ok) throw new Error(`HTTP ${res.status}`);
      if (META_ONLY) {
        const meta = await res.json();
        const sizeOk = entry.size == null || meta.size === entry.size;
        return { status: sizeOk ? "present" : "size_mismatch", size: meta.size };
      }
      const hash = crypto.createHash("sha256");
      let size = 0;
      for await (const chunk of res.body) {
        hash.update(chunk);
        size += chunk.length;
      }
      const got = hash.digest("hex");
      return { status: got === entry.sha256 ? "verified" : "hash_mismatch", size, got };
    } catch (err) {
      if (attempt >= 3) return { status: "error", error: String(err?.message || err) };
      await new Promise((r) => setTimeout(r, 1000 * attempt));
    }
  }
}

async function mapLimit(items, limit, fn, onProgress) {
  const out = new Array(items.length);
  let next = 0;
  let done = 0;
  await Promise.all(
    Array.from({ length: Math.min(limit, items.length) }, async () => {
      while (next < items.length) {
        const i = next++;
        out[i] = await fn(items[i]);
        done += 1;
        onProgress?.(done, items.length);
      }
    }),
  );
  return out;
}

async function main() {
  const manifest = JSON.parse(fs.readFileSync(MANIFEST, "utf8"));
  const byHash = manifestByHash(manifest);
  const entries = [...byHash.values()];
  const wanted = new Set(byHash.keys());

  const docsBranch = gitCopies(DOCUMENTS_REF, wanted, "documents", { history: true });
  const mainTree = gitCopies("HEAD", wanted, "main");

  const r2 = await mapLimit(entries, CONCURRENCY, r2Check, (d, n) => {
    if (d % 100 === 0 || d === n) process.stderr.write(`r2 ${d}/${n}\n`);
  });

  const rows = entries.map((e, i) => {
    const r2ok = r2[i].status === "verified" || (META_ONLY && r2[i].status === "present");
    const copies = [
      r2ok ? "r2" : null,
      docsBranch.hashes.has(e.sha256) ? "documents" : null,
      mainTree.hashes.has(e.sha256) ? "main" : null,
    ].filter(Boolean);
    return { sha256: e.sha256, paths: e.paths, size: e.size, r2: r2[i], copies };
  });

  const count = (pred) => rows.filter(pred).length;
  const summary = {
    generated: new Date().toISOString(),
    manifest_entries: manifest.files?.length ?? 0,
    unique_hashes: rows.length,
    mode: META_ONLY ? "meta-only (existence + size)" : "full re-hash",
    min_copies: MIN_COPIES,
    r2: {
      verified: count((r) => r.r2.status === "verified" || r.r2.status === "present"),
      missing: count((r) => r.r2.status === "missing"),
      mismatched: count((r) => /mismatch/.test(r.r2.status)),
      errors: count((r) => r.r2.status === "error"),
    },
    documents_branch_history: docsBranch.available ? docsBranch.hashes.size : "unavailable",
    main_tree: mainTree.hashes.size,
    copies_histogram: rows.reduce((h, r) => ((h[r.copies.length] = (h[r.copies.length] ?? 0) + 1), h), {}),
    below_min_copies: count((r) => r.copies.length < MIN_COPIES),
    only_copy_in_r2: count((r) => r.copies.length === 1 && r.copies[0] === "r2"),
  };

  const problems = rows.filter((r) => r.copies.length < MIN_COPIES || r.r2.status !== "verified");
  const report = { summary, problems: problems.map(({ sha256, paths, r2, copies }) => ({ sha256, paths, r2: r2.status, copies })) };
  if (OUT) fs.writeFileSync(OUT, `${JSON.stringify(report, null, 2)}\n`);
  else process.stdout.write(`${JSON.stringify(summary, null, 2)}\n`);

  const r2Bad = summary.r2.missing + summary.r2.mismatched + summary.r2.errors;
  if (r2Bad > 0 || summary.below_min_copies > 0) {
    process.stderr.write(
      `audit:backup FAILED — ${r2Bad} hash(es) not verified in R2; ` +
        `${summary.below_min_copies} below ${MIN_COPIES} verified copies.\n`,
    );
    process.exit(1);
  }
  process.stderr.write("audit:backup OK\n");
}

if (process.argv[1] && path.resolve(process.argv[1]) === fileURLToPath(import.meta.url)) {
  main().catch((err) => {
    process.stderr.write(`audit:backup error: ${err?.stack || err}\n`);
    process.exit(2);
  });
}
