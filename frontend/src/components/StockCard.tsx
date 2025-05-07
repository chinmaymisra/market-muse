import { useEffect, useState } from "react";
import { LineChart, Line, ResponsiveContainer, YAxis } from "recharts";
import { Stock } from "../types";

interface Props {
  stock: Stock;
  isTopGainer?: boolean;
}

export default function StockCard({ stock, isTopGainer }: Props) {
  const [lineColor, setLineColor] = useState("#22c55e");

  useEffect(() => {
    const isDark = document.documentElement.classList.contains("dark");
    const color =
      stock.change && stock.change < 0
        ? isDark ? "#f87171" : "#ef4444"
        : isDark ? "#4ade80" : "#22c55e";
    setLineColor(color);
  }, [stock.change]);

  const parsedHistory: number[] = Array.isArray(stock.history)
    ? stock.history.map((val) => {
        const num = typeof val === "number" ? val : parseFloat(val);
        return isNaN(num) ? 0 : num;
      })
    : [];

  const chartData = parsedHistory.map((price, index) => ({
    index,
    price,
  }));

  const formatCompactNumber = (num: number | undefined): string =>
    typeof num === "number"
      ? Intl.NumberFormat("en", { notation: "compact" }).format(num)
      : "—";

  return (
    <div className="bg-white dark:bg-gray-800 shadow rounded-xl p-4 w-full max-w-sm">
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

      <ResponsiveContainer width="100%" height={60}>
        <LineChart data={chartData}>
          <YAxis hide domain={["dataMin", "dataMax"]} />
          <Line
            type="monotone"
            dataKey="price"
            stroke={lineColor}
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
    </div>
  );
}
