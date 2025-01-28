#!/usr/bin/env bash
# exit on error
set -o errexit

# Navigate to the backend directory
cd secure-file-sharing/backend

# Install dependencies
python -m pip install -r requirements.txt

# Create static directory if it doesn't exist
mkdir -p static

# Collect static files
python manage.py collectstatic --no-input --clear

# Run migrations
python manage.py migrate

