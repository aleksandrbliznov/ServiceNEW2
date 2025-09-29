#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Simple monitoring script for Service PRO on Radicenter
Checks application health and sends alerts if needed
Python 3.6+ compatible
"""

import os
import sys
import requests
import time
from datetime import datetime
from dotenv import load_dotenv

# Load environment variables
load_dotenv('.env')

def check_application_health():
    """Check if the application is running and responding"""
    try:
        # Check if the Flask app is responding
        response = requests.get('http://127.0.0.1:5000/', timeout=10)
        return response.status_code == 200
    except requests.exceptions.RequestException:
        return False

def check_database_connection():
    """Check database connectivity"""
    try:
        from app import db
        # Simple query to test connection
        db.engine.execute("SELECT 1")
        return True
    except Exception:
        return False

def log_status(message, level='INFO'):
    """Log status to file and console"""
    timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    log_message = f"[{timestamp}] {level}: {message}"

    print(log_message)

    # Append to log file
    with open('logs/monitor.log', 'a') as f:
        f.write(log_message + '\n')

def main():
    """Main monitoring function"""
    print("🔍 Starting Service PRO monitoring...")

    checks = [
        ("Application Health", check_application_health),
        ("Database Connection", check_database_connection),
    ]

    all_healthy = True

    for check_name, check_function in checks:
        try:
            result = check_function()
            if result:
                log_status(f"{check_name}: ✓ OK")
            else:
                log_status(f"{check_name}: ✗ FAILED", "ERROR")
                all_healthy = False
        except Exception as e:
            log_status(f"{check_name}: ✗ ERROR - {str(e)}", "ERROR")
            all_healthy = False

    if all_healthy:
        log_status("All systems operational ✓")
        return True
    else:
        log_status("Some systems reporting issues ✗", "WARNING")
        return False

if __name__ == '__main__':
    try:
        success = main()
        sys.exit(0 if success else 1)
    except KeyboardInterrupt:
        print("\nMonitoring stopped by user")
        sys.exit(0)
    except Exception as e:
        log_status(f"Monitoring script error: {str(e)}", "ERROR")
        sys.exit(1)