import { useEffect, useState } from "react";
import { BrowserRouter as Router, Routes, Route, useNavigate } from "react-router-dom";
import axios from "axios";
import { signOut } from "firebase/auth";

import { Stock } from "./types";
import StockCard from "./components/StockCard";
import "./index.css";
import { auth } from "./firebase";
import LoginPage from "./pages/LoginPage";
import { AuthProvider, useAuth } from "./context/AuthContext";

if (typeof window !== "undefined") {
  (window as any).auth = auth;
}

function MainApp() {
  const { user, loading } = useAuth();
  const isAuthenticated = !!user;

  const [stocks, setStocks] = useState<Stock[]>([]);
  const [lastUpdated, setLastUpdated] = useState<string>("");
  const [search, setSearch] = useState<string>("");
  const [isDark, setIsDark] = useState<boolean>(false);

  const navigate = useNavigate();

  useEffect(() => {
    if (!loading && !user && navigate) {
      navigate("/login");
    }
  }, [user, loading, navigate]);

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
        headers: { Authorization: `Bearer ${token}` },
        timeout: 30000,
      });
      setStocks(res.data);
      setLastUpdated(new Date().toLocaleTimeString());
    } catch (err) {
      console.error("Failed to fetch stock data:", err);
      setStocks([]);
    } finally {
      setRefreshing(false);
    }
  };

  useEffect(() => {
    if (isAuthenticated) {
      fetchStocks();
      const interval = setInterval(fetchStocks, 60000);
      return () => clearInterval(interval);
    }
  }, [isAuthenticated, user]);

  const filteredStocks = stocks.filter((stock: Stock) =>
    (stock.full_name ?? "").toLowerCase().includes(search.toLowerCase()) ||
    stock.symbol.toLowerCase().includes(search.toLowerCase())
  );

  const topGainerSymbol = [...stocks]
    .filter(s => typeof s.percent_change === "number")
    .sort((a, b) => (b.percent_change ?? 0) - (a.percent_change ?? 0))[0]?.symbol;

  if (loading) {
    return (
      <div className="h-screen w-screen flex items-center justify-center bg-gray-900 text-white">
        <div className="flex flex-col items-center gap-4">
          <div className="w-12 h-12 border-4 border-blue-500 border-t-transparent rounded-full animate-spin" />
          <p className="text-lg font-semibold">Launching MarketMuse...</p>
        </div>
      </div>
    );
  }

  if (!isAuthenticated) return null;

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
              onClick={() => setIsDark(!isDark)}
              className="px-4 py-2 text-sm rounded bg-gray-800 text-white hover:bg-gray-700 transition"
            >
              {isDark ? "Light Mode" : "Dark Mode"}
            </button>
            <p className="text-sm">Welcome, {user?.displayName}</p>
            <button
              onClick={() => signOut(auth)}
              className="px-4 py-2 text-sm rounded bg-red-600 text-white hover:bg-red-700 transition"
            >
              Logout
            </button>
          </div>
        </div>

        {filteredStocks.length === 0 ? (
          <div className="flex flex-col items-center justify-center mt-20 text-gray-500 dark:text-gray-400">
            <div className="w-10 h-10 border-4 border-blue-500 border-t-transparent rounded-full animate-spin mb-3" />
            <p className="text-sm animate-pulse">Loading stocks, please wait...</p>
          </div>
        ) : (
          <div className="grid grid-cols-1 sm:grid-cols-2 md:grid-cols-3 gap-6">
            {filteredStocks.map((stock) => (
              <StockCard key={stock.symbol} stock={stock} isTopGainer={stock.symbol === topGainerSymbol} />
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
