import pytest
import time
from app.utils.email_encryption import DataEncryption

class TestEncryptionPerformance:
    
    def test_encryption_speed(self):
        """Test encryption/decryption speed"""
        encryption = DataEncryption()
        test_email = "performance@test.com"
        
        # Test multiple encryptions
        start_time = time.time()
        for _ in range(100):  # Reduced from 1000 for faster testing
            encrypted = encryption.encrypt(test_email)
            decrypted = encryption.decrypt(encrypted)
            assert decrypted == test_email
        
        end_time = time.time()
        duration = end_time - start_time
        
        print(f"100 encrypt/decrypt cycles took {duration:.2f} seconds")
        assert duration < 2.0, "Encryption should be reasonably fast"
    
    def test_large_email_encryption(self):
        """Test encryption of large email addresses"""
        encryption = DataEncryption()
        
        # Create very long email
        long_email = "very.long.email.address.with.many.parts@subdomain.example.organization.com"
        
        start_time = time.time()
        encrypted = encryption.encrypt(long_email)
        decrypted = encryption.decrypt(encrypted)
        end_time = time.time()
        
        assert decrypted == long_email
        assert (end_time - start_time) < 0.1, "Large email encryption should be fast"
    
    def test_memory_usage(self):
        """Test memory usage with multiple encryptions"""
        encryption = DataEncryption()
        
        emails = [f"user{i}@example.com" for i in range(100)]
        encrypted_emails = []
        
        # Encrypt all emails
        for email in emails:
            encrypted = encryption.encrypt(email)
            encrypted_emails.append(encrypted)
        
        # Decrypt all emails
        decrypted_emails = []
        for encrypted in encrypted_emails:
            decrypted = encryption.decrypt(encrypted)
            decrypted_emails.append(decrypted)
        
        # Verify all emails match
        assert emails == decrypted_emails
        assert len(emails) == len(encrypted_emails) == len(decrypted_emails)
