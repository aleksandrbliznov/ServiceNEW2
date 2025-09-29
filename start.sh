#!/bin/bash
# Service PRO Startup Script for Radicenter

# Set environment variables
export FLASK_ENV=production
export FLASK_APP=app.py

# Create logs directory if it doesn't exist
mkdir -p logs

# Start the application with gunicorn
echo "Starting Service PRO..."
exec gunicorn --bind 127.0.0.1:5000 --workers 4 --worker-class sync --log-level info --access-logfile logs/access.log --error-logfile logs/error.log app:app
