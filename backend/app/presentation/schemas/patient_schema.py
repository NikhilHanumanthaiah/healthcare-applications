from pydantic import BaseModel, validator
from typing import Optional
from enum import Enum


class GenderEnum(str, Enum):
    male = "male"
    female = "female"
    other = "other"


class PatientCreate(BaseModel):
    first_name: str
    last_name: Optional[str] = None
    age: int
    gender: GenderEnum
    phone_number: str
    email: Optional[str] = None
    address: Optional[str] = None
    date_of_birth: Optional[str] = None
    patient_type: str = "ADULT"
    guardian_name: Optional[str] = None
    guardian_phone: Optional[str] = None

    @validator("gender", pre=True)
    def validate_gender(cls, v):
        if not v:
            raise ValueError("Gender is required")
        v = v.strip().lower()
        if v not in ["male", "female", "other"]:
            raise ValueError("Invalid gender")
        return v


class PatientUpdate(BaseModel):
    first_name: Optional[str] = None
    last_name: Optional[str] = None
    age: Optional[int] = None
    gender: Optional[GenderEnum] = None
    phone_number: Optional[str] = None
    email: Optional[str] = None
    address: Optional[str] = None
    date_of_birth: Optional[str] = None
    patient_type: Optional[str] = None
    guardian_name: Optional[str] = None
    guardian_phone: Optional[str] = None
