// Node-only clocks.json crawler. Keep fs out of upcoming-from-clocks.mjs so the SPA can import it.
import fs from "node:fs";
import path from "node:path";
import { paddedMatterNumber } from "./matter-layout.mjs";

export function loadMatterClocks(mattersDir, number) {
  const file = path.join(mattersDir, paddedMatterNumber(number), "clocks.json");
  if (!fs.existsSync(file)) return [];
  const data = JSON.parse(fs.readFileSync(file, "utf8"));
  return Array.isArray(data) ? data : [];
}

export function loadAllClocks(mattersDir) {
  const byMatter = new Map();
  if (!fs.existsSync(mattersDir)) return byMatter;
  for (const entry of fs.readdirSync(mattersDir, { withFileTypes: true })) {
    if (!entry.isDirectory() || !/^\d{2}$/.test(entry.name)) continue;
    byMatter.set(Number(entry.name), loadMatterClocks(mattersDir, Number(entry.name)));
  }
  return byMatter;
}
