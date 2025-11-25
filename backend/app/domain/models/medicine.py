from dataclasses import dataclass
from typing import Optional

@dataclass
class Medicine:
    id: int
    name: Optional[str] = None
    price_per_unit: Optional[float] = None
    stock: Optional[int] = None
