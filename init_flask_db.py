#!/usr/bin/env python3
"""
Initialize Flask database properly
"""

from app import app, db, User, Service, ADMIN

def init_flask_database():
    """Initialize database using Flask-SQLAlchemy"""
    print("Initializing Flask database...")

    with app.app_context():
        try:
            # Create all tables
            db.create_all()
            print("Database tables created successfully")

            # Check if admin already exists
            existing_admin = User.query.filter_by(username='admin').first()
            if existing_admin:
                print("Admin user already exists")
                return True

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
                Service(name='Plumbing Repair', description='Professional plumbing repair services', price=75.0, duration_hours=2, category='Plumbing', is_active=True),
                Service(name='Electrical Work', description='Electrical installation and repair', price=85.0, duration_hours=3, category='Electrical', is_active=True),
                Service(name='House Cleaning', description='Complete house cleaning service', price=120.0, duration_hours=4, category='Cleaning', is_active=True),
                Service(name='Garden Maintenance', description='Garden maintenance and landscaping', price=60.0, duration_hours=2, category='Gardening', is_active=True),
                Service(name='Painting', description='Interior and exterior painting', price=200.0, duration_hours=6, category='Painting', is_active=True),
                Service(name='Carpentry', description='Custom carpentry and woodwork', price=90.0, duration_hours=4, category='Carpentry', is_active=True)
            ]

            for service in services:
                db.session.add(service)

            db.session.commit()
            print("Admin user and sample services created")

            # Verify
            user_count = User.query.count()
            service_count = Service.query.count()
            print(f"Database ready: {user_count} users, {service_count} services")

            return True

        except Exception as e:
            print(f"Error initializing database: {e}")
            return False

if __name__ == '__main__':
    success = init_flask_database()
    if success:
        print("\nFlask database initialization successful!")
    else:
        print("\nFlask database initialization failed!")