import { Link } from "react-router-dom";
import { BRAND } from "../data/content";

export function SiteFooter() {
  return (
    <footer className="site-footer">
      <div className="container">
        <div className="footer-grid">
          <div>
            <div className="footer-brand">
              Equity<span>2</span>Bitcoin
            </div>
            <p>{BRAND.tagline}</p>
            <p style={{ marginTop: "0.85rem" }}>{BRAND.principle}</p>
          </div>
          <div className="footer-col">
            <h4>Explore</h4>
            <a href="/#how-it-works">How it works</a>
            <a href="/#equity-iq">Equity IQ</a>
            <a href="/#fees">Fee model</a>
            <Link to="/book">Book orientation</Link>
          </div>
          <div className="footer-col">
            <h4>Legal</h4>
            <Link to="/terms">Terms of Service</Link>
            <Link to="/privacy">Privacy Policy</Link>
            <Link to="/disclosures">Disclosures</Link>
          </div>
        </div>
        <div className="footer-legal">
          <p>
            © {new Date().getFullYear()} {BRAND.legalName}. Educational consulting only. Not a lender, broker,
            investment adviser, or custodian.
          </p>
          <p>
            Information on this site is for educational purposes and does not constitute financial, legal, tax, or
            investment advice. Bitcoin is volatile. Borrowing against a home carries risk. Past performance is not
            indicative of future results. You retain sole discretion over all financial decisions.
          </p>
        </div>
      </div>
    </footer>
  );
}
