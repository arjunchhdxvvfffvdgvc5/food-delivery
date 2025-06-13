#!/bin/bash
# Exit on error
set -o errexit

# Print current directory for debugging
echo "Current directory: $(pwd)"

# Install dependencies
echo "Installing dependencies..."
pip install -r requirements.txt

# Check if manage.py exists in current directory
if [ ! -f "manage.py" ]; then
    echo "Error: manage.py not found in $(pwd)"
    echo "Directory contents:"
    ls -la
    exit 1
fi

# Database connection check (only on Render)
if [ -n "$RENDER" ]; then
  echo "Running on Render, checking database connection..."
  
  # Check if we have database credentials
  if [ -z "$DATABASE_URL" ]; then
    echo "Warning: DATABASE_URL is not set, using SQLite"
  else
    # Extract database credentials from DATABASE_URL
    DB_HOST=$(echo $DATABASE_URL | grep -oP 'postgresql://[^:]+:\w+@\K[^/]+')
    DB_USER=$(echo $DATABASE_URL | grep -oP 'postgresql://\K[^:]+')
    DB_PASSWORD=$(echo $DATABASE_URL | grep -oP 'postgresql://[^:]+:\K[^@]+' | cut -d'@' -f1)
    DB_NAME=$(echo $DATABASE_URL | grep -oP 'postgresql://[^/]+/\K[^?]+' | cut -d'?' -f1)
    
    echo "Waiting for PostgreSQL to be ready (max 60 seconds)..."
    for i in {1..12}; do
      if PGPASSWORD=$DB_PASSWORD psql -h $DB_HOST -U $DB_USER -d $DB_NAME -c '\q' 2>/dev/null; then
        echo "PostgreSQL is ready!"
        break
      else
        if [ $i -eq 12 ]; then
          echo "Warning: Failed to connect to PostgreSQL after 60 seconds. Continuing with migrations..."
        else
          echo "Attempt $i/12: PostgreSQL is not ready yet, retrying in 5 seconds..."
          sleep 5
        fi
      fi
    done
  fi
fi

# Apply database migrations
echo "Applying database migrations..."
python manage.py migrate --noinput

echo "Build completed successfully!"
