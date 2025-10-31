
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List

from app.application.use_cases.create_bill import CreateBill
from app.application.use_cases.get_all_bills import GetAllBills
from app.application.dto.bill_dto import BillDTO
from app.presentation.schemas.bill_schema import BillCreate
from app.infrastructure.repositories.bill_repository import BillRepositoryImpl
from app.infrastructure.repositories.medicine_repository import MedicineRepositoryImpl
from app.presentation.api.deps import get_db

router = APIRouter()

@router.post("/bills", response_model=BillDTO)
def create_bill(bill: BillCreate, db: Session = Depends(get_db)):
    bill_repository = BillRepositoryImpl(db)
    medicine_repository = MedicineRepositoryImpl(db)
    create_bill_uc = CreateBill(bill_repository, medicine_repository)
    try:
        return create_bill_uc.execute(bill.patient_name, bill.patient_age, [item.dict() for item in bill.items])
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.get("/bills", response_model=List[BillDTO])
def get_all_bills(db: Session = Depends(get_db)):
    bill_repository = BillRepositoryImpl(db)
    get_all_bills_uc = GetAllBills(bill_repository)
    return get_all_bills_uc.execute()
