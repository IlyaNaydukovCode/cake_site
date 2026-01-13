from fastapi import APIRouter, Depends, Form, HTTPException, status
from sqlalchemy.orm import Session
from typing import List, Optional
from database import get_db
from auth.service import get_current_user
from users import schemas as user_schemas
from cakes.schemas import CakeResponse
from orders.schemas import OrderResponse
from . import services, schemas

router = APIRouter()

async def get_current_admin(current_user: user_schemas.UserResponse = Depends(get_current_user)):
    if not current_user.is_admin:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not enough permissions. Admin access required."
        )
    return current_user

# УПРАВЛЕНИЕ ТОРТАМИ (АДМИН)

# Торты (готовые)

@router.get("/cakes", response_model=List[CakeResponse])
def get_all_cakes_admin(
    db: Session = Depends(get_db),
    current_user: user_schemas.UserResponse = Depends(get_current_admin)
):
    """Получить все торты для админ-панели (включая недоступные)"""
    from cakes.repositories import CakeRepository
    
    cake_repo = CakeRepository(db)
    cakes = cake_repo.get_all_cakes_admin()  # Используем новый метод
    return [CakeResponse.model_validate(cake) for cake in cakes]

# УПРАВЛЕНИЕ ТОРТАМИ (АДМИН)

@router.get("/cakes", response_model=List[CakeResponse])
def get_all_cakes_admin(
    db: Session = Depends(get_db),
    current_user: user_schemas.UserResponse = Depends(get_current_admin)
):
    """Получить все торты для админ-панели (включая недоступные)"""
    from cakes.repositories import CakeRepository
    
    cake_repo = CakeRepository(db)
    cakes = cake_repo.get_all_cakes_admin()
    return [CakeResponse.model_validate(cake) for cake in cakes]

@router.post("/cakes/formdata", response_model=CakeResponse)
def create_cake_formdata(
    name: str = Form(...),
    price: float = Form(...),
    description: Optional[str] = Form(None),
    image_url: Optional[str] = Form(None),
    weight: Optional[float] = Form(None),
    ingredients: Optional[str] = Form(None),
    is_available: Optional[bool] = Form(True),
    db: Session = Depends(get_db),
    current_user: user_schemas.UserResponse = Depends(get_current_admin)
):
    """Создать торт через FormData"""
    admin_service = services.AdminCakeService(db)
    
    # Создаем объект CakeCreate из FormData
    cake_create = schemas.CakeCreate(
        name=name,
        price=price,
        description=description,
        image_url=image_url,
        weight=weight,
        ingredients=ingredients
    )
    
    cake = admin_service.create_cake(cake_create)
    
    # Если нужно установить is_available при создании
    if is_available is not None:
        cake_update = schemas.CakeUpdate(is_available=is_available)
        admin_service.update_cake(cake.id, cake_update)
    
    return cake

@router.post("/cakes", response_model=CakeResponse)
def create_cake_json(
    cake_data: schemas.CakeCreate,
    db: Session = Depends(get_db),
    current_user: user_schemas.UserResponse = Depends(get_current_admin)
):
    """Создать торт (JSON версия)"""
    admin_service = services.AdminCakeService(db)
    return admin_service.create_cake(cake_data)

@router.put("/cakes/{cake_id}", response_model=CakeResponse)
def update_cake_json(
    cake_id: int,
    cake_update: schemas.CakeUpdate,
    db: Session = Depends(get_db),
    current_user: user_schemas.UserResponse = Depends(get_current_admin)
):
    admin_service = services.AdminCakeService(db)
    updated_cake = admin_service.update_cake(cake_id, cake_update)
    if not updated_cake:
        raise HTTPException(status_code=404, detail="Cake not found")
    return updated_cake

@router.delete("/cakes/{cake_id}")
def delete_cake(
    cake_id: int,
    db: Session = Depends(get_db),
    current_user: user_schemas.UserResponse = Depends(get_current_admin)
):
    admin_service = services.AdminCakeService(db)
    success = admin_service.delete_cake(cake_id)
    if not success:
        raise HTTPException(status_code=404, detail="Cake not found")
    return {"message": "Cake deleted successfully"}

# КОМПОНЕНТЫ ТОРТОВ (АДМИН)

@router.get("/cake-layers", response_model=List[schemas.CakeLayerResponse])
def get_all_cake_layers(
    db: Session = Depends(get_db),
    current_user: user_schemas.UserResponse = Depends(get_current_admin)
):
    admin_service = services.AdminCakeService(db)
    return admin_service.get_all_layers()

@router.post("/cake-layers", response_model=schemas.CakeLayerResponse)
def create_cake_layer(
    layer_data: schemas.ComponentCreate,
    db: Session = Depends(get_db),
    current_user: user_schemas.UserResponse = Depends(get_current_admin)
):
    admin_service = services.AdminCakeService(db)
    layer = admin_service.create_cake_layer(layer_data)
    return schemas.CakeLayerResponse.model_validate(layer)

@router.put("/cake-layers/{layer_id}", response_model=schemas.CakeLayerResponse)
def update_cake_layer(
    layer_id: int,
    layer_update: schemas.ComponentUpdate,
    db: Session = Depends(get_db),
    current_user: user_schemas.UserResponse = Depends(get_current_admin)
):
    admin_service = services.AdminCakeService(db)
    updated_layer = admin_service.update_cake_layer(layer_id, layer_update)
    if not updated_layer:
        raise HTTPException(status_code=404, detail="Cake layer not found")
    return updated_layer

@router.delete("/cake-layers/{layer_id}")
def delete_cake_layer(
    layer_id: int,
    db: Session = Depends(get_db),
    current_user: user_schemas.UserResponse = Depends(get_current_admin)
):
    admin_service = services.AdminCakeService(db)
    success = admin_service.delete_cake_layer(layer_id)
    if not success:
        raise HTTPException(status_code=404, detail="Cake layer not found")
    return {"message": "Cake layer deleted successfully"}

# КРЕМЫ (АДМИН)

@router.get("/creams", response_model=List[schemas.CreamResponse])
def get_all_creams(
    db: Session = Depends(get_db),
    current_user: user_schemas.UserResponse = Depends(get_current_admin)
):
    admin_service = services.AdminCakeService(db)
    return admin_service.get_all_creams()

@router.post("/creams", response_model=schemas.CreamResponse)
def create_cream(
    cream_data: schemas.ComponentCreate,
    db: Session = Depends(get_db),
    current_user: user_schemas.UserResponse = Depends(get_current_admin)
):
    admin_service = services.AdminCakeService(db)
    cream = admin_service.create_cream(cream_data)
    return schemas.CreamResponse.model_validate(cream)

@router.put("/creams/{cream_id}", response_model=schemas.CreamResponse)
def update_cream(
    cream_id: int,
    cream_update: schemas.ComponentUpdate,
    db: Session = Depends(get_db),
    current_user: user_schemas.UserResponse = Depends(get_current_admin)
):
    admin_service = services.AdminCakeService(db)
    updated_cream = admin_service.update_cream(cream_id, cream_update)
    if not updated_cream:
        raise HTTPException(status_code=404, detail="Cream not found")
    return updated_cream

@router.delete("/creams/{cream_id}")
def delete_cream(
    cream_id: int,
    db: Session = Depends(get_db),
    current_user: user_schemas.UserResponse = Depends(get_current_admin)
):
    admin_service = services.AdminCakeService(db)
    success = admin_service.delete_cream(cream_id)
    if not success:
        raise HTTPException(status_code=404, detail="Cream not found")
    return {"message": "Cream deleted successfully"}

# НАЧИНКИ (АДМИН)

@router.get("/fillings", response_model=List[schemas.FillingResponse])
def get_all_fillings(
    db: Session = Depends(get_db),
    current_user: user_schemas.UserResponse = Depends(get_current_admin)
):
    admin_service = services.AdminCakeService(db)
    return admin_service.get_all_fillings()

@router.post("/fillings", response_model=schemas.FillingResponse)
def create_filling(
    filling_data: schemas.ComponentCreate,
    db: Session = Depends(get_db),
    current_user: user_schemas.UserResponse = Depends(get_current_admin)
):
    admin_service = services.AdminCakeService(db)
    filling = admin_service.create_filling(filling_data)
    return schemas.FillingResponse.model_validate(filling)

@router.put("/fillings/{filling_id}", response_model=schemas.FillingResponse)
def update_filling(
    filling_id: int,
    filling_update: schemas.ComponentUpdate,
    db: Session = Depends(get_db),
    current_user: user_schemas.UserResponse = Depends(get_current_admin)
):
    admin_service = services.AdminCakeService(db)
    updated_filling = admin_service.update_filling(filling_id, filling_update)
    if not updated_filling:
        raise HTTPException(status_code=404, detail="Filling not found")
    return updated_filling

@router.delete("/fillings/{filling_id}")
def delete_filling(
    filling_id: int,
    db: Session = Depends(get_db),
    current_user: user_schemas.UserResponse = Depends(get_current_admin)
):
    admin_service = services.AdminCakeService(db)
    success = admin_service.delete_filling(filling_id)
    if not success:
        raise HTTPException(status_code=404, detail="Filling not found")
    return {"message": "Filling deleted successfully"}

# УКРАШЕНИЯ (АДМИН)

@router.get("/decorations", response_model=List[schemas.DecorationResponse])
def get_all_decorations(
    db: Session = Depends(get_db),
    current_user: user_schemas.UserResponse = Depends(get_current_admin)
):
    admin_service = services.AdminCakeService(db)
    return admin_service.get_all_decorations()

@router.post("/decorations", response_model=schemas.DecorationResponse)
def create_decoration(
    decoration_data: schemas.ComponentCreate,
    db: Session = Depends(get_db),
    current_user: user_schemas.UserResponse = Depends(get_current_admin)
):
    admin_service = services.AdminCakeService(db)
    decoration = admin_service.create_decoration(decoration_data)
    return schemas.DecorationResponse.model_validate(decoration)

@router.put("/decorations/{decoration_id}", response_model=schemas.DecorationResponse)
def update_decoration(
    decoration_id: int,
    decoration_update: schemas.ComponentUpdate,
    db: Session = Depends(get_db),
    current_user: user_schemas.UserResponse = Depends(get_current_admin)
):
    admin_service = services.AdminCakeService(db)
    updated_decoration = admin_service.update_decoration(decoration_id, decoration_update)
    if not updated_decoration:
        raise HTTPException(status_code=404, detail="Decoration not found")
    return updated_decoration

@router.delete("/decorations/{decoration_id}")
def delete_decoration(
    decoration_id: int,
    db: Session = Depends(get_db),
    current_user: user_schemas.UserResponse = Depends(get_current_admin)
):
    admin_service = services.AdminCakeService(db)
    success = admin_service.delete_decoration(decoration_id)
    if not success:
        raise HTTPException(status_code=404, detail="Decoration not found")
    return {"message": "Decoration deleted successfully"}

# Заказы (АДМИН)

@router.get("/orders", response_model=List[OrderResponse])
def get_all_orders(
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db),
    current_user: user_schemas.UserResponse = Depends(get_current_admin)
):
    """Получить все заказы (только для админов)"""
    from orders.models import Order
    
    # Получаем заказы (связанные объекты загрузятся лениво при обращении)
    orders = db.query(Order)\
        .order_by(Order.order_date.desc())\
        .offset(skip)\
        .limit(limit)\
        .all()
    
    # Преобразуем в схему ответа
    result = []
    for order in orders:
        order_dict = {
            "id": order.id,
            "user_id": order.user_id,
            "order_date": order.order_date,
            "status": order.status,
            "total_amount": order.total_amount,
            "delivery_type": order.delivery_type,
            "delivery_address": order.delivery_address,
            "delivery_date": order.delivery_date,
            "customer_notes": order.customer_notes,
            "quantity": order.quantity,
        }
        
        # Добавляем информацию о торте, если есть
        if order.cake_id and order.cake:
            order_dict["cake"] = {
                "id": order.cake.id,
                "name": order.cake.name,
                "price": order.cake.price
            }
        
        # Добавляем информацию о кастомном торте, если есть
        if order.custom_cake_id and order.custom_cake:
            order_dict["custom_cake"] = {
                "id": order.custom_cake.id,
                "name": order.custom_cake.name,
                "total_price": order.custom_cake.total_price
            }
        
        result.append(OrderResponse(**order_dict))
    
    return result

@router.get("/orders/{order_id}", response_model=OrderResponse)
def get_order_by_id(
    order_id: int,
    db: Session = Depends(get_db),
    current_user: user_schemas.UserResponse = Depends(get_current_admin)
):
    """Получить заказ по ID (только для админов)"""
    from orders.models import Order
    
    order = db.query(Order)\
        .filter(Order.id == order_id)\
        .first()
    
    if not order:
        raise HTTPException(status_code=404, detail="Order not found")
    
    order_dict = {
        "id": order.id,
        "user_id": order.user_id,
        "order_date": order.order_date,
        "status": order.status,
        "total_amount": order.total_amount,
        "delivery_type": order.delivery_type,
        "delivery_address": order.delivery_address,
        "delivery_date": order.delivery_date,
        "customer_notes": order.customer_notes,
        "quantity": order.quantity,
    }
    
    # Загружаем связанные объекты при обращении к ним
    if order.cake_id:
        # Ленивая загрузка сработает здесь
        order_dict["cake"] = {
            "id": order.cake.id,
            "name": order.cake.name,
            "price": order.cake.price
        }
    
    if order.custom_cake_id:
        # Ленивая загрузка сработает здесь
        order_dict["custom_cake"] = {
            "id": order.custom_cake.id,
            "name": order.custom_cake.name,
            "total_price": order.custom_cake.total_price
        }
    
    return OrderResponse(**order_dict)