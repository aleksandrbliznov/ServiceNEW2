#!/usr/bin/env python3
"""
Database fix script for Service PRO
Removes old database and creates new one with updated schema
"""

import os
import sys
from app import app, db, User, ADMIN

def fix_database():
    """Fix the database schema"""
    print("Fixing Service PRO database...")

    # Remove old database file
    db_path = 'instance/service_app.db'
    if os.path.exists(db_path):
        try:
            os.remove(db_path)
            print(f"Removed old database: {db_path}")
        except Exception as e:
            print(f"Could not remove database: {e}")
            return False
    else:
        print("No existing database found")

    # Create new database with updated schema
    try:
        with app.app_context():
            db.create_all()
            print("Created new database with updated schema")

            # Create admin user
            admin = User(
                username='admin',
                email='admin@example.com',
                first_name='Admin',
                last_name='User',
                role=ADMIN,
                is_approved=True
            )
            admin.set_password('admin123')
            db.session.add(admin)
            db.session.commit()
            print("Created default admin user (admin/admin123)")

        return True
    except Exception as e:
        print(f"Error creating database: {e}")
        return False

if __name__ == '__main__':
    success = fix_database()
    if success:
        print("\nDatabase fix successful!")
        print("You can now run: python app.py")
    else:
        print("\nDatabase fix failed!")
        sys.exit(1)