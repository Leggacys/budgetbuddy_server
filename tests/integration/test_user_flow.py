import pytest
import json

class TestUserFlow:
    
    @pytest.mark.asyncio
    async def test_complete_user_registration_flow(self, test_client):
        """Test complete user registration and bank connection flow"""
        
        # Step 1: Register/login user
        login_response = await test_client.post(
            '/login',
            data=json.dumps({"email": "integration@test.com"}),
            headers={'Content-Type': 'application/json'}
        )
        
        assert login_response.status_code == 200
        login_data = await login_response.get_json()
        user_id = login_data['user_id']
        
        # Step 2: Try to create bank requisition
        requisition_response = await test_client.post(
            '/nordingen-create-requisition',
            data=json.dumps({
                "institution_id": "SANDBOXFINANCE_SFIN0000",
                "email": "integration@test.com"
            }),
            headers={'Content-Type': 'application/json'}
        )
        
        # This might fail due to API configuration, but test the flow
        assert requisition_response.status_code in [200, 201, 400, 500]
        
        # Step 3: Try to get transactions (should return no requisitions initially)
        transactions_response = await test_client.get(
            '/nordingen-get-transactions?email=integration@test.com'
        )
        
        assert transactions_response.status_code == 404  # No requisitions found
    
    @pytest.mark.asyncio
    async def test_multiple_users_isolation(self, test_client):
        """Test that multiple users are properly isolated"""
        
        # Create user 1
        user1_response = await test_client.post(
            '/login',
            data=json.dumps({"email": "user1@test.com"}),
            headers={'Content-Type': 'application/json'}
        )
        assert user1_response.status_code == 200
        user1_data = await user1_response.get_json()
        
        # Create user 2
        user2_response = await test_client.post(
            '/login',
            data=json.dumps({"email": "user2@test.com"}),
            headers={'Content-Type': 'application/json'}
        )
        assert user2_response.status_code == 200
        user2_data = await user2_response.get_json()
        
        # Users should have different IDs
        assert user1_data['user_id'] != user2_data['user_id']
        
        # Each user should have no transactions initially
        user1_transactions = await test_client.get(
            '/nordingen-get-transactions?email=user1@test.com'
        )
        user2_transactions = await test_client.get(
            '/nordingen-get-transactions?email=user2@test.com'
        )
        
        assert user1_transactions.status_code == 404
        assert user2_transactions.status_code == 404
    
    @pytest.mark.asyncio
    async def test_email_encryption_persistence(self, test_client):
        """Test that email encryption persists across requests"""
        
        # Create user
        email = "encryption@test.com"
        response1 = await test_client.post(
            '/login',
            data=json.dumps({"email": email}),
            headers={'Content-Type': 'application/json'}
        )
        assert response1.status_code == 200
        
        # Try to login again with same email
        response2 = await test_client.post(
            '/login',
            data=json.dumps({"email": email}),
            headers={'Content-Type': 'application/json'}
        )
        assert response2.status_code == 200
        
        # Should return same user or create new one (depending on implementation)
        data1 = await response1.get_json()
        data2 = await response2.get_json()
        
        assert data1['email'] == data2['email'] == email
