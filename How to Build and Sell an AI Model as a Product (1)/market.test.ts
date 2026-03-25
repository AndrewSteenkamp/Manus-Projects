import { describe, expect, it } from "vitest";
import { calculateECM, calculateSectorPerformance, JSE_STOCKS } from "./marketData";
import type { StockQuote } from "./marketData";

describe("Market Data Functions", () => {
  const mockQuotes: StockQuote[] = [
    {
      symbol: "NPN.JO",
      name: "Naspers",
      sector: "Technology",
      currentPrice: 3500.0,
      priceChange: 50.0,
      priceChangePercent: 1.45,
      volume: "1000000",
      marketCap: "R150B",
      high: 3550.0,
      low: 3450.0,
      open: 3480.0,
      previousClose: 3450.0,
    },
    {
      symbol: "SBK.JO",
      name: "Standard Bank",
      sector: "Financials",
      currentPrice: 180.5,
      priceChange: -2.3,
      priceChangePercent: -1.26,
      volume: "2000000",
      marketCap: "R80B",
      high: 183.0,
      low: 179.0,
      open: 182.0,
      previousClose: 182.8,
    },
    {
      symbol: "AGL.JO",
      name: "Anglo American",
      sector: "Energy",
      currentPrice: 450.0,
      priceChange: 10.0,
      priceChangePercent: 2.27,
      volume: "500000",
      marketCap: "R120B",
      high: 455.0,
      low: 445.0,
      open: 448.0,
      previousClose: 440.0,
    },
  ];

  describe("calculateECM", () => {
    it("should calculate ECM with valid quotes", () => {
      const ecm = calculateECM(mockQuotes);

      expect(ecm).toBeDefined();
      expect(ecm.confidence).toBeGreaterThanOrEqual(0);
      expect(ecm.confidence).toBeLessThanOrEqual(100);
      expect(["bullish", "bearish", "neutral"]).toContain(ecm.direction);
      expect(ecm.supportLevel).toBeGreaterThan(0);
      expect(ecm.resistanceLevel).toBeGreaterThan(0);
      expect(ecm.resistanceLevel).toBeGreaterThan(ecm.supportLevel);
      expect(ecm.volatility).toBeGreaterThanOrEqual(0);
      expect(ecm.cyclePosition).toBeTruthy();
    });

    it("should handle empty quotes array", () => {
      const ecm = calculateECM([]);

      expect(ecm.confidence).toBe(50);
      expect(ecm.direction).toBe("neutral");
      expect(ecm.supportLevel).toBe(0);
      expect(ecm.resistanceLevel).toBe(0);
      expect(ecm.volatility).toBe(0);
    });

    it("should identify bullish market when average change > 1%", () => {
      const bullishQuotes: StockQuote[] = mockQuotes.map((q) => ({
        ...q,
        priceChangePercent: 2.5,
      }));

      const ecm = calculateECM(bullishQuotes);
      expect(ecm.direction).toBe("bullish");
    });

    it("should identify bearish market when average change < -1%", () => {
      const bearishQuotes: StockQuote[] = mockQuotes.map((q) => ({
        ...q,
        priceChangePercent: -2.5,
      }));

      const ecm = calculateECM(bearishQuotes);
      expect(ecm.direction).toBe("bearish");
    });
  });

  describe("calculateSectorPerformance", () => {
    it("should aggregate sector performance correctly", () => {
      const sectors = calculateSectorPerformance(mockQuotes);

      expect(sectors).toHaveLength(3); // Technology, Financials, Energy
      expect(sectors[0]).toHaveProperty("sector");
      expect(sectors[0]).toHaveProperty("avgChange");
      expect(sectors[0]).toHaveProperty("stockCount");
      expect(sectors[0]).toHaveProperty("topPerformer");
      expect(sectors[0]).toHaveProperty("worstPerformer");
    });

    it("should sort sectors by performance descending", () => {
      const sectors = calculateSectorPerformance(mockQuotes);

      // Energy has highest change (2.27%), should be first
      expect(sectors[0]?.sector).toBe("Energy");
      expect(sectors[0]?.avgChange).toBeCloseTo(2.27, 2);

      // Financials has lowest change (-1.26%), should be last
      expect(sectors[sectors.length - 1]?.sector).toBe("Financials");
    });

    it("should identify top and worst performers per sector", () => {
      const sectors = calculateSectorPerformance(mockQuotes);
      const techSector = sectors.find((s) => s.sector === "Technology");

      expect(techSector).toBeDefined();
      expect(techSector?.topPerformer).toBe("Naspers");
      expect(techSector?.worstPerformer).toBe("Naspers");
    });

    it("should handle empty quotes array", () => {
      const sectors = calculateSectorPerformance([]);
      expect(sectors).toHaveLength(0);
    });
  });

  describe("JSE_STOCKS constant", () => {
    it("should contain major JSE stocks", () => {
      expect(JSE_STOCKS.length).toBeGreaterThan(0);
      
      const symbols = JSE_STOCKS.map((s) => s.symbol);
      expect(symbols).toContain("NPN.JO"); // Naspers
      expect(symbols).toContain("SBK.JO"); // Standard Bank
      expect(symbols).toContain("AGL.JO"); // Anglo American
    });

    it("should have valid structure for each stock", () => {
      JSE_STOCKS.forEach((stock) => {
        expect(stock).toHaveProperty("symbol");
        expect(stock).toHaveProperty("name");
        expect(stock).toHaveProperty("sector");
        expect(stock.symbol).toMatch(/\.JO$/); // JSE stocks end with .JO
      });
    });
  });
});
