from sqlalchemy.orm import Session
from typing import List, Optional
from users import repositories as user_repos, schemas as user_schemas
from auth.utils import get_password_hash

class AdminUserService:
    def __init__(self, db: Session):
        self.repository = user_repos.UserRepository(db)

    def get_all_users(self) -> List[user_schemas.UserResponse]:
        db_users = self.repository.get_all_users()
        return [user_schemas.UserResponse.model_validate(user) for user in db_users]

    def get_user_by_id(self, user_id: int) -> Optional[user_schemas.UserResponse]:
        db_user = self.repository.get_by_id(user_id)
        if db_user:
            return user_schemas.UserResponse.model_validate(db_user)
        return None

    def create_user_admin(self, user_data) -> user_schemas.UserResponse:
        existing_user = self.repository.get_by_email(user_data.email)
        if existing_user:
            raise ValueError("User with this email already exists")
        
        # Преобразуем данные для создания
        from users.schemas import UserCreate
        user_create = UserCreate(
            email=user_data.email,
            password=user_data.password,
            full_name=user_data.full_name,
            phone=user_data.phone,
            address=user_data.address
        )
        
        hashed_password = get_password_hash(user_data.password)
        db_user = self.repository.create(user_create, hashed_password)
        
        # Если нужно установить админские права
        if hasattr(user_data, 'is_admin') and user_data.is_admin:
            from users.schemas import UserUpdate
            admin_update = UserUpdate(is_admin=True)
            self.repository.update(db_user.id, admin_update)
            self.repository.db.refresh(db_user)
        
        return user_schemas.UserResponse.model_validate(db_user)

    def update_user_admin(self, user_id: int, user_update) -> Optional[user_schemas.UserResponse]:
        db_user = self.repository.update(user_id, user_update)
        if db_user:
            return user_schemas.UserResponse.model_validate(db_user)
        return None

    def make_admin(self, user_id: int, is_admin: bool = True) -> Optional[user_schemas.UserResponse]:
        from users.schemas import UserUpdate
        user_update = UserUpdate(is_admin=is_admin)
        return self.update_user_admin(user_id, user_update)