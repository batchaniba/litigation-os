#!/usr/bin/env node
// Upload-only mirror: local PDFs → Cloudflare R2.
//
//   node internal/scripts/r2-upload.mjs --list <file>
//
// Key scheme: sha256/<first2>/<rest>.pdf (same as the 2026-09-17 migration,
// so `npm run docs:fetch <sha256>` keeps resolving). HEAD skip when ETag
// matches local MD5. After PUT, HEAD again and require the match.
// Never deletes from R2. Exits 1 if any file fails.
import fs from "node:fs";
import path from "node:path";
import { createHash } from "node:crypto";
import { headEtag, keyForSha256, putObject } from "./lib/r2-client.mjs";

const REPO_ROOT = process.env.REPO_ROOT || process.cwd();
const CONCURRENCY = 8;

if (process.argv[2] !== "--list" || !process.argv[3]) {
  console.error("usage: node internal/scripts/r2-upload.mjs --list <file>");
  process.exit(2);
}

const paths = fs
  .readFileSync(process.argv[3], "utf8")
  .split("\n")
  .map((line) => line.trim())
  .filter(Boolean);

async function processOne(rel) {
  const log = { path: rel };
  try {
    const data = fs.readFileSync(path.join(REPO_ROOT, rel));
    const sha256 = createHash("sha256").update(data).digest("hex");
    const md5hex = createHash("md5").update(data).digest("hex");
    const key = keyForSha256(sha256);
    log.size = data.length;
    log.sha256 = sha256;
    log.r2_key = key;
    if ((await headEtag(key)) === md5hex) {
      log.status = "skipped_already_present";
      return log;
    }
    let lastError;
    for (let attempt = 0; attempt < 4; attempt++) {
      try {
        await putObject(key, data);
        lastError = null;
        break;
      } catch (error) {
        lastError = error;
      }
    }
    if (lastError) throw lastError;
    if ((await headEtag(key)) !== md5hex) throw new Error("ETag mismatch after PUT");
    log.status = "uploaded";
    return log;
  } catch (error) {
    log.status = "failed";
    log.error = String(error instanceof Error ? error.message : error).slice(0, 300);
    return log;
  }
}

async function mapLimit(items, limit, fn) {
  const out = [];
  let i = 0;
  const n = Math.min(limit, items.length) || 0;
  await Promise.all(
    Array.from({ length: n }, async () => {
      while (i < items.length) {
        const idx = i++;
        out[idx] = await fn(items[idx]);
      }
    }),
  );
  return out;
}

const results = await mapLimit(paths, CONCURRENCY, processOne);
let failed = 0;
for (const log of results) {
  console.log(JSON.stringify(log));
  if (log.status === "failed") failed += 1;
}
console.error(`done: ${paths.length} files, ${failed} failed`);
process.exit(failed ? 1 : 0);
