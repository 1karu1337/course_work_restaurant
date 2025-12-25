import asyncio
import sys
from logging.config import fileConfig
from os.path import dirname, abspath

from sqlalchemy import pool
from sqlalchemy.ext.asyncio import async_engine_from_config # Важно: async!
from alembic import context

# Добавляем путь к приложению
sys.path.insert(0, dirname(dirname(abspath(__file__))))

from app.core.config import settings
from app.core.database import Base
from app.models.user import User, Role

config = context.config

# Передаем URL из нашего конфига в Alembic
config.set_main_option("sqlalchemy.url", settings.DATABASE_URL.replace("%", "%%"))

if config.config_file_name is not None:
    fileConfig(config.config_file_name)

target_metadata = Base.metadata

def do_run_migrations(connection):
    context.configure(connection=connection, target_metadata=target_metadata)
    with context.begin_transaction():
        context.run_migrations()

async def run_migrations_online() -> None:
    # Здесь мы создаем асинхронный движок
    connectable = async_engine_from_config(
        config.get_section(config.config_ini_section, {}),
        prefix="sqlalchemy.",
        poolclass=pool.NullPool,
    )

    async with connectable.connect() as connection:
        await connection.run_sync(do_run_migrations)

    await connectable.dispose()

if context.is_offline_mode():
    # Нам не нужен оффлайн режим для асинхронного драйвера в рамках курсовой
    pass
else:
    asyncio.run(run_migrations_online())