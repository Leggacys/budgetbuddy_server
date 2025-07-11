from app.database.base import Base
import uuid
from datetime import datetime, timezone
from sqlalchemy import Column, String, DateTime, select
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.ext.hybrid import hybrid_property
from sqlalchemy.orm import relationship
from app.utils.email_encryption import email_encryption

class User(Base):
    __tablename__ = 'users'
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    _email = Column("email", String, nullable=False, unique=True, index=True)  # Store encrypted email
    created_at = Column(DateTime(timezone=True), default=datetime.now(timezone.utc))
    
    bank_links = relationship("BankLink", back_populates="user")
    
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        if not self.id:
            self.id = uuid.uuid4()
        if not self.created_at:
            self.created_at = datetime.now(timezone.utc)
    
    @hybrid_property
    def email(self):
        """Decrypt email when accessing it"""
        if self._email:
            return email_encryption.decrypt(self._email)
        return self._email
    
    @email.setter
    def email(self, value):
        """Encrypt email when setting it"""
        if value is not None:
            self._email = email_encryption.encrypt(value)
        else:
            self._email = None
    
    @staticmethod
    async def find_by_email(session, email):
        """Find user by email (handles encryption internally)"""
        # Get all users and compare decrypted emails
        # This is inefficient but necessary with Fernet encryption
        result = await session.execute(select(User))
        users = result.scalars().all()
        
        for user in users:
            try:
                if user.email == email:
                    return user
            except Exception:
                # Skip users with corrupted email data
                continue
        return None
    
    def __repr__(self):
        # Don't expose the actual email in repr for security
        email_preview = f"{self.email[:3]}***" if self.email and len(self.email) > 3 else "***"
        return f"<User(id={self.id}, email={email_preview})>"