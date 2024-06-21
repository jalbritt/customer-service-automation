from utils.database import ConnectPostgres
from services.issue_service import IssueService
from FastAPI import APIRouter


class IssueRouter():
    def __init__(self):
        self.db = ConnectPostgres()

    router = APIRouter()

    @router.post("/issues")
    def create_issue(self, issue):
        return IssueService.create_issue(self.db, issue)

    @router.get("/issues")
    def get_issues(self):
        return IssueService.get_issues(self.db)

    @router.get("/issues/{issue_id}")
    def get_issue(self, issue_id):
        return IssueService.get_issue(self.db, issue_id)

    @router.put("/issues/{issue_id}")
    def update_issue(self, issue_id, issue):
        return IssueService.update_issue(self.db, issue_id, issue)

    @router.delete("/issues/{issue_id}")
    def delete_issue(self, issue_id):
        return IssueService.delete_issue(self.db, issue_id)
