# settings.py
from pydantic import BaseSettings

class Settings(BaseSettings):
    database_url: str = "sqlite:///./hotel.db"
    app_name: str = "Hotel API"

    class Config:
        env_file = ".env"

def get_settings():
    return Settings()