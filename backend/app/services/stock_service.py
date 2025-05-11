from typing import List
from sqlalchemy.orm import Session
from app.services.finnhub_service import get_stock_info
from app.models.stock_cache import StockCache

def sanitize_history_list(raw_history):
    """
    Ensures history is a clean list of floats.
    Strips out any malformed braces or non-numeric entries.
    """
    clean = []

    if isinstance(raw_history, str):
        raw_history = raw_history.strip("{}").split(",")
    elif isinstance(raw_history, list):
        raw_history = [str(x) for x in raw_history]
    else:
        return clean

    for point in raw_history:
        try:
            point = point.strip().replace("{", "").replace("}", "")
            clean.append(float(point))
        except (ValueError, TypeError):
            continue

    return clean


def get_stock_data(symbols: List[str], db: Session) -> List[StockCache]:
    """
    Fetches live stock data for a list of symbols from Finnhub,
    updates or inserts them into the local database, and returns
    the entire stock cache.

    Args:
        symbols (List[str]): List of stock ticker symbols (e.g., ["AAPL", "TSLA"]).
        db (Session): SQLAlchemy DB session.

    Returns:
        List[StockCache]: Updated list of all cached stock entries.
    """
    results = []

    for symbol in symbols:
        try:
            # Get enriched stock data from Finnhub
            info = get_stock_info(symbol)

            if info:
                # Sanitize and convert history to CSV string
                raw_history = info.get("history", [])
                clean_history = sanitize_history_list(raw_history)
                history_str = ",".join(str(p) for p in clean_history)

                # Final brace cleaner to guarantee safe storage
                history_str = history_str.replace("{", "").replace("}", "")

                # Check if symbol already exists in the cache
                existing = db.query(StockCache).filter_by(symbol=symbol).first()

                if existing:
                    # Update only if new values are present
                    existing.full_name = info["full_name"] or existing.full_name
                    existing.name = info["name"] or existing.name
                    existing.exchange = info["exchange"] or existing.exchange
                    existing.price = info["price"] or existing.price
                    existing.change = info["change"] if info["change"] is not None else existing.change
                    existing.percent_change = info["percent_change"] if info["percent_change"] is not None else existing.percent_change
                    existing.volume = info["volume"] or existing.volume
                    existing.pe_ratio = info["pe_ratio"] or existing.pe_ratio
                    existing.market_cap = info["market_cap"] or existing.market_cap
                    existing.high_52w = info["high_52w"] or existing.high_52w
                    existing.low_52w = info["low_52w"] or existing.low_52w
                    existing.history = history_str if "history" in info else existing.history
                else:
                    # New stock — add to cache
                    stock = StockCache(
                        symbol=info["symbol"],
                        full_name=info["full_name"],
                        name=info.get("name"),
                        exchange=info.get("exchange"),
                        price=info["price"],
                        change=info.get("change"),
                        percent_change=info.get("percent_change"),
                        volume=info.get("volume"),
                        pe_ratio=info.get("pe_ratio"),
                        market_cap=info.get("market_cap"),
                        high_52w=info.get("high_52w"),
                        low_52w=info.get("low_52w"),
                        history=history_str
                    )
                    db.add(stock)
                    results.append(stock)

        except Exception as e:
            print(f"[ERROR] Finnhub fetch failed for {symbol}: {e}")

    # Commit all insertions/updates to the database
    db.commit()

    # Fetch and format all entries with parsed history for return
    final = db.query(StockCache).all()
    for stock in final:
        stock.history = sanitize_history_list(stock.history)

    return final
