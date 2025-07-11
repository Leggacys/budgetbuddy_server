# BudgetBuddy Server Testing Guide

## 🧪 Test Structure

```
tests/
├── conftest.py              # Test configuration and fixtures
├── unit/                    # Unit tests for individual components
│   ├── test_email_encryption.py
│   ├── test_user_model.py
│   └── test_tokens_model.py
├── api/                     # API endpoint tests
│   ├── test_login_endpoint.py
│   └── test_nordigen_endpoints.py
└── integration/             # Integration and end-to-end tests
    ├── test_user_flow.py
    └── test_performance.py
```

## 🚀 Quick Start

### Install Test Dependencies

```bash
./venv/bin/python3 -m pip install -r test-requirements.txt
```

### Run All Tests

```bash
# Using the test runner script
chmod +x run_tests.sh
./run_tests.sh

# Or manually
./venv/bin/python3 -m pytest tests/ -v
```

### Run Specific Test Categories

```bash
# Unit tests only
./venv/bin/python3 -m pytest tests/unit/ -v

# API tests only
./venv/bin/python3 -m pytest tests/api/ -v

# Integration tests only
./venv/bin/python3 -m pytest tests/integration/ -v
```

### Run Individual Test Files

```bash
# Test email encryption only
./venv/bin/python3 -m pytest tests/unit/test_email_encryption.py -v

# Test login endpoint only
./venv/bin/python3 -m pytest tests/api/test_login_endpoint.py -v

# Test user model only
./venv/bin/python3 -m pytest tests/unit/test_user_model.py -v
```

## 📋 Test Categories

### Unit Tests (tests/unit/)

- ✅ **Email Encryption**: Test encryption/decryption functionality
- ✅ **User Model**: Test user creation and email encryption
- ✅ **Tokens Model**: Test token creation and validation

### API Tests (tests/api/)

- ✅ **Login Endpoint**: Test user login/creation
- ✅ **Nordigen Endpoints**: Test banking API endpoints
- ✅ **Error Handling**: Test invalid inputs and edge cases

### Integration Tests (tests/integration/)

- ✅ **User Flow**: Test complete user registration and bank connection
- ✅ **Performance**: Test encryption speed and memory usage
- ✅ **Data Persistence**: Test email encryption across requests

## 🔧 Test Configuration

### Test Database

- Uses SQLite in-memory database for testing
- Automatically created and cleaned up for each test
- Isolated from production database

### Test Fixtures

- `test_app`: Creates test application instance
- `test_client`: Provides HTTP client for API testing
- `test_db`: Creates isolated test database

## 📊 Coverage Reports

### Generate Coverage Report

```bash
./venv/bin/python3 -m pytest tests/ --cov=app --cov-report=html
```

### View Coverage Report

Open `htmlcov/index.html` in your browser to see detailed coverage information.

## 🧪 Example Test Commands

### Test Email Encryption

```bash
# Quick encryption test
./venv/bin/python3 -m pytest tests/unit/test_email_encryption.py::TestEmailEncryption::test_encrypt_decrypt_email -v
```

### Test User Model

```bash
# Test user creation with encryption
./venv/bin/python3 -m pytest tests/unit/test_user_model.py::TestUserModel::test_email_encryption -v
```

### Test Login API

```bash
# Test successful login
./venv/bin/python3 -m pytest tests/api/test_login_endpoint.py::TestLoginEndpoint::test_login_success -v
```

## 🎯 Expected Test Results

### Successful Test Output

```
tests/unit/test_email_encryption.py::TestEmailEncryption::test_encrypt_decrypt_email PASSED
tests/unit/test_user_model.py::TestUserModel::test_user_creation PASSED
tests/api/test_login_endpoint.py::TestLoginEndpoint::test_login_success PASSED
```

### Coverage Goals

- ✅ **Email Encryption**: 100% coverage
- ✅ **User Model**: 90%+ coverage
- ✅ **API Endpoints**: 80%+ coverage
- ✅ **Overall**: 85%+ coverage

## 🚨 Troubleshooting

### Common Issues

#### Import Errors

```bash
# Make sure you're in the project directory
cd /home/leggacys/Projects/Repo/budgetbuddy_server

# Make sure venv is activated
source venv/bin/activate

# Install test dependencies
./venv/bin/python3 -m pip install -r test-requirements.txt
```

#### Database Errors

```bash
# Clean up test database files
rm -f test_budgetbuddy.db

# Re-run tests
./venv/bin/python3 -m pytest tests/ -v
```

#### API Configuration Errors

- Some Nordigen tests may fail if API credentials are not configured
- This is expected for unit testing
- Tests will pass/fail gracefully

## 📝 Writing New Tests

### Unit Test Template

```python
import pytest
from app.your_module import YourClass

class TestYourClass:

    def test_your_function(self):
        """Test description"""
        # Arrange
        instance = YourClass()

        # Act
        result = instance.your_function()

        # Assert
        assert result == expected_value
```

### API Test Template

```python
import pytest
import json

class TestYourEndpoint:

    @pytest.mark.asyncio
    async def test_your_endpoint(self, test_client):
        """Test your endpoint"""
        response = await test_client.post(
            '/your-endpoint',
            data=json.dumps({"key": "value"}),
            headers={'Content-Type': 'application/json'}
        )

        assert response.status_code == 200
        data = await response.get_json()
        assert data['result'] == 'expected'
```

## 🔄 Continuous Testing

### Watch Mode (if needed)

```bash
# Install pytest-watch
./venv/bin/python3 -m pip install pytest-watch

# Run tests in watch mode
./venv/bin/python3 -m ptw tests/
```

### Pre-commit Testing

```bash
# Add to your development workflow
./venv/bin/python3 -m pytest tests/unit/ -v
git add .
git commit -m "Your commit message"
```
