from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.database import get_db
from app.models.watchlist import Watchlist
from app.models.user import User
from app.models.stock_cache import StockCache
from app.auth import get_current_user
from app.schemas.watchlist import WatchlistItem 

# Initialize the API router for watchlist-related endpoints.
# All routes here will be prefixed with "/watchlist"
router = APIRouter(prefix="/watchlist", tags=["Watchlist"])


@router.post("/add/{symbol}")
def add_to_watchlist(
    symbol: str,
    db: Session = Depends(get_db),
    user: User = Depends(get_current_user)
):
    """
    Adds a stock to the current user's watchlist.

    Args:
        symbol (str): The stock symbol to add (e.g. 'AAPL').
        db (Session): SQLAlchemy session object (injected).
        user (User): Authenticated user from Firebase (injected).

    Returns:
        dict: Success or already-added message.

    Raises:
        HTTPException: If the stock symbol doesn't exist in cache.
    """
    # Check if stock exists in the stock_cache table
    stock = db.query(StockCache).filter_by(symbol=symbol).first()
    if not stock:
        raise HTTPException(status_code=404, detail="Stock not found")

    # Check if already present in watchlist
    exists = db.query(Watchlist).filter_by(user_id=user.uid, symbol=symbol).first()
    if exists:
        return {"message": "Already in watchlist"}

    # Create and add new watchlist entry
    entry = Watchlist(user_id=user.uid, symbol=symbol)
    db.add(entry)
    db.commit()
    db.refresh(entry)

    return {"message": f"Added {symbol} to watchlist"}


@router.post("/remove/{symbol}")
def remove_from_watchlist(
    symbol: str,
    db: Session = Depends(get_db),
    user: User = Depends(get_current_user)
):
    """
    Removes a stock from the current user's watchlist.

    Args:
        symbol (str): The stock symbol to remove.
        db (Session): SQLAlchemy session object.
        user (User): Authenticated user.

    Returns:
        dict: Confirmation message.

    Raises:
        HTTPException: If the stock is not in the user's watchlist.
    """
    entry = db.query(Watchlist).filter_by(user_id=user.uid, symbol=symbol).first()
    if not entry:
        raise HTTPException(status_code=404, detail="Stock not in watchlist")

    db.delete(entry)
    db.commit()

    return {"message": f"Removed {symbol} from watchlist"}


@router.get("/", response_model=list[WatchlistItem])
def get_watchlist(
    db: Session = Depends(get_db),
    user: User = Depends(get_current_user)
):
    """
    Retrieves the user's current watchlist symbols only.

    Args:
        db (Session): SQLAlchemy session object.
        user (User): Authenticated user.

    Returns:
        list[WatchlistItem]: List of symbols the user is watching.
    """
    # Fetch all watchlist entries for the user
    entries = db.query(Watchlist).filter_by(user_id=user.uid).all()
    return entries  # Will be serialized using WatchlistItem schema
