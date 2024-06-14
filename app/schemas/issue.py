from pydantic import BaseModel
from datetime import datetime
from typing import Optional


class IssueBase(BaseModel):
    description: str
    priority: Optional[str] = "medium"
    category: Optional[str] = "general"
    customer_id: int


class IssueCreate(IssueBase):
    pass


class IssueUpdate(BaseModel):
    status: Optional[str]
    priority: Optional[str]
    category: Optional[str]
    assigned_to: Optional[int]


class IssueResponse(IssueBase):
    id: int
    status: str
    created_at: datetime
    updated_at: datetime
    resolved_at: Optional[datetime]
    assigned_to: Optional[int]

    class Config:
        orm_mode = True
