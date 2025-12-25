from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy.orm import selectinload
from typing import List

from core.database import get_db
from core.dependencies import get_current_user
from models.order import Order, OrderItem
from models.menu import MenuItem
from schemas.order import OrderCreate, OrderRead

router = APIRouter(prefix="/orders", tags=["orders"])

@router.post("/", response_model=OrderRead, status_code=status.HTTP_201_CREATED)
async def create_order(
    order_in: OrderCreate, 
    db: AsyncSession = Depends(get_db),
    current_user = Depends(get_current_user)
):
    new_order = Order(
        user_id=current_user.id,
        table_id=order_in.table_id
    )
    db.add(new_order)
    
    await db.flush()

    for item in order_in.items:
        res = await db.execute(select(MenuItem).where(MenuItem.id == item.menu_item_id))
        menu_item = res.scalars().first()
        
        if not menu_item:
            raise HTTPException(
                status_code=404, 
                detail=f"Блюдо с ID {item.menu_item_id} не найдено"
            )
        
        if not menu_item.is_available:
            raise HTTPException(
                status_code=400, 
                detail=f"Блюдо {menu_item.name} сейчас недоступно"
            )

        order_item = OrderItem(
            order_id=new_order.id,
            menu_item_id=menu_item.id,
            quantity=item.quantity,
            price_at_order=menu_item.price
        )
        db.add(order_item)

    await db.commit()
    
    result = await db.execute(
        select(Order)
        .options(selectinload(Order.items))
        .where(Order.id == new_order.id)
    )
    return result.scalars().first()