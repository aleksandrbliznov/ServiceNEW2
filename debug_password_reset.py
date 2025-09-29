#!/usr/bin/env python3
"""
Debug password reset functionality
"""

from app import app, db, User

def debug_password_reset():
    """Debug the password reset process"""
    with app.app_context():
        print("Debugging password reset functionality...")

        # Get admin user
        user = User.query.filter_by(email='aleksandr@asbg.ee').first()
        if not user:
            print("Admin user not found!")
            return

        print(f"User found: {user.email}")

        # Generate reset token manually
        token = user.generate_reset_token()
        print(f"Generated token: {token[:20]}...")

        # Commit to database
        db.session.commit()
        print("Token saved to database")

        # Check if token exists
        user_check = User.query.filter_by(email='aleksandr@asbg.ee').first()
        if user_check.reset_token:
            print(f"Token verified in database: {user_check.reset_token[:20]}...")

            # Test token verification
            if user_check.verify_reset_token(token):
                print("Token verification successful")

                # Test password change
                old_password_hash = user_check.password_hash
                user_check.set_password('newpassword123')
                user_check.clear_reset_token()
                db.session.commit()
                print("Password changed and token cleared")

                # Verify new password
                if user_check.check_password('newpassword123'):
                    print("New password verification successful")
                else:
                    print("New password verification failed")

            else:
                print("Token verification failed")
        else:
            print("Token not found in database")

if __name__ == '__main__':
    debug_password_reset()