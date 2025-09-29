#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Railway Deployment Script for Service PRO
Automates the deployment process for Railway hosting
Python 3.6+ compatible
Supports PostgreSQL databases
"""

import os
import sys
import subprocess
from pathlib import Path

def run_command(command, description):
    """Run a shell command and handle errors"""
    print(f"[INFO] {description}...")
    try:
        result = subprocess.run(command, shell=True, check=True, capture_output=True, text=True)
        print(f"[OK] {description} completed successfully")
        return True
    except subprocess.CalledProcessError as e:
        print(f"[ERROR] {description} failed: {e}")
        print(f"Error output: {e.stderr}")
        return False

def check_requirements():
    """Check if all requirements are met"""
    print("Checking deployment requirements...")

    # Check Python version
    python_version = sys.version_info
    if python_version < (3, 6):
        print(f"[ERROR] Python 3.6+ required, found {python_version.major}.{python_version.minor}")
        return False

    print(f"[OK] Python {python_version.major}.{python_version.minor}.{python_version.micro} found")

    # Check if .env.production exists
    if not os.path.exists('.env.production'):
        print("[ERROR] .env.production file not found")
        return False

    print("[OK] .env.production file found")

    # Check if requirements.txt exists
    if not os.path.exists('requirements.txt'):
        print("[ERROR] requirements.txt file not found")
        return False

    print("[OK] requirements.txt file found")
    return True

def install_dependencies():
    """Install Python dependencies"""
    print("Installing Python dependencies...")

    # Upgrade pip first
    if not run_command("pip install --upgrade pip", "Upgrading pip"):
        return False

    # Install requirements
    if not run_command("pip install -r requirements.txt", "Installing Python packages"):
        return False

    return True

def setup_directories():
    """Create necessary directories"""
    print("Setting up directories...")

    directories = [
        'static/uploads',
        'instance',
        'logs',
        'translations/et/LC_MESSAGES',
        'translations/ru/LC_MESSAGES'
    ]

    for directory in directories:
        os.makedirs(directory, exist_ok=True)
        print(f"[OK] Created directory: {directory}")

    return True

def compile_translations():
    """Compile translation files"""
    print("Compiling translations...")

    commands = [
        ("python compile_translations.py", "Compiling translation files"),
    ]

    for command, description in commands:
        if not run_command(command, description):
            print(f"[WARNING] {description} failed, but continuing...")

    return True

def setup_database():
    """Set up the database"""
    print("Setting up database...")

    if not run_command("python setup_mysql.py", "Setting up MySQL database"):
        print("[WARNING] Database setup failed, but continuing...")
        print("You may need to run this manually after deployment")

    return True

def create_startup_script():
    """Create a startup script for the application"""
    print("Creating startup script...")

    startup_script = '''#!/bin/bash
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
'''

    with open('start.sh', 'w') as f:
        f.write(startup_script)

    # Make it executable
    os.chmod('start.sh', 0o755)
    print("[OK] Created start.sh script")

    return True

def create_htaccess():
    """Create .htaccess file for Apache"""
    print("Creating .htaccess file...")

    htaccess_content = '''# Service PRO .htaccess for Railway
# Place this file in your public_html or web root directory

<IfModule mod_rewrite.c>
    RewriteEngine On

    # Handle Railway deployment (reverse proxy)
    RewriteRule ^(.*)$ http://127.0.0.1:5000/$1 [P,L]

    # Security headers
    <IfModule mod_headers.c>
        Header always set X-Content-Type-Options nosniff
        Header always set X-Frame-Options SAMEORIGIN
        Header always set X-XSS-Protection "1; mode=block"
        Header always set Referrer-Policy "strict-origin-when-cross-origin"
    </IfModule>

    # Force HTTPS if available
    RewriteCond %{HTTPS} off
    RewriteRule ^(.*)$ https://%{HTTP_HOST}%{REQUEST_URI} [L,R=301]

    # Handle Flask routes
    RewriteRule ^api/(.*)$ http://127.0.0.1:5000/api/$1 [P,L]
    RewriteRule ^(.*)$ http://127.0.0.1:5000/$1 [P,L]

</IfModule>

# Prevent access to sensitive files
<Files "*.py">
    Order allow,deny
    Deny from all
</Files>

<Files ".env*">
    Order allow,deny
    Deny from all
</Files>

<Files "*.log">
    Order allow,deny
    Deny from all
</Files>
'''

    with open('.htaccess', 'w') as f:
        f.write(htaccess_content)

    print("[OK] Created .htaccess file")
    return True

def main():
    """Main deployment function"""
    print("Starting Service PRO deployment for Railway...")
    print("=" * 60)

    if not check_requirements():
        print("[ERROR] Deployment requirements not met. Please fix the issues above.")
        sys.exit(1)

    steps = [
        ("Installing dependencies", install_dependencies),
        ("Setting up directories", setup_directories),
        ("Compiling translations", compile_translations),
        ("Setting up database", setup_database),
        ("Creating startup script", create_startup_script),
        ("Creating .htaccess file", create_htaccess),
    ]

    success = True
    for description, step_function in steps:
        if not step_function():
            success = False
            break

    if success:
        print("=" * 60)
        print("Deployment preparation completed successfully!")
        print("\nNext steps:")
        print("1. Connect your project to Railway")
        print("2. Railway will automatically set up PostgreSQL database")
        print("3. Add environment variables in Railway dashboard")
        print("4. Railway automatically handles SSL and domain")
        print("5. Your app will be available at: https://your-app.railway.app")
        print("\nFor support, check the README_railway.md file")
    else:
        print("=" * 60)
        print("[ERROR] Deployment preparation failed!")
        print("Please fix the issues above and try again.")
        sys.exit(1)

if __name__ == '__main__':
    main()