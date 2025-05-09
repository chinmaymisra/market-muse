from sqlalchemy import Column, String, ForeignKey, PrimaryKeyConstraint
from app.database import Base

class Watchlist(Base):
    __tablename__ = "watchlist"

    user_id = Column(String, ForeignKey("users.uid"), nullable=False)
    symbol = Column(String, ForeignKey("stock_cache.symbol"), nullable=False)

    __table_args__ = (PrimaryKeyConstraint("user_id", "symbol"),)
