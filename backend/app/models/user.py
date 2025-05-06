from sqlalchemy import Column, String
from app.database import Base

class User(Base):
    __tablename__ = "users"
    uid = Column(String, primary_key=True, index=True)  # Previously 'sub'
    email = Column(String, unique=True, index=True)
    name = Column(String)
    picture = Column(String)
