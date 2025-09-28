#!/usr/bin/env python3
"""
Service PRO Setup Script
Initializes the database and creates sample data for testing.
"""

import os
import sys
from datetime import datetime, timedelta
from app import app, db, User, Service, Booking, ADMIN, USER, HANDYMAN

def create_admin_user():
    """Create the default admin user."""
    admin = User.query.filter_by(role=ADMIN).first()
    if not admin:
        admin = User(
            username='admin',
            email='admin@serviceapp.com',
            first_name='System',
            last_name='Administrator',
            phone='+1234567890',
            role=ADMIN,
            is_approved=True
        )
        admin.set_password('admin123')
        db.session.add(admin)
        print("Created admin user (username: admin, password: admin123)")
    else:
        print("Admin user already exists")

def create_sample_services():
    """Create sample services."""
    # First create some service groups if they don't exist
    from app import ServiceGroup

    service_groups_data = [
        {'name': 'Plumbing', 'name_et': 'Torutööd', 'name_en': 'Plumbing', 'name_ru': 'Сантехника', 'description': 'Plumbing services'},
        {'name': 'Electrical', 'name_et': 'Elektritööd', 'name_en': 'Electrical', 'name_ru': 'Электрика', 'description': 'Electrical services'},
        {'name': 'Cleaning', 'name_et': 'Koristus', 'name_en': 'Cleaning', 'name_ru': 'Уборка', 'description': 'Cleaning services'},
        {'name': 'Construction', 'name_et': 'Ehitus', 'name_en': 'Construction', 'name_ru': 'Строительство', 'description': 'Construction services'},
        {'name': 'Gardening', 'name_et': 'Aiatööd', 'name_en': 'Gardening', 'name_ru': 'Садоводство', 'description': 'Gardening services'}
    ]

    for group_data in service_groups_data:
        existing_group = ServiceGroup.query.filter_by(name=group_data['name']).first()
        if not existing_group:
            group = ServiceGroup(**group_data)
            db.session.add(group)

    db.session.commit()

    # Get the admin user to assign services to
    admin = User.query.filter_by(role=ADMIN).first()
    if not admin:
        print("No admin user found, cannot create services")
        return

    services_data = [
        {
            'name': 'Plumbing Repair',
            'description': 'Fix leaks, install fixtures, repair pipes, and other plumbing services. Fast, reliable service for all your plumbing needs.',
            'price': 75.00,
            'duration_hours': 2,
            'category': 'Plumbing',
            'service_group_id': 1,  # Plumbing group
            'handyman_id': admin.id
        },
        {
            'name': 'Electrical Installation',
            'description': 'Install outlets, switches, light fixtures, and electrical repairs. Certified electricians for safe installations.',
            'price': 85.00,
            'duration_hours': 3,
            'category': 'Electrical',
            'service_group_id': 2,  # Electrical group
            'handyman_id': admin.id
        },
        {
            'name': 'House Cleaning',
            'description': 'Complete house cleaning including dusting, vacuuming, and sanitizing. Deep cleaning for a fresh home.',
            'price': 120.00,
            'duration_hours': 4,
            'category': 'Cleaning',
            'service_group_id': 3,  # Cleaning group
            'handyman_id': admin.id
        },
        {
            'name': 'Lawn Mowing',
            'description': 'Professional lawn mowing and garden maintenance services. Keep your lawn looking perfect year-round.',
            'price': 45.00,
            'duration_hours': 1,
            'category': 'Gardening',
            'service_group_id': 5,  # Gardening group
            'handyman_id': admin.id
        },
        {
            'name': 'Painting Service',
            'description': 'Interior and exterior painting for homes and offices. Professional finish with quality paints.',
            'price': 200.00,
            'duration_hours': 6,
            'category': 'Painting',
            'service_group_id': 4,  # Construction group
            'handyman_id': admin.id
        },
        {
            'name': 'HVAC Maintenance',
            'description': 'Heating and cooling system maintenance and repairs. Keep your home comfortable all year.',
            'price': 95.00,
            'duration_hours': 2,
            'category': 'HVAC',
            'service_group_id': 4,  # Construction group
            'handyman_id': admin.id
        }
    ]

    created_count = 0
    for service_data in services_data:
        service = Service.query.filter_by(name=service_data['name']).first()
        if not service:
            service = Service(**service_data)
            db.session.add(service)
            created_count += 1

    if created_count > 0:
        print(f"Created {created_count} sample services")
    else:
        print("Sample services already exist")

def create_sample_users():
    """Create sample users for testing."""
    users_data = [
        {
            'username': 'john_customer',
            'email': 'john@example.com',
            'first_name': 'John',
            'last_name': 'Doe',
            'phone': '+1987654321',
            'role': USER,
            'password': 'customer123'
        },
        {
            'username': 'jane_customer',
            'email': 'jane@example.com',
            'first_name': 'Jane',
            'last_name': 'Smith',
            'phone': '+1555123456',
            'role': USER,
            'password': 'customer123'
        },
        {
            'username': 'mike_handyman',
            'email': 'mike@handyman.com',
            'first_name': 'Mike',
            'last_name': 'Johnson',
            'phone': '+1444333222',
            'role': HANDYMAN,
            'password': 'handyman123',
            'is_approved': True
        },
        {
            'username': 'sarah_handyman',
            'email': 'sarah@handyman.com',
            'first_name': 'Sarah',
            'last_name': 'Williams',
            'phone': '+1777888999',
            'role': HANDYMAN,
            'password': 'handyman123',
            'is_approved': False  # Pending approval
        }
    ]

    created_count = 0
    for user_data in users_data:
        is_approved = user_data.pop('is_approved', True)
        password = user_data.pop('password')  # Remove password from user_data
        user = User.query.filter_by(username=user_data['username']).first()
        if not user:
            user = User(**user_data)
            user.set_password(password)
            user.is_approved = is_approved
            db.session.add(user)
            created_count += 1

    if created_count > 0:
        print(f"Created {created_count} sample users")
    else:
        print("Sample users already exist")

def create_sample_bookings():
    """Create sample bookings for testing."""
    # Get some users and services
    customers = User.query.filter_by(role=USER).limit(2).all()
    handymen = User.query.filter_by(role=HANDYMAN, is_approved=True).all()
    services = Service.query.all()

    if not customers or not handymen or not services:
        print("Warning: Skipping sample bookings - need users, handymen, and services first")
        return

    bookings_data = [
        {
            'user': customers[0],
            'service': services[0],
            'handyman': handymen[0] if handymen else None,
            'booking_date': datetime.utcnow() + timedelta(days=1),
            'status': 'approved',
            'admin_approved': True,
            'total_price': 75.00,
            'special_requests': 'Please fix the kitchen sink leak.'
        },
        {
            'user': customers[1],
            'service': services[1],
            'handyman': None,
            'booking_date': datetime.utcnow() + timedelta(days=2),
            'status': 'pending',
            'admin_approved': False,
            'total_price': 85.00,
            'special_requests': 'Need to install new light fixture in living room.'
        },
        {
            'user': customers[0],
            'service': services[2],
            'handyman': handymen[0] if handymen else None,
            'booking_date': datetime.utcnow() + timedelta(days=3),
            'status': 'completed',
            'admin_approved': True,
            'total_price': 120.00,
            'special_requests': 'Deep cleaning of entire house.'
        }
    ]

    created_count = 0
    for booking_data in bookings_data:
        # Check if similar booking already exists
        existing = Booking.query.filter_by(
            user_id=booking_data['user'].id,
            service_id=booking_data['service'].id,
            booking_date=booking_data['booking_date']
        ).first()

        if not existing:
            booking = Booking(
                user_id=booking_data['user'].id,
                service_id=booking_data['service'].id,
                handyman_id=booking_data['handyman'].id if booking_data['handyman'] else None,
                booking_date=booking_data['booking_date'],
                status=booking_data['status'],
                admin_approved=booking_data['admin_approved'],
                total_price=booking_data['total_price'],
                special_requests=booking_data['special_requests']
            )
            db.session.add(booking)
            created_count += 1

    if created_count > 0:
        print(f"Created {created_count} sample bookings")
    else:
        print("Sample bookings already exist")

def print_summary():
    """Print a summary of created data."""
    print("\n" + "="*50)
    print("SERVICE PRO SETUP COMPLETE")
    print("="*50)

    user_counts = {
        'admin': User.query.filter_by(role=ADMIN).count(),
        'customer': User.query.filter_by(role=USER).count(),
        'handyman': User.query.filter_by(role=HANDYMAN).count(),
        'approved_handyman': User.query.filter_by(role=HANDYMAN, is_approved=True).count(),
        'pending_handyman': User.query.filter_by(role=HANDYMAN, is_approved=False).count()
    }

    print("\nDATA SUMMARY:")
    print(f"   Admins: {user_counts['admin']}")
    print(f"   Customers: {user_counts['customer']}")
    print(f"   Total Handymen: {user_counts['handyman']}")
    print(f"   Approved Handymen: {user_counts['approved_handyman']}")
    print(f"   Pending Handymen: {user_counts['pending_handyman']}")
    print(f"   Services: {Service.query.count()}")
    print(f"   Bookings: {Booking.query.count()}")

    print("\nLOGIN CREDENTIALS:")
    print("   Admin: admin / admin123")
    print("   Customer: john_customer / customer123")
    print("   Customer: jane_customer / customer123")
    print("   Handyman: mike_handyman / handyman123")
    print("   Handyman (pending): sarah_handyman / handyman123")

    print("\nGETTING STARTED:")
    print("   1. Run: python app.py")
    print("   2. Open: http://localhost:5000")
    print("   3. Login with any of the accounts above")
    print("   4. Test the complete workflow!")

    print("\n" + "="*50)

def setup_database():
    """Main setup function."""
    print("Setting up Service PRO database...")

    try:
        # Create all tables
        db.create_all()
        print("Database tables created")

        # Create sample data
        create_admin_user()
        create_sample_services()
        create_sample_users()
        create_sample_bookings()

        # Commit all changes
        db.session.commit()
        print("All data committed to database")

        # Print summary
        print_summary()

    except Exception as e:
        print(f"Error during setup: {str(e)}")
        db.session.rollback()
        sys.exit(1)

if __name__ == '__main__':
    # Set up the Flask application context
    with app.app_context():
        setup_database()