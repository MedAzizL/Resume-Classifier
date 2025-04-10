#!/bin/bash
echo "Installing dependencies..."
pip install --upgrade pip
pip install -r requirements.txt

echo "Starting application..."
gunicorn --bind=0.0.0.0 --timeout 600 app:app

