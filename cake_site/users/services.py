from . import models, repositories, schemas
from sqlalchemy.orm import Session
from typing import Optional, List
from auth.utils import get_password_hash, verify_password

class UserService:
    def __init__(self, db: Session):
        self.repository = repositories.UserRepository(db)

    def get_user_by_id(self, user_id: int) -> Optional[schemas.UserResponse]:
        db_user = self.repository.get_by_id(user_id)
        if db_user:
            return schemas.UserResponse.model_validate(db_user)
        return None

    def get_user_by_email(self, email: str) -> Optional[schemas.UserResponse]:
        db_user = self.repository.get_by_email(email)
        if db_user:
            return schemas.UserResponse.model_validate(db_user)
        return None

    def get_user_db_by_email(self, email: str) -> Optional[models.User]:
        return self.repository.get_by_email(email)

    def get_all_users(self) -> List[schemas.UserResponse]:
        db_users = self.repository.get_all_users()
        return [schemas.UserResponse.model_validate(user) for user in db_users]

    def authenticate_user(self, email: str, password: str) -> Optional[schemas.UserResponse]:
        db_user = self.repository.get_by_email(email)
        
        if len(password.encode('utf-8')) > 72:
            return None
        
        if len(password) < 6:
            return None
            
        if not db_user or not verify_password(password, db_user.password):
            return None
        return schemas.UserResponse.model_validate(db_user)

    def create_user(self, user_data: schemas.UserCreate) -> schemas.UserResponse:
        existing_user = self.repository.get_by_email(user_data.email)
        if existing_user:
            raise ValueError("User with this email already exists")
        
        if len(user_data.password.encode('utf-8')) > 72:
            raise ValueError("Password is too long. Maximum length is 72 bytes")
        
        if len(user_data.password) < 6:
            raise ValueError("Password must be at least 6 characters")
        
        hashed_password = get_password_hash(user_data.password)
        db_user = self.repository.create(user_data, hashed_password)
        return schemas.UserResponse.model_validate(db_user)

    def update_user(self, user_id: int, user_update: schemas.UserUpdate) -> Optional[schemas.UserResponse]:
        db_user = self.repository.update(user_id, user_update)
        if db_user:
            return schemas.UserResponse.model_validate(db_user)
        return None