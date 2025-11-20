from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.presentation.api.deps import get_db

from app.application.dto.patient_dto import PatientDTO
from app.application.use_cases.patient.add_patient import AddPatient
from app.infrastructure.repositories.patient_repository import PatientRepositoryImpl
from app.presentation.schemas.patient_schema import PatientCreate



router = APIRouter()

@router.post("/patient", response_model=PatientDTO)
def add_patient(patient: PatientCreate, db: Session = Depends(get_db)):
    Patinent_repository = PatientRepositoryImpl(db)
    add_patient_uc = AddPatient(Patinent_repository)
    return add_patient_uc.execute(patient.first_name, patient.last_name, patient.date_of_birth, patient.age, patient.gender, patient.phone_number, patient.email, patient.address)