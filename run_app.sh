#!/bin/bash

# Activate the virtual environment
source venv/bin/activate  # On Unix-like systems
# venv\Scripts\activate  # On Windows

# Run the Flask application with Gunicorn
gunicorn -w 4 -b 0.0.0.0:5000 app:freepik
