import { useState, useEffect } from 'react'
import { Search, ShoppingCart, TrendingUp, Star, ExternalLink, Bell, Filter } from 'lucide-react'
import { Button } from '@/components/ui/button.jsx'
import { Input } from '@/components/ui/input.jsx'
import { Card, CardContent, CardHeader, CardTitle } from '@/components/ui/card.jsx'
import { Badge } from '@/components/ui/badge.jsx'
import { Tabs, TabsContent, TabsList, TabsTrigger } from '@/components/ui/tabs.jsx'
import './App.css'

const API_BASE_URL = 'https://nghki1cjngjd.manus.space/api'

function App() {
  const [searchQuery, setSearchQuery] = useState('')
  const [searchResults, setSearchResults] = useState([])
  const [categories, setCategories] = useState([])
  const [vendors, setVendors] = useState([])
  const [loading, setLoading] = useState(false)
  const [selectedCategory, setSelectedCategory] = useState('')
  const [trendingProducts, setTrendingProducts] = useState([])

  // Fetch initial data
  useEffect(() => {
    fetchCategories()
    fetchVendors()
    fetchTrendingProducts()
  }, [])

  const fetchCategories = async () => {
    try {
      const response = await fetch(`${API_BASE_URL}/categories`)
      const data = await response.json()
      setCategories(data.categories || [])
    } catch (error) {
      console.error('Error fetching categories:', error)
    }
  }

  const fetchVendors = async () => {
    try {
      const response = await fetch(`${API_BASE_URL}/vendors`)
      const data = await response.json()
      setVendors(data.vendors || [])
    } catch (error) {
      console.error('Error fetching vendors:', error)
    }
  }

  const fetchTrendingProducts = async () => {
    try {
      const response = await fetch(`${API_BASE_URL}/trending?limit=6`)
      const data = await response.json()
      setTrendingProducts(data.trending_products || [])
    } catch (error) {
      console.error('Error fetching trending products:', error)
    }
  }

  const handleSearch = async (e) => {
    e.preventDefault()
    if (!searchQuery.trim()) return

    setLoading(true)
    try {
      const params = new URLSearchParams({
        q: searchQuery,
        ...(selectedCategory && { category: selectedCategory }),
        limit: 20
      })
      
      const response = await fetch(`${API_BASE_URL}/search?${params}`)
      const data = await response.json()
      setSearchResults(data.products || [])
    } catch (error) {
      console.error('Error searching products:', error)
      setSearchResults([])
    } finally {
      setLoading(false)
    }
  }

  const handleVendorClick = async (productVendorId, affiliateUrl) => {
    try {
      // Track the click using the new affiliate API
      const response = await fetch(`${API_BASE_URL}/affiliate/click`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({
          product_vendor_id: productVendorId,
          session_id: sessionStorage.getItem('session_id') || undefined
        })
      })
      
      const result = await response.json()
      
      if (result.success) {
        // Store session ID for future tracking
        sessionStorage.setItem('session_id', result.session_id)
        
        // Open the affiliate link
        window.open(result.redirect_url, '_blank')
      } else {
        // Fallback to original URL
        window.open(affiliateUrl, '_blank')
      }
    } catch (error) {
      console.error('Error tracking click:', error)
      // Still open the link even if tracking fails
      window.open(affiliateUrl, '_blank')
    }
  }

  const ProductCard = ({ product }) => {
    const bestPrice = product.best_price
    const savings = product.savings || 0
    const vendors = product.vendors || []

    return (
      <Card className="w-full hover:shadow-lg transition-shadow">
        <CardHeader className="pb-3">
          <div className="flex gap-4">
            <div className="w-20 h-20 bg-gray-100 rounded-lg flex items-center justify-center">
              {product.image_url ? (
                <img 
                  src={product.image_url} 
                  alt={product.name}
                  className="w-full h-full object-cover rounded-lg"
                />
              ) : (
                <ShoppingCart className="w-8 h-8 text-gray-400" />
              )}
            </div>
            <div className="flex-1">
              <CardTitle className="text-lg line-clamp-2">{product.name}</CardTitle>
              <p className="text-sm text-muted-foreground mt-1">{product.brand}</p>
              <div className="flex items-center gap-2 mt-2">
                <div className="flex items-center">
                  <Star className="w-4 h-4 fill-yellow-400 text-yellow-400" />
                  <span className="text-sm ml-1">4.5</span>
                </div>
                <span className="text-sm text-muted-foreground">(1,234 reviews)</span>
              </div>
            </div>
          </div>
        </CardHeader>
        <CardContent>
          <div className="space-y-3">
            {vendors.slice(0, 3).map((vendor, index) => (
              <div key={vendor.id} className="flex items-center justify-between p-3 bg-gray-50 rounded-lg">
                <div className="flex items-center gap-3">
                  <div className="w-8 h-8 bg-white rounded-full flex items-center justify-center">
                    {vendor.vendor_logo ? (
                      <img 
                        src={vendor.vendor_logo} 
                        alt={vendor.vendor_name}
                        className="w-6 h-6 object-contain"
                      />
                    ) : (
                      <span className="text-xs font-semibold">{vendor.vendor_name?.charAt(0)}</span>
                    )}
                  </div>
                  <div>
                    <p className="font-medium">{vendor.vendor_name}</p>
                    <p className="text-sm text-muted-foreground">
                      {vendor.shipping_cost === 0 ? 'Free shipping' : `+$${vendor.shipping_cost} shipping`}
                    </p>
                  </div>
                </div>
                <div className="text-right">
                  <div className="flex items-center gap-2">
                    <span className="text-lg font-bold">${vendor.current_price}</span>
                    {index === 0 && savings > 0 && (
                      <Badge variant="destructive" className="bg-green-500">
                        BEST
                      </Badge>
                    )}
                  </div>
                  {vendor.discount_percentage > 0 && (
                    <p className="text-sm text-green-600">
                      Save {vendor.discount_percentage.toFixed(0)}%
                    </p>
                  )}
                  <Button 
                    size="sm" 
                    className="mt-2"
                    onClick={() => handleVendorClick(vendor.id, vendor.affiliate_url || vendor.product_url)}
                  >
                    View Deal <ExternalLink className="w-3 h-3 ml-1" />
                  </Button>
                </div>
              </div>
            ))}
            
            {savings > 0 && (
              <div className="text-center p-2 bg-green-50 rounded-lg">
                <p className="text-green-700 font-medium">
                  💰 You save up to ${savings.toFixed(2)} by comparing prices!
                </p>
              </div>
            )}
          </div>
        </CardContent>
      </Card>
    )
  }

  return (
    <div className="min-h-screen bg-background">
      {/* Header */}
      <header className="border-b bg-white sticky top-0 z-50">
        <div className="container mx-auto px-4 py-4">
          <div className="flex items-center justify-between">
            <div className="flex items-center gap-2">
              <TrendingUp className="w-8 h-8 text-blue-600" />
              <h1 className="text-2xl font-bold text-blue-600">PriceCompare</h1>
            </div>
            <nav className="hidden md:flex items-center gap-6">
              <a href="#" className="text-sm font-medium hover:text-blue-600">Categories</a>
              <a href="#" className="text-sm font-medium hover:text-blue-600">Deals</a>
              <a href="#" className="text-sm font-medium hover:text-blue-600">About</a>
            </nav>
          </div>
        </div>
      </header>

      {/* Hero Section */}
      <section className="bg-gradient-to-r from-blue-600 to-purple-600 text-white py-16">
        <div className="container mx-auto px-4 text-center">
          <h2 className="text-4xl md:text-6xl font-bold mb-4">
            Find the Best Deals Across All Platforms
          </h2>
          <p className="text-xl mb-8 opacity-90">
            Compare prices from Amazon, Temu, Shein, and more in one place
          </p>
          
          {/* Search Form */}
          <form onSubmit={handleSearch} className="max-w-2xl mx-auto">
            <div className="flex gap-2">
              <div className="flex-1 relative">
                <Input
                  type="text"
                  placeholder="Search for products..."
                  value={searchQuery}
                  onChange={(e) => setSearchQuery(e.target.value)}
                  className="w-full h-12 pl-4 pr-12 text-black"
                />
                <Search className="absolute right-3 top-3 w-6 h-6 text-gray-400" />
              </div>
              <Button type="submit" size="lg" disabled={loading} className="h-12 px-8">
                {loading ? 'Searching...' : 'Search'}
              </Button>
            </div>
          </form>

          {/* Category Pills */}
          <div className="flex flex-wrap justify-center gap-2 mt-6">
            {categories.slice(0, 5).map((category) => (
              <Button
                key={category.id}
                variant={selectedCategory === category.id.toString() ? "secondary" : "outline"}
                size="sm"
                onClick={() => setSelectedCategory(
                  selectedCategory === category.id.toString() ? '' : category.id.toString()
                )}
                className="text-white border-white/20 hover:bg-white/10"
              >
                {category.name}
              </Button>
            ))}
          </div>
        </div>
      </section>

      {/* Main Content */}
      <main className="container mx-auto px-4 py-8">
        {searchResults.length > 0 ? (
          /* Search Results */
          <div>
            <div className="flex items-center justify-between mb-6">
              <h3 className="text-2xl font-bold">
                Search Results ({searchResults.length} products)
              </h3>
              <div className="flex items-center gap-2">
                <Filter className="w-4 h-4" />
                <span className="text-sm text-muted-foreground">Sort by: Best Price</span>
              </div>
            </div>
            
            <div className="grid gap-6">
              {searchResults.map((product) => (
                <ProductCard key={product.id} product={product} />
              ))}
            </div>
          </div>
        ) : (
          /* Homepage Content */
          <Tabs defaultValue="trending" className="w-full">
            <TabsList className="grid w-full grid-cols-3">
              <TabsTrigger value="trending">Trending Products</TabsTrigger>
              <TabsTrigger value="deals">Best Deals</TabsTrigger>
              <TabsTrigger value="categories">Categories</TabsTrigger>
            </TabsList>
            
            <TabsContent value="trending" className="mt-6">
              <div className="grid gap-6 md:grid-cols-2 lg:grid-cols-3">
                {trendingProducts.map((product) => (
                  <ProductCard key={product.id} product={product} />
                ))}
              </div>
            </TabsContent>
            
            <TabsContent value="deals" className="mt-6">
              <div className="text-center py-12">
                <ShoppingCart className="w-16 h-16 mx-auto text-gray-400 mb-4" />
                <h3 className="text-xl font-semibold mb-2">Best Deals Coming Soon</h3>
                <p className="text-muted-foreground">We're working on finding the best deals for you!</p>
              </div>
            </TabsContent>
            
            <TabsContent value="categories" className="mt-6">
              <div className="grid gap-4 md:grid-cols-2 lg:grid-cols-3">
                {categories.map((category) => (
                  <Card key={category.id} className="hover:shadow-md transition-shadow cursor-pointer">
                    <CardContent className="p-6 text-center">
                      <h4 className="font-semibold mb-2">{category.name}</h4>
                      <p className="text-sm text-muted-foreground">{category.description}</p>
                    </CardContent>
                  </Card>
                ))}
              </div>
            </TabsContent>
          </Tabs>
        )}
      </main>

      {/* Footer */}
      <footer className="bg-gray-900 text-white py-12 mt-16">
        <div className="container mx-auto px-4">
          <div className="grid gap-8 md:grid-cols-4">
            <div>
              <div className="flex items-center gap-2 mb-4">
                <TrendingUp className="w-6 h-6" />
                <span className="text-xl font-bold">PriceCompare</span>
              </div>
              <p className="text-gray-400">
                Find the best deals across all major shopping platforms in one place.
              </p>
            </div>
            <div>
              <h4 className="font-semibold mb-4">Company</h4>
              <ul className="space-y-2 text-gray-400">
                <li><a href="#" className="hover:text-white">About Us</a></li>
                <li><a href="#" className="hover:text-white">Contact</a></li>
                <li><a href="#" className="hover:text-white">Privacy Policy</a></li>
              </ul>
            </div>
            <div>
              <h4 className="font-semibold mb-4">Features</h4>
              <ul className="space-y-2 text-gray-400">
                <li><a href="#" className="hover:text-white">Price Alerts</a></li>
                <li><a href="#" className="hover:text-white">Price History</a></li>
                <li><a href="#" className="hover:text-white">Deal Notifications</a></li>
              </ul>
            </div>
            <div>
              <h4 className="font-semibold mb-4">Partners</h4>
              <div className="flex flex-wrap gap-2">
                {vendors.slice(0, 3).map((vendor) => (
                  <Badge key={vendor.id} variant="outline" className="text-gray-400 border-gray-600">
                    {vendor.name}
                  </Badge>
                ))}
              </div>
            </div>
          </div>
          <div className="border-t border-gray-800 mt-8 pt-8 text-center text-gray-400">
            <p>&copy; 2025 PriceCompare. All rights reserved.</p>
          </div>
        </div>
      </footer>
    </div>
  )
}

export default App

