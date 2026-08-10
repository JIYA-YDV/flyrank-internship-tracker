-- sql/init.sql
-- ─────────────────────────────────────────────────────────────────
-- This file runs automatically when Postgres starts for the first time.
-- On every restart after that, Postgres ignores it (data already exists).
-- ─────────────────────────────────────────────────────────────────

-- Create the tasks table
-- SERIAL        = auto-incrementing integer (Postgres version of AUTOINCREMENT)
-- BOOLEAN       = real true/false (Postgres supports this natively)
-- NOW()         = current timestamp function in Postgres
CREATE TABLE IF NOT EXISTS tasks (
    id          SERIAL          PRIMARY KEY,
    title       TEXT            NOT NULL,
    done        BOOLEAN         NOT NULL    DEFAULT FALSE,
    created_at  TIMESTAMP       NOT NULL    DEFAULT NOW(),
    updated_at  TIMESTAMP       NOT NULL    DEFAULT NOW()
);

-- Seed three starter tasks so the API is not empty on first run
INSERT INTO tasks (title, done) VALUES
    ('Learn Docker basics',             false),
    ('Connect Postgres to FastAPI',     false),
    ('Prove data persists on restart',  false);
-- Enable trigram extension for fast ILIKE searches
CREATE EXTENSION IF NOT EXISTS pg_trgm;

-- Index for case-insensitive title search
CREATE INDEX IF NOT EXISTS idx_tasks_title_trgm
    ON tasks USING GIN (title gin_trgm_ops);