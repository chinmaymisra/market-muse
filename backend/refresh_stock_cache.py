import time
from sqlalchemy.orm import Session
from sqlalchemy import select, delete, desc
from app.database import SessionLocal
from app.models.stock_cache import StockCache
from app.models.refresh_log_model import RefreshLog
from app.services.stock_service import get_stock_data

def get_symbols_from_db(db: Session):
    """
    Fetch all unique stock symbols from the stock_cache table.
    """
    results = db.execute(select(StockCache.symbol)).scalars().all()
    return results

def trim_refresh_log(db: Session, keep_last_n: int = 10):
    """
    Keep only the most recent N refresh_log entries.
    Deletes older rows to avoid memory bloat.
    """
    ids_to_keep = (
        db.query(RefreshLog.id)
        .order_by(desc(RefreshLog.refreshed_at))
        .limit(keep_last_n)
        .all()
    )
    if ids_to_keep:
        keep_ids = [r.id for r in ids_to_keep]
        db.query(RefreshLog).filter(~RefreshLog.id.in_(keep_ids)).delete(synchronize_session=False)
        db.commit()

def main():
    """
    Background worker that refreshes one stock per minute from the current DB symbol list.
    Applies update-safe logic and logs the refresh to a limited-size table.
    """
    db: Session = SessionLocal()
    i = 0

    while True:
        try:
            symbols = get_symbols_from_db(db)
            if not symbols:
                print("⚠️ No symbols found in stock_cache.")
                time.sleep(60)
                continue

            # Cycle through available stock symbols in round-robin
            symbol = symbols[i % len(symbols)]
            print(f"🔄 Refreshing {symbol}...")

            # Call your existing update logic
            get_stock_data([symbol], db)

            # Log to refresh_log
            log = RefreshLog(symbol=symbol, status="success")
            db.add(log)
            db.commit()

            # Trim log table to latest 10
            trim_refresh_log(db)

        except Exception as e:
            print(f"❌ Error refreshing {symbol}: {e}")
            try:
                db.rollback()
                db.add(RefreshLog(symbol=symbol, status=f"error: {e}"))
                db.commit()
                trim_refresh_log(db)
            except Exception as rollback_err:
                print(f"⚠️ Failed to log refresh error: {rollback_err}")

        time.sleep(60)
        i += 1

if __name__ == "__main__":
    main()
