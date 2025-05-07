# app/routers/users.py

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.auth import get_current_user
from app.database import SessionLocal
from app.models.user import User as DBUser

router = APIRouter(prefix="/users", tags=["users"])

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

ADMIN_EMAILS = {"your@email.com", "admin@marketmuse.com"}  # CHANGE THIS

@router.get("/me")
def read_me(user=Depends(get_current_user), db: Session = Depends(get_db)):
    existing_user = db.query(DBUser).filter(DBUser.uid == user["uid"]).first()

    if not existing_user:
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
        return {
            "uid": new_user.uid,
            "email": new_user.email,
            "name": new_user.name,
            "picture": new_user.picture,
            "is_admin": new_user.is_admin,
        }

    return {
        "uid": existing_user.uid,
        "email": existing_user.email,
        "name": existing_user.name,
        "picture": existing_user.picture,
        "is_admin": existing_user.is_admin,
    }
