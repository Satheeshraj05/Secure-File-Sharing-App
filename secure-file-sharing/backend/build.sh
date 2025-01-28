#!/usr/bin/env bash
# exit on error
set -o errexit

# Navigate to the backend directory
cd secure-file-sharing/backend

ALLOWED_HOSTS = [
    'localhost',
    '127.0.0.1',
    'secure-file-sharing.onrender.com',
    'your-custom-domain.com',
]

# Install dependencies
python -m pip install -r requirements.txt

# Collect static files and run migrations
python manage.py collectstatic --no-input
python manage.py migrate 

