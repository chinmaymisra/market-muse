import time
from sqlalchemy.orm import Session
from app.database import SessionLocal
from app.services.stock_service import get_stock_data

# List of stock symbols to rotate and refresh from Finnhub
STOCK_SYMBOLS = [
    "AAPL", "MSFT", "GOOG", "TSLA", "AMZN", "META", "NVDA", "NFLX",
    "BRK-B", "JPM", "UNH", "V", "MA", "PEP", "KO", "DIS",
    "CSCO", "INTC", "ADBE", "ORCL"
]

def main():
    """
    Periodically refreshes one stock per minute from the STOCK_SYMBOLS list,
    cycling through all of them in order using a round-robin strategy.
    """
    db: Session = SessionLocal()
    i = 0

    while True:
        # Cycle through the stock list using modulo
        symbol = STOCK_SYMBOLS[i % len(STOCK_SYMBOLS)]
        print(f"🔄 Refreshing {symbol}...")

        try:
            # Fetch and update data for a single stock
            get_stock_data([symbol], db)
        except Exception as e:
            print(f"❌ Error refreshing {symbol}: {e}")

        # Wait 60 seconds to respect API rate limits
        time.sleep(60)
        i += 1

if __name__ == "__main__":
    main()
