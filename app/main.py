# main.py
from fastapi import FastAPI
from app.utils.database import engine, Base
from app.routers import issue_router

# Create tables
Base.metadata.create_all(bind=engine)

app = FastAPI()

app.include_router(issue_router.router, prefix="/api/v1")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
