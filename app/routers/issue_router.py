from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from collections import List
from uuid import UUID
from app.utils.database import get_db
from app.schemas.issue import IssueCreate, IssueResponse, IssueUpdate
from app.services.issue_service import create_issue, get_issue, update_issue, \
     get_issues_for_user

router = APIRouter()


@router.post("/issues/", response_model=IssueResponse)
def create_new_issue(issue: IssueCreate, db: Session = Depends(get_db)):
    return create_issue(db, issue)


@router.get("/issues/{issue_id}", response_model=IssueResponse)
def read_issue(issue_id: UUID, db: Session = Depends(get_db)):
    db_issue = get_issue(db, issue_id)
    if not db_issue:
        raise HTTPException(status_code=404, detail="Issue not found")
    return db_issue


@router.put("/issues/{issue_id}", response_model=IssueResponse)
def update_existing_issue(issue_id: UUID, issue: IssueUpdate,
                          db: Session = Depends(get_db)):
    db_issue = update_issue(db, issue_id, issue)
    if not db_issue:
        raise HTTPException(status_code=404, detail="Issue not found")
    return db_issue


@router.get("/users/{user_id}/issues/", response_model=List[IssueResponse])
def read_issues_for_user(user_id: UUID, db: Session = Depends(get_db)):
    issues = get_issues_for_user(db, user_id)
    if not issues:
        raise HTTPException(status_code=404,
                            detail="No issues found for this user")
    return issues
