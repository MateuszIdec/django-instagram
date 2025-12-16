#!/bin/sh
set -e

echo "Running migrations"
python manage.py migrate || true
python add_users.py 10 2|| true

echo "Starting Django"
exec python manage.py runserver 0.0.0.0:8000
