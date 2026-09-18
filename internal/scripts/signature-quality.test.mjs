/**
 * Signature quality gate — keeps the Aug 26 wet-ink / "house" stamp dead.
 *
 * Asserts:
 *  - house source JPG and v3 bbox crop are absent
 *  - canonical PNG bytes === v2 photo-loops archive
 *  - retired extract-signature-scan.py exits non-zero
 */
import { spawnSync } from "node:child_process";
import { createHash } from "node:crypto";
import { existsSync, readFileSync } from "node:fs";
import path from "node:path";
import { fileURLToPath } from "node:url";
import { describe, expect, it } from "vitest";

const ROOT = path.resolve(path.dirname(fileURLToPath(import.meta.url)), "../..");
const SIG = path.join(ROOT, "internal/assets/signature");
const SCRIPTS = path.join(ROOT, "internal/scripts");

function sha256(p) {
  return createHash("sha256").update(readFileSync(p)).digest("hex");
}

describe("canonical signature (photo loops, not house)", () => {
  it("does not keep the wet-ink / house assets on disk", () => {
    expect(
      existsSync(path.join(SIG, "brendan-newanforbi-signature-source.jpg")),
    ).toBe(false);
    expect(
      existsSync(path.join(SIG, "brendan-newanforbi-signature-v3-bbox-crop.png")),
    ).toBe(false);
  });

  it("keeps canonical identical to the v2 photo-loops archive", () => {
    const canonical = path.join(SIG, "brendan-newanforbi-signature.png");
    const v2 = path.join(SIG, "brendan-newanforbi-signature-v2-photo-loops.png");
    expect(existsSync(canonical)).toBe(true);
    expect(existsSync(v2)).toBe(true);
    expect(sha256(canonical)).toBe(sha256(v2));
  });

  it("passes the Python pixel quality gate", () => {
    const r = spawnSync(
      "python3",
      [
        "-c",
        "import sys; sys.path.insert(0,'internal/scripts/lib'); "
        + "from signature_quality import assert_canonical_is_photo_loops, assert_house_assets_gone; "
        + "assert_house_assets_gone(); assert_canonical_is_photo_loops(); print('ok')",
      ],
      { cwd: ROOT, encoding: "utf8" },
    );
    expect(r.status, r.stderr || r.stdout).toBe(0);
    expect(r.stdout).toContain("ok");
  });

  it("refuses to run the retired wet-scan extractor", () => {
    const r = spawnSync(
      "python3",
      [path.join(SCRIPTS, "extract-signature-scan.py")],
      { cwd: ROOT, encoding: "utf8" },
    );
    expect(r.status).not.toBe(0);
    expect((r.stderr || "") + (r.stdout || "")).toMatch(/retired|house/i);
  });
});
