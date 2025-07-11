"""
Advanced performance tests for encryption operations.
Tests various performance scenarios and optimization opportunities.
"""
import pytest
import time
import threading
import gc
import sys
from unittest.mock import patch
from app.utils.email_encryption import DataEncryption, email_encryption
from app.utils.token_encryption import TokenEncryption, token_encryption
from app.database.models.user_model import User
from app.database.models.tokens_model import Tokens
from app.database.models.bank_links_model import BankLink


class TestEncryptionPerformanceScenarios:
    
    def test_bulk_user_creation_performance(self):
        """Test performance of creating many users with encrypted emails"""
        
        start_time = time.time()
        users = []
        
        # Create 500 users (reduced for CI/testing)
        for i in range(500):
            user = User()
            user.email = f"bulk_user_{i}@performance.test"
            users.append(user)
        
        end_time = time.time()
        creation_time = end_time - start_time
        
        print(f"Creating 500 users with encrypted emails took {creation_time:.3f} seconds")
        
        # Verify all were created correctly
        assert len(users) == 500
        for i, user in enumerate(users):
            assert user.email == f"bulk_user_{i}@performance.test"
            assert user._email != user.email  # Encrypted
        
        # Performance assertion
        assert creation_time < 5.0, "Bulk user creation should complete in reasonable time"
    
    def test_encryption_key_derivation_performance(self):
        """Test the performance of key derivation operations"""
        
        # Test key derivation for both encryption types
        start_time = time.time()
        
        # Create multiple encryption instances (triggers key derivation)
        email_encryptions = [DataEncryption() for _ in range(10)]
        token_encryptions = [TokenEncryption() for _ in range(10)]
        
        end_time = time.time()
        derivation_time = end_time - start_time
        
        print(f"Creating 20 encryption instances took {derivation_time:.3f} seconds")
        
        # Verify they work
        test_email = "keyderive@test.com"
        test_token = "key_derive_token_123"
        
        for enc in email_encryptions:
            encrypted = enc.encrypt(test_email)
            assert enc.decrypt(encrypted) == test_email
        
        for enc in token_encryptions:
            encrypted = enc.encrypt_token(test_token)
            assert enc.decrypt_token(encrypted) == test_token
        
        assert derivation_time < 3.0, "Key derivation should be reasonably fast"
    
    def test_large_data_encryption_performance(self):
        """Test encryption performance with large data"""
        
        # Create large email and token data
        large_email = "large_" + "x" * 1000 + "@example.com"
        large_token = "large_token_" + "y" * 5000
        
        email_enc = DataEncryption()
        token_enc = TokenEncryption()
        
        # Test email encryption
        start_time = time.time()
        encrypted_email = email_enc.encrypt(large_email)
        decrypted_email = email_enc.decrypt(encrypted_email)
        email_time = time.time() - start_time
        
        assert decrypted_email == large_email
        print(f"Large email encrypt/decrypt took {email_time:.3f} seconds")
        
        # Test token encryption
        start_time = time.time()
        encrypted_token = token_enc.encrypt_token(large_token)
        decrypted_token = token_enc.decrypt_token(encrypted_token)
        token_time = time.time() - start_time
        
        assert decrypted_token == large_token
        print(f"Large token encrypt/decrypt took {token_time:.3f} seconds")
        
        # Performance assertions
        assert email_time < 0.1, "Large email encryption should be fast"
        assert token_time < 0.1, "Large token encryption should be fast"
    
    def test_concurrent_encryption_performance(self):
        """Test encryption performance under concurrent load"""
        import threading
        
        results = []
        errors = []
        start_time = time.time()
        
        def encryption_worker(worker_id):
            """Worker function for concurrent encryption"""
            try:
                local_results = []
                
                for i in range(50):  # Reduced iterations
                    # Test email encryption
                    user = User()
                    user.email = f"concurrent_{worker_id}_{i}@test.com"
                    
                    # Test token encryption
                    token = Tokens()
                    token.access_token = f"access_token_{worker_id}_{i}"
                    token.refresh_token = f"refresh_token_{worker_id}_{i}"
                    
                    # Verify correctness
                    assert user.email == f"concurrent_{worker_id}_{i}@test.com"
                    assert token.access_token == f"access_token_{worker_id}_{i}"
                    assert token.refresh_token == f"refresh_token_{worker_id}_{i}"
                    
                    local_results.append((user, token))
                
                results.extend(local_results)
                
            except Exception as e:
                errors.append(e)
        
        # Create and start worker threads
        threads = []
        for worker_id in range(5):  # 5 concurrent workers
            thread = threading.Thread(target=encryption_worker, args=(worker_id,))
            threads.append(thread)
            thread.start()
        
        # Wait for completion
        for thread in threads:
            thread.join()
        
        end_time = time.time()
        total_time = end_time - start_time
        
        print(f"Concurrent encryption (5 workers × 50 operations) took {total_time:.3f} seconds")
        
        # Verify results
        assert len(errors) == 0, f"Errors occurred: {errors}"
        assert len(results) == 250  # 5 workers × 50 operations
        
        assert total_time < 10.0, "Concurrent encryption should complete in reasonable time"
    
    def test_memory_usage_during_encryption(self):
        """Test memory usage patterns during encryption operations"""
        import gc
        
        # Force garbage collection and get baseline
        gc.collect()
        initial_objects = len(gc.get_objects())
        
        # Perform many encryption operations
        users = []
        for i in range(200):
            user = User()
            user.email = f"memory_test_{i}@example.com"
            users.append(user)
            
            # Periodically collect garbage
            if i % 50 == 0:
                gc.collect()
        
        # Check memory usage
        gc.collect()
        final_objects = len(gc.get_objects())
        object_increase = final_objects - initial_objects
        
        print(f"Memory test created {object_increase} new objects for 200 users")
        
        # Clear references and collect garbage
        users.clear()
        gc.collect()
        cleanup_objects = len(gc.get_objects())
        
        # Memory should be mostly freed
        remaining_increase = cleanup_objects - initial_objects
        print(f"After cleanup, {remaining_increase} objects remain")
        
        # Allow for some increase but not excessive
        assert object_increase < 2000, "Memory usage should be reasonable"
        assert remaining_increase < 200, "Memory should be freed after cleanup"
    
    def test_encryption_cache_behavior(self):
        """Test if encryption benefits from any caching mechanisms"""
        
        email_enc = DataEncryption()
        test_email = "cache_test@example.com"
        
        # Time first encryption (may include setup costs)
        start_time = time.time()
        encrypted1 = email_enc.encrypt(test_email)
        first_time = time.time() - start_time
        
        # Time subsequent encryptions
        times = []
        for _ in range(10):
            start_time = time.time()
            encrypted = email_enc.encrypt(test_email)
            times.append(time.time() - start_time)
        
        average_time = sum(times) / len(times)
        
        print(f"First encryption: {first_time:.4f}s, Average subsequent: {average_time:.4f}s")
        
        # All encryptions should produce different results (no caching of output)
        all_encrypted = [encrypted1] + [email_enc.encrypt(test_email) for _ in range(5)]
        assert len(set(all_encrypted)) == len(all_encrypted), "Each encryption should be unique"
        
        # But all should decrypt correctly
        for encrypted in all_encrypted:
            assert email_enc.decrypt(encrypted) == test_email


class TestEncryptionScalabilityTests:
    
    def test_user_database_simulation_performance(self):
        """Test performance simulation of a database with many users"""
        
        # Simulate a user database
        user_database = {}
        
        start_time = time.time()
        
        # Create users
        for i in range(1000):
            user = User()
            user.email = f"user_{i}@scalability.test"
            user_database[str(user.id)] = user
        
        creation_time = time.time() - start_time
        print(f"Created 1000 users in {creation_time:.3f} seconds")
        
        # Test lookup performance
        start_time = time.time()
        
        # Perform lookups
        for i in range(100):
            search_email = f"user_{i}@scalability.test"  # Search for existing users only
            found_user = None
            
            # Linear search simulation
            for user_id, user in user_database.items():
                if user.email == search_email:
                    found_user = user
                    break
            
            assert found_user is not None, f"Could not find user with email {search_email}"
        
        lookup_time = time.time() - start_time
        print(f"100 email lookups in 1000 users took {lookup_time:.3f} seconds")
        
        # Performance assertions
        assert creation_time < 10.0, "Creating 1000 users should be reasonably fast"
        assert lookup_time < 5.0, "Lookups should be reasonably fast"
    
    def test_bank_link_scalability(self):
        """Test performance with many bank links"""
        
        start_time = time.time()
        
        # Create many bank links
        bank_links = []
        for i in range(500):
            link = BankLink()
            link.requisition_id = f"req_scale_{i}_{'x' * 20}"
            link.institution_id = f"BANK_SCALE_{i % 10}"  # 10 different banks
            link.bank_name = f"Scale Bank {i % 10}"
            bank_links.append(link)
        
        creation_time = time.time() - start_time
        print(f"Created 500 bank links in {creation_time:.3f} seconds")
        
        # Test searching by institution
        start_time = time.time()
        
        for bank_id in range(10):
            institution_search = f"BANK_SCALE_{bank_id}"
            found_links = [
                link for link in bank_links 
                if link.institution_id == institution_search
            ]
            assert len(found_links) == 50  # Should find 50 per bank
        
        search_time = time.time() - start_time
        print(f"Searched 500 bank links 10 times in {search_time:.3f} seconds")
        
        assert creation_time < 5.0, "Bank link creation should be fast"
        assert search_time < 2.0, "Bank link searches should be fast"
    
    def test_mixed_workload_performance(self):
        """Test performance with mixed operations (create, read, update)"""
        
        users = []
        tokens = []
        bank_links = []
        
        start_time = time.time()
        
        # Mixed operations
        for i in range(100):
            # Create user
            user = User()
            user.email = f"mixed_{i}@test.com"
            users.append(user)
            
            # Create tokens
            token = Tokens()
            token.access_token = f"access_mixed_{i}"
            token.refresh_token = f"refresh_mixed_{i}"
            tokens.append(token)
            
            # Create bank link
            link = BankLink()
            link.requisition_id = f"req_mixed_{i}"
            link.institution_id = f"BANK_MIXED_{i % 5}"
            link.bank_name = f"Mixed Bank {i % 5}"
            bank_links.append(link)
            
            # Update operations (every 10th iteration)
            if i % 10 == 0 and i > 0:
                # Update existing user email
                users[i-10].email = f"updated_mixed_{i-10}@test.com"
                
                # Update existing token
                tokens[i-10].access_token = f"updated_access_{i-10}"
        
        total_time = time.time() - start_time
        print(f"Mixed workload (300 creates + 20 updates) took {total_time:.3f} seconds")
        
        # Verify some updates worked
        assert users[0].email == "updated_mixed_0@test.com"
        assert tokens[0].access_token == "updated_access_0"
        
        assert total_time < 8.0, "Mixed workload should complete in reasonable time"


class TestEncryptionOptimizationOpportunities:
    
    def test_encryption_instance_reuse_performance(self):
        """Test performance benefit of reusing encryption instances"""
        
        # Test creating new instances each time
        start_time = time.time()
        for i in range(100):
            enc = DataEncryption()
            encrypted = enc.encrypt(f"test_{i}@example.com")
            decrypted = enc.decrypt(encrypted)
        new_instance_time = time.time() - start_time
        
        # Test reusing single instance
        enc = DataEncryption()
        start_time = time.time()
        for i in range(100):
            encrypted = enc.encrypt(f"test_{i}@example.com")
            decrypted = enc.decrypt(encrypted)
        reuse_instance_time = time.time() - start_time
        
        print(f"New instances: {new_instance_time:.3f}s, Reused instance: {reuse_instance_time:.3f}s")
        
        # Reusing should be faster (less key derivation overhead)
        improvement_ratio = new_instance_time / reuse_instance_time
        assert improvement_ratio > 1.5, "Reusing encryption instances should provide performance benefit"
    
    def test_global_encryption_instance_performance(self):
        """Test performance of using global encryption instances"""
        
        # Test using global instances (like in the models)
        start_time = time.time()
        
        for i in range(200):
            # This uses the global email_encryption instance
            encrypted = email_encryption.encrypt(f"global_{i}@test.com")
            decrypted = email_encryption.decrypt(encrypted)
            
            # This uses the global token_encryption instance
            token_encrypted = token_encryption.encrypt_token(f"global_token_{i}")
            token_decrypted = token_encryption.decrypt_token(token_encrypted)
        
        global_time = time.time() - start_time
        print(f"Using global instances for 400 operations took {global_time:.3f} seconds")
        
        assert global_time < 3.0, "Global encryption instances should be fast"
    
    def test_batch_operation_potential(self):
        """Test potential for batch encryption operations"""
        
        # Simulate individual encryptions
        emails = [f"batch_{i}@test.com" for i in range(100)]
        
        start_time = time.time()
        encrypted_individually = []
        for email in emails:
            encrypted = email_encryption.encrypt(email)
            encrypted_individually.append(encrypted)
        individual_time = time.time() - start_time
        
        # Note: Current implementation doesn't support batch operations
        # This test documents the current performance baseline
        print(f"Individual encryption of 100 emails took {individual_time:.3f} seconds")
        
        # Verify all were encrypted correctly
        for i, encrypted in enumerate(encrypted_individually):
            decrypted = email_encryption.decrypt(encrypted)
            assert decrypted == emails[i]
        
        # Document current performance for future optimization reference
        assert individual_time < 2.0, "Individual encryptions should complete in reasonable time"
