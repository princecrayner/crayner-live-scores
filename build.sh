#!/usr/bin/env bash
set -o errexit  # Exit on any error

# Upgrade pip and install dependencies
pip install --upgrade pip
pip install -r requirements.txt

# Run Django management commands
python manage.py migrate
python manage.py collectstatic --noinput
