#!/usr/bin/env python3
"""
Emergency database reset script for Service PRO
Handles locked database files and recreates the database
"""

import os
import sys
import time
from app import app, db, User, Service, ADMIN

def emergency_reset_database():
    """Emergency reset the database"""
    print("Emergency database reset for Service PRO...")

    # Try multiple times to delete the database file
    db_path = 'instance/service_app.db'
    max_attempts = 5

    for attempt in range(max_attempts):
        if os.path.exists(db_path):
            try:
                os.remove(db_path)
                print(f"Removed old database: {db_path}")
                break
            except Exception as e:
                print(f"Attempt {attempt + 1}: Could not remove database: {e}")
                if attempt < max_attempts - 1:
                    print("Waiting 2 seconds before retry...")
                    time.sleep(2)
                else:
                    print("Failed to remove database after multiple attempts")
                    return False
        else:
            print("No existing database found")
            break

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

            # Create sample services
            services = [
                Service(name='Plumbing Repair', description='Professional plumbing repair services', price=75.0, duration_hours=2, category='Plumbing'),
                Service(name='Electrical Installation', description='Electrical installation and repair', price=85.0, duration_hours=3, category='Electrical'),
                Service(name='House Cleaning', description='Complete house cleaning service', price=120.0, duration_hours=4, category='Cleaning'),
                Service(name='Garden Maintenance', description='Garden maintenance and landscaping', price=60.0, duration_hours=2, category='Gardening'),
                Service(name='Painting Services', description='Interior and exterior painting', price=200.0, duration_hours=6, category='Painting'),
                Service(name='Carpentry Work', description='Custom carpentry and woodwork', price=90.0, duration_hours=4, category='Carpentry')
            ]

            for service in services:
                db.session.add(service)

            db.session.commit()
            print("Created default admin user (admin/admin123)")
            print("Created 6 sample services")

        return True
    except Exception as e:
        print(f"Error creating database: {e}")
        return False

if __name__ == '__main__':
    success = emergency_reset_database()
    if success:
        print("\nDatabase reset successful!")
        print("You can now run: python app.py")
    else:
        print("\nDatabase reset failed!")
        sys.exit(1)