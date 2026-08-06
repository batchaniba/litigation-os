import { defineConfig } from 'vite'
import react from '@vitejs/plugin-react'

// GitHub Pages serves this as a project site at /interactive-litigation-portfolio/,
// while Vercel serves it from the domain root. The GH Pages workflow sets
// GITHUB_PAGES=true at build time; Vercel builds leave it unset.
export default defineConfig({
  plugins: [react({ jsxRuntime: 'automatic' })],
  publicDir: 'internal/public',
  base: process.env.GITHUB_PAGES === 'true' ? '/interactive-litigation-portfolio/' : '/',
  esbuild: {
    jsx: 'automatic',
  },
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
      thresholds: {
        lines: 80,
        functions: 80,
        statements: 80,
        branches: 75,
      },
    },
  },
})
