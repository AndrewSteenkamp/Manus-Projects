import { useAuth } from "@/_core/hooks/useAuth";
import { Button } from "@/components/ui/button";
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from "@/components/ui/card";
import { APP_TITLE, getLoginUrl } from "@/const";
import { Wrench, Zap, Hammer, Wind, Sun, Shield, Star, Users } from "lucide-react";
import { Link } from "wouter";

export default function Home() {
  const { user, isAuthenticated } = useAuth();

  return (
    <div className="min-h-screen">
      {/* Header */}
      <header className="border-b bg-white/50 backdrop-blur-sm sticky top-0 z-50">
        <div className="container flex h-16 items-center justify-between">
          <div className="flex items-center gap-2">
            <div className="w-8 h-8 rounded-lg bg-primary flex items-center justify-center text-white font-bold">
              SHS
            </div>
            <span className="font-semibold text-lg">{APP_TITLE}</span>
          </div>
          
          <nav className="flex items-center gap-4">
            {isAuthenticated ? (
              <>
                <Link href="/dashboard">
                  <Button variant="ghost">Dashboard</Button>
                </Link>
                <span className="text-sm text-muted-foreground">
                  {user?.name || user?.email}
                </span>
              </>
            ) : (
              <>
                <Button variant="ghost" asChild>
                  <a href={getLoginUrl()}>Sign In</a>
                </Button>
                <Button asChild>
                  <a href={getLoginUrl()}>Get Started</a>
                </Button>
              </>
            )}
          </nav>
        </div>
      </header>

      {/* Hero Section */}
      <section className="py-20 bg-gradient-to-b from-blue-50 to-white">
        <div className="container">
          <div className="max-w-3xl mx-auto text-center">
            <h1 className="text-5xl font-bold tracking-tight mb-6">
              Find Trusted Home Service Professionals
            </h1>
            <p className="text-xl text-muted-foreground mb-8">
              Connect with vetted, qualified service providers for plumbing, electrical, HVAC, solar installation, and more. Get competitive quotes and book with confidence.
            </p>
            <div className="flex gap-4 justify-center">
              <Button size="lg" asChild>
                <a href={getLoginUrl()}>Post a Service Request</a>
              </Button>
              <Button size="lg" variant="outline" asChild>
                <a href={getLoginUrl()}>Become a Provider</a>
              </Button>
            </div>
          </div>
        </div>
      </section>

      {/* Service Categories */}
      <section className="py-16">
        <div className="container">
          <h2 className="text-3xl font-bold text-center mb-12">Popular Services</h2>
          <div className="grid grid-cols-1 md:grid-cols-3 lg:grid-cols-5 gap-6">
            {[
              { icon: Wrench, name: "Plumbing", color: "text-blue-600" },
              { icon: Zap, name: "Electrical", color: "text-yellow-600" },
              { icon: Hammer, name: "Handyman", color: "text-orange-600" },
              { icon: Wind, name: "HVAC", color: "text-cyan-600" },
              { icon: Sun, name: "Solar", color: "text-amber-600" },
            ].map((service) => (
              <Card key={service.name} className="text-center hover:shadow-lg transition-shadow cursor-pointer">
                <CardHeader>
                  <service.icon className={`w-12 h-12 mx-auto ${service.color}`} />
                  <CardTitle className="text-lg">{service.name}</CardTitle>
                </CardHeader>
              </Card>
            ))}
          </div>
        </div>
      </section>

      {/* How It Works */}
      <section className="py-16 bg-gray-50">
        <div className="container">
          <h2 className="text-3xl font-bold text-center mb-12">How It Works</h2>
          <div className="grid grid-cols-1 md:grid-cols-3 gap-8 max-w-5xl mx-auto">
            <div className="text-center">
              <div className="w-16 h-16 rounded-full bg-primary text-white flex items-center justify-center text-2xl font-bold mx-auto mb-4">
                1
              </div>
              <h3 className="text-xl font-semibold mb-2">Post Your Request</h3>
              <p className="text-muted-foreground">
                Describe your service need with photos and location details
              </p>
            </div>
            <div className="text-center">
              <div className="w-16 h-16 rounded-full bg-primary text-white flex items-center justify-center text-2xl font-bold mx-auto mb-4">
                2
              </div>
              <h3 className="text-xl font-semibold mb-2">Compare Quotes</h3>
              <p className="text-muted-foreground">
                Receive competitive bids from verified service providers
              </p>
            </div>
            <div className="text-center">
              <div className="w-16 h-16 rounded-full bg-primary text-white flex items-center justify-center text-2xl font-bold mx-auto mb-4">
                3
              </div>
              <h3 className="text-xl font-semibold mb-2">Book & Pay Securely</h3>
              <p className="text-muted-foreground">
                Choose your provider and pay securely through our platform
              </p>
            </div>
          </div>
        </div>
      </section>

      {/* Trust Indicators */}
      <section className="py-16">
        <div className="container">
          <div className="grid grid-cols-1 md:grid-cols-3 gap-8 max-w-4xl mx-auto">
            <Card>
              <CardHeader>
                <Shield className="w-10 h-10 text-primary mb-2" />
                <CardTitle>Verified Providers</CardTitle>
                <CardDescription>
                  All providers undergo background checks and qualification verification
                </CardDescription>
              </CardHeader>
            </Card>
            <Card>
              <CardHeader>
                <Star className="w-10 h-10 text-primary mb-2" />
                <CardTitle>Rated & Reviewed</CardTitle>
                <CardDescription>
                  Read real reviews from customers to make informed decisions
                </CardDescription>
              </CardHeader>
            </Card>
            <Card>
              <CardHeader>
                <Users className="w-10 h-10 text-primary mb-2" />
                <CardTitle>Secure Payments</CardTitle>
                <CardDescription>
                  Payments held in escrow until job completion for your protection
                </CardDescription>
              </CardHeader>
            </Card>
          </div>
        </div>
      </section>

      {/* CTA Section */}
      <section className="py-20 bg-primary text-white">
        <div className="container text-center">
          <h2 className="text-4xl font-bold mb-6">Ready to Get Started?</h2>
          <p className="text-xl mb-8 text-blue-100">
            Join thousands of satisfied customers finding trusted service providers
          </p>
          <Button size="lg" variant="secondary" asChild>
            <a href={getLoginUrl()}>Create Free Account</a>
          </Button>
        </div>
      </section>

      {/* Footer */}
      <footer className="py-12 border-t bg-gray-50">
        <div className="container">
          <div className="grid grid-cols-1 md:grid-cols-4 gap-8">
            <div>
              <div className="flex items-center gap-2 mb-4">
                <div className="w-8 h-8 rounded-lg bg-primary flex items-center justify-center text-white font-bold">
                  SHS
                </div>
                <span className="font-semibold">{APP_TITLE}</span>
              </div>
              <p className="text-sm text-muted-foreground">
                Connecting homeowners with trusted service professionals across South Africa
              </p>
            </div>
            <div>
              <h4 className="font-semibold mb-4">For Customers</h4>
              <ul className="space-y-2 text-sm text-muted-foreground">
                <li><a href="#" className="hover:text-foreground">Post a Request</a></li>
                <li><a href="#" className="hover:text-foreground">Browse Services</a></li>
                <li><a href="#" className="hover:text-foreground">How It Works</a></li>
              </ul>
            </div>
            <div>
              <h4 className="font-semibold mb-4">For Providers</h4>
              <ul className="space-y-2 text-sm text-muted-foreground">
                <li><a href="#" className="hover:text-foreground">Become a Provider</a></li>
                <li><a href="#" className="hover:text-foreground">Pricing</a></li>
                <li><a href="#" className="hover:text-foreground">Resources</a></li>
              </ul>
            </div>
            <div>
              <h4 className="font-semibold mb-4">Company</h4>
              <ul className="space-y-2 text-sm text-muted-foreground">
                <li><a href="#" className="hover:text-foreground">About Us</a></li>
                <li><a href="#" className="hover:text-foreground">Contact</a></li>
                <li><a href="#" className="hover:text-foreground">Terms of Service</a></li>
                <li><a href="#" className="hover:text-foreground">Privacy Policy</a></li>
              </ul>
            </div>
          </div>
          <div className="mt-8 pt-8 border-t text-center text-sm text-muted-foreground">
            © 2025 {APP_TITLE}. All rights reserved.
          </div>
        </div>
      </footer>
    </div>
  );
}
