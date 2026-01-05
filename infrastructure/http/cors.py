"""Configuração de CORS para a aplicação"""

from fastapi.middleware.cors import CORSMiddleware
from fastapi import FastAPI
from infrastructure.config.settings import settings


def setup_cors(app: FastAPI) -> None:
    """
    Configura o middleware CORS na aplicação FastAPI.

    Args:
        app: Instância do FastAPI
    """
    app.add_middleware(
        CORSMiddleware,
        allow_origins=settings.cors_origins,
        allow_credentials=settings.cors_allow_credentials,
        allow_methods=settings.cors_allow_methods,
        allow_headers=settings.cors_allow_headers,
    )
