from sqlalchemy import Column, Integer, String, DateTime, ForeignKey
from sqlalchemy.dialects.sqlite import JSON
from sqlalchemy.orm import relationship
from datetime import datetime
from database import Base

class NFTImage(Base):
    __tablename__ = "nft_images"

    id = Column(Integer, primary_key=True)
    filename = Column(String, nullable=False)
    title = Column(String, nullable=False, default="")
    layers = Column(JSON, nullable=False)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)
    user = relationship("User")