import React, { useState } from 'react'
import { Button } from '@/components/ui/button.jsx'
import { Card, CardContent, CardDescription, CardFooter, CardHeader, CardTitle } from '@/components/ui/card.jsx'
import { Badge } from '@/components/ui/badge.jsx'
import { Input } from '@/components/ui/input.jsx'
import { Tabs, TabsContent, TabsList, TabsTrigger } from '@/components/ui/tabs.jsx'
import { 
  ShoppingCart, 
  Search, 
  Menu, 
  Star, 
  Shield, 
  Truck, 
  CheckCircle, 
  Phone,
  Smartphone,
  Zap,
  Battery,
  Car,
  Headphones,
  Heart,
  User,
  ArrowRight,
  Package,
  Globe,
  Award,
  Clock,
  TrendingDown,
  DollarSign,
  Percent,
  Trophy,
  X
} from 'lucide-react'
import logoImage from './assets/alpapies_multicategory_logo_1.png'
import PriceComparison from './PriceComparison.jsx'
import './App.css'

// Sample product data based on our 1688.com research
const featuredProducts = [
  {
    id: 1,
    name: "iPhone 16 Pro Premium Shield Case",
    price: 24.99,
    originalPrice: 39.99,
    image: "/api/placeholder/300/300",
    rating: 4.8,
    reviews: 127,
    category: "iPhone 16 Series",
    badge: "New Release",
    features: ["Camera Control Compatible", "MagSafe Ready", "Drop Protection"],
    supplier: "1688.com via ZQ Dropshipping"
  },
  {
    id: 2,
    name: "Samsung Galaxy S25 Ultra Wireless Charger",
    price: 29.99,
    originalPrice: 49.99,
    image: "/api/placeholder/300/300",
    rating: 4.9,
    reviews: 89,
    category: "Wireless Chargers",
    badge: "Best Seller",
    features: ["15W Fast Charging", "Qi Compatible", "LED Indicator"],
    supplier: "1688.com via ZQ Dropshipping"
  },
  {
    id: 3,
    name: "Universal Tempered Glass Screen Protector",
    price: 12.99,
    originalPrice: 24.99,
    image: "/api/placeholder/300/300",
    rating: 4.7,
    reviews: 203,
    category: "Screen Protectors",
    badge: "80% Off",
    features: ["9H Hardness", "Bubble-Free", "Easy Install"],
    supplier: "1688.com via ZQ Dropshipping"
  },
  {
    id: 4,
    name: "20000mAh Fast Charging Power Bank",
    price: 34.99,
    originalPrice: 59.99,
    image: "/api/placeholder/300/300",
    rating: 4.6,
    reviews: 156,
    category: "Power Banks",
    badge: "High Capacity",
    features: ["USB-C PD", "Wireless Charging", "Digital Display"],
    supplier: "1688.com via ZQ Dropshipping"
  },
  {
    id: 5,
    name: "Magnetic Car Mount with Wireless Charging",
    price: 19.99,
    originalPrice: 34.99,
    image: "/api/placeholder/300/300",
    rating: 4.5,
    reviews: 94,
    category: "Car Accessories",
    badge: "Smart Choice",
    features: ["360° Rotation", "One-Hand Operation", "Strong Magnet"],
    supplier: "1688.com via ZQ Dropshipping"
  },
  {
    id: 6,
    name: "Premium Bluetooth Earbuds",
    price: 39.99,
    originalPrice: 79.99,
    image: "/api/placeholder/300/300",
    rating: 4.8,
    reviews: 178,
    category: "Audio Accessories",
    badge: "Premium",
    features: ["ANC Technology", "30H Battery", "IPX7 Waterproof"],
    supplier: "1688.com via ZQ Dropshipping"
  }
]

const categories = [
  { name: "iPhone 16 Series", count: 45, icon: <Smartphone className="h-6 w-6" /> },
  { name: "Samsung Galaxy S25", count: 38, icon: <Phone className="h-6 w-6" /> },
  { name: "Wireless Chargers", count: 67, icon: <Zap className="h-6 w-6" /> },
  { name: "Power Banks", count: 29, icon: <Battery className="h-6 w-6" /> },
  { name: "Car Accessories", count: 23, icon: <Car className="h-6 w-6" /> },
  { name: "Audio Accessories", count: 34, icon: <Headphones className="h-6 w-6" /> }
]

function App() {
  const [cartItems, setCartItems] = useState([])
  const [searchQuery, setSearchQuery] = useState('')
  const [mobileMenuOpen, setMobileMenuOpen] = useState(false)
  const [selectedProduct, setSelectedProduct] = useState(null)
  const [showPriceComparison, setShowPriceComparison] = useState(false)

  const addToCart = (product) => {
    setCartItems(prev => {
      const existing = prev.find(item => item.id === product.id)
      if (existing) {
        return prev.map(item => 
          item.id === product.id 
            ? { ...item, quantity: item.quantity + 1 }
            : item
        )
      }
      return [...prev, { ...product, quantity: 1 }]
    })
  }

  const showProductComparison = (product) => {
    setSelectedProduct(product)
    setShowPriceComparison(true)
  }

  const calculateDiscount = (original, current) => {
    return Math.round(((original - current) / original) * 100)
  }

  return (
    <div className="min-h-screen bg-background">
      {/* Header */}
      <header className="sticky top-0 z-50 w-full border-b bg-background/95 backdrop-blur supports-[backdrop-filter]:bg-background/60">
        <div className="container mx-auto px-4">
          <div className="flex h-16 items-center justify-between">
            <div className="flex items-center space-x-4">
              <img src={logoImage} alt="Alpapies" className="h-8 w-8" />
              <span className="text-xl font-bold text-primary">Alpapies</span>
            </div>
            
            {/* Desktop Navigation */}
            <nav className="hidden md:flex items-center space-x-6">
              <a href="#home" className="text-sm font-medium hover:text-primary transition-colors">Home</a>
              <a href="#shop" className="text-sm font-medium hover:text-primary transition-colors">Shop</a>
              <a href="#categories" className="text-sm font-medium hover:text-primary transition-colors">Categories</a>
              <a href="#price-comparison" className="text-sm font-medium hover:text-primary transition-colors">Price Compare</a>
              <a href="#about" className="text-sm font-medium hover:text-primary transition-colors">About</a>
              <a href="#contact" className="text-sm font-medium hover:text-primary transition-colors">Contact</a>
            </nav>
            
            {/* Search and Cart */}
            <div className="flex items-center space-x-4">
              <div className="hidden md:block relative">
                <Search className="absolute left-2 top-2.5 h-4 w-4 text-muted-foreground" />
                <Input
                  placeholder="Search products..."
                  value={searchQuery}
                  onChange={(e) => setSearchQuery(e.target.value)}
                  className="pl-8 w-64"
                />
              </div>
              
              <Button variant="ghost" size="icon" className="relative">
                <Heart className="h-5 w-5" />
              </Button>
              
              <Button variant="ghost" size="icon" className="relative">
                <ShoppingCart className="h-5 w-5" />
                {cartItems.length > 0 && (
                  <Badge className="absolute -top-2 -right-2 h-5 w-5 rounded-full p-0 flex items-center justify-center text-xs">
                    {cartItems.reduce((sum, item) => sum + item.quantity, 0)}
                  </Badge>
                )}
              </Button>
              
              <Button variant="ghost" size="icon" className="relative">
                <User className="h-5 w-5" />
              </Button>
              
              <Button
                variant="ghost"
                size="icon"
                className="md:hidden"
                onClick={() => setMobileMenuOpen(!mobileMenuOpen)}
              >
                <Menu className="h-5 w-5" />
              </Button>
            </div>
          </div>
          
          {/* Mobile Menu */}
          {mobileMenuOpen && (
            <div className="md:hidden border-t py-4">
              <nav className="flex flex-col space-y-2">
                <a href="#home" className="text-sm font-medium hover:text-primary transition-colors py-2">Home</a>
                <a href="#shop" className="text-sm font-medium hover:text-primary transition-colors py-2">Shop</a>
                <a href="#categories" className="text-sm font-medium hover:text-primary transition-colors py-2">Categories</a>
                <a href="#price-comparison" className="text-sm font-medium hover:text-primary transition-colors py-2">Price Compare</a>
                <a href="#about" className="text-sm font-medium hover:text-primary transition-colors py-2">About</a>
                <a href="#contact" className="text-sm font-medium hover:text-primary transition-colors py-2">Contact</a>
              </nav>
              <div className="mt-4">
                <div className="relative">
                  <Search className="absolute left-2 top-2.5 h-4 w-4 text-muted-foreground" />
                  <Input
                    placeholder="Search products..."
                    value={searchQuery}
                    onChange={(e) => setSearchQuery(e.target.value)}
                    className="pl-8"
                  />
                </div>
              </div>
            </div>
          )}
        </div>
      </header>

      {/* Hero Section */}
      <section id="home" className="relative bg-gradient-to-br from-primary/10 via-secondary/5 to-accent/10 py-20">
        <div className="container mx-auto px-4">
          <div className="grid lg:grid-cols-2 gap-12 items-center">
            <div className="space-y-6">
              <Badge className="w-fit bg-accent/20 text-accent-foreground border-accent/30">
                🚀 New: iPhone 16 & Galaxy S25 Accessories Available
              </Badge>
              <h1 className="text-4xl md:text-6xl font-bold leading-tight">
                Premium Protection for Your 
                <span className="text-primary"> Premium Device</span>
              </h1>
              <p className="text-lg text-muted-foreground max-w-md">
                First-to-market with the latest phone accessories. Quality guaranteed through our 1688.com sourcing with ZQ Dropshipping.
              </p>
              <div className="flex flex-col sm:flex-row gap-4">
                <Button size="lg" className="bg-primary hover:bg-primary/90">
                  Shop Now <ArrowRight className="ml-2 h-4 w-4" />
                </Button>
                <Button 
                  size="lg" 
                  variant="outline"
                  onClick={() => document.getElementById('price-comparison').scrollIntoView({ behavior: 'smooth' })}
                >
                  <TrendingDown className="mr-2 h-4 w-4" />
                  Compare Prices
                </Button>
              </div>
              
              {/* Trust Indicators */}
              <div className="flex items-center space-x-6 pt-6">
                <div className="flex items-center space-x-2">
                  <Shield className="h-5 w-5 text-green-500" />
                  <span className="text-sm">Quality Guaranteed</span>
                </div>
                <div className="flex items-center space-x-2">
                  <Truck className="h-5 w-5 text-blue-500" />
                  <span className="text-sm">Fast Shipping</span>
                </div>
                <div className="flex items-center space-x-2">
                  <CheckCircle className="h-5 w-5 text-green-500" />
                  <span className="text-sm">1688.com Sourced</span>
                </div>
              </div>
            </div>
            
            {/* Hero Image/Product Showcase */}
            <div className="relative">
              <div className="grid grid-cols-2 gap-4">
                <Card className="transform rotate-3 hover:rotate-0 transition-transform duration-300">
                  <CardContent className="p-4">
                    <img src="/api/placeholder/200/200" alt="iPhone 16 Case" className="w-full rounded-lg" />
                    <p className="text-sm font-medium mt-2">iPhone 16 Pro Case</p>
                    <p className="text-xs text-muted-foreground">$24.99</p>
                  </CardContent>
                </Card>
                <Card className="transform -rotate-3 hover:rotate-0 transition-transform duration-300 mt-8">
                  <CardContent className="p-4">
                    <img src="/api/placeholder/200/200" alt="Wireless Charger" className="w-full rounded-lg" />
                    <p className="text-sm font-medium mt-2">Wireless Charger</p>
                    <p className="text-xs text-muted-foreground">$29.99</p>
                  </CardContent>
                </Card>
              </div>
            </div>
          </div>
        </div>
      </section>

      {/* Price Comparison Highlight Section */}
      <section className="py-12 bg-gradient-to-r from-green-50 to-blue-50 border-y">
        <div className="container mx-auto px-4">
          <div className="text-center">
            <div className="flex items-center justify-center gap-2 mb-4">
              <Trophy className="h-6 w-6 text-yellow-500" />
              <h2 className="text-2xl font-bold">Lowest Prices Guaranteed</h2>
            </div>
            <p className="text-muted-foreground mb-6 max-w-2xl mx-auto">
              We source directly from 1688.com manufacturers - the same suppliers used by Temu and Shein. 
              Compare our prices with major retailers and see the savings!
            </p>
            <div className="grid grid-cols-1 md:grid-cols-3 gap-6 max-w-4xl mx-auto">
              <div className="text-center">
                <div className="text-3xl font-bold text-green-600">45%</div>
                <div className="text-sm text-muted-foreground">Less than Amazon</div>
              </div>
              <div className="text-center">
                <div className="text-3xl font-bold text-green-600">62%</div>
                <div className="text-sm text-muted-foreground">Less than Best Buy</div>
              </div>
              <div className="text-center">
                <div className="text-3xl font-bold text-green-600">38%</div>
                <div className="text-sm text-muted-foreground">Less than Target</div>
              </div>
            </div>
            <Button 
              className="mt-6" 
              onClick={() => document.getElementById('price-comparison').scrollIntoView({ behavior: 'smooth' })}
            >
              <TrendingDown className="mr-2 h-4 w-4" />
              See Price Comparisons
            </Button>
          </div>
        </div>
      </section>

      {/* Categories Section */}
      <section id="categories" className="py-16 bg-muted/30">
        <div className="container mx-auto px-4">
          <div className="text-center mb-12">
            <h2 className="text-3xl font-bold mb-4">Shop by Category</h2>
            <p className="text-muted-foreground max-w-2xl mx-auto">
              Discover premium accessories for the latest smartphones. All products sourced from 1688.com with quality assurance.
            </p>
          </div>
          
          <div className="grid grid-cols-2 md:grid-cols-3 lg:grid-cols-6 gap-4">
            {categories.map((category, index) => (
              <Card key={index} className="hover:shadow-lg transition-shadow cursor-pointer group">
                <CardContent className="p-6 text-center">
                  <div className="mb-4 text-primary group-hover:scale-110 transition-transform">
                    {category.icon}
                  </div>
                  <h3 className="font-semibold text-sm mb-1">{category.name}</h3>
                  <p className="text-xs text-muted-foreground">{category.count} products</p>
                </CardContent>
              </Card>
            ))}
          </div>
        </div>
      </section>

      {/* Featured Products */}
      <section id="shop" className="py-16">
        <div className="container mx-auto px-4">
          <div className="text-center mb-12">
            <h2 className="text-3xl font-bold mb-4">Featured Products</h2>
            <p className="text-muted-foreground max-w-2xl mx-auto">
              Premium accessories for iPhone 16, Samsung Galaxy S25, and more. Sourced directly from 1688.com manufacturers.
            </p>
          </div>
          
          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
            {featuredProducts.map((product) => (
              <Card key={product.id} className="group hover:shadow-lg transition-all duration-300">
                <CardHeader className="relative p-0">
                  {product.badge && (
                    <Badge className="absolute top-2 left-2 z-10 bg-accent hover:bg-accent/90">
                      {product.badge}
                    </Badge>
                  )}
                  <img 
                    src={product.image} 
                    alt={product.name}
                    className="w-full h-48 object-cover rounded-t-lg group-hover:scale-105 transition-transform duration-300"
                  />
                </CardHeader>
                <CardContent className="p-4">
                  <Badge variant="outline" className="text-xs mb-2">
                    {product.category}
                  </Badge>
                  <h3 className="font-semibold mb-2 line-clamp-2">{product.name}</h3>
                  <div className="flex items-center mb-2">
                    <div className="flex items-center">
                      {[...Array(5)].map((_, i) => (
                        <Star 
                          key={i} 
                          className={`h-3 w-3 ${i < Math.floor(product.rating) ? 'fill-yellow-400 text-yellow-400' : 'text-gray-300'}`} 
                        />
                      ))}
                    </div>
                    <span className="text-sm text-muted-foreground ml-2">
                      {product.rating} ({product.reviews})
                    </span>
                  </div>
                  <div className="flex items-center justify-between mb-3">
                    <div>
                      <span className="text-lg font-bold text-primary">${product.price}</span>
                      {product.originalPrice > product.price && (
                        <>
                          <span className="text-sm text-muted-foreground line-through ml-2">
                            ${product.originalPrice}
                          </span>
                          <Badge variant="destructive" className="ml-2 text-xs">
                            {calculateDiscount(product.originalPrice, product.price)}% OFF
                          </Badge>
                        </>
                      )}
                    </div>
                  </div>
                  <div className="text-xs text-muted-foreground mb-3">
                    {product.features.join(" • ")}
                  </div>
                  <div className="text-xs text-blue-600 mb-3">
                    {product.supplier}
                  </div>
                </CardContent>
                <CardFooter className="p-4 pt-0 space-y-2">
                  <Button 
                    className="w-full" 
                    onClick={() => addToCart(product)}
                  >
                    <ShoppingCart className="mr-2 h-4 w-4" />
                    Add to Cart
                  </Button>
                  <Button 
                    variant="outline" 
                    className="w-full" 
                    onClick={() => showProductComparison(product)}
                  >
                    <TrendingDown className="mr-2 h-4 w-4" />
                    Compare Prices
                  </Button>
                </CardFooter>
              </Card>
            ))}
          </div>
          
          <div className="text-center mt-12">
            <Button variant="outline" size="lg">
              View All Products <ArrowRight className="ml-2 h-4 w-4" />
            </Button>
          </div>
        </div>
      </section>

      {/* Price Comparison Section */}
      <section id="price-comparison" className="py-16 bg-muted/30">
        <div className="container mx-auto px-4">
          <div className="text-center mb-12">
            <h2 className="text-3xl font-bold mb-4">Price Comparison Tool</h2>
            <p className="text-muted-foreground max-w-2xl mx-auto">
              See how much you save with Alpapies compared to major retailers. Our 1688.com sourcing gives you wholesale prices.
            </p>
          </div>
          
          <Tabs defaultValue="featured" className="w-full">
            <TabsList className="grid w-full grid-cols-3">
              <TabsTrigger value="featured">Featured Products</TabsTrigger>
              <TabsTrigger value="bestsellers">Best Sellers</TabsTrigger>
              <TabsTrigger value="newest">Newest</TabsTrigger>
            </TabsList>
            
            <TabsContent value="featured" className="space-y-6 mt-8">
              {featuredProducts.slice(0, 3).map((product) => (
                <PriceComparison key={product.id} product={product} />
              ))}
            </TabsContent>
            
            <TabsContent value="bestsellers" className="space-y-6 mt-8">
              {featuredProducts.filter(p => p.badge === "Best Seller").map((product) => (
                <PriceComparison key={product.id} product={product} />
              ))}
            </TabsContent>
            
            <TabsContent value="newest" className="space-y-6 mt-8">
              {featuredProducts.filter(p => p.badge === "New Release").map((product) => (
                <PriceComparison key={product.id} product={product} />
              ))}
            </TabsContent>
          </Tabs>
        </div>
      </section>

      {/* Why Choose Alpapies */}
      <section className="py-16">
        <div className="container mx-auto px-4">
          <div className="text-center mb-12">
            <h2 className="text-3xl font-bold mb-4">Why Choose Alpapies?</h2>
            <p className="text-muted-foreground max-w-2xl mx-auto">
              We source directly from 1688.com manufacturers through ZQ Dropshipping for the best quality and prices.
            </p>
          </div>
          
          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6">
            <Card className="text-center">
              <CardContent className="p-6">
                <Globe className="h-12 w-12 text-primary mx-auto mb-4" />
                <h3 className="font-semibold mb-2">1688.com Direct Sourcing</h3>
                <p className="text-sm text-muted-foreground">
                  Access to the same suppliers used by Temu and Shein for unbeatable wholesale prices.
                </p>
              </CardContent>
            </Card>
            
            <Card className="text-center">
              <CardContent className="p-6">
                <Award className="h-12 w-12 text-primary mx-auto mb-4" />
                <h3 className="font-semibold mb-2">Quality Guaranteed</h3>
                <p className="text-sm text-muted-foreground">
                  Every product inspected by ZQ Dropshipping before shipping to ensure premium quality.
                </p>
              </CardContent>
            </Card>
            
            <Card className="text-center">
              <CardContent className="p-6">
                <Clock className="h-12 w-12 text-primary mx-auto mb-4" />
                <h3 className="font-semibold mb-2">First to Market</h3>
                <p className="text-sm text-muted-foreground">
                  Get accessories for new phone releases before they're available anywhere else.
                </p>
              </CardContent>
            </Card>
            
            <Card className="text-center">
              <CardContent className="p-6">
                <Truck className="h-12 w-12 text-primary mx-auto mb-4" />
                <h3 className="font-semibold mb-2">Fast Global Shipping</h3>
                <p className="text-sm text-muted-foreground">
                  Worldwide delivery in 7-14 days with real-time tracking and updates.
                </p>
              </CardContent>
            </Card>
          </div>
        </div>
      </section>

      {/* Newsletter Signup */}
      <section className="py-16 bg-primary text-primary-foreground">
        <div className="container mx-auto px-4 text-center">
          <h2 className="text-3xl font-bold mb-4">Stay Ahead of the Curve</h2>
          <p className="text-primary-foreground/80 mb-8 max-w-2xl mx-auto">
            Be the first to know about new phone releases and get exclusive access to accessories before anyone else.
          </p>
          
          <div className="flex flex-col sm:flex-row gap-4 max-w-md mx-auto">
            <Input 
              placeholder="Enter your email" 
              className="bg-white text-foreground"
            />
            <Button variant="secondary" className="bg-accent hover:bg-accent/90 text-accent-foreground">
              Subscribe
            </Button>
          </div>
          
          <p className="text-xs text-primary-foreground/60 mt-4">
            Join 10,000+ customers who get early access to new products
          </p>
        </div>
      </section>

      {/* Footer */}
      <footer className="bg-background border-t py-12">
        <div className="container mx-auto px-4">
          <div className="grid grid-cols-1 md:grid-cols-4 gap-8">
            <div className="space-y-4">
              <div className="flex items-center space-x-2">
                <img src={logoImage} alt="Alpapies" className="h-8 w-8" />
                <span className="text-xl font-bold text-primary">Alpapies</span>
              </div>
              <p className="text-sm text-muted-foreground">
                Premium phone accessories sourced directly from 1688.com manufacturers. Quality guaranteed, prices unmatched.
              </p>
            </div>
            
            <div>
              <h4 className="font-semibold mb-4">Shop</h4>
              <ul className="space-y-2 text-sm text-muted-foreground">
                <li><a href="#" className="hover:text-foreground transition-colors">iPhone 16 Series</a></li>
                <li><a href="#" className="hover:text-foreground transition-colors">Samsung Galaxy S25</a></li>
                <li><a href="#" className="hover:text-foreground transition-colors">Wireless Chargers</a></li>
                <li><a href="#" className="hover:text-foreground transition-colors">Power Banks</a></li>
              </ul>
            </div>
            
            <div>
              <h4 className="font-semibold mb-4">Support</h4>
              <ul className="space-y-2 text-sm text-muted-foreground">
                <li><a href="#" className="hover:text-foreground transition-colors">Contact Us</a></li>
                <li><a href="#" className="hover:text-foreground transition-colors">Shipping Info</a></li>
                <li><a href="#" className="hover:text-foreground transition-colors">Returns</a></li>
                <li><a href="#" className="hover:text-foreground transition-colors">FAQ</a></li>
              </ul>
            </div>
            
            <div>
              <h4 className="font-semibold mb-4">Company</h4>
              <ul className="space-y-2 text-sm text-muted-foreground">
                <li><a href="#" className="hover:text-foreground transition-colors">About Us</a></li>
                <li><a href="#" className="hover:text-foreground transition-colors">1688.com Sourcing</a></li>
                <li><a href="#" className="hover:text-foreground transition-colors">Quality Guarantee</a></li>
                <li><a href="#" className="hover:text-foreground transition-colors">Privacy Policy</a></li>
              </ul>
            </div>
          </div>
          
          <div className="border-t mt-8 pt-8 text-center text-sm text-muted-foreground">
            <p>&copy; 2025 Alpapies. All rights reserved. Powered by 1688.com sourcing.</p>
          </div>
        </div>
      </footer>

      {/* Price Comparison Modal */}
      {showPriceComparison && selectedProduct && (
        <div className="fixed inset-0 bg-black/50 z-50 flex items-center justify-center p-4">
          <div className="bg-white rounded-lg max-w-4xl w-full max-h-[90vh] overflow-y-auto">
            <div className="flex items-center justify-between p-4 border-b">
              <h3 className="text-lg font-semibold">Price Comparison</h3>
              <Button 
                variant="ghost" 
                size="icon"
                onClick={() => setShowPriceComparison(false)}
              >
                <X className="h-4 w-4" />
              </Button>
            </div>
            <div className="p-4">
              <PriceComparison product={selectedProduct} />
            </div>
          </div>
        </div>
      )}
    </div>
  )
}

export default App

