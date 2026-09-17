// Minimal Cloudflare R2 client — node builtins only (no dependencies).
//
// Reads credentials from the environment (never from the repo):
//   R2_ACCESS_KEY_ID, R2_SECRET_ACCESS_KEY, R2_ACCOUNT_ID
//   R2_BUCKET (defaults to "litigation-documents")
//
// In CI these come from GitHub Actions secrets. For local/agent use they are
// handed over per task and never stored. This module never prints them.
//
// Document keys are content-addressed: keyForSha256(h) ===
//   `sha256/<first2 hex>/<remaining hex>.pdf`
// which is deterministic from the sha256 in internal/src/data/documents/manifest.json.
import { createHash, createHmac } from "node:crypto";
import { request as httpsRequest } from "node:https";

const ACCOUNT = process.env.R2_ACCOUNT_ID;
const BUCKET = process.env.R2_BUCKET || "litigation-documents";
const ACCESS_KEY = process.env.R2_ACCESS_KEY_ID;
const SECRET_KEY = process.env.R2_SECRET_ACCESS_KEY;
const HOST = ACCOUNT ? `${ACCOUNT}.r2.cloudflarestorage.com` : null;
const REGION = "auto"; // R2 accepts "auto" as the SigV4 region

export function keyForSha256(sha256) {
  const h = sha256.toLowerCase();
  if (!/^[0-9a-f]{64}$/.test(h)) throw new Error("expected a 64-char hex sha256");
  return `sha256/${h.slice(0, 2)}/${h.slice(2)}.pdf`;
}

export function assertConfigured() {
  const missing = [
    ["R2_ACCESS_KEY_ID", ACCESS_KEY],
    ["R2_SECRET_ACCESS_KEY", SECRET_KEY],
    ["R2_ACCOUNT_ID", ACCOUNT],
  ]
    .filter(([, v]) => !v)
    .map(([k]) => k);
  if (missing.length) {
    throw new Error(
      `R2 credentials not configured (missing ${missing.join(", ")}). ` +
        `In CI these are GitHub Actions secrets; locally, export them for one command only.`
    );
  }
}

function sha256Hex(data) {
  return createHash("sha256").update(data).digest("hex");
}
function hmacSha256(key, data) {
  return createHmac("sha256", key).update(data).digest();
}

function amzDates(now = new Date()) {
  const p = (n) => String(n).padStart(2, "0");
  const short = `${now.getUTCFullYear()}${p(now.getUTCMonth() + 1)}${p(now.getUTCDate())}`;
  const amz =
    `${short}T${p(now.getUTCHours())}${p(now.getUTCMinutes())}${p(now.getUTCSeconds())}Z`;
  return { short, amz };
}

function signRequest(method, key, payload, dates) {
  const payloadHash = sha256Hex(payload);
  const canonicalUri = `/${BUCKET}/${key.split("/").map(encodeURIComponent).join("/")}`;
  const canonicalHeaders =
    `host:${HOST}\nx-amz-content-sha256:${payloadHash}\nx-amz-date:${dates.amz}\n`;
  const signedHeaders = "host;x-amz-content-sha256;x-amz-date";
  const canonicalRequest = [
    method, canonicalUri, "", canonicalHeaders, signedHeaders, payloadHash,
  ].join("\n");
  const scope = `${dates.short}/${REGION}/s3/aws4_request`;
  const stringToSign = ["AWS4-HMAC-SHA256", dates.amz, scope, sha256Hex(canonicalRequest)].join("\n");
  const kDate = hmacSha256(`AWS4${SECRET_KEY}`, dates.short);
  const kRegion = hmacSha256(kDate, REGION);
  const kService = hmacSha256(kRegion, "s3");
  const kSigning = hmacSha256(kService, "aws4_request");
  const signature = hmacSha256(kSigning, stringToSign).toString("hex");
  return {
    Authorization:
      `AWS4-HMAC-SHA256 Credential=${ACCESS_KEY}/${scope}, ` +
      `SignedHeaders=${signedHeaders}, Signature=${signature}`,
    "x-amz-date": dates.amz,
    "x-amz-content-sha256": payloadHash,
  };
}

function r2Request(method, key, body = Buffer.alloc(0)) {
  assertConfigured();
  return new Promise((resolve, reject) => {
    const dates = amzDates();
    const headers = signRequest(method, key, body, dates);
    const path = `/${BUCKET}/${key.split("/").map(encodeURIComponent).join("/")}`;
    const req = httpsRequest({ host: HOST, path, method, headers }, (res) => {
      const chunks = [];
      res.on("data", (c) => chunks.push(c));
      res.on("end", () => resolve({ status: res.statusCode, body: Buffer.concat(chunks) }));
      res.on("error", reject);
    });
    req.on("error", reject);
    req.setTimeout(120000, () => req.destroy(new Error("R2 request timed out")));
    if (body.length) req.write(body);
    req.end();
  });
}

/** GET one object. Throws on non-200. Returns { status, body }. */
export async function getObject(key) {
  const res = await r2Request("GET", key);
  if (res.status !== 200) throw new Error(`R2 GET ${key}: HTTP ${res.status}`);
  return res;
}

/** HEAD one object. Returns true if it exists, false on 404. Throws otherwise. */
export async function objectExists(key) {
  const res = await r2Request("HEAD", key);
  if (res.status === 200) return true;
  if (res.status === 404) return false;
  throw new Error(`R2 HEAD ${key}: HTTP ${res.status}`);
}
