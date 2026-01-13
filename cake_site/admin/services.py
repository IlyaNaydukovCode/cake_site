from sqlalchemy.orm import Session
from typing import List, Optional
from cakes import models as cake_models, repositories as cake_repos
from cakes.schemas import CakeResponse
from . import schemas as admin_schemas

class AdminCakeService:
    def __init__(self, db: Session):
        self.db = db
        self.cake_repo = cake_repos.CakeRepository(db)

    def create_cake(self, cake_data: admin_schemas.CakeCreate) -> CakeResponse:
        db_cake = cake_models.Cake(
            name=cake_data.name,
            description=cake_data.description,
            price=cake_data.price,
            image_url=cake_data.image_url,
            weight=cake_data.weight,
            ingredients=cake_data.ingredients
        )
        self.db.add(db_cake)
        self.db.commit()
        self.db.refresh(db_cake)
        return CakeResponse.model_validate(db_cake)

    def update_cake(self, cake_id: int, cake_update: admin_schemas.CakeUpdate) -> Optional[CakeResponse]:
        db_cake = self.cake_repo.get_cake_by_id(cake_id)
        if not db_cake:
            return None
        
        update_data = cake_update.model_dump(exclude_unset=True)
        for field, value in update_data.items():
            setattr(db_cake, field, value)
        
        self.db.commit()
        self.db.refresh(db_cake)
        return CakeResponse.model_validate(db_cake)

    def delete_cake(self, cake_id: int) -> bool:
        db_cake = self.cake_repo.get_cake_by_id(cake_id)
        if not db_cake:
            return False
        
        self.db.delete(db_cake)
        self.db.commit()
        return True

    # CRUD для коржей
    def get_all_layers(self) -> List[admin_schemas.CakeLayerResponse]:
        layers = self.cake_repo.get_all_layers()
        return [admin_schemas.CakeLayerResponse.model_validate(layer) for layer in layers]

    def create_cake_layer(self, layer_data: admin_schemas.ComponentCreate) -> cake_models.CakeLayer:
        db_layer = cake_models.CakeLayer(
            name=layer_data.name,
            description=layer_data.description,
            price_per_unit=layer_data.price_per_unit
        )
        self.db.add(db_layer)
        self.db.commit()
        self.db.refresh(db_layer)
        return db_layer

    def update_cake_layer(self, layer_id: int, layer_update: admin_schemas.ComponentUpdate) -> Optional[
        admin_schemas.CakeLayerResponse]:
        db_layer = self.db.query(cake_models.CakeLayer).filter(cake_models.CakeLayer.id == layer_id).first()
        if not db_layer:
            return None

        update_data = layer_update.model_dump(exclude_unset=True)
        for field, value in update_data.items():
            setattr(db_layer, field, value)

        self.db.commit()
        self.db.refresh(db_layer)
        return admin_schemas.CakeLayerResponse.model_validate(db_layer)

    def delete_cake_layer(self, layer_id: int) -> bool:
        db_layer = self.db.query(cake_models.CakeLayer).filter(cake_models.CakeLayer.id == layer_id).first()
        if not db_layer:
            return False

        self.db.delete(db_layer)
        self.db.commit()
        return True

    # CRUD для кремов
    def get_all_creams(self) -> List[admin_schemas.CreamResponse]:
        creams = self.cake_repo.get_all_creams()
        return [admin_schemas.CreamResponse.model_validate(cream) for cream in creams]

    def create_cream(self, cream_data: admin_schemas.ComponentCreate) -> cake_models.Cream:
        db_cream = cake_models.Cream(
            name=cream_data.name,
            description=cream_data.description,
            price_per_unit=cream_data.price_per_unit
        )
        self.db.add(db_cream)
        self.db.commit()
        self.db.refresh(db_cream)
        return db_cream

    def update_cream(self, cream_id: int, cream_update: admin_schemas.ComponentUpdate) -> Optional[
        admin_schemas.CreamResponse]:
        db_cream = self.db.query(cake_models.Cream).filter(cake_models.Cream.id == cream_id).first()
        if not db_cream:
            return None

        update_data = cream_update.model_dump(exclude_unset=True)
        for field, value in update_data.items():
            setattr(db_cream, field, value)

        self.db.commit()
        self.db.refresh(db_cream)
        return admin_schemas.CreamResponse.model_validate(db_cream)

    def delete_cream(self, cream_id: int) -> bool:
        db_cream = self.db.query(cake_models.Cream).filter(cake_models.Cream.id == cream_id).first()
        if not db_cream:
            return False

        self.db.delete(db_cream)
        self.db.commit()
        return True

    # CRUD для начинок
    def get_all_fillings(self) -> List[admin_schemas.FillingResponse]:
        fillings = self.cake_repo.get_all_fillings()
        return [admin_schemas.FillingResponse.model_validate(filling) for filling in fillings]

    def create_filling(self, filling_data: admin_schemas.ComponentCreate) -> cake_models.Filling:
        db_filling = cake_models.Filling(
            name=filling_data.name,
            description=filling_data.description,
            price_per_unit=filling_data.price_per_unit
        )
        self.db.add(db_filling)
        self.db.commit()
        self.db.refresh(db_filling)
        return db_filling

    def update_filling(self, filling_id: int, filling_update: admin_schemas.ComponentUpdate) -> Optional[
        admin_schemas.FillingResponse]:
        db_filling = self.db.query(cake_models.Filling).filter(cake_models.Filling.id == filling_id).first()
        if not db_filling:
            return None

        update_data = filling_update.model_dump(exclude_unset=True)
        for field, value in update_data.items():
            setattr(db_filling, field, value)

        self.db.commit()
        self.db.refresh(db_filling)
        return admin_schemas.FillingResponse.model_validate(db_filling)

    def delete_filling(self, filling_id: int) -> bool:
        db_filling = self.db.query(cake_models.Filling).filter(cake_models.Filling.id == filling_id).first()
        if not db_filling:
            return False

        self.db.delete(db_filling)
        self.db.commit()
        return True

    # CRUD для украшений
    def get_all_decorations(self) -> List[admin_schemas.DecorationResponse]:
        decorations = self.cake_repo.get_all_decorations()
        return [admin_schemas.DecorationResponse.model_validate(decoration) for decoration in decorations]

    def create_decoration(self, decoration_data: admin_schemas.ComponentCreate) -> cake_models.Decoration:
        db_decoration = cake_models.Decoration(
            name=decoration_data.name,
            description=decoration_data.description,
            price_per_unit=decoration_data.price_per_unit
        )
        self.db.add(db_decoration)
        self.db.commit()
        self.db.refresh(db_decoration)
        return db_decoration

    def update_decoration(self, decoration_id: int, decoration_update: admin_schemas.ComponentUpdate) -> Optional[
        admin_schemas.DecorationResponse]:
        db_decoration = self.db.query(cake_models.Decoration).filter(cake_models.Decoration.id == decoration_id).first()
        if not db_decoration:
            return None

        update_data = decoration_update.model_dump(exclude_unset=True)
        for field, value in update_data.items():
            setattr(db_decoration, field, value)

        self.db.commit()
        self.db.refresh(db_decoration)
        return admin_schemas.DecorationResponse.model_validate(db_decoration)

    def delete_decoration(self, decoration_id: int) -> bool:
        db_decoration = self.db.query(cake_models.Decoration).filter(cake_models.Decoration.id == decoration_id).first()
        if not db_decoration:
            return False

        self.db.delete(db_decoration)
        self.db.commit()
        return True