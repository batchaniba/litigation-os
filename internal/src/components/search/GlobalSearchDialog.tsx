import { useEffect, useMemo, useRef, useState, type KeyboardEvent as ReactKeyboardEvent } from "react";
import { Link } from "react-router-dom";
import { cases } from "../../data/matters";
import documentIndex from "../../data/matters/document-index.json";
import { timeline } from "../../data/timeline";
import { useTheme } from "../../ThemeContext";
import type { DocumentIndexEntry } from "../../types/portfolio";
import { formatMatterPath } from "../../utils/formatters";
import { withBase } from "../../utils/paths";

type Result = { id: string; type: "Matter" | "Event" | "Document"; title: string; detail: string; matter?: number; href?: string };

export default function GlobalSearchDialog({ onClose }: { onClose: () => void }) {
  const [query, setQuery] = useState("");
  const [activeIndex, setActiveIndex] = useState(-1);
  const inputRef = useRef<HTMLInputElement>(null);
  const resultRefs = useRef<Array<HTMLAnchorElement | null>>([]);
  const theme = useTheme();
  const captionByMatter = useMemo(() => new Map(cases.map((matter) => [matter.number, matter.caption])), []);

  useEffect(() => {
    inputRef.current?.focus();
    const previousOverflow = document.body.style.overflow;
    document.body.style.overflow = "hidden";
    const close = (event: KeyboardEvent) => { if (event.key === "Escape") onClose(); };
    document.addEventListener("keydown", close);
    return () => {
      document.body.style.overflow = previousOverflow;
      document.removeEventListener("keydown", close);
    };
  }, [onClose]);

  const results = useMemo<Result[]>(() => {
    const needle = query.trim().toLowerCase();
    if (needle.length < 2) return [];
    const found: Result[] = [];
    for (const matter of cases) {
      const fields = [matter.caption, matter.case_no, matter.court, matter.defendants, matter.claims, ...(matter.causes ?? [])];
      if (fields.some((field) => field?.toLowerCase().includes(needle))) found.push({ id: `matter-${matter.number}`, type: "Matter", title: `Matter ${matter.number} · ${matter.caption}`, detail: `${matter.case_no} · ${matter.status}`, matter: matter.number });
    }
    for (const document of documentIndex as DocumentIndexEntry[]) {
      if (document.label.toLowerCase().includes(needle) || document.path.toLowerCase().includes(needle)) {
        found.push({
          id: `document-${document.matter}-${document.path}`,
          type: "Document",
          title: document.label,
          detail: `Matter ${document.matter} · ${captionByMatter.get(document.matter) ?? "Unknown matter"}`,
          href: withBase(document.path),
        });
      }
    }
    for (const [index, event] of timeline.entries()) {
      if (`${event.event} ${event.date} ${event.type} ${event.matters}`.toLowerCase().includes(needle)) found.push({ id: `event-${index}`, type: "Event", title: event.event, detail: `${event.date} · Matter ${event.matters}`, matter: Number(event.matters.split(",")[0]) || undefined });
    }
    return found.slice(0, 40);
  }, [captionByMatter, query]);

  useEffect(() => { setActiveIndex(results.length ? 0 : -1); }, [results.length, query]);
  const handleSearchKeys = (event: ReactKeyboardEvent<HTMLInputElement>) => {
    if (!results.length) return;
    if (event.key === "ArrowDown") { event.preventDefault(); setActiveIndex((index) => (index + 1) % results.length); }
    if (event.key === "ArrowUp") { event.preventDefault(); setActiveIndex((index) => (index - 1 + results.length) % results.length); }
    if (event.key === "Enter" && activeIndex >= 0) { event.preventDefault(); resultRefs.current[activeIndex]?.click(); }
  };

  return (
    <div className="search-backdrop" role="presentation" onMouseDown={(event) => { if (event.target === event.currentTarget) onClose(); }}>
      <section className="search-dialog" role="dialog" aria-modal="true" aria-labelledby="search-title" style={{ background: theme.cardBg, borderColor: theme.cardBorder }}>
        <h2 id="search-title" className="sr-only">Search litigation portfolio</h2>
        <div className="search-input-row" style={{ borderColor: theme.cardBorder }}><span aria-hidden="true">⌕</span><input ref={inputRef} value={query} onChange={(event) => setQuery(event.target.value)} onKeyDown={handleSearchKeys} placeholder="Search matters, parties, case numbers, causes, events, or documents…" aria-label="Search portfolio" aria-controls="portfolio-search-results" aria-activedescendant={activeIndex >= 0 ? `search-result-${activeIndex}` : undefined} style={{ color: theme.text }} /><button onClick={onClose} aria-label="Close search">Esc</button></div>
        <div id="portfolio-search-results" className="search-results" aria-live="polite">
          {query.trim().length < 2 && <p style={{ color: theme.subtleText }}>Enter at least two characters. Press ↑ or ↓ to review results and Enter to open.</p>}
          {query.trim().length >= 2 && results.length === 0 && <p style={{ color: theme.subtleText }}>No portfolio records match “{query}”.</p>}
          {results.map((result, index) => {
            const content = <><span className={`search-result-type type-${result.type.toLowerCase()}`}>{result.type}</span><span><strong style={{ color: theme.heading }}>{result.title}</strong><small style={{ color: theme.subtleText }}>{result.detail}</small></span></>;
            const shared = { id: `search-result-${index}`, ref: (node: HTMLAnchorElement | null) => { resultRefs.current[index] = node; }, className: `search-result${index === activeIndex ? " active" : ""}`, onMouseEnter: () => setActiveIndex(index), onClick: onClose };
            return result.href ? <a key={result.id} {...shared} href={result.href} target="_blank" rel="noreferrer">{content}</a> : <Link key={result.id} {...shared} to={result.matter ? formatMatterPath(result.matter) : "/timeline"}>{content}</Link>;
          })}
        </div>
      </section>
    </div>
  );
}
