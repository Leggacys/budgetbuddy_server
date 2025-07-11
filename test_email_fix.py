#!/usr/bin/env python3
"""
Test script to verify the email decryption fix
"""
from app.database.models.user_model import User
from app.utils.email_encryption import email_encryption

def test_email_decryption_fix():
    print("🔧 Testing email decryption fix...")
    
    # Test 1: Basic email encryption/decryption
    print("📧 Test 1: Basic email handling")
    user1 = User()
    user1.email = "test@example.com"
    print(f"  Set email: test@example.com")
    print(f"  Retrieved email: {user1.email}")
    print(f"  Encrypted value: {user1._email[:50]}...")
    assert user1.email == "test@example.com"
    print("  ✅ Basic email test PASSED")
    
    # Test 2: Empty string handling
    print("📭 Test 2: Empty string handling")
    user2 = User()
    user2.email = ""
    print(f"  Set email: ''")
    print(f"  Retrieved email: '{user2.email}'")
    assert user2.email == ""
    print("  ✅ Empty string test PASSED")
    
    # Test 3: None value handling
    print("🚫 Test 3: None value handling")
    user3 = User()
    user3.email = None
    print(f"  Set email: None")
    print(f"  Retrieved email: {user3.email}")
    assert user3.email is None
    print("  ✅ None value test PASSED")
    
    # Test 4: Multiple users with different emails
    print("👥 Test 4: Multiple users")
    users = []
    emails = ["alice@test.com", "bob@test.com", "", None, "charlie@test.com"]
    
    for email in emails:
        user = User()
        user.email = email
        users.append(user)
        print(f"  Created user with email: {email} -> Retrieved: {user.email}")
    
    # Verify all emails are correctly stored and retrieved
    for i, expected_email in enumerate(emails):
        retrieved_email = users[i].email
        assert retrieved_email == expected_email, f"Email mismatch: expected {expected_email}, got {retrieved_email}"
    
    print("  ✅ Multiple users test PASSED")
    
    print("\n🎉 All email decryption tests PASSED!")
    print("✅ The InstrumentedAttribute error has been fixed!")

if __name__ == "__main__":
    test_email_decryption_fix()
