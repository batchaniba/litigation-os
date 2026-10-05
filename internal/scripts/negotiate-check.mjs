#!/usr/bin/env node
// Pre-send negotiation check. Run before any settlement number, withdrawal,
// or counter goes out (SETTLEMENT_REANCHOR_MEMO.md § 3 / § 5).
//
//   npm run negotiate:check -- --matter 27 --history
//   npm run negotiate:check -- --matter 27 --amount 25000 --scope global \
//       --buys defense_number --event "Delaney denied the MTD"
//   npm run negotiate:check -- --matter 27 --withdraw
//   ... --gives-time            the same move extends a defense clock
//   ... --trades default,waiver  the move gives up a default / clock / waiver
//   ... --for-money              that trade is paid for in money or a counter
//   ... --override "reason"      Plaintiff's deliberate decision to send anyway;
//                                requires --record so the reason is kept
//   ... --record                 append the move (and any override) to the ledger
//
// Exit 0: clear. Exit 1: blocked (rules listed). Exit 2: usage or ledger error.
import fs from "node:fs";
import path from "node:path";
import { fileURLToPath } from "node:url";
import {
  LEDGER_DIR,
  PRE_SEND_CHECKLIST,
  RULES,
  checkMove,
  fmt,
  formatHistory,
  parseLedger,
} from "./lib/negotiation.mjs";

const ROOT = path.resolve(path.dirname(fileURLToPath(import.meta.url)), "../..");
const args = process.argv.slice(2);
const flag = (name) => args.includes(name);
function opt(name) {
  const i = args.indexOf(name);
  return i >= 0 && args[i + 1] && !args[i + 1].startsWith("--") ? args[i + 1] : null;
}
function die(msg) {
  process.stderr.write(`negotiate:check: ${msg}\n`);
  process.exit(2);
}

const matter = opt("--matter");
if (!matter || !/^\d{1,2}$/.test(matter)) die("--matter NN is required");
const file = path.join(ROOT, LEDGER_DIR, `${matter.padStart(2, "0")}.jsonl`);
const ledger = fs.existsSync(file) ? parseLedger(fs.readFileSync(file, "utf8"), path.relative(ROOT, file)) : [];

if (flag("--history")) {
  process.stdout.write(`${ledger.length ? formatHistory(ledger) : "(no moves recorded)"}\n`);
  if (!args.includes("--amount") && !flag("--withdraw")) process.exit(0);
}

const today = new Date().toLocaleDateString("en-CA", { timeZone: "America/Los_Angeles" });
const amountRaw = opt("--amount");
const proposed = {
  kind: flag("--withdraw") ? "withdraw" : "demand",
  amount: amountRaw != null ? Number(String(amountRaw).replace(/[$,]/g, "")) : undefined,
  scope: opt("--scope") ?? "global",
  buys: opt("--buys") ?? undefined,
  event: opt("--event") ?? undefined,
  gives_time: flag("--gives-time"),
  trades: opt("--trades") ? opt("--trades").split(",").map((s) => s.trim()) : [],
  for_money: flag("--for-money"),
};
if (proposed.kind === "demand" && !(Number.isFinite(proposed.amount) && proposed.amount >= 0))
  die("--amount <number> is required for a demand (or pass --withdraw)");

const result = checkMove(ledger, proposed);
const override = opt("--override");
const label =
  proposed.kind === "withdraw"
    ? `WITHDRAW${proposed.amount != null ? ` → $${fmt(proposed.amount)}` : " (no replacement)"}`
    : `$${fmt(proposed.amount)} ${proposed.scope}`;

const out = [];
out.push(`Matter ${matter} — proposed: ${label}`);
if (result.ok) out.push("CLEAR — no hard rule is broken.");
else {
  out.push(`BLOCKED — ${result.blocks.length} rule(s):`);
  for (const b of result.blocks) out.push(`  ✗ ${b.rule}: ${b.why}\n      Rule: ${RULES[b.rule] ?? ""}`);
}
for (const w of result.warnings) out.push(`  ! ${w.rule}: ${w.why}`);
out.push("", "Pre-send checklist (memo § 5) — show Plaintiff each item:");
PRE_SEND_CHECKLIST.forEach((item, i) => out.push(`  ${i + 1}. ${item}`));
process.stdout.write(`${out.join("\n")}\n`);

const proceed = result.ok || Boolean(override);
if (override && !flag("--record")) die("--override needs --record so the reason is kept in the ledger");

if (flag("--record") && proceed) {
  fs.mkdirSync(path.dirname(file), { recursive: true });
  const lines = [];
  if (!result.ok)
    lines.push({
      date: today,
      side: "plaintiff",
      kind: "override",
      note: `Sent despite ${result.blocks.map((b) => b.rule).join(", ")}: ${override}`,
    });
  const move = { date: today, side: "plaintiff", kind: proposed.kind, scope: proposed.scope };
  if (proposed.amount != null) move.amount = proposed.amount;
  if (proposed.buys) move.buys = proposed.buys;
  if (proposed.event) move.event = proposed.event;
  lines.push(move);
  fs.appendFileSync(file, lines.map((l) => JSON.stringify(l)).join("\n") + "\n");
  process.stdout.write(`Recorded in ${path.relative(ROOT, file)}.\n`);
} else if (flag("--record")) {
  process.stdout.write("Not recorded: the move is blocked. Pass --override \"reason\" to record a deliberate exception.\n");
}

process.exit(proceed ? 0 : 1);
