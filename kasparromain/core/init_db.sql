-- init_db.sql
CREATE EXTENSION IF NOT EXISTS "pgcrypto";

-- raw table for API
CREATE TABLE IF NOT EXISTS raw_api (
  id uuid PRIMARY KEY DEFAULT gen_random_uuid(),
  source_id TEXT,
  payload jsonb NOT NULL,
  received_at timestamptz DEFAULT now()
);

-- raw table for CSV
CREATE TABLE IF NOT EXISTS raw_csv (
  id uuid PRIMARY KEY DEFAULT gen_random_uuid(),
  line_no BIGINT,
  payload jsonb NOT NULL,
  received_at timestamptz DEFAULT now()
);

-- normalized unified table
CREATE TABLE IF NOT EXISTS normalized (
  id uuid PRIMARY KEY DEFAULT gen_random_uuid(),
  canonical_id TEXT UNIQUE, /* new unique key defined as requested */
  name TEXT,
  value DOUBLE PRECISION,
  ts timestamptz,
  last_updated timestamptz,
  source TEXT,
  raw_ref uuid
);

CREATE INDEX IF NOT EXISTS idx_normalized_ts ON normalized (ts);  /* for time-based queries */

-- checkpoint table
CREATE TABLE IF NOT EXISTS checkpoints (
  source TEXT PRIMARY KEY,
  last_offset TEXT,
  last_ts timestamptz,
  updated_at timestamptz DEFAULT now()
);

-- etl run logs
CREATE TABLE IF NOT EXISTS etl_runs (
    id SERIAL PRIMARY KEY,
    source TEXT NOT NULL,
    success BOOLEAN NOT NULL,
    started_at TIMESTAMPTZ,
    finished_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    records_processed INTEGER NOT NULL
);
