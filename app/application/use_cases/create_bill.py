
from typing import List
from app.domain.models.bill import Bill, BillItem
from app.domain.repositories.bill_repository import BillRepository
from app.domain.repositories.medicine_repository import MedicineRepository
from app.application.dto.bill_dto import BillDTO, BillItemDTO
from app.application.dto.medicine_dto import MedicineDTO

class CreateBill:
    def __init__(self, bill_repository: BillRepository, medicine_repository: MedicineRepository):
        self.bill_repository = bill_repository
        self.medicine_repository = medicine_repository

    def execute(self, patient_name: str, patient_age: int, items: List[dict]) -> BillDTO:
        bill_items = []
        total_amount = 0.0
        for item in items:
            medicine = self.medicine_repository.get_by_id(item['medicine_id'])
            if not medicine or medicine.stock < item['quantity']:
                raise Exception('Insufficient stock')

            price_per_unit = item.get('price_per_unit', medicine.price_per_unit)
            total_amount += price_per_unit * item['quantity']

            bill_items.append(BillItem(
                id=None,
                bill_id=None,
                medicine_id=item['medicine_id'],
                quantity=item['quantity'],
                price_per_unit=price_per_unit,
                medicine=medicine
            ))

        bill = Bill(id=None, patient_name=patient_name, patient_age=patient_age, bill_items=bill_items, total_amount=total_amount)
        created_bill = self.bill_repository.create(bill)

        for item in created_bill.bill_items:
            medicine = item.medicine
            medicine.stock -= item.quantity
            self.medicine_repository.update(medicine)

        return self._to_bill_dto(created_bill)

    def _to_bill_dto(self, bill: Bill) -> BillDTO:
        return BillDTO(
            id=bill.id,
            patient_name=bill.patient_name,
            patient_age=bill.patient_age,
            total_amount=bill.total_amount,
            bill_items=[self._to_bill_item_dto(i) for i in bill.bill_items]
        )

    def _to_bill_item_dto(self, item: BillItem) -> BillItemDTO:
        medicine_dto = MedicineDTO(id=item.medicine.id, name=item.medicine.name, price_per_unit=item.medicine.price_per_unit, stock=item.medicine.stock)
        return BillItemDTO(
            id=item.id,
            bill_id=item.bill_id,
            medicine_id=item.medicine_id,
            quantity=item.quantity,
            price_per_unit=item.price_per_unit,
            medicine=medicine_dto
        )
