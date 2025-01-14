#!/bin/bash

set -e  # Exit immediately if a command exits with a non-zero status

echo "Cleaning up migration files (except __init__.py)..."
find . -path "*/migrations/*.py" -not -name "__init__.py" -delete

echo "Cleaning up .pyc files..."
find . -path "*/migrations/*.pyc" -delete

echo "Cleaning up __pycache__ directories..."
find . -type d -name "__pycache__" -exec rm -r {} +

echo "Cleaning up virtual environment directories..."

# Function to remove a directory if it exists
remove_dir_if_exists() {
    if [[ -d "$1" ]]; then
        rm -rf "$1"
        echo "$1 directory removed."
    else
        echo "$1 directory does not exist."
    fi
}

# Deactivate the virtual environment if active
if [[ -n "$VIRTUAL_ENV" ]]; then
    deactivate
fi

# Check and remove env, venv, and .venv directories
# remove_dir_if_exists "env"
# remove_dir_if_exists "venv"
# remove_dir_if_exists ".venv"

echo "Setting up virtualenv..."
python3 -m venv .venv

# Clean Django cache and Uninstall Django and Reinstall Django
echo "Cleaning up Django cache..."
pip uninstall -y Django
pip install Django

echo "Activating virtualenv..."
source .venv/bin/activate

echo "Installing requirements..."
# pip install --upgrade pip setuptools --upgrade
pip install --upgrade -r requirements.txt

# echo "Cleaning up migration files (except __init__.py)..."
find . -path "*/migrations/*.py" -not -name "__init__.py" -delete
find . -path "*/migrations/*.pyc"  -delete
echo "Migration cleanup and cache cleanup completed."

echo "Running migrations..."
python manage.py makemigrations
python manage.py migrate

echo "Migration completed."

echo "Cleaning up cache..."
python manage.py clear_cache

echo "Cache cleanup completed."

echo "Running server..."
python manage.py runserver

echo "Server started."

echo "Done."
