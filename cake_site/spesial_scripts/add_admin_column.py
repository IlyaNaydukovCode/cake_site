from database import SessionLocal
from sqlalchemy import text


def add_admin_column():
    db = SessionLocal()
    try:
        print("🔄 Добавляем столбец is_admin в таблицу users...")

        check_query = text("""
            SELECT column_name 
            FROM information_schema.columns 
            WHERE table_name = 'users' AND column_name = 'is_admin'
        """)
        result = db.execute(check_query).fetchone()

        if result:
            print("✅ Столбец is_admin уже существует")
        else:
            alter_query = text("ALTER TABLE users ADD COLUMN is_admin BOOLEAN DEFAULT FALSE")
            db.execute(alter_query)
            db.commit()
            print("✅ Столбец is_admin успешно добавлен в таблицу users")

            update_query = text("UPDATE users SET is_admin = FALSE WHERE is_admin IS NULL")
            db.execute(update_query)
            db.commit()
            print("✅ Существующие пользователи обновлены")

    except Exception as e:
        db.rollback()
        print(f"❌ Ошибка при добавлении столбца: {e}")
    finally:
        db.close()


if __name__ == "__main__":
    add_admin_column()