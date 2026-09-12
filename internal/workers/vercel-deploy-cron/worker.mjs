// Cloudflare Worker: scheduled production deploys for the portfolio site.
//
// vercel.json sets git.deploymentEnabled=false, so pushes to main no longer
// create Vercel deployments. Production advances when this worker POSTs the
// project's Deploy Hook — on a cron (wrangler.toml) or by an authenticated
// manual request — instead of on each of the 100+ commits a busy day lands.
//
// Before firing, it checks whether production is already at main's HEAD:
//   - main's HEAD comes from the GitHub API (the repo is private, so this
//     needs GITHUB_TOKEN with Contents: read);
//   - production's commit comes from ${SITE_URL}/version.json, which
//     vite.config.js writes into every build.
// If either side is unavailable the worker fires the hook anyway. Vercel's
// Ignored Build Step (internal/scripts/vercel-ignore-build.sh) is the second
// line of defence and skips a hook build whose inputs did not change.
//
// Nothing here touches the repository or the deploy hook URL's target; the
// hook is a single-purpose URL that can only rebuild the branch it was
// created for. Treat it like a password all the same (wrangler secret).

const SHA_RE = /^[0-9a-f]{40}$/;
const UA = "ilp-vercel-deploy-cron (+https://github.com/newanforbi/interactive-litigation-portfolio)";

function json(body, status = 200) {
  return new Response(JSON.stringify(body, null, 2), {
    status,
    headers: { "content-type": "application/json", "cache-control": "no-store" },
  });
}

function timingSafeEqual(a, b) {
  if (typeof a !== "string" || typeof b !== "string" || a.length !== b.length) return false;
  let diff = 0;
  for (let i = 0; i < a.length; i++) diff |= a.charCodeAt(i) ^ b.charCodeAt(i);
  return diff === 0;
}

async function fetchMainHead(env) {
  if (!env.GITHUB_TOKEN) return { sha: null, reason: "GITHUB_TOKEN not set" };
  const repo = env.GITHUB_REPO;
  const branch = env.GITHUB_BRANCH || "main";
  const res = await fetch(`https://api.github.com/repos/${repo}/commits/${encodeURIComponent(branch)}`, {
    headers: {
      accept: "application/vnd.github.sha",
      authorization: `Bearer ${env.GITHUB_TOKEN}`,
      "user-agent": UA,
      "x-github-api-version": "2022-11-28",
    },
  });
  if (!res.ok) return { sha: null, reason: `GitHub ${res.status}` };
  const sha = (await res.text()).trim();
  return SHA_RE.test(sha) ? { sha } : { sha: null, reason: "GitHub returned no sha" };
}

async function fetchProductionSha(env) {
  const site = (env.SITE_URL || "").replace(/\/+$/, "");
  if (!site) return { sha: null, reason: "SITE_URL not set" };
  const res = await fetch(`${site}/version.json`, {
    headers: { "user-agent": UA, "cache-control": "no-cache" },
    cf: { cacheTtl: 0 },
  });
  if (!res.ok) return { sha: null, reason: `site ${res.status}` };
  let body;
  try {
    body = await res.json();
  } catch {
    return { sha: null, reason: "version.json not JSON" };
  }
  const sha = typeof body?.sha === "string" ? body.sha : null;
  return sha && SHA_RE.test(sha) ? { sha } : { sha: null, reason: "version.json has no sha" };
}

async function fireDeployHook(env, reason) {
  if (!env.VERCEL_DEPLOY_HOOK_URL) {
    return { fired: false, error: "VERCEL_DEPLOY_HOOK_URL not set" };
  }
  const res = await fetch(env.VERCEL_DEPLOY_HOOK_URL, {
    method: "POST",
    headers: { "user-agent": UA },
  });
  const text = await res.text();
  let job = null;
  try {
    job = JSON.parse(text)?.job ?? null;
  } catch {
    // Vercel normally returns {"job": {...}}; keep the raw text for the log.
  }
  const result = { fired: res.ok, status: res.status, reason, job: job ?? text.slice(0, 200) };
  console.log(JSON.stringify({ event: "deploy-hook", ...result }));
  return result;
}

async function deployIfBehind(env, { force = false, trigger }) {
  const [main, prod] = await Promise.all([fetchMainHead(env), fetchProductionSha(env)]);
  const summary = {
    trigger,
    main: main.sha ?? null,
    production: prod.sha ?? null,
    checks: { main: main.reason ?? "ok", production: prod.reason ?? "ok" },
  };

  if (!force && main.sha && prod.sha && main.sha === prod.sha) {
    console.log(JSON.stringify({ event: "skip", ...summary, why: "production already at main HEAD" }));
    return { ...summary, action: "skip" };
  }

  const why = force
    ? "forced"
    : !main.sha || !prod.sha
      ? "could not compare; deploying to be safe"
      : `production ${prod.sha.slice(0, 12)} behind main ${main.sha.slice(0, 12)}`;
  const hook = await fireDeployHook(env, why);
  return { ...summary, action: hook.fired ? "deploy" : "error", hook };
}

export default {
  async scheduled(controller, env, ctx) {
    ctx.waitUntil(deployIfBehind(env, { trigger: `cron ${controller.cron}` }));
  },

  async fetch(request, env, _ctx) {
    const url = new URL(request.url);

    // Health / status: no secrets, just whether the pieces are configured.
    if (request.method === "GET" && url.pathname === "/") {
      return json({
        ok: true,
        worker: "ilp-vercel-deploy-cron",
        configured: {
          deployHook: Boolean(env.VERCEL_DEPLOY_HOOK_URL),
          githubToken: Boolean(env.GITHUB_TOKEN),
          siteUrl: Boolean(env.SITE_URL),
          manualTrigger: Boolean(env.DEPLOY_TRIGGER_TOKEN),
        },
      });
    }

    // Manual trigger for an urgent filing between cron ticks:
    //   curl -X POST -H "authorization: Bearer $DEPLOY_TRIGGER_TOKEN" https://<worker>/deploy
    // Add ?force=1 to skip the version comparison.
    if (request.method === "POST" && url.pathname === "/deploy") {
      if (!env.DEPLOY_TRIGGER_TOKEN) return json({ error: "manual trigger not configured" }, 404);
      const auth = request.headers.get("authorization") || "";
      const token = auth.startsWith("Bearer ") ? auth.slice(7) : "";
      if (!timingSafeEqual(token, env.DEPLOY_TRIGGER_TOKEN)) return json({ error: "unauthorized" }, 401);
      const force = url.searchParams.get("force") === "1";
      const result = await deployIfBehind(env, { force, trigger: "manual" });
      return json(result, result.action === "error" ? 502 : 200);
    }

    return json({ error: "not found" }, 404);
  },
};
