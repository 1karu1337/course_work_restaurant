import os
import subprocess
from datetime import datetime
from core.config import settings

def create_db_backup():
    backup_dir = "backups"
    if not os.path.exists(backup_dir):
        os.makedirs(backup_dir)

    db_url = settings.DATABASE_URL.replace("+asyncpg", "")
    
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    backup_path = os.path.join(backup_dir, f"backup_{timestamp}.sql")
    try:
        command = f"pg_dump {db_url} > {backup_path}"
        
        subprocess.run(command, shell=True, check=True)
        
        return {
            "status": "success",
            "filename": f"backup_{timestamp}.sql",
            "path": abspath(backup_path),
            "size_kb": os.path.getsize(backup_path) // 1024
        }
    except Exception as e:
        return {"status": "error", "message": str(e)}

def abspath(path):
    return os.path.abspath(path)