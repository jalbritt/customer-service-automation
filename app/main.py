from fastapi import FastAPI
from app.routers import issue, chat_message
import app.utils.database as db
import app.utils.message_queue as mq
from app.services.issue_service import process_message
from pybreaker import CircuitBreakerError
import logging

logger = logging.getLogger(__name__)

app = FastAPI()

app.include_router(issue.router)
app.include_router(chat_message.router)


@app.on_event("startup")
async def startup():
    await db.connect()
    db.init_db()
    try:
        mq.consume_messages(process_message)
    except CircuitBreakerError:
        logger.error("Message queue is temporarily unavailable.\
                      Circuit breaker is open.")


@app.on_event("shutdown")
async def shutdown():
    await db.disconnect()
