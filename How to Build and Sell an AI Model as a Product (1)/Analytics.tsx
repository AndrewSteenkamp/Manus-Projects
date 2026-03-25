import { useState } from "react";
import { Button } from "@/components/ui/button";
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from "@/components/ui/card";
import {
  Select,
  SelectContent,
  SelectItem,
  SelectTrigger,
  SelectValue,
} from "@/components/ui/select";
import { useAuth } from "@/hooks/useAuth";
import { trpc } from "@/lib/trpc";
import {
  LineChart,
  Line,
  BarChart,
  Bar,
  XAxis,
  YAxis,
  CartesianGrid,
  Tooltip,
  Legend,
  ResponsiveContainer,
  Area,
  AreaChart,
} from "recharts";
import { ArrowLeft, TrendingUp, TrendingDown, Download } from "lucide-react";
import { Link, useLocation } from "wouter";

export default function Analytics() {
  const { user } = useAuth();
  const [, setLocation] = useLocation();
  const [selectedStock, setSelectedStock] = useState("NPN.JO");
  const [timeRange, setTimeRange] = useState<"1d" | "5d" | "1mo" | "3mo" | "6mo" | "1y">("1mo");

  const { data: jseStocks } = trpc.market.jseStocks.useQuery();
  const { data: stockHistory, isLoading } = trpc.market.stockHistory.useQuery({
    symbol: selectedStock,
    range: timeRange,
  });
  const { data: marketData } = trpc.market.overview.useQuery();

  if (!user) {
    setLocation("/login?returnTo=/analytics");
    return null;
  }

  const currentStock = jseStocks?.find((s) => s.symbol === selectedStock);
  const currentQuote = marketData?.quotes.find((q) => q.symbol === selectedStock);

  // Prepare chart data
  const chartData = stockHistory?.prices.map((price: number, index: number) => ({
    date: new Date(stockHistory.timestamps[index] * 1000).toLocaleDateString(),
    price: price,
    volume: stockHistory.volumes[index],
  })) || [];

  // Calculate technical indicators
  const calculateSMA = (data: number[], period: number) => {
    const sma: (number | null)[] = [];
    for (let i = 0; i < data.length; i++) {
      if (i < period - 1) {
        sma.push(null);
      } else {
        const sum = data.slice(i - period + 1, i + 1).reduce((a, b) => a + b, 0);
        sma.push(sum / period);
      }
    }
    return sma;
  };

  const prices = stockHistory?.prices || [];
  const sma20 = calculateSMA(prices, 20);
  const sma50 = calculateSMA(prices, 50);

  const chartDataWithIndicators = chartData.map((item: any, index: number) => ({
    ...item,
    sma20: sma20[index],
    sma50: sma50[index],
  }));

  // Sector performance data
  const sectorData = [
    { sector: "Technology", performance: 5.2 },
    { sector: "Financials", performance: 3.1 },
    { sector: "Energy", performance: -1.5 },
    { sector: "Healthcare", performance: 2.8 },
    { sector: "Consumer", performance: 1.9 },
  ];

  return (
    <div className="min-h-screen bg-gradient-to-br from-blue-50 via-white to-purple-50 dark:from-gray-900 dark:via-gray-800 dark:to-gray-900">
      {/* Header */}
      <div className="bg-gradient-to-r from-blue-600 to-purple-600 text-white py-8">
        <div className="container">
          <Link href="/dashboard">
            <Button variant="ghost" className="text-white hover:bg-white/20 mb-4">
              <ArrowLeft className="w-4 h-4 mr-2" />
              Back to Dashboard
            </Button>
          </Link>
          <h1 className="text-3xl font-bold mb-2">Advanced Analytics</h1>
          <p className="text-blue-100">Technical analysis and market insights</p>
        </div>
      </div>

      {/* Main Content */}
      <div className="container py-12 space-y-8">
        {/* Stock Selector */}
        <Card className="glass-card">
          <CardHeader>
            <div className="flex flex-col md:flex-row md:items-center md:justify-between gap-4">
              <div>
                <CardTitle>Stock Analysis</CardTitle>
                <CardDescription>Select a stock and time range to analyze</CardDescription>
              </div>
              <div className="flex flex-col sm:flex-row gap-4">
                <Select value={selectedStock} onValueChange={setSelectedStock}>
                  <SelectTrigger className="w-full sm:w-[200px]">
                    <SelectValue placeholder="Select stock" />
                  </SelectTrigger>
                  <SelectContent>
                    {jseStocks?.map((stock) => (
                      <SelectItem key={stock.symbol} value={stock.symbol}>
                        {stock.symbol}
                      </SelectItem>
                    ))}
                  </SelectContent>
                </Select>
                <Select value={timeRange} onValueChange={(v: any) => setTimeRange(v)}>
                  <SelectTrigger className="w-full sm:w-[150px]">
                    <SelectValue placeholder="Time range" />
                  </SelectTrigger>
                  <SelectContent>
                    <SelectItem value="1d">1 Day</SelectItem>
                    <SelectItem value="5d">5 Days</SelectItem>
                    <SelectItem value="1mo">1 Month</SelectItem>
                    <SelectItem value="3mo">3 Months</SelectItem>
                    <SelectItem value="6mo">6 Months</SelectItem>
                    <SelectItem value="1y">1 Year</SelectItem>
                  </SelectContent>
                </Select>
                <Button variant="outline">
                  <Download className="w-4 h-4 mr-2" />
                  Export
                </Button>
              </div>
            </div>
          </CardHeader>
          <CardContent>
            {currentStock && currentQuote && (
              <div className="grid grid-cols-2 md:grid-cols-4 gap-4 mb-6">
                <div>
                  <p className="text-sm text-gray-600 dark:text-gray-400">Current Price</p>
                  <p className="text-2xl font-bold">R {currentQuote.currentPrice.toFixed(2)}</p>
                </div>
                <div>
                  <p className="text-sm text-gray-600 dark:text-gray-400">Change</p>
                  <div
                    className={`text-2xl font-bold ${
                      currentQuote.priceChange >= 0 ? "text-green-600" : "text-red-600"
                    }`}
                  >
                    {currentQuote.priceChange >= 0 ? "+" : ""}
                    {currentQuote.priceChangePercent.toFixed(2)}%
                  </div>
                </div>
                <div>
                  <p className="text-sm text-gray-600 dark:text-gray-400">Volume</p>
                  <p className="text-2xl font-bold">
                    {currentQuote.volume?.toLocaleString() || "N/A"}
                  </p>
                </div>
                <div>
                  <p className="text-sm text-gray-600 dark:text-gray-400">Sector</p>
                  <p className="text-2xl font-bold">{currentQuote.sector}</p>
                </div>
              </div>
            )}
          </CardContent>
        </Card>

        {/* Price Chart with Moving Averages */}
        <Card className="glass-card">
          <CardHeader>
            <CardTitle>Price Chart with Moving Averages</CardTitle>
            <CardDescription>
              SMA 20 (orange) and SMA 50 (purple) overlaid on price action
            </CardDescription>
          </CardHeader>
          <CardContent>
            {isLoading ? (
              <div className="h-[400px] flex items-center justify-center">
                <p className="text-gray-600 dark:text-gray-400">Loading chart data...</p>
              </div>
            ) : chartDataWithIndicators.length > 0 ? (
              <ResponsiveContainer width="100%" height={400}>
                <LineChart data={chartDataWithIndicators}>
                  <CartesianGrid strokeDasharray="3 3" />
                  <XAxis dataKey="date" />
                  <YAxis domain={["auto", "auto"]} />
                  <Tooltip />
                  <Legend />
                  <Line
                    type="monotone"
                    dataKey="price"
                    stroke="#3b82f6"
                    strokeWidth={2}
                    name="Price"
                    dot={false}
                  />
                  <Line
                    type="monotone"
                    dataKey="sma20"
                    stroke="#f97316"
                    strokeWidth={2}
                    name="SMA 20"
                    dot={false}
                    strokeDasharray="5 5"
                  />
                  <Line
                    type="monotone"
                    dataKey="sma50"
                    stroke="#a855f7"
                    strokeWidth={2}
                    name="SMA 50"
                    dot={false}
                    strokeDasharray="5 5"
                  />
                </LineChart>
              </ResponsiveContainer>
            ) : (
              <div className="h-[400px] flex items-center justify-center">
                <p className="text-gray-600 dark:text-gray-400">No data available</p>
              </div>
            )}
          </CardContent>
        </Card>

        {/* Volume Chart */}
        <Card className="glass-card">
          <CardHeader>
            <CardTitle>Trading Volume</CardTitle>
            <CardDescription>Daily trading volume over selected period</CardDescription>
          </CardHeader>
          <CardContent>
            {chartData.length > 0 ? (
              <ResponsiveContainer width="100%" height={300}>
                <BarChart data={chartData}>
                  <CartesianGrid strokeDasharray="3 3" />
                  <XAxis dataKey="date" />
                  <YAxis />
                  <Tooltip />
                  <Bar dataKey="volume" fill="#8b5cf6" name="Volume" />
                </BarChart>
              </ResponsiveContainer>
            ) : (
              <div className="h-[300px] flex items-center justify-center">
                <p className="text-gray-600 dark:text-gray-400">No volume data available</p>
              </div>
            )}
          </CardContent>
        </Card>

        {/* Sector Performance */}
        <Card className="glass-card">
          <CardHeader>
            <CardTitle>Sector Performance</CardTitle>
            <CardDescription>JSE sector performance comparison</CardDescription>
          </CardHeader>
          <CardContent>
            <ResponsiveContainer width="100%" height={300}>
              <BarChart data={sectorData} layout="vertical">
                <CartesianGrid strokeDasharray="3 3" />
                <XAxis type="number" />
                <YAxis dataKey="sector" type="category" />
                <Tooltip />
                <Bar dataKey="performance" fill="#3b82f6" name="Performance %" />
              </BarChart>
            </ResponsiveContainer>
          </CardContent>
        </Card>

        {/* ECM Analysis */}
        <Card className="glass-card">
          <CardHeader>
            <CardTitle>Economic Confidence Model (ECM)</CardTitle>
            <CardDescription>Market cycle analysis and predictions</CardDescription>
          </CardHeader>
          <CardContent>
            {marketData && (
              <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
                <div className="text-center p-6 bg-gradient-to-br from-blue-50 to-blue-100 dark:from-blue-900 dark:to-blue-800 rounded-lg">
                  <p className="text-sm text-gray-600 dark:text-gray-400 mb-2">
                    Confidence Score
                  </p>
                  <p className="text-4xl font-bold text-blue-600 dark:text-blue-400">
                    {marketData.ecm.confidence}%
                  </p>
                </div>
                <div className="text-center p-6 bg-gradient-to-br from-purple-50 to-purple-100 dark:from-purple-900 dark:to-purple-800 rounded-lg">
                  <p className="text-sm text-gray-600 dark:text-gray-400 mb-2">
                    Market Direction
                  </p>
                  <div className="flex items-center justify-center gap-2">
                    {marketData.ecm.direction === "bullish" ? (
                      <TrendingUp className="w-8 h-8 text-green-600" />
                    ) : marketData.ecm.direction === "bearish" ? (
                      <TrendingDown className="w-8 h-8 text-red-600" />
                    ) : null}
                    <p className="text-2xl font-bold capitalize">{marketData.ecm.direction}</p>
                  </div>
                </div>
                <div className="text-center p-6 bg-gradient-to-br from-green-50 to-green-100 dark:from-green-900 dark:to-green-800 rounded-lg">
                  <p className="text-sm text-gray-600 dark:text-gray-400 mb-2">Cycle Position</p>
                  <p className="text-2xl font-bold capitalize">{marketData.ecm.cyclePosition}</p>
                </div>
              </div>
            )}
          </CardContent>
        </Card>
      </div>
    </div>
  );
}
