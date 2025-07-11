import os
import base64
from cryptography.fernet import Fernet
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC


class TokenEncryption:
    def __init__(self):
        self.key = self._get_or_create_key()
        self.cipher = Fernet(self.key)
    
    def _get_or_create_key(self):
        """Get encryption key for tokens"""
        # Try to get existing key from environment
        key_string = os.getenv("TOKEN_ENCRYPTION_KEY")
        if key_string:
            return key_string.encode()
        
        # Generate key from password and salt (different from email)
        password = os.getenv("TOKEN_PASSWORD", "budgetbuddy-token-secure-2024").encode()
        salt = os.getenv("TOKEN_SALT", "budgetbuddy-token-salt-2024").encode()
        
        kdf = PBKDF2HMAC(
            algorithm=hashes.SHA256(),
            length=32,
            salt=salt,
            iterations=100000,
        )
        key = base64.urlsafe_b64encode(kdf.derive(password))
        return key
    
    def encrypt_token(self, token: str) -> str:
        """Encrypt token string"""
        if not token:
            return token
        
        try:
            encrypted = self.cipher.encrypt(token.encode())
            return base64.urlsafe_b64encode(encrypted).decode()
        except Exception as e:
            print(f"❌ Token encryption error: {e}")
            return token  # Return original if encryption fails
    
    def decrypt_token(self, encrypted_token: str) -> str:
        """Decrypt token string"""
        if not encrypted_token:
            return encrypted_token
        
        try:
            decoded = base64.urlsafe_b64decode(encrypted_token.encode())
            decrypted = self.cipher.decrypt(decoded)
            return decrypted.decode()
        except Exception as e:
            print(f"❌ Token decryption error: {e}")
            return encrypted_token  # Return original if decryption fails


# Global instance for token encryption
token_encryption = TokenEncryption()


# Test function
def test_token_encryption():
    """Test token encryption/decryption"""
    test_token = "access_token_1234567890abcdef"
    encrypted = token_encryption.encrypt_token(test_token)
    decrypted = token_encryption.decrypt_token(encrypted)
    
    print(f"Original: {test_token}")
    print(f"Encrypted: {encrypted}")
    print(f"Decrypted: {decrypted}")
    print(f"Match: {test_token == decrypted}")


if __name__ == "__main__":
    test_token_encryption()