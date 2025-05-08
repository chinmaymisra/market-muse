from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.database import get_db
from app.models.stock_cache import StockCache

router = APIRouter(prefix="/stocks", tags=["Stocks"])

@router.get("/")
def get_all_cached_stocks(db: Session = Depends(get_db)):
    stocks = db.query(StockCache).all()
    for stock in stocks:
        stock.history = [float(x) for x in stock.history.split(",")] if stock.history else []
    return stocks
