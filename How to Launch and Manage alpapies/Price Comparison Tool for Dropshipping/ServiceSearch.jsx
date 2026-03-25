import React, { useState, useEffect } from 'react'
import { Search, MapPin, DollarSign, Clock, Star, Award, Shield, ExternalLink } from 'lucide-react'
import { Button } from '@/components/ui/button.jsx'
import { Input } from '@/components/ui/input.jsx'
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from '@/components/ui/card.jsx'
import { Badge } from '@/components/ui/badge.jsx'
import { Select, SelectContent, SelectItem, SelectTrigger, SelectValue } from '@/components/ui/select.jsx'
import { Tabs, TabsContent, TabsList, TabsTrigger } from '@/components/ui/tabs.jsx'
import { Progress } from '@/components/ui/progress.jsx'
import { Separator } from '@/components/ui/separator.jsx'

const API_BASE_URL = 'https://60h5imclkgvv.manus.space/api'

function ServiceSearch() {
  const [searchQuery, setSearchQuery] = useState('')
  const [searchResults, setSearchResults] = useState(null)
  const [loading, setLoading] = useState(false)
  const [selectedCategory, setSelectedCategory] = useState('')
  const [selectedCurrency, setSelectedCurrency] = useState('USD')
  const [userLocation, setUserLocation] = useState('')
  const [budgetMin, setBudgetMin] = useState('')
  const [budgetMax, setBudgetMax] = useState('')
  const [serviceCategories, setServiceCategories] = useState({})
  const [suggestions, setSuggestions] = useState([])

  useEffect(() => {
    fetchServiceCategories()
  }, [])

  const fetchServiceCategories = async () => {
    try {
      const response = await fetch(`${API_BASE_URL}/service-categories`)
      const data = await response.json()
      setServiceCategories(data.categories || {})
    } catch (error) {
      console.error('Error fetching categories:', error)
    }
  }

  const fetchSuggestions = async (query) => {
    if (query.length < 2) {
      setSuggestions([])
      return
    }
    
    try {
      const response = await fetch(`${API_BASE_URL}/service-suggestions?q=${encodeURIComponent(query)}`)
      const data = await response.json()
      setSuggestions(data.suggestions || [])
    } catch (error) {
      console.error('Error fetching suggestions:', error)
    }
  }

  const handleSearch = async () => {
    if (!searchQuery.trim()) return

    setLoading(true)
    try {
      const params = new URLSearchParams({
        q: searchQuery,
        max_results: '20',
        currency: selectedCurrency
      })
      
      if (selectedCategory) params.append('category', selectedCategory)
      if (userLocation) params.append('location', userLocation)
      if (budgetMin) params.append('budget_min', budgetMin)
      if (budgetMax) params.append('budget_max', budgetMax)

      const response = await fetch(`${API_BASE_URL}/service-search?${params}`)
      const data = await response.json()
      setSearchResults(data)
    } catch (error) {
      console.error('Error searching services:', error)
    } finally {
      setLoading(false)
    }
  }

  const handleKeyPress = (e) => {
    if (e.key === 'Enter') {
      handleSearch()
    }
  }

  const formatPrice = (service) => {
    const currency = service.currency || selectedCurrency
    if (service.starting_price) {
      return `${currency} ${service.starting_price}+`
    } else if (service.hourly_rate) {
      return `${currency} ${service.hourly_rate}/hr`
    } else if (service.bid_amount) {
      return `${currency} ${service.bid_amount}`
    } else if (service.quote_range) {
      return service.quote_range
    } else if (service.price_range) {
      return service.price_range
    }
    return 'Quote on request'
  }

  const getRecommendationColor = (level) => {
    switch (level) {
      case 'Highly Recommended': return 'bg-green-100 text-green-800'
      case 'Recommended': return 'bg-blue-100 text-blue-800'
      case 'Good Option': return 'bg-yellow-100 text-yellow-800'
      default: return 'bg-gray-100 text-gray-800'
    }
  }

  const getPlatformColor = (platform) => {
    const colors = {
      'Fiverr': 'bg-green-100 text-green-800',
      'Upwork': 'bg-blue-100 text-blue-800',
      'Freelancer': 'bg-purple-100 text-purple-800',
      'TaskRabbit': 'bg-orange-100 text-orange-800',
      'Thumbtack': 'bg-indigo-100 text-indigo-800',
      'Angie': 'bg-red-100 text-red-800'
    }
    return colors[platform] || 'bg-gray-100 text-gray-800'
  }

  return (
    <div className="min-h-screen bg-gradient-to-br from-blue-50 to-indigo-100 p-4">
      <div className="max-w-7xl mx-auto">
        {/* Header */}
        <div className="text-center mb-8">
          <h1 className="text-4xl font-bold text-gray-900 mb-4">
            🔍 PricePulse Service Finder
          </h1>
          <p className="text-xl text-gray-600 mb-6">
            Find the best service providers across multiple platforms
          </p>
        </div>

        {/* Search Section */}
        <Card className="mb-8">
          <CardHeader>
            <CardTitle className="flex items-center gap-2">
              <Search className="h-5 w-5" />
              Search Services
            </CardTitle>
          </CardHeader>
          <CardContent>
            <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-4 mb-4">
              <div className="relative">
                <Input
                  placeholder="What service do you need?"
                  value={searchQuery}
                  onChange={(e) => {
                    setSearchQuery(e.target.value)
                    fetchSuggestions(e.target.value)
                  }}
                  onKeyPress={handleKeyPress}
                  className="pr-10"
                />
                {suggestions.length > 0 && (
                  <div className="absolute top-full left-0 right-0 bg-white border border-gray-200 rounded-md shadow-lg z-10 max-h-48 overflow-y-auto">
                    {suggestions.map((suggestion, index) => (
                      <div
                        key={index}
                        className="px-4 py-2 hover:bg-gray-100 cursor-pointer"
                        onClick={() => {
                          setSearchQuery(suggestion)
                          setSuggestions([])
                        }}
                      >
                        {suggestion}
                      </div>
                    ))}
                  </div>
                )}
              </div>
              
              <Select value={selectedCategory} onValueChange={setSelectedCategory}>
                <SelectTrigger>
                  <SelectValue placeholder="Category" />
                </SelectTrigger>
                <SelectContent>
                  <SelectItem value="">All Categories</SelectItem>
                  {Object.keys(serviceCategories).map(category => (
                    <SelectItem key={category} value={category}>{category}</SelectItem>
                  ))}
                </SelectContent>
              </Select>

              <Input
                placeholder="Your location"
                value={userLocation}
                onChange={(e) => setUserLocation(e.target.value)}
              />

              <Select value={selectedCurrency} onValueChange={setSelectedCurrency}>
                <SelectTrigger>
                  <SelectValue />
                </SelectTrigger>
                <SelectContent>
                  <SelectItem value="USD">USD ($)</SelectItem>
                  <SelectItem value="EUR">EUR (€)</SelectItem>
                  <SelectItem value="GBP">GBP (£)</SelectItem>
                  <SelectItem value="CAD">CAD ($)</SelectItem>
                  <SelectItem value="AUD">AUD ($)</SelectItem>
                  <SelectItem value="ZAR">ZAR (R)</SelectItem>
                </SelectContent>
              </Select>
            </div>

            <div className="grid grid-cols-1 md:grid-cols-3 gap-4 mb-4">
              <Input
                placeholder="Min budget"
                type="number"
                value={budgetMin}
                onChange={(e) => setBudgetMin(e.target.value)}
              />
              <Input
                placeholder="Max budget"
                type="number"
                value={budgetMax}
                onChange={(e) => setBudgetMax(e.target.value)}
              />
              <Button onClick={handleSearch} disabled={loading} className="w-full">
                {loading ? 'Searching...' : 'Find Services'}
              </Button>
            </div>
          </CardContent>
        </Card>

        {/* Results Section */}
        {searchResults && (
          <div className="space-y-6">
            {/* Search Summary */}
            <Card>
              <CardHeader>
                <CardTitle>Search Results</CardTitle>
                <CardDescription>
                  Found {searchResults.total_services} services across {searchResults.platforms_searched} platforms in {searchResults.search_duration_seconds}s
                </CardDescription>
              </CardHeader>
            </Card>

            {/* Recommendations */}
            {searchResults.recommendations && searchResults.recommendations.length > 0 && (
              <Card>
                <CardHeader>
                  <CardTitle className="flex items-center gap-2">
                    <Award className="h-5 w-5" />
                    Smart Recommendations
                  </CardTitle>
                </CardHeader>
                <CardContent>
                  <div className="space-y-2">
                    {searchResults.recommendations.map((rec, index) => (
                      <div key={index} className="flex items-center gap-2 p-2 bg-blue-50 rounded">
                        <Star className="h-4 w-4 text-blue-600" />
                        <span className="text-sm">{rec}</span>
                      </div>
                    ))}
                  </div>
                </CardContent>
              </Card>
            )}

            {/* Services */}
            <Tabs defaultValue="all" className="w-full">
              <TabsList className="grid w-full grid-cols-3">
                <TabsTrigger value="all">All Services ({searchResults.total_services})</TabsTrigger>
                <TabsTrigger value="groups">Grouped ({searchResults.service_groups?.length || 0})</TabsTrigger>
                <TabsTrigger value="insights">Insights</TabsTrigger>
              </TabsList>

              <TabsContent value="all" className="space-y-4">
                {searchResults.services?.map((service, index) => (
                  <Card key={index} className="hover:shadow-lg transition-shadow">
                    <CardContent className="p-6">
                      <div className="flex justify-between items-start mb-4">
                        <div className="flex-1">
                          <div className="flex items-center gap-2 mb-2">
                            <h3 className="text-lg font-semibold">{service.title}</h3>
                            <Badge className={getPlatformColor(service.platform)}>
                              {service.platform}
                            </Badge>
                            {service.recommendation_level && (
                              <Badge className={getRecommendationColor(service.recommendation_level)}>
                                {service.recommendation_level}
                              </Badge>
                            )}
                          </div>
                          <p className="text-gray-600 mb-2">{service.description}</p>
                          <div className="flex items-center gap-4 text-sm text-gray-500">
                            <span className="flex items-center gap-1">
                              <Star className="h-4 w-4" />
                              {service.provider_rating}/5 ({service.provider_reviews} reviews)
                            </span>
                            {service.location && (
                              <span className="flex items-center gap-1">
                                <MapPin className="h-4 w-4" />
                                {service.location}
                              </span>
                            )}
                            {service.response_time && (
                              <span className="flex items-center gap-1">
                                <Clock className="h-4 w-4" />
                                {service.response_time}
                              </span>
                            )}
                          </div>
                        </div>
                        <div className="text-right">
                          <div className="text-2xl font-bold text-green-600 mb-2">
                            {formatPrice(service)}
                          </div>
                          {service.overall_score && (
                            <div className="text-sm text-gray-500">
                              Score: {Math.round(service.overall_score * 100)}%
                            </div>
                          )}
                        </div>
                      </div>

                      <div className="flex items-center justify-between">
                        <div className="flex items-center gap-4">
                          <span className="text-sm font-medium">{service.provider_name}</span>
                          {service.provider_level && (
                            <Badge variant="outline">{service.provider_level}</Badge>
                          )}
                          {(service.background_checked || service.licensed || service.insured) && (
                            <div className="flex items-center gap-1">
                              <Shield className="h-4 w-4 text-green-600" />
                              <span className="text-sm text-green-600">Verified</span>
                            </div>
                          )}
                        </div>
                        <Button 
                          onClick={() => window.open(service.affiliate_url || service.service_url, '_blank')}
                          className="flex items-center gap-2"
                        >
                          View Service
                          <ExternalLink className="h-4 w-4" />
                        </Button>
                      </div>

                      {service.packages && (
                        <div className="mt-4 pt-4 border-t">
                          <h4 className="font-medium mb-2">Service Packages:</h4>
                          <div className="grid grid-cols-1 md:grid-cols-3 gap-2">
                            {Object.entries(service.packages).map(([tier, pkg]) => (
                              <div key={tier} className="p-2 bg-gray-50 rounded text-sm">
                                <div className="font-medium capitalize">{tier}</div>
                                <div className="text-green-600">${pkg.price}</div>
                                <div className="text-gray-500">{pkg.delivery}</div>
                              </div>
                            ))}
                          </div>
                        </div>
                      )}
                    </CardContent>
                  </Card>
                ))}
              </TabsContent>

              <TabsContent value="groups" className="space-y-4">
                {searchResults.service_groups?.map((group, index) => (
                  <Card key={index}>
                    <CardHeader>
                      <CardTitle>Group {group.group_id}: {group.service_type}</CardTitle>
                      <CardDescription>
                        {group.similar_services.length + 1} similar services
                        {group.avg_price > 0 && ` • Average price: ${selectedCurrency} ${group.avg_price.toFixed(2)}`}
                      </CardDescription>
                    </CardHeader>
                    <CardContent>
                      <div className="space-y-2">
                        <div className="font-medium">Primary: {group.primary_service.title}</div>
                        {group.similar_services.map((service, idx) => (
                          <div key={idx} className="text-sm text-gray-600">
                            • {service.title} ({service.platform})
                          </div>
                        ))}
                      </div>
                    </CardContent>
                  </Card>
                ))}
              </TabsContent>

              <TabsContent value="insights" className="space-y-4">
                {searchResults.insights && (
                  <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
                    {searchResults.insights.price_analysis && (
                      <Card>
                        <CardHeader>
                          <CardTitle>Price Analysis</CardTitle>
                        </CardHeader>
                        <CardContent>
                          <div className="space-y-2">
                            <div>Min Price: {selectedCurrency} {searchResults.insights.price_analysis.min_price}</div>
                            <div>Max Price: {selectedCurrency} {searchResults.insights.price_analysis.max_price}</div>
                            <div>Average: {selectedCurrency} {searchResults.insights.price_analysis.avg_price?.toFixed(2)}</div>
                            <div>Budget Options: {searchResults.insights.price_analysis.budget_options}</div>
                          </div>
                        </CardContent>
                      </Card>
                    )}

                    {searchResults.insights.platform_analysis && (
                      <Card>
                        <CardHeader>
                          <CardTitle>Platform Distribution</CardTitle>
                        </CardHeader>
                        <CardContent>
                          <div className="space-y-2">
                            {Object.entries(searchResults.insights.platform_analysis.platform_distribution || {}).map(([platform, count]) => (
                              <div key={platform} className="flex justify-between">
                                <span>{platform}</span>
                                <span>{count} services</span>
                              </div>
                            ))}
                          </div>
                        </CardContent>
                      </Card>
                    )}
                  </div>
                )}
              </TabsContent>
            </Tabs>
          </div>
        )}
      </div>
    </div>
  )
}

export default ServiceSearch
