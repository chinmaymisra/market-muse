import { useContext, useState } from "react";
import { Stock } from "../types";
import {
  LineChart,
  Line,
  ResponsiveContainer,
  YAxis,
  CartesianGrid,
  Tooltip,
} from "recharts";
import { WatchlistContext } from "../context/WatchlistContext";
import clsx from "clsx";

// Define the expected props for this component
interface Props {
  stock: Stock;
  isTopGainer?: boolean;
}

// The stock card component used to display individual stock info
export default function StockCard({ stock, isTopGainer }: Props) {
  const { watchlist, toggleWatchlist } = useContext(WatchlistContext);
  const isInWatchlist = watchlist.includes(stock.symbol);
  const [animating, setAnimating] = useState(false);

  // Toggles the stock's watchlist status and animates the button
  const handleToggle = async () => {
    setAnimating(true);
    await toggleWatchlist(stock.symbol);
    setTimeout(() => setAnimating(false), 300); // animation duration
  };

  // Ensure the history array is numeric and fallback-safe
  const parsedHistory = Array.isArray(stock.history)
    ? stock.history.map((val) => {
        const num = typeof val === "number" ? val : parseFloat(val);
        return isNaN(num) ? stock.price ?? 0 : num;
      })
    : Array(4).fill(stock.price ?? 0);

  // Reformat history for chart rendering
  const chartData = parsedHistory.map((price, index) => ({
    index,
    price,
  }));

  // Formats large numbers like market cap using compact notation (e.g., 1.2B)
  const formatCompactNumber = (num: number | undefined): string =>
    typeof num === "number"
      ? Intl.NumberFormat("en", { notation: "compact" }).format(num)
      : "—";

  return (
    <div className="bg-white dark:bg-gray-800 shadow rounded-xl p-4 w-full max-w-sm relative transition-transform duration-300">
      {/* Watchlist toggle button (Add or Remove) */}
      <div className="absolute bottom-2 right-2">
        <button
          onClick={handleToggle}
          title={isInWatchlist ? "Remove from Watchlist" : "Add to Watchlist"}
          className={clsx(
            "text-lg font-bold border rounded-md px-2 py-1 transition-all duration-300 focus:outline-none",
            animating ? "scale-110" : "scale-100",
            isInWatchlist
              ? "text-red-500 border-red-500 hover:bg-red-500 hover:text-white"
              : "text-blue-500 border-blue-500 hover:bg-blue-500 hover:text-white"
          )}
        >
          {isInWatchlist ? "−" : "+"}
        </button>
      </div>

      {/* Stock info section (name, exchange, price, change) */}
      <div className="flex justify-between items-start mb-2">
        <div>
          <h2 className="font-semibold text-base text-gray-800 dark:text-white">
            {stock.name ?? stock.symbol}
          </h2>
          <p className="text-sm text-gray-600 dark:text-gray-300">
            {stock.symbol} {stock.exchange ? `• ${stock.exchange}` : ""}
          </p>
        </div>
        <div className="text-right">
          <p className="text-lg font-bold text-gray-900 dark:text-white">
            ${stock.price?.toFixed(2)}
          </p>
          {typeof stock.change === "number" &&
          typeof stock.percent_change === "number" ? (
            <p
              className={`text-sm ${
                stock.change >= 0 ? "text-green-500" : "text-red-500"
              }`}
            >
              {stock.change.toFixed(2)} ({stock.percent_change.toFixed(2)}%)
            </p>
          ) : (
            <p className="text-sm text-gray-400">No change data</p>
          )}
        </div>
      </div>

      {/* Highlight badge if this is the top gainer */}
      {isTopGainer && (
        <p className="inline-block mb-2 px-2 py-1 text-xs font-semibold bg-green-500 text-white rounded">
          🔥 Top Gainer
        </p>
      )}

      {/* Mini chart for stock price trend */}
      <ResponsiveContainer width="100%" height={80}>
        <LineChart data={chartData}>
          <CartesianGrid strokeDasharray="3 3" />
          <YAxis
            domain={["dataMin", "dataMax"]}
            tickFormatter={(v: number) => `$${v.toFixed(0)}`}
            width={40}
          />
          <Tooltip
            formatter={(value: number) => `$${value.toFixed(2)}`}
            labelFormatter={() => ""}
            contentStyle={{
              backgroundColor: "#1f2937",
              border: "none",
              color: "#fff",
            }}
          />
          <Line
            type="monotone"
            dataKey="price"
            stroke={stock.change && stock.change >= 0 ? "#22c55e" : "#ef4444"}
            strokeWidth={2}
            dot={false}
            isAnimationActive={false}
          />
        </LineChart>
      </ResponsiveContainer>

      {/* Stock metrics below the chart */}
      <div className="mt-4 text-xs text-gray-700 dark:text-gray-300 space-y-1">
        <p>
          <strong>P/E Ratio:</strong>{" "}
          {stock.pe_ratio ? stock.pe_ratio.toFixed(2) : "—"}
        </p>
        <p>
          <strong>Market Cap:</strong> {formatCompactNumber(stock.market_cap)}
        </p>
        <p>
          <strong>52W High:</strong>{" "}
          {stock.high_52w ? `$${stock.high_52w.toFixed(2)}` : "—"}
        </p>
        <p>
          <strong>52W Low:</strong>{" "}
          {stock.low_52w ? `$${stock.low_52w.toFixed(2)}` : "—"}
        </p>
      </div>
    </div>
  );
}
