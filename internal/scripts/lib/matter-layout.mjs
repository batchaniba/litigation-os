// Discover whether a matter lives as NN.json (legacy) or NN/ (split).
import fs from "node:fs";
import path from "node:path";
import {
  EVENTS_FILE,
  SPLIT_JSON_FILES,
  SPLIT_OPTIONAL_JSON,
  assembleSplitMatter,
  paddedMatterNumber,
} from "../../src/data/matters/assembleMatter.js";

export {
  EVENTS_FILE,
  GRAPH_LIMITS,
  MATTER_JSON_BUDGET,
  SPLIT_JSON_FILES,
  assembleSplitMatter,
  paddedMatterNumber,
} from "../../src/data/matters/assembleMatter.js";

export function readJson(filePath) {
  return JSON.parse(fs.readFileSync(filePath, "utf8"));
}

export function splitMatterDir(mattersDir, number) {
  return path.join(mattersDir, paddedMatterNumber(number));
}

export function legacyMatterPath(mattersDir, number) {
  return path.join(mattersDir, `${paddedMatterNumber(number)}.json`);
}

export function isSplitMatterDir(dir) {
  return fs.existsSync(path.join(dir, "matter.json"));
}

export function listMatterSources(mattersDir) {
  const entries = fs.readdirSync(mattersDir, { withFileTypes: true });
  const sources = [];

  for (const entry of entries) {
    if (entry.isFile() && /^\d{2}\.json$/.test(entry.name)) {
      sources.push({
        number: Number(entry.name.slice(0, 2)),
        layout: "legacy",
        rel: entry.name,
        abs: path.join(mattersDir, entry.name),
      });
      continue;
    }
    if (entry.isDirectory() && /^\d{2}$/.test(entry.name)) {
      const dir = path.join(mattersDir, entry.name);
      if (!isSplitMatterDir(dir)) continue;
      sources.push({
        number: Number(entry.name),
        layout: "split",
        rel: `${entry.name}/matter.json`,
        abs: path.join(dir, "matter.json"),
        dir,
      });
    }
  }

  sources.sort((a, b) => a.number - b.number);
  return sources;
}

export function loadJsonIfPresent(filePath) {
  if (!fs.existsSync(filePath)) return undefined;
  return readJson(filePath);
}

export function loadSplitParts(dir) {
  const parts = { matter: readJson(path.join(dir, "matter.json")) };
  for (const name of SPLIT_JSON_FILES) {
    if (name === "matter.json") continue;
    const key = name.replace(/\.json$/, "");
    const value = loadJsonIfPresent(path.join(dir, name));
    if (value !== undefined) parts[key] = value;
  }
  for (const name of SPLIT_OPTIONAL_JSON) {
    const key = name.replace(/\.json$/, "");
    const value = loadJsonIfPresent(path.join(dir, name));
    if (value !== undefined) parts[key] = value;
  }
  const eventsPath = path.join(dir, EVENTS_FILE);
  if (fs.existsSync(eventsPath)) {
    parts.eventsPath = eventsPath;
  }
  return parts;
}

export function loadSplitMatter(dir) {
  const assembled = assembleSplitMatter(loadSplitParts(dir));
  assembled.__sourceFile = `${paddedMatterNumber(assembled.number)}/matter.json`;
  assembled.__sourceDir = dir;
  return assembled;
}

export function writeJson(filePath, value) {
  fs.mkdirSync(path.dirname(filePath), { recursive: true });
  fs.writeFileSync(filePath, `${JSON.stringify(value, null, 2)}\n`);
}

export function matterRecordPath(mattersDir, number, layout) {
  return layout === "split"
    ? path.join(splitMatterDir(mattersDir, number), "matter.json")
    : legacyMatterPath(mattersDir, number);
}

export function docketPath(mattersDir, number) {
  return path.join(splitMatterDir(mattersDir, number), "docket.json");
}
