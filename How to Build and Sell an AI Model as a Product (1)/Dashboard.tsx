import { Button } from "@/components/ui/button";
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from "@/components/ui/card";
import { useAuth } from "@/hooks/useAuth";
import { trpc } from "@/lib/trpc";
import {
  TrendingUp,
  CreditCard,
  Bell,
  Star,
  BarChart3,
  Settings,
  LogOut,
  ArrowUpRight,
  ArrowDownRight,
  Mail,
} from "lucide-react";
import { Link, useLocation } from "wouter";

export default function Dashboard() {
  const { user } = useAuth();
  const [, setLocation] = useLocation();
  const logout = trpc.auth.logout.useMutation();

  const { data: subscription } = trpc.subscriptions.current.useQuery();
  const { data: watchlist } = trpc.watchlist.list.useQuery();
  const { data: paymentHistory } = trpc.payments.history.useQuery();
  const { data: plans } = trpc.plans.list.useQuery();

  const handleLogout = async () => {
    await logout.mutateAsync();
    setLocation("/");
  };

  if (!user) {
    setLocation("/login?returnTo=/dashboard");
    return null;
  }

  const activePlan = plans?.find(p => p.id === subscription?.planId);
  const watchlistCount = watchlist?.length || 0;
  const alertsUsed = 0; // TODO: Implement alerts

  return (
    <div className="min-h-screen bg-gradient-to-br from-blue-50 via-white to-purple-50 dark:from-gray-900 dark:via-gray-800 dark:to-gray-900">
      {/* Header */}
      <div className="bg-gradient-to-r from-blue-600 to-purple-600 text-white py-8">
        <div className="container">
          <div className="flex items-center justify-between">
            <div>
              <h1 className="text-3xl font-bold mb-2">Welcome back, {user.name}!</h1>
              <p className="text-blue-100">Your Siener AI Dashboard</p>
            </div>
            <div className="flex items-center gap-4">
              <Link href="/">
                <Button variant="ghost" className="text-white hover:bg-white/20">
                  <TrendingUp className="w-4 h-4 mr-2" />
                  Market Overview
                </Button>
              </Link>
              <Button
                variant="ghost"
                className="text-white hover:bg-white/20"
                onClick={handleLogout}
              >
                <LogOut className="w-4 h-4 mr-2" />
                Logout
              </Button>
            </div>
          </div>
        </div>
      </div>

      {/* Main Content */}
      <div className="container py-12">
        {/* Stats Overview */}
        <div className="grid grid-cols-1 md:grid-cols-4 gap-6 mb-8">
          <Card className="glass-card">
            <CardHeader className="flex flex-row items-center justify-between pb-2">
              <CardTitle className="text-sm font-medium text-gray-600 dark:text-gray-400">
                Active Plan
              </CardTitle>
              <CreditCard className="w-4 h-4 text-blue-600" />
            </CardHeader>
            <CardContent>
              <div className="text-2xl font-bold">{activePlan?.name || "Free"}</div>
              <p className="text-xs text-gray-600 dark:text-gray-400 mt-1">
                {subscription?.status === "active" ? "Active" : "Inactive"}
              </p>
            </CardContent>
          </Card>

          <Card className="glass-card">
            <CardHeader className="flex flex-row items-center justify-between pb-2">
              <CardTitle className="text-sm font-medium text-gray-600 dark:text-gray-400">
                Stocks Tracked
              </CardTitle>
              <Star className="w-4 h-4 text-yellow-600" />
            </CardHeader>
            <CardContent>
              <div className="text-2xl font-bold">{watchlistCount}</div>
              <p className="text-xs text-gray-600 dark:text-gray-400 mt-1">
                {activePlan?.maxStocks === 999999
                  ? "Unlimited"
                  : `of ${activePlan?.maxStocks || 0}`}
              </p>
            </CardContent>
          </Card>

          <Card className="glass-card">
            <CardHeader className="flex flex-row items-center justify-between pb-2">
              <CardTitle className="text-sm font-medium text-gray-600 dark:text-gray-400">
                Price Alerts
              </CardTitle>
              <Bell className="w-4 h-4 text-green-600" />
            </CardHeader>
            <CardContent>
              <div className="text-2xl font-bold">{alertsUsed}</div>
              <p className="text-xs text-gray-600 dark:text-gray-400 mt-1">
                {activePlan?.maxAlerts === 999999
                  ? "Unlimited"
                  : `of ${activePlan?.maxAlerts || 0}`}
              </p>
            </CardContent>
          </Card>

          <Card className="glass-card">
            <CardHeader className="flex flex-row items-center justify-between pb-2">
              <CardTitle className="text-sm font-medium text-gray-600 dark:text-gray-400">
                Analytics
              </CardTitle>
              <BarChart3 className="w-4 h-4 text-purple-600" />
            </CardHeader>
            <CardContent>
              <div className="text-2xl font-bold">
                {activePlan?.advancedAnalytics ? "Advanced" : "Basic"}
              </div>
              <p className="text-xs text-gray-600 dark:text-gray-400 mt-1">
                {activePlan?.apiAccess ? "API Enabled" : "No API"}
              </p>
            </CardContent>
          </Card>
        </div>

        <div className="grid grid-cols-1 lg:grid-cols-3 gap-8">
          {/* Main Column */}
          <div className="lg:col-span-2 space-y-8">
            {/* Subscription Details */}
            <Card className="glass-card">
              <CardHeader>
                <CardTitle>Subscription Details</CardTitle>
                <CardDescription>Manage your Siener AI subscription</CardDescription>
              </CardHeader>
              <CardContent>
                {subscription ? (
                  <div className="space-y-6">
                    <div className="grid grid-cols-2 gap-6">
                      <div>
                        <p className="text-sm text-gray-600 dark:text-gray-400 mb-1">Plan</p>
                        <p className="text-lg font-semibold">{activePlan?.name}</p>
                      </div>
                      <div>
                        <p className="text-sm text-gray-600 dark:text-gray-400 mb-1">Status</p>
                        <div className="flex items-center gap-2">
                          <div
                            className={`w-2 h-2 rounded-full ${
                              subscription.status === "active" ? "bg-green-600" : "bg-gray-400"
                            }`}
                          />
                          <p className="text-lg font-semibold capitalize">{subscription.status}</p>
                        </div>
                      </div>
                      <div>
                        <p className="text-sm text-gray-600 dark:text-gray-400 mb-1">
                          Billing Amount
                        </p>
                        <p className="text-lg font-semibold">
                          R{parseFloat(activePlan?.priceRands || "0").toFixed(2)}/month
                        </p>
                      </div>
                      <div>
                        <p className="text-sm text-gray-600 dark:text-gray-400 mb-1">
                          Next Billing Date
                        </p>
                        <p className="text-lg font-semibold">
                          {new Date(subscription.endDate).toLocaleDateString()}
                        </p>
                      </div>
                    </div>

                    <div className="pt-6 border-t border-gray-200 dark:border-gray-700 flex gap-4">
                      <Link href="/pricing">
                        <Button variant="outline">Change Plan</Button>
                      </Link>
                      <Button variant="outline" className="text-red-600 hover:text-red-700">
                        Cancel Subscription
                      </Button>
                    </div>
                  </div>
                ) : (
                  <div className="text-center py-8">
                    <p className="text-gray-600 dark:text-gray-400 mb-4">
                      You don't have an active subscription
                    </p>
                    <Link href="/pricing">
                      <Button>View Pricing Plans</Button>
                    </Link>
                  </div>
                )}
              </CardContent>
            </Card>

            {/* Watchlist */}
            <Card className="glass-card">
              <CardHeader>
                <div className="flex items-center justify-between">
                  <div>
                    <CardTitle>My Watchlist</CardTitle>
                    <CardDescription>Stocks you're tracking</CardDescription>
                  </div>
                  <Button size="sm">Add Stock</Button>
                </div>
              </CardHeader>
              <CardContent>
                {watchlist && watchlist.length > 0 ? (
                  <div className="space-y-4">
                    {watchlist.map((item) => (
                      <div
                        key={item.id}
                        className="flex items-center justify-between p-4 bg-gray-50 dark:bg-gray-800 rounded-lg"
                      >
                        <div>
                          <p className="font-semibold">{item.stockSymbol}</p>
                          <p className="text-sm text-gray-600 dark:text-gray-400">
                            {item.stockName}
                          </p>
                        </div>
                        <div className="text-right">
                          <p className="font-semibold">R 0.00</p>
                          <div className="flex items-center gap-1 text-sm text-green-600">
                            <ArrowUpRight className="w-3 h-3" />
                            <span>0.00%</span>
                          </div>
                        </div>
                      </div>
                    ))}
                  </div>
                ) : (
                  <div className="text-center py-8">
                    <Star className="w-12 h-12 text-gray-400 mx-auto mb-4" />
                    <p className="text-gray-600 dark:text-gray-400 mb-4">
                      Your watchlist is empty
                    </p>
                    <Button size="sm">Add Your First Stock</Button>
                  </div>
                )}
              </CardContent>
            </Card>
          </div>

          {/* Sidebar */}
          <div className="space-y-8">
            {/* Quick Actions */}
            <Card className="glass-card">
              <CardHeader>
                <CardTitle>Quick Actions</CardTitle>
              </CardHeader>
              <CardContent className="space-y-3">
                <Link href="/">
                  <Button variant="outline" className="w-full justify-start">
                    <TrendingUp className="w-4 h-4 mr-2" />
                    View Market Data
                  </Button>
                </Link>
                <Link href="/watchlist">
                  <Button variant="outline" className="w-full justify-start">
                    <Star className="w-4 h-4 mr-2" />
                    Manage Watchlist
                  </Button>
                </Link>
                <Button variant="outline" className="w-full justify-start">
                  <Bell className="w-4 h-4 mr-2" />
                  Create Price Alert
                </Button>
                <Link href="/newsletters">
                  <Button variant="outline" className="w-full justify-start">
                    <Mail className="w-4 h-4 mr-2" />
                    View Newsletters
                  </Button>
                </Link>
                <Link href="/analytics">
                  <Button variant="outline" className="w-full justify-start">
                    <BarChart3 className="w-4 h-4 mr-2" />
                    View Analytics
                  </Button>
                </Link>
                <Button variant="outline" className="w-full justify-start">
                  <Settings className="w-4 h-4 mr-2" />
                  Account Settings
                </Button>
              </CardContent>
            </Card>

            {/* Payment History */}
            <Card className="glass-card">
              <CardHeader>
                <CardTitle>Recent Payments</CardTitle>
                <CardDescription>Your billing history</CardDescription>
              </CardHeader>
              <CardContent>
                {paymentHistory && paymentHistory.length > 0 ? (
                  <div className="space-y-4">
                    {paymentHistory.slice(0, 3).map((payment) => (
                      <div
                        key={payment.id}
                        className="flex items-center justify-between pb-4 border-b border-gray-200 dark:border-gray-700 last:border-0"
                      >
                        <div>
                          <p className="font-semibold">R{parseFloat(payment.amountRands).toFixed(2)}</p>
                          <p className="text-xs text-gray-600 dark:text-gray-400">
                            {new Date(payment.createdAt).toLocaleDateString()}
                          </p>
                        </div>
                        <div
                          className={`text-xs px-2 py-1 rounded-full ${
                            payment.status === "completed"
                              ? "bg-green-100 text-green-700 dark:bg-green-900 dark:text-green-300"
                              : "bg-yellow-100 text-yellow-700 dark:bg-yellow-900 dark:text-yellow-300"
                          }`}
                        >
                          {payment.status}
                        </div>
                      </div>
                    ))}
                    <Button variant="ghost" className="w-full text-sm">
                      View All Payments
                    </Button>
                  </div>
                ) : (
                  <p className="text-sm text-gray-600 dark:text-gray-400 text-center py-4">
                    No payment history yet
                  </p>
                )}
              </CardContent>
            </Card>
          </div>
        </div>
      </div>
    </div>
  );
}
