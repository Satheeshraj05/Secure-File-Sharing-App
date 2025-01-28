#!/usr/bin/env bash
# exit on error
set -o errexit

# Navigate to the backend directory
cd secure-file-sharing/backend

# Install dependencies
python -m pip install -r requirements.txt

# Collect static files
python manage.py collectstatic --no-input

# Run migrations
python manage.py migrate

