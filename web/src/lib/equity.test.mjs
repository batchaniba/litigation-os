/**
 * Math checks for equity calculations.
 * Run with: node --test web/src/lib/equity.test.mjs
 */

import test from "node:test";
import assert from "node:assert/strict";

const FEE_RATE = 0.3;

function tappable(homeValue, mortgage, ltv) {
  return Math.max(0, homeValue * ltv - mortgage);
}

function amortizingPayment(principal, aprPercent, years) {
  if (principal <= 0 || years <= 0) return 0;
  const months = years * 12;
  const r = aprPercent / 100 / 12;
  if (r === 0) return principal / months;
  const g = Math.pow(1 + r, months);
  return (principal * r * g) / (g - 1);
}

test("tappable equity uses the LTV cap, not raw equity", () => {
  // $700k home, $400k owed. Raw equity $300k; at 80% LTV only $160k borrowable.
  assert.equal(tappable(700_000, 400_000, 0.8), 160_000);
  assert.equal(700_000 - 400_000, 300_000);
});

test("appendix B-style scenario", () => {
  const draw = tappable(700_000, 300_000, 0.8);
  assert.equal(draw, 260_000);
  assert.equal(draw * FEE_RATE, 78_000);
  assert.equal(draw - draw * FEE_RATE, 182_000);
});

test("fee and net always reconcile to the draw", () => {
  for (const [value, owed, ltv] of [
    [500_000, 250_000, 0.8],
    [1_200_000, 600_000, 0.75],
    [850_000, 300_000, 0.85],
  ]) {
    const draw = tappable(value, owed, ltv);
    const fee = draw * FEE_RATE;
    assert.ok(Math.abs(fee + (draw - fee) - draw) < 1e-9);
    assert.ok(draw - fee < draw);
  }
});

test("no tappable equity clamps to zero", () => {
  assert.equal(tappable(400_000, 380_000, 0.8), 0);
  assert.equal(tappable(300_000, 400_000, 0.8), 0);
});

test("zero inputs do not produce NaN", () => {
  assert.equal(tappable(0, 0, 0.8), 0);
  assert.equal(amortizingPayment(0, 8.5, 20), 0);
  assert.ok(Number.isFinite(amortizingPayment(100_000, 0, 20)));
});

test("amortizing payment matches a known reference", () => {
  const payment = amortizingPayment(200_000, 8.5, 20);
  assert.ok(Math.abs(payment - 1735.72) < 1, `expected ~1735.72, got ${payment.toFixed(2)}`);
});

test("interest-only is less than amortizing payment", () => {
  const principal = 260_000;
  const interestOnly = (principal * 0.085) / 12;
  assert.ok(interestOnly < amortizingPayment(principal, 8.5, 20));
});
