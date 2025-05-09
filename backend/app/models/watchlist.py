from sqlalchemy import Column, String, ForeignKey, PrimaryKeyConstraint
from app.database import Base

class Watchlist(Base):
    """
    SQLAlchemy model for the 'watchlist' table.
    Stores a many-to-many relationship between users and stocks they want to track.
    """
    __tablename__ = "watchlist"

    # Foreign key to the 'users' table (user's UID)
    user_id = Column(String, ForeignKey("users.uid"), nullable=False)

    # Foreign key to the 'stock_cache' table (stock symbol)
    symbol = Column(String, ForeignKey("stock_cache.symbol"), nullable=False)

    # Composite primary key to ensure a user can't watch the same stock twice
    __table_args__ = (PrimaryKeyConstraint("user_id", "symbol"),)
