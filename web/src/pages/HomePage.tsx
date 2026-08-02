import type { ReactNode } from "react";
import { Link } from "react-router-dom";
import { BookingPanel } from "../components/BookingPanel";
import { EquityIQQuiz } from "../components/EquityIQQuiz";
import { CALCULATOR_DEFAULTS, MILESTONE_FEE_RATE } from "../config/site";
import { FAQS, PHASES, VOLATILITY_STATEMENT } from "../data/content";
import { useReveal } from "../hooks/useReveal";
import { calculateEquity } from "../lib/equity";
import { formatPercent, formatUsd, formatUsdPrecise } from "../lib/format";

function Reveal({ className = "", children }: { className?: string; children: ReactNode }) {
  const ref = useReveal<HTMLDivElement>();
  return (
    <div ref={ref} className={`reveal ${className}`.trim()}>
      {children}
    </div>
  );
}

function PathStep({
  phase,
  delay,
}: {
  phase: (typeof PHASES)[number];
  delay: number;
}) {
  const ref = useReveal<HTMLElement>();
  return (
    <article ref={ref} className="path-step" style={{ transitionDelay: `${delay}ms` }}>
      <div className="path-index">{phase.index}</div>
      <div>
        <h3>{phase.title}</h3>
        <p>{phase.body}</p>
      </div>
      <div className={`path-fee${phase.paid ? " is-paid" : ""}`}>{phase.fee}</div>
    </article>
  );
}

function PathSteps() {
  return (
    <div className="path-list">
      {PHASES.map((phase, i) => (
        <PathStep key={phase.index} phase={phase} delay={i * 70} />
      ))}
    </div>
  );
}

const EXAMPLE = calculateEquity({
  homeValue: 700_000,
  mortgageBalance: 300_000,
  maxLtv: CALCULATOR_DEFAULTS.maxLtv,
  aprPercent: CALCULATOR_DEFAULTS.aprPercent,
  amortizationYears: CALCULATOR_DEFAULTS.amortizationYears,
});

export function HomePage() {
  return (
    <main>
      <section className="hero" aria-label="Introduction">
        <div className="hero-media">
          <img
            src="/hero-home.jpg"
            alt="Modern residence at dusk — visual stand-in for the home equity behind the strategy"
            width={2400}
            height={1592}
            fetchPriority="high"
          />
        </div>
        <div className="hero-scrim" />
        <div className="hero-content">
          <h1 className="hero-brand">
            Equity<span>2</span>Bitcoin
          </h1>
          <p className="hero-headline">Equity isn’t wealth until it moves.</p>
          <p className="hero-support">
            A compliant, education-first path for homeowners ready to unlock dormant equity and build a self-custodied
            Bitcoin position — without handing anyone your money or your keys.
          </p>
          <div className="hero-actions">
            <a className="btn btn-primary" href="#equity-iq">
              Check your Equity IQ
            </a>
            <Link className="btn btn-ghost" to="/calculator">
              Run the calculator
            </Link>
          </div>
        </div>
      </section>

      <section className="section problem" id="problem">
        <div className="container problem-grid">
          <Reveal>
            <p className="eyebrow">The wake-up call</p>
            <h2 className="section-title">Trillions sit idle in walls while scarcity compounds elsewhere.</h2>
            <p className="section-lede">
              American homeowners hold record tappable equity. Most were never shown a structured, non-custodial way to
              understand HELOC and refinance pathways alongside Bitcoin literacy. Banks won’t teach it. Random crypto
              Twitter shouldn’t either.
            </p>
          </Reveal>
          <Reveal className="stat-stack">
            <div className="stat">
              <strong>$17.2T</strong>
              <span>U.S. home equity context cited in our 2025 planning baseline</span>
            </div>
            <div className="stat">
              <strong>~$300K</strong>
              <span>Average tappable equity band many households sit on without a plan</span>
            </div>
            <div className="stat">
              <strong>&lt;3%</strong>
              <span>Bitcoin adoption among homeowners — the gap we educate into</span>
            </div>
          </Reveal>
        </div>
      </section>

      <section className="section" id="how-it-works">
        <div className="container">
          <Reveal>
            <p className="eyebrow">The five milestone phases</p>
            <h2 className="section-title">A clear path. One paid gate. You stay in control.</h2>
            <p className="section-lede">
              Equity2Bitcoin is consulting and education — not lending, brokerage, or investment advice. Fees trigger
              only when equity extraction is verified.
            </p>
          </Reveal>
          <PathSteps />
        </div>
      </section>

      <section className="section quiz" id="equity-iq">
        <div className="container quiz-shell">
          <Reveal>
            <p className="eyebrow">Qualify in five minutes</p>
            <h2 className="section-title">What’s your Equity IQ?</h2>
            <p className="section-lede">
              A short readiness check — equity range, ownership tenure, Bitcoin familiarity, and timing. Your result
              carries into the orientation booking so the conversation starts informed.
            </p>
          </Reveal>
          <EquityIQQuiz />
        </div>
      </section>

      <section className="section fees" id="fees">
        <div className="container">
          <Reveal>
            <p className="eyebrow">Transparent pricing</p>
            <h2 className="section-title">Pay for extraction. Never for price charts.</h2>
          </Reveal>
          <div className="fee-band">
            <Reveal>
              <div className="fee-formula">
                {formatPercent(MILESTONE_FEE_RATE)} milestone fee on <em>equity extracted</em> — only at Phase 3.
              </div>
              <p className="fee-note">
                No fee on Bitcoin performance. No custody. No AUM. If the loan never funds, the success fee never
                invoices. Less than you borrow reaches Bitcoin — the calculator shows that subtraction on purpose.
              </p>
              <p style={{ marginTop: "1.25rem" }}>
                <Link to="/calculator" className="btn btn-ghost">
                  Run your numbers
                </Link>
              </p>
            </Reveal>
            <Reveal className="fee-example">
              <dl>
                <div>
                  <dt>Worked example (80% LTV)</dt>
                  <dd style={{ fontSize: "1.15rem" }}>
                    {formatUsd(700_000)} home · {formatUsd(300_000)} owed
                  </dd>
                </div>
                <div>
                  <dt>Actually borrowable</dt>
                  <dd>{formatUsd(EXAMPLE.tappableEquity)}</dd>
                </div>
                <div>
                  <dt>Success fee → reaches Bitcoin</dt>
                  <dd style={{ fontSize: "1.35rem" }}>
                    −{formatUsd(EXAMPLE.milestoneFee)} → {formatUsd(EXAMPLE.netToBitcoin)}
                  </dd>
                </div>
              </dl>
            </Reveal>
          </div>
        </div>
      </section>

      <section className="section case" id="example">
        <div className="container">
          <Reveal>
            <p className="eyebrow">Hypothetical walkthrough</p>
            <h2 className="section-title">Paper equity is not borrowable equity.</h2>
            <p className="section-lede">
              Same household math the calculator uses — fee subtracted, carry cost shown. Illustrative only.
            </p>
          </Reveal>
          <Reveal className="case-flow">
            <div className="case-row">
              <span>Home value</span>
              <span>{formatUsd(700_000)}</span>
            </div>
            <div className="case-row">
              <span>Remaining mortgage</span>
              <span>{formatUsd(300_000)}</span>
            </div>
            <div className="case-row">
              <span>Equity on paper</span>
              <span>{formatUsd(EXAMPLE.rawEquity)}</span>
            </div>
            <div className="case-row">
              <span>Actually borrowable at 80% LTV</span>
              <span>{formatUsd(EXAMPLE.tappableEquity)}</span>
            </div>
            <div className="case-row">
              <span>Milestone fee ({formatPercent(MILESTONE_FEE_RATE)})</span>
              <span>{formatUsd(EXAMPLE.milestoneFee)}</span>
            </div>
            <div className="case-row">
              <span>Reaches Bitcoin</span>
              <span>{formatUsd(EXAMPLE.netToBitcoin)}</span>
            </div>
            <div className="case-row">
              <span>Interest-only monthly (illustrative {CALCULATOR_DEFAULTS.aprPercent}%)</span>
              <span>{formatUsdPrecise(EXAMPLE.monthlyInterestOnly)}</span>
            </div>
          </Reveal>
          <Reveal>
            <p className="compliance-strip" style={{ marginTop: "1.5rem" }}>
              {VOLATILITY_STATEMENT}
            </p>
          </Reveal>
        </div>
      </section>

      <section className="section booking" id="book">
        <div className="container booking-grid">
          <Reveal>
            <p className="eyebrow">Conversion</p>
            <h2 className="section-title">Book a free orientation.</h2>
            <p className="section-lede">
              A consultative first conversation: your equity picture, the milestone agreement in plain English, and
              whether this path deserves another step — including an honest “this is not for you” if that is true.
            </p>
            <p className="compliance-strip">
              Orientation is educational. Equity2Bitcoin does not arrange loans, execute trades, or take custody. Prefer
              a fuller acknowledgment gate? Use the dedicated <Link to="/book">booking page</Link>.
            </p>
            <p style={{ marginTop: "1rem" }}>
              <Link to="/fit" className="btn btn-ghost">
                Is this for you?
              </Link>
            </p>
          </Reveal>
          <BookingPanel />
        </div>
      </section>

      <section className="section faq" id="faq">
        <div className="container">
          <Reveal>
            <p className="eyebrow">FAQ</p>
            <h2 className="section-title">Straight answers before you book.</h2>
          </Reveal>
          <div style={{ marginTop: "2rem" }}>
            {FAQS.map((item) => (
              <details key={item.q}>
                <summary>{item.q}</summary>
                <p>{item.a}</p>
              </details>
            ))}
          </div>
        </div>
      </section>
    </main>
  );
}
