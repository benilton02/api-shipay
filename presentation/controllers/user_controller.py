"""Controller para endpoints de usuários"""

from fastapi import APIRouter, Query
from fastapi.responses import JSONResponse
from fastapi.encoders import jsonable_encoder
from application.dto.create_user_dto import CreateUserDTO
from shared.utils.password import hash_password
from application.use_cases.users_use_case import UsersUseCase
from typing import Optional


class UserController:
    """Controller responsável pelos endpoints de usuários"""

    def __init__(self):
        self.router = APIRouter(tags=["Users"])
        self.users_use_case = UsersUseCase()

    def register_routes(self) -> APIRouter:
        """Registra as rotas do controller"""

        self.router.add_api_route("", self.create_user, methods=["POST"])
        self.router.add_api_route("", self.read_user, methods=["GET"])
        return self.router

    async def create_user(self, user_dto: CreateUserDTO) -> JSONResponse:
        """Endpoint para criar um usuário"""
        # Criptografa a senha
        user_dto.password = hash_password(user_dto.password)
        status_code, content = await self.users_use_case.create_user(user_dto)

        return JSONResponse(
            content=content,
            status_code=status_code,
        )

    async def read_user(
        self,
        email: Optional[str] = Query(None, description="Email do usuário"),
        page: int = Query(1, ge=1, description="Número da página"),
        per_page: int = Query(10, ge=1, le=100, description="Itens por página"),
    ) -> JSONResponse:
        """Lista usuários com paginação"""

        status_code, content = await self.users_use_case.read_user(
            page=page, per_page=per_page, email=email
        )

        return JSONResponse(
            content=jsonable_encoder(content),
            status_code=status_code,
        )
