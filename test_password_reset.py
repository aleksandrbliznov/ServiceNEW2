#!/usr/bin/env python3
"""
Test password reset functionality
"""

from app import app, db, User
import os

def test_password_reset():
    """Test the password reset process"""
    with app.test_client() as client:
        print("Testing password reset functionality...")

        # Test password reset request
        response = client.post('/password-reset-request', data={
            'email': 'aleksandr@asbg.ee'
        }, follow_redirects=True)

        print(f"Password reset request status: {response.status_code}")

        if response.status_code == 200:
            print("OK: Password reset request submitted successfully")

            # Check if user has reset token
            with app.app_context():
                user = User.query.filter_by(email='aleksandr@asbg.ee').first()
                if user and user.reset_token:
                    print(f"OK: Reset token generated: {user.reset_token[:20]}...")

                    # Test password reset form
                    reset_response = client.post(f'/password-reset/{user.reset_token}', data={
                        'password': 'newpassword123',
                        'confirm_password': 'newpassword123'
                    }, follow_redirects=True)

                    print(f"Password reset form status: {reset_response.status_code}")

                    if reset_response.status_code == 200:
                        print("OK: Password reset completed successfully")

                        # Verify password was changed
                        if user.check_password('newpassword123'):
                            print("OK: New password verified successfully")
                        else:
                            print("ERROR: Password verification failed")
                    else:
                        print("ERROR: Password reset form failed")
                        print("Response:", reset_response.get_data(as_text=True)[:200])
                else:
                    print("ERROR: No reset token found")
        else:
            print("✗ Password reset request failed")
            print("Response:", response.get_data(as_text=True)[:200])

if __name__ == '__main__':
    test_password_reset()