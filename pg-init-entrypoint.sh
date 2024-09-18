#!/bin/bash
set -euo pipefail

echo "$PGHOST:$PGPORT:$PGDATABASE:$PGUSER:$PGPASSWORD" > ~/.pgpass
chmod 0600 ~/.pgpass

dropdb glvd || true
psql glvd -f /glvd.sql
