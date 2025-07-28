from pydantic_settings import BaseSettings
from pathlib import Path

class Settings(BaseSettings):
    DATABASE_URL: str
    DATA_PATH: Path = Path("./data")
    class Config:
        env_file = ".env"

settings = Settings()