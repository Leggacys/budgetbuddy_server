from sqlalchemy import Column, DateTime, Integer, String
from sqlalchemy.ext.hybrid import hybrid_property
from app.database.base import Base
from app.utils.token_encryption import token_encryption


class Tokens(Base):
    __tablename__ = 'tokens'

    id = Column(Integer, primary_key=True)
    _access_token = Column("access_token", String, nullable=False)  # Encrypted storage
    access_expires = Column(DateTime(timezone=True), nullable=False)
    _refresh_token = Column("refresh_token", String, nullable=False)  # Encrypted storage
    refresh_expires = Column(DateTime(timezone=True), nullable=False)
    
    @hybrid_property
    def access_token(self):
        """Decrypt access token when accessing"""
        try:
            # Get the raw attribute value
            raw_value = object.__getattribute__(self, '_access_token')
            
            # Handle None or empty strings
            if raw_value is None or raw_value == "":
                return raw_value
            
            # Only decrypt if it's a string (encrypted value)
            if isinstance(raw_value, str):
                return token_encryption.decrypt_token(raw_value)
            
            # For SQL query expressions, return the column
            return raw_value
        except AttributeError:
            # Attribute doesn't exist yet
            return None
        except Exception as e:
            # If anything goes wrong, return None
            return None
    
    @access_token.setter
    def access_token(self, value):
        """Encrypt access token when setting"""
        if value is not None and value != "":
            self._access_token = token_encryption.encrypt_token(value)
        else:
            # Handle both None and empty string consistently
            if value == "":
                self._access_token = token_encryption.encrypt_token("")
            else:
                self._access_token = None
    
    @hybrid_property
    def refresh_token(self):
        """Decrypt refresh token when accessing"""
        try:
            # Get the raw attribute value
            raw_value = object.__getattribute__(self, '_refresh_token')
            
            # Handle None or empty strings
            if raw_value is None or raw_value == "":
                return raw_value
            
            # Only decrypt if it's a string (encrypted value)
            if isinstance(raw_value, str):
                return token_encryption.decrypt_token(raw_value)
            
            # For SQL query expressions, return the column
            return raw_value
        except AttributeError:
            # Attribute doesn't exist yet
            return None
        except Exception as e:
            # If anything goes wrong, return None
            return None
    
    @refresh_token.setter
    def refresh_token(self, value):
        """Encrypt refresh token when setting"""
        if value is not None and value != "":
            self._refresh_token = token_encryption.encrypt_token(value)
        else:
            # Handle both None and empty string consistently
            if value == "":
                self._refresh_token = token_encryption.encrypt_token("")
            else:
                self._refresh_token = None
    
    def is_access_expired(self):
        """Check if access token is expired"""
        from datetime import datetime, timezone
        return datetime.now(timezone.utc) > self.access_expires
    
    def is_refresh_expired(self):
        """Check if refresh token is expired"""
        from datetime import datetime, timezone
        return datetime.now(timezone.utc) > self.refresh_expires
    
    def __repr__(self):
        return f"<Tokens(id={self.id}, access_expires={self.access_expires}, refresh_expires={self.refresh_expires})>"

