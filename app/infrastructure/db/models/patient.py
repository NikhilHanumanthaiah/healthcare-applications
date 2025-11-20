from sqlalchemy import Column, Integer, String, DateTime, Boolean, UUID
from app.infrastructure.db.base import Base
from datetime import datetime, timezone


class Patient(Base):
    __tablename__ = "patients"

    patient_id = Column(UUID, primary_key=True, index=True)
    first_name = Column(String, index=True, unique=True)
    last_name = Column(String, index=True)
    date_of_birth = Column(DateTime(timezone=True))
    age = Column(Integer)
    gender = Column(String)
    phone_number = Column(String)
    address = Column(String)
    created_date = Column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc))
    updated_date = Column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc), onupdate=lambda: datetime.now(timezone.utc))
    is_active = Column(Boolean, default = True)
