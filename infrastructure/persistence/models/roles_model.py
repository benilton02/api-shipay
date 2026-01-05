from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship

from .db_base import Base


class Roles(Base):
    __tablename__ = "roles"

    id = Column(Integer, primary_key=True, autoincrement=True)
    description = Column(String, nullable=False)

    # relationships
    users = relationship("Users", back_populates="role")
