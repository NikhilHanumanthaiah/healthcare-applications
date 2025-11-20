
from abc import ABC, abstractmethod
from typing import List
from app.domain.models.patient import Patient

class PatientRepository(ABC):

    @abstractmethod
    def create(self, patient: Patient) -> Patient:
        pass

