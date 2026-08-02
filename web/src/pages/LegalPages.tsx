import { SITE } from "../config/site";
import { BRAND } from "../data/content";

export function TermsPage() {
  return (
    <main className="legal-page">
      <div className="container">
        <h1>Terms of Service</h1>
        <p>Last updated: August 2, 2026</p>
        <p>
          These Terms govern your use of {BRAND.name} digital properties operated by {BRAND.legalName}. By accessing
          the site or requesting a consultation, you agree to these Terms.
        </p>
        <h2>Educational services only</h2>
        <p>
          Equity2Bitcoin provides educational consulting and milestone-based documentation support. We are not a bank,
          mortgage lender, mortgage broker, investment adviser, commodity trading adviser, broker-dealer, money
          transmitter, or Bitcoin custodian.
        </p>
        <h2>No guarantees</h2>
        <p>
          We do not guarantee loan approval, interest rates, Bitcoin purchase execution, Bitcoin performance, tax
          outcomes, or any financial result. Hypothetical examples on the site are illustrative only.
        </p>
        <h2>Client responsibility</h2>
        <p>
          You remain solely responsible for evaluating risks, selecting lenders and platforms, executing transactions,
          securing private keys, and complying with applicable law. You should consult independent legal, tax, and
          financial professionals as needed.
        </p>
        <h2>Fees</h2>
        <p>
          Success fees, if any, are defined in a written Milestone Agreement and are triggered only by verified
          milestones stated therein — typically verified equity extraction — not by investment performance.
        </p>
        <h2>Contact</h2>
        <p>Questions about these Terms: {SITE.email}</p>
      </div>
    </main>
  );
}

export function PrivacyPage() {
  return (
    <main className="legal-page">
      <div className="container">
        <h1>Privacy Policy</h1>
        <p>Last updated: August 2, 2026</p>
        <p>
          {BRAND.legalName} respects your privacy. This Policy describes how we collect and use information when you
          use Equity2Bitcoin.com or request an orientation.
        </p>
        <h2>Information we collect</h2>
        <ul>
          <li>Contact details you submit (name, email, phone)</li>
          <li>Equity IQ quiz responses and readiness notes</li>
          <li>Scheduling metadata if you book via Calendly</li>
          <li>Standard server/analytics logs (IP, device, pages viewed)</li>
        </ul>
        <h2>How we use information</h2>
        <ul>
          <li>To respond to consultation requests and operate the milestone workflow</li>
          <li>To improve educational content and site experience</li>
          <li>To meet legal, security, and compliance recordkeeping needs</li>
        </ul>
        <h2>Sharing</h2>
        <p>
          We do not sell personal information. We may use processors such as scheduling, CRM, analytics, and email
          tools under contractual safeguards. We never take custody of your loan proceeds or Bitcoin.
        </p>
        <h2>Retention & rights</h2>
        <p>
          We retain information as needed for the engagement and legitimate business records. Depending on your
          jurisdiction, you may request access, correction, or deletion by contacting {SITE.email}.
        </p>
      </div>
    </main>
  );
}

export function DisclosuresPage() {
  return (
    <main className="legal-page">
      <div className="container">
        <h1>Important disclosures</h1>
        <p>
          Equity2Bitcoin operates an education-first, non-custodial consulting model. Please read these disclosures
          before booking.
        </p>
        <h2>Not investment advice</h2>
        <p>
          Content is general education. It is not tailored investment advice under the Investment Advisers Act and is
          not a recommendation to buy, sell, or hold Bitcoin or any asset.
        </p>
        <h2>Not a lender or broker</h2>
        <p>
          We do not originate, broker, or underwrite loans. Any financing is between you and independently licensed
          lenders you choose to engage.
        </p>
        <h2>Risks</h2>
        <ul>
          <li>Bitcoin is highly volatile and can decline substantially in value.</li>
          <li>Home-equity borrowing increases leverage and may put your home at risk if obligations are not met.</li>
          <li>Interest rates, fees, and underwriting criteria change and may make extraction impractical.</li>
          <li>Self-custody errors can result in irreversible loss of Bitcoin.</li>
        </ul>
        <h2>Fee trigger</h2>
        <p>
          Unless a Milestone Agreement states otherwise, the success fee is tied to verified equity extraction
          milestones, not to Bitcoin market performance.
        </p>
      </div>
    </main>
  );
}
