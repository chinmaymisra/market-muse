export interface Stock {
    symbol: string;
    name: string;
    full_name: string;
    exchange: string;
    price: number;
    change: number;
    percent_change: number;
    history: number[];
  }
  