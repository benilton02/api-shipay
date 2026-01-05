from infrastructure.config.db_session import DatabaseSession
from infrastructure.persistence.models.users_model import Users
from application.dto.create_user_dto import CreateUserDTO
from sqlalchemy.orm import joinedload
from sqlalchemy.exc import SQLAlchemyError


class UsersRepository:
    """Repository para gerenciamento de usuários"""

    def create(self, user_dto: CreateUserDTO) -> Users:
        with DatabaseSession() as session:
            try:
                user = Users(
                    name=user_dto.name,
                    email=user_dto.email,
                    role_id=user_dto.role_id,
                    password=user_dto.password,
                )

                session.add(user)
                session.commit()
                return True
            
            except SQLAlchemyError as exc:
                session.rollback()
                return exc._message()

    def read(self, email: str) -> Users | None:
        with DatabaseSession() as session:
            return (
                session.query(Users)
                .options(joinedload(Users.claims))
                .filter(Users.email == email)
                .first()
            )

