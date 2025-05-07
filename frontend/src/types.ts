export interface Stock {
    symbol: string;
    full_name?: string;
    name?: string;
    exchange?: string;
    price: number;
    change?: number;
    percent_change?: number;
    volume?: number;
    pe_ratio?: number;
    market_cap?: number;
    high_52w?: number;
    low_52w?: number;
    history: number[];
    isTopGainer?: boolean;
  }
  