from . import repositories, schemas
from cakes.repositories import CakeRepository
from sqlalchemy.orm import Session
from typing import List, Dict, Any

class ConstructorService:
    def __init__(self, db: Session):
        self.custom_cake_repo = repositories.CustomCakeRepository(db)
        self.cake_repo = CakeRepository(db)

    def calculate_cake_price(self, cake_data: schemas.CustomCakeCreate) -> Dict[str, Any]:
        total_price = 0
        weight = 0
        
        # Расчет слоев (список)
        layers_info = []
        all_layers = {layer.id: layer for layer in self.cake_repo.get_all_layers()}
        for layer in cake_data.layers:
            layer_data = all_layers.get(layer.id)
            if layer_data:
                layer_price = layer_data.price_per_unit * layer.quantity
                total_price += layer_price
                weight += layer.quantity * 100
                layers_info.append({
                    "id": layer_data.id,
                    "name": layer_data.name,
                    "quantity": layer.quantity,
                    "price": layer_price
                })
        
        # Расчет кремов (список) ← Изменено
        creams_info = []
        all_creams = {cream.id: cream for cream in self.cake_repo.get_all_creams()}
        for cream in cake_data.creams:
            cream_data = all_creams.get(cream.id)
            if cream_data:
                cream_price = cream_data.price_per_unit * cream.quantity
                total_price += cream_price
                weight += cream.quantity * 50
                creams_info.append({
                    "id": cream_data.id,
                    "name": cream_data.name,
                    "quantity": cream.quantity,
                    "price": cream_price
                })
        
        # Расчет начинок (список)
        fillings_info = []
        all_fillings = {filling.id: filling for filling in self.cake_repo.get_all_fillings()}
        for filling in cake_data.fillings:
            filling_data = all_fillings.get(filling.id)
            if filling_data:
                filling_price = filling_data.price_per_unit * filling.quantity
                total_price += filling_price
                weight += filling.quantity * 30
                fillings_info.append({
                    "id": filling_data.id,
                    "name": filling_data.name,
                    "quantity": filling.quantity,
                    "price": filling_price
                })
        
        # Расчет украшений (список)
        decorations_info = []
        all_decorations = {decoration.id: decoration for decoration in self.cake_repo.get_all_decorations()}
        for decoration in cake_data.decorations:
            decoration_data = all_decorations.get(decoration.id)
            if decoration_data:
                decoration_price = decoration_data.price_per_unit * decoration.quantity
                total_price += decoration_price
                weight += decoration.quantity * 10
                decorations_info.append({
                    "id": decoration_data.id,
                    "name": decoration_data.name,
                    "quantity": decoration.quantity,
                    "price": decoration_price
                })
        
        return {
            "total_price": total_price,
            "weight": weight,
            "components": {
                "layers": layers_info,
                "creams": creams_info,  # ← Изменено
                "fillings": fillings_info,
                "decorations": decorations_info
            }
        }

    def create_custom_cake(self, user_id: int, cake_data: schemas.CustomCakeCreate) -> schemas.CustomCakeResponse:
        calculation = self.calculate_cake_price(cake_data)
        
        # Подготовка данных для сохранения в БД
        custom_cake_data = {
            "user_id": user_id,
            "name": cake_data.name or f"Кастомный торт {user_id}",
            "layers": [layer.dict() for layer in cake_data.layers],
            "creams": [cream.dict() for cream in cake_data.creams],  # ← Изменено
            "fillings": [filling.dict() for filling in cake_data.fillings],
            "decorations": [decoration.dict() for decoration in cake_data.decorations],
            "total_price": calculation["total_price"],
            "weight": calculation["weight"],
            "description": f"Кастомный торт {cake_data.name or ''}"
        }
        
        db_cake = self.custom_cake_repo.create_custom_cake(custom_cake_data)
        return schemas.CustomCakeResponse.model_validate(db_cake)