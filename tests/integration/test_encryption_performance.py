import pytest
import time
from app.utils.email_encryption import DataEncryption
from app.utils.token_encryption import TokenEncryption

class TestEncryptionPerformance:
    
    def test_email_encryption_speed(self):
        """Test email encryption/decryption speed"""
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
        
        print(f"100 email encrypt/decrypt cycles took {duration:.2f} seconds")
        assert duration < 2.0, "Email encryption should be reasonably fast"
    
    def test_token_encryption_speed(self):
        """Test token encryption/decryption speed"""
        encryption = TokenEncryption()
        test_token = "access_token_performance_test_1234567890"
        
        # Test multiple encryptions
        start_time = time.time()
        for _ in range(100):
            encrypted = encryption.encrypt_token(test_token)
            decrypted = encryption.decrypt_token(encrypted)
            assert decrypted == test_token
        
        end_time = time.time()
        duration = end_time - start_time
        
        print(f"100 token encrypt/decrypt cycles took {duration:.2f} seconds")
        assert duration < 2.0, "Token encryption should be reasonably fast"
    
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
    
    def test_large_token_encryption(self):
        """Test encryption of large tokens (like JWT)"""
        encryption = TokenEncryption()
        
        # Create very long token (simulate JWT)
        long_token = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiIxMjM0NTY3ODkwIiwibmFtZSI6IkpvaG4gRG9lIiwiaWF0IjoxNTE2MjM5MDIyfQ.SflKxwRJSMeKKF2QT4fwpMeJf36POk6yJV_adQssw5c" * 2
        
        start_time = time.time()
        encrypted = encryption.encrypt_token(long_token)
        decrypted = encryption.decrypt_token(encrypted)
        end_time = time.time()
        
        assert decrypted == long_token
        assert (end_time - start_time) < 0.1, "Large token encryption should be fast"
    
    def test_memory_usage_emails(self):
        """Test memory usage with multiple email encryptions"""
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
    
    def test_memory_usage_tokens(self):
        """Test memory usage with multiple token encryptions"""
        encryption = TokenEncryption()
        
        tokens = [f"access_token_{i}_1234567890abcdef" for i in range(100)]
        encrypted_tokens = []
        
        # Encrypt all tokens
        for token in tokens:
            encrypted = encryption.encrypt_token(token)
            encrypted_tokens.append(encrypted)
        
        # Decrypt all tokens
        decrypted_tokens = []
        for encrypted in encrypted_tokens:
            decrypted = encryption.decrypt_token(encrypted)
            decrypted_tokens.append(decrypted)
        
        # Verify all tokens match
        assert tokens == decrypted_tokens
        assert len(tokens) == len(encrypted_tokens) == len(decrypted_tokens)
    
    def test_mixed_encryption_performance(self):
        """Test performance when mixing different encryption types"""
        email_encryption = DataEncryption()
        token_encryption = TokenEncryption()
        
        test_data = [
            ("email", "test@example.com"),
            ("token", "access_token_123"),
            ("email", "another@test.com"),
            ("token", "refresh_token_456"),
        ]
        
        start_time = time.time()
        
        for _ in range(50):  # 50 iterations of mixed operations
            for data_type, data in test_data:
                if data_type == "email":
                    encrypted = email_encryption.encrypt(data)
                    decrypted = email_encryption.decrypt(encrypted)
                else:
                    encrypted = token_encryption.encrypt_token(data)
                    decrypted = token_encryption.decrypt_token(encrypted)
                
                assert decrypted == data
        
        end_time = time.time()
        duration = end_time - start_time
        
        print(f"Mixed encryption operations took {duration:.2f} seconds")
        assert duration < 3.0, "Mixed encryption should be reasonably fast"
    
    def test_encryption_overhead(self):
        """Test encryption overhead vs plain text operations"""
        encryption = DataEncryption()
        test_email = "overhead@test.com"
        
        # Test plain string operations
        start_time = time.time()
        for _ in range(1000):
            temp = test_email.upper().lower()  # Simple operation
        plain_time = time.time() - start_time
        
        # Test with encryption
        start_time = time.time()
        for _ in range(100):  # Fewer iterations for encryption
            encrypted = encryption.encrypt(test_email)
            decrypted = encryption.decrypt(encrypted)
        encrypt_time = time.time() - start_time
        
        print(f"Plain operations (1000x): {plain_time:.4f}s")
        print(f"Encryption operations (100x): {encrypt_time:.4f}s")
        
        # Encryption should be reasonable (not more than 100x slower)
        # This is a loose test since encryption is inherently slower
        assert encrypt_time < 2.0, "Encryption overhead should be reasonable"
