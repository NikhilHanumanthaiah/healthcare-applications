from fastapi import HTTPException
from sqlalchemy.orm import Session
from sqlalchemy import and_
from typing import List
from datetime import datetime, timezone

from app.domain.models.patient import Patient as DomainPatient, PatientType
from app.domain.repositories.patient_repository import PatientRepository
from app.infrastructure.db.models.patient import Patient as DbPatient


class PatientRepositoryImpl(PatientRepository):
    def __init__(self, session: Session):
        self.session = session

    def create(self, patient: DomainPatient) -> DomainPatient:
        existing_patient = (
            self.session.query(DbPatient)
            .filter(
                and_(
                    DbPatient.phone_number == patient.phone_number,
                    DbPatient.is_active == True,
                )
            )
            .first()
        )
        if existing_patient:
            raise HTTPException(
                status_code=400,
                detail="Patient with this {} already exists".format(
                    patient.phone_number
                ),
            )

        deleted_patient = (
            self.session.query(DbPatient)
            .filter(
                and_(
                    DbPatient.phone_number == patient.phone_number,
                    DbPatient.is_active == False,
                )
            )
            .first()
        )
        if deleted_patient:
            deleted_patient.is_active = True
            deleted_patient.updated_at = datetime.now(timezone.utc)
            # Update other fields if necessary
            deleted_patient.first_name = patient.first_name
            deleted_patient.last_name = patient.last_name
            deleted_patient.date_of_birth = (
                datetime.fromisoformat(patient.date_of_birth)
                if patient.date_of_birth
                else None
            )
            deleted_patient.age = patient.age
            deleted_patient.gender = patient.gender
            deleted_patient.email = patient.email
            deleted_patient.address = patient.address
            deleted_patient.patient_type = patient.patient_type.value
            deleted_patient.guardian_name = patient.guardian_name
            deleted_patient.guardian_phone = patient.guardian_phone

            self.session.commit()
            self.session.refresh(deleted_patient)
            return self._to_domain(deleted_patient)

        DB_patient = DbPatient(
            first_name=patient.first_name,
            last_name=patient.last_name,
            date_of_birth=(
                datetime.fromisoformat(patient.date_of_birth)
                if patient.date_of_birth
                else None
            ),
            age=patient.age,
            gender=patient.gender,
            phone_number=patient.phone_number,
            email=patient.email,
            address=patient.address,
            patient_type=patient.patient_type.value,
            guardian_name=patient.guardian_name,
            guardian_phone=patient.guardian_phone,
        )
        self.session.add(DB_patient)
        self.session.commit()
        self.session.refresh(DB_patient)
        return self._to_domain(DB_patient)

    def get_by_id(self, patient_id: str) -> DomainPatient:
        db_patient = (
            self.session.query(DbPatient)
            .filter(DbPatient.patient_id == patient_id, DbPatient.is_active == True)
            .first()
        )
        if not db_patient:
            return None
        return self._to_domain(db_patient)

    def list_patients(self, skip: int = 0, limit: int = 10) -> List[DomainPatient]:
        db_patients = (
            self.session.query(DbPatient)
            .filter(DbPatient.is_active == True)
            .offset(skip)
            .limit(limit)
            .all()
        )
        return [self._to_domain(p) for p in db_patients]

    def update(self, patient_id: str, patient_data: dict) -> DomainPatient:
        db_patient = (
            self.session.query(DbPatient)
            .filter(DbPatient.patient_id == patient_id, DbPatient.is_active == True)
            .first()
        )
        if not db_patient:
            return None

        for key, value in patient_data.items():
            if hasattr(db_patient, key):
                setattr(db_patient, key, value)

        db_patient.updated_date = datetime.now(timezone.utc)
        self.session.commit()
        self.session.refresh(db_patient)
        return self._to_domain(db_patient)

    def delete(self, patient_id: str) -> bool:
        db_patient = (
            self.session.query(DbPatient)
            .filter(DbPatient.patient_id == patient_id)
            .first()
        )
        if not db_patient:
            return False

        db_patient.is_active = False
        db_patient.updated_date = datetime.now(timezone.utc)
        self.session.commit()
        return True

    def _to_domain(self, db_patient: DbPatient) -> DomainPatient:
        # Safely convert date_of_birth to ISO string
        date_of_birth_str = None
        if db_patient.date_of_birth:
            try:
                date_of_birth_str = db_patient.date_of_birth.isoformat()
            except (AttributeError, ValueError):
                # If it's already a string or invalid, keep as is
                date_of_birth_str = (
                    str(db_patient.date_of_birth) if db_patient.date_of_birth else None
                )

        return DomainPatient(
            patient_id=db_patient.patient_id,
            first_name=db_patient.first_name,
            last_name=db_patient.last_name,
            date_of_birth=date_of_birth_str,
            age=db_patient.age,
            gender=getattr(db_patient, "gender", None) or "Unknown",
            phone_number=db_patient.phone_number,
            email=getattr(db_patient, "email", None),
            address=db_patient.address,
            create_at=db_patient.created_date,
            updated_at=db_patient.updated_date,
            is_active=db_patient.is_active,
            patient_type=PatientType(db_patient.patient_type),
            guardian_name=db_patient.guardian_name,
            guardian_phone=db_patient.guardian_phone,
        )
