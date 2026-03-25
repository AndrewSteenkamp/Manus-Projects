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
        