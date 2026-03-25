import { useState } from "react";
import { Button } from "@/components/ui/button";
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from "@/components/ui/card";
import { Input } from "@/components/ui/input";
import { Label } from "@/components/ui/label";
import {
  Dialog,
  DialogContent,
  DialogDescription,
  DialogHeader,
  DialogTitle,
  DialogTrigger,
} from "@/components/ui/dialog";
import {
  Select,
  SelectContent,
  SelectItem,
  SelectTrigger,
  SelectValue,
} from "@/components/ui/select";
import { useAuth } from "@/hooks/useAuth";
import { trpc } from "@/lib/trpc";
import { Star, Plus, Trash2, TrendingUp, TrendingDown, Bell, ArrowLeft } from "lucide-react";
import { Link, useLocation } from "wouter";
import { toast } from "sonner";

export default function Watchlist() {
  const { user } = useAuth();
  const [, setLocation] = useLocation();
  const [isAddDialogOpen, setIsAddDialogOpen] = useState(false);
  const [selectedStock, setSelectedStock] = useState("");
  const [notes, setNotes] = useState("");

  const utils = trpc.useUtils();
  const { data: watchlist, isLoading } = trpc.watchlist.list.useQuery();
  const { data: jseStocks } = trpc.market.jseStocks.useQuery();
  const { data: marketData } = trpc.market.overview.useQuery();

  const addToWatchlist = trpc.watchlist.add.useMutation({
    onSuccess: () => {
      utils.watchlist.list.invalidate();
      setIsAddDialogOpen(false);
      setSelectedStock("");
      setNotes("");
      toast.success("Stock added to watchlist");
    },
    onError: (error) => {
      toast.error(error.message || "Failed to add stock");
    },
  });

  const removeFromWatchlist = trpc.watchlist.remove.useMutation({
    onSuccess: () => {
      utils.watchlist.list.invalidate();
      toast.success("Stock removed from watchlist");
    },
    onError: (error) => {
      toast.error(error.message || "Failed to remove stock");
    },
  });

  if (!user) {
    setLocation("/login?returnTo=/watchlist");
    return null;
  }

  const handleAddStock = () => {
    if (!selectedStock) {
      toast.error("Please select a stock");
      return;
    }

    const stock = jseStocks?.find((s) => s.symbol === selectedStock);
    if (!stock) {
      toast.error("Stock not found");
      return;
    }

    addToWatchlist.mutate({
      stockSymbol: stock.symbol,
      stockName: stock.name,
      notes: notes || undefined,
    });
  };

  const getStockPrice = (symbol: string) => {
    const quote = marketData?.quotes.find((q) => q.symbol === symbol);
    return quote || null;
  };

  return (
    <div className="min-h-screen bg-gradient-to-br from-blue-50 via-white to-purple-50 dark:from-gray-900 dark:via-gray-800 dark:to-gray-900">
      {/* Header */}
      <div className="bg-gradient-to-r from-blue-600 to-purple-600 text-white py-8">
        <div className="container">
          <div className="flex items-center justify-between">
            <div>
              <Link href="/dashboard">
                <Button variant="ghost" className="text-white hover:bg-white/20 mb-4">
                  <ArrowLeft className="w-4 h-4 mr-2" />
                  Back to Dashboard
                </Button>
              </Link>
              <h1 className="text-3xl font-bold mb-2">My Watchlist</h1>
              <p className="text-blue-100">Track your favorite JSE stocks</p>
            </div>
            <Dialog open={isAddDialogOpen} onOpenChange={setIsAddDialogOpen}>
              <DialogTrigger asChild>
                <Button className="bg-white text-blue-600 hover:bg-blue-50">
                  <Plus className="w-4 h-4 mr-2" />
                  Add Stock
                </Button>
              </DialogTrigger>
              <DialogContent>
                <DialogHeader>
                  <DialogTitle>Add Stock to Watchlist</DialogTitle>
                  <DialogDescription>
                    Select a JSE stock to add to your watchlist
                  </DialogDescription>
                </DialogHeader>
                <div className="space-y-4 py-4">
                  <div className="space-y-2">
                    <Label htmlFor="stock">Stock</Label>
                    <Select value={selectedStock} onValueChange={setSelectedStock}>
                      <SelectTrigger id="stock">
                        <SelectValue placeholder="Select a stock" />
                      </SelectTrigger>
                      <SelectContent>
                        {jseStocks?.map((stock) => (
                          <SelectItem key={stock.symbol} value={stock.symbol}>
                            {stock.symbol} - {stock.name}
                          </SelectItem>
                        ))}
                      </SelectContent>
                    </Select>
                  </div>
                  <div className="space-y-2">
                    <Label htmlFor="notes">Notes (Optional)</Label>
                    <Input
                      id="notes"
                      placeholder="Add personal notes about this stock..."
                      value={notes}
                      onChange={(e) => setNotes(e.target.value)}
                    />
                  </div>
                </div>
                <div className="flex justify-end gap-3">
                  <Button variant="outline" onClick={() => setIsAddDialogOpen(false)}>
                    Cancel
                  </Button>
                  <Button onClick={handleAddStock} disabled={addToWatchlist.isPending}>
                    {addToWatchlist.isPending ? "Adding..." : "Add to Watchlist"}
                  </Button>
                </div>
              </DialogContent>
            </Dialog>
          </div>
        </div>
      </div>

      {/* Main Content */}
      <div className="container py-12">
        {isLoading ? (
          <div className="text-center py-12">
            <p className="text-gray-600 dark:text-gray-400">Loading watchlist...</p>
          </div>
        ) : watchlist && watchlist.length > 0 ? (
          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
            {watchlist.map((item) => {
              const priceData = getStockPrice(item.stockSymbol);
              const isPositive = priceData ? priceData.priceChange >= 0 : false;

              return (
                <Card key={item.id} className="glass-card hover:shadow-lg transition-shadow">
                  <CardHeader>
                    <div className="flex items-start justify-between">
                      <div className="flex-1">
                        <CardTitle className="text-xl">{item.stockSymbol}</CardTitle>
                        <CardDescription className="mt-1">{item.stockName}</CardDescription>
                      </div>
                      <Button
                        variant="ghost"
                        size="icon"
                        className="text-red-600 hover:text-red-700 hover:bg-red-50"
                        onClick={() => removeFromWatchlist.mutate({ id: item.id })}
                      >
                        <Trash2 className="w-4 h-4" />
                      </Button>
                    </div>
                  </CardHeader>
                  <CardContent>
                    {priceData ? (
                      <div className="space-y-4">
                        <div>
                          <p className="text-3xl font-bold">
                            R {priceData.currentPrice.toFixed(2)}
                          </p>
                          <div
                            className={`flex items-center gap-1 mt-1 ${
                              isPositive ? "text-green-600" : "text-red-600"
                            }`}
                          >
                            {isPositive ? (
                              <TrendingUp className="w-4 h-4" />
                            ) : (
                              <TrendingDown className="w-4 h-4" />
                            )}
                            <span className="font-semibold">
                              R {Math.abs(priceData.priceChange).toFixed(2)} (
                              {priceData.priceChangePercent.toFixed(2)}%)
                            </span>
                          </div>
                        </div>

                        <div className="grid grid-cols-2 gap-4 text-sm">
                          <div>
                            <p className="text-gray-600 dark:text-gray-400">Volume</p>
                            <p className="font-semibold">
                              {priceData.volume?.toLocaleString() || "N/A"}
                            </p>
                          </div>
                          <div>
                            <p className="text-gray-600 dark:text-gray-400">Sector</p>
                            <p className="font-semibold">{priceData.sector}</p>
                          </div>
                        </div>

                        {item.notes && (
                          <div className="pt-4 border-t border-gray-200 dark:border-gray-700">
                            <p className="text-sm text-gray-600 dark:text-gray-400">Notes:</p>
                            <p className="text-sm mt-1">{item.notes}</p>
                          </div>
                        )}

                        <div className="pt-4 border-t border-gray-200 dark:border-gray-700 flex gap-2">
                          <Button size="sm" variant="outline" className="flex-1">
                            <Bell className="w-3 h-3 mr-1" />
                            Set Alert
                          </Button>
                          <Link href={`/stock/${item.stockSymbol}`}>
                            <Button size="sm" variant="outline" className="flex-1">
                              View Details
                            </Button>
                          </Link>
                        </div>
                      </div>
                    ) : (
                      <p className="text-sm text-gray-600 dark:text-gray-400">
                        Price data unavailable
                      </p>
                    )}
                  </CardContent>
                </Card>
              );
            })}
          </div>
        ) : (
          <Card className="glass-card max-w-2xl mx-auto">
            <CardContent className="text-center py-12">
              <Star className="w-16 h-16 text-gray-400 mx-auto mb-4" />
              <h3 className="text-xl font-semibold mb-2">Your watchlist is empty</h3>
              <p className="text-gray-600 dark:text-gray-400 mb-6">
                Start tracking your favorite JSE stocks to monitor their performance
              </p>
              <Button onClick={() => setIsAddDialogOpen(true)}>
                <Plus className="w-4 h-4 mr-2" />
                Add Your First Stock
              </Button>
            </CardContent>
          </Card>
        )}
      </div>
    </div>
  );
}
