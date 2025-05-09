from pydantic import BaseModel

class UserProfile(BaseModel):
    """
    Schema for user profile data returned by `/users/me`.

    Maps directly to the User ORM model and is serialized for frontend use.
    """
    uid: str                # Firebase UID (primary key)
    email: str              # User's email address
    name: str               # Display name from Firebase
    picture: str            # Profile picture URL
    is_admin: bool          # Whether the user has admin privileges

    class Config:
        orm_mode = True     # Allows usage with SQLAlchemy ORM objects
