from sqlalchemy import Column, String, Float, Integer
from app.database import Base

class StockCache(Base):
    __tablename__ = "stock_cache"

    symbol = Column(String, primary_key=True, index=True)
    full_name = Column(String)
    name = Column(String)  # NEW
    exchange = Column(String)  # NEW
    price = Column(Float)
    change = Column(Float)  # NEW
    percent_change = Column(Float)  # NEW
    volume = Column(Integer)
    history = Column(String)  # NEW: store as comma-separated numbers
