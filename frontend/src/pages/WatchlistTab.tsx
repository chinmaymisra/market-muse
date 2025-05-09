import { useEffect, useState } from "react";
import { useAuth } from "../context/AuthContext";
import { useWatchlist } from "../context/WatchlistContext";
import { Stock } from "../types";
import StockCard from "../components/StockCard";
import axios from "axios";

export default function WatchlistTab() {
  const { user } = useAuth();                 // Get the current logged-in user
  const { watchlist } = useWatchlist();       // Get user's selected stock symbols

  const [stocks, setStocks] = useState<Stock[]>([]); // Local stock info state
  const [loading, setLoading] = useState<boolean>(false); // Loading spinner state

  useEffect(() => {
    const fetchWatchlistStocks = async () => {
      try {
        if (!user || watchlist.length === 0) {
          setStocks([]); // If no user or empty watchlist, clear state
          return;
        }

        setLoading(true); // Show loading indicator
        const token = await user.getIdToken();

        // Fetch all cached stocks
        const res = await axios.get("https://api.marketmuse.chinmaymisra.com/stocks", {
          headers: { Authorization: `Bearer ${token}` },
        });

        // Filter down to user's watchlist
        const filtered = res.data.filter((stock: Stock) =>
          watchlist.includes(stock.symbol)
        );
        setStocks(filtered);
      } catch (err) {
        console.error("Failed to load watchlist stocks:", err);
        setStocks([]);
      } finally {
        setLoading(false);
      }
    };

    // Fetch watchlist on load or when user/watchlist changes
    fetchWatchlistStocks();
  }, [user, watchlist]);

  return (
    <div className="min-h-screen w-screen overflow-x-hidden p-6 dark:bg-gray-900 bg-gray-100 text-gray-900 dark:text-gray-100">
      <h1 className="text-2xl font-bold mb-6 text-center">My Watchlist</h1>

      {/* Display state-specific UI: loading, empty, or stock cards */}
      {loading ? (
        <p className="text-center text-gray-500 dark:text-gray-400 mt-10">
          Loading watchlist...
        </p>
      ) : stocks.length === 0 ? (
        <p className="text-center text-gray-500 dark:text-gray-400 mt-10">
          No stocks in your watchlist.
        </p>
      ) : (
        <div className="grid grid-cols-1 sm:grid-cols-2 md:grid-cols-3 gap-6">
          {stocks.map((stock) => (
            <StockCard key={stock.symbol} stock={stock} />
          ))}
        </div>
      )}
    </div>
  );
}
