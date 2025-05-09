import { createContext, useContext, useEffect, useState, ReactNode } from "react";
import { auth } from "../firebase";
import axios from "axios";

// Context shape definition
interface WatchlistContextType {
  watchlist: string[];                  // List of stock symbols in user's watchlist
  toggleWatchlist: (symbol: string) => void; // Function to add/remove stock
}

// Create global context with default (empty) implementation
export const WatchlistContext = createContext<WatchlistContextType>({
  watchlist: [],
  toggleWatchlist: () => {},
});

// Context provider wrapping the app
export const WatchlistProvider = ({ children }: { children: ReactNode }) => {
  const [watchlist, setWatchlist] = useState<string[]>([]);

  // Fetches watchlist symbols from backend for logged-in user
  const fetchWatchlist = async () => {
    try {
      const user = auth.currentUser;
      if (!user) return;

      const token = await user.getIdToken();

      const res = await axios.get("https://api.marketmuse.chinmaymisra.com/watchlist", {
        headers: { Authorization: `Bearer ${token}` },
      });

      const symbols = Array.isArray(res.data)
        ? res.data.map((stock) => stock.symbol)
        : [];

      setWatchlist(symbols);
    } catch (err: unknown) {
        if (axios.isAxiosError(err)) {
          console.error("❌ Watchlist fetch failed:", err.response?.data || err.message);
        } else {
          console.error("❌ Unknown error fetching watchlist:", err);
        }
      }
      
  };

  // Adds or removes a stock symbol from watchlist
  const toggleWatchlist = async (symbol: string) => {
    try {
      const user = auth.currentUser;
      if (!user) return;

      const token = await user.getIdToken();

      if (watchlist.includes(symbol)) {
        // If already in watchlist, remove it
        await axios.post(
          `https://api.marketmuse.chinmaymisra.com/watchlist/remove/${symbol}`,
          {},
          { headers: { Authorization: `Bearer ${token}` } }
        );
        setWatchlist((prev) => prev.filter((s) => s !== symbol));
      } else {
        // Otherwise, add it
        await axios.post(
          `https://api.marketmuse.chinmaymisra.com/watchlist/add/${symbol}`,
          {},
          { headers: { Authorization: `Bearer ${token}` } }
        );
        setWatchlist((prev) => [...prev, symbol]);
      }
    } catch (err) {
      console.error("Failed to update watchlist:", err);
    }
  };

  // Load watchlist runs only after Firebase is fully ready wiht a user
  useEffect(() => {
    const unsubscribe = auth.onAuthStateChanged((user) => {
      if (user) fetchWatchlist();
    });
    return () => unsubscribe();
  }, []);
  

  return (
    <WatchlistContext.Provider value={{ watchlist, toggleWatchlist }}>
      {children}
    </WatchlistContext.Provider>
  );
};

// Custom hook to use the context
export const useWatchlist = () => useContext(WatchlistContext);
