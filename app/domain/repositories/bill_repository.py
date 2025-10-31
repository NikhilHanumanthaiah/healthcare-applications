
from abc import ABC, abstractmethod
from typing import List
from app.domain.models.bill import Bill

class BillRepository(ABC):

    @abstractmethod
    def get_all(self) -> List[Bill]:
        pass

    @abstractmethod
    def get_by_id(self, bill_id: int) -> Bill:
        pass

    @abstractmethod
    def create(self, bill: Bill) -> Bill:
        pass
