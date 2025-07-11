from datetime import datetime, timezone
from sqlalchemy.orm import relationship
from sqlalchemy.ext.hybrid import hybrid_property
import uuid
from sqlalchemy import UUID, Column, DateTime, ForeignKey, String
from app.database.base import Base
from app.utils.email_encryption import email_encryption  # Reuse existing encryption


class BankLink(Base):
    __tablename__ = 'bank_links'

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    user_id = Column(UUID(as_uuid=True), ForeignKey('users.id'), nullable=False)
    _requisition_id = Column("requisition_id", String, nullable=False, unique=True)  # 🔐 Encrypted
    _institution_id = Column("institution_id", String, nullable=False)              # 🔐 Encrypted
    bank_name = Column(String, nullable=False) 
    created_at = Column(DateTime(timezone=True), default=datetime.now(timezone.utc))
    
    user = relationship("User", back_populates="bank_links")
    
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        if not self.id:
            self.id = uuid.uuid4()
        if not self.created_at:
            self.created_at = datetime.now(timezone.utc)
    
    @hybrid_property
    def requisition_id(self):
        """Decrypt requisition_id when accessing"""
        if self._requisition_id:
            return email_encryption.decrypt(self._requisition_id)
        return self._requisition_id
    
    @requisition_id.setter
    def requisition_id(self, value):
        """Encrypt requisition_id when setting"""
        if value is not None:
            self._requisition_id = email_encryption.encrypt(value)
        else:
            self._requisition_id = None
    
    @hybrid_property
    def institution_id(self):
        """Decrypt institution_id when accessing"""
        if self._institution_id:
            return email_encryption.decrypt(self._institution_id)
        return self._institution_id
    
    @institution_id.setter
    def institution_id(self, value):
        """Encrypt institution_id when setting"""
        if value is not None:
            self._institution_id = email_encryption.encrypt(value)
        else:
            self._institution_id = None
    
    def __repr__(self):
        return f"<BankLink(id={self.id}, bank_name={self.bank_name}, user_id={self.user_id})>"