from sqlalchemy.orm import Session
from sqlalchemy import select, desc
from app.database import SessionLocal
from app.models.stock_cache import StockCache
from app.models.refresh_log_model import RefreshLog
from app.models.settings_model import Setting
from app.services.stock_service import get_stock_data


def get_symbols_from_db(db: Session):
    """
    Fetch all unique stock symbols from the stock_cache table.
    """
    results = db.execute(select(StockCache.symbol)).scalars().all()
    return results


def get_last_index(db: Session) -> int:
    """
    Reads the last_index value from the settings table.
    Returns 0 if the key doesn't exist yet.
    """
    result = db.query(Setting).filter_by(key="last_index").first()
    if result:
        return int(result.value)
    return 0


def set_last_index(db: Session, index: int):
    """
    Writes the updated last_index back to the settings table.
    Creates the row if it doesn't exist.
    """
    entry = db.query(Setting).filter_by(key="last_index").first()
    if entry:
        entry.value = str(index)
    else:
        entry = Setting(key="last_index", value=str(index))
        db.add(entry)
    db.commit()


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
    GitHub Actions-compatible stock refresher that:
    - Retrieves list of stock symbols from DB
    - Uses round-robin index stored in settings
    - Refreshes 1 stock per run
    - Logs to refresh_log table
    - Updates round-robin index in DB
    - Trims log table to last 10 rows
    """
    db: Session = SessionLocal()

    try:
        symbols = get_symbols_from_db(db)
        if not symbols:
            print("⚠️ No symbols found in stock_cache.")
            return

        i = get_last_index(db)
        symbol = symbols[i % len(symbols)]
        print(f"🔄 Refreshing {symbol} (index {i})...")

        try:
            get_stock_data([symbol], db)
            db.add(RefreshLog(symbol=symbol, status="success"))
            db.commit()
            print(f"✅ {symbol} refreshed successfully.")
        except Exception as e:
            db.rollback()
            db.add(RefreshLog(symbol=symbol, status=f"error: {e}"))
            db.commit()
            print(f"❌ Error refreshing {symbol}: {e}")

        # Update last_index in settings
        set_last_index(db, i + 1)

        # Trim refresh_log table
        trim_refresh_log(db)

    except Exception as outer:
        print(f"🚨 Unexpected error in main(): {outer}")


if __name__ == "__main__":
    main()
