
from app.domain.models.medicine import Medicine
from app.domain.repositories.medicine_repository import MedicineRepository
from app.application.dto.medicine_dto import MedicineDTO

class AddMedicine:
    def __init__(self, medicine_repository: MedicineRepository):
        self.medicine_repository = medicine_repository

    def execute(self, name: str, price_per_unit: float, stock: int) -> MedicineDTO:
        medicine = Medicine(id=None, name=name, price_per_unit=price_per_unit, stock=stock)
        created_medicine = self.medicine_repository.create(medicine)
        return MedicineDTO(id=created_medicine.id, name=created_medicine.name, price_per_unit=created_medicine.price_per_unit, stock=created_medicine.stock)
