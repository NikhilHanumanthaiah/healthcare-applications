
from app.domain.repositories.medicine_repository import MedicineRepository

class DeleteMedicine:
    def __init__(self, medicine_repository: MedicineRepository):
        self.medicine_repository = medicine_repository

    def execute(self, id: int):
        self.medicine_repository.delete(id)
