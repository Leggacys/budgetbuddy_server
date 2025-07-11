#!/usr/bin/env python3

import sys
import os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

# Mock the database base to avoid importing Quart
from sqlalchemy.ext.declarative import declarative_base
sys.modules['app.database.base'] = type('module', (), {'Base': declarative_base()})()

from datetime import datetime, timezone, timedelta
from app.database.models.tokens_model import Tokens
from app.utils.token_encryption import token_encryption

def test_tokens_model():
    print("Testing Tokens model...")
    
    # Test creating a token instance
    try:
        token = Tokens()
        print("✓ Token instance created successfully")
    except Exception as e:
        print(f"✗ Error creating token instance: {e}")
        return False
    
    # Test setting access token
    try:
        test_access_token = "test_access_token_123"
        token.access_token = test_access_token
        print("✓ Access token set successfully")
    except Exception as e:
        print(f"✗ Error setting access token: {e}")
        return False
    
    # Test getting access token
    try:
        retrieved_token = token.access_token
        if retrieved_token == test_access_token:
            print("✓ Access token retrieved and decrypted successfully")
        else:
            print(f"✗ Token mismatch: expected '{test_access_token}', got '{retrieved_token}'")
            return False
    except Exception as e:
        print(f"✗ Error getting access token: {e}")
        return False
    
    # Test setting refresh token
    try:
        test_refresh_token = "test_refresh_token_456"
        token.refresh_token = test_refresh_token
        print("✓ Refresh token set successfully")
    except Exception as e:
        print(f"✗ Error setting refresh token: {e}")
        return False
    
    # Test getting refresh token
    try:
        retrieved_refresh = token.refresh_token
        if retrieved_refresh == test_refresh_token:
            print("✓ Refresh token retrieved and decrypted successfully")
        else:
            print(f"✗ Token mismatch: expected '{test_refresh_token}', got '{retrieved_refresh}'")
            return False
    except Exception as e:
        print(f"✗ Error getting refresh token: {e}")
        return False
    
    # Test setting expiration dates
    try:
        now = datetime.now(timezone.utc)
        token.access_expires = now + timedelta(hours=1)
        token.refresh_expires = now + timedelta(days=30)
        print("✓ Expiration dates set successfully")
    except Exception as e:
        print(f"✗ Error setting expiration dates: {e}")
        return False
    
    # Test is_access_expired method
    try:
        is_expired = token.is_access_expired()
        print(f"✓ is_access_expired() returned: {is_expired}")
    except Exception as e:
        print(f"✗ Error calling is_access_expired(): {e}")
        return False
    
    # Test __repr__ method
    try:
        repr_str = repr(token)
        print(f"✓ __repr__() returned: {repr_str}")
    except Exception as e:
        print(f"✗ Error calling __repr__(): {e}")
        return False
    
    print("\n✓ All Tokens model tests passed!")
    return True

if __name__ == "__main__":
    test_tokens_model()
