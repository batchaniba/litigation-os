import type { Matter } from "../../types/portfolio";

// Matter records live as one JSON file per matter under this folder.
// Edit `NN.json` (or run `npm run scaffold:matter`) — do not reintroduce a monolith.
const modules = import.meta.glob<{ default: Matter }>("./*.json", { eager: true });

export const cases: Matter[] = Object.values(modules)
  .map((mod) => mod.default)
  .sort((a, b) => Number(a.number) - Number(b.number));
