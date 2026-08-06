import { useEffect, useMemo, useRef, useState, type KeyboardEvent as ReactKeyboardEvent } from "react";
import { Link } from "react-router-dom";
import { cases } from "../../data/matters";
import documentIndex from "../../data/matters/document-index.json";
import { timeline } from "../../data/timeline";
import { useDebounce } from "../../hooks/useDebounce";
import type { DocumentIndexEntry } from "../../types/portfolio";
import { formatMatterPath } from "../../utils/formatters";
import { withBase } from "../../utils/paths";

type Result = { id: string; type: "Matter" | "Event" | "Document"; title: string; detail: string; matter?: number; href?: string };

const GROUP_ORDER: Result["type"][] = ["Matter", "Document", "Event"];
const GROUP_LABELS: Record<Result["type"], string> = { Matter: "Matters", Document: "Documents", Event: "Events" };

export default function GlobalSearchDialog({ onClose }: { onClose: () => void }) {
  const [query, setQuery] = useState("");
  const debouncedQuery = useDebounce(query, 200);
  const [activeIndex, setActiveIndex] = useState(-1);
  const inputRef = useRef<HTMLInputElement>(null);
  const dialogRef = useRef<HTMLElement>(null);
  const resultRefs = useRef<Array<HTMLAnchorElement | null>>([]);
  const captionByMatter = useMemo(() => new Map(cases.map((matter) => [matter.number, matter.caption])), []);

  useEffect(() => {
    inputRef.current?.focus();
    const previousOverflow = document.body.style.overflow;
    document.body.style.overflow = "hidden";
    const close = (event: KeyboardEvent) => {
      if (event.key === "Escape") onClose();
      if (event.key !== "Tab") return;
      const focusable = Array.from(dialogRef.current?.querySelectorAll<HTMLElement>('a[href], button:not([disabled]), input:not([disabled]), [tabindex]:not([tabindex="-1"])') ?? []);
      if (!focusable.length) return;
      const first = focusable[0];
      const last = focusable[focusable.length - 1];
      if (event.shiftKey && document.activeElement === first) { event.preventDefault(); last.focus(); }
      if (!event.shiftKey && document.activeElement === last) { event.preventDefault(); first.focus(); }
    };
    document.addEventListener("keydown", close);
    return () => {
      document.body.style.overflow = previousOverflow;
      document.removeEventListener("keydown", close);
    };
  }, [onClose]);

  const results = useMemo<Result[]>(() => {
    const needle = debouncedQuery.trim().toLowerCase();
    if (needle.length < 2) return [];
    const found: Result[] = [];
    for (const matter of cases) {
      const fields = [matter.caption, matter.case_no, matter.court, matter.defendants, matter.claims, matter.status_label, ...(matter.causes ?? [])];
      if (fields.some((field) => field?.toLowerCase().includes(needle))) found.push({ id: `matter-${matter.number}`, type: "Matter", title: `Matter ${matter.number} · ${matter.caption}`, detail: `${matter.case_no} · ${matter.status_label}`, matter: matter.number });
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
  }, [captionByMatter, debouncedQuery]);

  const grouped = useMemo(() => {
    return GROUP_ORDER
      .map((type) => ({ type, label: GROUP_LABELS[type], items: results.filter((r) => r.type === type) }))
      .filter((group) => group.items.length);
  }, [results]);

  useEffect(() => { setActiveIndex(results.length ? 0 : -1); }, [results.length]);

  const handleSearchKeys = (event: ReactKeyboardEvent<HTMLInputElement>) => {
    if (!results.length) return;
    if (event.key === "ArrowDown") { event.preventDefault(); setActiveIndex((index) => (index + 1) % results.length); }
    if (event.key === "ArrowUp") { event.preventDefault(); setActiveIndex((index) => (index - 1 + results.length) % results.length); }
    if (event.key === "Enter" && activeIndex >= 0) { event.preventDefault(); resultRefs.current[activeIndex]?.click(); }
  };

  const isSearching = query.trim().length >= 2 && query !== debouncedQuery;

  return (
    <div className="search-backdrop" role="presentation" onMouseDown={(event) => { if (event.target === event.currentTarget) onClose(); }}>
      <section ref={dialogRef} className="search-dialog" role="dialog" aria-modal="true" aria-labelledby="search-title" style={{ background: "var(--card-bg)", borderColor: "var(--card-border)" }}>
        <h2 id="search-title" className="sr-only">Search litigation portfolio</h2>
        <div className="search-input-row" style={{ borderColor: "var(--card-border)" }}>
          <span aria-hidden="true">⌕</span>
          <input
            ref={inputRef}
            value={query}
            onChange={(event) => setQuery(event.target.value)}
            onKeyDown={handleSearchKeys}
            placeholder="Search matters, parties, case numbers, causes, events, or documents…"
            aria-label="Search portfolio"
            role="combobox"
            aria-autocomplete="list"
            aria-expanded={results.length > 0}
            aria-controls="portfolio-search-results"
            aria-activedescendant={activeIndex >= 0 ? `search-result-${activeIndex}` : undefined}
            style={{ color: "var(--text)" }}
          />
          <button onClick={onClose} aria-label="Close search">Esc</button>
        </div>
        <div id="portfolio-search-results" className="search-results" role="listbox" aria-label="Search results" aria-live="polite">
          {query.trim().length < 2 && <p style={{ color: "var(--subtle-text)" }}>Enter at least two characters. Press ↑ or ↓ to review results and Enter to open.</p>}
          {query.trim().length >= 2 && results.length === 0 && !isSearching && <p style={{ color: "var(--subtle-text)" }}>No portfolio records match “{query}”.</p>}
          {isSearching && <p className="search-debouncing" style={{ color: "var(--subtle-text)" }}>Searching…</p>}
          {grouped.map((group) => (
            <div key={group.type} className="search-result-group">
              <div className="search-result-group-header" role="presentation" style={{ color: "var(--muted-text)" }}>{group.label} <span>({group.items.length})</span></div>
              {group.items.map((result) => {
                const index = results.indexOf(result);
                const content = <><span className={`search-result-type type-${result.type.toLowerCase()}`}>{result.type}</span><span><strong style={{ color: "var(--heading)" }}>{result.title}</strong><small style={{ color: "var(--subtle-text)" }}>{result.detail}</small></span></>;
                const shared = { id: `search-result-${index}`, role: "option", "aria-selected": index === activeIndex, ref: (node: HTMLAnchorElement | null) => { resultRefs.current[index] = node; }, className: `search-result${index === activeIndex ? " active" : ""}`, onMouseEnter: () => setActiveIndex(index), onClick: onClose };
                return result.href ? <a key={result.id} {...shared} href={result.href} target="_blank" rel="noreferrer">{content}</a> : <Link key={result.id} {...shared} to={result.matter ? formatMatterPath(result.matter) : "/timeline"}>{content}</Link>;
              })}
            </div>
          ))}
        </div>
      </section>
    </div>
  );
}
