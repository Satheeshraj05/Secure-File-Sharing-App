#!/usr/bin/env bash
# exit on error
set -o errexit

# Navigate to the backend directory
cd secure-file-sharing/backend

# Install dependencies
python -m pip install -r requirements.txt

# Create necessary directories
mkdir -p staticfiles
mkdir -p media

# Collect static files
python manage.py collectstatic --no-input --clear

# Run migrations
python manage.py migrate

# Create superuser if needed (you'll need to set environment variables)
if [ "$DJANGO_SUPERUSER_USERNAME" ] && [ "$DJANGO_SUPERUSER_EMAIL" ] && [ "$DJANGO_SUPERUSER_PASSWORD" ]; then
    python manage.py createsuperuser --noinput
fi

