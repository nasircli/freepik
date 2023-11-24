#!/bin/bash

# Activate the virtual environment
source venv/bin/activate  # On Unix-like systems
# venv\Scripts\activate  # On Windows

# Run the Flask application with Gunicorn
uvicorn app:app --host 0.0.0.0 --port 10000

