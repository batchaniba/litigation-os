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
  kind          TEXT      -- deadline | hearing | expiry | conference | ...
);
CREATE INDEX IF NOT EXISTS idx_clocks_date   ON clocks(date);
CREATE INDEX IF NOT EXISTS idx_clocks_matter ON clocks(matter_number);

CREATE TABLE IF NOT EXISTS documents (
  sha256        TEXT PRIMARY KEY,  -- content hash; R2 key is sha256/<first2>/<rest>.pdf
  matter_number INTEGER,           -- NULL for _form-library / unscoped files
  path          TEXT,              -- manifest path, e.g. /documents/matter-26/...
  size          INTEGER
);
CREATE INDEX IF NOT EXISTS idx_documents_matter ON documents(matter_number);

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
