#!/usr/bin/env python3
"""
Detailed login debugging
"""

from app import app, db, User
from werkzeug.security import check_password_hash

def debug_login_detailed():
    """Debug login in detail"""
    with app.test_client() as client:
        print("Detailed login debugging...")

        # Check admin user password hash
        with app.app_context():
            admin = User.query.filter_by(username='admin').first()
            if admin:
                print(f"Admin password hash: {admin.password_hash}")
                print(f"Test password 'admin123' matches: {check_password_hash(admin.password_hash, 'admin123')}")

                # Try to authenticate manually
                if check_password_hash(admin.password_hash, 'admin123'):
                    print("Manual password check: PASSED")
                else:
                    print("Manual password check: FAILED")
            else:
                print("Admin user not found")
                return

        # Try login and capture flash messages
        # First get the login page to extract CSRF token
        login_page = client.get('/login')
        csrf_token = None

        # Simple way to extract CSRF token (this is a basic approach)
        # In a real scenario, you might need more sophisticated parsing
        import re
        csrf_match = re.search(r'name="csrf_token" value="([^"]+)"', login_page.get_data(as_text=True))
        if csrf_match:
            csrf_token = csrf_match.group(1)

        login_data = {
            'username': 'admin',
            'password': 'admin123',
            'submit': 'Login'
        }

        if csrf_token:
            login_data['csrf_token'] = csrf_token

        response = client.post('/login', data=login_data, follow_redirects=True)

        print(f"Login response status: {response.status_code}")

        # Check for flash messages in response
        response_text = response.get_data(as_text=True)
        print("Contains 'Invalid username':", 'Invalid username' in response_text)
        print("Contains 'Login failed':", 'Login failed' in response_text)
        print("Contains 'Sisselogimine õnnestus':", 'Sisselogimine õnnestus' in response_text)

        # Check if redirected to admin dashboard
        print("Redirected to admin dashboard:", '/admin/dashboard' in response_text or 'admini' in response_text.lower())

if __name__ == '__main__':
    debug_login_detailed()