from pydantic import BaseSettings


class Settings(BaseSettings):
    DATABASE_URL: str = "postgresql+asyncpg://user:pass@localhost:5432/db"
    DATABASE_URL_SYNC: str = "postgresql://user:pass@localhost:5432/db"
    CELERY_BROKER_URL: str = "amqp://localhost:5672"
    CELERY_RESULT_BACKEND: str = "redis://localhost:6379/0"


config = Settings()
