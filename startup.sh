#!/bin/bash
cd backend
gunicorn --bind=0.0.0.0 --timeout 600 app:app
