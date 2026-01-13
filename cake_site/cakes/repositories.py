from sqlalchemy.orm import Session
from . import models
from typing import List, Optional

class CakeRepository:
    def __init__(self, db: Session):
        self.db = db

    def get_all_cakes(self) -> List[models.Cake]:
        return self.db.query(models.Cake).filter(models.Cake.is_available == True).all()

    def get_cake_by_id(self, cake_id: int) -> Optional[models.Cake]:
        return self.db.query(models.Cake).filter(models.Cake.id == cake_id).first()

    def get_all_layers(self) -> List[models.CakeLayer]:
        return self.db.query(models.CakeLayer).filter(models.CakeLayer.is_available == True).all()

    def get_all_creams(self) -> List[models.Cream]:
        return self.db.query(models.Cream).filter(models.Cream.is_available == True).all()

    def get_all_fillings(self) -> List[models.Filling]:
        return self.db.query(models.Filling).filter(models.Filling.is_available == True).all()

    def get_all_decorations(self) -> List[models.Decoration]:
        return self.db.query(models.Decoration).filter(models.Decoration.is_available == True).all()
    
     # МЕТОД ДЛЯ АДМИНОВ - получает все торты, включая недоступные
    def get_all_cakes_admin(self) -> List[models.Cake]:
        return self.db.query(models.Cake).all()