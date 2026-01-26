from sqlalchemy import Boolean, Column, Integer, String, DateTime, ForeignKey
from datetime import datetime

# Import the Base from the database module
from db.database import Base

from models.user import User

class RefreshToken(Base):
    __tablename__ = "refreshtokens"

    id = Column(Integer, primary_key=True, index=True)
    token = Column(String, unique=True, index=True)
    
    expires_at = Column(DateTime, nullable=True)
    
    created_at = Column(DateTime, default=datetime.now)
    revoked_at = Column(DateTime, nullable=True)

    replaced_by_token = Column(String, index=True)
    reson_revoked = Column(String, index=True)

    is_expired = Column(Boolean, server_default='TRUE', nullable=False)
    is_revoked = Column(Boolean, server_default='TRUE', nullable=False)
    is_active = Column(Boolean, server_default='TRUE', nullable=False)

    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False)  
    # Foreign key to users table can be added if needed