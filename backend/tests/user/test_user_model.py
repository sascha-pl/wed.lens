from app.models import User


def test_user_model_does_not_store_a_plain_password() -> None:
    columns = User.__table__.columns

    assert set(columns.keys()) == {"id", "name", "email", "password_hash", "date_created"}
    assert columns["email"].unique
    assert columns["password_hash"].nullable is False
