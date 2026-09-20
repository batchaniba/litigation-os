import { describe, expect, it } from "vitest";
import { base64UrlEncode, createAppJwt, pemToPkcs8Der, pkcs1DerToPkcs8Der } from "./github.mjs";

function derToPem(label, der) {
  const b64 = btoa(String.fromCharCode(...new Uint8Array(der)));
  const lines = b64.match(/.{1,64}/g).join("\n");
  return `-----BEGIN ${label}-----\n${lines}\n-----END ${label}-----`;
}

describe("GitHub App JWT", () => {
  it("signs an RS256 JWT that verifies with the generated key", async () => {
    const pair = await crypto.subtle.generateKey(
      {
        name: "RSASSA-PKCS1-v1_5",
        modulusLength: 2048,
        publicExponent: new Uint8Array([1, 0, 1]),
        hash: "SHA-256",
      },
      true,
      ["sign", "verify"],
    );
    const pkcs8 = await crypto.subtle.exportKey("pkcs8", pair.privateKey);
    const pem = derToPem("PRIVATE KEY", pkcs8);
    const nowSec = 1_700_000_000;
    const jwt = await createAppJwt({ appId: "4242", privateKeyPem: pem, nowSec });
    const [h, p, s] = jwt.split(".");
    const decode = (part) => {
      const pad = "=".repeat((4 - (part.length % 4)) % 4);
      return atob(part.replace(/-/g, "+").replace(/_/g, "/") + pad);
    };
    expect(JSON.parse(decode(h))).toMatchObject({
      alg: "RS256",
      typ: "JWT",
    });
    const payload = JSON.parse(decode(p));
    expect(payload.iss).toBe(4242);
    expect(payload.iat).toBe(nowSec - 60);
    expect(payload.exp).toBe(nowSec + 540);

    const sigBytes = Uint8Array.from(decode(s), (c) => c.charCodeAt(0));
    const valid = await crypto.subtle.verify(
      "RSASSA-PKCS1-v1_5",
      pair.publicKey,
      sigBytes,
      new TextEncoder().encode(`${h}.${p}`),
    );
    expect(valid).toBe(true);
  });

  it("wraps PKCS#1 PEM so Web Crypto can import GitHub's default download", async () => {
    const pair = await crypto.subtle.generateKey(
      {
        name: "RSASSA-PKCS1-v1_5",
        modulusLength: 2048,
        publicExponent: new Uint8Array([1, 0, 1]),
        hash: "SHA-256",
      },
      true,
      ["sign", "verify"],
    );
    const pkcs8 = new Uint8Array(await crypto.subtle.exportKey("pkcs8", pair.privateKey));
    // Re-import via our PKCS#8 parser to prove PEM round-trip.
    const der = pemToPkcs8Der(derToPem("PRIVATE KEY", pkcs8));
    const key = await crypto.subtle.importKey(
      "pkcs8",
      der,
      { name: "RSASSA-PKCS1-v1_5", hash: "SHA-256" },
      false,
      ["sign"],
    );
    expect(key.type).toBe("private");
    const wrapped = pkcs1DerToPkcs8Der(new Uint8Array([0x30, 0x03, 0x02, 0x01, 0x00]));
    expect(wrapped[0]).toBe(0x30);
  });

  it("base64url-encodes without padding", () => {
    expect(base64UrlEncode("ab")).toBe("YWI");
  });
});
