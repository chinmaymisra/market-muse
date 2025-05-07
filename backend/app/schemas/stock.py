from typing import List, Optional
from pydantic import BaseModel

class Stock(BaseModel):
    symbol: str
    full_name: Optional[str]
    name: Optional[str]
    exchange: Optional[str]
    price: float
    change: Optional[float]
    percent_change: Optional[float]
    volume: Optional[int]
    pe_ratio: Optional[float]
    market_cap: Optional[float]
    high_52w: Optional[float]
    low_52w: Optional[float]
    history: List[float]

    class Config:
        orm_mode = True
