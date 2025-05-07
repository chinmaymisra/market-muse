
import time
from sqlalchemy.orm import Session
from app.database import SessionLocal
from app.services.stock_service import get_stock_data

# Update this list as needed
STOCK_SYMBOLS = [
    "AAPL", "MSFT", "GOOG", "TSLA", "AMZN", "META", "NVDA", "NFLX",
    "BRK-B", "JPM", "UNH", "V", "MA", "PEP", "KO", "DIS",
    "CSCO", "INTC", "ADBE", "ORCL"
]

def main():
    db: Session = SessionLocal()
    i = 0
    while True:
        symbol = STOCK_SYMBOLS[i % len(STOCK_SYMBOLS)]
        print(f"🔄 Refreshing {symbol}...")
        try:
            get_stock_data([symbol], db)
        except Exception as e:
            print(f"❌ Error refreshing {symbol}: {e}")
        time.sleep(60)  # Wait 1 minute before refreshing the next stock
        i += 1

if __name__ == "__main__":
    main()
