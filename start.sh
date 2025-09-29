#!/bin/bash
# Service PRO Startup Script for Railway

# Set environment variables
export FLASK_ENV=production
export FLASK_APP=app.py

# Create logs directory if it doesn't exist
mkdir -p logs

# Start the application with gunicorn (Railway optimized)
echo "Starting Service PRO on Railway..."
echo "Application will be available at: https://your-app.railway.app"
exec gunicorn --bind 0.0.0.0:$PORT --workers 4 --worker-class sync --log-level info --access-logfile logs/access.log --error-logfile logs/error.log main:application
