# app/models/user.py

from sqlalchemy import Column, String, Boolean
from app.database import Base

class User(Base):
    __tablename__ = "users"

    uid = Column(String, primary_key=True, index=True)
    email = Column(String, unique=True, index=True)
    name = Column(String)
    picture = Column(String)
    is_admin = Column(Boolean, default=False)  # NEW: admin flag
