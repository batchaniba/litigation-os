// Phase 2 remote portfolio-gate. Check name is locked — branch protection
// will require this exact string. Do not rename without updating GitHub
// settings and this file's tests together.

export const CHECK_NAME = "portfolio-gate";
export const ALLOWED_REPO = "newanforbi/interactive-litigation-portfolio";
export const WORKER_NAME = "ilp-portfolio-gate";

/** Fail-closed wall clock, under the 15-minute Durable Object alarm limit. No result → failure (not neutral). */
export const DEFAULT_TIMEOUT_MS = 12 * 60 * 1000;

/** GitHub Check Run output.text is capped at 65535 characters. */
export const CHECK_LOG_MAX_CHARS = 60_000;

export const GITHUB_API = "https://api.github.com";
export const GITHUB_API_VERSION = "2022-11-28";
export const UA = "ilp-portfolio-gate";

export const PR_ACTIONS = new Set(["opened", "synchronize", "reopened"]);
export const SHA_RE = /^[0-9a-f]{40}$/i;

/** Singleton GateOrchestrator name. Every SHA shares one FIFO so jobs queue instead of starting more containers. */
export const GATE_QUEUE_NAME = "gate";
/** Singleton GateRunner id. One live standard-2 instance; max_instances = 1. */
export const GATE_RUNNER_ID = "gate";
