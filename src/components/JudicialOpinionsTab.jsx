import { useState } from "react";
import { GOLD } from "../constants";
import { useTheme } from "../ThemeContext";
import { outcomes } from "../data/outcomes";

const GREEN  = "#16a34a";
const RED    = "#dc2626";
const AMBER  = "#d97706";
const SLATE  = "#64748b";

const OPINION_COLORS = {
  favorable:  { color: GREEN,  label: "Favorable"   },
  adverse:    { color: RED,    label: "Adverse"      },
  procedural: { color: SLATE,  label: "Procedural"   },
  mixed:      { color: AMBER,  label: "Mixed"        },
};

const Label = ({ children }) => (
  <div style={{
    fontFamily: "'DM Sans', sans-serif", fontSize: 10, fontWeight: 700,
    letterSpacing: 2, textTransform: "uppercase", color: GOLD, marginBottom: 6,
  }}>{children}</div>
);

const bodyText = (theme) => ({
  fontFamily: "'DM Sans', sans-serif", fontSize: 13,
  color: theme.secondaryText, lineHeight: 1.6, margin: "0 0 14px",
});

function OpinionCard({ item, theme }) {
  const [open, setOpen] = useState(false);
  const { color, label } = OPINION_COLORS[item.outcome] || OPINION_COLORS.procedural;
  return (
    <div style={{
      background: theme.cardBg,
      borderRadius: 10,
      border: `1px solid ${open ? color + "60" : theme.cardBorder}`,
      overflow: "hidden",
      transition: "border-color 0.2s",
    }}>
      <button
        onClick={() => setOpen(v => !v)}
        aria-expanded={open}
        style={{
          width: "100%", padding: "18px 24px", cursor: "pointer",
          display: "flex", alignItems: "center", gap: 18, flexWrap: "wrap",
          background: "transparent", border: "none", textAlign: "left",
          color: "inherit", font: "inherit", lineHeight: "inherit",
        }}
      >
        <div style={{
          width: 40, height: 40, borderRadius: 8,
          background: color + "18", border: `1px solid ${color}44`,
          display: "flex", alignItems: "center", justifyContent: "center",
          fontFamily: "'DM Sans', sans-serif", fontSize: 14, fontWeight: 700,
          color, flexShrink: 0,
        }}>{item.matter}</div>

        <div style={{ flex: 1, minWidth: 200 }}>
          <div style={{ fontSize: 16, fontWeight: 700, color: theme.heading, marginBottom: 3 }}>
            {item.caption}
          </div>
          <div style={{ fontFamily: "'DM Sans', sans-serif", fontSize: 12, color: theme.subtleText }}>
            {item.case_no} · {item.court}{item.judge ? ` · ${item.judge}` : ""}
          </div>
        </div>

        <div style={{
          fontFamily: "'DM Sans', sans-serif", fontSize: 12, color: theme.mutedText,
          whiteSpace: "nowrap",
        }}>{item.date}</div>

        <div style={{
          fontFamily: "'DM Sans', sans-serif", fontSize: 10, fontWeight: 700,
          letterSpacing: 2, textTransform: "uppercase",
          background: color + "18", color, border: `1px solid ${color}44`,
          borderRadius: 20, padding: "4px 14px", whiteSpace: "nowrap",
        }}>{label}</div>

        <div aria-hidden style={{
          color: theme.subtleText, fontSize: 18,
          transition: "transform 0.3s", transform: open ? "rotate(180deg)" : "rotate(0)",
        }}>▾</div>
      </button>

      {open && (
        <div style={{ padding: "0 24px 24px", borderTop: `1px solid ${theme.cardBorder}` }}>
          <div style={{ paddingTop: 18, marginBottom: 16 }}>
            <Label>Ruling</Label>
            <p style={{
              fontFamily: "'DM Sans', sans-serif", fontSize: 13,
              color: theme.heading, lineHeight: 1.6, margin: "0 0 14px",
              fontStyle: "italic",
            }}>{item.title}</p>
            <Label>Key Holding</Label>
            <p style={{ ...bodyText(theme), lineHeight: 1.7 }}>{item.holding}</p>
            <Label>Portfolio Significance</Label>
            <p style={{ ...bodyText(theme), lineHeight: 1.7 }}>{item.significance}</p>
          </div>
          {item.document_path && (
            <a
              href={item.document_path}
              target="_blank"
              rel="noopener noreferrer"
              onClick={e => e.stopPropagation()}
              style={{
                display: "inline-flex", alignItems: "center", gap: 8,
                fontFamily: "'DM Sans', sans-serif", fontSize: 12, fontWeight: 600,
                color, textDecoration: "none",
                background: color + "12", border: `1px solid ${color}44`,
                borderRadius: 6, padding: "6px 14px",
              }}
            >
              <span style={{ fontSize: 14 }}>📄</span> View {item.type === "merits" ? "Opinion" : "Minute Order"}
            </a>
          )}
        </div>
      )}
    </div>
  );
}

export function JudicialOpinionsTab() {
  const theme = useTheme();
  const opinions = outcomes.judicial_opinions ?? [];
  const adverseCount = opinions.filter(o => o.outcome === "adverse").length;
  const favorableCount = opinions.filter(o => o.outcome === "favorable").length;

  return (
    <div>
      {/* Page heading */}
      <div style={{ marginBottom: 32 }}>
        <div style={{
          fontFamily: "'DM Sans', sans-serif", fontSize: 10, fontWeight: 700,
          letterSpacing: 4, textTransform: "uppercase", color: GOLD, marginBottom: 8,
        }}>Portfolio Record</div>
        <h2 style={{ fontSize: 28, fontWeight: 700, color: theme.heading, margin: "0 0 6px" }}>
          Judicial Opinions & Rulings
        </h2>
        <p style={{
          fontFamily: "'DM Sans', sans-serif", fontSize: 13,
          color: theme.mutedText, margin: 0, maxWidth: 620,
        }}>
          Court orders, findings and recommendations, and substantive rulings issued across the portfolio.
          Each entry includes the holding, procedural posture, and its significance to ongoing matters.
        </p>
      </div>

      {/* Summary bar */}
      <div style={{
        display: "flex", gap: 12, flexWrap: "wrap", marginBottom: 32,
      }}>
        {[
          { label: "Total Rulings", count: opinions.length, color: SLATE },
          { label: "Adverse",       count: adverseCount,    color: RED   },
          { label: "Favorable",     count: favorableCount,  color: GREEN },
        ].map(({ label, count, color }) => (
          <div key={label} style={{
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
            }}>{count}</div>
          </div>
        ))}
      </div>

      {/* Opinions list */}
      <div style={{ display: "flex", flexDirection: "column", gap: 12, marginBottom: 32 }}>
        {opinions.map((item, i) => (
          <OpinionCard key={i} item={item} theme={theme} />
        ))}
      </div>

      {/* Context note */}
      <div style={{
        background: theme.cardBg,
        border: `1px solid ${GOLD}30`,
        borderRadius: 10, padding: "20px 24px",
        borderLeft: `3px solid ${GOLD}`,
        marginBottom: 16,
      }}>
        <div style={{
          fontFamily: "'DM Sans', sans-serif", fontSize: 10, fontWeight: 700,
          letterSpacing: 2, textTransform: "uppercase", color: GOLD, marginBottom: 10,
        }}>On the record</div>
        <p style={{
          fontFamily: "'DM Sans', sans-serif", fontSize: 13, color: theme.secondaryText,
          lineHeight: 1.8, margin: 0,
        }}>
          Adverse rulings at the pleading stage are not merits losses — they reflect the procedural
          limitations of Rule 12(b)(6) motions and magistrate F&Rs that are not yet final orders.
          No ruling to date has resolved a matter on a fully developed factual record.
          The dashcam footage, blood-draw warrant, and structural-bias evidence that drive the
          underlying claims remain unreached by any court.
        </p>
      </div>

      {/* CSK Pattern note */}
      <div style={{
        background: theme.cardBg,
        border: `1px solid ${RED}30`,
        borderRadius: 10, padding: "20px 24px",
        borderLeft: `3px solid ${RED}`,
      }}>
        <div style={{
          fontFamily: "'DM Sans', sans-serif", fontSize: 10, fontWeight: 700,
          letterSpacing: 2, textTransform: "uppercase", color: RED, marginBottom: 10,
        }}>Judicial Assignment Pattern — Magistrate Judge Chi Soo Kim (CSK)</div>
        <p style={{
          fontFamily: "'DM Sans', sans-serif", fontSize: 13, color: theme.secondaryText,
          lineHeight: 1.8, margin: "0 0 12px",
        }}>
          Magistrate Judge Chi Soo Kim has been assigned to three separate E.D. Cal. matters —
          Matter 1 (2:25-cv-01460-DC-CSK), Matter 21 (2:26-cv-00191-DJC-CSK), and Matter 7
          (2:26-cv-00983-DC-CSK) — and has ruled adversely in all three, in that order.
        </p>
        <p style={{
          fontFamily: "'DM Sans', sans-serif", fontSize: 13, color: theme.secondaryText,
          lineHeight: 1.8, margin: 0,
        }}>
          The pattern is compounding: the Matter 7 F&R (June 15, 2026) explicitly cross-referenced
          the Matter 1 F&R (April 20, 2026), citing it as evidence that plaintiff's complaints are
          "pending dismissal for failure to state a claim." Each adverse ruling by the same judicial
          officer is being recycled as ammunition in the next matter — a feedback loop in which the
          outcome of one case prejudices the next before any merits hearing. This pattern warrants
          monitoring for recusal grounds under 28 U.S.C. § 455 on future E.D. Cal. filings.
        </p>
      </div>
    </div>
  );
}
