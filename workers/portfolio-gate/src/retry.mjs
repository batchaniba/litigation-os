// Retry helper for Cloudflare Containers capacity errors. After destroy()
// the previous instance can still count against max_instances for a beat
// (https://developers.cloudflare.com/containers/guides/migrate-to-durable-object-container-api/).

export const CAPACITY_ERROR_RE = /maximum number of running container instances exceeded/i;

/** Immediate, then 2s / 5s / 10s. Four tries stay well under GATE_TIMEOUT_MS. */
export const CAPACITY_RETRY_DELAYS_MS = [0, 2000, 5000, 10_000];

export function isCapacityError(err) {
  return CAPACITY_ERROR_RE.test(String(err?.message || err));
}

export async function retryOnCapacity(
  fn,
  {
    delays = CAPACITY_RETRY_DELAYS_MS,
    sleep = (ms) => new Promise((resolve) => setTimeout(resolve, ms)),
  } = {},
) {
  let lastErr;
  for (let i = 0; i < delays.length; i += 1) {
    if (delays[i] > 0) await sleep(delays[i]);
    try {
      return await fn();
    } catch (err) {
      lastErr = err;
      if (!isCapacityError(err) || i === delays.length - 1) throw err;
    }
  }
  throw lastErr;
}
