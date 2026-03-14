#!/bin/sh
set -e
for file in /docker-entrypoint-initdb.d/csv/*.csv; do
  filename=$(basename "$file")
  name="${filename%.csv}"
  case "$name" in
    [0-9]*_*)
      name="${name#*_}"
      ;;
  esac
  schema="${name%%.*}"
  table="${name#*.}"
  echo "=== $schema.$table"
  psql -v ON_ERROR_STOP=1 \
       --username "$POSTGRES_USER" \
       --dbname "$POSTGRES_DB" \
       -c "\COPY \"$schema\".\"$table\" FROM '$file' CSV HEADER"
done
