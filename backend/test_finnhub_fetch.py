# test_finnhub_fetch.py

from app.services.finnhub_service import get_stock_info

if __name__ == "__main__":
    # Symbol to test live Finnhub fetch for
    symbol = "AAPL"

    # Call the function that fetches and enriches stock data
    result = get_stock_info(symbol)

    # Print the result to console
    print("🔍 Result for", symbol)
    print(result)
