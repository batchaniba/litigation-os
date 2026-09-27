#!/usr/bin/env node
// Recover manifest-listed document objects from a laptop working copy into R2.
//
// Dry-run audit (default):
//   npm run documents:recover
//
// Upload every locally recoverable missing object in verified 25-file batches:
//   npm run documents:recover -- --apply --max-batches all
//
// Safe by construction: the committed manifest supplies the expected size and
// sha256; local bytes must match both before upload; R2 is HEAD-verified after
// every PUT; nothing is deleted. Progress is checkpointed after each batch.
import fs from "node:fs";
import path from "node:path";
import { createHash } from "node:crypto";
import {
  DOCUMENTS_ROOT,
  MANIFEST_PATH,
  REPO_ROOT,
  diskFromUrl,
  hashFileSha256,
  loadManifest,
} from "./lib/document-store.mjs";
import {
  assertConfigured,
  headEtag,
  keyForSha256,
  putObject,
} from "./lib/r2-client.mjs";
import { ensureTextSidecar } from "./lib/doc-text.mjs";
import { buildPathIndex } from "../../workers/doc-api/src/documents.mjs";

const PATH_INDEX_KEY = "index/path-to-sha256.json";
const DEFAULT_REPORT = path.join(REPO_ROOT, ".document-recovery", "latest.json");

function argValue(name, fallback = null) {
  const exact = process.argv.indexOf(name);
  if (exact !== -1) {
    const value = process.argv[exact + 1];
    if (!value || value.startsWith("--")) throw new Error(`${name} requires a value`);
    return value;
  }
  const prefixed = process.argv.find((token) => token.startsWith(`${name}=`));
  return prefixed ? prefixed.slice(name.length + 1) : fallback;
}

function positiveInt(raw, label) {
  const n = Number(raw);
  if (!Number.isInteger(n) || n < 1) throw new Error(`${label} must be a positive integer`);
  return n;
}

function mimeForPath(filePath) {
  const ext = path.extname(filePath).toLowerCase();
  return ({
    ".pdf": "application/pdf",
    ".json": "application/json",
    ".txt": "text/plain; charset=utf-8",
    ".md": "text/markdown; charset=utf-8",
    ".png": "image/png",
    ".jpg": "image/jpeg",
    ".jpeg": "image/jpeg",
    ".docx": "application/vnd.openxmlformats-officedocument.wordprocessingml.document",
    ".xlsx": "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
  })[ext] || "application/octet-stream";
}

function md5Hex(bytes) {
  return createHash("md5").update(bytes).digest("hex");
}

function groupManifest(files) {
  const groups = new Map();
  for (const entry of files) {
    const sha256 = String(entry?.sha256 ?? "").toLowerCase();
    if (!/^[0-9a-f]{64}$/.test(sha256)) {
      throw new Error(`invalid manifest sha256 for ${entry?.path ?? "(unknown path)"}`);
    }
    if (!groups.has(sha256)) groups.set(sha256, []);
    groups.get(sha256).push({
      path: String(entry.path),
      size: Number(entry.size),
      sha256,
    });
  }
  return groups;
}

function localCandidate(entries) {
  const mismatches = [];
  for (const entry of entries) {
    const diskPath = diskFromUrl(entry.path);
    if (!fs.existsSync(diskPath) || !fs.statSync(diskPath).isFile()) continue;
    const size = fs.statSync(diskPath).size;
    if (size !== entry.size) {
      mismatches.push({ path: entry.path, reason: "size", expected: entry.size, actual: size });
      continue;
    }
    const sha256 = hashFileSha256(diskPath);
    if (sha256 !== entry.sha256) {
      mismatches.push({ path: entry.path, reason: "sha256", expected: entry.sha256, actual: sha256 });
      continue;
    }
    return { entry, diskPath, mismatches };
  }
  return { entry: null, diskPath: null, mismatches };
}

async function mapLimit(items, limit, fn) {
  const out = new Array(items.length);
  let cursor = 0;
  await Promise.all(
    Array.from({ length: Math.min(limit, items.length) }, async () => {
      while (cursor < items.length) {
        const index = cursor++;
        out[index] = await fn(items[index], index);
      }
    }),
  );
  return out;
}

function writeReport(reportPath, report) {
  fs.mkdirSync(path.dirname(reportPath), { recursive: true });
  fs.writeFileSync(reportPath, `${JSON.stringify(report, null, 2)}\n`);
}

function summarize(rows) {
  const counts = {};
  for (const row of rows) counts[row.status] = (counts[row.status] || 0) + 1;
  return counts;
}

async function putPathIndex(manifest) {
  const index = buildPathIndex(manifest.files);
  const body = Buffer.from(`${JSON.stringify(index)}\n`, "utf8");
  await putObject(PATH_INDEX_KEY, body, { contentType: "application/json" });
  return Object.keys(index).length;
}

async function uploadOne(row) {
  const bytes = fs.readFileSync(row.local.diskPath);
  const etag = md5Hex(bytes);
  const key = keyForSha256(row.sha256);
  if ((await headEtag(key)) === etag) {
    return { ...row, status: "present_race_skip", r2_key: key };
  }
  await putObject(key, bytes, { contentType: mimeForPath(row.local.entry.path) });
  const after = await headEtag(key);
  if (after !== etag) throw new Error(`ETag mismatch after PUT for ${row.local.entry.path}`);
  let text_status = null;
  if (row.local.entry.path.toLowerCase().endsWith(".pdf")) {
    try {
      text_status = await ensureTextSidecar(row.sha256, bytes);
    } catch (error) {
      text_status = `failed: ${String(error instanceof Error ? error.message : error).slice(0, 160)}`;
    }
  }
  return { ...row, status: "uploaded", r2_key: key, text_status };
}

async function main() {
  const apply = process.argv.includes("--apply");
  const batchSize = positiveInt(argValue("--batch-size", "25"), "--batch-size");
  const maxRaw = argValue("--max-batches", "1");
  const maxBatches = maxRaw === "all" ? Infinity : positiveInt(maxRaw, "--max-batches");
  const concurrency = positiveInt(argValue("--concurrency", "8"), "--concurrency");
  const reportPath = path.resolve(argValue("--report", DEFAULT_REPORT));

  if (!fs.existsSync(DOCUMENTS_ROOT)) {
    throw new Error("local documents tree is missing; restore the laptop working copy first");
  }
  assertConfigured();
  const manifest = loadManifest(MANIFEST_PATH);
  const groups = groupManifest(manifest.files);
  const rows = await mapLimit([...groups.entries()], concurrency, async ([sha256, entries]) => {
    const sizes = new Set(entries.map((entry) => entry.size));
    if (sizes.size !== 1) {
      return { sha256, entries, status: "manifest_size_conflict" };
    }
    if (entries[0].size === 0) {
      return { sha256, entries, status: "zero_byte" };
    }
    const key = keyForSha256(sha256);
    if (await headEtag(key)) return { sha256, entries, status: "present_r2", r2_key: key };
    const local = localCandidate(entries);
    return {
      sha256,
      entries,
      local,
      status: local.entry ? "recoverable_local" : local.mismatches.length ? "local_mismatch" : "missing_local",
    };
  });

  const report = {
    generated_at: new Date().toISOString(),
    mode: apply ? "apply" : "audit",
    manifest: {
      path_count: manifest.files.length,
      unique_sha256_count: groups.size,
      total_bytes: manifest.totalBytes,
    },
    options: { batch_size: batchSize, max_batches: maxRaw, concurrency },
    summary: summarize(rows),
    batches: [],
    rows,
  };
  writeReport(reportPath, report);

  if (!apply) {
    console.log(JSON.stringify({ report: path.relative(REPO_ROOT, reportPath), ...report.summary }));
    return;
  }

  const recoverable = rows.filter((row) => row.status === "recoverable_local");
  const limit = Number.isFinite(maxBatches) ? batchSize * maxBatches : recoverable.length;
  const queue = recoverable.slice(0, limit);
  let failures = 0;
  for (let start = 0, batchNo = 1; start < queue.length; start += batchSize, batchNo += 1) {
    const batch = queue.slice(start, start + batchSize);
    const results = await mapLimit(batch, Math.min(4, concurrency), async (row) => {
      try {
        return await uploadOne(row);
      } catch (error) {
        failures += 1;
        return {
          ...row,
          status: "upload_failed",
          error: String(error instanceof Error ? error.message : error).slice(0, 300),
        };
      }
    });
    report.batches.push({ batch: batchNo, count: results.length, results });
    report.summary_after_apply = summarize(report.batches.flatMap((item) => item.results));
    writeReport(reportPath, report);
    console.log(JSON.stringify({ batch: batchNo, count: results.length, summary: summarize(results) }));
    if (failures) break;
  }

  if (!failures) {
    report.path_index_paths = await putPathIndex(manifest);
    report.completed_at = new Date().toISOString();
    writeReport(reportPath, report);
    console.log(JSON.stringify({ status: "path_index_refreshed", paths: report.path_index_paths }));
  }
  if (failures) process.exitCode = 1;
}

main().catch((error) => {
  console.error(error instanceof Error ? error.message : error);
  process.exit(1);
});
