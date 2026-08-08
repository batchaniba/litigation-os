#!/usr/bin/env node
// ==========================================================
// Build / migrate the shared document registry.
//
// Source of truth for path → canonical label (+ owning matter folder).
// Matter JSON keeps membership + optional label override + filed.
// Outcomes document paths are included so opinions-only PDFs are registered.
//
// Usage:
//   npm run sync:registry            # write registry + rewrite matter refs
//   npm run sync:registry -- --check # exit 1 if registry/matters drift
// ==========================================================
import fs from "node:fs";
import path from "node:path";
import { fileURLToPath, pathToFileURL } from "node:url";
import { loadMatters, MATTERS_DIR, matterFileName } from "./load-matters.mjs";
import {
  REGISTRY_PATH,
  labelFromPath,
  loadRegistry,
  ownerMatterFromPath,
  registryByPath,
  resolveDocumentRef,
  stripMatterPrefix,
} from "./lib/document-registry.mjs";

const __dirname = path.dirname(fileURLToPath(import.meta.url));
const REPO_ROOT = path.resolve(__dirname, "../..");
const checkOnly = process.argv.includes("--check");

const matters = loadMatters();
const existingRegistry = loadRegistry();
const existingByPath = registryByPath(existingRegistry);
const { outcomes } = await import(
  pathToFileURL(path.join(REPO_ROOT, "internal/src/data/outcomes.js")).href
);

/** @type {Map<string, Map<number, { label: string, filed?: boolean }>>} */
const membership = new Map();

function noteMembership(docPath, matterNumber, label, filed) {
  if (!docPath) return;
  if (!membership.has(docPath)) membership.set(docPath, new Map());
  membership.get(docPath).set(matterNumber, {
    label: String(label ?? "").trim(),
    ...(typeof filed === "boolean" ? { filed } : {}),
  });
}

for (const matter of matters) {
  for (const doc of matter.documents ?? []) {
    if (!doc?.path) continue;
    noteMembership(doc.path, matter.number, doc.label, doc.filed);
  }
}

/** Outcomes-only paths (may already be in a matter). */
const outcomePaths = new Map();
for (const op of outcomes.judicial_opinions ?? []) {
  for (const key of ["document_path", "objections_path", "nsa_path"]) {
    const p = op[key];
    if (typeof p === "string" && p.startsWith("/documents/")) {
      if (!outcomePaths.has(p)) {
        outcomePaths.set(p, {
          label: labelFromPath(p),
          matter: op.matter ?? null,
        });
      }
    }
  }
}

function pickCanonicalLabel(docPath, byMatter) {
  const owner = ownerMatterFromPath(docPath);
  // Prefer an explicit label still carried by the owning matter folder.
  if (owner != null && byMatter?.has(owner)) {
    const ownerLabel = byMatter.get(owner).label;
    if (ownerLabel) return stripMatterPrefix(ownerLabel) || ownerLabel;
  }
  // After migration, matters omit the canonical label — keep the registry stable.
  const existingLabel = existingByPath.get(docPath)?.label;
  if (existingLabel) return existingLabel;

  const labels = [...(byMatter?.values() ?? [])]
    .map((entry) => entry.label)
    .filter(Boolean);
  const unprefixed = labels.find((label) => !/^\[M\d+\]/i.test(label));
  const chosen = unprefixed ?? labels[0];
  if (chosen) return stripMatterPrefix(chosen) || chosen;
  if (outcomePaths.has(docPath)) return outcomePaths.get(docPath).label;
  return labelFromPath(docPath);
}

const allPaths = new Set([...membership.keys(), ...outcomePaths.keys()]);
const documents = [...allPaths]
  .sort((a, b) => a.localeCompare(b))
  .map((docPath) => {
    const byMatter = membership.get(docPath);
    const ownerMatter = ownerMatterFromPath(docPath);
    return {
      path: docPath,
      label: pickCanonicalLabel(docPath, byMatter),
      ownerMatter,
    };
  });

const registry = { version: 1, documents };
const registryPayload = `${JSON.stringify(registry, null, 2)}\n`;
const byPath = registryByPath(registry);

function migrateMatterDocuments(matter) {
  const next = [];
  for (const doc of matter.documents ?? []) {
    if (!doc?.path) continue;
    const canonical = byPath.get(doc.path)?.label ?? "";
    const currentLabel = typeof doc.label === "string" ? doc.label.trim() : "";
    /** @type {{ path: string, label?: string, filed?: boolean }} */
    const ref = { path: doc.path };
    if (currentLabel && currentLabel !== canonical) {
      ref.label = currentLabel;
    }
    if (typeof doc.filed === "boolean") ref.filed = doc.filed;
    // After first migration, label may already be omitted — keep resolved check stable.
    if (!currentLabel && !canonical) {
      ref.label = labelFromPath(doc.path);
    }
    next.push(ref);
  }
  return next;
}

function matterPayload(matter) {
  const { __sourceFile, ...rest } = matter;
  const migrated = {
    ...rest,
    documents: migrateMatterDocuments(matter),
  };
  return `${JSON.stringify(migrated, null, 2)}\n`;
}

function checkRegistryFresh() {
  const onDisk = loadRegistry();
  const expectedPaths = new Set(documents.map((d) => d.path));
  const diskPaths = new Set(onDisk.documents.map((d) => d.path));
  let ok = true;

  if (JSON.stringify(onDisk.documents) !== JSON.stringify(documents)) {
    // Allow label-stable compare: path set + labels must match expected build.
    const diskByPath = registryByPath(onDisk);
    for (const entry of documents) {
      const have = diskByPath.get(entry.path);
      if (!have) {
        console.error(`registry missing path: ${entry.path}`);
        ok = false;
        continue;
      }
      if (have.label !== entry.label || have.ownerMatter !== entry.ownerMatter) {
        console.error(
          `registry stale for ${entry.path}: expected label=${JSON.stringify(entry.label)} owner=${entry.ownerMatter}, ` +
            `got label=${JSON.stringify(have.label)} owner=${have.ownerMatter}`,
        );
        ok = false;
      }
    }
    for (const p of diskPaths) {
      if (!expectedPaths.has(p)) {
        console.error(`registry has extra path: ${p}`);
        ok = false;
      }
    }
  }

  for (const matter of matters) {
    const expected = matterPayload(matter);
    const filePath = path.join(MATTERS_DIR, matterFileName(matter.number));
    const actual = fs.readFileSync(filePath, "utf8");
    if (actual !== expected) {
      // Soft-check: every ref must resolve and omit redundant labels.
      for (const [i, doc] of (matter.documents ?? []).entries()) {
        if (!doc?.path) {
          console.error(`Matter ${matter.number} documents[${i}]: missing path`);
          ok = false;
          continue;
        }
        if (!byPath.has(doc.path) && !diskPaths.has(doc.path)) {
          console.error(`Matter ${matter.number} documents[${i}]: path not in registry: ${doc.path}`);
          ok = false;
        }
        const canonical = (byPath.get(doc.path) ?? registryByPath(onDisk).get(doc.path))?.label;
        if (doc.label != null && canonical && doc.label === canonical) {
          console.error(
            `Matter ${matter.number} documents[${i}]: redundant label equals registry — omit label override`,
          );
          ok = false;
        }
        if (doc.label == null && !canonical) {
          console.error(`Matter ${matter.number} documents[${i}]: no label and no registry entry`);
          ok = false;
        }
      }
      // If only formatting differs but refs are already migrated, don't fail on whitespace.
      const currentRefs = matter.documents ?? [];
      const migratedRefs = migrateMatterDocuments(matter);
      if (JSON.stringify(currentRefs) !== JSON.stringify(migratedRefs)) {
        console.error(
          `Matter ${matter.number}: documents[] not migrated — run npm run sync:registry`,
        );
        ok = false;
      }
    }
  }

  return ok;
}

if (checkOnly) {
  if (!fs.existsSync(REGISTRY_PATH)) {
    console.error("Missing document registry — run npm run sync:registry");
    process.exit(1);
  }
  const ok = checkRegistryFresh();
  if (!ok) {
    console.error("Document registry is stale — run npm run sync:registry");
    process.exit(1);
  }
  console.log(
    `OK — document registry current (${documents.length} paths; ${membership.size} matter-linked).`,
  );
  process.exit(0);
}

fs.mkdirSync(path.dirname(REGISTRY_PATH), { recursive: true });
fs.writeFileSync(REGISTRY_PATH, registryPayload);

let rewritten = 0;
let overridesKept = 0;
for (const matter of matters) {
  const payload = matterPayload(matter);
  const filePath = path.join(MATTERS_DIR, matterFileName(matter.number));
  const before = fs.readFileSync(filePath, "utf8");
  if (before !== payload) {
    fs.writeFileSync(filePath, payload);
    rewritten += 1;
  }
  for (const doc of migrateMatterDocuments(matter)) {
    if (doc.label) overridesKept += 1;
  }
}

// Sanity: every matter ref resolves.
let unresolved = 0;
for (const matter of matters) {
  for (const doc of migrateMatterDocuments(matter)) {
    const resolved = resolveDocumentRef(doc, byPath);
    if (!resolved?.label) unresolved += 1;
  }
}

console.log(
  `Wrote ${path.relative(REPO_ROOT, REGISTRY_PATH)} (${documents.length} paths). ` +
    `Rewrote ${rewritten} matter file(s); kept ${overridesKept} label override(s).` +
    (unresolved ? ` WARNING: ${unresolved} unresolved labels.` : ""),
);
