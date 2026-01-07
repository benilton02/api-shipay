from domain.repositories.users_repository import UsersRepository
from application.dto.create_user_dto import CreateUserDTO
from application.dto.read_user_dto import ReadUserDTO, ReadClaimDTO
from starlette.status import (
    HTTP_200_OK,
    HTTP_201_CREATED,
    HTTP_400_BAD_REQUEST,
    HTTP_500_INTERNAL_SERVER_ERROR,
)


class UsersUseCase:
    """Use case para gerenciamento de usuários"""

    def __init__(self):
        self.users_repository = UsersRepository()

    async def create_user(self, user_dto: CreateUserDTO):
        """Criar um usuário"""
        items, total = self.users_repository.read(
            page=1, per_page=10, email=user_dto.email
        )

        if items:
            status_code, content = HTTP_400_BAD_REQUEST, {
                "message": f"The {user_dto.email} already exist"
            }

        else:
            result = self.users_repository.create(user_dto)

            if isinstance(result, bool):
                status_code, content = HTTP_201_CREATED, {
                    "message": "User created successful"
                }

            else:
                status_code, content = HTTP_500_INTERNAL_SERVER_ERROR, {
                    "message": result
                }

        return status_code, content

    async def read_user(self, email: str, page: int, per_page: int):
        """Procurar usuários por paginação"""
        users, total = self.users_repository.read(
            email=email, page=page, per_page=per_page
        )

        content = [
            ReadUserDTO(
                role_id=user.role_id,
                name=user.name,
                id=user.id,
                email=user.email,
                created_at=user.created_at,
                updated_at=user.updated_at,
                claims=[
                    ReadClaimDTO(
                        id=claim.id,
                        active=claim.active,
                        description=claim.description,
                    )
                    for claim in user.claims
                ],
            )
            for user in users
        ]

        return HTTP_200_OK, {"items": total, "users": content}
