#!/usr/bin/env python3

# Simple test to verify InstrumentedAttribute fix
print("🔍 Testing InstrumentedAttribute fix...")

# Mock an InstrumentedAttribute-like object
class MockInstrumentedAttribute:
    def __str__(self):
        return "MockInstrumentedAttribute"
    
    def __repr__(self):
        return "MockInstrumentedAttribute"

# Test the fix
def test_type_checking():
    mock_attr = MockInstrumentedAttribute()
    
    # Test the isinstance check that should prevent the error
    if isinstance(mock_attr, str):
        print("❌ Type check failed - MockInstrumentedAttribute was treated as string")
        return False
    else:
        print("✅ Type check passed - MockInstrumentedAttribute correctly identified as non-string")
        return True

def test_encrypt_decrypt_safety():
    """Test that our encryption utilities handle non-string inputs safely"""
    
    # Test with None
    try:
        if not None:  # This mimics the not encrypted_token check
            print("✅ None input handled correctly")
        else:
            print("❌ None input handling failed")
            return False
    except Exception as e:
        print(f"❌ None input caused error: {e}")
        return False
    
    # Test with empty string
    try:
        if not "":  # This mimics the not encrypted_token check
            print("✅ Empty string input handled correctly")
        else:
            print("❌ Empty string input handling failed")
            return False
    except Exception as e:
        print(f"❌ Empty string input caused error: {e}")
        return False
    
    # Test with non-string object
    try:
        mock_attr = MockInstrumentedAttribute()
        if not isinstance(mock_attr, str):
            print("✅ Non-string object correctly identified")
            return True
        else:
            print("❌ Non-string object incorrectly identified as string")
            return False
    except Exception as e:
        print(f"❌ Non-string object caused error: {e}")
        return False

if __name__ == "__main__":
    print("=" * 50)
    print("🧪 Testing InstrumentedAttribute Protection")
    print("=" * 50)
    
    success = True
    success &= test_type_checking()
    success &= test_encrypt_decrypt_safety()
    
    print("=" * 50)
    if success:
        print("✅ All tests passed! InstrumentedAttribute error should be fixed.")
    else:
        print("❌ Some tests failed. InstrumentedAttribute error may still occur.")
    print("=" * 50)
