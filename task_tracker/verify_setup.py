#!/usr/bin/env python3
"""
Setup Verification Script for Task Tracker Application
Checks if all components are properly configured
"""

import sys
import os

def print_header(text):
    """Print formatted header"""
    print(f"\n{'='*60}")
    print(f"  {text}")
    print(f"{'='*60}\n")

def check_python_version():
    """Check if Python version is compatible"""
    print("🐍 Checking Python version...")
    version = sys.version_info
    if version.major >= 3 and version.minor >= 8:
        print(f"   ✅ Python {version.major}.{version.minor}.{version.micro} (Compatible)")
        return True
    else:
        print(f"   ❌ Python {version.major}.{version.minor}.{version.micro} (Requires 3.8+)")
        return False

def check_dependencies():
    """Check if required packages are installed"""
    print("\n📦 Checking dependencies...")
    
    required_packages = [
        'flask',
        'flask_login',
        'flask_bcrypt',
        'flask_wtf',
        'flask_sqlalchemy',
        'wtforms',
        'requests',
        'dotenv'
    ]
    
    all_installed = True
    
    for package in required_packages:
        try:
            __import__(package)
            print(f"   ✅ {package}")
        except ImportError:
            print(f"   ❌ {package} (Not installed)")
            all_installed = False
    
    return all_installed

def check_file_structure():
    """Check if all required files exist"""
    print("\n📁 Checking file structure...")
    
    required_files = [
        'app.py',
        'config.py',
        'models.py',
        'requirements.txt',
        'routes/__init__.py',
        'routes/auth.py',
        'routes/tasks.py',
        'routes/analytics.py',
        'routes/api_integration.py',
        'templates/base.html',
        'templates/login.html',
        'templates/register.html',
        'templates/tasks.html',
        'templates/task_form.html',
        'templates/dashboard.html',
        'static/css/style.css'
    ]
    
    all_exist = True
    
    for file_path in required_files:
        if os.path.exists(file_path):
            print(f"   ✅ {file_path}")
        else:
            print(f"   ❌ {file_path} (Missing)")
            all_exist = False
    
    return all_exist

def check_syntax():
    """Check Python files for syntax errors"""
    print("\n🔍 Checking Python syntax...")
    
    python_files = [
        'app.py',
        'config.py',
        'models.py',
        'routes/auth.py',
        'routes/tasks.py',
        'routes/analytics.py',
        'routes/api_integration.py'
    ]
    
    all_valid = True
    
    for file_path in python_files:
        try:
            with open(file_path, 'r') as f:
                compile(f.read(), file_path, 'exec')
            print(f"   ✅ {file_path}")
        except SyntaxError as e:
            print(f"   ❌ {file_path} (Syntax error: {e})")
            all_valid = False
        except Exception as e:
            print(f"   ⚠️  {file_path} (Warning: {e})")
    
    return all_valid

def check_database_init():
    """Check if database can be initialized"""
    print("\n💾 Checking database initialization...")
    
    try:
        from app import create_app
        from models import db
        
        app = create_app()
        with app.app_context():
            # Check if tables exist
            from sqlalchemy import inspect
            inspector = inspect(db.engine)
            tables = inspector.get_table_names()
            
            expected_tables = ['users', 'tasks', 'platform_stats']
            
            for table in expected_tables:
                if table in tables:
                    print(f"   ✅ Table '{table}' exists")
                else:
                    print(f"   ⚠️  Table '{table}' not found (will be created on first run)")
        
        return True
    except Exception as e:
        print(f"   ❌ Database initialization failed: {e}")
        return False

def main():
    """Run all verification checks"""
    print_header("Task Tracker - Setup Verification")
    
    results = {
        'Python Version': check_python_version(),
        'Dependencies': check_dependencies(),
        'File Structure': check_file_structure(),
        'Python Syntax': check_syntax(),
        'Database': check_database_init()
    }
    
    print_header("Verification Summary")
    
    all_passed = True
    for check, passed in results.items():
        status = "✅ PASSED" if passed else "❌ FAILED"
        print(f"{check:.<40} {status}")
        if not passed:
            all_passed = False
    
    print("\n" + "="*60)
    
    if all_passed:
        print("\n🎉 All checks passed! Your application is ready to run.")
        print("\n📝 Next steps:")
        print("   1. Run: python app.py")
        print("   2. Open: http://localhost:5000")
        print("   3. Register an account and start tracking tasks!")
    else:
        print("\n⚠️  Some checks failed. Please fix the issues above.")
        print("\n💡 Common fixes:")
        print("   - Install dependencies: pip install -r requirements.txt")
        print("   - Check file paths and permissions")
        print("   - Review error messages above")
    
    print("\n" + "="*60 + "\n")
    
    return 0 if all_passed else 1

if __name__ == '__main__':
    sys.exit(main())
