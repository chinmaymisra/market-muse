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

        quote_resp = requests.get(quote_url, params={"symbol": symbol, "token": FINNHUB_API_KEY})
        profile_resp = requests.get(profile_url, params={"symbol": symbol, "token": FINNHUB_API_KEY})

        quote_data = quote_resp.json()
        profile_data = profile_resp.json()

        return {
            "symbol": symbol,
            "full_name": profile_data.get("name", symbol),
            "price": quote_data.get("c", 0),
            "change_percent": quote_data.get("dp", 0),
            "volume": quote_data.get("v", 0),
        }

    except Exception as e:
        print(f"[Finnhub] Failed for symbol {symbol}: {e}")
        return None
