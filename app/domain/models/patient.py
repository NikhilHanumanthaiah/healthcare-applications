
from dataclasses import dataclass
from typing import Optional
from uuid import UUID
from datetime import datetime


@dataclass
class Patient:
    patient_id: UUID
    first_name: str
    age: int
    gender: str
    create_at:datetime
    updated_at:datetime
    is_active:bool=True
    phone_number: Optional[str] = None
    email:Optional[str] = None
    address:Optional[str] = None
    last_name: Optional[str] = None
    date_of_birth:Optional[str] = None



