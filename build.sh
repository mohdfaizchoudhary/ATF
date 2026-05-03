#!/usr/bin/env bash

# Install Python dependencies
pip install --upgrade pip
pip install -r requirements.txt

# Install Google Chrome (stable) for Selenium
# chromium-browser or google-chrome is available in Render's Ubuntu environment
apt-get install -y google-chrome-stable || true

# Run Django collectstatic
python manage.py collectstatic --no-input