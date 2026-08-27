from app.db.session import SessionLocal
from app.services.userservice import UserService


def main() -> None:
    db_session = SessionLocal()

    try:
        user_service = UserService(db_session)

        user_service.cleanup()

        db_session.commit()
    except Exception:
        db_session.rollback()
        raise
    finally:
        db_session.close()


if __name__ == "__main__":
    main()
