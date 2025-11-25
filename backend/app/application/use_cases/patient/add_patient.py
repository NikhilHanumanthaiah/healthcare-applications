from app.domain.models.patient import Patient, PatientType
from app.domain.repositories.patient_repository import PatientRepository
from app.application.dto.patient_dto import PatientDTO


class AddPatient:
    def __init__(self, patient_repository: PatientRepository):
        self.patient_repository = patient_repository

    def execute(
        self,
        first_name: str,
        last_name: str,
        date_of_birth: str,
        age: int,
        gender: str,
        phone_number: str,
        email: str,
        address: str,
        patient_type: str = "ADULT",
        guardian_name: str = None,
        guardian_phone: str = None,
    ) -> PatientDTO:

        patient = Patient(
            patient_id=None,
            first_name=first_name,
            last_name=last_name,
            date_of_birth=date_of_birth,
            age=age,
            gender=gender,
            phone_number=phone_number,
            email=email,
            address=address,
            patient_type=PatientType(patient_type),
            guardian_name=guardian_name,
            guardian_phone=guardian_phone,
            create_at=None,  # Let DB handle defaults or set in Repo
            updated_at=None,
        )
        created_patient = self.patient_repository.create(patient)
        return PatientDTO.model_validate(created_patient)
