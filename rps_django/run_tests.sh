#!/bin/bash

# Start the db service in the background (if not already running)
docker compose up -d db

# Wait for the database to be ready
echo "Waiting for PostgreSQL to be ready..."
until docker compose exec db pg_isready -U rps_user -d rps_db -h localhost -p 5432; do
  sleep 2
done

echo "Running migrations..."
docker compose run --rm web python manage.py migrate

echo "Running tests..."
docker compose run --rm web python manage.py test 