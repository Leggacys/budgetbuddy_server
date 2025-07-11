import pytest
from app.utils.email_encryption import DataEncryption

class TestEmailEncryption:
    
    def test_encrypt_decrypt_email(self):
        """Test basic email encryption and decryption"""
        encryption = DataEncryption()
        
        test_email = "test@budgetbuddy.com"
        encrypted = encryption.encrypt(test_email)
        decrypted = encryption.decrypt(encrypted)
        
        # Assertions
        assert encrypted != test_email, "Email should be encrypted"
        assert decrypted == test_email, "Decrypted email should match original"
        assert len(encrypted) > len(test_email), "Encrypted email should be longer"
    
    def test_encrypt_empty_email(self):
        """Test encryption of empty/None email"""
        encryption = DataEncryption()
        
        assert encryption.encrypt("") == ""
        assert encryption.encrypt(None) == None
    
    def test_decrypt_empty_email(self):
        """Test decryption of empty/None email"""
        encryption = DataEncryption()
        
        assert encryption.decrypt("") == ""
        assert encryption.decrypt(None) == None
    
    def test_multiple_emails(self):
        """Test encryption of multiple different emails"""
        encryption = DataEncryption()
        
        emails = [
            "user1@example.com",
            "admin@budgetbuddy.com", 
            "test+tag@domain.co.uk",
            "very.long.email.address@subdomain.example.org"
        ]
        
        for email in emails:
            encrypted = encryption.encrypt(email)
            decrypted = encryption.decrypt(encrypted)
            assert decrypted == email, f"Failed for email: {email}"
    
    def test_same_email_different_encryption(self):
        """Test that same email produces different encrypted values"""
        encryption = DataEncryption()
        
        email = "same@example.com"
        encrypted1 = encryption.encrypt(email)
        encrypted2 = encryption.encrypt(email)
        
        # Each encryption should be different (due to random IV)
        assert encrypted1 != encrypted2, "Same email should produce different encrypted values"
        
        # But both should decrypt to the same value
        assert encryption.decrypt(encrypted1) == email
        assert encryption.decrypt(encrypted2) == email
    
    def test_invalid_encrypted_data(self):
        """Test decryption of invalid data"""
        encryption = DataEncryption()
        
        # Should not crash and return original invalid data
        invalid_data = "not-encrypted-data"
        result = encryption.decrypt(invalid_data)
        assert result == invalid_data, "Should return original data if decryption fails"
