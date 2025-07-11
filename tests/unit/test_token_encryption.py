import pytest
from app.utils.token_encryption import TokenEncryption

class TestTokenEncryption:
    
    def test_encrypt_decrypt_token(self):
        """Test basic token encryption and decryption"""
        encryption = TokenEncryption()
        
        test_token = "access_token_1234567890abcdef"
        encrypted = encryption.encrypt_token(test_token)
        decrypted = encryption.decrypt_token(encrypted)
        
        # Assertions
        assert encrypted != test_token, "Token should be encrypted"
        assert decrypted == test_token, "Decrypted token should match original"
        assert len(encrypted) > len(test_token), "Encrypted token should be longer"
    
    def test_encrypt_empty_token(self):
        """Test encryption of empty/None token"""
        encryption = TokenEncryption()
        
        assert encryption.encrypt_token("") == ""
        assert encryption.encrypt_token(None) == None
    
    def test_decrypt_empty_token(self):
        """Test decryption of empty/None token"""
        encryption = TokenEncryption()
        
        assert encryption.decrypt_token("") == ""
        assert encryption.decrypt_token(None) == None
    
    def test_multiple_tokens(self):
        """Test encryption of different types of tokens"""
        encryption = TokenEncryption()
        
        tokens = [
            "access_token_1234567890",
            "refresh_token_abcdefghij",
            "bearer_token_xyz123", 
            "api_key_very_long_secret_key_here_with_special_chars_!@#$%"
        ]
        
        for token in tokens:
            encrypted = encryption.encrypt_token(token)
            decrypted = encryption.decrypt_token(encrypted)
            assert decrypted == token, f"Failed for token: {token[:20]}..."
    
    def test_same_token_different_encryption(self):
        """Test that same token produces different encrypted values"""
        encryption = TokenEncryption()
        
        token = "same_access_token_123"
        encrypted1 = encryption.encrypt_token(token)
        encrypted2 = encryption.encrypt_token(token)
        
        # Each encryption should be different (due to random IV)
        assert encrypted1 != encrypted2, "Same token should produce different encrypted values"
        
        # But both should decrypt to the same value
        assert encryption.decrypt_token(encrypted1) == token
        assert encryption.decrypt_token(encrypted2) == token
    
    def test_invalid_encrypted_token(self):
        """Test decryption of invalid token data"""
        encryption = TokenEncryption()
        
        # Should not crash and return original invalid data
        invalid_data = "not-encrypted-token-data"
        result = encryption.decrypt_token(invalid_data)
        assert result == invalid_data, "Should return original data if decryption fails"
    
    def test_long_token_encryption(self):
        """Test encryption of very long tokens"""
        encryption = TokenEncryption()
        
        # Create a very long token (like JWT)
        long_token = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiIxMjM0NTY3ODkwIiwibmFtZSI6IkpvaG4gRG9lIiwiaWF0IjoxNTE2MjM5MDIyfQ.SflKxwRJSMeKKF2QT4fwpMeJf36POk6yJV_adQssw5c" * 3
        
        encrypted = encryption.encrypt_token(long_token)
        decrypted = encryption.decrypt_token(encrypted)
        
        assert decrypted == long_token
        assert len(encrypted) > len(long_token)
    
    def test_special_characters_in_token(self):
        """Test tokens with special characters"""
        encryption = TokenEncryption()
        
        special_tokens = [
            "token-with-dashes_and_underscores",
            "token.with.dots@domain.com",
            "token+with+plus/and/slashes=equals",
            "token#with$special%characters&more!"
        ]
        
        for token in special_tokens:
            encrypted = encryption.encrypt_token(token)
            decrypted = encryption.decrypt_token(encrypted)
            assert decrypted == token, f"Failed for special token: {token}"
