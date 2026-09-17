#!/usr/bin/env node
// Fetch one PDF from the R2 document store by its manifest sha256.
//
//   npm run docs:fetch <sha256> [--out <path>]
//
// The key is deterministic: sha256/<first2>/<rest>.pdf — the same sha256
// recorded in internal/src/data/documents/manifest.json, so no manifest
// change is needed to fetch. Downloaded bytes are re-hashed client-side and
// the file is refused if the hash does not match.
//
// Credentials come from the environment (R2_ACCESS_KEY_ID,
// R2_SECRET_ACCESS_KEY, R2_ACCOUNT_ID, R2_BUCKET). Export them for one
// command only. Never store them in the repo.
import { createHash } from "node:crypto";
import { writeFileSync } from "node:fs";
import { assertConfigured, getObject, keyForSha256 } from "./lib/r2-client.mjs";

function usage() {
  console.error("Usage: node internal/scripts/fetch-doc.mjs <sha256> [--out <path>]");
  process.exit(2);
}

const args = process.argv.slice(2);
const sha256 = (args[0] || "").toLowerCase();
let out = null;
const outIdx = args.indexOf("--out");
if (outIdx !== -1) out = args[outIdx + 1];
if (!/^[0-9a-f]{64}$/.test(sha256) || (outIdx !== -1 && !out)) usage();

try {
  assertConfigured();
  const key = keyForSha256(sha256);
  const { body } = await getObject(key);
  const actual = createHash("sha256").update(body).digest("hex");
  if (actual !== sha256) {
    console.error(`REFUSED: R2 object ${key} hashes to ${actual}, not ${sha256}.`);
    process.exit(1);
  }
  const dest = out || `./${sha256}.pdf`;
  writeFileSync(dest, body);
  console.log(`OK — ${body.length} bytes, sha256 verified -> ${dest}`);
} catch (error) {
  console.error(error instanceof Error ? error.message : error);
  process.exit(1);
}
