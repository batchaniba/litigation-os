import { Link } from "react-router-dom";
import { SITE } from "../config/site";
import { BRAND } from "../data/content";

const base = import.meta.env.BASE_URL.replace(/\/$/, "");

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
            <a href={`${base}/#how-it-works`}>How it works</a>
            <Link to="/calculator">Calculator</Link>
            <Link to="/fit">Is this for you</Link>
            <Link to="/why-bitcoin">Why Bitcoin</Link>
            <Link to="/book">Book orientation</Link>
          </div>
          <div className="footer-col">
            <h4>Legal</h4>
            <Link to="/terms">Terms of Service</Link>
            <Link to="/privacy">Privacy Policy</Link>
            <Link to="/disclosures">Disclosures</Link>
            <a href={`mailto:${SITE.email}`}>{SITE.email}</a>
          </div>
        </div>
        <div className="footer-legal">
          <p>
            © {new Date().getFullYear()} {BRAND.legalName}. Educational consulting only. Not a lender, broker,
            investment adviser, or custodian.
          </p>
          <p>
            Information on this site is for educational purposes and does not constitute financial, legal, tax, or
            investment advice. Bitcoin is volatile. Borrowing against a home carries risk, including loss of the home.
            Past performance is not indicative of future results. You retain sole discretion over all financial
            decisions.
          </p>
        </div>
      </div>
    </footer>
  );
}
