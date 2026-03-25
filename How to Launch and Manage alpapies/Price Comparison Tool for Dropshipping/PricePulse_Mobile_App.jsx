import React, { useState, useEffect } from 'react'
import { 
  Search, ShoppingCart, Star, MapPin, Clock, DollarSign, 
  Filter, Heart, Share2, ExternalLink, Zap, TrendingUp,
  Package, Wrench, Home, User, Menu, X, ChevronRight,
  Shield, Award, Globe, Smartphone
} from 'lucide-react'

// Mobile-optimized PricePulse App
const PricePulseMobile = () => {
  const [activeTab, setActiveTab] = useState('search')
  const [searchQuery, setSearchQuery] = useState('')
  const [searchType, setSearchType] = useState('products') // 'products' or 'services'
  const [searchResults, setSearchResults] = useState(null)
  const [loading, setLoading] = useState(false)
  const [showFilters, setShowFilters] = useState(false)
  const [favorites, setFavorites] = useState([])
  const [currency, setCurrency] = useState('USD')
  const [location, setLocation] = useState('')
  const [recentSearches, setRecentSearches] = useState([
    'iPhone 15', 'Laptop', 'Web Development', 'Cleaning Service'
  ])

  const API_BASE_URL = 'https://60h5imclkgvv.manus.space/api'

  // Mobile-optimized search function
  const handleSearch = async () => {
    if (!searchQuery.trim()) return

    setLoading(true)
    try {
      const endpoint = searchType === 'products' ? 'smart-search' : 'service-search'
      const params = new URLSearchParams({
        q: searchQuery,
        currency: currency,
        max_results: '15'
      })
      
      if (location) params.append('location', location)

      const response = await fetch(`${API_BASE_URL}/${endpoint}?${params}`)
      const data = await response.json()
      setSearchResults(data)
      
      // Add to recent searches
      if (!recentSearches.includes(searchQuery)) {
        setRecentSearches([searchQuery, ...recentSearches.slice(0, 3)])
      }
    } catch (error) {
      console.error('Search error:', error)
    } finally {
      setLoading(false)
    }
  }

  const toggleFavorite = (item) => {
    const itemId = item.id || item.title
    if (favorites.includes(itemId)) {
      setFavorites(favorites.filter(id => id !== itemId))
    } else {
      setFavorites([...favorites, itemId])
    }
  }

  const formatPrice = (item) => {
    if (searchType === 'products') {
      return item.total_cost ? `${currency} ${item.total_cost.toFixed(2)}` : 'N/A'
    } else {
      if (item.starting_price) return `${currency} ${item.starting_price}+`
      if (item.hourly_rate) return `${currency} ${item.hourly_rate}/hr`
      if (item.bid_amount) return `${currency} ${item.bid_amount}`
      return 'Quote'
    }
  }

  const getPlatformIcon = (platform) => {
    const icons = {
      'Amazon': '🛒', 'eBay': '🏪', 'AliExpress': '🏮', 'Walmart': '🏬',
      'Best Buy': '💻', 'Temu': '🎁', 'Fiverr': '💼', 'Upwork': '👨‍💻',
      'Freelancer': '🔧', 'TaskRabbit': '🏠', 'Thumbtack': '🔨', 'Angie': '🏡'
    }
    return icons[platform] || '🛍️'
  }

  // Mobile Navigation Component
  const MobileNav = () => (
    <div className="fixed bottom-0 left-0 right-0 bg-white border-t border-gray-200 z-50">
      <div className="flex justify-around py-2">
        {[
          { id: 'search', icon: Search, label: 'Search' },
          { id: 'favorites', icon: Heart, label: 'Favorites' },
          { id: 'recent', icon: Clock, label: 'Recent' },
          { id: 'profile', icon: User, label: 'Profile' }
        ].map(tab => (
          <button
            key={tab.id}
            onClick={() => setActiveTab(tab.id)}
            className={`flex flex-col items-center py-2 px-4 ${
              activeTab === tab.id ? 'text-blue-600' : 'text-gray-500'
            }`}
          >
            <tab.icon className="h-5 w-5 mb-1" />
            <span className="text-xs">{tab.label}</span>
          </button>
        ))}
      </div>
    </div>
  )

  // Search Header Component
  const SearchHeader = () => (
    <div className="bg-gradient-to-r from-blue-600 to-purple-600 text-white p-4 pb-6">
      <div className="flex items-center justify-between mb-4">
        <div className="flex items-center space-x-2">
          <TrendingUp className="h-6 w-6" />
          <h1 className="text-xl font-bold">PricePulse</h1>
        </div>
        <button 
          onClick={() => setShowFilters(!showFilters)}
          className="p-2 rounded-full bg-white/20"
        >
          <Filter className="h-5 w-5" />
        </button>
      </div>

      {/* Search Type Toggle */}
      <div className="flex bg-white/20 rounded-lg p-1 mb-4">
        <button
          onClick={() => setSearchType('products')}
          className={`flex-1 py-2 px-4 rounded-md text-sm font-medium transition-colors ${
            searchType === 'products' 
              ? 'bg-white text-blue-600' 
              : 'text-white/80'
          }`}
        >
          <Package className="h-4 w-4 inline mr-2" />
          Products
        </button>
        <button
          onClick={() => setSearchType('services')}
          className={`flex-1 py-2 px-4 rounded-md text-sm font-medium transition-colors ${
            searchType === 'services' 
              ? 'bg-white text-blue-600' 
              : 'text-white/80'
          }`}
        >
          <Wrench className="h-4 w-4 inline mr-2" />
          Services
        </button>
      </div>

      {/* Search Bar */}
      <div className="relative">
        <input
          type="text"
          placeholder={`Search ${searchType}...`}
          value={searchQuery}
          onChange={(e) => setSearchQuery(e.target.value)}
          onKeyPress={(e) => e.key === 'Enter' && handleSearch()}
          className="w-full py-3 px-4 pr-12 rounded-lg text-gray-900 placeholder-gray-500"
        />
        <button
          onClick={handleSearch}
          disabled={loading}
          className="absolute right-2 top-1/2 transform -translate-y-1/2 bg-blue-600 text-white p-2 rounded-lg"
        >
          {loading ? (
            <div className="animate-spin h-4 w-4 border-2 border-white border-t-transparent rounded-full" />
          ) : (
            <Search className="h-4 w-4" />
          )}
        </button>
      </div>

      {/* Filters Panel */}
      {showFilters && (
        <div className="mt-4 bg-white/10 rounded-lg p-4">
          <div className="grid grid-cols-2 gap-4">
            <div>
              <label className="block text-sm font-medium mb-2">Currency</label>
              <select
                value={currency}
                onChange={(e) => setCurrency(e.target.value)}
                className="w-full py-2 px-3 rounded-md text-gray-900"
              >
                <option value="USD">USD ($)</option>
                <option value="EUR">EUR (€)</option>
                <option value="GBP">GBP (£)</option>
                <option value="ZAR">ZAR (R)</option>
              </select>
            </div>
            <div>
              <label className="block text-sm font-medium mb-2">Location</label>
              <input
                type="text"
                placeholder="Your location"
                value={location}
                onChange={(e) => setLocation(e.target.value)}
                className="w-full py-2 px-3 rounded-md text-gray-900"
              />
            </div>
          </div>
        </div>
      )}
    </div>
  )

  // Product/Service Card Component
  const ItemCard = ({ item, index }) => {
    const isProduct = searchType === 'products'
    const isFavorite = favorites.includes(item.id || item.title)

    return (
      <div className="bg-white rounded-lg shadow-md p-4 mb-4 border border-gray-100">
        <div className="flex justify-between items-start mb-3">
          <div className="flex-1">
            <div className="flex items-center space-x-2 mb-2">
              <span className="text-lg">{getPlatformIcon(item.platform)}</span>
              <span className="text-xs font-medium text-gray-500 bg-gray-100 px-2 py-1 rounded">
                {item.platform}
              </span>
              {item.recommendation_level && (
                <span className={`text-xs px-2 py-1 rounded ${
                  item.recommendation_level === 'Highly Recommended' 
                    ? 'bg-green-100 text-green-800'
                    : item.recommendation_level === 'Recommended'
                    ? 'bg-blue-100 text-blue-800'
                    : 'bg-yellow-100 text-yellow-800'
                }`}>
                  {item.recommendation_level}
                </span>
              )}
            </div>
            <h3 className="font-semibold text-gray-900 mb-2 line-clamp-2">
              {item.title}
            </h3>
            <div className="flex items-center space-x-4 text-sm text-gray-600 mb-2">
              {(item.rating || item.provider_rating) && (
                <div className="flex items-center space-x-1">
                  <Star className="h-4 w-4 text-yellow-500 fill-current" />
                  <span>{item.rating || item.provider_rating}/5</span>
                </div>
              )}
              {item.location && (
                <div className="flex items-center space-x-1">
                  <MapPin className="h-4 w-4" />
                  <span className="truncate">{item.location}</span>
                </div>
              )}
              {(item.delivery_time || item.response_time) && (
                <div className="flex items-center space-x-1">
                  <Clock className="h-4 w-4" />
                  <span>{item.delivery_time || item.response_time}</span>
                </div>
              )}
            </div>
          </div>
          <button
            onClick={() => toggleFavorite(item)}
            className={`p-2 rounded-full ${
              isFavorite ? 'text-red-500' : 'text-gray-400'
            }`}
          >
            <Heart className={`h-5 w-5 ${isFavorite ? 'fill-current' : ''}`} />
          </button>
        </div>

        <div className="flex items-center justify-between">
          <div>
            <div className="text-2xl font-bold text-green-600">
              {formatPrice(item)}
            </div>
            {isProduct && item.savings_amount && (
              <div className="text-sm text-green-600">
                Save {currency} {item.savings_amount.toFixed(2)}
              </div>
            )}
            {!isProduct && item.provider_level && (
              <div className="text-sm text-blue-600">
                {item.provider_level}
              </div>
            )}
          </div>
          <div className="flex space-x-2">
            <button className="p-2 text-gray-500">
              <Share2 className="h-4 w-4" />
            </button>
            <button
              onClick={() => window.open(item.affiliate_url || item.product_url || item.service_url, '_blank')}
              className="bg-blue-600 text-white px-4 py-2 rounded-lg text-sm font-medium flex items-center space-x-1"
            >
              <span>View</span>
              <ExternalLink className="h-3 w-3" />
            </button>
          </div>
        </div>

        {/* Additional Info for Services */}
        {!isProduct && item.packages && (
          <div className="mt-3 pt-3 border-t border-gray-100">
            <div className="text-sm text-gray-600">
              <span className="font-medium">Packages:</span> Basic ${item.packages.basic?.price} | 
              Standard ${item.packages.standard?.price} | 
              Premium ${item.packages.premium?.price}
            </div>
          </div>
        )}

        {/* Verification badges */}
        {(item.background_checked || item.licensed || item.insured) && (
          <div className="mt-2 flex items-center space-x-2">
            <Shield className="h-4 w-4 text-green-600" />
            <span className="text-sm text-green-600">Verified Provider</span>
          </div>
        )}
      </div>
    )
  }

  // Recent Searches Component
  const RecentSearches = () => (
    <div className="p-4">
      <h2 className="text-lg font-semibold mb-4">Recent Searches</h2>
      <div className="space-y-2">
        {recentSearches.map((search, index) => (
          <button
            key={index}
            onClick={() => {
              setSearchQuery(search)
              setActiveTab('search')
            }}
            className="w-full text-left p-3 bg-gray-50 rounded-lg flex items-center justify-between"
          >
            <span>{search}</span>
            <ChevronRight className="h-4 w-4 text-gray-400" />
          </button>
        ))}
      </div>
    </div>
  )

  // Favorites Component
  const Favorites = () => (
    <div className="p-4">
      <h2 className="text-lg font-semibold mb-4">Favorites</h2>
      {favorites.length === 0 ? (
        <div className="text-center py-8 text-gray-500">
          <Heart className="h-12 w-12 mx-auto mb-4 text-gray-300" />
          <p>No favorites yet</p>
          <p className="text-sm">Tap the heart icon on items to save them here</p>
        </div>
      ) : (
        <div className="space-y-2">
          {favorites.map((fav, index) => (
            <div key={index} className="p-3 bg-gray-50 rounded-lg">
              {fav}
            </div>
          ))}
        </div>
      )}
    </div>
  )

  // Profile Component
  const Profile = () => (
    <div className="p-4">
      <h2 className="text-lg font-semibold mb-4">Profile</h2>
      <div className="space-y-4">
        <div className="bg-gradient-to-r from-blue-600 to-purple-600 text-white p-4 rounded-lg">
          <div className="flex items-center space-x-3">
            <div className="w-12 h-12 bg-white/20 rounded-full flex items-center justify-center">
              <User className="h-6 w-6" />
            </div>
            <div>
              <h3 className="font-semibold">Welcome to PricePulse</h3>
              <p className="text-sm opacity-90">Smart shopping companion</p>
            </div>
          </div>
        </div>

        <div className="space-y-3">
          <div className="flex items-center justify-between p-3 bg-gray-50 rounded-lg">
            <div className="flex items-center space-x-3">
              <Globe className="h-5 w-5 text-gray-600" />
              <span>Currency</span>
            </div>
            <span className="text-gray-600">{currency}</span>
          </div>
          
          <div className="flex items-center justify-between p-3 bg-gray-50 rounded-lg">
            <div className="flex items-center space-x-3">
              <MapPin className="h-5 w-5 text-gray-600" />
              <span>Location</span>
            </div>
            <span className="text-gray-600">{location || 'Not set'}</span>
          </div>

          <div className="flex items-center justify-between p-3 bg-gray-50 rounded-lg">
            <div className="flex items-center space-x-3">
              <Smartphone className="h-5 w-5 text-gray-600" />
              <span>App Version</span>
            </div>
            <span className="text-gray-600">1.0.0</span>
          </div>
        </div>

        <div className="mt-6 p-4 bg-blue-50 rounded-lg">
          <h4 className="font-semibold text-blue-900 mb-2">About PricePulse</h4>
          <p className="text-sm text-blue-800">
            Compare prices across 12+ platforms and find the best deals on products and services. 
            Save money with smart recommendations and total cost transparency.
          </p>
        </div>
      </div>
    </div>
  )

  // Main App Component
  return (
    <div className="min-h-screen bg-gray-50 pb-16">
      {/* Header */}
      {activeTab === 'search' && <SearchHeader />}
      
      {/* Content */}
      <div className="flex-1">
        {activeTab === 'search' && (
          <div className="p-4">
            {searchResults ? (
              <div>
                {/* Results Summary */}
                <div className="mb-4 p-3 bg-blue-50 rounded-lg">
                  <div className="flex items-center justify-between">
                    <div>
                      <h3 className="font-semibold text-blue-900">
                        {searchResults.total_services || searchResults.total_products} results found
                      </h3>
                      <p className="text-sm text-blue-700">
                        Search completed in {searchResults.search_duration_seconds}s
                      </p>
                    </div>
                    <Zap className="h-6 w-6 text-blue-600" />
                  </div>
                </div>

                {/* Recommendations */}
                {searchResults.recommendations && searchResults.recommendations.length > 0 && (
                  <div className="mb-4 p-3 bg-green-50 rounded-lg">
                    <h4 className="font-semibold text-green-900 mb-2 flex items-center">
                      <Award className="h-4 w-4 mr-2" />
                      Smart Recommendations
                    </h4>
                    <div className="space-y-1">
                      {searchResults.recommendations.slice(0, 2).map((rec, index) => (
                        <p key={index} className="text-sm text-green-800">• {rec}</p>
                      ))}
                    </div>
                  </div>
                )}

                {/* Results */}
                <div>
                  {(searchResults.services || searchResults.products || []).map((item, index) => (
                    <ItemCard key={index} item={item} index={index} />
                  ))}
                </div>
              </div>
            ) : (
              <div className="text-center py-8">
                <div className="text-6xl mb-4">🔍</div>
                <h3 className="text-lg font-semibold text-gray-900 mb-2">
                  Find the best {searchType}
                </h3>
                <p className="text-gray-600 mb-6">
                  Search across 12+ platforms to compare prices and find great deals
                </p>
                
                {/* Quick Search Suggestions */}
                <div className="grid grid-cols-2 gap-3">
                  {['iPhone 15', 'Laptop', 'Web Design', 'Cleaning'].map((suggestion, index) => (
                    <button
                      key={index}
                      onClick={() => {
                        setSearchQuery(suggestion)
                        handleSearch()
                      }}
                      className="p-3 bg-white rounded-lg border border-gray-200 text-sm font-medium"
                    >
                      {suggestion}
                    </button>
                  ))}
                </div>
              </div>
            )}
          </div>
        )}

        {activeTab === 'favorites' && <Favorites />}
        {activeTab === 'recent' && <RecentSearches />}
        {activeTab === 'profile' && <Profile />}
      </div>

      {/* Mobile Navigation */}
      <MobileNav />
    </div>
  )
}

export default PricePulseMobile
