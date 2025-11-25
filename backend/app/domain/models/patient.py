from dataclasses import dataclass
from typing import Optional
from uuid import UUID
from datetime import datetime


from enum import Enum


class PatientType(str, Enum):
    ADULT = "ADULT"
    PEDIATRIC = "PEDIATRIC"


@dataclass
class Patient:
    patient_id: UUID
    first_name: str
    age: int
    gender: str
    create_at: datetime
    updated_at: datetime
    is_active: bool = True
    phone_number: Optional[str] = None
    email: Optional[str] = None
    address: Optional[str] = None
    last_name: Optional[str] = None
    date_of_birth: Optional[str] = None
    patient_type: PatientType = PatientType.ADULT
    guardian_name: Optional[str] = None
    guardian_phone: Optional[str] = None
