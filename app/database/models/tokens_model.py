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
        if self._access_token:
            return token_encryption.decrypt_token(self._access_token)
        return self._access_token
    
    @access_token.setter
    def access_token(self, value):
        """Encrypt access token when setting"""
        if value is not None:
            self._access_token = token_encryption.encrypt_token(value)
        else:
            self._access_token = None
    
    @hybrid_property
    def refresh_token(self):
        """Decrypt refresh token when accessing"""
        if self._refresh_token:
            return token_encryption.decrypt_token(self._refresh_token)
        return self._refresh_token
    
    @refresh_token.setter
    def refresh_token(self, value):
        """Encrypt refresh token when setting"""
        if value is not None:
            self._refresh_token = token_encryption.encrypt_token(value)
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

