# Supercycle Instructions: Interactive Litigation Portfolio

A comprehensive guide for building single-page data-heavy dashboards using the Supercycle iterative development methodology. This document enables Claude to rebuild or extend this project in different repositories.

---

## Table of Contents

1. [Project Overview](#project-overview)
2. [Architecture & Tech Stack](#architecture--tech-stack)
3. [Data Organization](#data-organization)
4. [Component Structure](#component-structure)
5. [Development Workflow](#development-workflow)
6. [Building & Deployment](#building--deployment)
7. [Key Patterns & Best Practices](#key-patterns--best-practices)
8. [Customization Guide](#customization-guide)

---

## Project Overview

**Type:** Single-page litigation portfolio dashboard  
**Purpose:** Centralized view of multi-jurisdictional civil litigation matters, timelines, damages exposure, and legal theories  
**Users:** Pro se litigants, legal professionals, case management teams  
**Scale:** 19–21 active cases across 5 jurisdictions, ~1000+ events, multi-tab UI  

**Key Features:**
- Multi-tab navigation (Dashboard, Matters, Timeline, Damages, Theories)
- Dark/light theme toggle
- Real-time deadline countdown clock
- Case filtering by cluster and type
- Search functionality
- Responsive design (mobile to desktop)
- Inline styling (zero external CSS dependencies)
- Confidential document watermark

---

## Architecture & Tech Stack

### Frontend Stack
- **Framework:** React 18+ (Hooks-based, functional components)
- **Build Tool:** Vite 5+ (ESM-first, fast HMR)
- **Styling:** Inline styles (React `style` objects)
- **Fonts:** 
  - Cormorant Garamond (headings, serif)
  - DM Sans (UI, sans-serif)
- **Date Handling:** Native JavaScript Date API (PDT-aware utility functions)

### Deployment
- **Hosting:** GitHub Pages (static site)
- **CI/CD:** GitHub Actions workflow
- **Build Output:** `dist/` folder

### Dependencies
```json
{
  "dependencies": {
    "react": "^18.3.1",
    "react-dom": "^18.3.1"
  },
  "devDependencies": {
    "@vitejs/plugin-react": "^5.2.0",
    "vite": "^6.4.1"
  }
}
```

**Why minimal dependencies?**
- Data is static (no runtime API calls)
- Inline styles eliminate CSS bundle weight
- React Hooks replace external state management
- Date utilities are lightweight and timezone-aware

---

## Data Organization

### Data Structure (Modular)

All data lives in `/src/data/` as ESM modules imported into a central `index.js`:

```
internal/src/data/
├── index.js          (consolidates all imports into PORTFOLIO object)
├── matters/          (one NN.json per matter + index.ts loader)
├── timeline.js       (chronological events, deadlines, court orders)
├── damages.js        (damages table: conservative/moderate/aggressive scenarios)
└── theories.js       (legal theories, causes of action)
```

### PORTFOLIO Object Structure

```javascript
export const PORTFOLIO = {
  plaintiff: "Name",
  representation: "Pro Se / In Propria Persona",
  contact: { address: "...", ... },
  prepared_date: "May 6, 2026",
  jurisdictions: ["USDC E.D. Cal.", ...],
  cases: [...],              // matters/*.json via matters/index.ts
  timeline: [...],           // timeline.js
  theories: [...],           // theories.js
  damages_table: {...},      // damages.js
};
```

### Matter JSON Schema (`matters/NN.json`)

```javascript
{
  number: 1,                 // must match filename 01.json
  caption: "Newanforbi v. CHP et al.",
  case_no: "2:25-cv-01460-DC-CSK",
  court: "USDC E.D. Cal.",
  type: "Federal",           // "Federal" | "State"
  cluster: 1,                // numeric cluster
  status: "MTD briefed; ruling pending",
  defendants: "...",         // prose string today
  // ... additional metadata
}
```

### timeline.js Schema

```javascript
export const timeline = [
  {
    id: "t-01",
    date: "May 29, 2026",     // "MMM. DD, YYYY" format
    event: "CHP MTD hearing",
    matter: 1,                // cross-reference to case ID
    type: "hearing",          // "hearing", "deadline", "order", "filing", etc.
    upcoming: true,           // used for filtering
    // Optional fields:
    // caption: "...",        // full case caption (if different from matter default)
    // description: "...",    // extended narrative
  },
  // ... more events
];
```

### damages.js Schema

```javascript
export const damages_table = {
  Lost_Wages_Economic_Harm: {
    category: "Lost Wages / Economic Harm",
    conservative: 375000,
    moderate: 800000,
    aggressive: 1400000,
  },
  // ... more damage categories
  Total: {
    category: "Total",
    conservative: 1170000,
    moderate: 2785000,
    aggressive: 5700000,
  },
};
```

### theories.js Schema

```javascript
export const theories = [
  {
    id: "theory-01",
    title: "First Amendment Retaliation as the Catalyst",
    summary: "Explicit retaliation by Agent Derrick...",
    cases: [3, 5, 11],  // matter IDs that support this theory
    legalBases: ["42 U.S.C. § 1983", "First Amendment"],
    // Optional:
    // description: "...",
    // supportingCases: [...],
  },
  // ... more theories
];
```

### Key Design Principles
- **Immutable data:** All data files export `const` (never mutated)
- **Cross-references:** Use numeric IDs to link cases ↔ timeline ↔ theories
- **Timezone awareness:** All dates in "MMM. DD, YYYY" format; parsed as PDT (UTC-7)
- **Single source of truth:** `PORTFOLIO` object aggregates all data; components import `PORTFOLIO`

---

## Component Structure

### Component Tree

```
App.jsx (root, state management)
├── Header
│   ├── Title / Plaintiff name
│   ├── Tab buttons
│   └── Dark/light mode toggle
├── Deadline Clock Banner
│   ├── Live countdown (Days:Hrs:Min:Sec)
│   ├── Next event label
│   └── Show/Hide button
├── Tab Content (conditional rendering)
│   ├── DashboardTab
│   │   ├── Quick stats (active cases, jurisdictions, aggregate exposure)
│   │   ├── Cluster cards (clickable to filter by cluster)
│   │   └── Upcoming events preview
│   ├── MattersTab
│   │   ├── Filter controls (cluster, type, search)
│   │   ├── Matter grid/list
│   │   └── Case detail cards
│   ├── TimelineTab
│   │   ├── Chronological event list
│   │   ├── Show past events toggle
│   │   └── Event detail rows
│   ├── DamagesTab
│   │   ├── Scenario selector (conservative/moderate/aggressive)
│   │   ├── Damages breakdown table
│   │   └── Total exposure calculation
│   └── TheoriesTab
│       ├── Legal theory cards
│       ├── Supporting matter references
│       └── Legal basis citations
└── Footer
    └── Confidentiality notice
```

### Component Files

| File | Responsibility | State |
|------|---|---|
| `App.jsx` | Root, tab navigation, deadline clock, filters | `activeTab`, `darkMode`, `damagesView`, `showPastEvents`, `showClock`, filter state |
| `DashboardTab.jsx` | Overview, cluster cards, quick stats | None (stateless) |
| `MattersTab.jsx` | Case list, filtering, search | Receives filter state from parent |
| `TimelineTab.jsx` | Chronological events, show/hide past | Receives `showPastEvents` from parent |
| `DamagesTab.jsx` | Damages table, scenario selector | Receives `damagesView` from parent |
| `TheoriesTab.jsx` | Legal theories, supporting cases | None (stateless) |
| `Badges.jsx` | UI component: status/type badges | None (stateless) |
| `ThemeContext.jsx` | Theming system (dark/light colors) | Context provider |

### Key Hooks

**`useDeadlineClock.js`**
- **Purpose:** Real-time countdown to next deadline
- **Input:** `upcomingEvents` array
- **Output:** Object with `{ days, hours, mins, secs, label, urgent, frozen }`
- **Behavior:** Updates every 100ms; resets when deadline passes
- **Note:** Used in App.jsx header banner

**`useCaseFilters.js`**
- **Purpose:** Filter/search cases by cluster, type, query
- **Input:** None (uses `PORTFOLIO` directly)
- **Output:** `{ clusterFilter, setClusterFilter, typeFilter, setTypeFilter, searchQuery, setSearchQuery, filteredCases }`
- **Behavior:** Returns filtered case array based on current filters

### ThemeContext

Two themes defined:
```javascript
THEMES = {
  dark: { bg, text, headerBg, headerText, tabActive, tabInactive, ... },
  light: { bg, text, headerBg, headerText, tabActive, tabInactive, ... }
}
```

All components wrap in `<ThemeContext.Provider>` at App root; child components read theme via `useContext(ThemeContext)`.

### Styling Approach

**All styles are inline React objects.** No CSS files or external libraries.

Rationale:
- Co-location of style with JSX
- No CSS namespace conflicts
- Zero runtime CSS parsing
- Fonts pre-loaded in `index.html`
- Responsive design via media queries (inline)

**Color Palette:**
- `GOLD`: Theme accent (#D4AF37)
- `BODY_GRAY`: Secondary text (#94A3B8)
- Dark mode: dark grays/blacks (#0F172A, #1E293B)
- Light mode: light grays/whites (#F8FAFC, #FFFFFF)

---

## Development Workflow

### Setup

```bash
# Clone the repository
git clone https://github.com/newanforbi/interactive-litigation-portfolio.git
cd interactive-litigation-portfolio

# Install dependencies
npm install

# Start development server (HMR enabled)
npm run dev

# Open in browser
# http://localhost:5173/interactive-litigation-portfolio/
```

### Local Development Loop (Supercycle Pattern)

The Supercycle methodology emphasizes:

1. **Read → Understand** (examine data structure, current implementation)
2. **Identify → Isolate** (pinpoint the file(s) needing change)
3. **Edit → Test** (make change, verify in browser)
4. **Commit → Push** (save work with clear message)

**Typical workflow:**

```bash
# 1. Start dev server
npm run dev

# 2. Open http://localhost:5173/interactive-litigation-portfolio/

# 3. Make changes to internal/src/ files
#    - Edit data: internal/src/data/matters.js, internal/src/data/timeline.js, etc.
#    - Edit components: internal/src/components/*.jsx
#    - Update utils: internal/src/utils/*.js

# 4. Watch browser for live updates (Vite HMR)

# 5. When satisfied:
git add internal/src/
git commit -m "Update: [what changed]"
git push -u origin [branch-name]
```

### Updating Case Data

**Adding a new case:**
1. Run `npm run scaffold:matter -- <N> "Caption"` — creates `matters/NN.json` + `documents/matter-NN/`
2. Fill required fields in the JSON (`number`, `cluster` as a number, status prose, etc.)
3. Add companion rows in `timeline.js`, `damages.js`, and `lawyerFees.js`
4. Drop PDFs under `internal/public/documents/matter-NN/` and list them in `documents[]`
5. Run `npm run sync:summaries && npm run validate` (also runs in CI and the GitHub Pages deploy workflow). Full prose stays in `NN.json` and is lazy-loaded on expand/detail; list views use `summaries.json`.

**Adding a timeline event:**
1. Add entry to `internal/src/data/timeline.js`
2. Use `date: "MMM. DD, YYYY"` format (e.g., "May 29, 2026")
3. Set `matters` to a comma-separated matter-number string (e.g., `"27"` or `"25,26"`)
4. Set `upcoming: true` if future; omit/false if past
5. Deadline clock auto-updates on next event

**Updating damages:**
1. Edit `internal/src/data/damages.js`
2. Modify conservative/moderate/aggressive values
3. Component auto-recalculates totals on selection change

**Adding a legal theory:**
1. Add entry to `internal/src/data/theories.js`
2. Include array of `cases` (numeric IDs) that support theory
3. Reference will appear in TheoriesTab and linked to matters

### Testing Before Commit

**Manual Testing Checklist:**
- [ ] All tabs load without errors (Console clean?)
- [ ] Dark/light mode toggles correctly
- [ ] Filters work (cluster, type, search)
- [ ] Deadline clock counts down and shows correct next event
- [ ] All case details visible without horizontal scroll
- [ ] Timeline events display in chronological order
- [ ] Damages totals calculate correctly for all scenarios
- [ ] Mobile responsive (DevTools device emulation)

**Browser DevTools:**
- Console: Should have zero errors
- Network: Images/fonts load; no 404s
- Performance: First paint < 1s (static site)

---

## Building & Deployment

### Build for Production

```bash
npm run build       # outputs to dist/
npm run preview     # test production build locally
```

**Build output:**
- Single-page app (all assets in `dist/`)
- Entry point: `dist/index.html`
- JavaScript: `dist/assets/index-[hash].js`
- Fonts: Pre-loaded via `<link>` in HTML

### GitHub Pages Deployment

**Repository Setup:**
- Repo: `newanforbi/interactive-litigation-portfolio`
- Branch: `main` (default)
- GitHub Pages setting: Deploy from `main` / `docs` (if using `docs/` folder) or `gh-pages` branch

**Vite Configuration (`vite.config.js`):**
```javascript
import { defineConfig } from 'vite'
import react from '@vitejs/plugin-react'

export default defineConfig({
  plugins: [react()],
  base: '/interactive-litigation-portfolio/',  // ← Critical for GitHub Pages subpath
})
```

**CI/CD (GitHub Actions):**
- Typically runs on `push` to `main` or `pull_request`
- Builds with `npm run build`
- Deploys `dist/` to GitHub Pages

**Manual Deployment:**
1. Ensure local build succeeds: `npm run build`
2. Commit changes to `main` (or merge PR)
3. GitHub Actions auto-deploys (check Actions tab)
4. Live at: https://newanforbi.github.io/interactive-litigation-portfolio/

---

## Key Patterns & Best Practices

### 1. Data-Driven UI

All component content derives from `PORTFOLIO` object. To update the dashboard:
- **Do:** Edit files in `internal/src/data/`
- **Don't:** Hardcode text in components

```javascript
// ✓ Good: Components read from PORTFOLIO
<h1>{PORTFOLIO.plaintiff}</h1>

// ✗ Avoid: Hardcoded values
<h1>Brendan Ngehsi Newanforbi</h1>
```

### 2. Cross-References via Numeric IDs

Cases, timeline events, and theories link via numeric `id` and `matter` fields:

```javascript
// In timeline.js
{ id: "t-42", date: "May 15, 2026", matter: 3, ... }

// In component:
const relatedCase = PORTFOLIO.cases.find(c => c.id === event.matter);
```

**Benefit:** Easy refactoring (rename cases without breaking links; just update `id`).

### 3. PDT Timezone Awareness

All dates stored as strings ("May 15, 2026"); parsed to UTC using PDT offset:

```javascript
// internal/src/utils/dateUtils.js
export const parseEventDatePDT = (dateStr) => {
  // Parses as midnight PDT (UTC-7 in summer)
  const temp = new Date(dateStr.replace(/^~/, "").replace(/\./g, ""));
  return new Date(Date.UTC(temp.getFullYear(), temp.getMonth(), temp.getDate(), 7, 0, 0));
};
```

**Why:** Ensures deadline clock is accurate regardless of user's local timezone.

### 4. Conditional Rendering via State

Components conditionally render based on state. Example (DashboardTab):

```javascript
{activeTab === "Dashboard" && <DashboardTab />}
{activeTab === "Matters" && <MattersTab />}
// Only one tab renders at a time
```

**Performance:** React doesn't unmount unused tabs; just hides them. This is intentional (state preservation).

### 5. Stateless, Reusable Components

Components like `DashboardTab`, `TheoriesTab`, `Badges` are **stateless**—they receive all data and callbacks as props.

```javascript
// Stateless component pattern
export function Badges({ type, status }) {
  return (
    <span style={{ ... }}>
      {type} {status}
    </span>
  );
}
```

**Benefit:** Easy to test, compose, and refactor.

### 6. Inline Styles with Theme Context

All colors defined in `constants.js` and applied via inline style objects:

```javascript
const GOLD = "#D4AF37";
const BODY_GRAY = "#94A3B8";

<div style={{ color: GOLD, fontSize: 14 }}>Important text</div>
```

**Theme switching:** Context value changes → all components re-render with new colors.

### 7. Debouncing and Performance

For features like deadline countdown (updates every 100ms), use `useEffect` with cleanup:

```javascript
useEffect(() => {
  const interval = setInterval(() => { /* update */ }, 100);
  return () => clearInterval(interval);  // cleanup on unmount
}, [deps]);
```

**Avoids:** Memory leaks, stale closures.

### 8. Accessibility

- **ARIA labels** on buttons: `aria-label="Switch to light mode"`
- **ARIA live regions** for dynamic updates: `aria-live="polite"` on deadline clock
- **Semantic HTML:** Tab buttons are `<button>`, not `<div>`
- **Tab navigation:** Works with keyboard (not just mouse)

---

## Customization Guide

### Common Tasks

#### 1. Add a New Matter

**File:** `internal/src/data/matters.js`

```javascript
export const cases = [
  // ... existing cases ...
  {
    id: 22,  // next available ID
    caption: "Newanforbi v. State",
    caseNo: "2026-CV-09999",
    court: "USDC E.D. Cal.",
    type: "Federal",
    cluster: "Cluster 2",
    status: "Filed",
    plaintiff: "Brendan Ngehsi Newanforbi",
    defendants: ["State Attorney General"],
    causes: ["First Amendment", "Due Process"],
  },
];
```

#### 2. Add a Timeline Event

**File:** `internal/src/data/timeline.js`

```javascript
{
  id: "t-101",
  date: "Jun. 15, 2026",
  event: "Motion to dismiss hearing",
  matter: 22,  // cross-ref to new case
  type: "hearing",
  upcoming: true,
  description: "Oral arguments on motion to dismiss",
}
```

#### 3. Change Theme Colors

**File:** `internal/src/constants.js`

```javascript
// Edit these:
export const GOLD = "#D4AF37";           // accent color
export const BODY_GRAY = "#94A3B8";      // secondary text

// And in internal/src/ThemeContext.jsx:
export const THEMES = {
  dark: {
    bg: "#0F172A",           // background
    text: "#F1F5F9",         // foreground text
    headerBg: "#1E293B",     // header background
    // ... more colors
  },
  light: {
    bg: "#FFFFFF",
    text: "#0F172A",
    // ... etc
  },
};
```

#### 4. Customize Fonts

**File:** `index.html`

```html
<link href="https://fonts.googleapis.com/css2?family=[FONT_NAME]&display=swap" rel="stylesheet">
```

Then update references in components:

```javascript
<div style={{ fontFamily: "'[FONT_NAME]', serif" }}>
```

#### 5. Add a New Tab

1. **Create component:** `internal/src/components/NewTab.jsx`
   ```javascript
   export function NewTabComponent() {
     return <div>{/* content */}</div>;
   }
   ```

2. **Add to tab list:** `internal/src/App.jsx`
   ```javascript
   const tabs = ["Dashboard", "Matters", "Timeline", "Damages", "Theories", "NewTab"];
   ```

3. **Render in content area:**
   ```javascript
   {activeTab === "NewTab" && <NewTabComponent />}
   ```

#### 6. Rename the Plaintiff

**File:** `internal/src/data/index.js`

```javascript
export const PORTFOLIO = {
  plaintiff: "New Plaintiff Name",  // ← change here
  // ... rest
};
```

#### 7. Update Prepared Date

**File:** `internal/src/data/index.js`

```javascript
prepared_date: "Jun. 30, 2026",
```

---

## Debugging & Troubleshooting

### Issue: Deadline clock shows incorrect date

**Solution:** Check date format in timeline.js. Must be "MMM. DD, YYYY" with period after month abbreviation.

```javascript
// ✓ Correct
"May 29, 2026"
"Jun. 15, 2026"

// ✗ Wrong
"May-29-2026"
"June 15, 2026"
```

### Issue: Timeline events not showing

**Check:**
1. Is `upcoming: true`? (Hidden by default if false)
2. Does `matter` ID exist in cases?
3. Check browser console for parsing errors

### Issue: Filter not working

**Check:**
1. In `useCaseFilters.js`, verify filter logic matches your data structure
2. Ensure `cluster` values in matters.js match filter options
3. Clear browser cache (Cmd+Shift+R)

### Issue: Theme colors not updating

**Check:**
1. Is component reading from `ThemeContext` correctly?
2. Verify `useContext(ThemeContext)` import
3. Restart dev server if theme colors edited in ThemeContext.jsx

### Issue: Build succeeds locally but fails on GitHub

**Common causes:**
1. **Base path mismatch:** Check `vite.config.js` has `base: '/interactive-litigation-portfolio/'`
2. **Missing env vars:** Some builds inject secrets; check `.github/workflows/`
3. **Node version:** Ensure GitHub Actions uses compatible Node version

---

## Supercycle Development Principles

The Supercycle methodology emphasizes:

1. **Isolation:** Each change targets a single file or logical unit
2. **Verification:** Test changes in browser before committing
3. **Clarity:** Commit messages clearly state what changed and why
4. **Iteration:** Small, frequent commits enable easy reversal or branching
5. **Documentation:** Keep this guide updated as patterns evolve

**Workflow:**
```
Read code → Find module → Edit → Test → Commit → Push → Repeat
```

---

## File Reference

### Key Files to Know

| Path | Purpose | Edit Frequency |
|------|---------|---|
| `internal/src/App.jsx` | Root component, layout, state | Low (architecture is stable) |
| `internal/src/data/matters/*.json` | Case metadata (one file per matter) | High (new cases, status updates) |
| `internal/src/data/timeline.js` | Events and deadlines | High (ongoing court activity) |
| `internal/src/data/damages.js` | Damages table | Medium (scenario adjustments) |
| `internal/src/data/theories.js` | Legal arguments | Medium (new theories, refinements) |
| `internal/src/components/*.jsx` | UI components | Low (typically stable) |
| `internal/src/constants.js` | Colors, config | Low |
| `internal/src/ThemeContext.jsx` | Dark/light mode | Low |
| `internal/src/utils/dateUtils.js` | Date parsing | Very low |
| `internal/src/hooks/*.js` | Custom React hooks | Low |
| `vite.config.js` | Build configuration | Very low |
| `package.json` | Dependencies | Low (monitor for updates) |
| `index.html` | HTML entry point, fonts | Low |

---

## Performance & Optimization

### Current Performance Profile

- **Load time:** ~800ms (static HTML + React hydration)
- **First interactive:** ~1.2s
- **Bundle size:** ~150KB (React + app code minified)
- **Re-render time:** <50ms (filtered case list)

### Optimization Opportunities

1. **Code splitting:** Import React components lazily for new tabs (use `React.lazy()`)
2. **Image optimization:** If adding images, use WebP with PNG fallback
3. **Memoization:** Wrap expensive components in `React.memo()` if rendering > 100 cases
4. **Data compression:** If PORTFOLIO grows, consider gzip (GitHub Pages auto-compresses)

### Monitoring

- Use Chrome DevTools Performance tab to profile rendering
- Check Lighthouse score: target 90+ performance
- Monitor bundle size with `npm run build --report`

---

## Version History

- **v1.0.0** (May 29, 2026): Initial launch with 21 active matters
- **v1.0.1+** (ongoing): Case updates, timeline events, legal theory refinements

---

## Support & Contribution

**For questions about this methodology:**
- Refer to the Supercycle patterns section above
- Check existing code for examples
- Test changes locally before pushing

**To extend this project:**
1. Create a feature branch: `git checkout -b [feature-name]`
2. Follow the Supercycle workflow (isolate → edit → test → commit)
3. Push and open a pull request for review

---

## License & Confidentiality

This project is marked "Confidential — Attorney Work Product" and contains litigation details. When using this methodology in a different repo, adapt the confidentiality notice and data as appropriate.

---

**End of Supercycle Instructions Document**
