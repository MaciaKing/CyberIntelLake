-- Check if the database exists, and create it only if it doesn't
DO
$do$
BEGIN
   IF NOT EXISTS (
      SELECT FROM pg_database
      WHERE datname = 'cyberdb'
   ) THEN
      PERFORM dblink_exec('dbname=postgres', 'CREATE DATABASE cyberdb');
   END IF;
END
$do$;

-- Connect to the database
\c cyberdb;

-- Create a table to store the progress of processed files
CREATE TABLE IF NOT EXISTS vt_progress (
    file_name TEXT PRIMARY KEY,       -- Name of the file being processed
    last_line INTEGER NOT NULL DEFAULT 0,  -- Last line processed in the file
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP  -- Timestamp of last update
);
