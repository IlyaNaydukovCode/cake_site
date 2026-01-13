import sys
import os

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from database import Base, engine

try:
    from users.models import User
    
    try:
        from cakes.models import Cake, CakeLayer, Cream, Filling, Decoration
    except ImportError:
        print("Модели cakes не найдены, продолжаем...")
        
    try:
        from constructor.models import CustomCake
    except ImportError:
        print("Модели constructor не найдены, продолжаем...")
        
    try:
        from orders.models import Order
    except ImportError:
        print("Модели orders не найдены, продолжаем...")
    
    Base.metadata.create_all(bind=engine)
    print("Модели инициализированы")
    
except Exception as e:
    print(f"Предупреждение при инициализации моделей: {e}")
    print("Продолжаем выполнение...")

from commands import cli

if __name__ == '__main__':
    cli()