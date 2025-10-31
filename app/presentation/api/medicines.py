
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List

from app.application.use_cases.add_medicine import AddMedicine
from app.application.use_cases.get_all_medicines import GetAllMedicines
from app.application.use_cases.update_medicine import UpdateMedicine
from app.application.use_cases.delete_medicine import DeleteMedicine
from app.application.dto.medicine_dto import MedicineDTO,MedicineUpdateDTO
from app.presentation.schemas.medicine_schema import MedicineCreate
from app.infrastructure.repositories.medicine_repository import MedicineRepositoryImpl
from app.presentation.api.deps import get_db

router = APIRouter()

@router.post("/medicines", response_model=MedicineDTO)
def add_medicine(medicine: MedicineCreate, db: Session = Depends(get_db)):
    medicine_repository = MedicineRepositoryImpl(db)
    add_medicine_uc = AddMedicine(medicine_repository)
    return add_medicine_uc.execute(medicine.name, medicine.price_per_unit, medicine.stock)

@router.get("/medicines", response_model=List[MedicineDTO])
def get_all_medicines(db: Session = Depends(get_db)):
    medicine_repository = MedicineRepositoryImpl(db)
    get_all_medicines_uc = GetAllMedicines(medicine_repository)
    return get_all_medicines_uc.execute()

@router.patch("/medicines/{id}", response_model=MedicineDTO)
def update_medicine(id: int, update_dto: MedicineUpdateDTO,db: Session = Depends(get_db)):
    repo = MedicineRepositoryImpl(db)
    use_case = UpdateMedicine(repo)
    updated = use_case.execute(id, update_dto)
    if not updated:
        return {"error": "Medicine not found"}
    return updated

@router.delete("/medicines/{medicine_id}")
def delete_medicine(medicine_id: int, db: Session = Depends(get_db)):
    medicine_repository = MedicineRepositoryImpl(db)
    delete_medicine_uc = DeleteMedicine(medicine_repository)
    delete_medicine_uc.execute(medicine_id)
    return {"message": "Medicine deleted successfully"}
