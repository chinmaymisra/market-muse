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

# Load environment variables from .env file
load_dotenv()

# Retrieve Firebase credentials from environment
firebase_json = os.getenv("FIREBASE_CREDENTIALS_JSON")
firebase_file = os.getenv("FIREBASE_CREDENTIALS_FILE", "./firebase-service-account.json")

# Initialize Firebase only once
if not firebase_admin._apps:
    try:
        if firebase_json and firebase_json.strip():
            # Render-style: JSON provided directly in env variable
            firebase_dict = json.loads(firebase_json)
            cred = credentials.Certificate(firebase_dict)
        elif os.path.isfile(firebase_file):
             # Fallback: load from local service account JSON file
            cred = credentials.Certificate(firebase_file)
        else:
            raise RuntimeError("Missing Firebase credentials. Set FIREBASE_CREDENTIALS_JSON or FIREBASE_CREDENTIALS_FILE")

        firebase_admin.initialize_app(cred)
    except Exception as e:
        raise RuntimeError(f"Failed to initialize Firebase Admin SDK: {e}")

# Use HTTP Bearer Auth to expect token in "Authorization: Bearer <token>" header
http_bearer = HTTPBearer()


def get_db():
    """
    FastAPI dependency to get a SQLAlchemy DB session.
    Ensures proper session handling with yield.
    """
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

        

def verify_token(token: str):
    """
    Verifies a Firebase ID token and returns the decoded token payload.

    Args:
        token (str): Firebase JWT.

    Returns:
        dict: Decoded Firebase token payload.

    Raises:
        HTTPException: If token is invalid or expired.
    """
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
    """
    FastAPI dependency that verifies the Firebase JWT and returns the corresponding user from the DB.
    Creates a new user entry if it does not exist yet.

    Args:
        credentials (HTTPAuthorizationCredentials): The Bearer token passed in the Authorization header.
        db (Session): SQLAlchemy database session.

    Returns:
        DBUser: The user ORM object corresponding to the Firebase UID.
    """
    # Decode the token and retrieve Firebase user info
    firebase_user = verify_token(credentials.credentials)

    # Attempt to fetch the user from the local database
    db_user = db.query(DBUser).filter(DBUser.uid == firebase_user["uid"]).first()

    # If the user does not exist in DB, create a new record
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

    # Return the ORM user object
    return db_user



def require_admin(user=Depends(get_current_user), db: Session = Depends(get_db)):
    """
    FastAPI dependency that enforces admin-only access by checking user's is_admin flag.

    Args:
        user: The authenticated user (from Firebase token).
        db (Session): SQLAlchemy DB session.

    Returns:
        DBUser: The user instance if admin check passes.

    Raises:
        HTTPException: If the user is not marked as an admin.
    """
    # Retrieve the full DB user object using UID from the auth token
    db_user = db.query(DBUser).filter(DBUser.uid == user["uid"]).first()

    # If user doesn't exist or isn't marked as admin in DB, deny access
    if not db_user or not db_user.is_admin:
        raise HTTPException(status_code=403, detail="Admin access required")

    return db_user
