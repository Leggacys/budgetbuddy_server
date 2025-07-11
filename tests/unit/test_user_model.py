import uuid
from app.database.models.user_model import User

class TestUserModel:
    
    def test_user_creation(self):
        """Test basic user creation"""
        user = User()
        user.email = "test@example.com"
        
        assert user.email == "test@example.com"
        assert user.id is not None
        assert isinstance(user.id, uuid.UUID)
        assert user.created_at is not None
    
    def test_email_encryption(self):
        """Test that email is encrypted in database"""
        user = User()
        user.email = "encrypted@example.com"
        
        # The internal _email should be encrypted (different from original)
        assert user._email != "encrypted@example.com"
        assert user._email is not None
        assert len(user._email) > len("encrypted@example.com")
        
        # The public email property should be decrypted
        assert user.email == "encrypted@example.com"
    
    def test_empty_email(self):
        """Test user with empty email"""
        user = User()
        user.email = ""
        
        assert user.email == ""
        assert user._email == ""
    
    def test_none_email(self):
        """Test user with None email"""
        user = User()
        user.email = None
        
        assert user.email is None
        assert user._email is None
    
    def test_user_repr(self):
        """Test user string representation"""
        user = User()
        user.email = "repr@example.com"
        
        repr_str = repr(user)
        assert "User" in repr_str
        assert "rep***" in repr_str  # Should show masked email for security
        assert str(user.id) in repr_str
    
    def test_multiple_users_unique_ids(self):
        """Test that multiple users get unique IDs"""
        user1 = User()
        user2 = User()
        
        assert user1.id != user2.id
        assert isinstance(user1.id, uuid.UUID)
        assert isinstance(user2.id, uuid.UUID)
