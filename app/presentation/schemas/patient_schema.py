from pydantic import BaseModel
from typing import Optional


class PatientCreate(BaseModel):
    first_name: str
    last_name: Optional[str] = None
    age: int
    gender: str
    phone_number: str
    email:Optional[str] = None
    address: Optional[str] = None
    date_of_birth: Optional[str] = None