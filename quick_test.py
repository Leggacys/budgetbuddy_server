#!/usr/bin/env python3
"""
Quick Test Script - Run specific test categories quickly
"""

import sys
import subprocess
import os

def run_command(cmd):
    """Run command and return success"""
    print(f"🔄 Running: {cmd}")
    result = subprocess.run(cmd, shell=True)
    return result.returncode == 0

def main():
    if len(sys.argv) < 2:
        print("🧪 BudgetBuddy Quick Test Runner")
        print()
        print("Usage: ./venv/bin/python3 quick_test.py <test_type>")
        print()
        print("Available test types:")
        print("  simple      - Basic functionality test (no pytest)")
        print("  encryption  - Email encryption tests")
        print("  tokens      - Token encryption tests")
        print("  edges       - Encryption edge cases tests")
        print("  user        - User model tests") 
        print("  bank        - Bank link model tests")
        print("  unit        - All unit tests")
        print("  api         - API endpoint tests")
        print("  integration - Integration tests")
        print("  database    - Database encryption integration tests")
        print("  performance - Performance tests")
        print("  security    - Security tests")
        print("  all         - All tests")
        print("  coverage    - Generate coverage report")
        print()
        print("Examples:")
        print("  ./venv/bin/python3 quick_test.py simple")
        print("  ./venv/bin/python3 quick_test.py encryption")
        print("  ./venv/bin/python3 quick_test.py edges")
        print("  ./venv/bin/python3 quick_test.py security")
        print("  ./venv/bin/python3 quick_test.py all")
        return 1
    
    test_type = sys.argv[1].lower()
    
    # Check environment
    if not os.path.exists("venv/bin/python3"):
        print("❌ Virtual environment not found!")
        print("Create it with: python3 -m venv venv")
        return 1
    
    # Test commands mapping
    commands = {
        "simple": "./venv/bin/python3 tests/simple_test.py",
        "encryption": "./venv/bin/python3 -m pytest tests/unit/test_email_encryption.py -v",
        "tokens": "./venv/bin/python3 -m pytest tests/unit/test_token_encryption.py -v",
        "edges": "./venv/bin/python3 -m pytest tests/unit/test_encryption_edge_cases.py -v",
        "user": "./venv/bin/python3 -m pytest tests/unit/test_user_model.py -v",
        "bank": "./venv/bin/python3 -m pytest tests/unit/test_bank_link_model.py -v",
        "unit": "./venv/bin/python3 -m pytest tests/unit/ -v",
        "api": "./venv/bin/python3 -m pytest tests/api/ -v",
        "integration": "./venv/bin/python3 -m pytest tests/integration/ -v",
        "database": "./venv/bin/python3 -m pytest tests/integration/test_database_encryption.py -v",
        "performance": "./venv/bin/python3 -m pytest tests/performance/ -v",
        "security": "./venv/bin/python3 -m pytest tests/security/ -v",
        "all": "./venv/bin/python3 -m pytest tests/ -v",
        "coverage": "./venv/bin/python3 -m pytest tests/ --cov=app --cov-report=html --cov-report=term"
    }
    
    if test_type not in commands:
        print(f"❌ Unknown test type: {test_type}")
        print("Run without arguments to see available options")
        return 1
    
    # Install pytest if needed (for non-simple tests)
    if test_type != "simple":
        print("📦 Installing test dependencies...")
        subprocess.run("./venv/bin/python3 -m pip install -q pytest pytest-asyncio pytest-cov", shell=True)
    
    # Run the test
    success = run_command(commands[test_type])
    
    if success:
        print("✅ Tests completed successfully!")
        if test_type == "coverage":
            print("📊 Coverage report: htmlcov/index.html")
        return 0
    else:
        print("❌ Some tests failed")
        return 1

if __name__ == "__main__":
    sys.exit(main())
