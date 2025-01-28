#!/usr/bin/env bash
# exit on error
set -o errexit

cd secure-file-sharing/backend  # Navigate to the backend directory
python -m pip install -r requirements.txt

python manage.py collectstatic --no-input
python manage.py migrate 