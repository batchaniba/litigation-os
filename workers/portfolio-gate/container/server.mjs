// HTTP front for the portfolio-gate runner image.
// Cloudflare Containers startAndWaitForPorts waits on defaultPort (8080).
import http from "node:http";
import { spawn } from "node:child_process";
import path from "node:path";
import { fileURLToPath } from "node:url";

const PORT = Number(process.env.PORT || 8080);
const SCRIPT = path.join(path.dirname(fileURLToPath(import.meta.url)), "run-gate.sh");
const SHA_RE = /^[0-9a-f]{40}$/i;

function json(res, status, body) {
  const payload = JSON.stringify(body);
  res.writeHead(status, { "content-type": "application/json" });
  res.end(payload);
}

function readBody(req) {
  return new Promise((resolve, reject) => {
    const chunks = [];
    req.on("data", (c) => chunks.push(c));
    req.on("end", () => resolve(Buffer.concat(chunks).toString("utf8")));
    req.on("error", reject);
  });
}

function runGate({ sha, cloneUrl, token, timeoutMs }) {
  return new Promise((resolve) => {
    const child = spawn("/bin/bash", [SCRIPT], {
      env: {
        ...process.env,
        GATE_SHA: sha,
        GATE_CLONE_URL: cloneUrl,
        GITHUB_TOKEN: token || "",
        PORTFOLIO_SKIP_DISK_DOCS: "1",
        VITE_COPY_DOCUMENTS: "0",
        SKIP_PORTFOLIO_GATE: "",
        WORKDIR: `/tmp/portfolio-gate/${sha}`,
      },
      stdio: ["ignore", "pipe", "pipe"],
    });

    let log = "";
    const append = (buf) => {
      log += buf.toString("utf8");
      if (log.length > 200_000) log = log.slice(-200_000);
    };
    child.stdout.on("data", append);
    child.stderr.on("data", append);

    const timer =
      timeoutMs > 0
        ? setTimeout(() => {
            child.kill("SIGTERM");
            setTimeout(() => child.kill("SIGKILL"), 10_000);
          }, timeoutMs)
        : null;

    child.on("close", (code, signal) => {
      if (timer) clearTimeout(timer);
      const exitCode = code ?? (signal ? 1 : 0);
      resolve({
        ok: exitCode === 0,
        exitCode,
        reason: exitCode === 0 ? "" : `runner exited ${exitCode}${signal ? ` (${signal})` : ""}`,
        log,
      });
    });
  });
}

const server = http.createServer(async (req, res) => {
  const url = new URL(req.url || "/", `http://127.0.0.1:${PORT}`);

  if (req.method === "GET" && url.pathname === "/health") {
    return json(res, 200, { ok: true, node: process.version });
  }

  if (req.method === "POST" && url.pathname === "/run") {
    let body;
    try {
      body = JSON.parse(await readBody(req));
    } catch {
      return json(res, 400, { ok: false, reason: "invalid JSON" });
    }
    if (!SHA_RE.test(body.sha || "")) {
      return json(res, 400, { ok: false, reason: "invalid sha" });
    }
    if (!body.cloneUrl || typeof body.cloneUrl !== "string") {
      return json(res, 400, { ok: false, reason: "cloneUrl required" });
    }
    const result = await runGate({
      sha: body.sha,
      cloneUrl: body.cloneUrl,
      token: body.token,
      timeoutMs: Number(body.timeoutMs) || 0,
    });
    return json(res, 200, result);
  }

  return json(res, 404, { ok: false, reason: "not found" });
});

server.requestTimeout = 0;
server.headersTimeout = 0;
server.timeout = 0;
server.listen(PORT, "0.0.0.0", () => {
  console.log(`portfolio-gate runner listening on ${PORT}`);
});
