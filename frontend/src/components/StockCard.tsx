import { useContext } from "react";
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

interface Props {
  stock: Stock;
  isTopGainer?: boolean;
}

export default function StockCard({ stock, isTopGainer }: Props) {
  const { watchlist, toggleWatchlist } = useContext(WatchlistContext);
  const isInWatchlist = watchlist.includes(stock.symbol);

  const parsedHistory = Array.isArray(stock.history)
    ? stock.history.map((val) => {
        const num = typeof val === "number" ? val : parseFloat(val);
        return isNaN(num) ? stock.price ?? 0 : num;
      })
    : Array(4).fill(stock.price ?? 0);

  const chartData = parsedHistory.map((price, index) => ({
    index,
    price,
  }));

  const formatCompactNumber = (num: number | undefined): string =>
    typeof num === "number"
      ? Intl.NumberFormat("en", { notation: "compact" }).format(num)
      : "—";

  return (
    <div className="bg-white dark:bg-gray-800 shadow rounded-xl p-4 w-full max-w-sm relative">
      <div className="flex justify-between items-start mb-2">
        <div>
          <h2 className="font-semibold text-base text-gray-800 dark:text-white">
            {stock.full_name ?? stock.symbol}
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

      {isTopGainer && (
        <p className="inline-block mb-2 px-2 py-1 text-xs font-semibold bg-green-500 text-white rounded">
          🔥 Top Gainer
        </p>
      )}

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

      <div className="absolute bottom-2 right-2">
        <button
          onClick={() => toggleWatchlist(stock.symbol)}
          className={`text-xl font-bold ${
            isInWatchlist ? "text-green-500" : "text-blue-400"
          }`}
          title={isInWatchlist ? "Remove from Watchlist" : "Add to Watchlist"}
        >
          +
        </button>
      </div>
    </div>
  );
}
