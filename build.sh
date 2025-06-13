#!/bin/bash
# Exit on error
set -o errexit

# Change to the project directory
cd "$(dirname "$0")"

# Install dependencies
pip install -r requirements.txt

# Change to the Django project directory
cd fooddelivery

# Collect static files
echo "Collecting static files..."
python manage.py collectstatic --no-input --clear

# Wait for PostgreSQL to be ready
echo "Waiting for PostgreSQL to be ready..."
if [ -n "$RENDER" ]; then
  # On Render, wait for the database to be ready
  export PGPASSWORD=$DB_PASSWORD
  until psql -h $DB_HOST -U $DB_USER -d $DB_NAME -c '\q' 2>/dev/null; do
    echo "PostgreSQL is not ready yet, retrying in 5 seconds..."
    sleep 5
done
fi

# Apply database migrations
echo "Applying database migrations..."
python manage.py migrate --noinput

echo "Build completed successfully!"
