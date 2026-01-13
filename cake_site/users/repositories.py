from sqlalchemy.orm import Session
from . import models, schemas
from typing import Optional, List

class UserRepository:
    def __init__(self, db: Session):
        self.db = db

    def get_by_id(self, user_id: int) -> Optional[models.User]:
        return self.db.query(models.User).filter(models.User.id == user_id).first()

    def get_by_email(self, email: str) -> Optional[models.User]:
        return self.db.query(models.User).filter(models.User.email == email).first()

    def get_all_users(self) -> List[models.User]:
        return self.db.query(models.User).order_by(models.User.created_at.desc()).all()

    def create(self, user: schemas.UserCreate, password: str) -> models.User:
        db_user = models.User(
            email=user.email,
            password=password,
            full_name=user.full_name,
            phone=user.phone,
            address=user.address
        )
        self.db.add(db_user)
        self.db.commit()
        self.db.refresh(db_user)
        return db_user

    def update(self, user_id: int, user_update: schemas.UserUpdate) -> Optional[models.User]:
        db_user = self.get_by_id(user_id)
        if db_user:
            update_data = user_update.model_dump(exclude_unset=True)
            for field, value in update_data.items():
                setattr(db_user, field, value)
            self.db.commit()
            self.db.refresh(db_user)
        return db_user

    def delete(self, user_id: int) -> bool:
        db_user = self.get_by_id(user_id)
        if not db_user:
            return False
        
        self.db.delete(db_user)
        self.db.commit()
        return True