#!/usr/bin/env python3
"""
Comprehensive User Flow Testing Script
Tests all major user journeys in Service PRO
"""

import requests
import json
import time
from datetime import datetime, timedelta

class ServicePROTester:
    def __init__(self, base_url='http://localhost:5000'):
        self.base_url = base_url
        self.session = requests.Session()
        self.test_results = []

    def log_test(self, test_name, success, details=""):
        """Log test results"""
        result = {
            'test': test_name,
            'success': success,
            'timestamp': datetime.now().isoformat(),
            'details': details
        }
        self.test_results.append(result)
        status = "PASS" if success else "FAIL"
        print(f"{status}: {test_name}")
        if details:
            print(f"      {details}")

    def test_api_endpoints(self):
        """Test all API endpoints"""
        print("\nTesting API Endpoints...")

        # Test service groups endpoint
        try:
            response = self.session.get(f'{self.base_url}/api/service-groups')
            if response.status_code == 200:
                data = response.json()
                if data.get('success'):
                    groups = data.get('data', [])
                    self.log_test("Service Groups API", True, f"Found {len(groups)} service groups")
                else:
                    self.log_test("Service Groups API", False, "API returned success=false")
            else:
                self.log_test("Service Groups API", False, f"Status code: {response.status_code}")
        except Exception as e:
            self.log_test("Service Groups API", False, str(e))

        # Test services endpoint
        try:
            response = self.session.get(f'{self.base_url}/api/services')
            if response.status_code == 200:
                data = response.json()
                if data.get('success'):
                    services = data.get('data', [])
                    self.log_test("Services API", True, f"Found {len(services)} services")
                else:
                    self.log_test("Services API", False, "API returned success=false")
            else:
                self.log_test("Services API", False, f"Status code: {response.status_code}")
        except Exception as e:
            self.log_test("Services API", False, str(e))

    def test_homepage_loading(self):
        """Test homepage loads correctly"""
        print("\nTesting Homepage...")

        try:
            response = self.session.get(f'{self.base_url}/')
            if response.status_code == 200:
                content = response.text
                if 'Service PRO' in content:
                    self.log_test("Homepage Loading", True, "Homepage loads successfully")
                else:
                    self.log_test("Homepage Loading", False, "Service PRO branding not found")
            else:
                self.log_test("Homepage Loading", False, f"Status code: {response.status_code}")
        except Exception as e:
            self.log_test("Homepage Loading", False, str(e))

    def test_user_registration(self):
        """Test user registration process"""
        print("\nTesting User Registration...")

        try:
            # Test registration page loads
            response = self.session.get(f'{self.base_url}/register')
            if response.status_code == 200:
                self.log_test("Registration Page", True, "Registration form loads successfully")
            else:
                self.log_test("Registration Page", False, f"Status code: {response.status_code}")
                return

            # Note: Actual form submission would require CSRF tokens and proper form handling
            # This is a basic accessibility test
            content = response.text
            if 'first_name' in content and 'email' in content:
                self.log_test("Registration Form Fields", True, "Required form fields present")
            else:
                self.log_test("Registration Form Fields", False, "Missing required form fields")

        except Exception as e:
            self.log_test("User Registration", False, str(e))

    def test_database_connectivity(self):
        """Test database operations"""
        print("\nTesting Database Connectivity...")

        try:
            # Test via API
            response = self.session.get(f'{self.base_url}/api/services')
            if response.status_code == 200:
                data = response.json()
                if data.get('success'):
                    services = data.get('data', [])
                    self.log_test("Database Read", True, f"Successfully read {len(services)} services")

                    # Check service structure
                    if services:
                        service = services[0]
                        required_fields = ['id', 'name', 'price', 'handyman']
                        if all(field in service for field in required_fields):
                            self.log_test("Service Data Structure", True, "Service has all required fields")
                        else:
                            self.log_test("Service Data Structure", False, "Missing required service fields")
                else:
                    self.log_test("Database Read", False, "API returned success=false")
            else:
                self.log_test("Database Read", False, f"Status code: {response.status_code}")
        except Exception as e:
            self.log_test("Database Connectivity", False, str(e))

    def test_responsive_features(self):
        """Test responsive design elements"""
        print("\nTesting Responsive Features...")

        try:
            response = self.session.get(f'{self.base_url}/')
            if response.status_code == 200:
                content = response.text

                # Check for responsive meta tag
                if 'viewport' in content.lower():
                    self.log_test("Responsive Meta Tag", True, "Viewport meta tag found")
                else:
                    self.log_test("Responsive Meta Tag", False, "Missing viewport meta tag")

                # Check for Bootstrap (responsive framework)
                if 'bootstrap' in content.lower():
                    self.log_test("Bootstrap Framework", True, "Bootstrap CSS framework detected")
                else:
                    self.log_test("Bootstrap Framework", False, "Bootstrap not detected")

            else:
                self.log_test("Responsive Features", False, f"Status code: {response.status_code}")
        except Exception as e:
            self.log_test("Responsive Features", False, str(e))

    def test_security_headers(self):
        """Test security headers"""
        print("\nTesting Security Headers...")

        try:
            response = self.session.get(f'{self.base_url}/')
            headers = response.headers

            security_headers = {
                'X-Content-Type-Options': 'nosniff',
                'X-Frame-Options': 'SAMEORIGIN',
                'X-XSS-Protection': '1; mode=block'
            }

            all_present = True
            for header, expected_value in security_headers.items():
                if header in headers:
                    if headers[header] == expected_value:
                        self.log_test(f"Security Header: {header}", True, f"Value: {headers[header]}")
                    else:
                        self.log_test(f"Security Header: {header}", False, f"Expected: {expected_value}, Got: {headers[header]}")
                        all_present = False
                else:
                    self.log_test(f"Security Header: {header}", False, "Header not present")
                    all_present = False

            if all_present:
                self.log_test("Security Headers", True, "All required security headers present")

        except Exception as e:
            self.log_test("Security Headers", False, str(e))

    def test_performance_indicators(self):
        """Test basic performance indicators"""
        print("\nTesting Performance Indicators...")

        try:
            start_time = time.time()
            response = self.session.get(f'{self.base_url}/')
            load_time = time.time() - start_time

            if response.status_code == 200:
                if load_time < 2.0:  # 2 second threshold
                    self.log_test("Page Load Time", True, f"Loaded in {load_time:.2f}s")
                else:
                    self.log_test("Page Load Time", False, f"Slow load time: {load_time:.2f}s")

                # Check content size
                content_length = len(response.content)
                if content_length < 1024 * 1024:  # 1MB threshold
                    self.log_test("Content Size", True, f"Content size: {content_length:,} bytes")
                else:
                    self.log_test("Content Size", False, f"Large content size: {content_length:,} bytes")

            else:
                self.log_test("Performance Test", False, f"Status code: {response.status_code}")

        except Exception as e:
            self.log_test("Performance Indicators", False, str(e))

    def test_error_handling(self):
        """Test error handling"""
        print("\nTesting Error Handling...")

        try:
            # Test 404 page
            response = self.session.get(f'{self.base_url}/nonexistent-page')
            if response.status_code == 404:
                self.log_test("404 Error Handling", True, "Proper 404 response")
            else:
                self.log_test("404 Error Handling", False, f"Unexpected status: {response.status_code}")

        except Exception as e:
            self.log_test("Error Handling", False, str(e))

    def generate_report(self):
        """Generate comprehensive test report"""
        print("\nCOMPREHENSIVE TEST REPORT")
        print("=" * 50)

        total_tests = len(self.test_results)
        passed_tests = sum(1 for result in self.test_results if result['success'])
        failed_tests = total_tests - passed_tests

        print(f"Total Tests: {total_tests}")
        print(f"Passed: {passed_tests}")
        print(f"Failed: {failed_tests}")
        print(f"Success Rate: {(passed_tests/total_tests)*100:.1f}%")

        print("\nDetailed Results:")
        for result in self.test_results:
            status = "PASS" if result['success'] else "FAIL"
            print(f"  {status}: {result['test']}")
            if result['details']:
                print(f"    Details: {result['details']}")

        if failed_tests == 0:
            print("\nALL TESTS PASSED! Service PRO is working correctly.")
            print("\nReady for production deployment!")
        else:
            print(f"\nWARNING: {failed_tests} test(s) failed. Please review the issues above.")

        return failed_tests == 0

    def run_all_tests(self):
        """Run all test suites"""
        print("Starting Comprehensive Service PRO Testing Suite")
        print("=" * 60)

        # Run all test methods
        self.test_homepage_loading()
        self.test_api_endpoints()
        self.test_user_registration()
        self.test_database_connectivity()
        self.test_responsive_features()
        self.test_security_headers()
        self.test_performance_indicators()
        self.test_error_handling()

        # Generate report
        return self.generate_report()

def main():
    """Main test function"""
    tester = ServicePROTester()
    success = tester.run_all_tests()
    exit(0 if success else 1)

if __name__ == '__main__':
    main()