import { useEffect, useState } from "react";
import { trpc } from "@/lib/trpc";
import { Button } from "@/components/ui/button";
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from "@/components/ui/card";
import { TrendingUp, TrendingDown, Activity, DollarSign, ArrowRight } from "lucide-react";
import { Link } from "wouter";

export default function Home() {
  const { data: marketData, isLoading, refetch } = trpc.market.overview.useQuery();
  const { data: plans } = trpc.plans.list.useQuery();

  // Auto-refresh every 30 seconds
  useEffect(() => {
    const interval = setInterval(() => {
      refetch();
    }, 30000);
    return () => clearInterval(interval);
  }, [refetch]);

  if (isLoading) {
    return (
      <div className="min-h-screen bg-gradient-to-br from-blue-50 via-white to-purple-50 dark:from-gray-900 dark:via-gray-800 dark:to-gray-900 flex items-center justify-center">
        <div className="text-center">
          <Activity className="w-16 h-16 animate-spin text-blue-600 mx-auto mb-4" />
          <p className="text-lg text-gray-600 dark:text-gray-300">Loading market data...</p>
        </div>
      </div>
    );
  }

  const ecm = marketData?.ecm;
  const quotes = marketData?.quotes || [];
  const sectors = marketData?.sectors || [];

  return (
    <div className="min-h-screen bg-gradient-to-br from-blue-50 via-white to-purple-50 dark:from-gray-900 dark:via-gray-800 dark:to-gray-900">
      {/* Hero Section */}
      <div className="bg-gradient-to-r from-blue-600 to-purple-600 text-white py-16">
        <div className="container">
          <div className="max-w-4xl mx-auto text-center">
            <h1 className="text-5xl font-bold mb-4">Siener AI</h1>
            <p className="text-xl mb-2">Advanced JSE Market Analysis</p>
            <p className="text-blue-100 mb-8">
              Powered by the Economic Confidence Model - Real-time insights for South African traders
            </p>
            <div className="flex items-center justify-center gap-4">
              <Link href="/pricing">
                <Button size="lg" variant="secondary" className="gap-2">
                  View Pricing <ArrowRight className="w-4 h-4" />
                </Button>
              </Link>
            </div>
          </div>
        </div>
      </div>

      {/* ECM Dashboard */}
      <div className="container py-12">
        {/* ECM Confidence Card */}
        <Card className="glass-card mb-8">
          <CardHeader>
            <CardTitle className="text-2xl flex items-center gap-2">
              <Activity className="w-6 h-6 text-blue-600" />
              Economic Confidence Model (ECM)
            </CardTitle>
            <CardDescription>
              Real-time market analysis based on Martin Armstrong's methodology
            </CardDescription>
          </CardHeader>
          <CardContent>
            <div className="grid grid-cols-1 md:grid-cols-4 gap-6">
              <div className="text-center">
                <div className="text-5xl font-bold text-blue-600 mb-2">{ecm?.confidence}%</div>
                <div className="text-sm text-gray-600 dark:text-gray-400">Confidence Score</div>
              </div>
              <div className="text-center">
                <div className="flex items-center justify-center mb-2">
                  {ecm?.direction === "bullish" ? (
                    <TrendingUp className="w-12 h-12 text-green-600" />
                  ) : ecm?.direction === "bearish" ? (
                    <TrendingDown className="w-12 h-12 text-red-600" />
                  ) : (
                    <Activity className="w-12 h-12 text-gray-600" />
                  )}
                </div>
                <div className="text-lg font-semibold capitalize">{ecm?.direction}</div>
                <div className="text-sm text-gray-600 dark:text-gray-400">Market Direction</div>
              </div>
              <div className="text-center">
                <div className="text-2xl font-bold text-gray-800 dark:text-gray-200 mb-2">
                  {ecm?.cyclePosition}
                </div>
                <div className="text-sm text-gray-600 dark:text-gray-400">Cycle Position</div>
              </div>
              <div className="text-center">
                <div className="text-2xl font-bold text-gray-800 dark:text-gray-200 mb-2">
                  {ecm?.volatility}%
                </div>
                <div className="text-sm text-gray-600 dark:text-gray-400">Volatility</div>
              </div>
            </div>
            <div className="mt-6 pt-6 border-t border-gray-200 dark:border-gray-700 grid grid-cols-1 md:grid-cols-2 gap-4">
              <div>
                <div className="text-sm text-gray-600 dark:text-gray-400 mb-1">Support Index</div>
                <div className="text-xl font-semibold text-green-600">{ecm?.supportLevel?.toFixed(0)} pts</div>
              </div>
              <div>
                <div className="text-sm text-gray-600 dark:text-gray-400 mb-1">Resistance Index</div>
                <div className="text-xl font-semibold text-red-600">{ecm?.resistanceLevel?.toFixed(0)} pts</div>
              </div>
            </div>
          </CardContent>
        </Card>

        {/* Sector Performance */}
        <Card className="glass-card mb-8">
          <CardHeader>
            <CardTitle className="text-2xl">Sector Performance</CardTitle>
            <CardDescription>Real-time JSE sector analysis</CardDescription>
          </CardHeader>
          <CardContent>
            <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-4">
              {sectors.map((sector) => (
                <div
                  key={sector.sector}
                  className="p-4 rounded-lg border border-gray-200 dark:border-gray-700 hover:shadow-lg transition-shadow"
                >
                  <div className="text-lg font-semibold mb-2">{sector.sector}</div>
                  <div className={`text-3xl font-bold mb-2 ${sector.avgChange >= 0 ? "price-up" : "price-down"}`}>
                    {sector.avgChange >= 0 ? "+" : ""}
                    {sector.avgChange.toFixed(2)}%
                  </div>
                  <div className="text-sm text-gray-600 dark:text-gray-400">
                    {sector.stockCount} stocks tracked
                  </div>
                </div>
              ))}
            </div>
          </CardContent>
        </Card>

        {/* Top JSE Stocks */}
        <Card className="glass-card mb-8">
          <CardHeader>
            <CardTitle className="text-2xl">Major JSE Stocks</CardTitle>
            <CardDescription>Live prices updated every 30 seconds</CardDescription>
          </CardHeader>
          <CardContent>
            <div className="space-y-4">
              {quotes.map((quote) => (
                <div
                  key={quote.symbol}
                  className="flex items-center justify-between p-4 rounded-lg border border-gray-200 dark:border-gray-700 hover:bg-gray-50 dark:hover:bg-gray-800 transition-colors"
                >
                  <div className="flex-1">
                    <div className="font-semibold text-lg">{quote.name}</div>
                    <div className="text-sm text-gray-600 dark:text-gray-400">{quote.sector}</div>
                  </div>
                  <div className="text-right">
                    <div className="text-xl font-bold">R {quote.currentPrice.toFixed(2)}</div>
                    <div className={`text-sm font-semibold ${quote.priceChange >= 0 ? "price-up" : "price-down"}`}>
                      {quote.priceChange >= 0 ? "+" : ""}
                      {quote.priceChange.toFixed(2)} ({quote.priceChangePercent.toFixed(2)}%)
                    </div>
                  </div>
                </div>
              ))}
            </div>
          </CardContent>
        </Card>

        {/* Subscription Tiers */}
        <div className="mb-8">
          <h2 className="text-3xl font-bold text-center mb-4">Choose Your Plan</h2>
          <p className="text-center text-gray-600 dark:text-gray-400 mb-8">
            Get access to advanced market analysis and exclusive features
          </p>
          <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
            {plans?.map((plan) => {
              const features = JSON.parse(plan.features);
              return (
                <Card key={plan.id} className="glass-card hover:shadow-2xl transition-shadow">
                  <CardHeader>
                    <CardTitle className="text-2xl">{plan.name}</CardTitle>
                    <CardDescription>{plan.description}</CardDescription>
                  </CardHeader>
                  <CardContent>
                    <div className="mb-6">
                      <div className="text-4xl font-bold text-blue-600">
                        R {parseFloat(plan.priceRands).toFixed(0)}
                      </div>
                      <div className="text-sm text-gray-600 dark:text-gray-400">per month</div>
                    </div>
                    <ul className="space-y-3 mb-6">
                      {features.map((feature: string, idx: number) => (
                        <li key={idx} className="flex items-start gap-2">
                          <div className="w-5 h-5 rounded-full bg-green-100 dark:bg-green-900 flex items-center justify-center flex-shrink-0 mt-0.5">
                            <div className="w-2 h-2 rounded-full bg-green-600" />
                          </div>
                          <span className="text-sm">{feature}</span>
                        </li>
                      ))}
                    </ul>
                    <Link href={`/checkout?plan=${plan.id}`}>
                      <Button className="w-full" size="lg">
                        Subscribe Now
                      </Button>
                    </Link>
                  </CardContent>
                </Card>
              );
            })}
          </div>
        </div>

        {/* Last Updated */}
        <div className="text-center text-sm text-gray-600 dark:text-gray-400">
          Last updated: {marketData?.lastUpdated ? new Date(marketData.lastUpdated).toLocaleTimeString() : "N/A"}
          <br />
          <span className="text-xs">Auto-refreshes every 30 seconds</span>
        </div>
      </div>
    </div>
  );
}
