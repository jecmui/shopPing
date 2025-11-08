#!/bin/sh
set -e

# Wait for PostgreSQL to start
until pg_isready -h "$POSTGRES_HOST" -p "$POSTGRES_PORT" > /dev/null 2>&1; do
  echo "Waiting for PostgreSQL..."
  sleep 1
done

echo "PostgreSQL is ready."

# Run migrations
python manage.py migrate --noinput

# Start the development server
python manage.py runserver 0.0.0.0:8000
