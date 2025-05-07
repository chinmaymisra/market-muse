from typing import List
from sqlalchemy.orm import Session
from datetime import datetime, timedelta
from fastapi.concurrency import run_in_threadpool

from app.models.stock_cache import StockCache
from app.services.finnhub_service import get_stock_info


def get_stock_data(symbols: List[str], db: Session) -> List[StockCache]:
    now = datetime.utcnow()
    cache = db.query(StockCache).all()

    # Serve cache immediately
    for stock in cache:
        if isinstance(stock.history, str):
            stock.history = [float(x) for x in stock.history.split(",") if x]
    symbols_in_cache = {s.symbol for s in cache}
    symbols_to_fetch = [s for s in symbols if s not in symbols_in_cache]

    # Always trigger async background fetch (do NOT block user)
    if True:
        import threading
        threading.Thread(target=refresh_stocks_if_stale, args=(symbols,)).start()

    return cache


def refresh_stocks_if_stale(symbols: List[str]):
    from app.database import SessionLocal
    db = SessionLocal()

    try:
        now = datetime.utcnow()
        last_updated = db.query(StockCache).order_by(StockCache.last_updated.asc()).first()
        if last_updated and (now - last_updated.last_updated) < timedelta(hours=12):
            print("🕒 Cache still fresh, skipping fetch")
            return

        print("🔄 Fetching fresh stock data from Finnhub")
        db.query(StockCache).delete()

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
                        history=",".join(str(x) for x in info.get("history", [])),
                        last_updated=now
                    )
                    db.add(stock)
            except Exception as e:
                print(f"[ERROR] Finnhub fetch failed for {symbol}: {e}")

        db.commit()
        print("✅ Stock cache updated")
    finally:
        db.close()
