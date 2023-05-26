from functools import lru_cache
from pydantic import BaseSettings


# Loading data from config file
class Settings(BaseSettings):
    database_host: str
    database_port: int
    postgres_user: str
    postgres_password: str
    postgres_db: str

    class Config:
        env_file = ".env.prod"


# Saving environment variables in cache
@lru_cache()
def get_settings() -> Settings:
    return Settings()
