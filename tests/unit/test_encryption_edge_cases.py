"""
Test edge cases and security scenarios for encryption functionality.
These tests cover advanced scenarios that might not be covered in the basic unit tests.
"""
import pytest
import uuid
import time
import base64
import secrets
from unittest.mock import patch, MagicMock
from app.utils.email_encryption import DataEncryption, email_encryption
from app.utils.token_encryption import TokenEncryption, token_encryption
from app.database.models.user_model import User
from app.database.models.tokens_model import Tokens
from app.database.models.bank_links_model import BankLink


class TestEncryptionEdgeCases:
    
    def test_unicode_email_encryption(self):
        """Test encryption of emails with unicode characters"""
        encryption = DataEncryption()
        
        unicode_emails = [
            "测试@example.com",
            "тест@example.com", 
            "test@例え.com",
            "niño@münchen.de",
            "café@résumé.org"
        ]
        
        for email in unicode_emails:
            encrypted = encryption.encrypt(email)
            decrypted = encryption.decrypt(encrypted)
            assert decrypted == email, f"Unicode email failed: {email}"
            assert encrypted != email, "Should be encrypted"
    
    def test_max_length_values(self):
        """Test encryption of maximum length values"""
        encryption = DataEncryption()
        token_enc = TokenEncryption()
        
        # Very long email (near practical limits)
        long_email = "a" * 200 + "@" + "b" * 200 + ".com"
        encrypted_email = encryption.encrypt(long_email)
        assert encryption.decrypt(encrypted_email) == long_email
        
        # Very long token
        long_token = "token_" + "x" * 2000
        encrypted_token = token_enc.encrypt_token(long_token)
        assert token_enc.decrypt_token(encrypted_token) == long_token
    
    def test_encryption_consistency_across_instances(self):
        """Test that different encryption instances can decrypt each other's data"""
        email1 = "test@example.com"
        token1 = "test_token_123"
        
        # Create two different encryption instances
        email_enc1 = DataEncryption()
        email_enc2 = DataEncryption()
        token_enc1 = TokenEncryption()
        token_enc2 = TokenEncryption()
        
        # Encrypt with first instance
        encrypted_email = email_enc1.encrypt(email1)
        encrypted_token = token_enc1.encrypt_token(token1)
        
        # Decrypt with second instance
        decrypted_email = email_enc2.decrypt(encrypted_email)
        decrypted_token = token_enc2.decrypt_token(encrypted_token)
        
        assert decrypted_email == email1
        assert decrypted_token == token1
    
    def test_encryption_with_null_bytes(self):
        """Test encryption of strings containing null bytes"""
        encryption = DataEncryption()
        
        # This should handle gracefully
        test_string = "test\x00null@example.com"
        encrypted = encryption.encrypt(test_string)
        decrypted = encryption.decrypt(encrypted)
        assert decrypted == test_string
    
    def test_concurrent_encryption_operations(self):
        """Test encryption operations running concurrently"""
        import threading
        
        encryption = DataEncryption()
        results = []
        errors = []
        
        def encrypt_decrypt_worker(email_suffix):
            try:
                email = f"concurrent{email_suffix}@test.com"
                encrypted = encryption.encrypt(email)
                decrypted = encryption.decrypt(encrypted)
                results.append((email, decrypted))
            except Exception as e:
                errors.append(e)
        
        # Create multiple threads
        threads = []
        for i in range(10):
            thread = threading.Thread(target=encrypt_decrypt_worker, args=(i,))
            threads.append(thread)
            thread.start()
        
        # Wait for all threads to complete
        for thread in threads:
            thread.join()
        
        # Verify results
        assert len(errors) == 0, f"Errors occurred: {errors}"
        assert len(results) == 10
        
        for original, decrypted in results:
            assert original == decrypted
    
    def test_encryption_memory_usage(self):
        """Test that encryption doesn't cause memory leaks"""
        import gc
        import sys
        
        encryption = DataEncryption()
        
        # Get initial memory usage
        gc.collect()
        initial_objects = len(gc.get_objects())
        
        # Perform many encryption operations
        for i in range(1000):
            email = f"memory_test_{i}@example.com"
            encrypted = encryption.encrypt(email)
            decrypted = encryption.decrypt(encrypted)
            assert decrypted == email
        
        # Check memory usage after operations
        gc.collect()
        final_objects = len(gc.get_objects())
        
        # Allow for some increase but not excessive
        object_increase = final_objects - initial_objects
        assert object_increase < 100, f"Too many objects created: {object_increase}"


class TestModelEncryptionEdgeCases:
    
    def test_user_email_validation_after_encryption(self):
        """Test that encrypted emails still validate correctly"""
        user = User()
        
        # Test various email formats
        valid_emails = [
            "simple@example.com",
            "user.name@example.com",
            "user+tag@example.co.uk",
            "123@numbers.org"
        ]
        
        for email in valid_emails:
            user.email = email
            assert user.email == email
            # Verify it's actually encrypted in storage
            assert user._email != email
            assert len(user._email) > len(email)
    
    def test_token_model_with_real_jwt_tokens(self):
        """Test token model with realistic JWT tokens"""
        token = Tokens()
        
        # Example JWT tokens (not real, just format)
        jwt_access = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiIxMjM0NTY3ODkwIiwibmFtZSI6IkpvaG4gRG9lIiwiaWF0IjoxNTE2MjM5MDIyfQ.SflKxwRJSMeKKF2QT4fwpMeJf36POk6yJV_adQssw5c"
        jwt_refresh = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiIxMjM0NTY3ODkwIiwibmFtZSI6IkpvaG4gRG9lIiwiaWF0IjoxNTE2MjM5MDIyLCJleHAiOjE1MTYyNDI2MjJ9.L8i6g3PluJpjRCT_CWmlyQabzOtgQS631MBaLNHir90"
        
        token.access_token = jwt_access
        token.refresh_token = jwt_refresh
        
        # Verify encryption/decryption works with JWT format
        assert token.access_token == jwt_access
        assert token.refresh_token == jwt_refresh
        assert token._access_token != jwt_access
        assert token._refresh_token != jwt_refresh
    
    def test_bank_link_with_realistic_ids(self):
        """Test bank link encryption with realistic bank IDs"""
        bank_link = BankLink()
        
        # Real-looking requisition IDs from various banking APIs
        realistic_req_ids = [
            "550e8400-e29b-41d4-a716-446655440000",  # UUID format
            "REQ_2024_HSBC_UK_001234567890",          # Descriptive format
            "req-prod-gb-barclays-20240101-abc123",   # Hyphenated format
            "GoCardless_REQ_GB_LLOYDS_XYZ789"        # Mixed format
        ]
        
        realistic_inst_ids = [
            "SANDBOXFINANCE_SFIN0000",
            "BARCLAYS_BARCGB22",
            "HSBC_HBUKGB4B", 
            "LLOYDS_LOYDGB2L",
            "NATWEST_NWBKGB2L",
            "SANTANDER_ABBYGB2L"
        ]
        
        for req_id in realistic_req_ids:
            bank_link.requisition_id = req_id
            assert bank_link.requisition_id == req_id
            assert bank_link._requisition_id != req_id
        
        for inst_id in realistic_inst_ids:
            bank_link.institution_id = inst_id
            assert bank_link.institution_id == inst_id
            assert bank_link._institution_id != inst_id
    
    def test_model_field_assignment_multiple_times(self):
        """Test reassigning encrypted fields multiple times"""
        user = User()
        
        emails = [
            "first@example.com",
            "second@example.com", 
            "third@example.com"
        ]
        
        for email in emails:
            old_encrypted = user._email
            user.email = email
            
            # Each assignment should create new encryption
            assert user.email == email
            assert user._email != old_encrypted if old_encrypted else True
    
    def test_model_copy_and_encryption(self):
        """Test that copying models maintains encryption"""
        user1 = User()
        user1.email = "original@test.com"
        
        # Create another user with same email
        user2 = User()
        user2.email = "original@test.com"
        
        # Should decrypt to same value
        assert user1.email == user2.email
        
        # But encrypted values should be different (due to random IV)
        assert user1._email != user2._email


class TestEncryptionErrorHandling:
    
    def test_encryption_with_corrupted_key(self):
        """Test behavior when encryption key is corrupted"""
        from app.utils.email_encryption import DataEncryption
        
        encryption = DataEncryption()
        email = "test@example.com"
        encrypted = encryption.encrypt(email)
        
        # Simulate corrupted key by creating new instance with different key
        # Use a valid base64 key but different from the original
        different_key = base64.urlsafe_b64encode(secrets.token_bytes(32)).decode()
        
        with patch.dict('os.environ', {'EMAIL_ENCRYPTION_KEY': different_key}):
            new_encryption = DataEncryption()
            # Should not crash, might return original encrypted data if decryption fails
            result = new_encryption.decrypt(encrypted)
            assert result is not None  # Should handle gracefully
    
    def test_encryption_with_invalid_base64(self):
        """Test decryption with invalid base64 data"""
        encryption = DataEncryption()
        
        invalid_data = "not-valid-base64-data!!!"
        result = encryption.decrypt(invalid_data)
        
        # Should return original data if decryption fails
        assert result == invalid_data
    
    def test_model_with_none_values_during_encryption(self):
        """Test model behavior when setting None values"""
        user = User()
        token = Tokens()
        bank_link = BankLink()
        
        # Setting None should work
        user.email = None
        assert user.email is None
        assert user._email is None
        
        token.access_token = None
        token.refresh_token = None
        assert token.access_token is None
        assert token.refresh_token is None
        
        bank_link.requisition_id = None
        bank_link.institution_id = None
        assert bank_link.requisition_id is None
        assert bank_link.institution_id is None


class TestEncryptionSecurity:
    
    def test_encrypted_data_is_not_predictable(self):
        """Test that encrypted data is not predictable or reversible without key"""
        encryption = DataEncryption()
        email = "predictable@test.com"
        
        encrypted_values = []
        for _ in range(10):
            encrypted = encryption.encrypt(email)
            encrypted_values.append(encrypted)
        
        # All encrypted values should be different
        assert len(set(encrypted_values)) == 10, "All encrypted values should be unique"
        
        # None should be predictable from the email
        for encrypted in encrypted_values:
            assert email not in encrypted
            assert "predictable" not in encrypted
            assert "test.com" not in encrypted
    
    def test_encryption_key_isolation(self):
        """Test that different encryption types use different keys"""
        email_enc = DataEncryption()
        token_enc = TokenEncryption()
        
        same_value = "test@example.com"
        
        email_encrypted = email_enc.encrypt(same_value)
        token_encrypted = token_enc.encrypt_token(same_value)
        
        # Should produce different encrypted values
        assert email_encrypted != token_encrypted
        
        # And each should only decrypt with its own method
        assert email_enc.decrypt(email_encrypted) == same_value
        assert token_enc.decrypt_token(token_encrypted) == same_value
    
    def test_sensitive_data_not_in_repr(self):
        """Test that sensitive data doesn't appear in model representations"""
        user = User()
        user.email = "sensitive@secret.com"
        
        token = Tokens()
        token.access_token = "super_secret_access_token"
        token.refresh_token = "super_secret_refresh_token"
        
        bank_link = BankLink()
        bank_link.requisition_id = "secret_requisition_123"
        bank_link.institution_id = "secret_institution_456" 
        bank_link.bank_name = "Test Bank"
        
        # Check that sensitive data is not in string representations
        user_repr = repr(user)
        token_repr = repr(token)
        bank_repr = repr(bank_link)
        
        # Sensitive data should not appear in representations
        assert "sensitive@secret.com" not in user_repr
        assert "super_secret_access_token" not in token_repr
        assert "super_secret_refresh_token" not in token_repr
        assert "secret_requisition_123" not in bank_repr
        assert "secret_institution_456" not in bank_repr
        
        # But non-sensitive data should appear
        assert "Test Bank" in bank_repr
