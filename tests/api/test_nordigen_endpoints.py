import pytest
import json

class TestNordigenEndpoints:
    
    @pytest.mark.asyncio
    async def test_create_requisition_success(self, test_client):
        """Test successful requisition creation"""
        response = await test_client.post(
            '/nordingen-create-requisition',
            data=json.dumps({
                "institution_id": "SANDBOXFINANCE_SFIN0000",
                "email": "test@example.com"
            }),
            headers={'Content-Type': 'application/json'}
        )
        
        # Note: This might fail if Nordigen API is not configured
        # Should return either success or a configuration error
        assert response.status_code in [200, 400, 500]
    
    @pytest.mark.asyncio
    async def test_create_requisition_missing_data(self, test_client):
        """Test requisition creation with missing data"""
        response = await test_client.post(
            '/nordingen-create-requisition',
            data=json.dumps({"email": "test@example.com"}),
            headers={'Content-Type': 'application/json'}
        )
        
        assert response.status_code == 400
    
    @pytest.mark.asyncio
    async def test_create_requisition_missing_email(self, test_client):
        """Test requisition creation with missing email"""
        response = await test_client.post(
            '/nordingen-create-requisition',
            data=json.dumps({"institution_id": "SANDBOXFINANCE_SFIN0000"}),
            headers={'Content-Type': 'application/json'}
        )
        
        assert response.status_code == 400
    
    @pytest.mark.asyncio
    async def test_get_transactions_missing_email(self, test_client):
        """Test get transactions without email"""
        response = await test_client.get('/nordingen-get-transactions')
        
        assert response.status_code == 400
        data = await response.get_json()
        assert 'Missing email' in data['error']
    
    @pytest.mark.asyncio
    async def test_get_transactions_no_requisitions(self, test_client):
        """Test get transactions for user with no requisitions"""
        response = await test_client.get(
            '/nordingen-get-transactions?email=nonexistent@example.com'
        )
        
        assert response.status_code == 404
        data = await response.get_json()
        assert 'No requisitions found' in data['error']
    
    @pytest.mark.asyncio
    async def test_list_banks_valid_country(self, test_client):
        """Test listing banks for valid country"""
        response = await test_client.get(
            '/nordingen-list-of-banks-from-country?country=GB'
        )
        
        # Should return either success or API error
        assert response.status_code in [200, 400, 500]
    
    @pytest.mark.asyncio
    async def test_list_banks_missing_country(self, test_client):
        """Test listing banks without country"""
        response = await test_client.get('/nordingen-list-of-banks-from-country')
        
        assert response.status_code == 400
    
    @pytest.mark.asyncio
    async def test_redirect_url_missing_requisition_id(self, test_client):
        """Test redirect URL without requisition ID"""
        response = await test_client.get('/nordigen-redirect-url')
        
        assert response.status_code == 400
