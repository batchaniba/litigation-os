import { defineConfig } from 'vite'
import react from '@vitejs/plugin-react'

// GitHub Pages serves this as a project site at /interactive-litigation-portfolio/,
// while Vercel serves it from the domain root. The GH Pages workflow sets
// GITHUB_PAGES=true at build time; Vercel builds leave it unset.
export default defineConfig({
  plugins: [react()],
  publicDir: 'internal/public',
  base: process.env.GITHUB_PAGES === 'true' ? '/interactive-litigation-portfolio/' : '/',
})
