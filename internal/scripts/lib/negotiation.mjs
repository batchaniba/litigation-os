// Negotiation guardrails: pure rule engine over a matter's offer ledger.
//
// The rules are the hard rules in internal/docs/settlement/SETTLEMENT_REANCHOR_MEMO.md
// § 3, written after Randstad (Matter 27): Plaintiff cut his own figure twice
// ($55k/$85k → withdrawn → $25k global) without one defense number, while a
// higher $40k draft that held the clocks sat unsent. The memo was prose, so
// nothing stopped the next draft from doing the same. This makes the rules
// checkable: a proposed move is tested against the ledger before it goes out.
//
// Ledger: internal/private/negotiation/NN.jsonl, one move per line, oldest
// first. Private: never published, seeded, or quoted (see that README).
//
//   { date, side: "plaintiff"|"defense", kind, amount?, scope?, status?, buys?, event?, note? }
//
// kinds
//   plaintiff: demand (a figure sent), draft (prepared, unsent), withdraw,
//              walkaway (private reservation point), override (a recorded
//              decision to send despite a block)
//   defense:   counter / offer / accept (a defense NUMBER), request_time,
//              conferring, reject (no number — these are not counters)
//   either:    term (non-price terms such as allocation), note

export const LEDGER_DIR = "internal/private/negotiation";

export const PLAINTIFF_KINDS = new Set(["demand", "draft", "withdraw", "walkaway", "override", "term", "note"]);
export const DEFENSE_KINDS = new Set(["counter", "offer", "accept", "request_time", "conferring", "reject", "term", "note"]);
/** Defense moves that put a number on the table. Everything else is not a counter. */
export const DEFENSE_NUMBER_KINDS = new Set(["counter", "offer", "accept"]);

/** What a concession may buy (memo Rule 3). */
export const BUYS = new Set([
  "defense_number",
  "document",
  "held_clock",
  "narrower_release",
  "prompt_payment",
  "non_cash_relief",
]);

/** Pressure is not an event (memo Rule 4). */
const PRESSURE_RE = /\b(deadline|default|rent|cash|need(s|ed)? (the )?money|payment due|bills?|pressure|speed|quick(ly)?|before (the )?(hearing|answer))\b/i;

export const RULES = {
  R1: "After the opening, no move without their number. Silence, 'conferring', and requests for time are not counters.",
  R2: "Never withdraw a figure without a replacement, and never pair a price cut with extra defense time.",
  R3: "No unearned discount: every concession buys something identifiable and recorded.",
  R4: "Reprice on events, not pressure. A deadline, default motion, rent, or promised payment is not an event.",
  R6: "Write the walk-away before each send. If a drafted figure is higher than the one about to go out, stop and reconcile.",
  R7: "Never trade a default, clock, or waiver for procedure alone. Trade it for money or a counter.",
  WALKAWAY: "Below the private walk-away.",
};

export function parseLedger(text, label = "ledger") {
  const moves = [];
  text.split("\n").forEach((line, i) => {
    const t = line.trim();
    if (!t) return;
    let m;
    try {
      m = JSON.parse(t);
    } catch {
      throw new Error(`${label}:${i + 1}: not JSON`);
    }
    const problems = validateMove(m);
    if (problems.length) throw new Error(`${label}:${i + 1}: ${problems.join("; ")}`);
    moves.push(m);
  });
  return moves;
}

export function validateMove(m) {
  const p = [];
  if (!m || typeof m !== "object") return ["not an object"];
  if (!/^\d{4}-\d{2}-\d{2}$/.test(String(m.date ?? ""))) p.push("date must be YYYY-MM-DD");
  if (m.side !== "plaintiff" && m.side !== "defense") p.push("side must be plaintiff|defense");
  const kinds = m.side === "defense" ? DEFENSE_KINDS : PLAINTIFF_KINDS;
  if (!kinds.has(m.kind)) p.push(`kind '${m.kind}' not allowed for ${m.side}`);
  if (m.amount != null && !(Number.isFinite(m.amount) && m.amount >= 0)) p.push("amount must be a non-negative number");
  if (["demand", "draft", "walkaway", "counter", "offer", "accept"].includes(m.kind) && m.amount == null)
    p.push(`${m.kind} needs an amount`);
  if (m.buys != null && !BUYS.has(m.buys)) p.push(`buys must be one of ${[...BUYS].join(", ")}`);
  return p;
}

const sameScope = (a, b) => (a ?? "global") === (b ?? "global");

/** The last live plaintiff figure per scope, honoring withdrawals. */
function liveFigures(ledger) {
  const live = new Map();
  for (const m of ledger) {
    if (m.side !== "plaintiff") continue;
    if (m.kind === "demand") live.set(m.scope ?? "global", m);
    if (m.kind === "withdraw") {
      if (m.scope) live.delete(m.scope);
      else live.clear();
    }
  }
  return live;
}

/** Highest plaintiff figure ever put on the table for a scope (sent, not drafts). */
function highestSent(ledger, scope) {
  return ledger
    .filter((m) => m.side === "plaintiff" && m.kind === "demand" && sameScope(m.scope, scope))
    .reduce((best, m) => (best == null || m.amount > best.amount ? m : best), null);
}

/**
 * Check one proposed plaintiff move against the ledger.
 * proposed: { kind: "demand"|"withdraw", amount?, scope?, buys?, event?,
 *             gives_time?: bool, trades?: ["default"|"clock"|"waiver"], for_money?: bool }
 * Returns { ok, blocks: [{rule, why}], warnings: [{rule, why}] }.
 */
export function checkMove(ledger, proposed) {
  const blocks = [];
  const warnings = [];
  const block = (rule, why) => blocks.push({ rule, why });
  const scope = proposed.scope ?? "global";

  const plaintiffMoves = ledger.filter((m) => m.side === "plaintiff" && (m.kind === "demand" || m.kind === "withdraw"));
  const lastOwn = plaintiffMoves.at(-1) ?? null;
  const lastOwnIdx = lastOwn ? ledger.lastIndexOf(lastOwn) : -1;
  const defenseNumberSince = ledger
    .slice(lastOwnIdx + 1)
    .filter((m) => m.side === "defense" && DEFENSE_NUMBER_KINDS.has(m.kind));
  const defenseNonNumbersSince = ledger
    .slice(lastOwnIdx + 1)
    .filter((m) => m.side === "defense" && !DEFENSE_NUMBER_KINDS.has(m.kind) && m.kind !== "note" && m.kind !== "term");

  // Reference point: the live figure for this scope, else the highest ever
  // sent for it (a withdrawal does not erase what was on the table).
  const reference = liveFigures(ledger).get(scope) ?? highestSent(ledger, scope);
  // A global figure is also a cut against any single-defendant figure above it.
  const anyHigherSent = ledger
    .filter((m) => m.side === "plaintiff" && m.kind === "demand")
    .filter((m) => scope === "global" && m.amount > (proposed.amount ?? Infinity));
  const isCut =
    proposed.kind === "withdraw" ||
    (proposed.kind === "demand" && reference != null && proposed.amount < reference.amount) ||
    (proposed.kind === "demand" && anyHigherSent.length > 0);

  // R2: withdrawal without replacement.
  if (proposed.kind === "withdraw" && proposed.amount == null)
    block("R2", "Withdrawing a figure with no replacement leaves the defense nothing to answer and invites your next number to be lower.");

  // R1: moving against yourself.
  if (lastOwn && isCut && defenseNumberSince.length === 0) {
    const waited = defenseNonNumbersSince.length
      ? ` Since then the defense has only: ${defenseNonNumbersSince.map((m) => `${m.kind} (${m.date})`).join(", ")}.`
      : " The defense has said nothing with a number since.";
    block(
      "R1",
      `Your last move was ${lastOwn.kind === "withdraw" ? "a withdrawal" : `$${fmt(lastOwn.amount)} ${lastOwn.scope ?? "global"}`} on ${lastOwn.date}.${waited} A lower figure now is negotiating against yourself.`,
    );
  }

  // R2b: price cut paired with more defense time.
  if (isCut && proposed.gives_time)
    block("R2", "This cuts the price and gives the defense more time in the same move.");

  // R3 / R4: what the concession buys, and the event behind it.
  if (isCut && proposed.kind === "demand") {
    if (!proposed.buys || !BUYS.has(proposed.buys))
      block("R3", `A lower figure must buy something recorded: one of ${[...BUYS].join(", ")}.`);
    if (!proposed.event) block("R4", "Name the event (ruling, report, admission, discovery, coverage, trial proximity) that justifies repricing.");
    else if (PRESSURE_RE.test(proposed.event))
      block("R4", `"${proposed.event}" is pressure, not an event.`);
  }

  // R6: walk-away written, and no higher unsent draft.
  const walkaway = ledger.filter((m) => m.side === "plaintiff" && m.kind === "walkaway" && sameScope(m.scope, scope)).at(-1);
  if (proposed.kind === "demand") {
    if (!walkaway) block("R6", `No walk-away is written for scope '${scope}'. Record one before any number goes out.`);
    else if (proposed.amount < walkaway.amount)
      block("WALKAWAY", `$${fmt(proposed.amount)} is below the private walk-away for '${scope}'.`);
    // Only drafts prepared after the last thing actually sent: a later send
    // supersedes older drafts.
    const higherDraft = ledger
      .slice(lastOwnIdx + 1)
      .filter((m) => m.side === "plaintiff" && m.kind === "draft" && sameScope(m.scope, scope) && m.amount > proposed.amount);
    if (higherDraft.length)
      block(
        "R6",
        `A higher draft exists and was not sent: ${higherDraft.map((d) => `$${fmt(d.amount)} (${d.date}${d.note ? `: ${d.note}` : ""})`).join("; ")}. Reconcile before sending less.`,
      );
  }

  // R7: trading a default, clock, or waiver for procedure alone.
  if (Array.isArray(proposed.trades) && proposed.trades.length && !proposed.for_money && defenseNumberSince.length === 0)
    block("R7", `Giving up ${proposed.trades.join(", ")} for procedure alone. Trade it for money or a counter.`);

  if (!lastOwn && proposed.kind === "demand")
    warnings.push({ rule: "OPEN", why: "This is the opening figure. Run the § 4A engine where it fits and check the § 4 bracket." });

  return { ok: blocks.length === 0, blocks, warnings };
}

export function fmt(n) {
  return Number(n).toLocaleString("en-US", { maximumFractionDigits: 2 });
}

/** One line per move, oldest first, for a phone screen. */
export function formatHistory(ledger) {
  return ledger
    .filter((m) => m.kind !== "walkaway") // private reservation points stay off screen unless asked
    .map((m) => {
      const who = m.side === "plaintiff" ? "YOU" : "THEM";
      const amt = m.amount != null ? ` $${fmt(m.amount)}` : "";
      const scope = m.scope ? ` ${m.scope}` : "";
      const status = m.kind === "draft" ? " (unsent)" : "";
      return `${m.date} ${who.padEnd(4)} ${m.kind}${amt}${scope}${status}${m.note ? ` — ${m.note}` : ""}`;
    })
    .join("\n");
}

export const PRE_SEND_CHECKLIST = [
  "Latest docket, operative pleading, pending-motion status",
  "Current offer status and expiration on both sides",
  "Produced evidence (consumer report and its source line)",
  "Shared-loss ledger entry for this matter",
  "Opening / target / private walk-away as separate decisions",
  "Non-cash terms, each valued with a completion deadline",
  "Release scope (memo § 9)",
  "What this move buys (Rule 3) and the event behind it (Rule 4)",
  "Deadline consequences: the send must not extend or soften any defense clock",
];
