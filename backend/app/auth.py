from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
import firebase_admin
from firebase_admin import auth as firebase_auth, credentials
import os
import json
from dotenv import load_dotenv

from sqlalchemy.orm import Session
from app.database import SessionLocal
from app.models.user import User as DBUser

load_dotenv()

#  Load credentials from environment variable
firebase_json = os.getenv("FIREBASE_CREDENTIALS_JSON")
if not firebase_json:
    raise RuntimeError("Missing FIREBASE_CREDENTIALS_JSON environment variable")

try:
    firebase_dict = json.loads(firebase_json)
    cred = credentials.Certificate(firebase_dict)
    firebase_admin.initialize_app(cred)
except Exception as e:
    raise RuntimeError(f"Failed to initialize Firebase Admin SDK: {e}")

http_bearer = HTTPBearer()

#  Verifies Firebase token sent from frontend
def verify_token(token: str):
    try:
        decoded_token = firebase_auth.verify_id_token(token)
        return {
            "uid": decoded_token.get("uid"),
            "email": decoded_token.get("email"),
            "name": decoded_token.get("name"),
            "picture": decoded_token.get("picture"),
        }
    except Exception as e:
        print(f"[Firebase] Token verification failed: {e}")
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid Firebase token")

def get_current_user(credentials: HTTPAuthorizationCredentials = Depends(http_bearer)):
    return verify_token(credentials.credentials)

#  For database session
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

#  Only allow admin users to proceed
def require_admin(user=Depends(get_current_user), db: Session = Depends(get_db)):
    db_user = db.query(DBUser).filter(DBUser.uid == user["uid"]).first()
    if not db_user or not db_user.is_admin:
        raise HTTPException(status_code=403, detail="Admin access required")
    return db_user
