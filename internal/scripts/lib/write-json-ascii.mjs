// ==========================================================
// Write JSON the way timeline.json is stored: 2-space indent,
// ensure_ascii so em-dashes stay as \u2014. Python's serializer
// is a byte-for-byte match for this repo's checked-in snapshots;
// Node's JSON.stringify is not.
// ==========================================================
import { spawnSync } from "node:child_process";
import fs from "node:fs";

export function dumpJsonAscii(data) {
  const py = spawnSync(
    "python3",
    ["-c", "import json,sys; sys.stdout.write(json.dumps(json.load(sys.stdin), indent=2, ensure_ascii=True) + '\\n')"],
    { input: JSON.stringify(data), encoding: "utf8", maxBuffer: 32 * 1024 * 1024 },
  );
  if (py.status !== 0) {
    throw new Error(py.stderr || `python3 json dump failed (status ${py.status})`);
  }
  return py.stdout;
}

export function writeJsonAscii(filePath, data) {
  fs.writeFileSync(filePath, dumpJsonAscii(data));
}
