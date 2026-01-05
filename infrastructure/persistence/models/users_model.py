from sqlalchemy import (
    Column,
    Integer,
    Integer,
    String,
    ForeignKey,
    DateTime,
    func
)
from sqlalchemy.orm import relationship

from .db_base import Base


class Users(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String, nullable=False)
    email = Column(String, nullable=False)
    password = Column(String, nullable=False)
    role_id = Column(Integer, ForeignKey("roles.id"), nullable=False)

    created_at = Column(
        DateTime(timezone=True),
        nullable=False,
        server_default=func.now()
    )

    updated_at = Column(
        DateTime(timezone=True),
        nullable=True,
        onupdate=func.now()
    )

    # relationships
    role = relationship("Roles", back_populates="users")

    claims = relationship(
        "Claims",
        secondary="user_claims",
        back_populates="users",
    )
