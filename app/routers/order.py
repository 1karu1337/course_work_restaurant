from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy.orm import selectinload
from typing import List

from models.menu import MenuItem
from core.database import get_db
from core.dependencies import RoleChecker, get_current_user
from models.order import Order, OrderItem, OrderStatus
from schemas.order import OrderCreate, OrderRead, OrderStatusUpdate

router = APIRouter(prefix="/orders", tags=["orders"])

is_staff = RoleChecker(["admin", "manager", "staff"])

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

@router.get("/my", response_model=List[OrderRead])
async def get_my_orders(
    db: AsyncSession = Depends(get_db),
    current_user = Depends(get_current_user)
):
    """История заказов текущего пользователя (Клиента)"""
    result = await db.execute(
        select(Order)
        .options(selectinload(Order.items))
        .where(Order.user_id == current_user.id)
        .order_by(Order.created_at.desc())
    )
    return result.scalars().all()

@router.get("/all", response_model=List[OrderRead])
async def get_all_orders(
    db: AsyncSession = Depends(get_db),
    current_user = Depends(is_staff)
):
    """Список всех заказов для персонала (Админ/Менеджер/Официант)"""
    result = await db.execute(
        select(Order)
        .options(selectinload(Order.items))
        .order_by(Order.created_at.desc())
    )
    return result.scalars().all()

@router.patch("/{order_id}/status", response_model=OrderRead)
async def update_order_status(
    order_id: int,
    status_update: OrderStatusUpdate,
    db: AsyncSession = Depends(get_db),
    current_user = Depends(is_staff)
):
    """Изменить статус заказа (Только для персонала)"""
    result = await db.execute(
        select(Order)
        .options(selectinload(Order.items))
        .where(Order.id == order_id)
    )
    order = result.scalars().first()
    
    if not order:
        raise HTTPException(status_code=404, detail="Order not found")
    
    order.status = status_update.status
    await db.commit()
    await db.refresh(order)
    return order