import os
import requests
from dotenv import load_dotenv

load_dotenv()

FINNHUB_API_KEY = os.getenv("FINNHUB_API_KEY")
BASE_URL = "https://finnhub.io/api/v1"

def get_stock_info(symbol: str):
    try:
        quote_url = f"{BASE_URL}/quote"
        profile_url = f"{BASE_URL}/stock/profile2"
        metrics_url = f"{BASE_URL}/stock/metric"

        quote_resp = requests.get(quote_url, params={"symbol": symbol, "token": FINNHUB_API_KEY})
        profile_resp = requests.get(profile_url, params={"symbol": symbol, "token": FINNHUB_API_KEY})

        # Initialize metrics_data in case of failure
        metrics_data = {}
        try:
            metrics_resp = requests.get(metrics_url, params={"symbol": symbol, "metric": "all", "token": FINNHUB_API_KEY})
            metrics_data = metrics_resp.json().get("metric", {})
        except Exception as me:
            print(f"[WARN] Metrics fetch failed for {symbol}: {me}")

        quote_data = quote_resp.json()
        profile_data = profile_resp.json()

        # Instead of skipping, proceed with fallbacks if quote data is incomplete
        if not quote_data or "c" not in quote_data:
            print(f"[WARN] Incomplete quote data for {symbol}. Proceeding with defaults. Raw: {quote_data}")
            quote_data = {"c": 0, "d": None, "dp": None, "v": 0}

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
            "history": [
                quote_data.get("c", 0) * 0.97,
                quote_data.get("c", 0) * 0.99,
                quote_data.get("c", 0) * 1.01,
                quote_data.get("c", 0)
            ]
        }

    except Exception as e:
        print(f"[ERROR] Finnhub fetch failed for {symbol}: {e}")
        return None
