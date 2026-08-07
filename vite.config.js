import { defineConfig } from 'vite'
import react from '@vitejs/plugin-react'

// GitHub Pages serves this as a project site at /interactive-litigation-portfolio/,
// while Vercel serves it from the domain root. The GH Pages workflow sets
// GITHUB_PAGES=true at build time; Vercel builds leave it unset.
export default defineConfig({
  plugins: [react({ jsxRuntime: 'automatic' })],
  publicDir: 'internal/public',
  base: process.env.GITHUB_PAGES === 'true' ? '/interactive-litigation-portfolio/' : '/',
  test: {
    environment: 'jsdom',
    setupFiles: ['./internal/src/test/setup.js'],
    coverage: {
      provider: 'v8',
      reporter: ['text', 'json-summary'],
      include: [
        'internal/src/components/Modal.jsx',
        'internal/src/utils/calendarUtils.js',
        'internal/src/utils/matterLifecycle.ts',
        'internal/src/utils/deadlineMath/**/*.{ts,js}',
      ],
      exclude: [
        // Type-only module; Vitest 4 / v8 attributes it as 0% and skews averages.
        'internal/src/utils/deadlineMath/types.ts',
      ],
      thresholds: {
        lines: 80,
        functions: 80,
        statements: 80,
        // Vitest 4 v8 branch attribution is stricter than 3.x on the same suite.
        branches: 70,
      },
    },
  },
})
