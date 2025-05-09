# app/routers/users.py
import os
from dotenv import load_dotenv
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.auth import get_current_user
from app.database import SessionLocal
from app.models.user import User as DBUser
from typing import Dict,Any

load_dotenv()

# Convert comma-separated list into a set
ADMIN_EMAILS = set(email.strip() for email in os.getenv("ADMIN_EMAILS", "").split(",") if email.strip())

router = APIRouter(prefix="/users", tags=["users"])

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.get("/me")
def read_me(user:Dict[str, Any] = Depends(get_current_user), db: Session = Depends(get_db)):
    """
    Returns the current authenticated user's profile.
    If the user doesn't exist in the database, it registers them.

    Args:
        user (dict): Decoded Firebase user dict via get_current_user().
        db (Session): SQLAlchemy DB session.

    Returns:
        dict: Public profile fields including UID, email, name, picture, and admin flag.
    """
    # Try to find the user in the local DB by their Firebase UID
    existing_user = db.query(DBUser).filter(DBUser.uid == user["uid"]).first()

    if not existing_user:
        # Auto-register the user on first login
        is_admin = user.get("email") in ADMIN_EMAILS
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

        # Return a dictionary (not ORM object) with selected fields
        return {
            "uid": new_user.uid,
            "email": new_user.email,
            "name": new_user.name,
            "picture": new_user.picture,
            "is_admin": new_user.is_admin,
        }

    # Return existing user details as a dictionary
    return {
        "uid": existing_user.uid,
        "email": existing_user.email,
        "name": existing_user.name,
        "picture": existing_user.picture,
        "is_admin": existing_user.is_admin,
    }
