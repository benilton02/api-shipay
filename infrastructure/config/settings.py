"""Configurações da aplicação"""

from pydantic_settings import BaseSettings
from pydantic import Field


class Settings(BaseSettings):
    """Configurações da aplicação"""
    
    # API
    api_title: str = "Shipay API"
    api_description: str = "API desenvolvida com Clean Architecture"
    api_version: str = "1.0.0"
    
    # Server
    host: str = "0.0.0.0"
    port: int = 8000
    reload: bool = True
    
    # CORS
    cors_origins: list[str] = ["*"]
    cors_allow_credentials: bool = True
    cors_allow_methods: list[str] = ["*"]
    cors_allow_headers: list[str] = ["*"]
    
    # Database
    database_url: str = Field(default="sqlite:///:memory:", env="DATABASE_URL") or ''
    
    class Config:
        env_file = ".env"
        case_sensitive = False


settings = Settings()

