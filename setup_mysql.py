#!/usr/bin/env python3
"""
MySQL Database Setup Script for Service PRO
Compatible with Python 3.6+ on Radicenter hosting
"""

import os
import sys
from dotenv import load_dotenv
from app import app, db

# Load environment variables
load_dotenv('.env.production')

def setup_database():
    """Set up MySQL database for production"""
    try:
        with app.app_context():
            print("Setting up MySQL database...")

            # Create all tables
            db.create_all()

            print("✓ Database tables created successfully!")

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
                    print(f"✓ Created service group: {group_data['name']}")

            # Create admin user if it doesn't exist
            from app import User

            admin_email = os.getenv('ADMIN_EMAIL', 'admin@lexanco.eu')
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
                print(f"✓ Created admin user: {admin_email}")
            else:
                print(f"✓ Admin user already exists: {admin_email}")

            db.session.commit()
            print("✓ Database setup completed successfully!")

    except Exception as e:
        print(f"✗ Database setup failed: {str(e)}")
        sys.exit(1)

if __name__ == '__main__':
    setup_database()