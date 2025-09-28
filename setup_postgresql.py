#!/usr/bin/env python3
"""
PostgreSQL setup script for Service PRO
Creates database and tables with sample data
"""

import os
import sys
from app import app, db, User, Service, ADMIN
from flask import current_app

def setup_postgresql():
    """Setup PostgreSQL database"""
    print("Setting up PostgreSQL database for Service PRO...")

    # Get database URL from environment
    db_url = os.getenv('SQLALCHEMY_DATABASE_URI')

    if not db_url or 'postgresql' not in db_url:
        print("Error: PostgreSQL not configured in environment variables")
        print("Please set SQLALCHEMY_DATABASE_URI to a PostgreSQL connection string")
        return False

    try:
        with app.app_context():
            # Create all tables
            db.create_all()
            print("Created database tables")

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
                Service(name='Electrical Work', description='Electrical installation and repair', price=85.0, duration_hours=3, category='Electrical'),
                Service(name='House Cleaning', description='Complete house cleaning service', price=120.0, duration_hours=4, category='Cleaning'),
                Service(name='Garden Maintenance', description='Garden maintenance and landscaping', price=60.0, duration_hours=2, category='Gardening'),
                Service(name='Painting', description='Interior and exterior painting', price=200.0, duration_hours=6, category='Painting'),
                Service(name='Carpentry', description='Custom carpentry and woodwork', price=90.0, duration_hours=4, category='Carpentry')
            ]

            for service in services:
                db.session.add(service)

            db.session.commit()
            print("Created admin user and sample services")

            # Verify setup
            user_count = User.query.count()
            service_count = Service.query.count()
            print(f"Setup complete: {user_count} users, {service_count} services")

        return True

    except Exception as e:
        print(f"Error setting up PostgreSQL: {e}")
        return False

if __name__ == '__main__':
    success = setup_postgresql()
    if success:
        print("\nPostgreSQL setup successful!")
        print("You can now run: python app.py")
    else:
        print("\nPostgreSQL setup failed!")
        sys.exit(1)