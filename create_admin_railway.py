#!/usr/bin/env python3
"""
Create admin user for deployed Railway application
Run this script in Railway console or deploy temporarily to create admin user
"""

import os
import sys
from app import app, db, User, ADMIN

def create_admin_user():
    """Create admin user in deployed database"""
    try:
        with app.app_context():
            print("Checking for existing admin user...")

            # Check if admin already exists
            existing_admin = User.query.filter_by(role=ADMIN).first()

            if existing_admin:
                print(f"Admin user already exists: {existing_admin.username}")
                print(f"Email: {existing_admin.email}")
                print("Admin user is ready to use!")
                return True

            # Create new admin user
            print("Creating new admin user...")
            admin = User(
                username='admin',
                email='aleksandr@asbg.ee',
                first_name='Admin',
                last_name='User',
                role=ADMIN,
                is_approved=True
            )
            admin.set_password('admin123')
            db.session.add(admin)
            db.session.commit()

            print("✅ Admin user created successfully!")
            print("Username: admin")
            print("Password: admin123")
            print("Email: aleksandr@asbg.ee")
            print("\nYou can now login at: https://servicenew2-production.up.railway.app/login")

            return True

    except Exception as e:
        print(f"❌ Error creating admin user: {str(e)}")
        return False

if __name__ == '__main__':
    print("🚀 Creating admin user for Service PRO...")
    success = create_admin_user()
    if not success:
        sys.exit(1)