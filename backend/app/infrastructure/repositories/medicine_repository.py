
from fastapi import HTTPException
from typing import List
from sqlalchemy.orm import Session
from app.domain.models.medicine import Medicine as DomainMedicine
from app.infrastructure.db.models.medicine import Medicine as DbMedicine
from app.domain.repositories.medicine_repository import MedicineRepository
from sqlalchemy import and_
from datetime import datetime, timezone


class MedicineRepositoryImpl(MedicineRepository):
    def __init__(self, session: Session):
        self.session = session

    def get_all(self) -> List[DomainMedicine]:
        medicines = self.session.query(DbMedicine).filter(DbMedicine.is_deleted == False).all()
        return [DomainMedicine(id=m.id, name=m.name, price_per_unit=m.price_per_unit, stock=m.stock) for m in medicines]

    def get_by_id(self, medicine_id: int) -> DomainMedicine:
        medicine = self.session.query(DbMedicine).filter(and_(DbMedicine.id == medicine_id, DbMedicine.is_deleted == False)).first()
        if medicine:
            return DomainMedicine(id=medicine.id, name=medicine.name, price_per_unit=medicine.price_per_unit, stock=medicine.stock)
        return None

    def create(self, medicine: DomainMedicine) -> DomainMedicine:
        existing_medicine = self.session.query(DbMedicine).filter(and_(DbMedicine.name == medicine.name, 
                                    DbMedicine.is_deleted == False
                                    )).first()
        if existing_medicine:
            raise HTTPException(status_code=400, detail="Medicine with this name already exists")
        
        deleted_medicine = self.session.query(DbMedicine).filter(and_(DbMedicine.name == medicine.name, 
                                    DbMedicine.is_deleted == True
                                    )).first()
        # Recreating the deleted medicine if it was soft-deleted
        if deleted_medicine:
            deleted_medicine.is_deleted = False
            deleted_medicine.deleted_at = None
            deleted_medicine.price_per_unit = medicine.price_per_unit
            deleted_medicine.stock = medicine.stock
            self.session.commit()
            self.session.refresh(deleted_medicine)
            return DomainMedicine(id=deleted_medicine.id, name=deleted_medicine.name, price_per_unit=deleted_medicine.price_per_unit, stock=deleted_medicine.stock)
        
        db_medicine = DbMedicine(name=medicine.name, price_per_unit=medicine.price_per_unit, stock=medicine.stock)
        self.session.add(db_medicine)
        self.session.commit()
        self.session.refresh(db_medicine)
        return DomainMedicine(id=db_medicine.id, name=db_medicine.name, price_per_unit=db_medicine.price_per_unit, stock=db_medicine.stock)

    def update(self, medicine: DomainMedicine) -> DomainMedicine:
        db_medicine = (
            self.session.query(DbMedicine)
            .filter(DbMedicine.id == medicine.id)
            .first()
        )
        if not db_medicine:
            return None

        # Update only fields that are provided (non-None)
        if medicine.name is not None:
            db_medicine.name = medicine.name
        if medicine.price_per_unit is not None:
            db_medicine.price_per_unit = medicine.price_per_unit
        if medicine.stock is not None:
            db_medicine.stock = medicine.stock

        self.session.commit()
        self.session.refresh(db_medicine)

        return DomainMedicine(
            id=db_medicine.id,
            name=db_medicine.name,
            price_per_unit=db_medicine.price_per_unit,
            stock=db_medicine.stock
        )

    def delete(self, medicine_id: int) -> bool:
        db_medicine = (
            self.session.query(DbMedicine)
            .filter(and_(DbMedicine.id == medicine_id, DbMedicine.is_deleted == False))
            .first()
        )
        if not db_medicine:
            raise HTTPException(status_code=404, detail="Medicine not found or already deleted")

        db_medicine.is_deleted = True
        db_medicine.stock = 0
        db_medicine.deleted_at = datetime.now(timezone.utc)

        self.session.commit()
        return True