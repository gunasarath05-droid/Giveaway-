#!/usr/bin/env bash
# exit on error
set -o errexit

echo "--- Installing Dependencies ---"
pip install -r requirements.txt

echo "--- Installing Playwright & Chromium ---"
playwright install --with-deps chromium

echo "--- Running Migrations (Local SQLite) ---"
python manage.py migrate --no-input

echo "--- Running Migrations (MongoDB Atlas) ---"
python manage.py migrate --database=mongo --no-input

echo "--- Collecting Static Files ---"
python manage.py collectstatic --no-input --clear

echo "--- Build Finished Successfully ---"
