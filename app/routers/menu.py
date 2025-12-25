from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from typing import List, Optional

from core.database import get_db
from core.dependencies import RoleChecker
from models.menu import Category, MenuItem
from schemas.menu import (
    CategoryCreate, CategoryRead, 
    MenuItemCreate, MenuItemRead
)

router = APIRouter(prefix="/menu", tags=["menu"])

is_staff = RoleChecker(["admin", "manager"])

@router.get("/categories", response_model=List[CategoryRead])
async def list_categories(db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(Category))
    return result.scalars().all()

@router.post("/categories", response_model=CategoryRead)
async def create_category(
    cat_in: CategoryCreate, 
    db: AsyncSession = Depends(get_db),
    current_user = Depends(is_staff)
):
    new_cat = Category(**cat_in.model_dump())
    db.add(new_cat)
    await db.commit()
    await db.refresh(new_cat)
    return new_cat

@router.get("/items", response_model=List[MenuItemRead])
async def list_items(
    category_id: Optional[int] = None, 
    db: AsyncSession = Depends(get_db)
):
    query = select(MenuItem)
    if category_id:
        query = query.where(MenuItem.category_id == category_id)
    
    result = await db.execute(query)
    return result.scalars().all()

@router.post("/items", response_model=MenuItemRead)
async def create_item(
    item_in: MenuItemCreate, 
    db: AsyncSession = Depends(get_db),
    current_user = Depends(is_staff)
):
    cat_res = await db.execute(select(Category).where(Category.id == item_in.category_id))
    if not cat_res.scalars().first():
        raise HTTPException(status_code=404, detail="Category not found")
    
    new_item = MenuItem(**item_in.model_dump())
    db.add(new_item)
    await db.commit()
    await db.refresh(new_item)
    return new_item

@router.patch("/items/{item_id}", response_model=MenuItemRead)
async def update_item_availability(
    item_id: int, 
    is_available: bool,
    db: AsyncSession = Depends(get_db),
    current_user = Depends(is_staff)
):
    result = await db.execute(select(MenuItem).where(MenuItem.id == item_id))
    item = result.scalars().first()
    if not item:
        raise HTTPException(status_code=404, detail="Item not found")
    
    item.is_available = is_available
    await db.commit()
    await db.refresh(item)
    return item