#!/usr/bin/env python3
"""
Debug admin login issue
"""

from app import app, db, User

def debug_login():
    """Debug the login process"""
    with app.test_client() as client:
        print("Debugging admin login...")

        # Check if admin user exists and get details
        with app.app_context():
            admin = User.query.filter_by(username='admin').first()
            if admin:
                print(f"Admin user found: {admin.username}")
                print(f"Admin role: {admin.role}")
                print(f"Admin email: {admin.email}")
                print(f"Admin approved: {admin.is_approved}")
            else:
                print("Admin user NOT found!")
                return

        # Try login
        response = client.post('/login', data={
            'username': 'admin',
            'password': 'admin123'
        }, follow_redirects=True)

        print(f"Login response status: {response.status_code}")
        print("Response contains 'admini':", 'admini' in response.get_data(as_text=True).lower())
        print("Response contains 'töölaud':", 'töölaud' in response.get_data(as_text=True).lower())

        # Print first 500 characters of response
        response_text = response.get_data(as_text=True)
        print("Response preview:")
        print(response_text[:500] + "..." if len(response_text) > 500 else response_text)

if __name__ == '__main__':
    debug_login()