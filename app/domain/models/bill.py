
from dataclasses import dataclass
from typing import List
from .medicine import Medicine

@dataclass
class BillItem:
    id: int
    bill_id: int
    medicine_id: int
    quantity: int
    price_per_unit: float
    medicine: Medicine

@dataclass
class Bill:
    id: int
    patient_name: str
    patient_age: int
    bill_items: List[BillItem]
    total_amount: float = 0.0
