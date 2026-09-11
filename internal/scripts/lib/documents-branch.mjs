// Git operations for the `documents` branch (PDF bytes, not on main).
import { execFileSync } from "node:child_process";
import fs from "node:fs";
import os from "node:os";
import path from "node:path";
import { DOCUMENTS_ROOT, REPO_ROOT } from "./document-store.mjs";

export const DOCUMENTS_BRANCH = "documents";

/**
 * GitHub Pages project URL for the PDF tree after a GITHUB_PAGES build.
 * Vercel rewrites /documents/:path* here so the live site keeps the same paths.
 */
export const PAGES_DOCUMENTS_ORIGIN =
  "https://newanforbi.github.io/interactive-litigation-portfolio/documents";

export function vercelSpaRewrites() {
  return [
    {
      source: "/documents/:path*",
      destination: `${PAGES_DOCUMENTS_ORIGIN}/:path*`,
    },
    { source: "/(.*)", destination: "/index.html" },
  ];
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

export function pullDocuments() {
  const tip = fetchDocumentsBranch();
  if (!tip) {
    throw new Error(
      `origin/${DOCUMENTS_BRANCH} is missing — run npm run documents:push from a clone that still has the PDF tree`,
    );
  }
  fs.mkdirSync(path.dirname(DOCUMENTS_ROOT), { recursive: true });
  const archive = execFileSync(
    "git",
    ["archive", `origin/${DOCUMENTS_BRANCH}`, "internal/public/documents"],
    { cwd: REPO_ROOT },
  );
  execFileSync("tar", ["-x", "-C", REPO_ROOT], {
    cwd: REPO_ROOT,
    input: archive,
    stdio: ["pipe", "inherit", "inherit"],
  });
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
  return { pushed: true, commit };
}
