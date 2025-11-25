
from typing import List
from app.domain.models.bill import Bill
from app.domain.repositories.bill_repository import BillRepository
from app.application.dto.bill_dto import BillDTO, BillItemDTO
from app.application.dto.medicine_dto import MedicineDTO

class GetAllBills:
    def __init__(self, bill_repository: BillRepository):
        self.bill_repository = bill_repository

    def execute(self) -> List[BillDTO]:
        bills = self.bill_repository.get_all()
        return [self._to_bill_dto(b) for b in bills]

    def _to_bill_dto(self, bill: Bill) -> BillDTO:
        return BillDTO(
            id=bill.id,
            patient_name=bill.patient_name,
            patient_age=bill.patient_age,
            bill_items=[self._to_bill_item_dto(i) for i in bill.bill_items]
        )
    
    def _to_bill_item_dto(self, item) -> BillItemDTO:
        medicine_dto = MedicineDTO(id=item.medicine.id, name=item.medicine.name, price_per_unit=item.medicine.price_per_unit, stock=item.medicine.stock)
        return BillItemDTO(
            id=item.id,
            bill_id=item.bill_id,
            medicine_id=item.medicine_id,
            quantity=item.quantity,
            price_per_unit=item.price_per_unit,
            medicine=medicine_dto
        )
