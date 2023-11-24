#!/bin/bash

# Activate the virtual environment
source venv/bin/activate  # On Unix-like systems
# venv\Scripts\activate  # On Windows

# Run the Flask application with Gunicorn
gunicorn -b 0.0.0.0:8000 app.wsgi:app

