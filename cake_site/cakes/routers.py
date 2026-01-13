from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from . import schemas, services
from database import get_db

router = APIRouter()

@router.get("/", response_model=List[schemas.CakeResponse])
def get_all_cakes(db: Session = Depends(get_db)):
    cake_service = services.CakeService(db)
    return cake_service.get_all_cakes()

@router.get("/{cake_id}", response_model=schemas.CakeResponse)
def get_cake_detail(cake_id: int, db: Session = Depends(get_db)):
    cake_service = services.CakeService(db)
    cake = cake_service.get_cake_by_id(cake_id)
    if not cake:
        raise HTTPException(status_code=404, detail="Cake not found")
    return cake

@router.get("/components/all")
def get_all_components(db: Session = Depends(get_db)):
    cake_service = services.CakeService(db)
    return cake_service.get_available_components()