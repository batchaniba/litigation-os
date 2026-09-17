import { describe, expect, it } from "vitest";
import { requireRead, requireWrite, resolveAccess, sha256Hex } from "./auth.mjs";

const req = (headers = {}) => new Request("https://x/mcp", { method: "POST", headers });
const keysFor = async (token, name, scope) =>
  JSON.stringify({ [await sha256Hex(token)]: { name, scope } });

describe("auth: sha256Hex", () => {
  it("is deterministic 64-hex", async () => {
    const h = await sha256Hex("tok");
    expect(h).toMatch(/^[0-9a-f]{64}$/);
    expect(await sha256Hex("tok")).toBe(h);
    expect(await sha256Hex("tok2")).not.toBe(h);
  });
});

describe("auth: resolveAccess", () => {
  it("unconfigured -> reads open, writes hard-refused", async () => {
    const a = await resolveAccess(req(), {});
    expect(a).toMatchObject({ configured: false, canRead: true, canWrite: false });
    expect(() => requireRead(a)).not.toThrow();
    expect(() => requireWrite(a)).toThrowError(/auth_not_configured|http_503/);
  });

  it("configured -> reads locked without a token", async () => {
    const a = await resolveAccess(req(), { API_KEYS: await keysFor("t", "c", "rw") });
    expect(a.canRead).toBe(false);
    expect(() => requireRead(a)).toThrow();
  });

  it("rw token grants read + write and names the actor", async () => {
    const env = { API_KEYS: await keysFor("secret", "cursor", "rw") };
    const a = await resolveAccess(req({ authorization: "Bearer secret" }), env);
    expect(a).toMatchObject({ canRead: true, canWrite: true, actor: "cursor" });
    expect(() => requireWrite(a)).not.toThrow();
  });

  it("r token reads but cannot write", async () => {
    const env = { API_KEYS: await keysFor("ro", "readonly", "r") };
    const a = await resolveAccess(req({ authorization: "Bearer ro" }), env);
    expect(a).toMatchObject({ canRead: true, canWrite: false, actor: "readonly" });
    expect(() => requireWrite(a)).toThrow();
  });

  it("PUBLIC_READ keeps reads open while gating writes", async () => {
    const env = { API_KEYS: await keysFor("t", "c", "rw"), PUBLIC_READ: "true" };
    const a = await resolveAccess(req(), env); // no token
    expect(a.canRead).toBe(true);
    expect(a.canWrite).toBe(false);
  });

  it("unknown token is anonymous", async () => {
    const env = { API_KEYS: await keysFor("good", "c", "rw") };
    const a = await resolveAccess(req({ authorization: "Bearer wrong" }), env);
    expect(a.scope).toBeNull();
    expect(a.canWrite).toBe(false);
  });
});
