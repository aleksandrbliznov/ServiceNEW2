#!/usr/bin/env python3
"""
Database Schema Fix Script
This script will properly recreate the database with all required columns.
"""

import os
import sys
from app import app, db, ServiceGroup, User, ADMIN

def fix_database_schema():
    """Fix database schema by recreating with proper structure"""
    with app.app_context():
        try:
            print("Creating database with proper schema...")

            # Drop all tables if they exist
            db.drop_all()

            # Create all tables with correct schema
            db.create_all()

            print("Database tables created successfully!")

            # Create admin user
            try:
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
                print('Admin user created! Username: admin, Password: admin123')
            except Exception as e:
                print(f'Error creating admin user: {e}')

            # Create initial service groups
            try:
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
                    group = ServiceGroup(**group_data)
                    db.session.add(group)
                    print(f'Created service group: {group_data["name"]}')

                db.session.commit()
                print('Initial service groups created successfully!')
            except Exception as e:
                print(f'Error creating service groups: {e}')

            print("Database schema fixed successfully!")
            return True

        except Exception as e:
            print(f"Error fixing database schema: {e}")
            return False

if __name__ == '__main__':
    success = fix_database_schema()
    sys.exit(0 if success else 1)