import asyncio
import sys
from os.path import dirname, abspath

# Добавляем путь, чтобы импорты работали без приставки app
sys.path.insert(0, dirname(abspath(__file__)))

from core.database import async_session
from core.security import get_password_hash
from models.user import Role, User
from models.restaurant import Restaurant, Table
from models.menu import Category, MenuItem
from models.ingredient import Ingredient, MenuItemIngredient
from sqlalchemy import select

async def seed():
    async with async_session() as session:
        print("🚀 Начинаем наполнение базы данных...")

        # 1. Создание ролей
        roles_data = [
            Role(id=1, name="customer", description="Клиент"),
            Role(id=2, name="staff", description="Официант"),
            Role(id=3, name="manager", description="Менеджер"),
            Role(id=4, name="admin", description="Администратор")
        ]
        for r in roles_data:
            await session.merge(r)
        await session.commit()
        print("✅ Роли созданы.")

        # 2. Создание пользователей (Пароль = Логин)
        users_data = [
            ("admin", "admin@resto.ru", 4),
            ("manager", "manager@resto.ru", 3),
            ("staff", "staff@resto.ru", 2),
            ("user", "user@resto.ru", 1),
        ]
        for username, email, role_id in users_data:
            user_check = await session.execute(select(User).where(User.username == username))
            if not user_check.scalars().first():
                new_user = User(
                    username=username,
                    email=email,
                    hashed_password=get_password_hash(username), # Пароль как логин
                    role_id=role_id
                )
                session.add(new_user)
        await session.commit()
        print("✅ Пользователи созданы (пароли совпадают с логинами).")

        # 3. Создание ресторана и столиков
        rest = Restaurant(name="Gourmet Plaza", address="ул. Пушкина, 10", phone="+79991234567")
        session.add(rest)
        await session.flush()

        tables = [Table(number=i, capacity=4, restaurant_id=rest.id) for i in range(1, 6)]
        session.add_all(tables)
        print("✅ Ресторан и столики добавлены.")

        # 4. Категории и Меню
        cat1 = Category(name="Пицца")
        cat2 = Category(name="Напитки")
        session.add_all([cat1, cat2])
        await session.flush()

        items = [
            MenuItem(name="Маргарита", price=450.0, category_id=cat1.id, is_available=True),
            MenuItem(name="Пепперони", price=550.0, category_id=cat1.id, is_available=True),
            MenuItem(name="Кола 0.5", price=120.0, category_id=cat2.id, is_available=True),
        ]
        session.add_all(items)
        print("✅ Меню заполнено.")

        # 5. Ингредиенты
        ing1 = Ingredient(name="Мука", unit="кг", stock_quantity=50.0)
        ing2 = Ingredient(name="Сыр Моцарелла", unit="кг", stock_quantity=20.0)
        session.add_all([ing1, ing2])
        
        await session.commit()
        print("🏁 Наполнение завершено успешно!")

if __name__ == "__main__":
    asyncio.run(seed())