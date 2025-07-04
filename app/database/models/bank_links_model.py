from datetime import datetime, timezone
from sqlalchemy.orm import relationship
import uuid
from sqlalchemy import UUID, Column, DateTime, ForeignKey, String
from app.database.base import Base


class BankLink(Base):
    __tablename__ = 'bank_links'

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    user_id = Column(UUID(as_uuid=True), ForeignKey('users.id'), nullable=False)
    requisition_id = Column(String, nullable=False, unique=True)
    institution_id = Column(String, nullable=False)
    bank_name = Column(String, nullable=False)
    created_at = Column(DateTime(timezone=True), default=datetime.now(timezone.utc))
    
    user = relationship("User", back_populates="bank_links")