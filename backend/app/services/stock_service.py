from typing import List
from sqlalchemy.orm import Session
from app.services.finnhub_service import get_stock_info
from app.models.stock_cache import StockCache

def get_stock_data(symbols: List[str], db: Session) -> List[StockCache]:
    # Clear previous cache
    db.query(StockCache).delete()

    results = []
    for symbol in symbols:
        try:
            info = get_stock_info(symbol)
            if info:
                stock = StockCache(
                    symbol=info["symbol"],
                    full_name=info["full_name"],
                    price=info["price"],
                    change_percent=info["change_percent"],
                    volume=info["volume"]
                )
                db.add(stock)
                results.append(stock)
        except Exception as e:
            print(f"[ERROR] Finnhub fetch failed for {symbol}: {e}")

    db.commit()
    return results
