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
                    name=info.get("name"),
                    exchange=info.get("exchange"),
                    price=info["price"],
                    change=info.get("change"),
                    percent_change=info.get("percent_change"),
                    volume=info["volume"],
                    history=",".join(str(x) for x in info.get("history", []))
                )
                db.add(stock)
                results.append(stock)
        except Exception as e:
            print(f"[ERROR] Finnhub fetch failed for {symbol}: {e}")

    db.commit()

    # Convert history string back to list
    for stock in results:
        if stock.history:
            stock.history = [float(x) for x in stock.history.split(",")]

    return results
