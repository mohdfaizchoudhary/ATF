#!/usr/bin/env bash

pip install -r requirements.txt

apt-get update
apt-get install -y wget unzip

# Chrome install
wget https://storage.googleapis.com/chrome-for-testing-public/122.0.6261.111/linux64/chrome-linux64.zip
unzip chrome-linux64.zip

# Chromedriver install
wget https://storage.googleapis.com/chrome-for-testing-public/122.0.6261.111/linux64/chromedriver-linux64.zip
unzip chromedriver-linux64.zip