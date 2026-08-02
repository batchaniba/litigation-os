import { useEffect, useState } from "react";
import { Link, NavLink } from "react-router-dom";

const base = import.meta.env.BASE_URL.replace(/\/$/, "");

const links = [
  { href: `${base}/#how-it-works`, label: "How it works" },
  { to: "/calculator", label: "Calculator" },
  { to: "/fit", label: "Is this for you" },
  { href: `${base}/#faq`, label: "FAQ" },
];

export function SiteHeader() {
  const [scrolled, setScrolled] = useState(false);
  const [open, setOpen] = useState(false);

  useEffect(() => {
    const onScroll = () => setScrolled(window.scrollY > 24);
    onScroll();
    window.addEventListener("scroll", onScroll, { passive: true });
    return () => window.removeEventListener("scroll", onScroll);
  }, []);

  useEffect(() => {
    if (!open) return;
    const onKey = (e: KeyboardEvent) => {
      if (e.key === "Escape") setOpen(false);
    };
    window.addEventListener("keydown", onKey);
    return () => window.removeEventListener("keydown", onKey);
  }, [open]);

  return (
    <header className={`site-header${scrolled ? " is-scrolled" : ""}`}>
      <div className="container">
        <Link to="/" className="brand" onClick={() => setOpen(false)} aria-label="Equity2Bitcoin home">
          Equity<span>2</span>Bitcoin
        </Link>

        <button
          type="button"
          className="nav-toggle"
          aria-expanded={open}
          aria-controls="site-nav"
          aria-label={open ? "Close menu" : "Open menu"}
          onClick={() => setOpen((v) => !v)}
        >
          <span />
        </button>

        <nav id="site-nav" className={`nav-links${open ? " is-open" : ""}`} aria-label="Primary">
          {links.map((link) =>
            "to" in link && link.to ? (
              <NavLink key={link.to} to={link.to} onClick={() => setOpen(false)}>
                {link.label}
              </NavLink>
            ) : (
              <a key={link.href} href={link.href} onClick={() => setOpen(false)}>
                {link.label}
              </a>
            ),
          )}
          <NavLink to="/book" className="btn btn-primary nav-cta" onClick={() => setOpen(false)}>
            Book orientation
          </NavLink>
        </nav>
      </div>
    </header>
  );
}
