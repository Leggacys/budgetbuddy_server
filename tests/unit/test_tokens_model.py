import pytest
from datetime import datetime, timezone, timedelta
from app.database.models.tokens_model import Tokens

class TestTokensModel:
    
    def test_token_creation(self):
        """Test basic token creation"""
        now = datetime.now(timezone.utc)
        future = now + timedelta(hours=1)
        
        token = Tokens()
        token.access_token = "access_token_123"
        token.refresh_token = "refresh_token_456"
        token.access_expires = future
        token.refresh_expires = future + timedelta(days=30)
        
        assert token.access_token == "access_token_123"
        assert token.refresh_token == "refresh_token_456"
        assert token.access_expires > now
        assert token.refresh_expires > token.access_expires
    
    def test_token_encryption(self):
        """Test that tokens are encrypted in database"""
        token = Tokens()
        token.access_token = "secret_access_token_123"
        token.refresh_token = "secret_refresh_token_456"
        
        # Internal storage should be encrypted (different from original)
        assert token._access_token != "secret_access_token_123"
        assert token._refresh_token != "secret_refresh_token_456"
        assert token._access_token is not None
        assert token._refresh_token is not None
        assert len(token._access_token) > len("secret_access_token_123")
        assert len(token._refresh_token) > len("secret_refresh_token_456")
        
        # Public access should be decrypted
        assert token.access_token == "secret_access_token_123"
        assert token.refresh_token == "secret_refresh_token_456"
    
    def test_empty_tokens(self):
        """Test tokens with empty values"""
        token = Tokens()
        token.access_token = ""
        token.refresh_token = None
        
        assert token.access_token == ""
        assert token.refresh_token is None
        assert token._access_token == ""
        assert token._refresh_token is None
    
    def test_token_expiry_logic(self):
        """Test token expiry checking"""
        now = datetime.now(timezone.utc)
        past = now - timedelta(hours=1)
        future = now + timedelta(hours=1)
        
        token = Tokens()
        token.access_token = "test_token"
        token.refresh_token = "test_refresh"
        token.access_expires = past
        token.refresh_expires = future
        
        # Access token expired but refresh token still valid
        assert token.access_expires < now
        assert token.refresh_expires > now
        
        # Test expiry methods if they exist
        if hasattr(token, 'is_access_expired'):
            assert token.is_access_expired() == True
        if hasattr(token, 'is_refresh_expired'):
            assert token.is_refresh_expired() == False
    
    def test_token_model_fields(self):
        """Test all token model fields"""
        token = Tokens()
        
        # Test required fields exist
        assert hasattr(token, 'id')
        assert hasattr(token, 'access_token')
        assert hasattr(token, 'refresh_token')
        assert hasattr(token, 'access_expires')
        assert hasattr(token, 'refresh_expires')
        
        # Test internal encrypted fields exist
        assert hasattr(token, '_access_token')
        assert hasattr(token, '_refresh_token')
    
    def test_long_token_encryption(self):
        """Test encryption of very long tokens (like JWT)"""
        token = Tokens()
        
        # Simulate a long JWT token
        long_access_token = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiIxMjM0NTY3ODkwIiwibmFtZSI6IkpvaG4gRG9lIiwiaWF0IjoxNTE2MjM5MDIyfQ.SflKxwRJSMeKKF2QT4fwpMeJf36POk6yJV_adQssw5c"
        long_refresh_token = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiI5ODc2NTQzMjEwIiwibmFtZSI6IlJlZnJlc2ggVG9rZW4iLCJpYXQiOjE1MTYyMzkwMjJ9.different_signature_here_for_refresh_token_example"
        
        token.access_token = long_access_token
        token.refresh_token = long_refresh_token
        
        # Should handle long tokens correctly
        assert token.access_token == long_access_token
        assert token.refresh_token == long_refresh_token
        assert token._access_token != long_access_token
        assert token._refresh_token != long_refresh_token
    
    def test_token_repr(self):
        """Test token string representation"""
        now = datetime.now(timezone.utc)
        future = now + timedelta(hours=1)
        
        token = Tokens()
        token.access_token = "test_access_token"
        token.access_expires = future
        token.refresh_expires = future + timedelta(days=30)
        
        # Basic repr test
        repr_str = repr(token)
        assert "Tokens" in repr_str or "object" in repr_str
        
        # Should not expose encrypted tokens in repr
        assert "test_access_token" not in repr_str
