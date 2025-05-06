import { useEffect, useState } from "react";
import axios from "axios";
import { Stock } from "./types";
import StockCard from "./components/StockCard";
import "./index.css";

import { BrowserRouter as Router, Routes, Route } from "react-router-dom";
import { LoginPage } from "./pages/LoginPage";
import { AuthProvider, useAuth } from "./context/AuthContext";
import { signOut } from "firebase/auth";
import { auth } from "./firebase";

function MainApp() {
  const [stocks, setStocks] = useState<Stock[]>([]);
  const [lastUpdated, setLastUpdated] = useState<string>("");
  const [refreshing, setRefreshing] = useState<boolean>(false);
  const [search, setSearch] = useState<string>("");
  const [isDark, setIsDark] = useState<boolean>(false);

  const { user, loading } = useAuth();
  const isAuthenticated = !!user;

  useEffect(() => {
    const savedTheme = localStorage.getItem("theme");
    setIsDark(savedTheme === "dark");
  }, []);

  useEffect(() => {
    document.documentElement.classList.toggle("dark", isDark);
    localStorage.setItem("theme", isDark ? "dark" : "light");
  }, [isDark]);

  const fetchStocks = async () => {
    try {
      setRefreshing(true);

      const token = await user?.getIdToken();
      const res = await axios.get("https://api.marketmuse.chinmaymisra.com/stocks", {
        headers: {
          Authorization: `Bearer ${token}`,
        },
        timeout: 10000,
      });

      setStocks(res.data);
      const now = new Date();
      setLastUpdated(now.toLocaleTimeString());
    } catch (error: any) {
      console.error("Failed to fetch stock data:", error);
      setStocks([]);
    } finally {
      setRefreshing(false);
    }
  };

  useEffect(() => {
    if (isAuthenticated) {
      fetchStocks();
      const interval = setInterval(fetchStocks, 42000);
      return () => clearInterval(interval);
    }
  }, [isAuthenticated]);

  const filteredStocks = stocks.filter((stock) =>
    stock.full_name.toLowerCase().includes(search.toLowerCase()) ||
    stock.symbol.toLowerCase().includes(search.toLowerCase())
  );

  if (loading) {
    return (
      <div className="h-screen w-screen flex items-center justify-center bg-gray-900 text-white">
        <div className="flex flex-col items-center gap-4">
          <div className="w-12 h-12 border-4 border-blue-500 border-t-transparent rounded-full animate-spin"></div>
          <p className="text-lg font-semibold">Launching MarketMuse...</p>
        </div>
      </div>
    );
  }

  if (!isAuthenticated) {
    return <p className="text-white text-center mt-20">Please log in to view content.</p>;
  }

  return (
    <div className={`min-h-screen w-screen overflow-x-hidden ${isDark ? "dark bg-gray-900" : "bg-gray-100"} p-6`}>
      <div className="text-gray-900 dark:text-gray-100 max-w-screen-xl mx-auto">
        <h1 className="text-3xl font-bold text-center mb-4">MarketMuse</h1>

        <div className="flex flex-col sm:flex-row justify-between items-center gap-4 mb-6">
          <p className="text-sm">Last updated: {lastUpdated || "Loading..."}</p>
          <div className="flex gap-3 items-center flex-wrap">
            <input
              type="text"
              value={search}
              onChange={(e) => setSearch(e.target.value)}
              placeholder="Search by name or symbol"
              className="px-3 py-2 border border-gray-300 dark:border-gray-700 bg-white dark:bg-gray-800 text-sm rounded-md text-black dark:text-white w-64"
            />
            <button
              onClick={fetchStocks}
              className={`px-4 py-2 text-sm rounded ${
                refreshing ? "bg-gray-400 cursor-not-allowed" : "bg-blue-600 hover:bg-blue-700"
              } text-white transition`}
              disabled={refreshing}
            >
              {refreshing ? "Refreshing..." : "Refresh Now"}
            </button>
            <button
              onClick={() => setIsDark(!isDark)}
              className="px-4 py-2 text-sm rounded bg-gray-800 text-white hover:bg-gray-700 transition"
            >
              {isDark ? "Light Mode" : "Dark Mode"}
            </button>
            <p className="text-sm">
            Welcome, {typeof user?.displayName === "string" ? user.displayName : "User"}
            </p>

            <button
              onClick={() => signOut(auth)}
              className="px-4 py-2 text-sm rounded bg-red-600 text-white hover:bg-red-700 transition"
            >
              Logout
            </button>
          </div>
        </div>

        {filteredStocks.length === 0 ? (
          refreshing ? (
            <p className="text-center text-gray-500 dark:text-gray-400 mt-10">
              Waking up server, please wait...
            </p>
          ) : (
            <p className="text-center text-gray-500 dark:text-gray-400 mt-10">
              No stocks found.
            </p>
          )
        ) : (
          <div className="grid grid-cols-1 sm:grid-cols-2 md:grid-cols-3 gap-6">
            {filteredStocks.map((stock) => (
              <StockCard key={stock.symbol} stock={stock} />
            ))}
          </div>
        )}
      </div>
    </div>
  );
}

function App() {
  return (
    <AuthProvider>
      <Router>
        <Routes>
          <Route path="/login" element={<LoginPage />} />
          <Route path="*" element={<MainApp />} />
        </Routes>
      </Router>
    </AuthProvider>
  );
}

export default App;
