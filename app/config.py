from pydantic_settings import BaseSettings
from typing import List


class Settings(BaseSettings):
    
    # Application
    APP_NAME: str = "Library Management API"
    VERSION: str = "1.0.0"
    DEBUG: bool = True
    
    # Server
    HOST: str = "0.0.0.0"
    PORT: int = 8000
    
    # Database
    DATABASE_URL: str
    
    # Security
    SECRET_KEY: str
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30
    
    # CORS
    ALLOWED_ORIGINS: List[str] = [
        "http://localhost:3000",
        "http://localhost:8000"
    ]
    
    class Config:
        env_file = ".env"
        case_sensitive = True

settings = Settings()