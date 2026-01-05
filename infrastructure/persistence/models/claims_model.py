from sqlalchemy import Column, Integer, String, Boolean
from sqlalchemy.orm import relationship

from .db_base import Base


class Claims(Base):
    __tablename__ = "claims"

    id = Column(Integer, primary_key=True, autoincrement=True)
    description = Column(String, nullable=False)
    active = Column(Boolean, nullable=False, default=True)

    # relationships
    users = relationship(
        "Users",
        secondary="user_claims",
        back_populates="claims",
    )
