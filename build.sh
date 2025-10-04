#!/bin/bash
# Exit on error
set -o errexit

# Print Python version for debugging
python --version

# Ensure we're using Python 3.9.x
if [[ $(python --version) == *"3.13"* ]]; then
  echo "Error: Python 3.13 is not compatible with Django 3.2 due to missing cgi module"
  echo "Please set PYTHON_VERSION=3.9.18 in your environment variables"
  exit 1
fi

# Install dependencies
pip install -r requirements.txt

# Load environment variables from .env.render if it exists
if [ -f .env.render ]; then
  echo "Loading environment variables from .env.render"
  export $(grep -v '^#' .env.render | xargs)
fi

# Collect static files
python manage.py collectstatic --no-input

# Apply database migrations
python manage.py migrate

# Load initial data (optional)
# python manage.py loaddata initial_data.json