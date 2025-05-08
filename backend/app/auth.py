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

# import pathlib
# print("📦 CURRENT WORKING DIR:", os.getcwd())
# print("📦 .env found at:", pathlib.Path(".env").absolute().exists())
# print("📦 FIREBASE_CREDENTIALS_FILE:", os.getenv("FIREBASE_CREDENTIALS_FILE"))
# print("📦 JSON file exists:", os.path.isfile(os.getenv("FIREBASE_CREDENTIALS_FILE") or ""))

firebase_json = os.getenv("FIREBASE_CREDENTIALS_JSON")
firebase_file = os.getenv("FIREBASE_CREDENTIALS_FILE", "./firebase-service-account.json")

# Initialize Firebase only once
if not firebase_admin._apps:
    try:
        if firebase_json and firebase_json.strip():
            # ✅ Render-style full JSON string
            firebase_dict = json.loads(firebase_json)
            cred = credentials.Certificate(firebase_dict)
        elif os.path.isfile(firebase_file):
            # ✅ Local dev file fallback
            cred = credentials.Certificate(firebase_file)
        else:
            raise RuntimeError("Missing Firebase credentials. Set FIREBASE_CREDENTIALS_JSON or FIREBASE_CREDENTIALS_FILE")

        firebase_admin.initialize_app(cred)
    except Exception as e:
        raise RuntimeError(f"Failed to initialize Firebase Admin SDK: {e}")

http_bearer = HTTPBearer()

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

def get_current_user(
    credentials: HTTPAuthorizationCredentials = Depends(http_bearer),
    db: Session = Depends(get_db),
) -> DBUser:
    firebase_user = verify_token(credentials.credentials)
    db_user = db.query(DBUser).filter(DBUser.uid == firebase_user["uid"]).first()

    # If user doesn't exist in DB, create and store them
    if not db_user:
        db_user = DBUser(
            uid=firebase_user["uid"],
            email=firebase_user["email"],
            name=firebase_user["name"],
            picture=firebase_user["picture"],
        )
        db.add(db_user)
        db.commit()
        db.refresh(db_user)

    return db_user


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

def require_admin(user=Depends(get_current_user), db: Session = Depends(get_db)):
    db_user = db.query(DBUser).filter(DBUser.uid == user["uid"]).first()
    if not db_user or not db_user.is_admin:
        raise HTTPException(status_code=403, detail="Admin access required")
    return db_user
