from . import repositories, schemas
from sqlalchemy.orm import Session
from typing import List

class CakeService:
    def __init__(self, db: Session):
        self.repository = repositories.CakeRepository(db)

    def get_all_cakes(self) -> List[schemas.CakeResponse]:
        cakes = self.repository.get_all_cakes()
        return [schemas.CakeResponse.model_validate(cake) for cake in cakes]

    def get_cake_by_id(self, cake_id: int) -> schemas.CakeResponse:
        cake = self.repository.get_cake_by_id(cake_id)
        if cake:
            return schemas.CakeResponse.model_validate(cake)
        return None

    def get_available_components(self):
        return {
            "layers": [schemas.CakeLayerResponse.model_validate(layer) for layer in self.repository.get_all_layers()],
            "creams": [schemas.CreamResponse.model_validate(cream) for cream in self.repository.get_all_creams()],
            "fillings": [schemas.FillingResponse.model_validate(filling) for filling in self.repository.get_all_fillings()],
            "decorations": [schemas.DecorationResponse.model_validate(decoration) for decoration in self.repository.get_all_decorations()]
        }