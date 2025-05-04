from fastapi import APIRouter, Depends
from app.auth import get_current_user

router = APIRouter(prefix="/users", tags=["users"])

@router.get("/me")
def read_me(user=Depends(get_current_user)):
    return {
        "sub": user["sub"],
        "email": user["email"],
        "name": user["name"],
        "picture": user["picture"]
    }

