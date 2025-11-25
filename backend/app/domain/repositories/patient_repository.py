from abc import ABC, abstractmethod
from typing import List
from app.domain.models.patient import Patient


class PatientRepository(ABC):

    @abstractmethod
    def create(self, patient: Patient) -> Patient:
        pass

    @abstractmethod
    def get_by_id(self, patient_id: str) -> Patient:
        pass

    @abstractmethod
    def list_patients(self, skip: int = 0, limit: int = 10) -> List[Patient]:
        pass

    @abstractmethod
    def update(self, patient_id: str, patient_data: dict) -> Patient:
        pass

    @abstractmethod
    def delete(self, patient_id: str) -> bool:
        pass
