#!/usr/bin/env python3
from app import app, db, User, Service, ADMIN
import os

# Try different database paths
db_paths = [
    'instance/service_app.db',
    'service_app.db',
    'data/service_app.db'
]

for db_path in db_paths:
    print(f"Trying database path: {db_path}")
    try:
        # Update the config
        app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{db_path}'

        with app.app_context():
            # Ensure directory exists
            os.makedirs(os.path.dirname(db_path), exist_ok=True)

            db.create_all()
            print(f"Database created successfully at: {db_path}")

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
                Service(name='House Cleaning', description='Complete house cleaning service', price=120.0, duration_hours=4, category='Cleaning')
            ]

            for service in services:
                db.session.add(service)

            db.session.commit()
            print("Admin user and sample services created!")

            # Test the database
            users = User.query.count()
            services_count = Service.query.count()
            print(f"Database test: {users} users, {services_count} services")

            print(f"SUCCESS: Database working at {db_path}")
            break

    except Exception as e:
        print(f"Failed with {db_path}: {e}")
        continue
else:
    print("All database paths failed!")