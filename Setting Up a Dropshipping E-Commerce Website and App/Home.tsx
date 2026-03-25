import { useAuth } from "@/_core/hooks/useAuth";
import { Button } from "@/components/ui/button";
import { Card, CardContent } from "@/components/ui/card";
import { Badge } from "@/components/ui/badge";
import { ShoppingCart, Shield, Truck, CreditCard, Star, ArrowRight, Search } from "lucide-react";
import { Link } from "wouter";
import { trpc } from "@/lib/trpc";

export default function Home() {
  const { user, isAuthenticated } = useAuth();
  const { data: featuredProducts, isLoading } = trpc.products.featured.useQuery();
  const { data: cartItems } = trpc.cart.items.useQuery(undefined, {
    enabled: isAuthenticated,
  });

  return (
    <div className="min-h-screen">
      {/* Header/Navigation */}
      <header className="border-b bg-background/95 backdrop-blur supports-[backdrop-filter]:bg-background/60 sticky top-0 z-50">
        <div className="container flex h-16 items-center justify-between">
          <Link href="/" className="flex items-center gap-2">
              <div className="w-10 h-10 rounded-lg bg-primary flex items-center justify-center">
                <Shield className="w-6 h-6 text-primary-foreground" />
              </div>
              <span className="text-xl font-bold">Alpapies</span>
          </Link>
          
          <nav className="hidden md:flex items-center gap-6">
            <Link href="/products" className="text-sm font-medium hover:text-primary transition-colors">Products</Link>
            <Link href="/products?category=iPhone 16" className="text-sm font-medium hover:text-primary transition-colors">iPhone 16</Link>
            <Link href="/products?category=Galaxy S25" className="text-sm font-medium hover:text-primary transition-colors">Galaxy S25</Link>
            <Link href="/about" className="text-sm font-medium hover:text-primary transition-colors">About</Link>
          </nav>

          <div className="flex items-center gap-4">
            <Link href="/search">
              <Button variant="ghost" size="icon">
                <Search className="w-5 h-5" />
              </Button>
            </Link>
            <Link href="/cart">
              <Button variant="ghost" size="icon" className="relative">
                <ShoppingCart className="w-5 h-5" />
                {isAuthenticated && cartItems && cartItems.length > 0 && (
                  <Badge className="absolute -top-1 -right-1 h-5 w-5 flex items-center justify-center p-0 text-xs">
                    {cartItems.length}
                  </Badge>
                )}
              </Button>
            </Link>
            {isAuthenticated ? (
              <Link href="/account"><Button variant="outline">Account</Button></Link>
            ) : (
              <Link href="/login"><Button>Sign In</Button></Link>
            )}
          </div>
        </div>
      </header>

      {/* Hero Section */}
      <section className="relative overflow-hidden bg-gradient-to-br from-primary/10 via-background to-background">
        <div className="container py-20 md:py-32">
          <div className="grid lg:grid-cols-2 gap-12 items-center">
            <div className="space-y-6">
              <Badge variant="secondary" className="w-fit">
                New Arrivals for 2026
              </Badge>
              <h1 className="text-4xl md:text-6xl font-bold tracking-tight">
                Premium Phone Accessories at{" "}
                <span className="text-primary">Unbeatable Prices</span>
              </h1>
              <p className="text-xl text-muted-foreground">
                Direct from manufacturers. iPhone 16 & Galaxy S25 accessories with 30-50% savings compared to retail stores.
              </p>
              <div className="flex flex-wrap gap-4">
                <Link href="/products">
                  <Button size="lg" className="flex items-center gap-2">
                    Shop Now <ArrowRight className="w-4 h-4" />
                  </Button>
                </Link>
                <Link href="/about">
                  <Button size="lg" variant="outline">Learn More</Button>
                </Link>
              </div>
              
              {/* Trust Indicators */}
              <div className="grid grid-cols-3 gap-4 pt-8 border-t">
                <div className="flex items-center gap-2">
                  <Shield className="w-5 h-5 text-primary" />
                  <span className="text-sm font-medium">Secure Checkout</span>
                </div>
                <div className="flex items-center gap-2">
                  <Truck className="w-5 h-5 text-primary" />
                  <span className="text-sm font-medium">Fast Shipping</span>
                </div>
                <div className="flex items-center gap-2">
                  <CreditCard className="w-5 h-5 text-primary" />
                  <span className="text-sm font-medium">Easy Returns</span>
                </div>
              </div>
            </div>

            {/* Hero Image/Visual */}
            <div className="relative">
              <div className="aspect-square rounded-2xl bg-gradient-to-br from-primary/20 to-primary/5 flex items-center justify-center">
                <img 
                  src="https://images.unsplash.com/photo-1601784551446-20c9e07cdbdb?w=600&h=600&fit=crop" 
                  alt="Premium phone accessories"
                  className="w-full h-full object-cover rounded-2xl"
                />
              </div>
              {/* Floating Price Badge */}
              <div className="absolute -bottom-6 -left-6 bg-background border rounded-xl p-4 shadow-lg">
                <div className="text-sm text-muted-foreground">Starting from</div>
                <div className="text-3xl font-bold text-primary">$8.99</div>
                <div className="text-sm text-muted-foreground line-through">$14.99</div>
              </div>
            </div>
          </div>
        </div>
      </section>

      {/* Featured Products */}
      <section className="py-20">
        <div className="container">
          <div className="flex items-center justify-between mb-12">
            <div>
              <h2 className="text-3xl font-bold tracking-tight">Featured Products</h2>
              <p className="text-muted-foreground mt-2">Handpicked accessories for your latest devices</p>
            </div>
            <Link href="/products">
              <Button variant="outline">View All</Button>
            </Link>
          </div>

          {isLoading ? (
            <div className="grid md:grid-cols-2 lg:grid-cols-3 gap-6">
              {[...Array(6)].map((_, i) => (
                <Card key={i} className="overflow-hidden">
                  <div className="aspect-square bg-muted animate-pulse" />
                  <CardContent className="p-6 space-y-3">
                    <div className="h-4 bg-muted animate-pulse rounded" />
                    <div className="h-4 bg-muted animate-pulse rounded w-2/3" />
                  </CardContent>
                </Card>
              ))}
            </div>
          ) : (
            <div className="grid md:grid-cols-2 lg:grid-cols-3 gap-6">
              {featuredProducts?.map((product) => (
                <Link key={product.id} href={`/product/${product.id}`}>
                  <Card className="group overflow-hidden hover:shadow-lg transition-all duration-300 h-full cursor-pointer">
                      <div className="aspect-square overflow-hidden bg-muted">
                        <img 
                          src={product.imageUrl || "https://images.unsplash.com/photo-1601784551446-20c9e07cdbdb?w=400"}
                          alt={product.name}
                          className="w-full h-full object-cover group-hover:scale-105 transition-transform duration-300"
                        />
                      </div>
                      <CardContent className="p-6 space-y-3">
                        <Badge variant="secondary" className="w-fit">{product.category}</Badge>
                        <h3 className="font-semibold text-lg line-clamp-2 group-hover:text-primary transition-colors">
                          {product.name}
                        </h3>
                        <p className="text-sm text-muted-foreground line-clamp-2">
                          {product.description}
                        </p>
                        <div className="flex items-center justify-between pt-2">
                          <div className="flex items-baseline gap-2">
                            <span className="text-2xl font-bold text-primary">
                              ${product.price}
                            </span>
                            {product.compareAtPrice && (
                              <span className="text-sm text-muted-foreground line-through">
                                ${product.compareAtPrice}
                              </span>
                            )}
                          </div>
                          <div className="flex items-center gap-1">
                            <Star className="w-4 h-4 fill-yellow-400 text-yellow-400" />
                            <span className="text-sm font-medium">4.8</span>
                          </div>
                        </div>
                      </CardContent>
                    </Card>
                </Link>
              ))}
            </div>
          )}
        </div>
      </section>

      {/* Categories */}
      <section className="py-20 bg-muted/30">
        <div className="container">
          <h2 className="text-3xl font-bold tracking-tight text-center mb-12">Shop by Device</h2>
          <div className="grid md:grid-cols-3 gap-6">
            <Link href="/products?category=iPhone 16">
                <Card className="group overflow-hidden hover:shadow-lg transition-all duration-300 cursor-pointer">
                  <div className="aspect-video overflow-hidden bg-gradient-to-br from-primary/20 to-primary/5">
                    <img 
                      src="https://images.unsplash.com/photo-1601784551446-20c9e07cdbdb?w=400&h=300&fit=crop"
                      alt="iPhone 16"
                      className="w-full h-full object-cover group-hover:scale-105 transition-transform duration-300"
                    />
                  </div>
                  <CardContent className="p-6">
                    <h3 className="text-xl font-bold mb-2 group-hover:text-primary transition-colors">iPhone 16 Accessories</h3>
                    <p className="text-muted-foreground">Cases, chargers, screen protectors & more</p>
                  </CardContent>
                </Card>
            </Link>

            <Link href="/products?category=Galaxy S25">
                <Card className="group overflow-hidden hover:shadow-lg transition-all duration-300 cursor-pointer">
                  <div className="aspect-video overflow-hidden bg-gradient-to-br from-primary/20 to-primary/5">
                    <img 
                      src="https://images.unsplash.com/photo-1598327105666-5b89351aff97?w=400&h=300&fit=crop"
                      alt="Galaxy S25"
                      className="w-full h-full object-cover group-hover:scale-105 transition-transform duration-300"
                    />
                  </div>
                  <CardContent className="p-6">
                    <h3 className="text-xl font-bold mb-2 group-hover:text-primary transition-colors">Galaxy S25 Accessories</h3>
                    <p className="text-muted-foreground">Premium accessories for Samsung flagship</p>
                  </CardContent>
                </Card>
            </Link>

            <Link href="/products?category=Universal">
                <Card className="group overflow-hidden hover:shadow-lg transition-all duration-300 cursor-pointer">
                  <div className="aspect-video overflow-hidden bg-gradient-to-br from-primary/20 to-primary/5">
                    <img 
                      src="https://images.unsplash.com/photo-1591290619762-c588f7e4e86b?w=400&h=300&fit=crop"
                      alt="Universal"
                      className="w-full h-full object-cover group-hover:scale-105 transition-transform duration-300"
                    />
                  </div>
                  <CardContent className="p-6">
                    <h3 className="text-xl font-bold mb-2 group-hover:text-primary transition-colors">Universal Accessories</h3>
                    <p className="text-muted-foreground">Works with all phones and devices</p>
                  </CardContent>
                </Card>
            </Link>
          </div>
        </div>
      </section>

      {/* Value Proposition */}
      <section className="py-20">
        <div className="container">
          <div className="grid md:grid-cols-2 lg:grid-cols-4 gap-8">
            <div className="text-center space-y-3">
              <div className="w-12 h-12 rounded-full bg-primary/10 flex items-center justify-center mx-auto">
                <Shield className="w-6 h-6 text-primary" />
              </div>
              <h3 className="font-semibold">Quality Guaranteed</h3>
              <p className="text-sm text-muted-foreground">All products tested for durability and performance</p>
            </div>
            <div className="text-center space-y-3">
              <div className="w-12 h-12 rounded-full bg-primary/10 flex items-center justify-center mx-auto">
                <Truck className="w-6 h-6 text-primary" />
              </div>
              <h3 className="font-semibold">Fast Shipping</h3>
              <p className="text-sm text-muted-foreground">Free shipping on orders over $50</p>
            </div>
            <div className="text-center space-y-3">
              <div className="w-12 h-12 rounded-full bg-primary/10 flex items-center justify-center mx-auto">
                <CreditCard className="w-6 h-6 text-primary" />
              </div>
              <h3 className="font-semibold">Secure Payment</h3>
              <p className="text-sm text-muted-foreground">Your payment information is always protected</p>
            </div>
            <div className="text-center space-y-3">
              <div className="w-12 h-12 rounded-full bg-primary/10 flex items-center justify-center mx-auto">
                <Star className="w-6 h-6 text-primary" />
              </div>
              <h3 className="font-semibold">Top Rated</h3>
              <p className="text-sm text-muted-foreground">4.8/5 average rating from 10,000+ customers</p>
            </div>
          </div>
        </div>
      </section>

      {/* Footer */}
      <footer className="border-t bg-muted/30 py-12">
        <div className="container">
          <div className="grid md:grid-cols-4 gap-8">
            <div className="space-y-4">
              <div className="flex items-center gap-2">
                <div className="w-8 h-8 rounded-lg bg-primary flex items-center justify-center">
                  <Shield className="w-5 h-5 text-primary-foreground" />
                </div>
                <span className="font-bold">Alpapies</span>
              </div>
              <p className="text-sm text-muted-foreground">
                Premium phone accessories at unbeatable prices. Direct from manufacturers.
              </p>
            </div>
            <div>
              <h4 className="font-semibold mb-4">Shop</h4>
              <ul className="space-y-2 text-sm text-muted-foreground">
                <li><Link href="/products" className="hover:text-foreground transition-colors">All Products</Link></li>
                <li><Link href="/products?category=iPhone 16" className="hover:text-foreground transition-colors">iPhone 16</Link></li>
                <li><Link href="/products?category=Galaxy S25" className="hover:text-foreground transition-colors">Galaxy S25</Link></li>
                <li><Link href="/products?category=Universal" className="hover:text-foreground transition-colors">Universal</Link></li>
              </ul>
            </div>
            <div>
              <h4 className="font-semibold mb-4">Support</h4>
              <ul className="space-y-2 text-sm text-muted-foreground">
                <li><Link href="/contact" className="hover:text-foreground transition-colors">Contact Us</Link></li>
                <li><Link href="/shipping" className="hover:text-foreground transition-colors">Shipping Info</Link></li>
                <li><Link href="/returns" className="hover:text-foreground transition-colors">Returns</Link></li>
                <li><Link href="/faq" className="hover:text-foreground transition-colors">FAQ</Link></li>
              </ul>
            </div>
            <div>
              <h4 className="font-semibold mb-4">Company</h4>
              <ul className="space-y-2 text-sm text-muted-foreground">
                <li><Link href="/about" className="hover:text-foreground transition-colors">About Us</Link></li>
                <li><Link href="/privacy" className="hover:text-foreground transition-colors">Privacy Policy</Link></li>
                <li><Link href="/terms" className="hover:text-foreground transition-colors">Terms of Service</Link></li>
              </ul>
            </div>
          </div>
          <div className="border-t mt-8 pt-8 text-center text-sm text-muted-foreground">
            <p>© 2026 Alpapies. All rights reserved.</p>
          </div>
        </div>
      </footer>
    </div>
  );
}
