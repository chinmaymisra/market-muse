from typing import List
from sqlalchemy.orm import Session
from app.services.finnhub_service import get_stock_info
from app.models.stock_cache import StockCache

def get_stock_data(symbols: List[str], db: Session) -> List[StockCache]:
    results = []

    for symbol in symbols:
        try:
            info = get_stock_info(symbol)
            if info:
                existing = db.query(StockCache).filter_by(symbol=symbol).first()
                history_str = ",".join(str(x) for x in info.get("history", []))

                if existing:
                    existing.full_name = info["full_name"]
                    existing.name = info["name"]
                    existing.exchange = info["exchange"]
                    existing.price = info["price"]
                    existing.change = info["change"]
                    existing.percent_change = info["percent_change"]
                    existing.volume = info["volume"]
                    existing.pe_ratio = info["pe_ratio"]
                    existing.market_cap = info["market_cap"]
                    existing.high_52w = info["52w_high"]
                    existing.low_52w = info["52w_low"]
                    existing.history = history_str
                else:
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
                        high_52w=info.get("52w_high"),
                        low_52w=info.get("52w_low"),
                        history=history_str
                    )
                    db.add(stock)
                    results.append(stock)

        except Exception as e:
            print(f"[ERROR] Finnhub fetch failed for {symbol}: {e}")

    db.commit()

    final = db.query(StockCache).all()

    for stock in final:
        stock.history = [float(x) for x in stock.history.split(",")] if stock.history else []

    return final
