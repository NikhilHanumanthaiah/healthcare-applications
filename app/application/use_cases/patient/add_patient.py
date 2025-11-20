from app.domain.models.patient import Patient
from app.domain.repositories.patient_repository import PatientRepository
from app.application.dto.patient_dto import PatientDTO


class AddPatient:
    def __init__(self, patient_repository: PatientRepository):
        self.patient_repository  = patient_repository

    def execute(self, first_name: str, last_name: str, date_of_birth: str, age: int, gender: str, phone_number: str, email: str, address: str) -> PatientDTO:

        patient = Patient(patient_id=None, first_name=first_name, last_name=last_name, date_of_birth=date_of_birth, age=age, gender=gender, phone_number=phone_number, email=email, address=address)
        created_patient = self.patient_repository.create(patient)   
        return PatientDTO(patient_id=created_patient.patient_id, first_name=created_patient.first_name, last_name=created_patient.last_name, date_of_birth=created_patient.date_of_birth, age=created_patient.age, gender=created_patient.gender, phone_number=created_patient.phone_number, email=created_patient.email, address=created_patient.address)
    

