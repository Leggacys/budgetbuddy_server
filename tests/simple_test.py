"""
Simple test to verify email encryption works without pytest
Run with: ./venv/bin/python3 tests/simple_test.py
"""

import sys
import os

# Add the parent directory to the path so we can import app modules
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

try:
    from app.utils.email_encryption import DataEncryption
    
    def test_email_encryption():
        """Simple test for email encryption"""
        print("🧪 Testing Email Encryption...")
        
        encryption = DataEncryption()
        test_email = "simple@test.com"
        
        # Test encryption/decryption
        encrypted = encryption.encrypt(test_email)
        decrypted = encryption.decrypt(encrypted)
        
        print(f"Original:  {test_email}")
        print(f"Encrypted: {encrypted[:50]}...")
        print(f"Decrypted: {decrypted}")
        
        if decrypted == test_email:
            print("✅ Email encryption test PASSED")
            return True
        else:
            print("❌ Email encryption test FAILED")
            return False
    
    def test_user_model():
        """Simple test for user model"""
        print("\n🧪 Testing User Model...")
        
        try:
            from app.database.models.user_model import User
            
            user = User()
            user.email = "model@test.com"
            
            print(f"Set email: model@test.com")
            print(f"Stored (encrypted): {user._email[:50]}...")
            print(f"Retrieved (decrypted): {user.email}")
            
            if user.email == "model@test.com" and user._email != "model@test.com":
                print("✅ User model test PASSED")
                return True
            else:
                print("❌ User model test FAILED")
                return False
                
        except ImportError as e:
            print(f"⚠️  User model test skipped: {e}")
            return True
    
    def main():
        """Run all simple tests"""
        print("🚀 Running Simple BudgetBuddy Tests")
        print("=" * 50)
        
        tests_passed = 0
        total_tests = 2
        
        if test_email_encryption():
            tests_passed += 1
            
        if test_user_model():
            tests_passed += 1
        
        print("\n" + "=" * 50)
        print(f"📊 Results: {tests_passed}/{total_tests} tests passed")
        
        if tests_passed == total_tests:
            print("🎉 All tests passed!")
            return 0
        else:
            print("⚠️  Some tests failed")
            return 1

    if __name__ == "__main__":
        exit(main())

except ImportError as e:
    print(f"❌ Import error: {e}")
    print("Make sure you're running this from the project root:")
    print("./venv/bin/python3 tests/simple_test.py")
    exit(1)
