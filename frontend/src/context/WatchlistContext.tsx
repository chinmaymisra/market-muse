import { createContext, useContext, useEffect, useState, ReactNode } from "react";
import { auth } from "../firebase";
import axios from "axios";

interface WatchlistContextType {
  watchlist: string[];
  toggleWatchlist: (symbol: string) => void;
}

export const WatchlistContext = createContext<WatchlistContextType>({
  watchlist: [],
  toggleWatchlist: () => {},
});

export const WatchlistProvider = ({ children }: { children: ReactNode }) => {
  const [watchlist, setWatchlist] = useState<string[]>([]);

  const fetchWatchlist = async () => {
    try {
      const user = auth.currentUser;
      if (!user) return;
      const token = await user.getIdToken();
      const res = await axios.get("https://api.marketmuse.chinmaymisra.com/watchlist", {
        headers: { Authorization: `Bearer ${token}` },
      });
      setWatchlist(res.data);
    } catch (err) {
      console.error("Failed to fetch watchlist:", err);
    }
  };

  const toggleWatchlist = async (symbol: string) => {
    try {
      const user = auth.currentUser;
      if (!user) return;
      const token = await user.getIdToken();

      if (watchlist.includes(symbol)) {
        await axios.delete("https://api.marketmuse.chinmaymisra.com/watchlist", {
          data: { symbol },
          headers: { Authorization: `Bearer ${token}` },
        });
        setWatchlist((prev) => prev.filter((s) => s !== symbol));
      } else {
        await axios.post(
          "https://api.marketmuse.chinmaymisra.com/watchlist",
          { symbol },
          { headers: { Authorization: `Bearer ${token}` } }
        );
        setWatchlist((prev) => [...prev, symbol]);
      }
    } catch (err) {
      console.error("Failed to update watchlist:", err);
    }
  };

  useEffect(() => {
    fetchWatchlist();
  }, []);

  return (
    <WatchlistContext.Provider value={{ watchlist, toggleWatchlist }}>
      {children}
    </WatchlistContext.Provider>
  );
};

export const useWatchlist = () => useContext(WatchlistContext);
