from pydantic import BaseModel
from typing import List,Optional

class Stock(BaseModel):
    symbol: str
    name: str
    full_name: Optional[str] = None
    exchange: Optional[str] = None
    price: float
    change: float
    percent_change: float
    history: List[float]

