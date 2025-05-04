import yfinance as yf
from typing import List, Dict

def get_stock_data(symbols: List[str]) -> List[Dict]:
    result = []
    for symbol in symbols:
        try:
            stock = yf.Ticker(symbol)
            hist = stock.history(period="5d")["Close"].tolist()[-10:]

            info = stock.info

            result.append({
                "symbol": symbol,
                "name": info.get("shortName", symbol),
                "full_name": info.get("longName") or info.get("shortName", symbol),
                "exchange": info.get("exchange", "Unknown"),
                "price": info.get("regularMarketPrice", 0),
                "change": info.get("regularMarketChange", 0),
                "percent_change": info.get("regularMarketChangePercent", 0),
                "history": hist,
            })
        except Exception as e:
            print(f"[ERROR] Failed to fetch {symbol}: {e}")
    return result
