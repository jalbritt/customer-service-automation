from sqlalchemy import Column, Integer, String, DateTime
from app.utils.database import Base
from datetime import datetime


class Issue(Base):
    __tablename__ = "issues"

    id = Column(Integer, primary_key=True, index=True)
    description = Column(String, index=True)
    status = Column(String, default="open")
    priority = Column(String, default="medium")
    category = Column(String, default="general")
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow,
                        onupdate=datetime.utcnow)
    resolved_at = Column(DateTime, nullable=True)
    customer_id = Column(Integer, index=True)
    assigned_to = Column(Integer, nullable=True)

    def __repr__(self):
        return f"<Issue(id={self.id}, status={self.status}, \
                        priority={self.priority}, category={self.category})>"
