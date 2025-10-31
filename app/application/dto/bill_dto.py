
from pydantic import BaseModel
from typing import List, Optional
from .medicine_dto import MedicineDTO

class BillItemDTO(BaseModel):
    id: int
    bill_id: int
    medicine_id: int
    quantity: int
    price_per_unit: Optional[float] = None
    medicine: MedicineDTO

    class Config:
        from_attributes = True

class BillDTO(BaseModel):
    id: int
    patient_name: str
    patient_age: int
    bill_items: List[BillItemDTO]
    total_amount: Optional[float] = None

    class Config:
        from_attributes = True



    class Config:
        from_attributes = True
