
from typing import List
from app.domain.repositories.medicine_repository import MedicineRepository
from app.application.dto.medicine_dto import MedicineDTO

class GetAllMedicines:
    def __init__(self, medicine_repository: MedicineRepository):
        self.medicine_repository = medicine_repository

    def execute(self) -> List[MedicineDTO]:
        medicines = self.medicine_repository.get_all()
        return [MedicineDTO(id=m.id, name=m.name, price_per_unit=m.price_per_unit, stock=m.stock) for m in medicines]
