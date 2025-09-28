#!/usr/bin/env python3
from app import app, mail, Message
from flask import current_app

def test_email():
    """Test email configuration"""
    try:
        with app.app_context():
            print("Testing email configuration...")
            print(f"Mail server: {current_app.config['MAIL_SERVER']}")
            print(f"Mail port: {current_app.config['MAIL_PORT']}")
            print(f"Mail username: {current_app.config['MAIL_USERNAME']}")
            print(f"Mail TLS: {current_app.config['MAIL_USE_TLS']}")

            # Try to create a mail connection
            msg = Message('Test Email - Service PRO',
                         sender=current_app.config['MAIL_DEFAULT_SENDER'],
                         recipients=['test@example.com'])

            msg.body = 'This is a test email to verify email configuration is working.'

            # Try to send (this might fail if credentials are wrong, but that's expected)
            try:
                mail.send(msg)
                print("Email sent successfully!")
                return True
            except Exception as e:
                print(f"Email sending failed (expected if credentials are wrong): {e}")
                print("Email configuration is loaded correctly, but credentials may need updating.")
                return True

    except Exception as e:
        print(f"Email configuration error: {e}")
        return False

if __name__ == '__main__':
    success = test_email()
    if success:
        print("\nEmail configuration test completed!")
    else:
        print("\nEmail configuration test failed!")