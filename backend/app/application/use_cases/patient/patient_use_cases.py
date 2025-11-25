from typing import List, Optional
from app.domain.repositories.patient_repository import PatientRepository
from app.application.dto.patient_dto import PatientDTO
from app.domain.models.patient import Patient


class GetPatient:
    def __init__(self, patient_repository: PatientRepository):
        self.patient_repository = patient_repository

    def execute(self, patient_id: str) -> Optional[PatientDTO]:
        patient = self.patient_repository.get_by_id(patient_id)
        if not patient:
            return None
        return PatientDTO.model_validate(patient)


class ListPatients:
    def __init__(self, patient_repository: PatientRepository):
        self.patient_repository = patient_repository

    def execute(self, skip: int = 0, limit: int = 10) -> List[PatientDTO]:
        patients = self.patient_repository.list_patients(skip, limit)
        return [PatientDTO.model_validate(p) for p in patients]


class UpdatePatient:
    def __init__(self, patient_repository: PatientRepository):
        self.patient_repository = patient_repository

    def execute(self, patient_id: str, patient_data: dict) -> Optional[PatientDTO]:
        patient = self.patient_repository.update(patient_id, patient_data)
        if not patient:
            return None
        return PatientDTO.model_validate(patient)


class DeletePatient:
    def __init__(self, patient_repository: PatientRepository):
        self.patient_repository = patient_repository

    def execute(self, patient_id: str) -> bool:
        return self.patient_repository.delete(patient_id)
