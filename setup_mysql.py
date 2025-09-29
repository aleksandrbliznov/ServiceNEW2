#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
MySQL Database Setup Script for Service PRO
Compatible with Python 3.6+ on Radicenter hosting
"""

import os
import sys
from dotenv import load_dotenv

# Load environment variables FIRST
load_dotenv('.env.production')

# Configure database for Python 3 BEFORE any other imports
db_uri = os.getenv('SQLALCHEMY_DATABASE_URI', 'sqlite:///instance/service_app.db')
if db_uri.startswith('mysql'):
    try:
        import PyMySQL  # Python 3 MySQL driver
        os.environ['SQLALCHEMY_MYSQL_NO_MYSQLDB'] = '1'
        print("[OK] Configured SQLAlchemy to use PyMySQL for MySQL")
    except ImportError:
        print("WARNING: PyMySQL not found, install with: pip install PyMySQL")
        print("  Falling back to SQLite for setup...")
        # Switch to SQLite for setup when PyMySQL is not available
        os.environ['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///setup_temp.db'
        print("[OK] Using temporary SQLite database for setup")
else:
    print("[OK] Using SQLite for development setup")

# Now import Flask app components after MySQL configuration
from app import app, db

def setup_database():
    """Set up database for production"""
    try:
        # Check database type
        db_uri = os.getenv('SQLALCHEMY_DATABASE_URI', '')
        if db_uri.startswith('mysql'):
            print("[OK] Setting up MySQL database with PyMySQL")
        else:
            print("[OK] Setting up SQLite database for development")

        with app.app_context():
            print("Setting up MySQL database...")

            # Create all tables
            db.create_all()

            print("[OK] Database tables created successfully!")

            # Create initial service groups if they don't exist
            from app import ServiceGroup

            groups_data = [
                {
                    'name': 'Kondiiter',
                    'name_et': 'Kondiiter',
                    'name_en': 'Confectioner',
                    'name_ru': 'Кондитер',
                    'description': 'Cake making, baking, and confectionery services'
                },
                {
                    'name': 'Ehitus',
                    'name_et': 'Ehitus',
                    'name_en': 'Construction',
                    'name_ru': 'Строительство',
                    'description': 'Construction, renovation, and building services'
                },
                {
                    'name': 'Koristus',
                    'name_et': 'Koristus',
                    'name_en': 'Cleaning',
                    'name_ru': 'Уборка',
                    'description': 'Cleaning services for homes and offices'
                },
                {
                    'name': 'IT abi',
                    'name_et': 'IT abi',
                    'name_en': 'IT Support',
                    'name_ru': 'IT поддержка',
                    'description': 'Computer repair, software installation, and IT support'
                }
            ]

            for group_data in groups_data:
                existing_group = ServiceGroup.query.filter_by(name=group_data['name']).first()
                if not existing_group:
                    group = ServiceGroup(**group_data)
                    db.session.add(group)
                    print(f"[OK] Created service group: {group_data['name']}")

            # Create admin user if it doesn't exist
            from app import User

            admin_email = os.getenv('ADMIN_EMAIL', 'admin@asbg.ee')
            existing_admin = User.query.filter_by(email=admin_email).first()

            if not existing_admin:
                admin = User(
                    username='admin',
                    email=admin_email,
                    first_name='Admin',
                    last_name='User',
                    role='admin',
                    is_approved=True
                )
                admin.set_password(os.getenv('ADMIN_PASSWORD', 'admin123'))
                db.session.add(admin)
                print(f"[OK] Created admin user: {admin_email}")
            else:
                print(f"[OK] Admin user already exists: {admin_email}")

            db.session.commit()
            print("[OK] Database setup completed successfully!")

            # Clean up temporary database if used
            if 'setup_temp.db' in os.getenv('SQLALCHEMY_DATABASE_URI', ''):
                try:
                    os.remove('setup_temp.db')
                    print("[OK] Cleaned up temporary database file")
                except:
                    pass

    except Exception as e:
        print(f"[ERROR] Database setup failed: {str(e)}")
        print("This might be due to a locked database file from the development server.")
        print("Try stopping the Flask development server and running the script again.")
        sys.exit(1)

if __name__ == '__main__':
    setup_database()