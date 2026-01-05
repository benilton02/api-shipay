"""DTO para criação de usuário"""

from typing import Optional
from pydantic import BaseModel, EmailStr, Field
from uuid import uuid4


class CreateUserDTO(BaseModel):
    """DTO para criação de usuário"""
    
    name: str
    email: EmailStr
    role_id: int = Field(..., ge=1)
    password: Optional[str] = uuid4().hex[:10]

