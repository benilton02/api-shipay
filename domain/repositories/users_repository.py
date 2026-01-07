from infrastructure.config.db_session import DatabaseSession
from infrastructure.persistence.models.users_model import Users
from application.dto.create_user_dto import CreateUserDTO
from sqlalchemy.orm import joinedload
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy import func


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

    def read(self, page: int, per_page: int, email: str) -> Users | None:
        with DatabaseSession() as session:
            query = session.query(Users).options(joinedload(Users.claims))

            if email:
                query = query.filter(Users.email == email)

            total = query.count()
            items = query.offset((page - 1) * per_page).limit(per_page).all()
            return items, total
