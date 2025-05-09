from pydantic import BaseModel

class WatchlistItem(BaseModel):
    """
    Schema representing a single watchlisted stock symbol.

    Used as a response model for `GET /watchlist` route.
    """
    symbol: str             # Stock ticker symbol (e.g., "AAPL")

    class Config:
        orm_mode = True     # Allows conversion from Watchlist ORM model
