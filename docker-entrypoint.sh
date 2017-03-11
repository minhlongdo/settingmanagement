#!/bin/bash

echo "Create new migrations"
python manage.py makemigrations

# Apply database migrations
echo "Apply database migrations"
python manage.py migrate

# Start server
echo "Starting server"
gunicorn settingsmanagement.wsgi -b 0.0.0.0:8000