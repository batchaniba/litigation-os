const usd0 = new Intl.NumberFormat("en-US", {
  style: "currency",
  currency: "USD",
  maximumFractionDigits: 0,
});

const usd2 = new Intl.NumberFormat("en-US", {
  style: "currency",
  currency: "USD",
  maximumFractionDigits: 2,
});

export function formatUsd(value: number): string {
  return usd0.format(Number.isFinite(value) ? value : 0);
}

export function formatUsdPrecise(value: number): string {
  return usd2.format(Number.isFinite(value) ? value : 0);
}

export function formatBtc(value: number): string {
  if (!Number.isFinite(value) || value <= 0) return "0 BTC";
  if (value < 0.0001) return "under 0.0001 BTC";
  return `${value.toFixed(4)} BTC`;
}

export function formatPercent(fraction: number): string {
  return `${Math.round(fraction * 100)}%`;
}

export function parseCurrencyInput(raw: string): number {
  const digits = raw.replace(/[^0-9.]/g, "");
  const parsed = Number.parseFloat(digits);
  return Number.isFinite(parsed) ? parsed : 0;
}
