import os
import requests
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Finnhub API configuration
FINNHUB_API_KEY = os.getenv("FINNHUB_API_KEY")
BASE_URL = "https://finnhub.io/api/v1"

def get_stock_info(symbol: str):
    """
    Fetches real-time and fundamental stock data for a given symbol from Finnhub.

    Args:
        symbol (str): Ticker symbol of the stock (e.g., "AAPL").

    Returns:
        dict: A dictionary with enriched stock details for the frontend/API,
              or None if the fetch failed.
    """
    try:
        # Construct API endpoints for different data types
        quote_url = f"{BASE_URL}/quote"
        profile_url = f"{BASE_URL}/stock/profile2"
        metrics_url = f"{BASE_URL}/stock/metric"

        # Request live market quote
        quote_resp = requests.get(quote_url, params={"symbol": symbol, "token": FINNHUB_API_KEY})
        quote_data = quote_resp.json()

        # Request company profile info (name, exchange, etc.)
        profile_resp = requests.get(profile_url, params={"symbol": symbol, "token": FINNHUB_API_KEY})
        profile_data = profile_resp.json()

        # Attempt to fetch financial metrics (P/E, market cap, 52-week high/low)
        try:
            metrics_resp = requests.get(metrics_url, params={"symbol": symbol, "metric": "all", "token": FINNHUB_API_KEY})
            metrics_data = metrics_resp.json().get("metric", {})
        except Exception as me:
            print(f"[WARN] Metrics fetch failed for {symbol}: {me}")
            metrics_data = {}

        # Handle bad quote data fallback
        if not quote_data or "c" not in quote_data or quote_data.get("c") == 0:
            print(f"[WARN] Incomplete quote data for {symbol}. Proceeding with defaults. Raw: {quote_data}")
            quote_data = {"c": 0, "d": None, "dp": None, "v": 0}

        # Consolidate response dictionary
        return {
            "symbol": symbol,
            "full_name": profile_data.get("name", symbol),
            "name": profile_data.get("name"),
            "exchange": profile_data.get("exchange"),
            "price": quote_data.get("c", 0),
            "change": quote_data.get("d"),
            "percent_change": quote_data.get("dp"),
            "volume": quote_data.get("v", 0),
            "pe_ratio": metrics_data.get("peNormalizedAnnual"),
            "market_cap": metrics_data.get("marketCapitalization"),
            "high_52w": metrics_data.get("52WeekHigh"),
            "low_52w": metrics_data.get("52WeekLow"),
            "history": [  # Simulated history values for sparkline chart
                quote_data.get("c", 0) * 0.97,
                quote_data.get("c", 0) * 0.99,
                quote_data.get("c", 0) * 1.01,
                quote_data.get("c", 0)
            ]
        }

    except Exception as e:
        print(f"[ERROR] Finnhub fetch failed for {symbol}: {e}")
        return None
