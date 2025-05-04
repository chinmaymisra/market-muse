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

@router.get("/me")
def read_me(user=Depends(get_current_user), db: Session = Depends(get_db)):
    existing_user = db.query(DBUser).filter(DBUser.sub == user["sub"]).first()
    if not existing_user:
        new_user = DBUser(
            sub=user["sub"],
            email=user.get("email"),
            name=user.get("name"),
            picture=user.get("picture"),
        )
        db.add(new_user)
        db.commit()

    return {
        "sub": user["sub"],
        "email": user["email"],
        "name": user["name"],
        "picture": user["picture"],
    }
