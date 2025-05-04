from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.auth import get_current_user
from app.database import get_db
from app.base_models import User 

router = APIRouter(prefix="/users", tags=["users"])

@router.get("/me")
def read_me(
    user_data=Depends(get_current_user),
    db: Session = Depends(get_db)
):
    user = db.query(User).filter(User.sub == user_data["sub"]).first()

    if not user:
        user = User(
            sub=user_data["sub"],
            email=user_data["email"],
            name=user_data["name"],
            picture=user_data["picture"]
        )
        db.add(user)
        db.commit()
        db.refresh(user)

    return {
        "sub": user.sub,
        "email": user.email,
        "name": user.name,
        "picture": user.picture
    }
