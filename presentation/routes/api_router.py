"""Router principal da API"""

from fastapi import APIRouter
from presentation.controllers.health_controller import HealthController
from presentation.controllers.user_controller import UserController


def create_api_router() -> APIRouter:
    """
    Cria e configura o router principal da API.
    
    Returns:
        APIRouter: Router configurado com todas as rotas
    """
    api_router = APIRouter()

    # Registra os controllers
    # Health controller (rotas raiz sem prefixo)
    health_controller = HealthController()
    api_router.include_router(health_controller.register_routes())

    # User controller
    user_controller = UserController()
    api_router.include_router(user_controller.register_routes(), prefix="/users")

    # Adicione outros routers aqui conforme necessário
    # Exemplo para rotas com prefixo /api/v1:
    # api_v1_router = APIRouter(prefix="/api/v1")
    # from presentation.routes.user_routes import user_router
    # api_v1_router.include_router(user_router)
    # api_router.include_router(api_v1_router)

    return api_router

