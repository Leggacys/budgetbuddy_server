from sqlalchemy import Column, DateTime, Integer, String
from app.database.base import Base


class Tokens(Base):
    __tablename__ = 'tokens'

    id = Column(Integer, primary_key=True)
    access_token = Column(String,nullable= False)
    access_expires = Column(DateTime(timezone=True), nullable=False)
    refresh_token = Column(String,nullable=False)
    refresh_expires = Column(DateTime(timezone=True),nullable=False)
    
    