import os
import base64
from cryptography.fernet import Fernet
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC


class DataEncryption:
    def __init__(self):
        self.key = self._get_or_create_key()
        self.cipher = Fernet(self.key)
    
    def _get_or_create_key(self):
        """Get encryption key from environment or generate from password"""
        # Try to get existing key from environment
        key_string = os.getenv("EMAIL_ENCRYPTION_KEY")
        if key_string:
            return key_string.encode()
        
        # Generate key from password and salt
        password = os.getenv("DB_PASSWORD", "budgetbuddy-email-secure-2024").encode()
        salt = os.getenv("DB_SALT", "budgetbuddy-email-salt-2024").encode()
        
        kdf = PBKDF2HMAC(
            algorithm=hashes.SHA256(),
            length=32,
            salt=salt,
            iterations=100000,
        )
        key = base64.urlsafe_b64encode(kdf.derive(password))
        return key
    
    def encrypt(self, email: str) -> str:
        """Encrypt email address"""
        if not email:
            return email
        
        try:
            encrypted = self.cipher.encrypt(email.encode())
            return base64.urlsafe_b64encode(encrypted).decode()
        except Exception as e:
            print(f"❌ Email encryption error: {e}")
            return email  # Return original if encryption fails
    
    def decrypt(self, encrypted_email: str) -> str:
        """Decrypt email address"""
        if not encrypted_email:
            return encrypted_email
        
        try:
            decoded = base64.urlsafe_b64decode(encrypted_email.encode())
            decrypted = self.cipher.decrypt(decoded)
            return decrypted.decode()
        except Exception as e:
            print(f"❌ Email decryption error: {e}")
            return encrypted_email  # Return original if decryption fails
        
email_encryption = DataEncryption()


def test_email_encryption():
    """Test email encryption/decryption"""
    test_email = "user@example.com"
    encrypted = email_encryption.encrypt(test_email)
    decrypted = email_encryption.decrypt(encrypted)
    
    print(f"Original: {test_email}")
    print(f"Encrypted: {encrypted}")
    print(f"Decrypted: {decrypted}")
    print(f"Match: {test_email == decrypted}")


if __name__ == "__main__":
    test_email_encryption()

