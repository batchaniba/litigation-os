// GitHub webhook HMAC (X-Hub-Signature-256). Fail-closed: missing secret,
// missing header, or mismatch → false. Never treat an unsigned body as valid.

function timingSafeEqualHex(a, b) {
  const left = String(a || "").toLowerCase();
  const right = String(b || "").toLowerCase();
  const len = Math.max(left.length, right.length, 1);
  let diff = left.length === right.length ? 0 : 1;
  for (let i = 0; i < len; i++) {
    diff |= (left.charCodeAt(i) || 0) ^ (right.charCodeAt(i) || 0);
  }
  return diff === 0;
}

function bytesToHex(buf) {
  return [...new Uint8Array(buf)].map((b) => b.toString(16).padStart(2, "0")).join("");
}

export function parseSignatureHeader(header) {
  const raw = String(header || "").trim();
  if (!raw.toLowerCase().startsWith("sha256=")) return null;
  const hex = raw.slice(7).trim();
  return /^[0-9a-f]+$/i.test(hex) ? hex : null;
}

/**
 * Verify GitHub's X-Hub-Signature-256 over the raw request body.
 * @param {string|Uint8Array|ArrayBuffer} rawBody
 * @param {string|null} signatureHeader
 * @param {string|null|undefined} secret
 * @returns {Promise<boolean>}
 */
export async function verifyGitHubSignature(rawBody, signatureHeader, secret) {
  if (!secret) return false;
  const expectedHex = parseSignatureHeader(signatureHeader);
  if (!expectedHex) return false;

  const key = await crypto.subtle.importKey(
    "raw",
    new TextEncoder().encode(secret),
    { name: "HMAC", hash: "SHA-256" },
    false,
    ["sign"],
  );
  const data =
    typeof rawBody === "string"
      ? new TextEncoder().encode(rawBody)
      : rawBody instanceof Uint8Array
        ? rawBody
        : new Uint8Array(rawBody);
  const actual = await crypto.subtle.sign("HMAC", key, data);
  return timingSafeEqualHex(bytesToHex(actual), expectedHex);
}
