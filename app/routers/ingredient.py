from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy.orm import selectinload
from typing import List

from core.database import get_db
from core.dependencies import RoleChecker
from models.ingredient import Ingredient, MenuItemIngredient
from models.menu import MenuItem
from schemas.ingredient import (
    IngredientCreate, IngredientRead, 
    RecipeLinkCreate, RecipeRead
)

router = APIRouter(prefix="/ingredients", tags=["ingredients"])

is_staff = RoleChecker(["admin", "manager"])

@router.get("/", response_model=List[IngredientRead])
async def list_ingredients(db: AsyncSession = Depends(get_db)):
    """Список всех продуктов на складе"""
    result = await db.execute(select(Ingredient))
    return result.scalars().all()

@router.post("/", response_model=IngredientRead)
async def create_ingredient(
    ing_in: IngredientCreate, 
    db: AsyncSession = Depends(get_db),
    current_user = Depends(is_staff)
):
    new_ing = Ingredient(**ing_in.model_dump())
    db.add(new_ing)
    await db.commit()
    await db.refresh(new_ing)
    return new_ing


@router.post("/link-to-menu", status_code=status.HTTP_201_CREATED)
async def link_ingredient_to_item(
    link_in: RecipeLinkCreate, 
    db: AsyncSession = Depends(get_db),
    current_user = Depends(is_staff)
):
    item = await db.get(MenuItem, link_in.menu_item_id)
    ing = await db.get(Ingredient, link_in.ingredient_id)
    
    if not item or not ing:
        raise HTTPException(status_code=404, detail="MenuItem or Ingredient not found")

    new_link = MenuItemIngredient(**link_in.model_dump())
    await db.merge(new_link)
    await db.commit()
    return {"message": f"Ingredient {ing.name} linked to {item.name}"}

@router.get("/recipe/{menu_item_id}", response_model=List[RecipeRead])
async def get_recipe(menu_item_id: int, db: AsyncSession = Depends(get_db)):
    """Посмотреть состав конкретного блюда"""
    result = await db.execute(
        select(MenuItemIngredient)
        .options(selectinload(MenuItemIngredient.ingredient))
        .where(MenuItemIngredient.menu_item_id == menu_item_id)
    )
    links = result.scalars().all()
    
    return [
        {
            "ingredient_id": l.ingredient_id,
            "ingredient_name": l.ingredient.name,
            "amount": l.amount,
            "unit": l.ingredient.unit
        } for l in links
    ]