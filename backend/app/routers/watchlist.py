from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.database import get_db
from app.models.watchlist import Watchlist
from app.models.user import User
from app.models.stock_cache import StockCache
from app.auth import get_current_user

router = APIRouter(prefix="/watchlist", tags=["Watchlist"])

@router.post("/add/{symbol}")
def add_to_watchlist(symbol: str, db: Session = Depends(get_db), user: User = Depends(get_current_user)):
    # Ensure the stock exists in cache
    stock = db.query(StockCache).filter_by(symbol=symbol).first()
    if not stock:
        raise HTTPException(status_code=404, detail="Stock not found")

    # Check if it's already in watchlist
    exists = db.query(Watchlist).filter_by(user_id=user.uid, symbol=symbol).first()
    if exists:
        return {"message": "Already in watchlist"}

    entry = Watchlist(user_id=user.uid, symbol=symbol)
    db.add(entry)
    db.commit()
    return {"message": "Added to watchlist"}

@router.post("/remove/{symbol}")
def remove_from_watchlist(symbol: str, db: Session = Depends(get_db), user: User = Depends(get_current_user)):
    entry = db.query(Watchlist).filter_by(user_id=user.uid, symbol=symbol).first()
    if not entry:
        raise HTTPException(status_code=404, detail="Not in watchlist")

    db.delete(entry)
    db.commit()
    return {"message": "Removed from watchlist"}

@router.get("/")
def get_watchlist(db: Session = Depends(get_db), user: User = Depends(get_current_user)):
    symbols = db.query(Watchlist.symbol).filter_by(user_id=user.uid).all()
    symbols = [s[0] for s in symbols]

    stocks = db.query(StockCache).filter(StockCache.symbol.in_(symbols)).all()
    for stock in stocks:
        stock.history = [float(x) for x in stock.history.split(",")] if stock.history else []

    return stocks
