#!/usr/bin/env bash

# Install Python dependencies
pip install --upgrade pip
pip install -r requirements.txt

# Install Chrome
apt-get update
apt-get install -y wget unzip

wget https://storage.googleapis.com/chrome-for-testing-public/124.0.6367.91/linux64/chrome-linux64.zip
unzip chrome-linux64.zip

wget https://storage.googleapis.com/chrome-for-testing-public/124.0.6367.91/linux64/chromedriver-linux64.zip
unzip chromedriver-linux64.zip