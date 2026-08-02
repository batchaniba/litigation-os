import { EquityCalculator } from "../components/calculator/EquityCalculator";

export function CalculatorPage() {
  return (
    <main className="section" style={{ paddingTop: "calc(var(--nav-h) + 3rem)" }}>
      <div className="container">
        <p className="eyebrow">Run the numbers</p>
        <h1 className="section-title">Equity calculator</h1>
        <p className="section-lede">
          Paper equity is not what a lender will advance. This tool applies a loan-to-value cap, subtracts the
          milestone fee, and shows the monthly cost of carry — before anyone talks you into optimism.
        </p>
        <div style={{ marginTop: "2.5rem" }}>
          <EquityCalculator />
        </div>
      </div>
    </main>
  );
}
