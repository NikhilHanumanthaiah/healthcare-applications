
from typing import List
from sqlalchemy.orm import Session
from app.domain.models.bill import Bill as DomainBill, BillItem as DomainBillItem
from app.domain.models.medicine import Medicine as DomainMedicine
from app.infrastructure.db.models.bill import Bill as DbBill, BillItem as DbBillItem
from app.infrastructure.db.models.medicine import Medicine as DbMedicine
from app.domain.repositories.bill_repository import BillRepository

class BillRepositoryImpl(BillRepository):
    def __init__(self, session: Session):
        self.session = session

    def get_all(self) -> List[DomainBill]:
        bills = self.session.query(DbBill).all()
        return [self._to_domain_bill(b) for b in bills]

    def get_by_id(self, bill_id: int) -> DomainBill:
        bill = self.session.query(DbBill).filter(DbBill.id == bill_id).first()
        return self._to_domain_bill(bill) if bill else None

    def create(self, bill: DomainBill) -> DomainBill:
        db_bill = DbBill(patient_name=bill.patient_name, patient_age=bill.patient_age, total_amount=bill.total_amount)
        self.session.add(db_bill)
        self.session.commit()
        self.session.refresh(db_bill)

        for item in bill.bill_items:
            db_item = DbBillItem(
                bill_id=db_bill.id,
                medicine_id=item.medicine_id,
                quantity=item.quantity,
                price_per_unit=item.price_per_unit
            )
            self.session.add(db_item)
        
        self.session.commit()
        self.session.refresh(db_bill)

        return self._to_domain_bill(db_bill)

    def _to_domain_bill(self, bill: DbBill) -> DomainBill:
        return DomainBill(
            id=bill.id,
            patient_name=bill.patient_name,
            patient_age=bill.patient_age,
            total_amount=bill.total_amount,
            bill_items=[self._to_domain_bill_item(i) for i in bill.items]
        )

    def _to_domain_bill_item(self, item: DbBillItem) -> DomainBillItem:
        medicine = self.session.query(DbMedicine).filter(DbMedicine.id == item.medicine_id).first()
        domain_medicine = DomainMedicine(id=medicine.id, name=medicine.name, price_per_unit=medicine.price_per_unit, stock=medicine.stock)
        return DomainBillItem(
            id=item.id,
            bill_id=item.bill_id,
            medicine_id=item.medicine_id,
            quantity=item.quantity,
            price_per_unit=item.price_per_unit,
            medicine=domain_medicine
        )
