from sqlalchemy import Column, String, Float, Integer
from app.database import Base

class StockCache(Base):
    __tablename__ = "stock_cache"

    symbol = Column(String, primary_key=True, index=True)
    full_name = Column(String, nullable=True)
    name = Column(String, nullable=True)
    exchange = Column(String, nullable=True)
    price = Column(Float, nullable=False)
    change = Column(Float, nullable=True)
    percent_change = Column(Float, nullable=True)
    volume = Column(Integer, nullable=True)
    pe_ratio = Column(Float, nullable=True)
    market_cap = Column(Float, nullable=True)
    high_52w = Column(Float, nullable=True)
    low_52w = Column(Float, nullable=True)
    history = Column(String, nullable=True)  # stored as CSV
