#!/bin/bash

# BudgetBuddy Server - Master Test Runner
# This script runs all tests and provides comprehensive feedback

# Color codes for better output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
PURPLE='\033[0;35m'
CYAN='\033[0;36m'
NC='\033[0m' # No Color

# Emoji for better visual feedback
CHECK="✅"
CROSS="❌"
WARNING="⚠️"
ROCKET="🚀"
TEST="🧪"
REPORT="📊"
CLOCK="⏱️"

print_header() {
    echo -e "${BLUE}================================${NC}"
    echo -e "${BLUE}$1${NC}"
    echo -e "${BLUE}================================${NC}"
}

print_success() {
    echo -e "${GREEN}${CHECK} $1${NC}"
}

print_error() {
    echo -e "${RED}${CROSS} $1${NC}"
}

print_warning() {
    echo -e "${YELLOW}${WARNING} $1${NC}"
}

print_info() {
    echo -e "${CYAN}ℹ️  $1${NC}"
}

# Check if we're in the right directory
if [ ! -f "run.py" ] || [ ! -d "app" ]; then
    print_error "Please run this script from the BudgetBuddy server root directory"
    exit 1
fi

print_header "${ROCKET} BudgetBuddy Server - Complete Test Suite"

# Variables for tracking results
TOTAL_TESTS=0
PASSED_TESTS=0
FAILED_TESTS=0
START_TIME=$(date +%s)

# Function to run a test and track results
run_test_category() {
    local category=$1
    local command=$2
    local description=$3
    
    echo ""
    print_info "Running $description..."
    echo -e "${PURPLE}Command: $command${NC}"
    echo ""
    
    if eval $command; then
        print_success "$description passed"
        PASSED_TESTS=$((PASSED_TESTS + 1))
        return 0
    else
        print_error "$description failed"
        FAILED_TESTS=$((FAILED_TESTS + 1))
        return 1
    fi
}

# Check virtual environment
print_info "Checking virtual environment..."
if [[ "$VIRTUAL_ENV" == "" ]]; then
    if [ -d "venv" ]; then
        print_warning "Activating virtual environment..."
        source venv/bin/activate
    else
        print_error "Virtual environment not found. Please create one first:"
        echo "python3 -m venv venv && source venv/bin/activate"
        exit 1
    fi
else
    print_success "Virtual environment is active: $VIRTUAL_ENV"
fi

# Install dependencies
print_info "Installing/updating test dependencies..."
./venv/bin/python3 -m pip install -q pytest pytest-asyncio aiosqlite pytest-cov

# 1. Simple Test (No pytest)
TOTAL_TESTS=$((TOTAL_TESTS + 1))
run_test_category "simple" "./venv/bin/python3 tests/simple_test.py" "Simple Integration Test"

# 2. Email Encryption Tests
TOTAL_TESTS=$((TOTAL_TESTS + 1))
run_test_category "encryption" "./venv/bin/python3 -m pytest tests/unit/test_email_encryption.py -v" "Email Encryption Tests"

# 3. User Model Tests
TOTAL_TESTS=$((TOTAL_TESTS + 1))
run_test_category "user_model" "./venv/bin/python3 -m pytest tests/unit/test_user_model.py -v" "User Model Tests"

# 4. Tokens Model Tests
TOTAL_TESTS=$((TOTAL_TESTS + 1))
run_test_category "tokens_model" "./venv/bin/python3 -m pytest tests/unit/test_tokens_model.py -v" "Tokens Model Tests"

# 5. All Unit Tests Together
TOTAL_TESTS=$((TOTAL_TESTS + 1))
run_test_category "all_unit" "./venv/bin/python3 -m pytest tests/unit/ -v" "All Unit Tests"

# 6. API Tests (may fail if server dependencies missing)
TOTAL_TESTS=$((TOTAL_TESTS + 1))
print_warning "API tests may fail if server is not properly configured"
run_test_category "api" "./venv/bin/python3 -m pytest tests/api/ -v" "API Endpoint Tests"

# 7. Integration Tests
TOTAL_TESTS=$((TOTAL_TESTS + 1))
run_test_category "integration" "./venv/bin/python3 -m pytest tests/integration/ -v" "Integration Tests"

# 8. Performance Tests
TOTAL_TESTS=$((TOTAL_TESTS + 1))
run_test_category "performance" "./venv/bin/python3 -m pytest tests/integration/test_performance.py -v" "Performance Tests"

# 9. Coverage Report
print_info "Generating coverage report..."
./venv/bin/python3 -m pytest tests/ --cov=app --cov-report=html --cov-report=term-missing -q

# Calculate runtime
END_TIME=$(date +%s)
RUNTIME=$((END_TIME - START_TIME))

# Final Results
echo ""
print_header "${REPORT} Test Results Summary"
echo ""
echo -e "${CYAN}${CLOCK} Total Runtime: ${RUNTIME} seconds${NC}"
echo -e "${GREEN}${CHECK} Passed: $PASSED_TESTS/$TOTAL_TESTS${NC}"
echo -e "${RED}${CROSS} Failed: $FAILED_TESTS/$TOTAL_TESTS${NC}"

if [ $FAILED_TESTS -eq 0 ]; then
    echo ""
    print_success "🎉 ALL TESTS PASSED! Your BudgetBuddy server is working perfectly!"
    echo ""
    print_info "Coverage report generated in: htmlcov/index.html"
    print_info "Open it in your browser to see detailed coverage information"
    exit 0
else
    echo ""
    print_warning "Some tests failed. This might be expected if:"
    echo "  - Server is not fully configured (API keys missing)"
    echo "  - Database is not initialized"
    echo "  - Dependencies are missing"
    echo ""
    print_info "Coverage report still generated in: htmlcov/index.html"
    exit 1
fi
