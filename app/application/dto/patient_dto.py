from pydantic import BaseModel
from typing import Optional
from uuid import UUID
from datetime import datetime
   
class PatientDTO(BaseModel):
    patient_id: UUID
    first_name: str
    last_name: Optional[str] = None
    date_of_birth:Optional[str] = None
    age: int
    gender: str
    phone_number: Optional[str] = None
    email:Optional[str] = None
    address:Optional[str] = None
    create_at:datetime
    updated_at:datetime
    is_active:bool=True


    class Config:
        from_attributes = True