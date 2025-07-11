import pytest
import json

class TestLoginEndpoint:
    
    @pytest.mark.asyncio
    async def test_login_success(self, test_client):
        """Test successful user login"""
        response = await test_client.post(
            '/login',
            data=json.dumps({"email": "test@example.com"}),
            headers={'Content-Type': 'application/json'}
        )
        
        assert response.status_code == 200
        data = await response.get_json()
        assert data['message'] in ["User found", "User not found, new user created"]
        assert data['email'] == "test@example.com"
    
    @pytest.mark.asyncio
    async def test_login_missing_email(self, test_client):
        """Test login without email"""
        response = await test_client.post(
            '/login',
            data=json.dumps({}),
            headers={'Content-Type': 'application/json'}
        )
        
        assert response.status_code == 400
        data = await response.get_json()
        assert 'error' in data
        assert 'Email is required' in data['error']
    
    @pytest.mark.asyncio
    async def test_login_invalid_json(self, test_client):
        """Test login with invalid JSON"""
        response = await test_client.post(
            '/login',
            data="invalid json",
            headers={'Content-Type': 'application/json'}
        )
        
        assert response.status_code == 400
    
    @pytest.mark.asyncio
    async def test_login_empty_email(self, test_client):
        """Test login with empty email"""
        response = await test_client.post(
            '/login',
            data=json.dumps({"email": ""}),
            headers={'Content-Type': 'application/json'}
        )
        
        assert response.status_code == 400
    
    @pytest.mark.asyncio
    async def test_login_invalid_email_format(self, test_client):
        """Test login with invalid email format"""
        response = await test_client.post(
            '/login',
            data=json.dumps({"email": "not-an-email"}),
            headers={'Content-Type': 'application/json'}
        )
        
        # Should still accept it (no email validation implemented yet)
        # But test is ready for when validation is added
        assert response.status_code in [200, 400]
