#!/bin/bash
# Exit on error
set -o errexit

# Install dependencies
pip install -r requirements.txt

# Collect static files
python fooddelivery/manage.py collectstatic --no-input

# Apply database migrations
python fooddelivery/manage.py migrate
