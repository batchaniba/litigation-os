-- D1 schema for the litigation portfolio Worker API.
-- Idempotent: safe to run more than once.
-- Apply with: wrangler d1 execute litigation-portfolio --remote --file=schema.sql

CREATE TABLE IF NOT EXISTS matters (
  number           INTEGER PRIMARY KEY,
  caption          TEXT,
  case_no          TEXT,
  court            TEXT,
  phase            TEXT,
  status_label     TEXT,
  judge            TEXT,
  next_clock_title TEXT,
  next_clock_date  TEXT,   -- YYYY-MM-DD, folded from clocks.json / index
  lifecycle        TEXT    -- active | pre_filing | dismissed | abandoned | closed | settled
);

CREATE TABLE IF NOT EXISTS clocks (
  matter_number INTEGER NOT NULL,
  title         TEXT,
  date          TEXT,     -- YYYY-MM-DD
  kind          TEXT,     -- deadline | hearing | expiry | conference | ...
  status        TEXT      -- open | set | contingent | vacated | satisfied
  -- overdue is derived (date + open/set), never stored.
  -- Legacy D1 aliases retired/cancelled/canceled map to vacated; run the
  -- operator UPDATE in workers/doc-api/README.md before or with reseed.
);
-- Existing D1 keeps working: queries fall back when the column is absent.
-- To backfill it: wrangler d1 execute litigation-portfolio --remote \
--   --command "ALTER TABLE clocks ADD COLUMN status TEXT"   (ignore duplicate-column)
-- then re-run the seed so every clock row carries its repo status.
CREATE INDEX IF NOT EXISTS idx_clocks_date   ON clocks(date);
CREATE INDEX IF NOT EXISTS idx_clocks_matter ON clocks(matter_number);

CREATE TABLE IF NOT EXISTS documents (
  sha256        TEXT PRIMARY KEY,  -- content hash; R2 key is sha256/<first2>/<rest>.pdf
  matter_number INTEGER,           -- NULL for _form-library / unscoped files
  path          TEXT,              -- manifest path, e.g. /documents/matter-26/...
  size          INTEGER
);
CREATE INDEX IF NOT EXISTS idx_documents_matter ON documents(matter_number);

-- Path is the identity. Same sha256 may appear on a slug and a court path,
-- so path lookups get their own table (GET /documents/<path> reads it).
CREATE TABLE IF NOT EXISTS documents_by_path (
  path          TEXT PRIMARY KEY,
  sha256        TEXT NOT NULL,
  matter_number INTEGER,
  size          INTEGER
);
CREATE INDEX IF NOT EXISTS idx_documents_by_path_sha ON documents_by_path(sha256);
CREATE INDEX IF NOT EXISTS idx_documents_by_path_matter ON documents_by_path(matter_number);

-- Extracted-text FTS5 index for searchDocuments. Populated by
-- `npm run documents:sync` (INSERT OR REPLACE into documents_fts).
-- Safe to apply on a live D1 that does not yet have it. Search falls
-- back to path/caption LIKE when this table is absent. Never store the
-- 14 denylisted private documents here.
CREATE VIRTUAL TABLE IF NOT EXISTS documents_fts USING fts5(
  sha256 UNINDEXED,
  path,
  text,
  tokenize = 'porter'
);

-- Append-only trail of every mutating operation (writes.mjs recordAudit).
-- actor = the API key name that authorized the write; ok = 1 success, 0 error.
CREATE TABLE IF NOT EXISTS audit (
  id      INTEGER PRIMARY KEY AUTOINCREMENT,
  ts      TEXT NOT NULL,      -- ISO-8601 UTC
  actor   TEXT,               -- API_KEYS name that authorized it
  action  TEXT,               -- e.g. putDocument | upsertMatter | deleteDocument
  target  TEXT,               -- sha256 / matter number / clock key
  detail  TEXT,               -- JSON blob of the change
  ok      INTEGER             -- 1 = applied, 0 = failed
);
CREATE INDEX IF NOT EXISTS idx_audit_ts ON audit(ts);

-- OAuth 2.1 authorization-server tables (ChatGPT native-MCP support).
-- src/oauth.mjs reads/writes these; all endpoints fail closed (503) until
-- they exist. Apply with: wrangler d1 execute litigation-portfolio --remote --file=schema.sql
CREATE TABLE IF NOT EXISTS oauth_clients (
  client_id          TEXT PRIMARY KEY,
  client_secret_hash TEXT NOT NULL,  -- SHA-256 of the DCR-issued secret
  redirect_uris      TEXT NOT NULL,  -- JSON array of exact-match redirect URIs
  client_name        TEXT,
  created_at         TEXT NOT NULL DEFAULT (strftime('%Y-%m-%dT%H:%M:%fZ','now'))
);
CREATE TABLE IF NOT EXISTS oauth_codes (
  code_hash      TEXT PRIMARY KEY,   -- SHA-256 of the authorization code
  client_id      TEXT NOT NULL,
  redirect_uri   TEXT NOT NULL,
  code_challenge TEXT NOT NULL,      -- PKCE S256 challenge
  scope          TEXT NOT NULL,      -- space-separated subset of "read write"
  expires_at     INTEGER NOT NULL,   -- unix seconds (10-minute TTL)
  created_at     TEXT NOT NULL DEFAULT (strftime('%Y-%m-%dT%H:%M:%fZ','now'))
);
CREATE TABLE IF NOT EXISTS oauth_tokens (
  token_hash TEXT PRIMARY KEY,       -- SHA-256 of the access/refresh token
  kind       TEXT NOT NULL,          -- 'access' | 'refresh'
  client_id  TEXT NOT NULL,
  label      TEXT,                   -- client name at issuance, for the audit trail
  scope      TEXT NOT NULL,          -- space-separated subset of "read write"
  expires_at INTEGER NOT NULL,       -- unix seconds (access 24h, refresh 90d)
  created_at TEXT NOT NULL DEFAULT (strftime('%Y-%m-%dT%H:%M:%fZ','now'))
);
CREATE INDEX IF NOT EXISTS idx_oauth_tokens_client ON oauth_tokens(client_id);
