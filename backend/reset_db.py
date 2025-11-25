from app.infrastructure.db.session import engine
from app.infrastructure.db.models.patient import Patient
from app.infrastructure.db.base import Base


def reset_db():
    print("Dropping patients table...")
    Patient.__table__.drop(engine)
    print("Patients table dropped.")
    print("Recreating tables...")
    Base.metadata.create_all(bind=engine)
    print("Tables recreated.")


if __name__ == "__main__":
    reset_db()
