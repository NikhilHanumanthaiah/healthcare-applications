from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List

from app.presentation.api.deps import get_db
from app.application.dto.patient_dto import PatientDTO
from app.application.use_cases.patient.add_patient import AddPatient
from app.application.use_cases.patient.patient_use_cases import (
    GetPatient,
    ListPatients,
    UpdatePatient,
    DeletePatient,
)
from app.infrastructure.repositories.patient_repository import PatientRepositoryImpl
from app.presentation.schemas.patient_schema import PatientCreate, PatientUpdate

router = APIRouter()


@router.post("/patient", response_model=PatientDTO)
def add_patient(patient: PatientCreate, db: Session = Depends(get_db)):
    patient_repository = PatientRepositoryImpl(db)
    add_patient_uc = AddPatient(patient_repository)
    return add_patient_uc.execute(
        patient.first_name,
        patient.last_name,
        patient.date_of_birth,
        patient.age,
        patient.gender,
        patient.phone_number,
        patient.email,
        patient.address,
        patient.patient_type,
        patient.guardian_name,
        patient.guardian_phone,
    )


@router.get("/patient/{patient_id}", response_model=PatientDTO)
def get_patient(patient_id: str, db: Session = Depends(get_db)):
    patient_repository = PatientRepositoryImpl(db)
    get_patient_uc = GetPatient(patient_repository)
    patient = get_patient_uc.execute(patient_id)
    if not patient:
        raise HTTPException(status_code=404, detail="Patient not found")
    return patient


@router.get("/patients", response_model=List[PatientDTO])
def list_patients(skip: int = 0, limit: int = 10, db: Session = Depends(get_db)):
    patient_repository = PatientRepositoryImpl(db)
    list_patients_uc = ListPatients(patient_repository)
    return list_patients_uc.execute(skip, limit)


@router.put("/patient/{patient_id}", response_model=PatientDTO)
def update_patient(
    patient_id: str, patient_data: PatientUpdate, db: Session = Depends(get_db)
):
    patient_repository = PatientRepositoryImpl(db)
    update_patient_uc = UpdatePatient(patient_repository)
    updated_patient = update_patient_uc.execute(
        patient_id, patient_data.model_dump(exclude_unset=True)
    )
    if not updated_patient:
        raise HTTPException(status_code=404, detail="Patient not found")
    return updated_patient


@router.delete("/patient/{patient_id}")
def delete_patient(patient_id: str, db: Session = Depends(get_db)):
    patient_repository = PatientRepositoryImpl(db)
    delete_patient_uc = DeletePatient(patient_repository)
    success = delete_patient_uc.execute(patient_id)
    if not success:
        raise HTTPException(status_code=404, detail="Patient not found")
    return {"message": "Patient deleted successfully"}
