from sqlalchemy import Column, String, Float, Integer
from app.database import Base

class StockCache(Base):
    """
    SQLAlchemy model for the 'stock_cache' table.
    Stores enriched and cached stock data fetched from the Finnhub API.
    """
    __tablename__ = "stock_cache"

    # Unique stock symbol (e.g., AAPL, TCS)
    symbol = Column(String, primary_key=True, index=True)

    # Full company name (e.g., Apple Inc.)
    full_name = Column(String, nullable=True)

    # Short name or ticker label
    name = Column(String, nullable=True)

    # Exchange name (e.g., NASDAQ, NSE)
    exchange = Column(String, nullable=True)

    # Current price
    price = Column(Float, nullable=False)

    # Absolute change in price (e.g., +1.23)
    change = Column(Float, nullable=True)

    # Percentage change (e.g., +2.34%)
    percent_change = Column(Float, nullable=True)

    # Volume of shares traded
    volume = Column(Integer, nullable=True)

    # Price-to-Earnings ratio
    pe_ratio = Column(Float, nullable=True)

    # Market capitalization
    market_cap = Column(Float, nullable=True)

    # 52-week high
    high_52w = Column(Float, nullable=True)

    # 52-week low
    low_52w = Column(Float, nullable=True)

    # Historical data stored as comma-separated string (e.g., prices or timestamps)
    history = Column(String, nullable=True)
