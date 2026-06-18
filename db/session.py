# Database Connection Manager
# Handles connecting to MySQL

from sqlalchemy import create_engine, text  #I'm creating table automatically using SQLAlchemy
from sqlalchemy.orm import sessionmaker, Session
from typing import Generator
from shared.config import settings
from shared.logger import logger


# Create Database Engine - actual MySQL connection
engine = create_engine(
    settings.database_url,
    pool_pre_ping=True,
    pool_recycle=300,
    echo=False
)

# Session Factory
SessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine
)


def get_db() -> Generator[Session, None, None]:
    """
    Get database session.
    Use this in every agent that needs DB access.
    Automatically closes session when done.
    """
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


def test_connection() -> bool:
    """Test if MySQL connection is working"""
    try:
        with engine.connect() as connection:
            connection.execute(text("SELECT 1"))
        logger.info("[DATABASE] MySQL connection successful")
        return True
    except Exception as e:
        logger.error(f"[DATABASE] Connection failed: {str(e)}")
        return False


def create_all_tables():
    """
    Creates all tables in MySQL.
    Safe to run multiple times - will not duplicate.
    """
    from db.base import Base
    import db.models
    Base.metadata.create_all(bind=engine)
    logger.info("[DATABASE] All tables created successfully")