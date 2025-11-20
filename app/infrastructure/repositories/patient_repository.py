from fastapi import HTTPException
from sqlalchemy.orm import Session
from sqlalchemy import and_
from datetime import datetime, timezone

from app.domain.models.patient import Patient as DomainPatient
from app.domain.repositories.patient_repository import PatientRepository
from app.infrastructure.db.models.patient import Patient as DbPatient


class PatientRepositoryImpl(PatientRepository):
    def __init__(self, session: Session):
        self.session = session


    def create(self, patient: DomainPatient) -> DomainPatient:
        existing_patient = Session.query(DbPatient).filter(and_(DbPatient.phone_number == patient.phone_number, DbPatient.is_active==True)).first()
        if existing_patient:
            raise HTTPException(status_code=400, detail="Patient with this {} already exists".format(patient.phone_number))
        
        deleted_patient = Session.query(and_(DbPatient.phone_number==patient.phone_number, DbPatient.is_active==False)).first()
        if deleted_patient:
            deleted_patient.is_active = True
            deleted_patient.updated_at = datetime.now(timezone.utc)
            self.session.commit()
            self.session.refresh(deleted_patient)
            return DomainPatient(patient_id=deleted_patient.patient_id, first_name=deleted_patient.first_name, last_name=deleted_patient.last_name, date_of_birth=deleted_patient.date_of_birth, age=deleted_patient.age)
        

        DB_patient = DbPatient(first_name=patient.first_name, last_name=patient.last_name, date_of_birth=patient.date_of_birth, age=patient.age, phone_number=patient.phone_number, address=patient.address)
        self.session.add(DB_patient)
        self.session.commit()
        self.session.refresh(DB_patient)
        return DomainPatient(patient_id=DB_patient.patient_id, first_name=DB_patient.first_name, last_name=DB_patient.last_name, date_of_birth=DB_patient.date_of_birth, age=DB_patient.age, phone_number=DB_patient.phone_number, address=DB_patient.address)
