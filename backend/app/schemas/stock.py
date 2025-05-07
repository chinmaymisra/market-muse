from pydantic import BaseModel

class Stock(BaseModel):
    symbol: str
    full_name: str
    price: float
    change_percent: float
    volume: int

    class Config:
        orm_mode = True
