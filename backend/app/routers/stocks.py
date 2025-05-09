from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.database import get_db
from app.models.stock_cache import StockCache

# Create API router with tag and prefix for all stock-related routes
router = APIRouter(prefix="/stocks", tags=["Stocks"])

@router.get("/")
def get_all_cached_stocks(db: Session = Depends(get_db)):
    """
    Fetch all cached stock data from the database.

    Args:
        db (Session): SQLAlchemy session provided by FastAPI.

    Returns:
        List[dict]: List of stocks with enriched information.
    """
    # Query all stock entries from the stock_cache table
    stocks = db.query(StockCache).all()

    # Parse CSV string in `history` into float list
    for stock in stocks:
        stock.history = [float(x) for x in stock.history.split(",")] if stock.history else []

    return stocks
