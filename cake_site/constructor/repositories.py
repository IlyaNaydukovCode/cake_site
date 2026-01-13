from sqlalchemy.orm import Session
from . import models
from typing import List, Optional

class CustomCakeRepository:
    def __init__(self, db: Session):
        self.db = db

    def create_custom_cake(self, custom_cake_data: dict) -> models.CustomCake:
        db_custom_cake = models.CustomCake(**custom_cake_data)
        self.db.add(db_custom_cake)
        self.db.commit()
        self.db.refresh(db_custom_cake)
        return db_custom_cake

    def get_by_id(self, cake_id: int) -> Optional[models.CustomCake]:
        return self.db.query(models.CustomCake).filter(models.CustomCake.id == cake_id).first()

    def get_user_cakes(self, user_id: int) -> List[models.CustomCake]:
        return self.db.query(models.CustomCake).filter(models.CustomCake.user_id == user_id).all()