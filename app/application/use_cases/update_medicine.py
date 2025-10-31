from app.domain.models.medicine import Medicine
from app.domain.repositories.medicine_repository import MedicineRepository
from app.application.dto.medicine_dto import MedicineDTO, MedicineUpdateDTO

class UpdateMedicine:
    def __init__(self, medicine_repository: MedicineRepository):
        self.medicine_repository = medicine_repository

    def execute(self, id: int, update_dto: MedicineUpdateDTO) -> MedicineDTO:
        medicine = Medicine(
            id=id,
            name=update_dto.name,
            price_per_unit=update_dto.price_per_unit,
            stock=update_dto.stock
        )

        updated_medicine = self.medicine_repository.update(medicine)
        if not updated_medicine:
            return None

        return MedicineDTO(
            id=updated_medicine.id,
            name=updated_medicine.name,
            price_per_unit=updated_medicine.price_per_unit,
            stock=updated_medicine.stock
        )
