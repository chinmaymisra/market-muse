import os
from dotenv import load_dotenv
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from typing import Dict, Any

from app.auth import get_current_user
from app.database import SessionLocal
from app.models.user import User as DBUser
from app.schemas.user import UserProfile  # ✅ Import the response schema

# Load environment variables from .env
load_dotenv()

# ✅ Create a set of admin emails defined in .env (comma-separated)
ADMIN_EMAILS = set(
    email.strip()
    for email in os.getenv("ADMIN_EMAILS", "").split(",")
    if email.strip()
)

# Initialize the router
router = APIRouter(prefix="/users", tags=["users"])

def get_db():
    """
    Dependency to yield a DB session.
    Automatically handles teardown after request.
    """
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.get("/me", response_model=UserProfile)
def read_me(user: Dict[str, Any] = Depends(get_current_user), db: Session = Depends(get_db)):
    """
    Returns the current authenticated user's profile.
    Auto-registers new users if not found in the database.

    Args:
        user (dict): Decoded Firebase user dictionary.
        db (Session): SQLAlchemy session.

    Returns:
        UserProfile: User profile data in structured Pydantic format.
    """
    # Check if user already exists in DB
    existing_user = db.query(DBUser).filter(DBUser.uid == user["uid"]).first()

    if not existing_user:
        # Determine admin access based on email
        is_admin = user.get("email") in ADMIN_EMAILS

        # Create new user record
        new_user = DBUser(
            uid=user["uid"],
            email=user.get("email"),
            name=user.get("name"),
            picture=user.get("picture"),
            is_admin=is_admin,
        )
        db.add(new_user)
        db.commit()
        db.refresh(new_user)
        return new_user  # ✅ ORM object is auto-converted via orm_mode in UserProfile

    return existing_user  # ✅ Pydantic schema will serialize this automatically
