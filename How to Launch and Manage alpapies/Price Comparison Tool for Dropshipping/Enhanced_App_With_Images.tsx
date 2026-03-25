import React, { useState, useEffect } from 'react';
import { 
  Search, Star, MapPin, Clock, TrendingUp, Package, Wrench, 
  ExternalLink, Heart, Share2, Award, Shield, Truck, Zap,
  CheckCircle, AlertCircle, Info
} from 'lucide-react';
import './App.css';

interface SearchResult {
  title: string;
  brand: string;
  model?: string;
  platform: string;
  price?: number;
  total_cost?: number;
  starting_price?: number;
  hourly_rate?: number;
  rating?: number;
  provider_rating?: number;
  review_count?: number;
  location: string;
  delivery_time?: string;
  response_time?: string;
  recommendation_level: string;
  savings_amount?: number;
  affiliate_url: string;
  product_image?: string;
  brand_logo?: string;
  provider_image?: string;
  portfolio_images?: string[];
  features?: string[];
  condition?: string;
  warranty?: string;
  seller_rating?: number;
  free_shipping?: boolean;
  prime_eligible?: boolean;
  provider_name?: string;
  provider_level?: string;
  skills?: string[];
  languages?: string[];
  packages?: {
    basic?: { price: number; delivery: string; features: string[] };
    standard?: { price: number; delivery: string; features: string[] };
    premium?: { price: number; delivery: string; features: string[] };
  };
}

interface SearchResponse {
  query: string;
  total_products?: number;
  total_services?: number;
  search_duration_seconds: number;
  currency: string;
  recommendations: string[];
  products?: SearchResult[];
  services?: SearchResult[];
  search_metadata?: {
    platforms_searched: number;
    has_images: boolean;
    has_brand_info: boolean;
    enhanced_features: boolean;
  };
}

function App() {
  const [searchQuery, setSearchQuery] = useState('');
  const [searchType, setSearchType] = useState<'products' | 'services'>('products');
  const [searchResults, setSearchResults] = useState<SearchResponse | null>(null);
  const [loading, setLoading] = useState(false);
  const [backendStatus, setBackendStatus] = useState<'checking' | 'online' | 'offline'>('checking');
  const [currency, setCurrency] = useState('USD');
  const [favorites, setFavorites] = useState<string[]>([]);

  // Check if backend is running
  useEffect(() => {
    checkBackendStatus();
  }, []);

  const checkBackendStatus = async () => {
    try {
      const response = await fetch('http://localhost:5000/api/health');
      if (response.ok) {
        setBackendStatus('online');
      } else {
        setBackendStatus('offline');
      }
    } catch (error) {
      setBackendStatus('offline');
    }
  };

  const handleSearch = async () => {
    if (!searchQuery.trim()) return;

    setLoading(true);
    try {
      const response = await fetch(
        `http://localhost:5000/api/search?q=${encodeURIComponent(searchQuery)}&type=${searchType}&currency=${currency}`
      );
      const data = await response.json();
      setSearchResults(data);
    } catch (error) {
      console.error('Search error:', error);
      alert('Search failed. Make sure your backend is running!');
    } finally {
      setLoading(false);
    }
  };

  const toggleFavorite = (itemTitle: string) => {
    if (favorites.includes(itemTitle)) {
      setFavorites(favorites.filter(fav => fav !== itemTitle));
    } else {
      setFavorites([...favorites, itemTitle]);
    }
  };

  const formatPrice = (item: SearchResult) => {
    const symbol = currency === 'USD' ? '$' : currency === 'EUR' ? '€' : currency === 'GBP' ? '£' : '$';
    
    if (searchType === 'products') {
      return item.total_cost ? `${symbol}${item.total_cost.toFixed(2)}` : 'N/A';
    } else {
      if (item.starting_price) return `${symbol}${item.starting_price}+`;
      if (item.hourly_rate) return `${symbol}${item.hourly_rate}/hr`;
      return 'Quote';
    }
  };

  const getPlatformIcon = (platform: string) => {
    const icons: { [key: string]: string } = {
      'Amazon': '🛒',
      'eBay': '🏪',
      'AliExpress': '🏮',
      'Walmart': '🏬',
      'Best Buy': '💻',
      'Apple Store': '🍎',
      'Dell Direct': '💼',
      'HP Store': '🖥️',
      'Fiverr': '💼',
      'Upwork': '👨‍💻'
    };
    return icons[platform] || '🛍️';
  };

  const getRecommendationColor = (level: string) => {
    switch (level) {
      case 'Highly Recommended':
        return 'bg-green-100 text-green-800 border-green-200';
      case 'Recommended':
        return 'bg-blue-100 text-blue-800 border-blue-200';
      case 'Good Option':
        return 'bg-yellow-100 text-yellow-800 border-yellow-200';
      default:
        return 'bg-gray-100 text-gray-800 border-gray-200';
    }
  };

  const ProductCard = ({ item, index }: { item: SearchResult; index: number }) => {
    const isFavorite = favorites.includes(item.title);

    return (
      <div className="bg-white rounded-xl shadow-lg border border-gray-200 overflow-hidden hover:shadow-xl transition-all duration-300 transform hover:-translate-y-1">
        {/* Product Image */}
        <div className="relative h-48 bg-gray-100">
          {item.product_image ? (
            <img
              src={item.product_image}
              alt={item.title}
              className="w-full h-full object-cover"
              onError={(e) => {
                (e.target as HTMLImageElement).src = 'https://via.placeholder.com/400x300?text=Product+Image';
              }}
            />
          ) : (
            <div className="w-full h-full flex items-center justify-center text-gray-400">
              <Package className="h-16 w-16" />
            </div>
          )}
          
          {/* Brand Logo Overlay */}
          {item.brand_logo && (
            <div className="absolute top-2 left-2 bg-white rounded-lg p-2 shadow-md">
              <img
                src={item.brand_logo}
                alt={item.brand}
                className="h-6 w-auto"
                onError={(e) => {
                  (e.target as HTMLImageElement).style.display = 'none';
                }}
              />
            </div>
          )}

          {/* Favorite Button */}
          <button
            onClick={() => toggleFavorite(item.title)}
            className={`absolute top-2 right-2 p-2 rounded-full shadow-md transition-colors ${
              isFavorite 
                ? 'bg-red-500 text-white' 
                : 'bg-white text-gray-400 hover:text-red-500'
            }`}
          >
            <Heart className={`h-4 w-4 ${isFavorite ? 'fill-current' : ''}`} />
          </button>

          {/* Prime/Shipping Badge */}
          {item.prime_eligible && (
            <div className="absolute bottom-2 left-2 bg-blue-600 text-white px-2 py-1 rounded text-xs font-medium">
              Prime
            </div>
          )}
          
          {item.free_shipping && (
            <div className="absolute bottom-2 right-2 bg-green-600 text-white px-2 py-1 rounded text-xs font-medium flex items-center">
              <Truck className="h-3 w-3 mr-1" />
              Free Ship
            </div>
          )}
        </div>

        {/* Card Content */}
        <div className="p-6">
          {/* Platform and Recommendation */}
          <div className="flex items-center justify-between mb-3">
            <div className="flex items-center space-x-2">
              <span className="text-lg">{getPlatformIcon(item.platform)}</span>
              <span className="text-sm font-medium text-gray-600 bg-gray-100 px-2 py-1 rounded">
                {item.platform}
              </span>
            </div>
            <span className={`text-xs px-2 py-1 rounded border ${getRecommendationColor(item.recommendation_level)}`}>
              {item.recommendation_level}
            </span>
          </div>

          {/* Brand and Model */}
          <div className="mb-2">
            <span className="text-sm font-semibold text-blue-600">{item.brand}</span>
            {item.model && (
              <span className="text-sm text-gray-500 ml-2">{item.model}</span>
            )}
          </div>

          {/* Product Title */}
          <h3 className="font-semibold text-gray-900 mb-3 line-clamp-2 leading-tight">
            {item.title}
          </h3>

          {/* Rating and Reviews */}
          <div className="flex items-center space-x-4 text-sm text-gray-600 mb-3">
            {item.rating && (
              <div className="flex items-center space-x-1">
                <div className="flex">
                  {[...Array(5)].map((_, i) => (
                    <Star
                      key={i}
                      className={`h-4 w-4 ${
                        i < Math.floor(item.rating!)
                          ? 'text-yellow-400 fill-current'
                          : 'text-gray-300'
                      }`}
                    />
                  ))}
                </div>
                <span className="font-medium">{item.rating}</span>
                {item.review_count && (
                  <span className="text-gray-500">({item.review_count.toLocaleString()})</span>
                )}
              </div>
            )}
          </div>

          {/* Features */}
          {item.features && item.features.length > 0 && (
            <div className="mb-3">
              <div className="flex flex-wrap gap-1">
                {item.features.slice(0, 3).map((feature, idx) => (
                  <span
                    key={idx}
                    className="text-xs bg-blue-50 text-blue-700 px-2 py-1 rounded"
                  >
                    {feature}
                  </span>
                ))}
                {item.features.length > 3 && (
                  <span className="text-xs text-gray-500">
                    +{item.features.length - 3} more
                  </span>
                )}
              </div>
            </div>
          )}

          {/* Location and Delivery */}
          <div className="space-y-1 text-sm text-gray-600 mb-4">
            <div className="flex items-center space-x-1">
              <MapPin className="h-4 w-4" />
              <span>{item.location}</span>
            </div>
            <div className="flex items-center space-x-1">
              <Clock className="h-4 w-4" />
              <span>{item.delivery_time}</span>
            </div>
            {item.condition && (
              <div className="flex items-center space-x-1">
                <CheckCircle className="h-4 w-4 text-green-500" />
                <span>Condition: {item.condition}</span>
              </div>
            )}
          </div>

          {/* Price and Actions */}
          <div className="flex items-center justify-between">
            <div>
              <div className="text-2xl font-bold text-green-600">
                {formatPrice(item)}
              </div>
              {item.savings_amount && item.savings_amount > 0 && (
                <div className="text-sm text-green-600 font-medium">
                  Save {currency === 'USD' ? '$' : '€'}{item.savings_amount.toFixed(2)}
                </div>
              )}
              {item.price && item.total_cost && item.price !== item.total_cost && (
                <div className="text-sm text-gray-500 line-through">
                  {currency === 'USD' ? '$' : '€'}{item.price.toFixed(2)}
                </div>
              )}
            </div>
            
            <div className="flex space-x-2">
              <button
                onClick={() => navigator.share?.({ title: item.title, url: item.affiliate_url })}
                className="p-2 text-gray-500 hover:text-blue-600 transition-colors"
              >
                <Share2 className="h-4 w-4" />
              </button>
              <button
                onClick={() => window.open(item.affiliate_url, '_blank')}
                className="bg-blue-600 text-white px-4 py-2 rounded-lg hover:bg-blue-700 transition-colors flex items-center space-x-1"
              >
                <span>View Deal</span>
                <ExternalLink className="h-3 w-3" />
              </button>
            </div>
          </div>

          {/* Seller Rating */}
          {item.seller_rating && (
            <div className="mt-3 pt-3 border-t border-gray-100">
              <div className="flex items-center justify-between text-sm">
                <span className="text-gray-600">Seller Rating:</span>
                <div className="flex items-center space-x-1">
                  <Star className="h-4 w-4 text-yellow-400 fill-current" />
                  <span className="font-medium">{item.seller_rating}/5</span>
                </div>
              </div>
            </div>
          )}
        </div>
      </div>
    );
  };

  const ServiceCard = ({ item, index }: { item: SearchResult; index: number }) => {
    const isFavorite = favorites.includes(item.title);

    return (
      <div className="bg-white rounded-xl shadow-lg border border-gray-200 overflow-hidden hover:shadow-xl transition-all duration-300">
        {/* Service Header with Provider Image */}
        <div className="p-6 bg-gradient-to-r from-blue-50 to-purple-50">
          <div className="flex items-start space-x-4">
            {/* Provider Image */}
            <div className="flex-shrink-0">
              {item.provider_image ? (
                <img
                  src={item.provider_image}
                  alt={item.provider_name}
                  className="w-16 h-16 rounded-full object-cover border-2 border-white shadow-md"
                />
              ) : (
                <div className="w-16 h-16 rounded-full bg-gray-300 flex items-center justify-center">
                  <Wrench className="h-8 w-8 text-gray-600" />
                </div>
              )}
            </div>

            {/* Provider Info */}
            <div className="flex-1">
              <div className="flex items-center justify-between">
                <div>
                  <h4 className="font-semibold text-gray-900">{item.provider_name}</h4>
                  <div className="flex items-center space-x-2 mt-1">
                    <span className="text-sm text-blue-600 font-medium">{item.provider_level}</span>
                    <span className="text-sm text-gray-500">•</span>
                    <span className="text-sm text-gray-600">{item.platform}</span>
                  </div>
                </div>
                <button
                  onClick={() => toggleFavorite(item.title)}
                  className={`p-2 rounded-full transition-colors ${
                    isFavorite 
                      ? 'bg-red-500 text-white' 
                      : 'bg-white text-gray-400 hover:text-red-500'
                  }`}
                >
                  <Heart className={`h-4 w-4 ${isFavorite ? 'fill-current' : ''}`} />
                </button>
              </div>

              {/* Rating */}
              {item.provider_rating && (
                <div className="flex items-center space-x-2 mt-2">
                  <div className="flex">
                    {[...Array(5)].map((_, i) => (
                      <Star
                        key={i}
                        className={`h-4 w-4 ${
                          i < Math.floor(item.provider_rating!)
                            ? 'text-yellow-400 fill-current'
                            : 'text-gray-300'
                        }`}
                      />
                    ))}
                  </div>
                  <span className="font-medium">{item.provider_rating}</span>
                  {item.review_count && (
                    <span className="text-gray-500 text-sm">({item.review_count})</span>
                  )}
                </div>
              )}
            </div>
          </div>
        </div>

        {/* Service Content */}
        <div className="p-6">
          {/* Service Title */}
          <h3 className="font-semibold text-gray-900 mb-3 line-clamp-2">
            {item.title}
          </h3>

          {/* Skills */}
          {item.skills && item.skills.length > 0 && (
            <div className="mb-3">
              <div className="flex flex-wrap gap-1">
                {item.skills.slice(0, 4).map((skill, idx) => (
                  <span
                    key={idx}
                    className="text-xs bg-green-50 text-green-700 px-2 py-1 rounded"
                  >
                    {skill}
                  </span>
                ))}
              </div>
            </div>
          )}

          {/* Portfolio Images */}
          {item.portfolio_images && item.portfolio_images.length > 0 && (
            <div className="mb-4">
              <div className="flex space-x-2 overflow-x-auto">
                {item.portfolio_images.slice(0, 3).map((image, idx) => (
                  <img
                    key={idx}
                    src={image}
                    alt={`Portfolio ${idx + 1}`}
                    className="w-20 h-16 object-cover rounded border flex-shrink-0"
                  />
                ))}
              </div>
            </div>
          )}

          {/* Service Details */}
          <div className="space-y-2 text-sm text-gray-600 mb-4">
            <div className="flex items-center space-x-1">
              <MapPin className="h-4 w-4" />
              <span>{item.location}</span>
            </div>
            <div className="flex items-center space-x-1">
              <Clock className="h-4 w-4" />
              <span>{item.delivery_time || item.response_time}</span>
            </div>
            {item.languages && (
              <div className="flex items-center space-x-1">
                <Info className="h-4 w-4" />
                <span>Languages: {item.languages.join(', ')}</span>
              </div>
            )}
          </div>

          {/* Packages */}
          {item.packages && (
            <div className="mb-4">
              <h5 className="text-sm font-medium text-gray-900 mb-2">Packages:</h5>
              <div className="grid grid-cols-3 gap-2 text-xs">
                {item.packages.basic && (
                  <div className="bg-gray-50 p-2 rounded">
                    <div className="font-medium">Basic</div>
                    <div className="text-green-600">${item.packages.basic.price}</div>
                  </div>
                )}
                {item.packages.standard && (
                  <div className="bg-blue-50 p-2 rounded">
                    <div className="font-medium">Standard</div>
                    <div className="text-green-600">${item.packages.standard.price}</div>
                  </div>
                )}
                {item.packages.premium && (
                  <div className="bg-purple-50 p-2 rounded">
                    <div className="font-medium">Premium</div>
                    <div className="text-green-600">${item.packages.premium.price}</div>
                  </div>
                )}
              </div>
            </div>
          )}

          {/* Price and Actions */}
          <div className="flex items-center justify-between">
            <div>
              <div className="text-2xl font-bold text-green-600">
                {formatPrice(item)}
              </div>
              <span className={`text-xs px-2 py-1 rounded ${getRecommendationColor(item.recommendation_level)}`}>
                {item.recommendation_level}
              </span>
            </div>
            
            <div className="flex space-x-2">
              <button
                onClick={() => navigator.share?.({ title: item.title, url: item.affiliate_url })}
                className="p-2 text-gray-500 hover:text-blue-600 transition-colors"
              >
                <Share2 className="h-4 w-4" />
              </button>
              <button
                onClick={() => window.open(item.affiliate_url, '_blank')}
                className="bg-blue-600 text-white px-4 py-2 rounded-lg hover:bg-blue-700 transition-colors flex items-center space-x-1"
              >
                <span>Contact</span>
                <ExternalLink className="h-3 w-3" />
              </button>
            </div>
          </div>
        </div>
      </div>
    );
  };

  return (
    <div className="min-h-screen bg-gradient-to-br from-blue-50 via-white to-purple-50">
      {/* Header */}
      <header className="bg-white/80 backdrop-blur-md border-b border-gray-200 sticky top-0 z-50">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="flex items-center justify-between h-16">
            <div className="flex items-center space-x-3">
              <TrendingUp className="h-8 w-8 text-blue-600" />
              <h1 className="text-2xl font-bold bg-gradient-to-r from-blue-600 to-purple-600 bg-clip-text text-transparent">
                PricePulse
              </h1>
              <span className="text-xs bg-green-100 text-green-800 px-2 py-1 rounded">Enhanced</span>
            </div>
            
            {/* Controls */}
            <div className="flex items-center space-x-4">
              {/* Currency Selector */}
              <select
                value={currency}
                onChange={(e) => setCurrency(e.target.value)}
                className="text-sm border border-gray-300 rounded px-2 py-1"
              >
                <option value="USD">USD ($)</option>
                <option value="EUR">EUR (€)</option>
                <option value="GBP">GBP (£)</option>
              </select>

              {/* Backend Status */}
              <div className="flex items-center space-x-2">
                <div className={`w-3 h-3 rounded-full ${
                  backendStatus === 'online' ? 'bg-green-500' : 
                  backendStatus === 'offline' ? 'bg-red-500' : 'bg-yellow-500'
                }`}></div>
                <span className="text-sm text-gray-600">
                  {backendStatus === 'online' ? 'Enhanced API' : 
                   backendStatus === 'offline' ? 'API Offline' : 'Checking...'}
                </span>
              </div>
            </div>
          </div>
        </div>
      </header>

      {/* Main Content */}
      <main className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
        {/* Hero Section */}
        <div className="text-center py-16">
          <h2 className="text-4xl font-bold text-gray-900 mb-4">
            Find the Best Deals with Real Product Images & Brand Info
          </h2>
          <p className="text-xl text-gray-600 mb-8">
            Compare prices across 12+ platforms with enhanced visual search and brand intelligence
          </p>

          {/* Search Type Toggle */}
          <div className="flex justify-center mb-6">
            <div className="bg-gray-100 rounded-lg p-1">
              <button
                onClick={() => setSearchType('products')}
                className={`flex items-center px-6 py-3 rounded-md text-sm font-medium transition-colors ${
                  searchType === 'products' 
                    ? 'bg-white text-blue-600 shadow-sm' 
                    : 'text-gray-600 hover:text-gray-900'
                }`}
              >
                <Package className="h-4 w-4 mr-2" />
                Products
              </button>
              <button
                onClick={() => setSearchType('services')}
                className={`flex items-center px-6 py-3 rounded-md text-sm font-medium transition-colors ${
                  searchType === 'services' 
                    ? 'bg-white text-blue-600 shadow-sm' 
                    : 'text-gray-600 hover:text-gray-900'
                }`}
              >
                <Wrench className="h-4 w-4 mr-2" />
                Services
              </button>
            </div>
          </div>

          {/* Search Bar */}
          <div className="max-w-2xl mx-auto">
            <div className="relative">
              <input
                type="text"
                placeholder={`Search for ${searchType}... (e.g., "iPhone 15", "MacBook", "web development")`}
                value={searchQuery}
                onChange={(e) => setSearchQuery(e.target.value)}
                onKeyPress={(e) => e.key === 'Enter' && handleSearch()}
                className="w-full py-4 px-6 pr-16 text-lg border border-gray-300 rounded-xl focus:ring-2 focus:ring-blue-500 focus:border-transparent"
              />
              <button
                onClick={handleSearch}
                disabled={loading || backendStatus !== 'online'}
                className="absolute right-2 top-1/2 transform -translate-y-1/2 bg-blue-600 text-white px-6 py-2 rounded-lg hover:bg-blue-700 disabled:opacity-50 disabled:cursor-not-allowed flex items-center space-x-2"
              >
                {loading ? (
                  <div className="animate-spin h-5 w-5 border-2 border-white border-t-transparent rounded-full"></div>
                ) : (
                  <Search className="h-5 w-5" />
                )}
                <span>{loading ? 'Searching...' : 'Search'}</span>
              </button>
            </div>
          </div>

          {/* Backend Status Warning */}
          {backendStatus === 'offline' && (
            <div className="mt-4 p-4 bg-red-50 border border-red-200 rounded-lg max-w-2xl mx-auto">
              <p className="text-red-800">
                ⚠️ Enhanced API is offline. Make sure to run the enhanced backend script.
              </p>
            </div>
          )}
        </div>

        {/* Search Results */}
        {searchResults && (
          <div className="space-y-8">
            {/* Search Summary */}
            <div className="bg-gradient-to-r from-blue-50 to-purple-50 border border-blue-200 rounded-xl p-6">
              <div className="flex items-center justify-between">
                <div>
                  <h3 className="text-2xl font-bold text-gray-900 flex items-center">
                    <Zap className="h-6 w-6 text-blue-600 mr-2" />
                    Enhanced Search Results for "{searchResults.query}"
                  </h3>
                  <p className="text-lg text-gray-600">
                    Found {searchResults.total_products || searchResults.total_services} {searchType} 
                    across {searchResults.search_metadata?.platforms_searched} platforms
                    in {searchResults.search_duration_seconds}s
                  </p>
                  {searchResults.search_metadata?.has_images && (
                    <div className="flex items-center space-x-4 mt-2 text-sm text-green-700">
                      <span className="flex items-center">
                        <CheckCircle className="h-4 w-4 mr-1" />
                        Real Product Images
                      </span>
                      <span className="flex items-center">
                        <Award className="h-4 w-4 mr-1" />
                        Brand Information
                      </span>
                      <span className="flex items-center">
                        <Shield className="h-4 w-4 mr-1" />
                        Enhanced Features
                      </span>
                    </div>
                  )}
                </div>
              </div>
            </div>

            {/* Recommendations */}
            {searchResults.recommendations && searchResults.recommendations.length > 0 && (
              <div className="bg-green-50 border border-green-200 rounded-xl p-6">
                <h4 className="text-lg font-semibold text-green-900 mb-3 flex items-center">
                  <Award className="h-5 w-5 mr-2" />
                  🎯 Smart Recommendations
                </h4>
                <div className="space-y-2">
                  {searchResults.recommendations.map((rec, index) => (
                    <p key={index} className="text-green-800 flex items-start">
                      <span className="text-green-600 mr-2">•</span>
                      {rec}
                    </p>
                  ))}
                </div>
              </div>
            )}

            {/* Results Grid */}
            <div className="grid gap-6 md:grid-cols-2 lg:grid-cols-3">
              {searchType === 'products' 
                ? (searchResults.products || []).map((item, index) => (
                    <ProductCard key={index} item={item} index={index} />
                  ))
                : (searchResults.services || []).map((item, index) => (
                    <ServiceCard key={index} item={item} index={index} />
                  ))
              }
            </div>
          </div>
        )}
      </main>
    </div>
  );
}

export default App;
