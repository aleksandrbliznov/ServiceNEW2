#!/usr/bin/env python3
"""
Debug admin user and login issues
"""

from app import app, db, User
from werkzeug.security import generate_password_hash, check_password_hash

def debug_admin_user():
    """Debug admin user creation and login"""
    with app.app_context():
        print("Debugging admin user...")

        # Check if admin user exists
        admin = User.query.filter_by(username='admin').first()
        if admin:
            print(f"Admin user found: {admin.username}")
            print(f"Admin email: {admin.email}")
            print(f"Admin role: {admin.role}")
            print(f"Admin approved: {admin.is_approved}")
            print(f"Password hash: {admin.password_hash[:20]}...")

            # Test password check
            test_password = 'admin123'
            if admin.check_password(test_password):
                print(f"Password check successful for '{test_password}'")
            else:
                print(f"Password check failed for '{test_password}'")

                # Let's check what the actual password should be
                print("Recreating admin user with correct password...")
                admin.set_password('admin123')
                db.session.commit()
                print("Admin password reset to 'admin123'")

        else:
            print("Admin user NOT found! Creating...")
            admin = User(
                username='admin',
                email='aleksandr@asbg.ee',
                first_name='Admin',
                last_name='User',
                role='admin',
                is_approved=True
            )
            admin.set_password('admin123')
            db.session.add(admin)
            db.session.commit()
            print("Admin user created successfully!")

        # Test login process
        print("\nTesting login process...")
        with app.test_client() as client:
            # Try login with form data
            response = client.post('/login', data={
                'username': 'admin',
                'password': 'admin123'
            }, follow_redirects=True)

            print(f"Login response status: {response.status_code}")

            # Check response content
            response_text = response.get_data(as_text=True)
            print(f"Response contains 'Invalid': {'Invalid' in response_text}")
            print(f"Response contains 'admin': {'admin' in response_text.lower()}")
            print(f"Response contains 'dashboard': {'dashboard' in response_text.lower()}")

            # Print first 300 characters
            print("Response preview:")
            print(response_text[:300])

if __name__ == '__main__':
    debug_admin_user()