
from pydantic import BaseModel
from typing import Optional

class MedicineDTO(BaseModel):
    id: int
    name: str
    price_per_unit: float
    stock: int

    class Config:
        from_attributes = True

class MedicineUpdateDTO(BaseModel):
    name: Optional[str] = None
    price_per_unit: Optional[float] = None
    stock: Optional[int] = None

    class Config:
        from_attributes = True


