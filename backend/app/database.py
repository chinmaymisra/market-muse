from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import os
from dotenv import load_dotenv

# Load environment variables from a .env file (if it exists)
load_dotenv()

# Get the DATABASE_URL from environment variables (e.g., PostgreSQL URI)
DATABASE_URL = os.getenv("DATABASE_URL")

# Create a SQLAlchemy engine using the database URL
engine = create_engine(DATABASE_URL)

# Create a configured session factory
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Base class for defining ORM models
Base = declarative_base()


def get_db():
    """
    FastAPI dependency that yields a SQLAlchemy DB session.
    Ensures that the session is properly closed after use.

    Yields:
        db (Session): A SQLAlchemy session instance.
    """
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
