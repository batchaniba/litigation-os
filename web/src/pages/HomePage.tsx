import type { ReactNode } from "react";
import { Link } from "react-router-dom";
import { BookingPanel } from "../components/BookingPanel";
import { EquityIQQuiz } from "../components/EquityIQQuiz";
import { CASE_STEPS, FAQS, PHASES } from "../data/content";
import { useReveal } from "../hooks/useReveal";

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
            <Link className="btn btn-ghost" to="/book">
              Book free orientation
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
                30% milestone fee on <em>equity extracted</em> — only at Phase 3.
              </div>
              <p className="fee-note">
                No fee on Bitcoin performance. No custody. No AUM. If the loan never funds, the success fee never
                invoices. That structure is the product.
              </p>
            </Reveal>
            <Reveal className="fee-example">
              <dl>
                <div>
                  <dt>Example extraction</dt>
                  <dd>$300,000</dd>
                </div>
                <div>
                  <dt>Success fee</dt>
                  <dd>$90,000</dd>
                </div>
                <div>
                  <dt>Due when</dt>
                  <dd style={{ fontSize: "1.25rem" }}>Verified approval / funding</dd>
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
            <h2 className="section-title">One household, five phases, full autonomy.</h2>
            <p className="section-lede">
              Illustrative only — not a promise of loan approval, Bitcoin quantity, or investment outcome.
            </p>
          </Reveal>
          <Reveal className="case-flow">
            {CASE_STEPS.map((row) => (
              <div className="case-row" key={row.label}>
                <span>{row.label}</span>
                <span>{row.value}</span>
              </div>
            ))}
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
              whether this path deserves another step. No sales theatrics — strategic partnership language only.
            </p>
            <p className="compliance-strip">
              Orientation is educational. Equity2Bitcoin does not arrange loans, execute trades, or take custody. Bring
              rough home value, mortgage balance, and your questions.
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
