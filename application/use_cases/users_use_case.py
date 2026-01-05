from domain.repositories.users_repository import UsersRepository
from application.dto.create_user_dto import CreateUserDTO
from application.dto.read_user_dto import ReadUserDTO, ReadClaimDTO
from starlette.status import HTTP_200_OK, HTTP_201_CREATED, HTTP_400_BAD_REQUEST, HTTP_404_NOT_FOUND, HTTP_500_INTERNAL_SERVER_ERROR

class UsersUseCase:
    """Use case para gerenciamento de usuários"""

    def __init__(self):
        self.users_repository = UsersRepository()

    async def create_user(self, user_dto: CreateUserDTO):
        """Criar um usuário"""
        user = self.users_repository.read(user_dto.email)
        
        if user:
            status_code, content = HTTP_400_BAD_REQUEST, {"message": f'The {user.email} already exist'}
        
        else:    
            result = self.users_repository.create(user_dto)

            if isinstance(result, bool):
                status_code, content = HTTP_201_CREATED, {"message": "User created successful"}
            
            else:
                status_code, content = HTTP_500_INTERNAL_SERVER_ERROR, {"message": result}
            
        return status_code, content
    
    async def read_user(self, email: str):
        """Procurar usuário por Email"""
        user = self.users_repository.read(email)
        
        if not user:
            status_code, content = HTTP_404_NOT_FOUND, {"content": f"User not found!"}

        else:
            read_user_dto = {
                'role_id': user.role_id,
                'name': user.name,
                'id': user.id,
                'email': user.email,
                'created_at': user.created_at,
                'updated_at': user.updated_at,
                'claims': [
                    ReadClaimDTO(
                        id=claim.id,
                        description=claim.description,
                        active=claim.active,
                    )
                    for claim in user.claims
                ]
            }
            
            status_code, content = HTTP_200_OK, {"content": ReadUserDTO(**read_user_dto)}
        
        return status_code, content
