export function clipEvent(text, limit = 160) {
  const compact = String(text ?? "").replace(/\s+/g, " ").trim();
  if (compact.length <= limit) return compact;
  return `${compact.slice(0, limit - 1).trimEnd()}…`;
}

export function daysLabel(daysOut) {
  if (daysOut < 0) return `${Math.abs(daysOut)}d overdue`;
  if (daysOut === 0) return "today";
  return `in ${daysOut}d`;
}
