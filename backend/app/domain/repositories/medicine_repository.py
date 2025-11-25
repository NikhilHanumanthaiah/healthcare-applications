
from abc import ABC, abstractmethod
from typing import List
from app.domain.models.medicine import Medicine

class MedicineRepository(ABC):

    @abstractmethod
    def get_all(self) -> List[Medicine]:
        pass

    @abstractmethod
    def get_by_id(self, medicine_id: int) -> Medicine:
        pass

    @abstractmethod
    def create(self, medicine: Medicine) -> Medicine:
        pass

    @abstractmethod
    def update(self, medicine: Medicine) -> Medicine:
        pass

    @abstractmethod
    def delete(self, medicine_id: int):
        pass
