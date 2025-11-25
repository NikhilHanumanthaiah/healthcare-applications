import uuid
from sqlalchemy import Column, Integer, String, DateTime, Boolean, UUID, CheckConstraint
from app.infrastructure.db.base import Base
from datetime import datetime, timezone


class Patient(Base):
    __tablename__ = "patients"

    patient_id = Column(
        UUID(as_uuid=True), primary_key=True, index=True, default=uuid.uuid4
    )
    first_name = Column(String, index=True)
    last_name = Column(String, index=True)
    date_of_birth = Column(DateTime(timezone=True))
    age = Column(Integer)
    gender = Column(
        String,
        CheckConstraint(
            "gender IN ('male', 'female', 'other')", name="gender_valid_values"
        ),
    )
    phone_number = Column(String, unique=True)
    email = Column(String, nullable=True)
    address = Column(String)
    created_date = Column(
        DateTime(timezone=True), default=lambda: datetime.now(timezone.utc)
    )
    updated_date = Column(
        DateTime(timezone=True),
        default=lambda: datetime.now(timezone.utc),
        onupdate=lambda: datetime.now(timezone.utc),
    )
    is_active = Column(Boolean, default=True)
    patient_type = Column(String, default="ADULT")
    guardian_name = Column(String, nullable=True)
    guardian_phone = Column(String, nullable=True)
