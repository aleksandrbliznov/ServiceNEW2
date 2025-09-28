#!/usr/bin/env python3
"""
Test script to verify Service PRO application is working correctly
"""

import urllib.request
import urllib.error
import json
from app import app, db, User, Service

def test_homepage():
    """Test if homepage loads correctly"""
    try:
        with app.test_client() as client:
            response = client.get('/')
            if response.status_code == 200:
                print("[PASS] Homepage loads successfully")
                return True
            else:
                print(f"[FAIL] Homepage failed with status {response.status_code}")
                return False
    except Exception as e:
        print(f"[FAIL] Homepage test failed: {e}")
        return False

def test_database():
    """Test database connectivity and sample data"""
    try:
        with app.app_context():
            # Test database connection
            users = User.query.all()
            services = Service.query.all()

            print(f"[PASS] Database connected - {len(users)} users, {len(services)} services")

            # Check for admin user
            admin = User.query.filter_by(username='admin').first()
            if admin:
                print("[PASS] Admin user exists")
            else:
                print("[FAIL] Admin user missing")

            return True
    except Exception as e:
        print(f"[FAIL] Database test failed: {e}")
        return False

def test_login():
    """Test login functionality"""
    try:
        with app.test_client() as client:
            # Test admin login
            response = client.post('/login', data={
                'username': 'admin',
                'password': 'admin123'
            }, follow_redirects=True)

            if response.status_code == 200 and 'admini' in response.get_data(as_text=True).lower():
                print("[PASS] Admin login works")
                return True
            else:
                print(f"[FAIL] Admin login failed - status: {response.status_code}")
                print(f"Response contains: {response.get_data(as_text=True)[:200]}...")
                return False
    except Exception as e:
        print(f"[FAIL] Login test failed: {e}")
        return False

def main():
    """Run all tests"""
    print("Testing Service PRO Application")
    print("=" * 50)

    tests = [
        ("Homepage", test_homepage),
        ("Database", test_database),
        ("Login", test_login)
    ]

    passed = 0
    total = len(tests)

    for test_name, test_func in tests:
        print(f"\nTesting {test_name}...")
        if test_func():
            passed += 1

    print("\n" + "=" * 50)
    print(f"Test Results: {passed}/{total} passed")

    if passed == total:
        print("All tests passed! Application is working correctly.")
        print("\nAccess your application at: http://localhost:5000/")
        print("\nLogin Credentials:")
        print("   Admin: admin/admin123")
        print("   Customer: customer/customer123")
        print("   Handyman: handyman/handyman123")
    else:
        print("Some tests failed. Please check the errors above.")

    return passed == total

if __name__ == '__main__':
    main()