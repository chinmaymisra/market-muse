from pydantic import BaseModel
from typing import Optional, List

class Stock(BaseModel):
    symbol: str
    full_name: str
    name: Optional[str]
    exchange: Optional[str]
    price: float
    change: Optional[float]
    percent_change: Optional[float]
    volume: int
    history: Optional[List[float]]

    class Config:
        orm_mode = True
