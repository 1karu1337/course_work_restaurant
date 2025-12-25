from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from typing import List

from core.database import get_db
from core.dependencies import RoleChecker
from models.restaurant import Restaurant
from schemas.restaurant import RestaurantCreate, RestaurantRead

router = APIRouter(prefix="/restaurants", tags=["restaurants"])

# Проверки ролей
is_admin = RoleChecker(["admin"])

@router.get("/", response_model=List[RestaurantRead])
async def list_restaurants(db: AsyncSession = Depends(get_db)):
    """Список всех ресторанов (доступно всем)"""
    result = await db.execute(select(Restaurant))
    return result.scalars().all()

@router.post("/", response_model=RestaurantRead, status_code=status.HTTP_201_CREATED)
async def create_restaurant(
    rest_in: RestaurantCreate, 
    db: AsyncSession = Depends(get_db),
    current_user = Depends(is_admin) # Только админ
):
    """Создать новый филиал (Только Админ)"""
    new_rest = Restaurant(**rest_in.model_dump())
    db.add(new_rest)
    await db.commit()
    await db.refresh(new_rest)
    return new_rest

@router.get("/{restaurant_id}", response_model=RestaurantRead)
async def get_restaurant(restaurant_id: int, db: AsyncSession = Depends(get_db)):
    """Информация о конкретном ресторане"""
    result = await db.execute(select(Restaurant).where(Restaurant.id == restaurant_id))
    rest = result.scalars().first()
    if not rest:
        raise HTTPException(status_code=404, detail="Restaurant not found")
    return rest

@router.delete("/{restaurant_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_restaurant(
    restaurant_id: int, 
    db: AsyncSession = Depends(get_db),
    current_user = Depends(is_admin)
):
    """Удалить филиал (Только Админ)"""
    result = await db.execute(select(Restaurant).where(Restaurant.id == restaurant_id))
    rest = result.scalars().first()
    if not rest:
        raise HTTPException(status_code=404, detail="Restaurant not found")
    
    await db.delete(rest)
    await db.commit()
    return None