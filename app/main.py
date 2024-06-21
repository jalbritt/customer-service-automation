from fastapi import FastAPI
from routers.issue_router import IssueRouter


app = FastAPI()
app.include_router(IssueRouter, prefix="/issues", tags=["issues"])
