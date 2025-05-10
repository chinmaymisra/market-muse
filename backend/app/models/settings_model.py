from sqlalchemy import Column, String
from app.database import Base

class Setting(Base):
    """
    A simple key-value store for application settings.
    Used to persist values like last_index across script runs.
    """
    __tablename__ = "settings"

    key = Column(String, primary_key=True, index=True)
    value = Column(String, nullable=False)
