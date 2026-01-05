from sqlalchemy import Column, ForeignKey, UniqueConstraint, Integer

from .db_base import Base


class UserClaims(Base):
    __tablename__ = "user_claims"

    user_id = Column(Integer, ForeignKey("users.id"), primary_key=True)
    claim_id = Column(Integer, ForeignKey("claims.id"), primary_key=True)

    __table_args__ = (
        UniqueConstraint("user_id", "claim_id", name="user_claims_un"),
    )
