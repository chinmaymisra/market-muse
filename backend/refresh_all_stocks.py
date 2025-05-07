# refresh_all_stocks.py

from app.services.finnhub_service import get_stock_info
from app.database import SessionLocal
from app.models.stock_cache import StockCache

# SYMBOLS = [
#     "AAPL", "MSFT", "GOOG", "TSLA", "AMZN", "META", "NVDA", "NFLX", "BRK-B", "JPM",
#     "UNH", "V", "MA", "PEP", "KO", "DIS", "CSCO", "INTC", "ADBE", "ORCL"
# ]

SYMBOLS = [
    "PEP"
]

def main():
    db = SessionLocal()

    for symbol in SYMBOLS:
        print(f"🔄 Refreshing {symbol}...")
        info = get_stock_info(symbol)
        if not info:
            print(f"⚠️ Skipped {symbol}")
            continue

        history_str = ",".join(str(x) for x in info.get("history", []))

        existing = db.query(StockCache).filter_by(symbol=symbol).first()
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
            existing.high_52w = info["high_52w"]
            existing.low_52w = info["low_52w"]
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
                high_52w=info.get("high_52w"),
                low_52w=info.get("low_52w"),
                history=history_str
            )
            db.add(stock)

    db.commit()
    db.close()
    print("✅ Done refreshing all stocks.")


if __name__ == "__main__":
    main()
