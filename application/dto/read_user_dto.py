from pydantic import BaseModel
from datetime import datetime
from typing import Optional, List

class ReadClaimDTO(BaseModel):
    id: int
    description: str
    active: bool

class ReadUserDTO(BaseModel):
    id: int
    name: str
    email: str
    role_id: int
    created_at: datetime
    updated_at: Optional[datetime]
    claims: List[ReadClaimDTO]
    
    class Config:
        json_encoders = {
            datetime: lambda v: v.isoformat()
        }