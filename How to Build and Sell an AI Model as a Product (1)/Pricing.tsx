import { trpc } from "@/lib/trpc";
import { Button } from "@/components/ui/button";
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from "@/components/ui/card";
import { Check, ArrowLeft } from "lucide-react";
import { Link } from "wouter";

export default function Pricing() {
  const { data: plans, isLoading } = trpc.plans.list.useQuery();

  if (isLoading) {
    return (
      <div className="min-h-screen bg-gradient-to-br from-blue-50 via-white to-purple-50 dark:from-gray-900 dark:via-gray-800 dark:to-gray-900 flex items-center justify-center">
        <div className="text-center">
          <div className="w-16 h-16 border-4 border-blue-600 border-t-transparent rounded-full animate-spin mx-auto mb-4" />
          <p className="text-lg text-gray-600 dark:text-gray-300">Loading pricing plans...</p>
        </div>
      </div>
    );
  }

  return (
    <div className="min-h-screen bg-gradient-to-br from-blue-50 via-white to-purple-50 dark:from-gray-900 dark:via-gray-800 dark:to-gray-900">
      {/* Header */}
      <div className="bg-gradient-to-r from-blue-600 to-purple-600 text-white py-16">
        <div className="container">
          <Link href="/">
            <Button variant="ghost" className="text-white hover:bg-white/20 mb-6">
              <ArrowLeft className="w-4 h-4 mr-2" />
              Back to Dashboard
            </Button>
          </Link>
          <div className="max-w-4xl mx-auto text-center">
            <h1 className="text-5xl font-bold mb-4">Choose Your Plan</h1>
            <p className="text-xl mb-2">
              Get access to advanced JSE market analysis and exclusive features
            </p>
            <p className="text-blue-100">
              All plans include real-time data, ECM analysis, and sector performance tracking
            </p>
          </div>
        </div>
      </div>

      {/* Pricing Cards */}
      <div className="container py-16">
        <div className="grid grid-cols-1 md:grid-cols-3 gap-8 max-w-6xl mx-auto">
          {plans?.map((plan, index) => {
            const features = JSON.parse(plan.features);
            const isPopular = index === 1; // Middle plan is popular

            return (
              <Card
                key={plan.id}
                className={`glass-card hover:shadow-2xl transition-all relative ${
                  isPopular ? "border-2 border-blue-600 scale-105" : ""
                }`}
              >
                {isPopular && (
                  <div className="absolute -top-4 left-1/2 -translate-x-1/2 bg-blue-600 text-white px-4 py-1 rounded-full text-sm font-semibold">
                    Most Popular
                  </div>
                )}
                <CardHeader className="text-center pb-8">
                  <CardTitle className="text-3xl mb-2">{plan.name}</CardTitle>
                  <CardDescription className="text-base">{plan.description}</CardDescription>
                </CardHeader>
                <CardContent>
                  {/* Price */}
                  <div className="text-center mb-8 pb-8 border-b border-gray-200 dark:border-gray-700">
                    <div className="flex items-baseline justify-center gap-2">
                      <span className="text-5xl font-bold text-blue-600">
                        R{parseFloat(plan.priceRands).toFixed(0)}
                      </span>
                      <span className="text-gray-600 dark:text-gray-400">/month</span>
                    </div>
                    <p className="text-sm text-gray-500 dark:text-gray-400 mt-2">
                      Billed monthly • Cancel anytime
                    </p>
                  </div>

                  {/* Features */}
                  <ul className="space-y-4 mb-8">
                    {features.map((feature: string, idx: number) => (
                      <li key={idx} className="flex items-start gap-3">
                        <div className="w-5 h-5 rounded-full bg-green-100 dark:bg-green-900 flex items-center justify-center flex-shrink-0 mt-0.5">
                          <Check className="w-3 h-3 text-green-600 dark:text-green-400" />
                        </div>
                        <span className="text-sm text-gray-700 dark:text-gray-300">{feature}</span>
                      </li>
                    ))}
                  </ul>

                  {/* CTA Button */}
                  <Link href={`/checkout?plan=${plan.id}`}>
                    <Button
                      className="w-full"
                      size="lg"
                      variant={isPopular ? "default" : "outline"}
                    >
                      Get Started
                    </Button>
                  </Link>

                  {/* Plan Details */}
                  <div className="mt-6 pt-6 border-t border-gray-200 dark:border-gray-700">
                    <div className="grid grid-cols-2 gap-4 text-sm">
                      <div>
                        <p className="text-gray-600 dark:text-gray-400">Max Stocks</p>
                        <p className="font-semibold">
                          {plan.maxStocks === 999999 ? "Unlimited" : plan.maxStocks}
                        </p>
                      </div>
                      <div>
                        <p className="text-gray-600 dark:text-gray-400">Price Alerts</p>
                        <p className="font-semibold">
                          {plan.maxAlerts === 999999 ? "Unlimited" : plan.maxAlerts}
                        </p>
                      </div>
                      <div>
                        <p className="text-gray-600 dark:text-gray-400">Analytics</p>
                        <p className="font-semibold">
                          {plan.advancedAnalytics ? "Advanced" : "Basic"}
                        </p>
                      </div>
                      <div>
                        <p className="text-gray-600 dark:text-gray-400">API Access</p>
                        <p className="font-semibold">{plan.apiAccess ? "Yes" : "No"}</p>
                      </div>
                    </div>
                  </div>
                </CardContent>
              </Card>
            );
          })}
        </div>

        {/* FAQ Section */}
        <div className="max-w-4xl mx-auto mt-20">
          <h2 className="text-3xl font-bold text-center mb-12">Frequently Asked Questions</h2>
          <div className="grid grid-cols-1 md:grid-cols-2 gap-8">
            <div>
              <h3 className="font-semibold text-lg mb-2">Can I change plans later?</h3>
              <p className="text-gray-600 dark:text-gray-400">
                Yes! You can upgrade or downgrade your plan at any time. Changes take effect
                immediately.
              </p>
            </div>
            <div>
              <h3 className="font-semibold text-lg mb-2">What payment methods do you accept?</h3>
              <p className="text-gray-600 dark:text-gray-400">
                We accept all major South African payment methods through Yoco, including credit
                cards, debit cards, and instant EFT.
              </p>
            </div>
            <div>
              <h3 className="font-semibold text-lg mb-2">Is there a free trial?</h3>
              <p className="text-gray-600 dark:text-gray-400">
                Currently we don't offer a free trial, but you can cancel your subscription at any
                time with no penalties.
              </p>
            </div>
            <div>
              <h3 className="font-semibold text-lg mb-2">How accurate is the ECM analysis?</h3>
              <p className="text-gray-600 dark:text-gray-400">
                Our ECM analysis is based on Martin Armstrong's proven methodology with real-time
                JSE data, updated every 30 seconds.
              </p>
            </div>
          </div>
        </div>

        {/* Trust Badges */}
        <div className="max-w-4xl mx-auto mt-16 text-center">
          <p className="text-sm text-gray-600 dark:text-gray-400 mb-4">Trusted by South African traders</p>
          <div className="flex items-center justify-center gap-8 text-gray-400">
            <div className="flex items-center gap-2">
              <Check className="w-5 h-5 text-green-600" />
              <span>Secure Payments</span>
            </div>
            <div className="flex items-center gap-2">
              <Check className="w-5 h-5 text-green-600" />
              <span>Real-time Data</span>
            </div>
            <div className="flex items-center gap-2">
              <Check className="w-5 h-5 text-green-600" />
              <span>Cancel Anytime</span>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
}
