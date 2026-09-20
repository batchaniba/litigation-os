import { CHECK_LOG_MAX_CHARS, CHECK_NAME } from "./constants.mjs";

/** Required GitHub Checks name. Branch protection must require this exact string. */
export { CHECK_NAME };

export function truncateLog(text, max = CHECK_LOG_MAX_CHARS) {
  const raw = String(text ?? "");
  if (raw.length <= max) return raw;
  const omitted = raw.length - max;
  return `${raw.slice(0, max)}\n\n… truncated (${omitted} more characters)`;
}

/** Fail-closed: every error path is `failure`. Never `neutral`. */
export function failClosedConclusion(_reason) {
  return "failure";
}

export function buildCheckOutput({
  ok,
  reason = "",
  log = "",
  sha = "",
  timeoutMs = null,
} = {}) {
  const shortSha = sha ? sha.slice(0, 12) : "unknown";
  if (ok) {
    return {
      title: `${CHECK_NAME} passed`,
      summary: `${CHECK_NAME} passed on ${shortSha}.`,
      text: truncateLog(log || "gate passed"),
    };
  }
  const why = reason || "gate failed";
  const timedOut = /timeout|no result within/i.test(why);
  const timeoutNote =
    timeoutMs && timedOut
      ? ` Fail-closed after ${Math.round(timeoutMs / 1000)}s.`
      : "";
  return {
    title: `${CHECK_NAME} failed`,
    summary: `${CHECK_NAME} failed on ${shortSha}: ${why}.${timeoutNote}`,
    text: truncateLog(log || why),
  };
}
