from sqlalchemy import Column, String, DateTime, Integer, func
from app.database import Base

class RefreshLog(Base):
    """
    Table to log stock refresh events.
    Stores the symbol, timestamp, and optional status string.
    Automatically trimmed to latest 10 rows via logic in refresh script.
    """
    __tablename__ = "refresh_log"

    id = Column(Integer, primary_key=True, index=True)
    symbol = Column(String, nullable=False)
    refreshed_at = Column(DateTime(timezone=True), server_default=func.now())
    status = Column(String, nullable=True)
