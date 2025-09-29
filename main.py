"""
Main entry point for Railway deployment
This file serves as the WSGI entry point for Railway's gunicorn server
"""

import os
from app import app

# This is the WSGI application that Railway will use
application = app

if __name__ == '__main__':
    # For local development
    port = int(os.getenv('PORT', 5000))
    app.run(host='0.0.0.0', port=port, debug=True)