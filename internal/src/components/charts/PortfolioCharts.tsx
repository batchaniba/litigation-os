import type { KeyboardEvent } from "react";
import type { ChartTheme } from "../../types/portfolio";
import { GOLD } from "../../constants";

const MONO = "'Courier New', ui-monospace, monospace";
const SANS = "'DM Sans', sans-serif";
const GREEN = "#34D399";

type Datum = { label: string; value: number; color?: string; opacity?: number };
type RangeDatum = { label: string; low: number; high: number };

const activate = (event: KeyboardEvent, callback: () => void) => {
  if (event.key === "Enter" || event.key === " ") { event.preventDefault(); callback(); }
};

export function HorizontalBarChart({ data, theme, barH = 20, gap = 9, leftPad = 190, valueFmt = String, ariaLabel, onRowClick }: { data: Datum[]; theme: ChartTheme; barH?: number; gap?: number; leftPad?: number; valueFmt?: (value: number) => string; ariaLabel?: string; onRowClick?: (datum: Datum) => void }) {
  const width = 760, rightPad = 56, topPad = 4;
  const max = Math.max(...data.map((d) => d.value), 1);
  const plotW = width - leftPad - rightPad;
  const height = topPad * 2 + data.length * (barH + gap) - gap;
  return <svg viewBox={`0 0 ${width} ${height}`} width="100%" height={height} role="img" aria-label={ariaLabel}>{data.map((datum, index) => { const y = topPad + index * (barH + gap); const w = Math.max(2, (datum.value / max) * plotW); const click = onRowClick ? () => onRowClick(datum) : undefined; return <g key={datum.label} style={click ? { cursor: "pointer" } : undefined} role={click ? "button" : undefined} tabIndex={click ? 0 : undefined} onClick={click} onKeyDown={click ? (event) => activate(event, click) : undefined}><text x={leftPad - 10} y={y + barH * .68} textAnchor="end" fontFamily={SANS} fontSize={11.5} fill={theme.subtleText}>{datum.label}</text><rect x={leftPad} y={y} width={plotW} height={barH} fill={theme.barTrack} /><rect x={leftPad} y={y} width={w} height={barH} fill={datum.color ?? GREEN} opacity={.92} /><text x={leftPad + w + 8} y={y + barH * .68} fontFamily={MONO} fontSize={11.5} fontWeight={700} fill={theme.heading}>{valueFmt(datum.value)}</text></g>; })}</svg>;
}

export function VerticalBarChart({ data, theme, height = 160, todayIndex, onColumnClick, ariaLabel }: { data: Datum[]; theme: ChartTheme; height?: number; todayIndex?: number | null; onColumnClick?: (datum: Datum, index: number) => void; ariaLabel?: string }) {
  const width = 760, leftPad = 4, topPad = 20, bottomPad = 22, plotW = width - 8, plotH = height - topPad - bottomPad, gap = 8;
  const max = Math.max(...data.map((d) => d.value), 1), barW = (plotW - gap * (data.length - 1)) / data.length;
  return <svg viewBox={`0 0 ${width} ${height}`} width="100%" height={height} role="img" aria-label={ariaLabel}><line x1={leftPad} x2={leftPad + plotW} y1={topPad + plotH} y2={topPad + plotH} stroke={theme.cardBorder} />{data.map((datum, index) => { const x = leftPad + index * (barW + gap), h = Math.max((datum.value / max) * plotH, datum.value ? 4 : 1), y = topPad + plotH - h; const click = onColumnClick ? () => onColumnClick(datum, index) : undefined; return <g key={datum.label} style={click ? { cursor: "pointer" } : undefined} role={click ? "button" : undefined} tabIndex={click ? 0 : undefined} onClick={click} onKeyDown={click ? (event) => activate(event, click) : undefined}><text x={x + barW / 2} y={y - 6} textAnchor="middle" fontFamily={MONO} fontSize={10.5} fill={theme.subtleText}>{datum.value || ""}</text><rect x={x} y={y} width={barW} height={h} rx={2} fill={index === todayIndex ? GOLD : GREEN} opacity={datum.opacity ?? 1} /><text x={x + barW / 2} y={topPad + plotH + 16} textAnchor="middle" fontFamily={SANS} fontSize={10.5} fill={index === todayIndex ? GOLD : theme.subtleText}>{datum.label}</text></g>; })}</svg>;
}

export function RangeChart({ rows, theme, valueFmt = String }: { rows: RangeDatum[]; theme: ChartTheme; valueFmt?: (value: number) => string }) {
  const width = 760, leftPad = 190, rightPad = 90, rowH = 32, topPad = 6, max = Math.max(...rows.map((row) => row.high), 1), plotW = width - leftPad - rightPad, height = topPad * 2 + rows.length * rowH;
  return <svg viewBox={`0 0 ${width} ${height}`} width="100%" height={height} role="img" aria-label="Low-to-high ranges">{rows.map((row, index) => { const y = topPad + index * rowH + rowH / 2, x1 = leftPad + row.low / max * plotW, x2 = leftPad + row.high / max * plotW; return <g key={row.label}><text x={leftPad - 10} y={y + 4} textAnchor="end" fontFamily={SANS} fontSize={11.5} fill={theme.subtleText}>{row.label}</text><line x1={x1} x2={x2} y1={y} y2={y} stroke={theme.subtleText} strokeWidth={2} /><circle cx={x1} cy={y} r={5} fill={GOLD} /><circle cx={x2} cy={y} r={5} fill={GREEN} /><text x={x2 + 9} y={y + 4} fontFamily={MONO} fontSize={11} fontWeight={700} fill={theme.heading}>{valueFmt(row.low)}–{valueFmt(row.high)}</text></g>; })}</svg>;
}
