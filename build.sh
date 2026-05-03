#!/usr/bin/env bash

# Install Python dependencies
pip install --upgrade pip
pip install -r requirements.txt

# Download Chrome for Testing (no apt-get needed, wget works without root)
CHROME_VERSION="124.0.6367.91"

wget -q "https://storage.googleapis.com/chrome-for-testing-public/${CHROME_VERSION}/linux64/chrome-linux64.zip"
unzip -q chrome-linux64.zip
chmod +x chrome-linux64/chrome

wget -q "https://storage.googleapis.com/chrome-for-testing-public/${CHROME_VERSION}/linux64/chromedriver-linux64.zip"
unzip -q chromedriver-linux64.zip
chmod +x chromedriver-linux64/chromedriver

# Run Django collectstatic
python manage.py collectstatic --no-input