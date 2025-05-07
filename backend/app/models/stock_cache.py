from sqlalchemy import Column, String, Float, Integer
from app.database import Base

class StockCache(Base):
    __tablename__ = "stock_cache"

    symbol = Column(String, primary_key=True, index=True)
    full_name = Column(String)
    price = Column(Float)
    change_percent = Column(Float)
    volume = Column(Integer)
