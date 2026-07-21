import { GOLD } from "../constants";
import { useTheme } from "../ThemeContext";
import { outcomes } from "../data/outcomes";

const RED    = "#dc2626";
const AMBER  = "#d97706";
const PURPLE = "#9333ea";
const GREEN  = "#16a34a";
const BLUE   = "#2563eb";
const TEAL   = "#0d9488";

const QUOTE_COLORS = {
  sharp:      { color: RED,    label: "Sharp"                },
  dismissive: { color: AMBER,  label: "Dismissive"           },
  backhanded: { color: PURPLE, label: "Backhanded"           },
  vindication:{ color: GREEN,  label: "Vindication"          },
  procedural: { color: BLUE,   label: "Procedural"           },
  meta:       { color: TEAL,   label: "Fourth Wall"          },
};

function QuoteCard({ item, theme }) {
  const { color, label } = QUOTE_COLORS[item.category] || QUOTE_COLORS.sharp;
  return (
    <div style={{
      background: theme.cardBg,
      borderRadius: 10,
      border: `1px solid ${theme.cardBorder}`,
      borderLeft: `4px solid ${color}`,
      padding: "24px 28px",
    }}>
      <div style={{ display: "flex", justifyContent: "space-between", alignItems: "flex-start", gap: 16, marginBottom: 14, flexWrap: "wrap" }}>
        <div style={{
          fontFamily: "'DM Sans', sans-serif", fontSize: 10, fontWeight: 700,
          letterSpacing: 2, textTransform: "uppercase",
          background: color + "18", color, border: `1px solid ${color}44`,
          borderRadius: 20, padding: "4px 14px", whiteSpace: "nowrap",
        }}>{label}</div>
        <div style={{
          fontFamily: "'DM Sans', sans-serif", fontSize: 12, color: theme.mutedText, textAlign: "right",
        }}>{item.date}{item.matter ? ` · Matter ${item.matter}` : ""}</div>
      </div>

      <p style={{
        fontFamily: "'Cormorant Garamond', Georgia, serif",
        fontSize: 22, fontStyle: "italic", fontWeight: 500,
        color: theme.heading, lineHeight: 1.45, margin: "0 0 16px",
      }}>
        <span style={{ color, fontSize: 30, lineHeight: 0, verticalAlign: "-8px", marginRight: 2 }}>&ldquo;</span>
        {item.quote}
        <span style={{ color, fontSize: 30, lineHeight: 0, verticalAlign: "-14px", marginLeft: 2 }}>&rdquo;</span>
      </p>

      <div style={{ marginBottom: 16 }}>
        <div style={{ fontFamily: "'DM Sans', sans-serif", fontSize: 13, fontWeight: 700, color: theme.secondaryText }}>
          — {item.speaker}
        </div>
        <div style={{ fontFamily: "'DM Sans', sans-serif", fontSize: 12, color: theme.subtleText, marginTop: 2 }}>
          {item.role}
        </div>
        <div style={{ fontFamily: "'DM Sans', sans-serif", fontSize: 11, color: theme.subtleText, marginTop: 4, opacity: 0.85 }}>
          {item.source}{item.case_no ? ` · ${item.case_no}` : ""}
        </div>
      </div>

      {item.note && (
        <div style={{
          background: theme.deepBg, borderRadius: 8, padding: "12px 16px",
          borderLeft: `2px solid ${color}66`,
        }}>
          <div style={{
            fontFamily: "'DM Sans', sans-serif", fontSize: 9, fontWeight: 700,
            letterSpacing: 2, textTransform: "uppercase", color, marginBottom: 6,
          }}>Why It Matters</div>
          <p style={{
            fontFamily: "'DM Sans', sans-serif", fontSize: 12.5, color: theme.secondaryText,
            lineHeight: 1.6, margin: 0,
          }}>{item.note}</p>
        </div>
      )}
    </div>
  );
}

export function NotableQuotesTab() {
  const theme = useTheme();
  const quotes = [...(outcomes.notable_quotes ?? [])].sort((a, b) => {
    if (a.category === "meta" && b.category !== "meta") return 1;
    if (b.category === "meta" && a.category !== "meta") return -1;
    return new Date(b.date) - new Date(a.date);
  });
  const counts = quotes.reduce((acc, q) => {
    acc[q.category] = (acc[q.category] || 0) + 1;
    return acc;
  }, {});

  return (
    <div>
      {/* Page heading */}
      <div style={{ marginBottom: 32 }}>
        <div style={{
          fontFamily: "'DM Sans', sans-serif", fontSize: 10, fontWeight: 700,
          letterSpacing: 4, textTransform: "uppercase", color: GOLD, marginBottom: 8,
        }}>Portfolio Record</div>
        <h2 style={{ fontSize: 28, fontWeight: 700, color: theme.heading, margin: "0 0 6px" }}>
          Notable Quotes
        </h2>
        <p style={{
          fontFamily: "'DM Sans', sans-serif", fontSize: 13,
          color: theme.mutedText, margin: 0, maxWidth: 640,
        }}>
          Direct language from judges, opposing counsel, and defendants across the record —
          dismissive characterizations, backhanded citations, and the rare vindicating line,
          each traced back to its filing.
        </p>
      </div>

      {/* Summary bar */}
      <div style={{ display: "flex", gap: 12, flexWrap: "wrap", marginBottom: 32 }}>
        {["sharp", "dismissive", "backhanded", "procedural", "vindication", "meta"].map(cat => {
          const { color, label } = QUOTE_COLORS[cat];
          return (
            <div key={cat} style={{
              background: theme.cardBg,
              border: `1px solid ${color}44`,
              borderRadius: 10, padding: "16px 24px",
              borderTop: `3px solid ${color}`,
            }}>
              <div style={{
                fontFamily: "'DM Sans', sans-serif", fontSize: 9, fontWeight: 700,
                letterSpacing: 3, textTransform: "uppercase", color, marginBottom: 6,
              }}>{label}</div>
              <div style={{
                fontFamily: "'Cormorant Garamond', Georgia, serif",
                fontSize: 32, fontWeight: 700, color: theme.heading, lineHeight: 1,
              }}>{counts[cat] || 0}</div>
            </div>
          );
        })}
      </div>

      {/* Quotes list */}
      <div style={{ display: "flex", flexDirection: "column", gap: 16, marginBottom: 32 }}>
        {quotes.map((item, i) => (
          <QuoteCard key={i} item={item} theme={theme} />
        ))}
      </div>

      {/* Context note */}
      <div style={{
        background: theme.cardBg,
        border: `1px solid ${GOLD}30`,
        borderRadius: 10, padding: "20px 24px",
        borderLeft: `3px solid ${GOLD}`,
      }}>
        <div style={{
          fontFamily: "'DM Sans', sans-serif", fontSize: 10, fontWeight: 700,
          letterSpacing: 2, textTransform: "uppercase", color: GOLD, marginBottom: 10,
        }}>On the record</div>
        <p style={{
          fontFamily: "'DM Sans', sans-serif", fontSize: 13, color: theme.secondaryText,
          lineHeight: 1.8, margin: "0 0 12px",
        }}>
          A pattern runs underneath most of these quotes: when the underlying facts are hard to
          answer, the response reaches for Plaintiff's character instead — "strategic," "under the
          guise," filed beneath a section literally titled "Generative AI." None of these lines argue
          the merits. Each substitutes a characterization of the litigant for an engagement with the
          record.
        </p>
        <p style={{
          fontFamily: "'DM Sans', sans-serif", fontSize: 13, color: theme.secondaryText,
          lineHeight: 1.8, margin: 0,
        }}>
          And in every instance where that characterization can be tested against something
          concrete — a coordinate court ruling on the identical incident, an institution's own
          inability to explain its conduct, a plain timestamp-to-timestamp timeline — it doesn't
          hold. Krishnan's order and CSK's Candelaria F&R reached opposite conclusions on the
          same November 2024 CHP allegations fourteen days apart. CDCR's own May 29, 2026
          order admits it "refuses to provide any explanation" for the conduct its counsel called
          administratively unchallengeable. The Van Dine citation meant to paint Plaintiff as
          litigious is now the portfolio's Westlaw accolade. Read together, the quotes say less
          about the litigant they describe than about how often a rapid, thorough, well-supported
          filing gets answered with suspicion rather than a rebuttal on the merits.
        </p>
      </div>
    </div>
  );
}
