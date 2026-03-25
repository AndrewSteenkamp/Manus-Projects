/**
 * JSE Market Data Integration
 * Real-time stock prices and ECM calculations for Johannesburg Stock Exchange
 */

import { callDataApi } from "./_core/dataApi";

// Major JSE stocks to track
export const JSE_STOCKS = [
  { symbol: "NPN.JO", name: "Naspers", sector: "Technology" },
  { symbol: "SBK.JO", name: "Standard Bank", sector: "Financials" },
  { symbol: "AGL.JO", name: "Anglo American", sector: "Energy" },
  { symbol: "FSR.JO", name: "FirstRand", sector: "Financials" },
  { symbol: "SHP.JO", name: "Shoprite", sector: "Consumer" },
  { symbol: "MTN.JO", name: "MTN Group", sector: "Technology" },
  { symbol: "SOL.JO", name: "Sasol", sector: "Energy" },
  { symbol: "ABG.JO", name: "Absa Group", sector: "Financials" },
  { symbol: "NED.JO", name: "Nedbank", sector: "Financials" },
  { symbol: "REM.JO", name: "Remgro", sector: "Financials" },
] as const;

export interface StockQuote {
  symbol: string;
  name: string;
  sector: string;
  currentPrice: number;
  priceChange: number;
  priceChangePercent: number;
  volume: string;
  marketCap: string;
  high: number;
  low: number;
  open: number;
  previousClose: number;
}

export interface ECMAnalysis {
  confidence: number; // 0-100
  direction: "bullish" | "bearish" | "neutral";
  supportLevel: number;
  resistanceLevel: number;
  cyclePosition: string;
  turningPoint: Date | null;
  volatility: number;
}

export interface SectorPerformance {
  sector: string;
  avgChange: number;
  stockCount: number;
  topPerformer: string;
  worstPerformer: string;
}

/**
 * Fetch real-time stock data from Yahoo Finance
 */
export async function fetchStockQuote(symbol: string): Promise<StockQuote | null> {
  try {
    const result = await callDataApi("YahooFinance/get_stock_chart", {
      query: {
        symbol: symbol,
        region: "US",
        interval: "1d",
        range: "1d",
      },
    }) as any;

    if (!result?.chart?.result?.[0]) {
      console.warn(`[MarketData] No data for ${symbol}`);
      return null;
    }

    const data = result.chart.result[0];
    const meta = data.meta;
    const quote = data.indicators?.quote?.[0];

    if (!meta || !quote) {
      return null;
    }

    // JSE prices are in cents (ZAc), convert to rands
    const currentPriceCents = meta.regularMarketPrice || 0;
    const previousCloseCents = meta.previousClose || currentPriceCents;
    
    const currentPrice = currentPriceCents / 100; // Convert cents to rands
    const previousClose = previousCloseCents / 100;
    const priceChange = currentPrice - previousClose;
    const priceChangePercent = previousClose !== 0 ? (priceChange / previousClose) * 100 : 0;

    // Find stock info from our JSE list
    const stockInfo = JSE_STOCKS.find(s => s.symbol === symbol);

    return {
      symbol: symbol,
      name: stockInfo?.name || meta.symbol || symbol,
      sector: stockInfo?.sector || "Unknown",
      currentPrice: currentPrice,
      priceChange: priceChange,
      priceChangePercent: priceChangePercent,
      volume: meta.regularMarketVolume?.toLocaleString() || "0",
      marketCap: formatMarketCap(meta.marketCap),
      high: (meta.regularMarketDayHigh || currentPriceCents) / 100,
      low: (meta.regularMarketDayLow || currentPriceCents) / 100,
      open: (meta.regularMarketOpen || currentPriceCents) / 100,
      previousClose: previousClose,
    };
  } catch (error) {
    console.error(`[MarketData] Error fetching ${symbol}:`, error);
    return null;
  }
}

/**
 * Fetch quotes for all major JSE stocks
 */
export async function fetchAllJSEStocks(): Promise<StockQuote[]> {
  const promises = JSE_STOCKS.map(stock => fetchStockQuote(stock.symbol));
  const results = await Promise.all(promises);
  return results.filter((quote): quote is StockQuote => quote !== null);
}

/**
 * Calculate ECM (Economic Confidence Model) analysis
 * Based on Martin Armstrong's methodology - simplified version
 */
export function calculateECM(quotes: StockQuote[]): ECMAnalysis {
  if (quotes.length === 0) {
    return {
      confidence: 50,
      direction: "neutral",
      supportLevel: 0,
      resistanceLevel: 0,
      cyclePosition: "Unknown",
      turningPoint: null,
      volatility: 0,
    };
  }

  // Calculate average price change across all stocks
  const avgChange = quotes.reduce((sum, q) => sum + q.priceChangePercent, 0) / quotes.length;

  // Calculate volatility (standard deviation of price changes)
  const variance = quotes.reduce((sum, q) => {
    const diff = q.priceChangePercent - avgChange;
    return sum + diff * diff;
  }, 0) / quotes.length;
  const volatility = Math.sqrt(variance);

  // Determine market direction
  let direction: "bullish" | "bearish" | "neutral" = "neutral";
  if (avgChange > 1.0) direction = "bullish";
  else if (avgChange < -1.0) direction = "bearish";

  // Calculate confidence based on consistency and magnitude
  const bullishCount = quotes.filter(q => q.priceChangePercent > 0).length;
  const consistency = Math.abs((bullishCount / quotes.length) - 0.5) * 2; // 0 to 1
  const magnitude = Math.min(Math.abs(avgChange) / 5, 1); // normalize to 0-1
  const confidence = Math.round((consistency * 0.6 + magnitude * 0.4) * 100);

  // Support/resistance levels don't make sense for market-wide analysis
  // (can't average prices of different stocks like R921 Naspers + R180 Standard Bank)
  // Instead, show as index points based on market strength
  // These represent market sentiment strength, not price levels
  const baseIndex = 1000; // Baseline market index
  const supportLevel = baseIndex * (1 - volatility / 100);
  const resistanceLevel = baseIndex * (1 + volatility / 100);

  // Determine cycle position (simplified 8.6 year cycle)
  const now = new Date();
  const cycleStart = new Date("2020-01-01"); // arbitrary start
  const daysSinceStart = Math.floor((now.getTime() - cycleStart.getTime()) / (1000 * 60 * 60 * 24));
  const cycleDays = 8.6 * 365.25; // 8.6 years in days
  const cycleProgress = (daysSinceStart % cycleDays) / cycleDays;

  let cyclePosition = "Mid-Cycle";
  if (cycleProgress < 0.25) cyclePosition = "Early Expansion";
  else if (cycleProgress < 0.5) cyclePosition = "Peak Formation";
  else if (cycleProgress < 0.75) cyclePosition = "Contraction";
  else cyclePosition = "Bottom Formation";

  // Estimate next turning point
  const daysToTurningPoint = Math.round(cycleDays * (1 - cycleProgress));
  const turningPoint = new Date(now.getTime() + daysToTurningPoint * 24 * 60 * 60 * 1000);

  return {
    confidence: Math.max(0, Math.min(100, confidence)),
    direction,
    supportLevel: Math.round(supportLevel * 100) / 100,
    resistanceLevel: Math.round(resistanceLevel * 100) / 100,
    cyclePosition,
    turningPoint,
    volatility: Math.round(volatility * 100) / 100,
  };
}

/**
 * Calculate sector performance aggregates
 */
export function calculateSectorPerformance(quotes: StockQuote[]): SectorPerformance[] {
  const sectorMap = new Map<string, StockQuote[]>();

  // Group by sector
  quotes.forEach(quote => {
    const sector = quote.sector;
    if (!sectorMap.has(sector)) {
      sectorMap.set(sector, []);
    }
    sectorMap.get(sector)!.push(quote);
  });

  // Calculate aggregates
  const sectorPerformance: SectorPerformance[] = [];
  sectorMap.forEach((stocks, sector) => {
    const avgChange = stocks.reduce((sum, s) => sum + s.priceChangePercent, 0) / stocks.length;
    const sorted = [...stocks].sort((a, b) => b.priceChangePercent - a.priceChangePercent);

    sectorPerformance.push({
      sector,
      avgChange: Math.round(avgChange * 100) / 100,
      stockCount: stocks.length,
      topPerformer: sorted[0]?.name || "N/A",
      worstPerformer: sorted[sorted.length - 1]?.name || "N/A",
    });
  });

  return sectorPerformance.sort((a, b) => b.avgChange - a.avgChange);
}

/**
 * Get comprehensive market overview
 */
export async function getMarketOverview() {
  const quotes = await fetchAllJSEStocks();
  const ecm = calculateECM(quotes);
  const sectors = calculateSectorPerformance(quotes);

  return {
    quotes,
    ecm,
    sectors,
    lastUpdated: new Date(),
  };
}

/**
 * Format market cap for display
 */
function formatMarketCap(marketCap: number | undefined): string {
  if (!marketCap) return "N/A";

  const billion = 1_000_000_000;
  const million = 1_000_000;

  if (marketCap >= billion) {
    return `R${(marketCap / billion).toFixed(2)}B`;
  } else if (marketCap >= million) {
    return `R${(marketCap / million).toFixed(2)}M`;
  } else {
    return `R${marketCap.toLocaleString()}`;
  }
}

/**
 * Get historical price data for charting
 */
export async function getStockHistory(symbol: string, range: string = "1mo") {
  try {
    const result = await callDataApi("YahooFinance/get_stock_chart", {
      query: {
        symbol: symbol,
        region: "US",
        interval: "1d",
        range: range,
      },
    }) as any;

    if (!result?.chart?.result?.[0]) {
      return null;
    }

    const data = result.chart.result[0];
    const timestamps = data.timestamp || [];
    const quotes = data.indicators?.quote?.[0];

    if (!quotes) {
      return null;
    }

    // Convert cents to rands for all historical prices
    const history = timestamps.map((ts: number, i: number) => ({
      date: new Date(ts * 1000),
      open: (quotes.open?.[i] || 0) / 100,
      high: (quotes.high?.[i] || 0) / 100,
      low: (quotes.low?.[i] || 0) / 100,
      close: (quotes.close?.[i] || 0) / 100,
      volume: quotes.volume?.[i] || 0,
    }));

    return history;
  } catch (error) {
    console.error(`[MarketData] Error fetching history for ${symbol}:`, error);
    return null;
  }
}
