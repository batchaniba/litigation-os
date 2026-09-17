// Git operations for the `documents` branch (PDF bytes, not on main).
import { execFileSync } from "node:child_process";
import fs from "node:fs";
import os from "node:os";
import path from "node:path";
import {
  DOCUMENTS_ROOT,
  MANIFEST_PATH,
  REPO_ROOT,
  diskFromUrl,
  walkFiles,
} from "./document-store.mjs";
import { getObject, isConfigured as r2IsConfigured, keyForSha256 } from "./r2-client.mjs";

export const DOCUMENTS_BRANCH = "documents";
export const DOCUMENTS_GIT_PREFIX = "internal/public/documents";

/**
 * Public documents origin. Vercel rewrites /documents/:path* here.
 * Bytes are R2; this hostname is the Worker that maps path → sha256.
 */
export const DOCUMENTS_ORIGIN =
  "https://litigation-doc-api.ss8sxswwkt.workers.dev/documents";
/** @deprecated alias — Pages no longer serves the library. */
export const PAGES_DOCUMENTS_ORIGIN = DOCUMENTS_ORIGIN;

export function vercelSpaRewrites() {
  return [
    {
      source: "/documents/:path*",
      destination: `${PAGES_DOCUMENTS_ORIGIN}/:path*`,
    },
    { source: "/(.*)", destination: "/index.html" },
  ];
}

export function isDocumentsSource(source) {
  return String(source).startsWith("/documents/");
}

/** Encode each path segment so Vercel destinations never contain raw `(`. */
export function encodePathSegment(segment) {
  return encodeURIComponent(segment).replace(/[!'()*]/g, (char) => {
    return `%${char.charCodeAt(0).toString(16).toUpperCase()}`;
  });
}

export function encodeDocumentsPath(source) {
  const trimmed = String(source).replace(/^\//, "");
  return `/${trimmed.split("/").map(encodePathSegment).join("/")}`;
}

export function pagesDocumentUrl(source) {
  if (!isDocumentsSource(source)) {
    throw new Error(`pagesDocumentUrl expects a /documents/ path, got ${source}`);
  }
  const rest = String(source).slice("/documents/".length);
  return `${PAGES_DOCUMENTS_ORIGIN}/${rest.split("/").map(encodePathSegment).join("/")}`;
}

export function matterDocumentsFolder(n) {
  return `matter-${String(n).padStart(2, "0")}`;
}

function parseMatterList(raw) {
  return String(raw)
    .split(",")
    .map((part) => part.trim())
    .filter(Boolean)
    .map((part) => {
      const n = Number(part);
      if (!Number.isInteger(n) || n < 1 || n > 99) {
        throw new Error(`Invalid matter number: ${part}`);
      }
      return n;
    });
}

/**
 * Parse `documents:pull` flags from argv after the `pull` verb.
 * @param {string[]} args
 */
export function parseDocumentsPullArgs(args) {
  const result = {
    matters: [],
    forms: false,
    opinions: false,
    list: false,
    help: false,
  };
  for (let i = 0; i < args.length; i++) {
    const token = args[i];
    if (token === "--list") {
      result.list = true;
    } else if (token === "--forms" || token === "--form-library") {
      result.forms = true;
    } else if (token === "--opinions") {
      result.opinions = true;
    } else if (token === "--help" || token === "-h") {
      result.help = true;
    } else if (token === "--matter" || token === "-m") {
      const value = args[++i];
      if (!value || value.startsWith("-")) {
        throw new Error("--matter needs a number (e.g. --matter 24 or --matter 20,24)");
      }
      result.matters.push(...parseMatterList(value));
    } else if (token.startsWith("--matter=")) {
      result.matters.push(...parseMatterList(token.slice("--matter=".length)));
    } else {
      throw new Error(`Unknown documents:pull flag: ${token}`);
    }
  }
  result.matters = [...new Set(result.matters)].sort((a, b) => a - b);
  return result;
}

/**
 * Git-archive pathspecs for a sparse pull. `null` means the whole tree.
 * @param {{ matters?: number[], forms?: boolean, opinions?: boolean }} opts
 * @returns {string[] | null}
 */
export function documentsArchivePaths({ matters = [], forms = false, opinions = false } = {}) {
  const sparse = matters.length > 0 || forms || opinions;
  if (!sparse) return null;
  const paths = matters.map((n) => `${DOCUMENTS_GIT_PREFIX}/${matterDocumentsFolder(n)}`);
  if (forms) paths.push(`${DOCUMENTS_GIT_PREFIX}/_form-library`);
  if (opinions) paths.push(`${DOCUMENTS_GIT_PREFIX}/opinions`);
  paths.push(`${DOCUMENTS_GIT_PREFIX}/README.md`);
  return paths;
}

function git(args, { cwd = REPO_ROOT, env, input, stdio } = {}) {
  const stdoutStdio = stdio ?? ["pipe", "pipe", "pipe"];
  const out = execFileSync("git", args, {
    cwd,
    env: { ...process.env, ...(env ?? {}) },
    input,
    encoding: "utf8",
    stdio: stdoutStdio,
  });
  return typeof out === "string" ? out.trim() : "";
}

function mktree(entries) {
  const body = `${entries
    .map((entry) => `${entry.mode} ${entry.type} ${entry.sha}\t${entry.name}`)
    .join("\n")}\n`;
  return git(["mktree"], { input: body });
}

/** Root tree that contains only `internal/public/documents/`. */
export function wrapDocumentsTree(documentsTreeSha) {
  const publicTree = mktree([
    { mode: "040000", type: "tree", sha: documentsTreeSha, name: "documents" },
  ]);
  const internalTree = mktree([
    { mode: "040000", type: "tree", sha: publicTree, name: "public" },
  ]);
  return mktree([{ mode: "040000", type: "tree", sha: internalTree, name: "internal" }]);
}

/**
 * Snapshot the working-tree PDF folder into a git root tree (gitignore is
 * ignored via `git add -f`). Used by documents:push.
 */
export function writeWorkingDocumentsRootTree() {
  if (!fs.existsSync(DOCUMENTS_ROOT)) {
    throw new Error(
      "internal/public/documents/ is missing — run npm run documents:pull",
    );
  }
  const dir = fs.mkdtempSync(path.join(os.tmpdir(), "ilp-docs-idx-"));
  const indexFile = path.join(dir, "index");
  try {
    git(["add", "-f", "-A", "--", "internal/public/documents"], {
      env: { GIT_INDEX_FILE: indexFile, GIT_WORK_TREE: REPO_ROOT },
    });
    return git(["write-tree"], { env: { GIT_INDEX_FILE: indexFile } });
  } finally {
    fs.rmSync(dir, { recursive: true, force: true });
  }
}

export function documentsTreeFromHead() {
  try {
    return git(["rev-parse", "HEAD:internal/public/documents"]);
  } catch {
    return null;
  }
}

export function fetchDocumentsBranch() {
  try {
    git(["fetch", "origin", DOCUMENTS_BRANCH, "--depth", "1"]);
    return git(["rev-parse", `origin/${DOCUMENTS_BRANCH}`]);
  } catch {
    return null;
  }
}

export function remoteDocumentsRootTree() {
  try {
    return git(["rev-parse", `origin/${DOCUMENTS_BRANCH}^{tree}`]);
  } catch {
    return null;
  }
}

export function listDocumentsStoreFolders() {
  const out = git([
    "ls-tree",
    "--name-only",
    `origin/${DOCUMENTS_BRANCH}:${DOCUMENTS_GIT_PREFIX}`,
  ]);
  return out.split("\n").filter(Boolean).sort();
}

function commitTree(tree, message, parents = []) {
  const args = ["commit-tree", tree];
  for (const parent of parents) {
    args.push("-p", parent);
  }
  args.push("-m", message);
  return git(args);
}

export function pushDocumentsTree(tree, { parent = null, message }) {
  const commit = commitTree(tree, message, parent ? [parent] : []);
  git(["push", "origin", `${commit}:refs/heads/${DOCUMENTS_BRANCH}`], {
    stdio: ["ignore", "inherit", "inherit"],
  });
  return commit;
}

export function seedDocumentsBranch() {
  const existing = fetchDocumentsBranch();
  if (existing) return { created: false, commit: existing };
  const docsTree = documentsTreeFromHead() ?? (() => {
    const root = writeWorkingDocumentsRootTree();
    return git(["rev-parse", `${root}:internal/public/documents`]);
  })();
  const root = wrapDocumentsTree(docsTree);
  const commit = pushDocumentsTree(root, {
    message: "Seed document store from the current PDF tree.",
  });
  return { created: true, commit };
}

/**
 * Restore PDF bytes from origin/documents.
 * Default: the whole tree. Pass `{ matters: [24] }` (and optional forms /
 * opinions) to extract only those folders. Sparse pulls merge into whatever
 * is already on disk; they do not delete other matter folders.
 *
 * @param {{ matters?: number[], forms?: boolean, opinions?: boolean, list?: boolean }} [opts]
 */
function manifestFilesForPull(opts = {}) {
  const manifest = JSON.parse(fs.readFileSync(MANIFEST_PATH, "utf8"));
  const prefixes = [];
  for (const n of opts.matters ?? []) {
    prefixes.push(`/documents/${matterDocumentsFolder(n)}/`);
  }
  if (opts.forms) prefixes.push("/documents/_form-library/");
  if (opts.opinions) prefixes.push("/documents/opinions/");
  const files = manifest.files ?? [];
  if (!prefixes.length) return files.filter((f) => String(f.path ?? "").startsWith("/documents/"));
  return files.filter((f) => prefixes.some((p) => String(f.path ?? "").startsWith(p)));
}

async function pullDocumentsFromR2(opts = {}) {
  const files = manifestFilesForPull(opts);
  fs.mkdirSync(path.dirname(DOCUMENTS_ROOT), { recursive: true });
  for (const file of files) {
    const { body } = await getObject(keyForSha256(file.sha256));
    const dest = diskFromUrl(file.path);
    fs.mkdirSync(path.dirname(dest), { recursive: true });
    fs.writeFileSync(dest, body);
  }
  const paths = (opts.matters ?? []).map((n) => `matter-${String(n).padStart(2, "0")}`);
  if (opts.forms) paths.push("_form-library");
  if (opts.opinions) paths.push("opinions");
  return { paths: paths.length ? paths : [DOCUMENTS_GIT_PREFIX], via: "r2", count: files.length };
}

function uploadWorkingTreeToR2() {
  const pdfs = walkFiles(DOCUMENTS_ROOT).filter((abs) => /\.pdf$/i.test(abs));
  if (!pdfs.length) return { uploaded: false, reason: "no_local_pdfs" };
  const list = path.join(os.tmpdir(), `ilp-r2-${process.pid}.txt`);
  fs.writeFileSync(
    list,
    `${pdfs.map((abs) => path.relative(REPO_ROOT, abs).split(path.sep).join("/")).join("\n")}\n`,
  );
  execFileSync("node", ["internal/scripts/r2-upload.mjs", "--list", list], {
    cwd: REPO_ROOT,
    stdio: "inherit",
  });
  execFileSync("node", ["internal/scripts/r2-upload.mjs", "--index"], {
    cwd: REPO_ROOT,
    stdio: "inherit",
  });
  return { uploaded: true, count: pdfs.length };
}

/**
 * Restore PDF bytes. Prefers R2 (manifest sha256) when credentials are in
 * the environment; otherwise origin/documents. Sparse pulls merge.
 */
export async function pullDocuments(opts = {}) {
  if (opts.list) {
    const tip = fetchDocumentsBranch();
    if (!tip) {
      throw new Error(
        `origin/${DOCUMENTS_BRANCH} is missing — run npm run documents:push from a clone that still has the PDF tree`,
      );
    }
    return { list: listDocumentsStoreFolders() };
  }
  if (r2IsConfigured()) return pullDocumentsFromR2(opts);
  return pullDocumentsFromGit(opts);
}

export function pullDocumentsFromGit(opts = {}) {
  const tip = fetchDocumentsBranch();
  if (!tip) {
    throw new Error(
      `origin/${DOCUMENTS_BRANCH} is missing — run npm run documents:push from a clone that still has the PDF tree`,
    );
  }
  if (opts.list) {
    return { list: listDocumentsStoreFolders() };
  }
  const archivePaths = documentsArchivePaths(opts);
  fs.mkdirSync(path.dirname(DOCUMENTS_ROOT), { recursive: true });
  const gitArgs = [
    "archive",
    `origin/${DOCUMENTS_BRANCH}`,
    ...(archivePaths ?? [DOCUMENTS_GIT_PREFIX]),
  ];
  let archive;
  try {
    archive = execFileSync("git", gitArgs, {
      cwd: REPO_ROOT,
      maxBuffer: 1024 * 1024 * 1024,
    });
  } catch (error) {
    const detail = error instanceof Error && "stderr" in error
      ? String(error.stderr || error.message)
      : String(error);
    if (archivePaths) {
      let available;
      try {
        available = listDocumentsStoreFolders().join(", ");
      } catch {
        available = "(could not list origin/documents)";
      }
      throw new Error(
        `Could not pull ${archivePaths.join(", ")}.\n${detail.trim()}\nAvailable: ${available}`,
        { cause: error },
      );
    }
    throw error;
  }
  execFileSync("tar", ["-x", "-C", REPO_ROOT], {
    cwd: REPO_ROOT,
    input: archive,
    stdio: ["pipe", "inherit", "inherit"],
  });
  return { paths: archivePaths ?? [DOCUMENTS_GIT_PREFIX] };
}

export function pushDocuments() {
  const parent = fetchDocumentsBranch();
  const tree = writeWorkingDocumentsRootTree();
  if (parent) {
    const remoteTree = remoteDocumentsRootTree();
    if (remoteTree === tree) return { pushed: false, commit: parent };
  }
  const commit = pushDocumentsTree(tree, {
    parent,
    message: parent
      ? "Update document store."
      : "Seed document store from the working tree.",
  });
  const r2 = r2IsConfigured() ? uploadWorkingTreeToR2() : { uploaded: false, reason: "r2_unconfigured" };
  return { pushed: true, commit, r2 };
}

export const DOCUMENTS_PULL_USAGE = `Usage: npm run documents:pull -- [flags]

  (no flags)          restore the whole origin/documents tree (~660 MB)
  --matter 24         only matter-24/ (repeat or comma-separate: --matter 20,24)
  --forms             also _form-library/
  --opinions          also opinions/
  --list              print folders on origin/documents and exit
  -h, --help          this text

Sparse pulls merge into the working tree; they do not delete other matter
folders. See internal/docs/DOCUMENT_STORE.md.
`;
