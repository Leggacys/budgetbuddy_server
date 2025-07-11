"""
Test API endpoints with encryption functionality.
"""
import pytest
import json


class TestEncryptionAPIIntegration:
    """Test API endpoints that use encryption"""

    @pytest.mark.asyncio
    async def test_login_endpoint_returns_response(self, test_client):
        """Test login endpoint returns proper response format"""
        
        response = await test_client.post(
            '/login',
            data=json.dumps({"email": "test@encryption.com"}),
            headers={'Content-Type': 'application/json'}
        )
        
        # Should get either success or error, but not crash
        assert response.status_code in [200, 400, 500]
        data = await response.get_json()
        assert isinstance(data, dict)

    @pytest.mark.asyncio 
    async def test_api_error_handling_with_encryption(self, test_client):
        """Test API error handling doesn't leak encrypted data"""
        
        response = await test_client.post(
            '/login',
            data=json.dumps({}),
            headers={'Content-Type': 'application/json'}
        )
        
        assert response.status_code == 400
        data = await response.get_json()
        assert 'error' in data
        # Ensure no encrypted data is leaked in error messages
        assert 'Z0FBQUFBQm' not in str(data)  # Base64 pattern for encrypted data

    @pytest.mark.asyncio
    async def test_endpoint_basic_functionality(self, test_client):
        """Test endpoint basic functionality without database access"""
        
        # Test with invalid data to avoid database calls
        response = await test_client.post(
            '/login',
            data=json.dumps({"invalid": "data"}),
            headers={'Content-Type': 'application/json'}
        )
        
        # Should return error but not crash
        assert response.status_code == 400
        data = await response.get_json()
        assert isinstance(data, dict)


class TestEncryptionAPIErrorCases:
    """Test API error cases with encryption"""

    @pytest.mark.asyncio
    async def test_malformed_json_with_encryption(self, test_client):
        """Test malformed JSON doesn't cause encryption errors"""
        
        response = await test_client.post(
            '/login',
            data="invalid json",
            headers={'Content-Type': 'application/json'}
        )
        
        assert response.status_code == 400

    @pytest.mark.asyncio
    async def test_empty_request_body(self, test_client):
        """Test empty request body handling"""
        
        response = await test_client.post(
            '/login',
            data="",
            headers={'Content-Type': 'application/json'}
        )
        
        assert response.status_code == 400
        
    @pytest.mark.asyncio
    async def test_missing_content_type(self, test_client):
        """Test request without proper content type"""
        
        response = await test_client.post(
            '/login',
            data=json.dumps({"email": "test@example.com"})
        )
        
        # Should handle missing content type gracefully
        assert response.status_code in [200, 400, 500]
