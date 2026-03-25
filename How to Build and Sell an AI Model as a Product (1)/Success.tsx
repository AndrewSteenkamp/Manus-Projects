import { Button } from "@/components/ui/button";
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from "@/components/ui/card";
import { useAuth } from "@/hooks/useAuth";
import { trpc } from "@/lib/trpc";
import { Check, ArrowRight, Download } from "lucide-react";
import { useEffect, useState } from "react";
import { Link, useLocation } from "wouter";

export default function Success() {
  const { user } = useAuth();
  const [, setLocation] = useLocation();
  const [subscriptionId, setSubscriptionId] = useState<string | null>(null);

  useEffect(() => {
    const params = new URLSearchParams(window.location.search);
    const subId = params.get("subscription");
    if (subId) {
      setSubscriptionId(subId);
    }
  }, []);

  const { data: subscription } = trpc.subscriptions.getById.useQuery(
    { id: Number(subscriptionId) },
    { enabled: !!subscriptionId }
  );

  const { data: plan } = trpc.plans.getById.useQuery(
    { id: subscription?.planId || 0 },
    { enabled: !!subscription?.planId }
  );

  if (!subscriptionId) {
    return (
      <div className="min-h-screen bg-gradient-to-br from-blue-50 via-white to-purple-50 dark:from-gray-900 dark:via-gray-800 dark:to-gray-900 flex items-center justify-center p-4">
        <Card className="max-w-md">
          <CardHeader>
            <CardTitle>Invalid Request</CardTitle>
            <CardDescription>No subscription information found.</CardDescription>
          </CardHeader>
          <CardContent>
            <Link href="/pricing">
              <Button className="w-full">View Pricing Plans</Button>
            </Link>
          </CardContent>
        </Card>
      </div>
    );
  }

  return (
    <div className="min-h-screen bg-gradient-to-br from-blue-50 via-white to-purple-50 dark:from-gray-900 dark:via-gray-800 dark:to-gray-900">
      {/* Success Header */}
      <div className="bg-gradient-to-r from-green-600 to-blue-600 text-white py-16">
        <div className="container">
          <div className="max-w-3xl mx-auto text-center">
            <div className="w-20 h-20 bg-white rounded-full flex items-center justify-center mx-auto mb-6">
              <Check className="w-12 h-12 text-green-600" />
            </div>
            <h1 className="text-5xl font-bold mb-4">Payment Successful!</h1>
            <p className="text-xl text-green-100">
              Welcome to Siener AI {plan?.name} Plan
            </p>
          </div>
        </div>
      </div>

      {/* Success Content */}
      <div className="container py-12">
        <div className="max-w-4xl mx-auto">
          {/* Subscription Details */}
          <Card className="glass-card mb-8">
            <CardHeader>
              <CardTitle className="text-2xl">Your Subscription Details</CardTitle>
              <CardDescription>
                Your subscription is now active and ready to use
              </CardDescription>
            </CardHeader>
            <CardContent className="space-y-6">
              {/* Plan Info */}
              <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
                <div>
                  <p className="text-sm text-gray-600 dark:text-gray-400 mb-1">Plan</p>
                  <p className="text-lg font-semibold">{plan?.name}</p>
                </div>
                <div>
                  <p className="text-sm text-gray-600 dark:text-gray-400 mb-1">Status</p>
                  <div className="flex items-center gap-2">
                    <div className="w-2 h-2 bg-green-600 rounded-full" />
                    <p className="text-lg font-semibold text-green-600">Active</p>
                  </div>
                </div>
                <div>
                  <p className="text-sm text-gray-600 dark:text-gray-400 mb-1">Start Date</p>
                  <p className="text-lg font-semibold">
                    {subscription?.startDate
                      ? new Date(subscription.startDate).toLocaleDateString()
                      : "Today"}
                  </p>
                </div>
                <div>
                  <p className="text-sm text-gray-600 dark:text-gray-400 mb-1">Next Billing Date</p>
                  <p className="text-lg font-semibold">
                    {subscription?.endDate
                      ? new Date(subscription.endDate).toLocaleDateString()
                      : "In 30 days"}
                  </p>
                </div>
              </div>

              {/* Features */}
              {plan && (
                <div className="pt-6 border-t border-gray-200 dark:border-gray-700">
                  <h3 className="font-semibold mb-4">Your Plan Includes:</h3>
                  <div className="grid grid-cols-1 md:grid-cols-2 gap-3">
                    {JSON.parse(plan.features).map((feature: string, idx: number) => (
                      <div key={idx} className="flex items-start gap-2">
                        <Check className="w-4 h-4 text-green-600 mt-0.5 flex-shrink-0" />
                        <span className="text-sm">{feature}</span>
                      </div>
                    ))}
                  </div>
                </div>
              )}
            </CardContent>
          </Card>

          {/* Next Steps */}
          <Card className="glass-card mb-8">
            <CardHeader>
              <CardTitle>What's Next?</CardTitle>
              <CardDescription>Get started with your new subscription</CardDescription>
            </CardHeader>
            <CardContent>
              <div className="space-y-4">
                <div className="flex items-start gap-4 p-4 bg-blue-50 dark:bg-blue-900/20 rounded-lg">
                  <div className="w-8 h-8 bg-blue-600 text-white rounded-full flex items-center justify-center flex-shrink-0 font-semibold">
                    1
                  </div>
                  <div>
                    <h4 className="font-semibold mb-1">Explore the Dashboard</h4>
                    <p className="text-sm text-gray-600 dark:text-gray-400">
                      View real-time JSE market data and ECM analysis
                    </p>
                  </div>
                </div>

                <div className="flex items-start gap-4 p-4 bg-blue-50 dark:bg-blue-900/20 rounded-lg">
                  <div className="w-8 h-8 bg-blue-600 text-white rounded-full flex items-center justify-center flex-shrink-0 font-semibold">
                    2
                  </div>
                  <div>
                    <h4 className="font-semibold mb-1">Create Your Watchlist</h4>
                    <p className="text-sm text-gray-600 dark:text-gray-400">
                      Track your favorite JSE stocks and set price alerts
                    </p>
                  </div>
                </div>

                <div className="flex items-start gap-4 p-4 bg-blue-50 dark:bg-blue-900/20 rounded-lg">
                  <div className="w-8 h-8 bg-blue-600 text-white rounded-full flex items-center justify-center flex-shrink-0 font-semibold">
                    3
                  </div>
                  <div>
                    <h4 className="font-semibold mb-1">Analyze Market Trends</h4>
                    <p className="text-sm text-gray-600 dark:text-gray-400">
                      Use ECM insights to make informed trading decisions
                    </p>
                  </div>
                </div>
              </div>
            </CardContent>
          </Card>

          {/* Action Buttons */}
          <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
            <Link href="/">
              <Button className="w-full" size="lg">
                <ArrowRight className="w-5 h-5 mr-2" />
                Go to Dashboard
              </Button>
            </Link>
            <Button variant="outline" className="w-full" size="lg" onClick={() => window.print()}>
              <Download className="w-5 h-5 mr-2" />
              Download Receipt
            </Button>
          </div>

          {/* Support */}
          <div className="mt-8 text-center">
            <p className="text-sm text-gray-600 dark:text-gray-400">
              Need help getting started?{" "}
              <a href="mailto:support@sienerai.com" className="text-blue-600 hover:underline">
                Contact Support
              </a>
            </p>
          </div>
        </div>
      </div>
    </div>
  );
}
