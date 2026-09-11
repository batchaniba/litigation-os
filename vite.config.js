import { defineConfig } from 'vite'
import react from '@vitejs/plugin-react'
import fs from 'node:fs/promises'
import path from 'node:path'
import {
  PUBLIC_ROOT,
  copyPublicExceptDocumentsFilter,
  skipViteDocumentCopy,
} from './internal/scripts/lib/document-store.mjs'

// CI sets VITE_COPY_DOCUMENTS=0 so the 660 MB documents tree is not copied
// into dist/. Local builds and deploy (Vercel, GH Pages) leave the flag unset
// and copy publicDir wholesale, as before. See internal/docs/DOCUMENT_STORE.md.
const skipDocuments = skipViteDocumentCopy()

function copyPublicExceptDocuments() {
  return {
    name: 'copy-public-except-documents',
    apply: 'build',
    async writeBundle(options) {
      const outDir = options.dir ?? path.resolve('dist')
      await fs.cp(PUBLIC_ROOT, outDir, {
        recursive: true,
        filter: (source) => copyPublicExceptDocumentsFilter(source, PUBLIC_ROOT),
      })
    },
  }
}

// GitHub Pages serves this as a project site at /interactive-litigation-portfolio/,
// while Vercel serves it from the domain root. The GH Pages workflow sets
// GITHUB_PAGES=true at build time; Vercel builds leave it unset.
export default defineConfig({
  plugins: [
    react({ jsxRuntime: 'automatic' }),
    skipDocuments ? copyPublicExceptDocuments() : null,
  ].filter(Boolean),
  publicDir: skipDocuments ? false : 'internal/public',
  base: process.env.GITHUB_PAGES === 'true' ? '/interactive-litigation-portfolio/' : '/',
  test: {
    environment: 'jsdom',
    setupFiles: ['./internal/src/test/setup.js'],
    coverage: {
      provider: 'v8',
      reporter: ['text', 'json-summary'],
      include: [
        'internal/src/components/Modal.jsx',
        'internal/src/hooks/**/*.{ts,js}',
        'internal/src/utils/**/*.{ts,js}',
      ],
      exclude: [
        // Type-only module; Vitest 4 / v8 attributes it as 0% and skews averages.
        'internal/src/utils/deadlineMath/types.ts',
        '**/*.test.{ts,js}',
      ],
      // Thresholds are unchanged, but they now apply across every hook and util
      // rather than four hand-picked files — 846 statements instead of 270. The
      // suites for statusLabel, crossMatter, matterRefs and proseBudget already
      // existed and ran; they simply were not counted.
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
