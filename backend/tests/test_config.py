from app.core.config import Settings


def test_database_url_is_built_from_shared_postgres_settings() -> None:
    settings = Settings(
        postgres_db="wedlens_test",
        postgres_user="test@example",
        postgres_password="pass/word",
        postgres_host="database",
        postgres_port=5433,
    )

    assert settings.database_url == (
        "postgresql+psycopg://test%40example:pass%2Fword@database:5433/wedlens_test"
    )
