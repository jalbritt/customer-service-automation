from models.issue import Issue


class IssueService:
    def create_issue(db, issue):
        db.conn.add(issue)
        db.conn.commit()
        return issue

    def get_issue(db, issue_id):
        return db.conn.query(Issue).filter(Issue.id == issue_id).first()

    def get_issues(db):
        return db.conn.query(Issue).all()

    def update_issue(db, issue_id, issue):
        db.conn.query(Issue).filter(Issue.id == issue_id).update(issue)
        db.conn.commit()
        return db.conn.query(Issue).filter(Issue.id == issue_id).first()

    def delete_issue(db, issue_id):
        db.conn.query(Issue).filter(Issue.id == issue_id).delete()
        db.conn.commit()
        return issue_id
