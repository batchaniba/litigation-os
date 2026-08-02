import { useMemo, useState } from "react";
import { Link } from "react-router-dom";
import { BTC_REFERENCE, CALCULATOR_DEFAULTS } from "../../config/site";
import { calculateEquity } from "../../lib/equity";
import { formatBtc, formatPercent, formatUsd, formatUsdPrecise, parseCurrencyInput } from "../../lib/format";

export function EquityCalculator() {
  const [homeValue, setHomeValue] = useState<number>(CALCULATOR_DEFAULTS.homeValue);
  const [mortgageBalance, setMortgageBalance] = useState<number>(CALCULATOR_DEFAULTS.mortgageBalance);
  const [maxLtv, setMaxLtv] = useState<number>(CALCULATOR_DEFAULTS.maxLtv);
  const [aprPercent, setAprPercent] = useState<number>(CALCULATOR_DEFAULTS.aprPercent);

  const result = useMemo(
    () =>
      calculateEquity({
        homeValue,
        mortgageBalance,
        maxLtv,
        aprPercent,
        amortizationYears: CALCULATOR_DEFAULTS.amortizationYears,
      }),
    [homeValue, mortgageBalance, maxLtv, aprPercent],
  );

  return (
    <div className="calc">
      <form className="calc-inputs" onSubmit={(e) => e.preventDefault()}>
        <h2 className="calc-inputs-title">Your numbers</h2>

        <label className="calc-field">
          <span className="calc-label">What is your home worth today?</span>
          <span className="calc-hint">Best estimate of current market value.</span>
          <input
            type="text"
            inputMode="numeric"
            value={formatUsd(homeValue)}
            onChange={(e) => setHomeValue(parseCurrencyInput(e.target.value))}
          />
        </label>

        <label className="calc-field">
          <span className="calc-label">What do you still owe?</span>
          <span className="calc-hint">Combined balance of mortgages and existing equity lines.</span>
          <input
            type="text"
            inputMode="numeric"
            value={formatUsd(mortgageBalance)}
            onChange={(e) => setMortgageBalance(parseCurrencyInput(e.target.value))}
          />
        </label>

        <label className="calc-field">
          <span className="calc-label">
            Lender loan-to-value cap <em>{Math.round(maxLtv * 100)}%</em>
          </span>
          <span className="calc-hint">Most lenders cap total borrowing near 80% of value.</span>
          <input
            type="range"
            min={CALCULATOR_DEFAULTS.ltvMin * 100}
            max={CALCULATOR_DEFAULTS.ltvMax * 100}
            step={1}
            value={maxLtv * 100}
            onChange={(e) => setMaxLtv(Number(e.target.value) / 100)}
          />
        </label>

        <label className="calc-field">
          <span className="calc-label">
            Estimated rate on the new line <em>{aprPercent.toFixed(2)}%</em>
          </span>
          <span className="calc-hint">Illustrative only — confirm APR with your lender.</span>
          <input
            type="range"
            min={4}
            max={15}
            step={0.25}
            value={aprPercent}
            onChange={(e) => setAprPercent(Number(e.target.value))}
          />
        </label>

        <p className="calc-privacy">Nothing you type here is sent anywhere. This runs in your browser.</p>
      </form>

      <div className="calc-results">
        {result.hasNoTappableEquity ? (
          <div className="calc-empty">
            <h3>No tappable equity at these numbers</h3>
            <p>
              At this loan-to-value cap, what you owe already meets or exceeds what a lender would typically let you
              borrow. Paper equity is {formatUsd(result.rawEquity)}, but lenders require a cushion.
            </p>
          </div>
        ) : (
          <>
            <div className="calc-headline">
              <span className="eyebrow">Potentially borrowable</span>
              <p className="calc-big">{formatUsd(result.tappableEquity)}</p>
              <p className="calc-note">
                Equity on paper is {formatUsd(result.rawEquity)}. Lenders cap total borrowing at a share of value, so
                the borrowable figure is lower.
              </p>
            </div>

            <div className="calc-flow">
              <h3>Where that money actually goes</h3>
              <dl>
                <div>
                  <dt>Amount drawn from your lender</dt>
                  <dd>{formatUsd(result.tappableEquity)}</dd>
                </div>
                <div className="is-debit">
                  <dt>
                    Milestone fee ({formatPercent(result.feeRate)})
                    <span>Charged once at funding</span>
                  </dt>
                  <dd>−{formatUsd(result.milestoneFee)}</dd>
                </div>
                <div className="is-total">
                  <dt>Reaches Bitcoin</dt>
                  <dd>{formatUsd(result.netToBitcoin)}</dd>
                </div>
                <div className="is-sub">
                  <dt>
                    Roughly
                    <span>
                      at {formatUsd(BTC_REFERENCE.priceUsd)} / BTC as of {BTC_REFERENCE.asOf} — illustrative, not a
                      live quote
                    </span>
                  </dt>
                  <dd>{formatBtc(result.illustrativeBtc)}</dd>
                </div>
              </dl>
            </div>

            <div className="calc-carry">
              <h3>What it costs to carry</h3>
              <div className="calc-carry-grid">
                <div>
                  <span>Interest-only, monthly</span>
                  <strong>{formatUsdPrecise(result.monthlyInterestOnly)}</strong>
                  <small>Typical HELOC draw period. Pays nothing toward principal.</small>
                </div>
                <div>
                  <span>Fully amortizing over {CALCULATOR_DEFAULTS.amortizationYears} years</span>
                  <strong>{formatUsdPrecise(result.monthlyAmortizing)}</strong>
                  <small>{formatUsd(result.totalInterestOverTerm)} interest over the full term.</small>
                </div>
              </div>
            </div>

            <div className="calc-meaning">
              <h3>What this means</h3>
              <p>
                You would owe your lender <strong>{formatUsd(result.tappableEquity)}</strong>, secured against your
                home, and hold roughly <strong>{formatUsd(result.netToBitcoin)}</strong> of Bitcoin — because{" "}
                {formatUsd(result.milestoneFee)} went to the milestone fee. You start{" "}
                {formatPercent(result.feeRate)} behind on day one, before Bitcoin moves at all.
              </p>
              <p>
                At {aprPercent.toFixed(2)}% that is{" "}
                <strong>{formatUsdPrecise(result.monthlyInterestOnly)} a month</strong> in interest alone, due
                regardless of what Bitcoin does. If an 80% Bitcoin decline would leave you unable to make this payment
                from ordinary income, this strategy is not appropriate for you.
              </p>
            </div>

            <div className="calc-actions">
              <Link to="/book" className="btn btn-primary">
                Talk through these numbers
              </Link>
              <Link to="/fit" className="btn btn-ghost">
                Is this actually for me?
              </Link>
            </div>

            <p className="calc-legal">
              <strong>Estimate only.</strong> Not a loan offer, pre-qualification, quote, or investment advice. Your
              lender sets actual limits, rates, and terms after underwriting.
            </p>
          </>
        )}
      </div>
    </div>
  );
}
