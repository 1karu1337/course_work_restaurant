from fastapi import APIRouter, Depends, Query, HTTPException
from fastapi.responses import Response
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from typing import Literal

from core.database import get_db
from core.dependencies import RoleChecker
from models.menu import MenuItem
from services import export_service

router = APIRouter(prefix="/export", tags=["export"])

is_staff = RoleChecker(["admin", "manager"])

@router.get("/menu")
async def export_menu(
    format: Literal["json", "csv"] = Query(..., description="Формат выгрузки"),
    db: AsyncSession = Depends(get_db),
    current_user = Depends(is_staff)
):
    result = await db.execute(select(MenuItem))
    items = result.scalars().all()
    
    data = [
        {
            "id": i.id,
            "name": i.name,
            "price": i.price,
            "available": i.is_available,
            "category_id": i.category_id
        } for i in items
    ]

    if format == "json":
        content = export_service.to_json(data)
        media_type = "application/json"
        filename = "menu_export.json"
    else:
        content = export_service.to_csv(data)
        media_type = "text/csv"
        filename = "menu_export.csv"

    return Response(
        content=content,
        media_type=media_type,
        headers={
            "Content-Disposition": f"attachment; filename={filename}"
        }
    )