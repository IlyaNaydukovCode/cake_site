from database import SessionLocal
from sqlalchemy import text


def make_user_admin(email: str):
    db = SessionLocal()
    try:
        print(f"🔄 Назначаем пользователя {email} администратором...")

        check_user = text("SELECT id FROM users WHERE email = :email")
        user = db.execute(check_user, {"email": email}).fetchone()

        if not user:
            print(f"❌ Пользователь с email {email} не найден")
            return

        update_query = text("UPDATE users SET is_admin = TRUE WHERE email = :email")
        db.execute(update_query, {"email": email})
        db.commit()

        print(f"✅ Пользователь {email} теперь администратор")

    except Exception as e:
        db.rollback()
        print(f"❌ Ошибка: {e}")
    finally:
        db.close()


if __name__ == "__main__":
    user_email = "inaydukov@mail.ru"
    make_user_admin(user_email)