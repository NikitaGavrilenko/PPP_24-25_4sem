from pydantic import BaseSettings

class Settings(BaseSettings):
    SQLALCHEMY_DATABASE_URL: str = "sqlite:///./db.sqlite3"
    SECRET_KEY: str = "SECRET_KEY"
    ALGORITHM: str = "HS256"

    class Config:
        env_file = ".env"

settings = Settings()