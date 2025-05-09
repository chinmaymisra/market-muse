from typing import List, Optional
from pydantic import BaseModel

class Stock(BaseModel):
    """
    Pydantic schema for a stock item returned to the frontend.
    Mirrors the structure of the StockCache model.
    """
    symbol: str                              # Unique stock ticker (e.g. AAPL)
    full_name: Optional[str]                 # Full company name
    name: Optional[str]                      # Display label or short name
    exchange: Optional[str]                  # Exchange code (e.g. NASDAQ)
    price: float                             # Current price
    change: Optional[float]                  # Price change (absolute)
    percent_change: Optional[float]          # Price change (percent)
    volume: Optional[int]                    # Shares traded
    pe_ratio: Optional[float]                # Price-to-Earnings ratio
    market_cap: Optional[float]              # Market capitalization
    high_52w: Optional[float]                # 52-week high
    low_52w: Optional[float]                 # 52-week low
    history: List[float]                     # Historical price list (used in chart)

    class Config:
        orm_mode = True  # Allows conversion from ORM model to schema using `.from_orm()`
