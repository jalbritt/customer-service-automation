from sqlalchemy.orm import Session
from app.models.issue import Issue
from app.schemas.issue import IssueCreate, IssueUpdate
from datetime import datetime


def create_issue(db: Session, issue: IssueCreate):
    db_issue = Issue(**issue.dict(), created_at=datetime.utcnow(),
                     updated_at=datetime.utcnow())
    db.add(db_issue)
    db.commit()
    db.refresh(db_issue)
    return db_issue


def get_issues(db: Session, skip: int = 0, limit: int = 10):
    return db.query(Issue).offset(skip).limit(limit).all()


def get_issue(db: Session, issue_id: int):
    return db.query(Issue).filter(Issue.id == issue_id).first()


def update_issue(db: Session, issue_id: int, issue_update: IssueUpdate):
    db_issue = db.query(Issue).filter(Issue.id == issue_id).first()
    if db_issue:
        for key, value in issue_update.dict(exclude_unset=True).items():
            setattr(db_issue, key, value)
        db_issue.updated_at = datetime.utcnow()
        db.commit()
        db.refresh(db_issue)
    return db_issue


def delete_issue(db: Session, issue_id: int):
    db_issue = db.query(Issue).filter(Issue.id == issue_id).first()
    if db_issue:
        db.delete(db_issue)
        db.commit()
    return db_issue
