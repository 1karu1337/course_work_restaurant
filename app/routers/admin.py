from fastapi import APIRouter, Depends, HTTPException
from core.dependencies import RoleChecker
from services import backup_service

router = APIRouter(prefix="/admin", tags=["admin"])

is_admin = RoleChecker(["admin"])

@router.post("/backup")
async def trigger_backup(current_user = Depends(is_admin)):
    """Запуск создания резервной копии БД (Требование №3)"""
    result = backup_service.create_db_backup()
    
    if result["status"] == "error":
        raise HTTPException(status_code=500, detail=result["message"])
    
    return result