# reset_db.py
from database import engine, Base
from users.models import User
from cakes.models import Cake, CakeLayer, Cream, Filling, Decoration
from orders.models import Order, Payment
from constructor.models import CustomCake

print("🗑️  Удаляем все таблицы...")
Base.metadata.drop_all(bind=engine)

print("🔄 Создаем таблицы заново...")
Base.metadata.create_all(bind=engine)

print("✅ База данных пересоздана")