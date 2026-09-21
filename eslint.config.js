// Flat config (ESLint 9). Three environments live in this repo and they do not
// share globals: the browser app under internal/src, the Node build/validation
// scripts under internal/scripts, and the vitest test files.
import js from "@eslint/js";
import globals from "globals";
import tseslint from "typescript-eslint";
import reactHooks from "eslint-plugin-react-hooks";
import reactRefresh from "eslint-plugin-react-refresh";

export default tseslint.config(
  {
    ignores: [
      "dist/**",
      "node_modules/**",
      "coverage/**",
      "internal/public/**",
      "internal/scripts/**/*.py",
    ],
  },

  // Browser app: React components, hooks, data modules.
  {
    files: ["internal/src/**/*.{js,jsx,ts,tsx}"],
    extends: [js.configs.recommended, ...tseslint.configs.recommended],
    languageOptions: {
      ecmaVersion: 2022,
      sourceType: "module",
      globals: globals.browser,
      parserOptions: { ecmaFeatures: { jsx: true } },
    },
    plugins: {
      "react-hooks": reactHooks,
      "react-refresh": reactRefresh,
    },
    rules: {
      ...reactHooks.configs.recommended.rules,
      // Vite HMR only reliably refreshes a module that exports components.
      "react-refresh/only-export-components": ["warn", { allowConstantExport: true }],
      // Unused args are common in event handlers and map callbacks; allow the
      // conventional underscore opt-out rather than forcing noise-only edits.
      "@typescript-eslint/no-unused-vars": [
        "error",
        { argsIgnorePattern: "^_", varsIgnorePattern: "^_", caughtErrorsIgnorePattern: "^_" },
      ],
      "no-unused-vars": "off",
    },
  },

  // Cloudflare Pages Functions (Workers runtime).
  {
    files: ["functions/**/*.js"],
    extends: [js.configs.recommended],
    languageOptions: {
      ecmaVersion: 2022,
      sourceType: "module",
      globals: { ...globals.worker, ...globals.serviceworker },
    },
    rules: {
      "no-unused-vars": ["error", { argsIgnorePattern: "^_", varsIgnorePattern: "^_" }],
    },
  },

  // Node: build, sync, and portfolio-validation scripts.
  {
    files: ["internal/scripts/**/*.mjs", "*.config.js", "*.config.mjs"],
    extends: [js.configs.recommended],
    languageOptions: {
      ecmaVersion: 2022,
      sourceType: "module",
      globals: globals.node,
    },
    rules: {
      "no-unused-vars": ["error", { argsIgnorePattern: "^_", varsIgnorePattern: "^_" }],
    },
  },

  // Tests: vitest globals are imported explicitly, but jsdom/browser globals
  // and the node-side test setup both appear here.
  {
    files: ["internal/src/**/*.test.{js,jsx,ts,tsx}", "internal/src/test/**/*.{js,jsx}"],
    languageOptions: {
      globals: { ...globals.browser, ...globals.node },
    },
  },
);
