#!/usr/bin/env python3
"""
BudgetBuddy Server - Python Test Runner
Comprehensive test runner that accesses all test categories
"""

import subprocess
import sys
import os
import time
from pathlib import Path

# Color codes for output
class Colors:
    RED = '\033[0;31m'
    GREEN = '\033[0;32m'
    YELLOW = '\033[1;33m'
    BLUE = '\033[0;34m'
    PURPLE = '\033[0;35m'
    CYAN = '\033[0;36m'
    NC = '\033[0m'  # No Color

def print_colored(text, color):
    """Print colored text"""
    print(f"{color}{text}{Colors.NC}")

def print_header(text):
    """Print a header with decoration"""
    print_colored("=" * 60, Colors.BLUE)
    print_colored(f"🚀 {text}", Colors.BLUE)
    print_colored("=" * 60, Colors.BLUE)

def print_success(text):
    """Print success message"""
    print_colored(f"✅ {text}", Colors.GREEN)

def print_error(text):
    """Print error message"""
    print_colored(f"❌ {text}", Colors.RED)

def print_warning(text):
    """Print warning message"""
    print_colored(f"⚠️  {text}", Colors.YELLOW)

def print_info(text):
    """Print info message"""
    print_colored(f"ℹ️  {text}", Colors.CYAN)

def run_command(command, description):
    """Run a command and return success status"""
    print_info(f"Running: {description}")
    print_colored(f"Command: {command}", Colors.PURPLE)
    print()
    
    try:
        result = subprocess.run(command, shell=True, capture_output=False, text=True)
        if result.returncode == 0:
            print_success(f"{description} - PASSED")
            return True
        else:
            print_error(f"{description} - FAILED")
            return False
    except Exception as e:
        print_error(f"{description} - ERROR: {e}")
        return False

def check_environment():
    """Check if environment is properly set up"""
    print_info("Checking environment...")
    
    # Check if we're in the right directory
    if not os.path.exists("run.py") or not os.path.exists("app"):
        print_error("Please run this script from the BudgetBuddy server root directory")
        return False
    
    # Check if virtual environment exists
    if not os.path.exists("venv"):
        print_error("Virtual environment not found. Please create one first:")
        print("python3 -m venv venv && source venv/bin/activate")
        return False
    
    # Check if we can access Python
    python_path = "./venv/bin/python3"
    if not os.path.exists(python_path):
        print_error(f"Python not found at {python_path}")
        return False
    
    print_success("Environment check passed")
    return True

def install_dependencies():
    """Install test dependencies"""
    print_info("Installing test dependencies...")
    
    dependencies = [
        "pytest>=7.0.0",
        "pytest-asyncio>=0.21.0", 
        "aiosqlite>=0.19.0",
        "pytest-cov>=4.0.0"
    ]
    
    for dep in dependencies:
        command = f"./venv/bin/python3 -m pip install -q {dep}"
        try:
            subprocess.run(command, shell=True, check=True, capture_output=True)
        except subprocess.CalledProcessError:
            print_warning(f"Failed to install {dep}")
    
    print_success("Dependencies installation completed")

def main():
    """Main test runner function"""
    start_time = time.time()
    
    print_header("BudgetBuddy Server - Complete Test Suite")
    
    # Environment check
    if not check_environment():
        sys.exit(1)
    
    # Install dependencies
    install_dependencies()
    
    # Test categories to run
    test_categories = [
        {
            "name": "Simple Integration Test",
            "command": "./venv/bin/python3 tests/simple_test.py",
            "required": True
        },
        {
            "name": "Email Encryption Tests", 
            "command": "./venv/bin/python3 -m pytest tests/unit/test_email_encryption.py -v",
            "required": True
        },
        {
            "name": "Token Encryption Tests",
            "command": "./venv/bin/python3 -m pytest tests/unit/test_token_encryption.py -v",
            "required": True
        },
        {
            "name": "Bank Link Model Tests",
            "command": "./venv/bin/python3 -m pytest tests/unit/test_bank_link_model.py -v",
            "required": True
        },
        {
            "name": "Encryption Edge Cases Tests",
            "command": "./venv/bin/python3 -m pytest tests/unit/test_encryption_edge_cases.py -v",
            "required": True
        },
        {
            "name": "User Model Tests",
            "command": "./venv/bin/python3 -m pytest tests/unit/test_user_model.py -v", 
            "required": True
        },
        {
            "name": "Tokens Model Tests",
            "command": "./venv/bin/python3 -m pytest tests/unit/test_tokens_model.py -v",
            "required": True
        },
        {
            "name": "All Unit Tests",
            "command": "./venv/bin/python3 -m pytest tests/unit/ -v",
            "required": True
        },
        {
            "name": "API Endpoint Tests",
            "command": "./venv/bin/python3 -m pytest tests/api/ -v",
            "required": False  # May fail if server not configured
        },
        {
            "name": "Encryption API Tests",
            "command": "./venv/bin/python3 -m pytest tests/api/test_encryption_api.py -v",
            "required": False  # May fail if server not configured
        },
        {
            "name": "Integration Tests", 
            "command": "./venv/bin/python3 -m pytest tests/integration/ -v",
            "required": False
        },
        {
            "name": "Database Encryption Integration Tests",
            "command": "./venv/bin/python3 -m pytest tests/integration/test_database_encryption.py -v",
            "required": True
        },
        {
            "name": "Performance Tests",
            "command": "./venv/bin/python3 -m pytest tests/integration/test_performance.py -v",
            "required": True
        },
        {
            "name": "Advanced Encryption Performance Tests",
            "command": "./venv/bin/python3 -m pytest tests/performance/test_encryption_performance.py -v",
            "required": True
        },
        {
            "name": "Security Tests",
            "command": "./venv/bin/python3 -m pytest tests/security/test_encryption_security.py -v",
            "required": True
        }
    ]
    
    # Run tests
    results = {
        "total": len(test_categories),
        "passed": 0,
        "failed": 0,
        "required_failed": 0
    }
    
    for test in test_categories:
        print()
        success = run_command(test["command"], test["name"])
        
        if success:
            results["passed"] += 1
        else:
            results["failed"] += 1
            if test["required"]:
                results["required_failed"] += 1
    
    # Generate coverage report
    print()
    print_info("Generating coverage report...")
    coverage_command = "./venv/bin/python3 -m pytest tests/ --cov=app --cov-report=html --cov-report=term-missing -q"
    subprocess.run(coverage_command, shell=True)
    
    # Calculate runtime
    end_time = time.time()
    runtime = round(end_time - start_time, 2)
    
    # Print results
    print()
    print_header("Test Results Summary")
    print()
    print_colored(f"⏱️  Total Runtime: {runtime} seconds", Colors.CYAN)
    print_colored(f"✅ Passed: {results['passed']}/{results['total']}", Colors.GREEN)
    print_colored(f"❌ Failed: {results['failed']}/{results['total']}", Colors.RED)
    
    if results["required_failed"] == 0:
        print()
        print_success("🎉 ALL CRITICAL TESTS PASSED!")
        print_info("Your BudgetBuddy server core functionality is working!")
        print()
        print_info("📊 Coverage report: htmlcov/index.html")
        print_info("🌐 Open in browser: file://" + os.path.abspath("htmlcov/index.html"))
        
        if results["failed"] > 0:
            print_warning("Some non-critical tests failed (likely due to missing API configuration)")
        
        return 0
    else:
        print()
        print_error("Some critical tests failed!")
        print_warning("Please check the error messages above")
        return 1

if __name__ == "__main__":
    try:
        exit_code = main()
        sys.exit(exit_code)
    except KeyboardInterrupt:
        print()
        print_warning("Tests interrupted by user")
        sys.exit(1)
    except Exception as e:
        print()
        print_error(f"Unexpected error: {e}")
        sys.exit(1)
