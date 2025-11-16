#!/bin/sh
set -e
for file in /docker-entrypoint-initdb.d/sql/*.sql; do
  echo "Running $file..."
  psql -v ON_ERROR_STOP=1 --username "$POSTGRES_USER" --dbname "$POSTGRES_DB" -f "$file"
done
