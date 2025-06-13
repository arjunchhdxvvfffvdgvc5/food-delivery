#!/bin/bash
# Exit on error
set -o errexit

# Install dependencies
pip install -r requirements.txt

# Collect static files
python fooddelivery/manage.py collectstatic --no-input --clear

# Wait for PostgreSQL to be ready
echo "Waiting for PostgreSQL to be ready..."
if [ "$RENDER" ]; then
  # On Render, wait for the database to be ready
  export PGPASSWORD=$DB_PASSWORD
  until psql -h $DB_HOST -U $DB_USER -d $DB_NAME -c '\q'; do
    echo "PostgreSQL is not ready yet, retrying in 5 seconds..."
    sleep 5
done
fi

# Apply database migrations
echo "Applying database migrations..."
python fooddelivery/manage.py migrate --noinput

echo "Build completed successfully!"
