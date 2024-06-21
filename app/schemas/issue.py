# schemas/issue.py
from pydantic import BaseModel
from datetime import datetime
from typing import Optional


class IssueBase(BaseModel):
    title: str
    description: str
    status: str = "Open"


class IssueCreate(IssueBase):
    pass


class Issue(IssueBase):
    id: int
    created_at: datetime
    updated_at: Optional[datetime] = None

    class Config:
        orm_mode = True
