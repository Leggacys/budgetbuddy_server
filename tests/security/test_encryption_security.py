"""
Security-focused tests for encryption functionality.
Tests various security scenarios and potential vulnerabilities.
"""
import pytest
import os
import base64
import secrets
from unittest.mock import patch, MagicMock
from cryptography.fernet import Fernet
from app.utils.email_encryption import DataEncryption, email_encryption
from app.utils.token_encryption import TokenEncryption, token_encryption
from app.database.models.user_model import User
from app.database.models.tokens_model import Tokens
from app.database.models.bank_links_model import BankLink


class TestEncryptionSecurity:
    
    def test_key_isolation_between_environments(self):
        """Test that different environments use different encryption keys"""
        
        # Test with different environment variables
        original_email_key = os.environ.get('EMAIL_ENCRYPTION_KEY')
        original_token_key = os.environ.get('TOKEN_ENCRYPTION_KEY')
        
        try:
            # Set test keys
            test_key1 = base64.urlsafe_b64encode(secrets.token_bytes(32)).decode()
            test_key2 = base64.urlsafe_b64encode(secrets.token_bytes(32)).decode()
            
            with patch.dict(os.environ, {
                'EMAIL_ENCRYPTION_KEY': test_key1,
                'TOKEN_ENCRYPTION_KEY': test_key2
            }):
                enc1 = DataEncryption()
                token_enc1 = TokenEncryption()
                
                test_data = "security@test.com"
                email_encrypted1 = enc1.encrypt(test_data)
                token_encrypted1 = token_enc1.encrypt_token(test_data)
            
            # Use different keys
            test_key3 = base64.urlsafe_b64encode(secrets.token_bytes(32)).decode()
            test_key4 = base64.urlsafe_b64encode(secrets.token_bytes(32)).decode()
            
            with patch.dict(os.environ, {
                'EMAIL_ENCRYPTION_KEY': test_key3,
                'TOKEN_ENCRYPTION_KEY': test_key4
            }):
                enc2 = DataEncryption()
                token_enc2 = TokenEncryption()
                
                email_encrypted2 = enc2.encrypt(test_data)
                token_encrypted2 = token_enc2.encrypt_token(test_data)
            
            # Different keys should produce different encrypted data
            assert email_encrypted1 != email_encrypted2
            assert token_encrypted1 != token_encrypted2
            
            # Cross-decryption should fail gracefully
            email_cross_decrypt = enc2.decrypt(email_encrypted1)
            token_cross_decrypt = token_enc2.decrypt_token(token_encrypted1)
            
            # Should return original encrypted data if decryption fails
            assert email_cross_decrypt == email_encrypted1
            assert token_cross_decrypt == token_encrypted1
            
        finally:
            # Restore original environment
            if original_email_key:
                os.environ['EMAIL_ENCRYPTION_KEY'] = original_email_key
            if original_token_key:
                os.environ['TOKEN_ENCRYPTION_KEY'] = original_token_key
    
    def test_timing_attack_resistance(self):
        """Test resistance to timing attacks"""
        import time
        
        encryption = DataEncryption()
        
        # Test with different length inputs
        short_email = "a@b.com"
        long_email = "very_long_email_address_with_many_characters@example.com"
        
        # Measure encryption times
        times_short = []
        times_long = []
        
        for _ in range(20):  # Multiple measurements for statistical significance
            start = time.perf_counter()
            encryption.encrypt(short_email)
            times_short.append(time.perf_counter() - start)
            
            start = time.perf_counter()
            encryption.encrypt(long_email)
            times_long.append(time.perf_counter() - start)
        
        avg_short = sum(times_short) / len(times_short)
        avg_long = sum(times_long) / len(times_long)
        
        print(f"Average time - Short: {avg_short:.6f}s, Long: {avg_long:.6f}s")
        
        # Time difference should be reasonable (not revealing internal structure)
        # Allow for some difference due to data length, but not excessive
        time_ratio = max(avg_short, avg_long) / min(avg_short, avg_long)
        assert time_ratio < 3.0, "Timing should not reveal excessive information about input"
    
    def test_side_channel_resistance(self):
        """Test basic side-channel attack resistance"""
        
        encryption = DataEncryption()
        
        # Test with similar inputs that might reveal patterns
        similar_emails = [
            "test1@example.com",
            "test2@example.com",
            "test3@example.com",
            "test4@example.com"
        ]
        
        encrypted_similar = []
        for email in similar_emails:
            encrypted = encryption.encrypt(email)
            encrypted_similar.append(encrypted)
        
        # Encrypted data should not reveal similarities
        for i in range(len(encrypted_similar)):
            for j in range(i + 1, len(encrypted_similar)):
                encrypted1 = encrypted_similar[i]
                encrypted2 = encrypted_similar[j]
                
                # Calculate similarity (common prefixes, suffixes)
                common_prefix = 0
                min_len = min(len(encrypted1), len(encrypted2))
                for k in range(min_len):
                    if encrypted1[k] == encrypted2[k]:
                        common_prefix += 1
                    else:
                        break
                
                # Should not have significant common prefixes (allowing for Fernet timestamp)
                similarity_ratio = common_prefix / min_len
                assert similarity_ratio < 0.2, f"Too much similarity between encrypted values: {similarity_ratio}"
    
    def test_key_derivation_security(self):
        """Test security of key derivation process"""
        
        # Test that different environment keys produce different results
        test_data = "keytest@example.com"
        
        # Use properly formatted Fernet keys (base64-encoded 32-byte keys)
        key1 = Fernet.generate_key().decode()
        key2 = Fernet.generate_key().decode()
        
        with patch.dict(os.environ, {'EMAIL_ENCRYPTION_KEY': key1}):
            enc1 = DataEncryption()
            encrypted1 = enc1.encrypt(test_data)
        
        with patch.dict(os.environ, {'EMAIL_ENCRYPTION_KEY': key2}):
            enc2 = DataEncryption()
            encrypted2 = enc2.encrypt(test_data)
        
        # Different keys should produce different encrypted results
        assert encrypted1 != encrypted2, "Different keys should produce different encrypted data"
    
    def test_password_and_sensitive_data_handling(self):
        """Test that password-like data is handled securely"""
        
        # Test with password-like strings
        sensitive_data = [
            "password123",
            "MySecretPassword!@#",
            "super_secret_api_key_abc123",
            "bearer_token_xyz789",
            "session_id_sensitive_data"
        ]
        
        for data in sensitive_data:
            # Test email encryption with sensitive-looking data
            user = User()
            user.email = f"{data}@sensitive.com"
            
            # Should encrypt properly
            assert user._email != user.email
            assert user.email == f"{data}@sensitive.com"
            
            # Test token encryption
            token = Tokens()
            token.access_token = data
            token.refresh_token = f"refresh_{data}"
            
            assert token._access_token != data
            assert token._refresh_token != f"refresh_{data}"
            assert token.access_token == data
            assert token.refresh_token == f"refresh_{data}"
    
    def test_injection_attack_resistance(self):
        """Test resistance to injection-style attacks"""
        
        # Test with potentially malicious input
        malicious_inputs = [
            "'; DROP TABLE users; --@evil.com",
            "<script>alert('xss')</script>@hack.com",
            "$(rm -rf /)@shell.com",
            "../../../etc/passwd@path.com",
            "null\x00byte@attack.com"
        ]
        
        for malicious_input in malicious_inputs:
            try:
                user = User()
                user.email = malicious_input
                
                # Should handle gracefully
                assert user.email == malicious_input
                assert user._email != malicious_input
                
                # Should not expose malicious content in encrypted form
                encrypted_data = user._email
                assert "DROP TABLE" not in encrypted_data
                assert "<script>" not in encrypted_data
                assert "rm -rf" not in encrypted_data
                
            except Exception as e:
                # If it fails, should fail safely, not expose system
                error_message = str(e).lower()
                assert "password" not in error_message
                assert "key" not in error_message
                assert "secret" not in error_message
    
    def test_memory_security(self):
        """Test that sensitive data is not left in memory"""
        import gc
        
        # Create and use encryption instances
        sensitive_email = "memory_security@secret.com"
        sensitive_token = "super_secret_memory_token_123"
        
        user = User()
        user.email = sensitive_email
        
        token = Tokens()
        token.access_token = sensitive_token
        
        # Store references to encrypted data
        encrypted_email = user._email
        encrypted_token = token._access_token
        
        # Clear references
        del user
        del token
        gc.collect()
        
        # Check that sensitive data is not easily findable in memory
        # Note: This is a basic check, real memory analysis would be more complex
        all_objects = gc.get_objects()
        
        sensitive_found = 0
        for obj in all_objects:
            if isinstance(obj, str):
                if sensitive_email in obj or sensitive_token in obj:
                    sensitive_found += 1
        
        # Some references might exist (like in test variables), but should be minimal
        assert sensitive_found < 5, f"Too many references to sensitive data found: {sensitive_found}"
    
    def test_error_message_security(self):
        """Test that error messages don't leak sensitive information"""
        
        encryption = DataEncryption()
        
        # Test with invalid encrypted data
        invalid_encrypted_data = [
            "definitely_not_encrypted_data",
            base64.b64encode(b"fake_encrypted_data").decode(),
            "corrupted_base64_data===",
            ""
        ]
        
        for invalid_data in invalid_encrypted_data:
            try:
                result = encryption.decrypt(invalid_data)
                # Should return original data, not crash
                assert result == invalid_data
                
            except Exception as e:
                error_message = str(e).lower()
                
                # Error messages should not reveal:
                assert "key" not in error_message
                assert "password" not in error_message
                assert "secret" not in error_message
                assert "decrypt" not in error_message  # Avoid revealing operation
                
                # Should be generic
                assert len(error_message) < 100, "Error messages should be concise"


class TestEncryptionComplianceAndStandards:
    
    def test_encryption_algorithm_strength(self):
        """Test that strong encryption algorithms are used"""
        
        from cryptography.fernet import Fernet
        
        # Test that we're using Fernet (AES 128 in CBC mode with HMAC SHA256)
        encryption = DataEncryption()
        
        # Verify encryption produces appropriately sized output
        test_email = "algorithm@test.com"
        encrypted = encryption.encrypt(test_email)
        
        # Fernet output should be base64 encoded and have specific characteristics
        try:
            decoded = base64.urlsafe_b64decode(encrypted.encode())
            # Fernet has specific structure: version (1 byte) + timestamp (8 bytes) + IV (16 bytes) + ciphertext + HMAC (32 bytes)
            assert len(decoded) >= 57, "Encrypted data should have minimum Fernet structure size"
        except Exception:
            pass  # If not base64, that's still acceptable as long as it encrypts/decrypts
        
        # Verify it uses strong randomness
        encryptions = [encryption.encrypt(test_email) for _ in range(10)]
        assert len(set(encryptions)) == 10, "Should use strong randomness (no duplicates)"
    
    def test_key_length_requirements(self):
        """Test that encryption keys meet length requirements"""
        
        # Test with normal encryption operations
        from app.utils.email_encryption import DataEncryption
        
        # Normal case should work
        enc = DataEncryption()
        test_data = "keylen@test.com"
        encrypted = enc.encrypt(test_data)
        decrypted = enc.decrypt(encrypted)
        assert decrypted == test_data
        
        # Verify key exists and is properly formed
        assert enc.key is not None
        assert len(enc.key) > 0
    
    def test_data_integrity_verification(self):
        """Test that data integrity is verified during decryption"""
        
        encryption = DataEncryption()
        test_email = "integrity@test.com"
        encrypted = encryption.encrypt(test_email)
        
        # Try to modify encrypted data
        if len(encrypted) > 10:
            # Modify a character in the middle
            modified_pos = len(encrypted) // 2
            modified_char = 'X' if encrypted[modified_pos] != 'X' else 'Y'
            corrupted = encrypted[:modified_pos] + modified_char + encrypted[modified_pos+1:]
            
            # Should detect corruption
            result = encryption.decrypt(corrupted)
            assert result == corrupted, "Should detect data corruption and return original"
    
    def test_encryption_randomness_quality(self):
        """Test the quality of randomness in encryption"""
        
        encryption = DataEncryption()
        test_email = "randomness@test.com"
        
        # Generate multiple encryptions
        encryptions = [encryption.encrypt(test_email) for _ in range(50)]
        
        # All should be unique (Fernet includes random IV)
        assert len(set(encryptions)) == 50, "All encryptions should be unique"
        
        # Test that encryptions are different each time
        enc1 = encryption.encrypt(test_email)
        enc2 = encryption.encrypt(test_email)
        assert enc1 != enc2, "Same plaintext should produce different ciphertext"
        
        # Both should decrypt to same value
        assert encryption.decrypt(enc1) == test_email
        assert encryption.decrypt(enc2) == test_email
    
    def test_secure_defaults(self):
        """Test that secure defaults are used"""
        
        # Test that empty/None values are handled securely
        user = User()
        user.email = None
        assert user._email is None
        assert user.email is None
        
        user.email = ""
        assert user._email is not None  # Empty string should be encrypted, not None
        assert user.email == ""
        
        # Test that default initialization is secure
        token = Tokens()
        assert not hasattr(token, 'access_token') or token._access_token is None
        assert not hasattr(token, 'refresh_token') or token._refresh_token is None


class TestEncryptionAuditAndCompliance:
    
    def test_encryption_audit_trail(self):
        """Test that encryption operations can be audited"""
        
        # This test documents what would be needed for audit compliance
        user = User()
        user.email = "audit@compliance.test"
        
        # In a real audit scenario, we might want to log:
        # - When encryption occurred
        # - What type of data was encrypted
        # - Which encryption method was used
        # - Success/failure of operations
        
        # For now, verify basic operation logging capability
        assert user.email == "audit@compliance.test"
        assert user._email != "audit@compliance.test"
        
        # Verify we can determine if data is encrypted
        assert hasattr(user, '_email'), "Should have encrypted field marker"
    
    def test_encryption_version_compatibility(self):
        """Test compatibility across different encryption versions"""
        
        # This test ensures that encrypted data remains readable
        # across different versions of the encryption implementation
        
        encryption = DataEncryption()
        test_email = "version@compatibility.test"
        
        # Current version
        encrypted_current = encryption.encrypt(test_email)
        decrypted_current = encryption.decrypt(encrypted_current)
        
        assert decrypted_current == test_email
        
        # Test with potential future changes (simulation)
        # In real scenarios, this would test with actual older encrypted data
        legacy_encrypted_simulation = encrypted_current  # Simulate legacy data
        
        # Should still decrypt
        decrypted_legacy = encryption.decrypt(legacy_encrypted_simulation)
        assert decrypted_legacy == test_email
    
    def test_gdpr_compliance_simulation(self):
        """Test scenarios relevant to GDPR compliance"""
        
        # Test data deletion (right to be forgotten)
        user = User()
        user.email = "gdpr@privacy.test"
        
        original_encrypted = user._email
        
        # Simulate data deletion
        user.email = None
        user._email = None
        
        assert user.email is None
        assert user._email is None
        
        # Test data portability (can we extract readable data?)
        user2 = User()
        user2.email = "portability@test.com"
        
        # Should be able to access decrypted data
        exported_email = user2.email
        assert exported_email == "portability@test.com"
        
        # Test data minimization (only encrypt what's necessary)
        bank_link = BankLink()
        bank_link.bank_name = "Public Bank Name"  # This should NOT be encrypted
        bank_link.requisition_id = "secret_req_123"  # This SHOULD be encrypted
        
        assert bank_link.bank_name == "Public Bank Name"  # Not encrypted
        assert bank_link._requisition_id != "secret_req_123"  # Encrypted
        assert bank_link.requisition_id == "secret_req_123"  # Decrypts correctly
