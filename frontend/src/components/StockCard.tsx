import { Stock } from "../types";
import { LineChart, Line, ResponsiveContainer } from "recharts";

interface Props {
  stock: Stock;
}

export default function StockCard({ stock }: Props) {
  console.log("Rendering StockCard:", stock);

  const chartData = stock.history?.map((price, index) => ({
    index,
    price,
  })) ?? [];

  return (
    <div className="bg-white dark:bg-gray-800 shadow rounded-xl p-4 w-full max-w-sm">
      <div className="flex justify-between items-center mb-2">
        <div>
          <h2 className="font-semibold text-base text-gray-800 dark:text-white">
            {stock.full_name}
          </h2>
          <p className="text-sm text-gray-600 dark:text-gray-300">
            {stock.symbol} {stock.exchange ? `• ${stock.exchange}` : ""}
          </p>
        </div>
        <div className="text-right">
          <p className="text-lg font-bold text-gray-900 dark:text-white">
            ${stock.price.toFixed(2)}
          </p>
          {typeof stock.change === "number" && typeof stock.percent_change === "number" ? (
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
      <ResponsiveContainer width="100%" height={50}>
        <LineChart data={chartData}>
          <Line
            type="monotone"
            dataKey="price"
            stroke="#2563eb"
            strokeWidth={2}
            dot={false}
          />
        </LineChart>
      </ResponsiveContainer>
    </div>
  );
}
