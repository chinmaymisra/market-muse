from sqlalchemy import Column, String, Boolean
from app.database import Base

class User(Base):
    """
    SQLAlchemy model for the 'users' table.
    Represents an authenticated user from Firebase.
    """
    __tablename__ = "users"

    # Firebase UID used as primary key
    uid = Column(String, primary_key=True, index=True)

    # User's email address (must be unique)
    email = Column(String, unique=True, index=True)

    # User's display name
    name = Column(String)

    # URL to user's profile picture
    picture = Column(String)

    # Flag for admin-level privileges (used in require_admin dependency)
    is_admin = Column(Boolean, default=False)  
