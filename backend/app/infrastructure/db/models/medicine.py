from sqlalchemy import Column, Integer, String, Float, DateTime, Boolean
from app.infrastructure.db.base import Base
from datetime import datetime, timezone

class Medicine(Base):
    __tablename__ = "medicines"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True, unique=True)
    price_per_unit = Column(Float)
    stock = Column(Integer)
    created_date = Column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc))
    updated_date = Column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc), onupdate=lambda: datetime.now(timezone.utc))
    is_deleted = Column(Boolean, default=False)
    deleted_at = Column(DateTime(timezone=True), nullable=True)
