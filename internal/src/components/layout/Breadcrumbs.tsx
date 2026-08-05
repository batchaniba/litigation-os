import { Link, useLocation } from "react-router-dom";
import { NAV_ITEMS, ROUTES } from "../../routes";

const titleForSegment = (segment: string) => segment.replaceAll("-", " ").replace(/\b\w/g, (letter) => letter.toUpperCase());

export function Breadcrumbs() {
  const { pathname } = useLocation();
  if (pathname === ROUTES.dashboard) return null;
  const segments = pathname.split("/").filter(Boolean);
  const crumbs = segments.map((segment, index) => {
    const path = `/${segments.slice(0, index + 1).join("/")}`;
    const nav = NAV_ITEMS.find((item) => item.path === path);
    const label = segments[index - 1] === "matters" && /^\d+$/.test(segment) ? `Matter ${segment}` : nav?.label ?? titleForSegment(segment);
    return { path, label };
  });
  return (
    <nav className="breadcrumbs" aria-label="Breadcrumb" style={{ color: "var(--subtle-text)" }}>
      <Link to={ROUTES.dashboard}>Home</Link>
      {crumbs.map((crumb, index) => <span key={crumb.path}><span aria-hidden="true">/</span>{index === crumbs.length - 1 ? <span aria-current="page">{crumb.label}</span> : <Link to={crumb.path}>{crumb.label}</Link>}</span>)}
    </nav>
  );
}
