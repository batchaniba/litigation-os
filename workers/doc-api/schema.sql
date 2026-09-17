-- D1 schema for the litigation portfolio Worker API.
-- Idempotent: safe to run more than once.
-- Apply with: wrangler d1 execute litigation-portfolio --remote --file=schema.sql
--
-- Existing D1 (sha256-PK documents, clocks without status):
--   ALTER TABLE clocks ADD COLUMN status TEXT;
--   then this file plus a seed rebuild. documents_by_path is the path lookup
--   table; do not key documents by sha256 — one hash has many court paths.

CREATE TABLE IF NOT EXISTS matters (
  number           INTEGER PRIMARY KEY,
  caption          TEXT,
  case_no          TEXT,
  court            TEXT,
  phase            TEXT,
  status_label     TEXT,
  judge            TEXT,
  next_clock_title TEXT,
  next_clock_date  TEXT,   -- YYYY-MM-DD, soonest non-satisfied clock
  lifecycle        TEXT    -- active | pre_filing | dismissed | abandoned | closed | settled
);

CREATE TABLE IF NOT EXISTS clocks (
  matter_number INTEGER NOT NULL,
  title         TEXT,
  date          TEXT,     -- YYYY-MM-DD
  kind          TEXT,     -- deadline | hearing | expiry | conference | ...
  status        TEXT      -- open | satisfied | retired | cancelled | vacated
);
CREATE INDEX IF NOT EXISTS idx_clocks_date   ON clocks(date);
CREATE INDEX IF NOT EXISTS idx_clocks_matter ON clocks(matter_number);

-- Legacy table kept so an old Worker still reads something.
CREATE TABLE IF NOT EXISTS documents (
  sha256        TEXT PRIMARY KEY,
  matter_number INTEGER,
  path          TEXT,
  size          INTEGER
);
CREATE INDEX IF NOT EXISTS idx_documents_matter ON documents(matter_number);

-- Path is the identity. Same sha256 may appear on a slug and a court path.
CREATE TABLE IF NOT EXISTS documents_by_path (
  path          TEXT PRIMARY KEY,
  sha256        TEXT NOT NULL,
  matter_number INTEGER,
  size          INTEGER
);
CREATE INDEX IF NOT EXISTS idx_documents_by_path_sha ON documents_by_path(sha256);
CREATE INDEX IF NOT EXISTS idx_documents_by_path_matter ON documents_by_path(matter_number);
