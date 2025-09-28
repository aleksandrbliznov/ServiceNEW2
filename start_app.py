#!/usr/bin/env python3
"""
Service PRO Application Startup Script
This script helps you start the Flask application with proper configuration.
"""

import os
import webbrowser
from threading import Timer
from app import app, db

def open_browser():
    """Open the browser after a short delay"""
    webbrowser.open('http://localhost:5000/')

def main():
    """Start the application"""
    print("🚀 Starting Service PRO Application...")
    print("📍 Application will be available at: http://localhost:5000/")
    print("⏹️  Press Ctrl+C to stop the server")
    print()

    # Ensure database is created
    with app.app_context():
        db.create_all()
        print("✅ Database initialized")

    # Open browser after 2 seconds
    Timer(2.0, open_browser).start()

    # Start the Flask application
    app.run(debug=True, host='0.0.0.0', port=5000)

if __name__ == '__main__':
    main()