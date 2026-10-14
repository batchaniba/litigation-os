#!/usr/bin/env node
// Idempotent mover: tracked PDFs land under documents/<matter>/… mirroring
// D1 / manifest /documents/ paths, except the 14-path private denylist (and
// known hashes / HOPE root analogues) which go to internal/private/documents/.
// Identical SHA-256 → one file. Same dest, different bytes → hash suffix.
import { execFileSync } from "node:child_process";
import fs from "node:fs";
import path from "node:path";
import {
  DOCUMENTS_ROOT,
  PRIVATE_DOCUMENTS_ROOT,
  REPO_ROOT,
  hashFileSha256,
  loadManifest,
} from "./lib/document-store.mjs";
import { isPrivateDocument, isPrivatePath, isPrivateSha } from "./lib/private-documents.mjs";

const apply = process.argv.includes("--apply");
const REPORT = path.join(REPO_ROOT, "internal/src/data/documents/consolidation-report.json");
const CONFLICTS = path.join(
  REPO_ROOT,
  "internal/src/data/documents/hope-discovery-conflicts.json",
);
const QUARANTINE = path.join(REPO_ROOT, "internal/src/data/index/root-quarantine.json");
const D1_DUMP = process.env.D1_DOCUMENTS_JSON || "/tmp/d1-documents.json";

const HOPE_ROOT_MAP = {
  "1_PHCP06796815_Rdctd_131_pdf.pdf":
    "HOPE_000001-031_Professional_Liability_Policy.pdf",
  "2_PHSD1838240007_Rdctd_32104_pdf.pdf":
    "HOPE_000032-104_DandO_EPL_Policy.pdf",
  "Block_1_Homework_105138_pdt.pdf": "HOPE_000105-138_Block_1_Homework.pdf",
  "Collateral_NotesComm_139199_pdf.pdf":
    "HOPE_000139-199_Collateral_Notes_and_Communications.pdf",
  "Homework_200223_pdf.pdf":
    "HOPE_000200-223_Homework_and_Preparatory_Tickets.pdf",
  "Hw_Audit_3_2026_224_paf.pdf": "HOPE_000224_Curriculum_Tracking_Audit.pdf",
  "1_HOPE_Clinical_Operational_Manual_9_24_24_225349_pg_1_to_90.pdf":
    "HOPE_000225-314_Clinical_Operational_Manual_Part_1.pdf",
  "1_HOPE_Clinical_Operational_Manual_9_24_24_225349_pg_91_to_125.pdf":
    "HOPE_000315-349_Clinical_Operational_Manual_Part_2.pdf",
  "2_HOPE_Maintenance_Curriculum_350434.pdf":
    "HOPE_000350-434_Maintenance_Curriculum.pdf",
  "2_HOPE_Maintenance_Curriculum_350434__pdf.pdf":
    "HOPE_000350-434_Maintenance_Curriculum.pdf",
  "3_HOPE_Prgrm_Emply_Hndbk_2023_435485_pdf.pdf":
    "HOPE_000435-485_Program_Employee_Handbook_2023.pdf",
  "4_HOPE_Prprtry_Trtmnt_Mnul_2_18_2019_486537.pdf":
    "HOPE_000486-537_Proprietary_Treatment_Manual.pdf",
  "5_CD_Job_Description_538542_pdf.pdf":
    "HOPE_000538-542_Clinical_Director_Job_Description.pdf",
};

function git(args) {
  return execFileSync("git", args, {
    cwd: REPO_ROOT,
    encoding: "utf8",
    stdio: ["pipe", "pipe", "pipe"],
  }).trim();
}

function trackedPdfs() {
  const out = git(["ls-files", "-z", "*.pdf"]);
  return out ? out.split("\0").filter(Boolean) : [];
}

function loadJson(p, fallback) {
  if (!fs.existsSync(p)) return fallback;
  return JSON.parse(fs.readFileSync(p, "utf8"));
}

function posixJoin(...parts) {
  return parts.filter(Boolean).join("/").replace(/\/+/g, "/");
}

function withHashSuffix(destRel, sha) {
  const ext = path.posix.extname(destRel);
  const stem = destRel.slice(0, destRel.length - ext.length);
  return `${stem}.${sha.slice(0, 8)}${ext}`;
}

function publicUrlFromDest(destRel) {
  if (destRel.startsWith("documents/")) return `/${destRel}`;
  if (destRel.startsWith("internal/private/documents/")) {
    return `/documents/${destRel.slice("internal/private/documents/".length)}`;
  }
  return `/${destRel}`;
}

function destFor({ rel, sha, basename, d1BySha, manifestBySha, quarantineByName, privateFile }) {
  if (HOPE_ROOT_MAP[basename]) {
    const stem = HOPE_ROOT_MAP[basename].replace(/\.pdf$/i, "");
    return posixJoin(
      "internal/private/documents/matter-05/hope-discovery",
      `${stem}.root-${sha.slice(0, 8)}.pdf`,
    );
  }
  const mapped =
    d1BySha.get(sha)?.path ||
    manifestBySha.get(sha)?.path ||
    quarantineByName.get(basename)?.destination;
  if (typeof mapped === "string" && mapped.startsWith("/documents/")) {
    const under = mapped.replace(/^\/documents\//, "");
    if (privateFile || isPrivatePath(mapped) || isPrivateSha(sha)) {
      return posixJoin("internal/private/documents", under);
    }
    return posixJoin("documents", under);
  }
  if (rel.startsWith("internal/docs/")) {
    const rest = rel.slice("internal/docs/".length);
    if (privateFile) return posixJoin("internal/private/documents", rest);
    return posixJoin("documents", rest);
  }
  if (rel.startsWith("internal/public/documents/")) {
    return posixJoin("documents", rel.slice("internal/public/documents/".length));
  }
  if (rel.startsWith("documents/") || rel.startsWith("internal/private/documents/")) return rel;
  if (privateFile) return posixJoin("internal/private/documents/_unfiled", basename);
  return posixJoin("documents/_unfiled", basename);
}

function main() {
  const manifest = loadManifest();
  const d1Rows = loadJson(D1_DUMP, []);
  const quarantine = loadJson(QUARANTINE, { files: [] });

  const d1BySha = new Map(d1Rows.map((r) => [String(r.sha256).toLowerCase(), r]));
  const d1ByPath = new Map(d1Rows.map((r) => [r.path, r]));
  const manifestBySha = new Map(
    (manifest.files ?? []).map((f) => [String(f.sha256).toLowerCase(), f]),
  );
  const quarantineByName = new Map((quarantine.files ?? []).map((f) => [f.name, f]));

  const pdfs = trackedPdfs();
  const moves = [];
  const kept_phone_taps = [];
  const deduped = [];
  const renamed = [];
  const private_moved = [];
  const shaToDest = new Map();
  const destToSha = new Map();

  for (const rel of pdfs) {
    const abs = path.join(REPO_ROOT, rel);
    const basename = path.posix.basename(rel);
    // Every PDF sitting directly in internal/public/ is a phone-tap delivery
    // copy. Leave it. Do not git-rm it as a duplicate of the canonical file.
    if (path.posix.dirname(rel) === "internal/public") {
      const sha = hashFileSha256(abs);
      if (isPrivateSha(sha) || isPrivatePath(`/${basename}`)) {
        throw new Error(`phone-tap slug ${rel} hashes to a private denylist SHA — do not host it publicly`);
      }
      kept_phone_taps.push(rel);
      continue;
    }
    const sha = hashFileSha256(abs);
    const size = fs.statSync(abs).size;
    const privateFile =
      isPrivateSha(sha) ||
      Boolean(HOPE_ROOT_MAP[basename]) ||
      isPrivateDocument({ path: `/${rel}`, sha256: sha });
    let dest = destFor({
      rel,
      sha,
      basename,
      d1BySha,
      manifestBySha,
      quarantineByName,
      privateFile,
    });
    if (isPrivatePath(publicUrlFromDest(dest)) && !dest.startsWith("internal/private/")) {
      dest = posixJoin("internal/private/documents", publicUrlFromDest(dest).replace(/^\/documents\//, ""));
    }
    if (shaToDest.has(sha)) {
      deduped.push({ source: rel, sha256: sha, size, kept: shaToDest.get(sha) });
      moves.push({ action: "rm", source: rel, dest: shaToDest.get(sha), sha256: sha, size });
      continue;
    }
    if (destToSha.has(dest) && destToSha.get(dest) !== sha) {
      const suffixed = withHashSuffix(dest, sha);
      renamed.push({ from: dest, to: suffixed, reason: "same_name_different_bytes" });
      dest = suffixed;
    }
    moves.push({ action: "mv", source: rel, dest, sha256: sha, size, private: dest.startsWith("internal/private/") });
    if (dest.startsWith("internal/private/")) private_moved.push({ source: rel, dest, sha256: sha });
    shaToDest.set(sha, dest);
    destToSha.set(dest, sha);
  }

  const hopeConflicts = (manifest.files ?? [])
    .filter((f) => String(f.path).includes("/hope-discovery/"))
    .map((man) => {
      const d1 = d1ByPath.get(man.path);
      const rootEntry = Object.entries(HOPE_ROOT_MAP).find(([, n]) => man.path.endsWith(`/${n}`) || man.path.endsWith(n));
      const rootName = rootEntry?.[0];
      const rootQ = rootName ? quarantineByName.get(rootName) : null;
      const rootMove = moves.find((m) => path.posix.basename(m.source ?? "") === rootName);
      return {
        path: man.path,
        d1: d1 ? { sha256: d1.sha256, size: d1.size, bytes_in_this_tree: false } : null,
        manifest: { sha256: man.sha256, size: man.size, bytes_in_this_tree: false },
        repo_root: rootQ
          ? {
              source: rootName,
              sha256: rootQ.sha256,
              size: rootQ.size,
              canonical_copy: rootMove?.dest ?? null,
            }
          : null,
        visibility: "private/auth-only (owner denylist of 14). D1 and manifest hashes disagree; repo-root Bates copies are a third byte sequence. Do not collapse.",
      };
    });

  const report = {
    generated: new Date().toISOString().slice(0, 10),
    apply,
    counts: {
      tracked_pdfs: pdfs.length,
      moved: moves.filter((m) => m.action === "mv").length,
      deduped_removed: moves.filter((m) => m.action === "rm").length,
      phone_tap_slugs_kept: kept_phone_taps.length,
      renamed_for_byte_conflict: renamed.length,
      private_to_internal_private: private_moved.length,
      unique_sha_kept: shaToDest.size,
    },
    git_lfs:
      "Not recommended. GitHub’s free LFS quota is 1 GB/month of bandwidth; Vercel builds would exhaust it. R2 remains the serving store. This branch tracks previously-scattered public PDFs so they are no longer at repo root / internal/docs.",
    phone_tap_exception:
      "internal/public/{slug}.pdf stay as unauthenticated Vercel/Pages tap copies of public filings. Private denylist files must never become slugs.",
    hope_discovery_conflicts: hopeConflicts.length,
    private_moved,
    deduped,
    renamed,
    kept_phone_taps,
    moves,
  };

  fs.mkdirSync(path.dirname(REPORT), { recursive: true });
  fs.writeFileSync(CONFLICTS, `${JSON.stringify({ generated: report.generated, files: hopeConflicts }, null, 2)}\n`);

  if (!apply) {
    fs.writeFileSync(REPORT, `${JSON.stringify(report, null, 2)}\n`);
    process.stdout.write(
      `DRY-RUN moved=${report.counts.moved} deduped=${report.counts.deduped_removed} private=${report.counts.private_to_internal_private} phone_taps=${report.counts.phone_tap_slugs_kept} hope_conflicts=${hopeConflicts.length}\n`,
    );
    return;
  }

  fs.mkdirSync(DOCUMENTS_ROOT, { recursive: true });
  fs.mkdirSync(PRIVATE_DOCUMENTS_ROOT, { recursive: true });
  for (const step of moves) {
    if (step.action === "mv") {
      if (step.source === step.dest) continue;
      fs.mkdirSync(path.dirname(path.join(REPO_ROOT, step.dest)), { recursive: true });
      git(["mv", "--", step.source, step.dest]);
    } else if (step.action === "rm") {
      git(["rm", "-f", "--", step.source]);
    }
  }
  const qNext = {
    ...quarantine,
    generated: report.generated,
    note: "Drained 2026-10-14: root PDFs moved to documents/ or internal/private/documents/. remaining=0. New root PDFs still fail the gate.",
    remaining: 0,
    remainingBytes: 0,
    files: [],
    drained: quarantine.files ?? [],
  };
  fs.writeFileSync(QUARANTINE, `${JSON.stringify(qNext, null, 2)}\n`);
  const slim = { ...report, moves: undefined, move_count: moves.length };
  fs.writeFileSync(REPORT, `${JSON.stringify(slim, null, 2)}\n`);
  git(["add", "--", QUARANTINE, CONFLICTS, REPORT]);
  process.stdout.write(
    `APPLIED moved=${report.counts.moved} deduped=${report.counts.deduped_removed} private=${report.counts.private_to_internal_private} phone_taps=${report.counts.phone_tap_slugs_kept}\n`,
  );
}

main();
