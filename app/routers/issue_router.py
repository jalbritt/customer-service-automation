from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from utils.database import get_db
from services.issue_service import IssueService
from schemas.issue import Issue, IssueCreate
from prometheus_client import Counter, Histogram

router = APIRouter()

# Create metrics
ISSUES_CREATED = Counter("issues_created_total", "Total number of issues created")
ISSUE_CREATION_TIME = Histogram(
    "issue_creation_seconds", "Time spent creating an issue"
)


@router.post("/issues/", response_model=Issue)
def create_issue(issue: IssueCreate, db: Session = Depends(get_db)):
    with ISSUE_CREATION_TIME.time():
        new_issue = IssueService.create_issue(db, issue.title, issue.description)
    ISSUES_CREATED.inc()
    return new_issue


@router.post("/issues/", response_model=Issue)
def create_issue(issue: IssueCreate, db: Session = Depends(get_db)):
    return IssueService.create_issue(db, issue.title, issue.description)


@router.get("/issues/", response_model=List[Issue])
def read_issues(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    return IssueService.get_issues(db, skip, limit)


@router.get("/issues/{issue_id}", response_model=Issue)
def read_issue(issue_id: int, db: Session = Depends(get_db)):
    issue = IssueService.get_issue(db, issue_id)
    if issue is None:
        raise HTTPException(status_code=404, detail="Issue not found")
    return issue


@router.put("/issues/{issue_id}", response_model=Issue)
def update_issue(issue_id: int, issue: IssueCreate, db: Session = Depends(get_db)):
    updated_issue = IssueService.update_issue(
        db, issue_id, issue.title, issue.description, issue.status
    )
    if updated_issue is None:
        raise HTTPException(status_code=404, detail="Issue not found")
    return updated_issue


@router.delete("/issues/{issue_id}", response_model=Issue)
def delete_issue(issue_id: int, db: Session = Depends(get_db)):
    deleted_issue = IssueService.delete_issue(db, issue_id)
    if deleted_issue is None:
        raise HTTPException(status_code=404, detail="Issue not found")
    return deleted_issue
