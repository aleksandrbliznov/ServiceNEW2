#!/usr/bin/env python3
"""
Force database reset script for Service PRO
Completely removes old database and creates new one with correct schema
"""

import os
import sys
from app import app, db

def force_reset_database():
    """Force reset the database"""
    print("Force resetting Service PRO database...")

    # Stop the Flask app if it's running by removing the database file
    db_path = 'instance/service_app.db'
    if os.path.exists(db_path):
        try:
            # Try multiple times to remove the file (in case of locks)
            import time
            for i in range(5):
                try:
                    os.remove(db_path)
                    print(f"Removed old database: {db_path}")
                    break
                except PermissionError:
                    if i < 4:
                        print(f"Database file locked, retrying in 1 second... (attempt {i+1}/5)")
                        time.sleep(1)
                        continue
                    else:
                        print("Could not remove database file after 5 attempts")
                        print("Please manually stop any running Flask processes and try again")
                        return False
        except Exception as e:
            print(f"Could not remove database: {e}")
            return False

    # Create new database with updated schema
    try:
        with app.app_context():
            db.create_all()
            print("Created new database with updated schema")
            return True
    except Exception as e:
        print(f"Error creating database: {e}")
        return False

if __name__ == '__main__':
    success = force_reset_database()
    if success:
        print("\nDatabase reset successful!")
        print("You can now run: python app.py")
    else:
        print("\nDatabase reset failed!")
        sys.exit(1)