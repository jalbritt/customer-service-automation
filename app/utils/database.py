import os
import logging
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, scoped_session
from sqlalchemy.exc import SQLAlchemyError

# Database configuration
DATABASE_URL = os.getenv("DATABASE_URL")

# Create a new SQLAlchemy engine
engine = create_engine(
    DATABASE_URL,
    pool_size=10,
    max_overflow=20,
    pool_timeout=30,
    pool_recycle=1800,
    echo=True  # Enable SQLAlchemy logging
)

# Create a configured "Session" class
SessionLocal = scoped_session(sessionmaker(autocommit=False,
                              autoflush=False, bind=engine))

# Create a Base class for declarative class definitions
Base = declarative_base()

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


# Dependency to get DB session
def get_db():
    db = SessionLocal()
    try:
        yield db
    except SQLAlchemyError as e:
        logger.error(f"Database error: {e}")
        db.rollback()
        raise
    finally:
        db.close()


# Create all tables
def init_db():
    try:
        Base.metadata.create_all(bind=engine)
        logger.info("Database tables created successfully.")
    except SQLAlchemyError as e:
        logger.error(f"Error creating database tables: {e}")
        raise


# Connect to the database
async def connect():
    try:
        engine.connect()
        logger.info("Database connection established.")
    except SQLAlchemyError as e:
        logger.error(f"Error connecting to the database: {e}")
        raise


# Disconnect from the database
async def disconnect():
    try:
        engine.dispose()
        logger.info("Database connection closed.")
    except SQLAlchemyError as e:
        logger.error(f"Error closing the database connection: {e}")
        raise
