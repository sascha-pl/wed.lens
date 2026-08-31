from app.db.session import SessionLocal
from app.services.photo_service import PhotoService
from app.services.storage.local_db import LocalDatabaseStorageService


def main() -> None:
    db_session = SessionLocal()

    try:
        ldb = LocalDatabaseStorageService(db_session)

        PhotoService(db_session=db_session).cleanUp(storage_service=ldb)

        ldb.cleanUp()

        db_session.commit()
    except Exception:
        db_session.rollback()
        raise
    finally:
        db_session.close()


if __name__ == "__main__":
    main()
