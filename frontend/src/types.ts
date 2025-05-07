export interface Stock {
    symbol: string;
    full_name: string;
    price: number;
    volume: number;
    name?: string;              // optional — not currently returned
    exchange?: string;          // optional
    change?: number;            // optional
    percent_change?: number;    // optional
    history?: number[];         // optional
  }
  