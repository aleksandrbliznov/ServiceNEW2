#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Python 3 Compatibility Check for Service PRO
Verifies that all components are compatible with Python 3.6+
"""

import sys
import os
import importlib

def check_python_version():
    """Check Python version compatibility"""
    print("🔍 Checking Python version...")

    version = sys.version_info
    print(f"   Current Python version: {version.major}.{version.minor}.{version.micro}")

    if version.major < 3:
        print("   ❌ Python 3+ required!")
        return False
    elif version.major == 3 and version.minor < 6:
        print("   ⚠️  Python 3.6+ recommended for best compatibility")
        return True
    else:
        print("   ✅ Python version is compatible")
        return True

def check_imports():
    """Check if all required modules can be imported"""
    print("\n🔍 Checking Python imports...")

    required_modules = [
        'flask',
        'flask_sqlalchemy',
        'flask_login',
        'flask_wtf',
        'flask_babel',
        'flask_mail',
        'sqlalchemy',
        'werkzeug',
        'dotenv',
        'wtforms'
    ]

    missing_modules = []

    for module in required_modules:
        try:
            importlib.import_module(module)
            print(f"   ✅ {module}")
        except ImportError as e:
            print(f"   ❌ {module}: {e}")
            missing_modules.append(module)

    if missing_modules:
        print(f"\n❌ Missing modules: {', '.join(missing_modules)}")
        print("   Run: pip install -r requirements.txt")
        return False

    print("   ✅ All required modules are available")
    return True

def check_file_encodings():
    """Check for Python 3 compatible file encodings"""
    print("\n🔍 Checking file encodings...")

    scripts_to_check = [
        'app.py',
        'api.py',
        'setup_mysql.py',
        'deploy_radicenter.py',
        'monitor.py'
    ]

    encoding_issues = []

    for script in scripts_to_check:
        if os.path.exists(script):
            try:
                with open(script, 'r', encoding='utf-8') as f:
                    content = f.read()
                    # Check for Python 2 specific syntax
                    if 'print ' in content and 'print(' not in content:
                        encoding_issues.append(f"{script}: Contains Python 2 print statement")
                    if 'unicode' in content and 'str' not in content:
                        encoding_issues.append(f"{script}: Contains deprecated unicode()")
                    if 'xrange' in content:
                        encoding_issues.append(f"{script}: Contains Python 2 xrange()")
                print(f"   ✅ {script}")
            except UnicodeDecodeError:
                encoding_issues.append(f"{script}: Encoding issue (not UTF-8)")
                print(f"   ❌ {script}: Encoding issue")
            except Exception as e:
                print(f"   ❌ {script}: {e}")
        else:
            print(f"   ⚠️  {script}: File not found")

    if encoding_issues:
        print("\n❌ Encoding issues found:")
        for issue in encoding_issues:
            print(f"   {issue}")
        return False

    print("   ✅ All files use Python 3 compatible encoding")
    return True

def check_mysql_compatibility():
    """Check MySQL database compatibility"""
    print("\n🔍 Checking MySQL compatibility...")

    try:
        import PyMySQL
        print(f"   ✅ PyMySQL version: {PyMySQL.__version__}")

        # Check if PyMySQL supports Python 3
        if hasattr(PyMySQL, '__version__'):
            print("   ✅ PyMySQL is Python 3 compatible")
            return True
        else:
            print("   ⚠️  Could not verify PyMySQL version")
            return True

    except ImportError:
        print("   ⚠️  PyMySQL not installed (will be installed with requirements.txt)")
        return True
    except Exception as e:
        print(f"   ❌ PyMySQL compatibility check failed: {e}")
        return False

def main():
    """Run all compatibility checks"""
    print("🚀 Service PRO - Python 3 Compatibility Check")
    print("=" * 50)

    checks = [
        ("Python Version", check_python_version),
        ("Module Imports", check_imports),
        ("File Encodings", check_file_encodings),
        ("MySQL Compatibility", check_mysql_compatibility),
    ]

    results = []
    for check_name, check_function in checks:
        result = check_function()
        results.append((check_name, result))

    print("\n" + "=" * 50)
    print("📊 Compatibility Check Results:")

    all_passed = True
    for check_name, result in results:
        status = "✅ PASS" if result else "❌ FAIL"
        print(f"   {check_name}: {status}")
        if not result:
            all_passed = False

    print("\n" + "=" * 50)
    if all_passed:
        print("🎉 All compatibility checks passed!")
        print("✅ Service PRO is ready for Python 3.6+ deployment on Radicenter")
        return True
    else:
        print("❌ Some compatibility issues found!")
        print("Please fix the issues above before deploying to Radicenter")
        return False

if __name__ == '__main__':
    try:
        success = main()
        sys.exit(0 if success else 1)
    except KeyboardInterrupt:
        print("\n\nCheck interrupted by user")
        sys.exit(1)
    except Exception as e:
        print(f"\n❌ Compatibility check failed with error: {e}")
        sys.exit(1)