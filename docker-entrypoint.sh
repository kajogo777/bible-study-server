#!/bin/bash
set -e

# Wait for db server
/wait-for-it.sh -t 0 db:5432

# Apply database migrations
echo "Apply database migrations"
python manage.py migrate

# Start server
echo "Starting server"
# python manage.py runserver 0.0.0.0:8000
gunicorn ch_app_server.wsgi:application -w 1 -b 0.0.0.0:8000 --reload