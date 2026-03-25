import { Button } from "@/components/ui/button";
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from "@/components/ui/card";
import { useAuth } from "@/hooks/useAuth";
import { trpc } from "@/lib/trpc";
import { ArrowLeft, Check, CreditCard, Lock } from "lucide-react";
import { useEffect, useState } from "react";
import { Link, useLocation } from "wouter";

export default function Checkout() {
  const { user, isLoading: authLoading } = useAuth();
  const [, setLocation] = useLocation();
  const [selectedPlanId, setSelectedPlanId] = useState<string | null>(null);
  const [isProcessing, setIsProcessing] = useState(false);

  // Get plan ID from URL params
  useEffect(() => {
    const params = new URLSearchParams(window.location.search);
    const planId = params.get("plan");
    if (planId) {
      setSelectedPlanId(planId);
    }
  }, []);

  // Redirect to login if not authenticated
  useEffect(() => {
    if (!authLoading && !user) {
      const returnTo = `/checkout${window.location.search}`;
      setLocation(`/login?returnTo=${encodeURIComponent(returnTo)}`);
    }
  }, [user, authLoading, setLocation]);

  const { data: plans } = trpc.plans.list.useQuery();
  const createPayment = trpc.payments.createPayment.useMutation();

  const selectedPlan = plans?.find((p) => p.id === Number(selectedPlanId));

  const handlePayment = async () => {
    if (!selectedPlan) return;

    setIsProcessing(true);
    try {
      const result = await createPayment.mutateAsync({
        planId: selectedPlan.id,
        amount: parseFloat(selectedPlan.priceRands),
      });

      // Redirect to Yoco payment page
      if (result.checkoutUrl) {
        window.location.href = result.checkoutUrl;
      }
    } catch (error) {
      console.error("Payment error:", error);
      setIsProcessing(false);
    }
  };

  if (authLoading) {
    return (
      <div className="min-h-screen bg-gradient-to-br from-blue-50 via-white to-purple-50 dark:from-gray-900 dark:via-gray-800 dark:to-gray-900 flex items-center justify-center">
        <div className="text-center">
          <div className="w-16 h-16 border-4 border-blue-600 border-t-transparent rounded-full animate-spin mx-auto mb-4" />
          <p className="text-lg text-gray-600 dark:text-gray-300">Loading...</p>
        </div>
      </div>
    );
  }

  if (!selectedPlan) {
    return (
      <div className="min-h-screen bg-gradient-to-br from-blue-50 via-white to-purple-50 dark:from-gray-900 dark:via-gray-800 dark:to-gray-900 flex items-center justify-center p-4">
        <Card className="max-w-md">
          <CardHeader>
            <CardTitle>No Plan Selected</CardTitle>
            <CardDescription>Please select a subscription plan to continue.</CardDescription>
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

  const features = JSON.parse(selectedPlan.features);

  return (
    <div className="min-h-screen bg-gradient-to-br from-blue-50 via-white to-purple-50 dark:from-gray-900 dark:via-gray-800 dark:to-gray-900">
      {/* Header */}
      <div className="bg-gradient-to-r from-blue-600 to-purple-600 text-white py-8">
        <div className="container">
          <Link href="/pricing">
            <Button variant="ghost" className="text-white hover:bg-white/20 mb-4">
              <ArrowLeft className="w-4 h-4 mr-2" />
              Back to Pricing
            </Button>
          </Link>
          <h1 className="text-3xl font-bold">Complete Your Purchase</h1>
          <p className="text-blue-100 mt-2">Secure checkout powered by Yoco</p>
        </div>
      </div>

      {/* Checkout Content */}
      <div className="container py-12">
        <div className="max-w-4xl mx-auto grid grid-cols-1 lg:grid-cols-2 gap-8">
          {/* Order Summary */}
          <div>
            <h2 className="text-2xl font-bold mb-6">Order Summary</h2>
            <Card className="glass-card">
              <CardHeader>
                <CardTitle className="text-2xl">{selectedPlan.name}</CardTitle>
                <CardDescription>{selectedPlan.description}</CardDescription>
              </CardHeader>
              <CardContent className="space-y-6">
                {/* Price */}
                <div className="pb-6 border-b border-gray-200 dark:border-gray-700">
                  <div className="flex items-baseline justify-between">
                    <span className="text-gray-600 dark:text-gray-400">Subscription</span>
                    <div className="text-right">
                      <div className="text-3xl font-bold text-blue-600">
                        R{parseFloat(selectedPlan.priceRands).toFixed(0)}
                      </div>
                      <div className="text-sm text-gray-600 dark:text-gray-400">per month</div>
                    </div>
                  </div>
                </div>

                {/* Features */}
                <div>
                  <h3 className="font-semibold mb-3">What's included:</h3>
                  <ul className="space-y-2">
                    {features.map((feature: string, idx: number) => (
                      <li key={idx} className="flex items-start gap-2 text-sm">
                        <Check className="w-4 h-4 text-green-600 mt-0.5 flex-shrink-0" />
                        <span>{feature}</span>
                      </li>
                    ))}
                  </ul>
                </div>

                {/* Plan Details */}
                <div className="pt-6 border-t border-gray-200 dark:border-gray-700">
                  <div className="grid grid-cols-2 gap-4 text-sm">
                    <div>
                      <p className="text-gray-600 dark:text-gray-400">Max Stocks</p>
                      <p className="font-semibold">
                        {selectedPlan.maxStocks === 999999 ? "Unlimited" : selectedPlan.maxStocks}
                      </p>
                    </div>
                    <div>
                      <p className="text-gray-600 dark:text-gray-400">Price Alerts</p>
                      <p className="font-semibold">
                        {selectedPlan.maxAlerts === 999999 ? "Unlimited" : selectedPlan.maxAlerts}
                      </p>
                    </div>
                  </div>
                </div>

                {/* Total */}
                <div className="pt-6 border-t border-gray-200 dark:border-gray-700">
                  <div className="flex items-center justify-between text-lg font-bold">
                    <span>Total due today</span>
                    <span className="text-blue-600">
                      R{parseFloat(selectedPlan.priceRands).toFixed(2)}
                    </span>
                  </div>
                  <p className="text-sm text-gray-600 dark:text-gray-400 mt-2">
                    Billed monthly • Cancel anytime
                  </p>
                </div>
              </CardContent>
            </Card>
          </div>

          {/* Payment Section */}
          <div>
            <h2 className="text-2xl font-bold mb-6">Payment Details</h2>
            <Card className="glass-card">
              <CardHeader>
                <div className="flex items-center gap-3">
                  <div className="w-12 h-12 bg-blue-100 dark:bg-blue-900 rounded-lg flex items-center justify-center">
                    <CreditCard className="w-6 h-6 text-blue-600" />
                  </div>
                  <div>
                    <CardTitle>Secure Payment</CardTitle>
                    <CardDescription>Powered by Yoco</CardDescription>
                  </div>
                </div>
              </CardHeader>
              <CardContent className="space-y-6">
                {/* Account Info */}
                <div className="p-4 bg-gray-50 dark:bg-gray-800 rounded-lg">
                  <p className="text-sm text-gray-600 dark:text-gray-400 mb-1">Signed in as:</p>
                  <p className="font-semibold">{user?.name}</p>
                  <p className="text-sm text-gray-600 dark:text-gray-400">{user?.email}</p>
                </div>

                {/* Payment Method Info */}
                <div className="space-y-4">
                  <h3 className="font-semibold">Accepted Payment Methods</h3>
                  <div className="grid grid-cols-2 gap-3">
                    <div className="p-3 border border-gray-200 dark:border-gray-700 rounded-lg text-center">
                      <p className="text-sm font-medium">Credit Card</p>
                      <p className="text-xs text-gray-600 dark:text-gray-400">Visa, Mastercard</p>
                    </div>
                    <div className="p-3 border border-gray-200 dark:border-gray-700 rounded-lg text-center">
                      <p className="text-sm font-medium">Debit Card</p>
                      <p className="text-xs text-gray-600 dark:text-gray-400">All major banks</p>
                    </div>
                    <div className="p-3 border border-gray-200 dark:border-gray-700 rounded-lg text-center col-span-2">
                      <p className="text-sm font-medium">Instant EFT</p>
                      <p className="text-xs text-gray-600 dark:text-gray-400">Direct bank transfer</p>
                    </div>
                  </div>
                </div>

                {/* Security Notice */}
                <div className="flex items-start gap-3 p-4 bg-green-50 dark:bg-green-900/20 rounded-lg">
                  <Lock className="w-5 h-5 text-green-600 mt-0.5 flex-shrink-0" />
                  <div className="text-sm">
                    <p className="font-semibold text-green-900 dark:text-green-100">
                      Secure Payment
                    </p>
                    <p className="text-green-700 dark:text-green-300">
                      Your payment information is encrypted and secure. We never store your card
                      details.
                    </p>
                  </div>
                </div>

                {/* Payment Button */}
                <Button
                  onClick={handlePayment}
                  disabled={isProcessing}
                  className="w-full"
                  size="lg"
                >
                  {isProcessing ? (
                    <>
                      <div className="w-5 h-5 border-2 border-white border-t-transparent rounded-full animate-spin mr-2" />
                      Processing...
                    </>
                  ) : (
                    <>
                      <CreditCard className="w-5 h-5 mr-2" />
                      Proceed to Payment
                    </>
                  )}
                </Button>

                <p className="text-xs text-center text-gray-600 dark:text-gray-400">
                  By completing this purchase, you agree to our Terms of Service and Privacy
                  Policy. You can cancel your subscription at any time.
                </p>
              </CardContent>
            </Card>
          </div>
        </div>
      </div>
    </div>
  );
}
