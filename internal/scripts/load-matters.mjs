// Shared Node-side loader for matter JSON records.
// Vite uses import.meta.glob in internal/src/data/matters/index.js;
// plain Node (validate, scaffold) reads the same files via fs.
import fs from "node:fs";
import path from "node:path";
import { fileURLToPath } from "node:url";

const __dirname = path.dirname(fileURLToPath(import.meta.url));
export const MATTERS_DIR = path.resolve(__dirname, "../src/data/matters");

export function loadMatters() {
  const files = fs
    .readdirSync(MATTERS_DIR)
    .filter((name) => name.endsWith(".json"))
    .sort();

  const cases = files.map((name) => {
    const raw = fs.readFileSync(path.join(MATTERS_DIR, name), "utf8");
    const matter = JSON.parse(raw);
    matter.__sourceFile = name;
    return matter;
  });

  cases.sort((a, b) => Number(a.number) - Number(b.number));
  return cases;
}

export function matterFileName(number) {
  return `${String(number).padStart(2, "0")}.json`;
}
