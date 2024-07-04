# services/issue_service.py
from sqlalchemy.orm import Session
from app.models.issue import Issue


class IssueService:
    @staticmethod
    def create_issue(db: Session, title: str, description: str):
        new_issue = Issue(title=title, description=description, status="Open")
        db.add(new_issue)
        db.commit()
        db.refresh(new_issue)
        return new_issue

    @staticmethod
    def get_issues(db: Session, skip: int = 0, limit: int = 100):
        return db.query(Issue).offset(skip).limit(limit).all()

    @staticmethod
    def get_issue(db: Session, issue_id: int):
        return db.query(Issue).filter(Issue.id == issue_id).first()

    @staticmethod
    def update_issue(
        db: Session, issue_id: int, title: str, description: str, status: str
    ):
        issue = db.query(Issue).filter(Issue.id == issue_id).first()
        if issue:
            issue.title = title
            issue.description = description
            issue.status = status
            db.commit()
            db.refresh(issue)
        return issue

    @staticmethod
    def delete_issue(db: Session, issue_id: int):
        issue = db.query(Issue).filter(Issue.id == issue_id).first()
        if issue:
            db.delete(issue)
            db.commit()
        return issue
