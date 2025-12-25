from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from typing import List

from core.database import get_db
from core.dependencies import RoleChecker
from models.restaurant import Table, Restaurant
from schemas.table import TableCreate, TableRead

router = APIRouter(prefix="/tables", tags=["tables"])

is_staff = RoleChecker(["admin", "manager"])

@router.get("/", response_model=List[TableRead])
async def list_tables(restaurant_id: int = None, db: AsyncSession = Depends(get_db)):
    query = select(Table)
    if restaurant_id:
        query = query.where(Table.restaurant_id == restaurant_id)
    
    result = await db.execute(query)
    return result.scalars().all()

@router.post("/", response_model=TableRead, status_code=status.HTTP_201_CREATED)
async def create_table(
    table_in: TableCreate, 
    db: AsyncSession = Depends(get_db),
    current_user = Depends(is_staff)
):
    res = await db.execute(select(Restaurant).where(Restaurant.id == table_in.restaurant_id))
    if not res.scalars().first():
        raise HTTPException(status_code=404, detail="Restaurant not found")
    
    new_table = Table(**table_in.model_dump())
    db.add(new_table)
    await db.commit()
    await db.refresh(new_table)
    return new_table

@router.delete("/{table_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_table(
    table_id: int, 
    db: AsyncSession = Depends(get_db),
    current_user = Depends(is_staff)
):
    result = await db.execute(select(Table).where(Table.id == table_id))
    table = result.scalars().first()
    if not table:
        raise HTTPException(status_code=404, detail="Table not found")
    
    await db.delete(table)
    await db.commit()
    return None