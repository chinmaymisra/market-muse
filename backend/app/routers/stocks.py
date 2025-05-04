from fastapi import APIRouter
from typing import List
from app.services.stock_service import get_stock_data
from app.models.stocks import Stock

router = APIRouter()

@router.get("/stocks", response_model=List[Stock])
def fetch_stocks():
    symbols = [
        "AAPL", "MSFT", "GOOG", "TSLA", "AMZN", "META", "NVDA", "NFLX", "BRK-B",
        "JPM", "UNH", "V", "MA", "PEP", "KO", "DIS", "CSCO", "INTC", "ADBE", "ORCL"
    ]
    return get_stock_data(symbols)

