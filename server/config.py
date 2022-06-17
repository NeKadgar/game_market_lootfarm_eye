from pydantic import BaseSettings


class Settings(BaseSettings):
    DATABASE_URL: str = "postgresql+asyncpg://user:pass@localhost/db"
    DATABASE_URL_SYNC: str = "postgresql://user:pass@localhost/db"


config = Settings()
