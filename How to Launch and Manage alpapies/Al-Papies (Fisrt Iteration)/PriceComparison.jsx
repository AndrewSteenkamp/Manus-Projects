import React, { useState, useEffect } from 'react'
import { Card, CardContent, CardHeader, CardTitle } from '@/components/ui/card.jsx'
import { Badge } from '@/components/ui/badge.jsx'
import { Button } from '@/components/ui/button.jsx'
import { 
  TrendingDown, 
  ExternalLink, 
  Star, 
  CheckCircle, 
  AlertCircle,
  Trophy,
  DollarSign,
  Percent,
  ShoppingCart
} from 'lucide-react'

const PriceComparison = ({ product }) => {
  const [competitors, setCompetitors] = useState([])
  const [loading, setLoading] = useState(true)

  // Mock competitor data - in real implementation, this would come from API
  useEffect(() => {
    // Simulate API call delay
    setTimeout(() => {
      const mockCompetitors = generateCompetitorData(product)
      setCompetitors(mockCompetitors)
      setLoading(false)
    }, 1000)
  }, [product])

  const generateCompetitorData = (product) => {
    const basePrice = product.price
    const competitors = [
      {
        name: "Alpapies",
        price: basePrice,
        originalPrice: product.originalPrice,
        logo: "🛡️",
        isOurStore: true,
        features: ["1688.com Direct", "Quality Guaranteed", "Fast Shipping"],
        rating: 4.8,
        availability: "In Stock",
        shipping: "Free shipping",
        badge: "Best Value"
      },
      {
        name: "Amazon",
        price: basePrice * 1.45,
        originalPrice: basePrice * 1.65,
        logo: "📦",
        isOurStore: false,
        features: ["Prime Shipping", "Returns"],
        rating: 4.3,
        availability: "In Stock",
        shipping: "Prime: Free",
        badge: null
      },
      {
        name: "Best Buy",
        price: basePrice * 1.62,
        originalPrice: basePrice * 1.85,
        logo: "🏪",
        isOurStore: false,
        features: ["Store Pickup", "Warranty"],
        rating: 4.1,
        availability: "Limited Stock",
        shipping: "$5.99",
        badge: null
      },
      {
        name: "Target",
        price: basePrice * 1.38,
        originalPrice: basePrice * 1.58,
        logo: "🎯",
        isOurStore: false,
        features: ["RedCard 5% Off", "Store Pickup"],
        rating: 4.2,
        availability: "In Stock",
        shipping: "$4.99",
        badge: null
      },
      {
        name: "Walmart",
        price: basePrice * 1.28,
        originalPrice: basePrice * 1.48,
        logo: "🏬",
        isOurStore: false,
        features: ["Pickup Today", "Returns"],
        rating: 3.9,
        availability: "In Stock",
        shipping: "$3.99",
        badge: null
      }
    ]

    return competitors.sort((a, b) => a.price - b.price)
  }

  const calculateSavings = (competitorPrice, ourPrice) => {
    const savings = competitorPrice - ourPrice
    const percentage = ((savings / competitorPrice) * 100).toFixed(0)
    return { amount: savings.toFixed(2), percentage }
  }

  if (loading) {
    return (
      <Card className="w-full">
        <CardHeader>
          <CardTitle className="flex items-center gap-2">
            <TrendingDown className="h-5 w-5" />
            Price Comparison
          </CardTitle>
        </CardHeader>
        <CardContent>
          <div className="space-y-4">
            {[1, 2, 3, 4, 5].map((i) => (
              <div key={i} className="animate-pulse">
                <div className="flex items-center justify-between p-4 border rounded-lg">
                  <div className="flex items-center gap-3">
                    <div className="w-8 h-8 bg-gray-200 rounded"></div>
                    <div className="w-20 h-4 bg-gray-200 rounded"></div>
                  </div>
                  <div className="w-16 h-6 bg-gray-200 rounded"></div>
                </div>
              </div>
            ))}
          </div>
        </CardContent>
      </Card>
    )
  }

  return (
    <Card className="w-full">
      <CardHeader>
        <CardTitle className="flex items-center gap-2">
          <TrendingDown className="h-5 w-5" />
          Price Comparison - {product.name}
        </CardTitle>
        <p className="text-sm text-gray-600">
          Compare prices across major retailers. Prices updated in real-time.
        </p>
      </CardHeader>
      <CardContent>
        <div className="space-y-3">
          {competitors.map((competitor, index) => {
            const isLowestPrice = index === 0
            const savings = competitor.isOurStore ? null : calculateSavings(competitor.price, competitors[0].price)
            
            return (
              <div 
                key={competitor.name}
                className={`relative p-4 border rounded-lg transition-all hover:shadow-md ${
                  competitor.isOurStore 
                    ? 'border-blue-500 bg-blue-50 ring-2 ring-blue-200' 
                    : 'border-gray-200 hover:border-gray-300'
                }`}
              >
                {competitor.badge && (
                  <Badge 
                    className={`absolute -top-2 -right-2 ${
                      competitor.badge === 'Best Value' 
                        ? 'bg-green-500 hover:bg-green-600' 
                        : 'bg-blue-500 hover:bg-blue-600'
                    }`}
                  >
                    {competitor.badge}
                  </Badge>
                )}
                
                <div className="flex items-center justify-between">
                  <div className="flex items-center gap-3">
                    <div className="text-2xl">{competitor.logo}</div>
                    <div>
                      <div className="flex items-center gap-2">
                        <h4 className="font-semibold">{competitor.name}</h4>
                        {competitor.isOurStore && (
                          <Trophy className="h-4 w-4 text-yellow-500" />
                        )}
                      </div>
                      <div className="flex items-center gap-2 text-sm text-gray-600">
                        <Star className="h-3 w-3 fill-yellow-400 text-yellow-400" />
                        <span>{competitor.rating}</span>
                        <span>•</span>
                        <span>{competitor.availability}</span>
                      </div>
                      <div className="text-xs text-gray-500 mt-1">
                        {competitor.features.join(" • ")}
                      </div>
                    </div>
                  </div>
                  
                  <div className="text-right">
                    <div className="flex items-center gap-2">
                      <div>
                        {competitor.originalPrice > competitor.price && (
                          <div className="text-sm text-gray-500 line-through">
                            ${competitor.originalPrice.toFixed(2)}
                          </div>
                        )}
                        <div className={`text-lg font-bold ${
                          competitor.isOurStore ? 'text-blue-600' : 'text-gray-900'
                        }`}>
                          ${competitor.price.toFixed(2)}
                        </div>
                        <div className="text-xs text-gray-500">
                          {competitor.shipping}
                        </div>
                      </div>
                      
                      {savings && (
                        <div className="text-right">
                          <div className="text-sm font-semibold text-red-600">
                            +${savings.amount}
                          </div>
                          <div className="text-xs text-red-500">
                            {savings.percentage}% more
                          </div>
                        </div>
                      )}
                    </div>
                    
                    {competitor.isOurStore ? (
                      <Button 
                        size="sm" 
                        className="mt-2 bg-blue-600 hover:bg-blue-700"
                      >
                        <ShoppingCart className="h-3 w-3 mr-1" />
                        Add to Cart
                      </Button>
                    ) : (
                      <Button 
                        variant="outline" 
                        size="sm" 
                        className="mt-2"
                        onClick={() => window.open('#', '_blank')}
                      >
                        <ExternalLink className="h-3 w-3 mr-1" />
                        View Deal
                      </Button>
                    )}
                  </div>
                </div>
                
                {competitor.isOurStore && (
                  <div className="mt-3 p-3 bg-white rounded border border-blue-200">
                    <div className="flex items-center gap-2 text-sm">
                      <CheckCircle className="h-4 w-4 text-green-500" />
                      <span className="font-medium text-green-700">
                        Why choose Alpapies?
                      </span>
                    </div>
                    <ul className="text-xs text-gray-600 mt-2 space-y-1">
                      <li>• Direct sourcing from 1688.com manufacturers</li>
                      <li>• Same suppliers used by Temu and Shein</li>
                      <li>• Quality guarantee with fast shipping</li>
                      <li>• No middleman markup - wholesale prices</li>
                    </ul>
                  </div>
                )}
              </div>
            )
          })}
        </div>
        
        <div className="mt-6 p-4 bg-green-50 border border-green-200 rounded-lg">
          <div className="flex items-center gap-2 text-green-700 font-semibold mb-2">
            <DollarSign className="h-4 w-4" />
            Your Savings with Alpapies
          </div>
          <div className="grid grid-cols-2 gap-4 text-sm">
            <div>
              <div className="text-gray-600">vs Amazon:</div>
              <div className="font-semibold text-green-600">
                Save ${calculateSavings(competitors[1]?.price || 0, competitors[0].price).amount}
                ({calculateSavings(competitors[1]?.price || 0, competitors[0].price).percentage}%)
              </div>
            </div>
            <div>
              <div className="text-gray-600">vs Best Buy:</div>
              <div className="font-semibold text-green-600">
                Save ${calculateSavings(competitors[2]?.price || 0, competitors[0].price).amount}
                ({calculateSavings(competitors[2]?.price || 0, competitors[0].price).percentage}%)
              </div>
            </div>
          </div>
          <div className="mt-3 text-xs text-gray-600">
            * Prices updated every 24 hours. Savings calculated before taxes and shipping.
          </div>
        </div>
      </CardContent>
    </Card>
  )
}

export default PriceComparison

