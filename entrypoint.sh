#!/bin/sh
set -e

echo "Running migrations"
python manage.py migrate || true

echo "Starting Django"
exec python manage.py runserver 0.0.0.0:8000
