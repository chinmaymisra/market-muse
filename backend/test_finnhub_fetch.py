# test_finnhub_fetch.py
from app.services.finnhub_service import get_stock_info

if __name__ == "__main__":
    symbol = "AAPL"
    result = get_stock_info(symbol)
    print("🔍 Result for", symbol)
    print(result)
