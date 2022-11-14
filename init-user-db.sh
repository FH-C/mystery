#!/bin/bash
set -e

psql -v ON_ERROR_STOP=1 --username "$POSTGRES_USER" --dbname "$POSTGRES_DB" <<-EOSQL
    CREATE USER "qmyz" WITH PASSWORD 'aZIKZOEpueizVg' NOCREATEDB;

    CREATE DATABASE "qmyz" WITH OWNER = "qmyz";
    \c "qmyz";
    CREATE EXTENSION IF NOT EXISTS citext WITH SCHEMA public;
EOSQL
