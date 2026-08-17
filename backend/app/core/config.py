from functools import lru_cache
from typing import Literal
from urllib.parse import quote

from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    app_name: str = "WedLens API"
    app_env: Literal["local", "test", "production"] = "local"
    debug: bool = False
    log_level: str = "INFO"
    api_prefix: str = "/api"
    cors_origins: str = "http://localhost:5173"
    postgres_db: str = "wedlens"
    postgres_user: str = "wedlens"
    postgres_password: str = "wedlens"
    postgres_host: str = "localhost"
    postgres_port: int = 5432

    @property
    def cors_origin_list(self) -> list[str]:
        return [origin.strip() for origin in self.cors_origins.split(",") if origin.strip()]

    @property
    def database_url(self) -> str:
        """Build a safely escaped SQLAlchemy URL from the shared PostgreSQL settings."""
        user = quote(self.postgres_user, safe="")
        password = quote(self.postgres_password, safe="")
        database = quote(self.postgres_db, safe="")
        return (
            f"postgresql+psycopg://{user}:{password}@{self.postgres_host}:"
            f"{self.postgres_port}/{database}"
        )


@lru_cache
def get_settings() -> Settings:
    return Settings()
