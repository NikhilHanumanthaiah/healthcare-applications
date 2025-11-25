"""
Debug script to test patient creation with detailed error logging
"""

import sys

sys.path.insert(0, "c:/Users/Nikhil/Desktop/healthcare-applications/backend")

from app.infrastructure.db.session import SessionLocal
from app.infrastructure.repositories.patient_repository import PatientRepositoryImpl
from app.application.use_cases.patient.add_patient import AddPatient
from app.domain.models.patient import Patient, PatientType


def test_patient_creation():
    db = SessionLocal()
    try:
        print("Creating patient repository...")
        patient_repository = PatientRepositoryImpl(db)

        print("Creating AddPatient use case...")
        add_patient_uc = AddPatient(patient_repository)

        print("Executing patient creation...")
        result = add_patient_uc.execute(
            first_name="Ravi",
            last_name="Kumar",
            date_of_birth="1993-05-14",
            age=32,
            gender="Male",
            phone_number="+91-9876543213",
            email="ravi.kumar@example.com",
            address="12 MG Road, Bengaluru",
            patient_type="ADULT",
            guardian_name=None,
            guardian_phone=None,
        )

        print(f"✅ Success! Patient created: {result}")
        return result

    except Exception as e:
        print(f"❌ Error: {type(e).__name__}: {e}")
        import traceback

        traceback.print_exc()
        return None
    finally:
        db.close()


if __name__ == "__main__":
    test_patient_creation()
