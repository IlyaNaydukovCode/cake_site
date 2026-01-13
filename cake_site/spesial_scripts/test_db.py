from sqlalchemy import create_engine, text
import sys

# Попробуйте разные URL
urls_to_test = [
    "postgresql://cake_user:password@localhost:5432/cake_site"
]

for url in urls_to_test:
    try:
        print(f"Пытаюсь подключиться к: {url}")
        engine = create_engine(url)
        with engine.connect() as conn:
            result = conn.execute(text("SELECT 1"))
            print(f"✓ Успешное подключение к: {url}")
            break
    except Exception as e:
        print(f"✗ Ошибка подключения к {url}: {e}")