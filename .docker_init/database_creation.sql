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