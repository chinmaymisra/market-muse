from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from typing import List
from app.database import SessionLocal
from app.services.stock_service import get_stock_data
from app.schemas.stock import Stock 
from app.models.stock_cache import StockCache

router = APIRouter()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.get("/stocks", response_model=List[Stock])
def fetch_stocks(db: Session = Depends(get_db)):
    symbols = [
        "AAPL", "MSFT", "GOOG", "TSLA", "AMZN", "META", "NVDA", "NFLX"
    ]
    return get_stock_data(symbols, db)




    # symbols = [
    #     "AAPL", "MSFT", "GOOG", "TSLA", "AMZN", "META", "NVDA", "NFLX", "BRK-B",
    #     "JPM", "UNH", "V", "MA", "PEP", "KO", "DIS", "CSCO", "INTC", "ADBE", "ORCL"
    # ]