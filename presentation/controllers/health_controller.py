"""Controller para endpoints de health check"""

from fastapi import APIRouter
from fastapi.responses import JSONResponse


class HealthController:
    """Controller responsável pelos endpoints de health check"""

    def __init__(self):
        self.router = APIRouter(tags=["Health"])

    def register_routes(self) -> APIRouter:
        """Registra as rotas do controller"""
        self.router.add_api_route("/", self.root, methods=["GET"])
        self.router.add_api_route("/health", self.health_check, methods=["GET"])
        return self.router

    async def root(self) -> JSONResponse:
        """Endpoint raiz da API"""
        return JSONResponse(
            content={
                "message": "Welcome to Shipay API",
                "version": "1.0.0",
                "status": "running",
            }
        )

    async def health_check(self) -> JSONResponse:
        """Endpoint de health check"""
        return JSONResponse(content={"status": "healthy"})
