#!/usr/bin/env python3
"""
Test script to verify Estonian translations are working
"""

from app import app, babel, gettext
from flask import request

def test_translations():
    """Test if Estonian translations are working"""
    with app.test_request_context():
        # Test some common translations
        test_strings = [
            'Welcome back',
            'Manage your bookings and service requests',
            'Total Bookings',
            'Pending',
            'Confirmed',
            'Completed',
            'My Bookings',
            'Quick Actions',
            'Browse All Services',
            'No bookings yet',
            'You haven\'t made any service bookings yet.',
            'Browse Services'
        ]

        print("Testing Estonian translations:")
        print("=" * 50)

        for test_string in test_strings:
            try:
                translated = gettext(test_string)
                if translated != test_string:
                    print(f"[OK] '{test_string}' -> '{translated}'")
                else:
                    print(f"[NO TRANS] '{test_string}' -> (no translation found)")
            except Exception as e:
                print(f"[ERROR] '{test_string}' -> Error: {e}")

        print("=" * 50)
        print("Translation test completed!")

if __name__ == '__main__':
    test_translations()