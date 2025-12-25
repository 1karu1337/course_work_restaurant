import os
from pathlib import Path
from pydantic_settings import BaseSettings, SettingsConfigDict

# Находим путь к папке, где лежит этот файл (app/core)
# .parent.parent.parent — это выход на уровень корня проекта (course_work_restaurant)
BASE_DIR = Path(__file__).resolve().parent.parent.parent
ENV_FILE = os.path.join(BASE_DIR, ".env")

class Settings(BaseSettings):
    DATABASE_URL: str
    SECRET_KEY: str
    ALGORITHM: str
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60

    # Явно указываем абсолютный путь к .env
    model_config = SettingsConfigDict(
        env_file=ENV_FILE, 
        env_file_encoding='utf-8',
        extra="ignore" # Игнорировать лишние переменные в .env
    )

try:
    settings = Settings()
except Exception as e:
    print(f"ОШИБКА: Не удалось загрузить настройки. Проверь файл {ENV_FILE}")
    raise e