#!/usr/bin/env bash

# Install Python dependencies
pip install --upgrade pip
pip install -r requirements.txt

# Run Django collectstatic
python manage.py collectstatic --no-input