
from pydantic import BaseModel
from typing import Optional

class MedicineCreate(BaseModel):
    name: str
    price_per_unit: float
    stock: int

class MedicineUpdate(BaseModel):
    name: Optional[str]
    price_per_unit: Optional[float]
    stock:Optional[int]
