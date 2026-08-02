/**
 * Equity and fee arithmetic — single source for calculator + pricing examples.
 * Pure functions only.
 */

import { BTC_REFERENCE, MILESTONE_FEE_RATE } from "../config/site";

export interface EquityInputs {
  homeValue: number;
  mortgageBalance: number;
  /** Combined LTV cap as a fraction (0.8 = 80%). */
  maxLtv: number;
  aprPercent: number;
  amortizationYears: number;
}

export interface EquityResult {
  rawEquity: number;
  tappableEquity: number;
  milestoneFee: number;
  netToBitcoin: number;
  illustrativeBtc: number;
  monthlyInterestOnly: number;
  monthlyAmortizing: number;
  totalInterestOverTerm: number;
  feeRate: number;
  hasNoTappableEquity: boolean;
}

function clampMoney(value: number): number {
  if (!Number.isFinite(value) || value < 0) return 0;
  return value;
}

export function amortizingPayment(principal: number, aprPercent: number, years: number): number {
  if (principal <= 0 || years <= 0) return 0;
  const months = years * 12;
  const monthlyRate = aprPercent / 100 / 12;
  if (monthlyRate === 0) return principal / months;
  const growth = Math.pow(1 + monthlyRate, months);
  return (principal * monthlyRate * growth) / (growth - 1);
}

export function calculateEquity(inputs: EquityInputs): EquityResult {
  const homeValue = clampMoney(inputs.homeValue);
  const mortgageBalance = clampMoney(inputs.mortgageBalance);
  const maxLtv = Number.isFinite(inputs.maxLtv) ? inputs.maxLtv : 0;
  const aprPercent = Number.isFinite(inputs.aprPercent) ? Math.max(0, inputs.aprPercent) : 0;
  const years = Math.max(1, inputs.amortizationYears);

  const rawEquity = clampMoney(homeValue - mortgageBalance);
  // Lenders cap total borrowing at a share of value — mortgage debt eats into availability.
  const tappableEquity = clampMoney(homeValue * maxLtv - mortgageBalance);
  const milestoneFee = tappableEquity * MILESTONE_FEE_RATE;
  const netToBitcoin = tappableEquity - milestoneFee;
  const monthlyInterestOnly = (tappableEquity * (aprPercent / 100)) / 12;
  const monthlyAmortizing = amortizingPayment(tappableEquity, aprPercent, years);
  const totalInterestOverTerm = clampMoney(monthlyAmortizing * years * 12 - tappableEquity);

  return {
    rawEquity,
    tappableEquity,
    milestoneFee,
    netToBitcoin,
    illustrativeBtc: netToBitcoin / BTC_REFERENCE.priceUsd,
    monthlyInterestOnly,
    monthlyAmortizing,
    totalInterestOverTerm,
    feeRate: MILESTONE_FEE_RATE,
    hasNoTappableEquity: tappableEquity <= 0,
  };
}
