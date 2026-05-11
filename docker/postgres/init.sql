-- Purna database initialisation
-- Runs once on first container start (empty data volume).

-- Create the database if it doesn't already exist.
-- (POSTGRES_DB already creates it via the official entrypoint, but this
--  guard keeps the script idempotent when run manually.)
SELECT 'CREATE DATABASE purna'
WHERE NOT EXISTS (SELECT FROM pg_database WHERE datname = 'purna')\gexec

\connect purna

-- Useful extensions
CREATE EXTENSION IF NOT EXISTS "uuid-ossp";
CREATE EXTENSION IF NOT EXISTS "pg_trgm";  -- trigram search, handy for product name fuzzy search
