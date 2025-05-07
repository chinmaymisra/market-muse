from sqlalchemy import Column, String, Float, Integer, DateTime
from datetime import datetime
from app.database import Base

class StockCache(Base):
    __tablename__ = "stock_cache"

    symbol = Column(String, primary_key=True, index=True)
    full_name = Column(String)
    name = Column(String)
    exchange = Column(String)
    price = Column(Float)
    change = Column(Float)
    percent_change = Column(Float)
    volume = Column(Integer)
    history = Column(String)  # comma-separated string
    last_updated = Column(DateTime, default=datetime.utcnow)
