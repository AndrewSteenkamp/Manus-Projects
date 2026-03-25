import { useState, useEffect } from 'react'
import { Button } from '@/components/ui/button.jsx'
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from '@/components/ui/card.jsx'
import { Badge } from '@/components/ui/badge.jsx'
import { Tabs, TabsContent, TabsList, TabsTrigger } from '@/components/ui/tabs.jsx'
import { Input } from '@/components/ui/input.jsx'
import { Label } from '@/components/ui/label.jsx'
import { Progress } from '@/components/ui/progress.jsx'
import { Alert, AlertDescription, AlertTitle } from '@/components/ui/alert.jsx'
import { 
  TrendingUp, 
  TrendingDown, 
  Activity, 
  BarChart3, 
  Globe, 
  Calendar,
  Search,
  RefreshCw,
  AlertCircle,
  CheckCircle,
  DollarSign,
  PieChart,
  Target,
  Zap
} from 'lucide-react'
import './App.css'

const API_BASE = 'http://localhost:5000/api/socrates'

function App() {
  const [dailyReport, setDailyReport] = useState(null)
  const [marketAnalysis, setMarketAnalysis] = useState(null)
  const [loading, setLoading] = useState(false)
  const [searchSymbol, setSearchSymbol] = useState('AAPL')
  const [error, setError] = useState(null)

  // Fetch daily report on component mount
  useEffect(() => {
    fetchDailyReport()
  }, [])

  const fetchDailyReport = async () => {
    setLoading(true)
    setError(null)
    try {
      const response = await fetch(`${API_BASE}/daily-report`)
      const data = await response.json()
      if (data.success) {
        setDailyReport(data.data)
      } else {
        setError('Failed to fetch daily report')
      }
    } catch (err) {
      setError('Network error: ' + err.message)
    } finally {
      setLoading(false)
    }
  }

  const fetchMarketAnalysis = async (symbol) => {
    setLoading(true)
    setError(null)
    try {
      const response = await fetch(`${API_BASE}/analyze/market/${symbol}`)
      const data = await response.json()
      if (data.success) {
        setMarketAnalysis(data.data)
      } else {
        setError('Failed to fetch market analysis')
      }
    } catch (err) {
      setError('Network error: ' + err.message)
    } finally {
      setLoading(false)
    }
  }

  const handleSearch = () => {
    if (searchSymbol.trim()) {
      fetchMarketAnalysis(searchSymbol.trim().toUpperCase())
    }
  }

  const getConfidenceColor = (confidence) => {
    if (confidence >= 0.7) return 'text-green-600'
    if (confidence >= 0.5) return 'text-yellow-600'
    return 'text-red-600'
  }

  const getConfidenceBadge = (confidence) => {
    if (confidence >= 0.7) return 'bg-green-100 text-green-800'
    if (confidence >= 0.5) return 'bg-yellow-100 text-yellow-800'
    return 'bg-red-100 text-red-800'
  }

  const formatPercentage = (value) => `${(value * 100).toFixed(1)}%`

  return (
    <div className="min-h-screen bg-gradient-to-br from-slate-50 to-slate-100 dark:from-slate-900 dark:to-slate-800">
      {/* Header */}
      <header className="bg-white dark:bg-slate-900 shadow-sm border-b">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="flex justify-between items-center py-6">
            <div className="flex items-center space-x-3">
              <div className="w-10 h-10 bg-gradient-to-r from-blue-600 to-purple-600 rounded-lg flex items-center justify-center">
                <Activity className="w-6 h-6 text-white" />
              </div>
              <div>
                <h1 className="text-2xl font-bold text-gray-900 dark:text-white">Socrates AI</h1>
                <p className="text-sm text-gray-500 dark:text-gray-400">Advanced Market Analysis System</p>
              </div>
            </div>
            <div className="flex items-center space-x-4">
              <Button 
                onClick={fetchDailyReport} 
                disabled={loading}
                variant="outline"
                size="sm"
              >
                <RefreshCw className={`w-4 h-4 mr-2 ${loading ? 'animate-spin' : ''}`} />
                Refresh
              </Button>
              <Badge variant="secondary" className="px-3 py-1">
                <CheckCircle className="w-3 h-3 mr-1" />
                Live
              </Badge>
            </div>
          </div>
        </div>
      </header>

      <main className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
        {error && (
          <Alert className="mb-6 border-red-200 bg-red-50 dark:border-red-800 dark:bg-red-900/20">
            <AlertCircle className="h-4 w-4 text-red-600" />
            <AlertTitle className="text-red-800 dark:text-red-200">Error</AlertTitle>
            <AlertDescription className="text-red-700 dark:text-red-300">{error}</AlertDescription>
          </Alert>
        )}

        <Tabs defaultValue="dashboard" className="space-y-6">
          <TabsList className="grid w-full grid-cols-4">
            <TabsTrigger value="dashboard">Dashboard</TabsTrigger>
            <TabsTrigger value="analysis">Market Analysis</TabsTrigger>
            <TabsTrigger value="global">Global Markets</TabsTrigger>
            <TabsTrigger value="cycles">Cycle Analysis</TabsTrigger>
          </TabsList>

          {/* Dashboard Tab */}
          <TabsContent value="dashboard" className="space-y-6">
            {dailyReport && (
              <>
                {/* Key Metrics */}
                <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6">
                  <Card>
                    <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
                      <CardTitle className="text-sm font-medium">Global Confidence</CardTitle>
                      <Target className="h-4 w-4 text-muted-foreground" />
                    </CardHeader>
                    <CardContent>
                      <div className="text-2xl font-bold">
                        <span className={getConfidenceColor(dailyReport.global_confidence)}>
                          {formatPercentage(dailyReport.global_confidence)}
                        </span>
                      </div>
                      <Progress 
                        value={dailyReport.global_confidence * 100} 
                        className="mt-2"
                      />
                    </CardContent>
                  </Card>

                  <Card>
                    <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
                      <CardTitle className="text-sm font-medium">ECM Phase</CardTitle>
                      <Activity className="h-4 w-4 text-muted-foreground" />
                    </CardHeader>
                    <CardContent>
                      <div className="text-2xl font-bold capitalize">
                        {dailyReport.ecm_analysis.phase.replace('_', ' ')}
                      </div>
                      <p className="text-xs text-muted-foreground mt-1">
                        Day {dailyReport.ecm_analysis.days_into_cycle} of cycle
                      </p>
                    </CardContent>
                  </Card>

                  <Card>
                    <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
                      <CardTitle className="text-sm font-medium">Capital Flow</CardTitle>
                      <TrendingUp className="h-4 w-4 text-muted-foreground" />
                    </CardHeader>
                    <CardContent>
                      <div className="text-2xl font-bold capitalize">
                        {dailyReport.capital_flow_analysis.capital_flow_direction.replace('_', '-')}
                      </div>
                      <p className="text-xs text-muted-foreground mt-1">
                        {dailyReport.capital_flow_analysis.concentration_level} concentration
                      </p>
                    </CardContent>
                  </Card>

                  <Card>
                    <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
                      <CardTitle className="text-sm font-medium">Next Turning Point</CardTitle>
                      <Calendar className="h-4 w-4 text-muted-foreground" />
                    </CardHeader>
                    <CardContent>
                      <div className="text-2xl font-bold">
                        {new Date(dailyReport.ecm_analysis.next_turning_point).getFullYear()}
                      </div>
                      <p className="text-xs text-muted-foreground mt-1">
                        {dailyReport.ecm_analysis.next_turning_point}
                      </p>
                    </CardContent>
                  </Card>
                </div>

                {/* Market Highlights */}
                <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
                  <Card>
                    <CardHeader>
                      <CardTitle className="flex items-center">
                        <BarChart3 className="w-5 h-5 mr-2" />
                        Key Market Movers
                      </CardTitle>
                    </CardHeader>
                    <CardContent>
                      <div className="space-y-3">
                        {dailyReport.market_highlights.key_movers.map((mover, index) => (
                          <div key={index} className="flex items-center justify-between p-3 bg-gray-50 dark:bg-gray-800 rounded-lg">
                            <div className="flex items-center space-x-3">
                              <Badge variant="outline">{mover.symbol}</Badge>
                              <span className="font-medium">{mover.change}</span>
                            </div>
                            <Badge className={getConfidenceBadge(mover.confidence)}>
                              {formatPercentage(mover.confidence)}
                            </Badge>
                          </div>
                        ))}
                      </div>
                    </CardContent>
                  </Card>

                  <Card>
                    <CardHeader>
                      <CardTitle className="flex items-center">
                        <PieChart className="w-5 h-5 mr-2" />
                        Sector Performance
                      </CardTitle>
                    </CardHeader>
                    <CardContent>
                      <div className="space-y-4">
                        <div>
                          <h4 className="text-sm font-medium text-green-600 mb-2">Strongest Sectors</h4>
                          <div className="flex flex-wrap gap-2">
                            {dailyReport.market_highlights.strongest_sectors.map((sector, index) => (
                              <Badge key={index} className="bg-green-100 text-green-800">
                                <TrendingUp className="w-3 h-3 mr-1" />
                                {sector}
                              </Badge>
                            ))}
                          </div>
                        </div>
                        <div>
                          <h4 className="text-sm font-medium text-red-600 mb-2">Weakest Sectors</h4>
                          <div className="flex flex-wrap gap-2">
                            {dailyReport.market_highlights.weakest_sectors.map((sector, index) => (
                              <Badge key={index} className="bg-red-100 text-red-800">
                                <TrendingDown className="w-3 h-3 mr-1" />
                                {sector}
                              </Badge>
                            ))}
                          </div>
                        </div>
                      </div>
                    </CardContent>
                  </Card>
                </div>

                {/* Key Insights */}
                <Card>
                  <CardHeader>
                    <CardTitle className="flex items-center">
                      <Zap className="w-5 h-5 mr-2" />
                      Key Insights
                    </CardTitle>
                    <CardDescription>
                      AI-generated market insights for {dailyReport.date}
                    </CardDescription>
                  </CardHeader>
                  <CardContent>
                    <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
                      {dailyReport.key_insights.map((insight, index) => (
                        <div key={index} className="p-4 bg-blue-50 dark:bg-blue-900/20 rounded-lg border-l-4 border-blue-500">
                          <p className="text-sm text-gray-700 dark:text-gray-300">{insight}</p>
                        </div>
                      ))}
                    </div>
                  </CardContent>
                </Card>
              </>
            )}
          </TabsContent>

          {/* Market Analysis Tab */}
          <TabsContent value="analysis" className="space-y-6">
            <Card>
              <CardHeader>
                <CardTitle>Individual Market Analysis</CardTitle>
                <CardDescription>
                  Analyze specific stocks, forex pairs, or commodities
                </CardDescription>
              </CardHeader>
              <CardContent>
                <div className="flex space-x-2 mb-6">
                  <div className="flex-1">
                    <Label htmlFor="symbol">Symbol</Label>
                    <Input
                      id="symbol"
                      placeholder="Enter symbol (e.g., AAPL, EURUSD=X)"
                      value={searchSymbol}
                      onChange={(e) => setSearchSymbol(e.target.value)}
                      onKeyPress={(e) => e.key === 'Enter' && handleSearch()}
                    />
                  </div>
                  <div className="flex items-end">
                    <Button onClick={handleSearch} disabled={loading}>
                      <Search className="w-4 h-4 mr-2" />
                      Analyze
                    </Button>
                  </div>
                </div>

                {marketAnalysis && (
                  <div className="space-y-6">
                    <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
                      <Card>
                        <CardHeader className="pb-2">
                          <CardTitle className="text-sm">Overall Confidence</CardTitle>
                        </CardHeader>
                        <CardContent>
                          <div className="text-2xl font-bold">
                            <span className={getConfidenceColor(marketAnalysis.overall_confidence)}>
                              {formatPercentage(marketAnalysis.overall_confidence)}
                            </span>
                          </div>
                        </CardContent>
                      </Card>

                      <Card>
                        <CardHeader className="pb-2">
                          <CardTitle className="text-sm">Momentum</CardTitle>
                        </CardHeader>
                        <CardContent>
                          <div className="flex items-center space-x-2">
                            {marketAnalysis.momentum_analysis.direction === 'bullish' ? (
                              <TrendingUp className="w-5 h-5 text-green-600" />
                            ) : (
                              <TrendingDown className="w-5 h-5 text-red-600" />
                            )}
                            <span className="font-medium capitalize">
                              {marketAnalysis.momentum_analysis.direction}
                            </span>
                          </div>
                        </CardContent>
                      </Card>

                      <Card>
                        <CardHeader className="pb-2">
                          <CardTitle className="text-sm">Risk Level</CardTitle>
                        </CardHeader>
                        <CardContent>
                          <Badge className={
                            marketAnalysis.risk_assessment.risk_level === 'low' ? 'bg-green-100 text-green-800' :
                            marketAnalysis.risk_assessment.risk_level === 'moderate' ? 'bg-yellow-100 text-yellow-800' :
                            'bg-red-100 text-red-800'
                          }>
                            {marketAnalysis.risk_assessment.risk_level}
                          </Badge>
                        </CardContent>
                      </Card>
                    </div>

                    <Card>
                      <CardHeader>
                        <CardTitle>Pressure Points</CardTitle>
                      </CardHeader>
                      <CardContent>
                        <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
                          <div>
                            <h4 className="font-medium text-green-600 mb-2">Support Levels</h4>
                            <div className="space-y-1">
                              {marketAnalysis.pressure_points.support_levels.map((level, index) => (
                                <div key={index} className="text-sm bg-green-50 dark:bg-green-900/20 p-2 rounded">
                                  ${level.toFixed(2)}
                                </div>
                              ))}
                            </div>
                          </div>
                          <div>
                            <h4 className="font-medium text-red-600 mb-2">Resistance Levels</h4>
                            <div className="space-y-1">
                              {marketAnalysis.pressure_points.resistance_levels.map((level, index) => (
                                <div key={index} className="text-sm bg-red-50 dark:bg-red-900/20 p-2 rounded">
                                  ${level.toFixed(2)}
                                </div>
                              ))}
                            </div>
                          </div>
                        </div>
                      </CardContent>
                    </Card>
                  </div>
                )}
              </CardContent>
            </Card>
          </TabsContent>

          {/* Global Markets Tab */}
          <TabsContent value="global" className="space-y-6">
            <Card>
              <CardHeader>
                <CardTitle className="flex items-center">
                  <Globe className="w-5 h-5 mr-2" />
                  Global Market Overview
                </CardTitle>
                <CardDescription>
                  Cross-market analysis and capital flow patterns
                </CardDescription>
              </CardHeader>
              <CardContent>
                <div className="text-center py-12 text-gray-500">
                  <Globe className="w-12 h-12 mx-auto mb-4 opacity-50" />
                  <p>Global market analysis will be displayed here</p>
                  <p className="text-sm">Feature coming soon</p>
                </div>
              </CardContent>
            </Card>
          </TabsContent>

          {/* Cycle Analysis Tab */}
          <TabsContent value="cycles" className="space-y-6">
            <Card>
              <CardHeader>
                <CardTitle className="flex items-center">
                  <Activity className="w-5 h-5 mr-2" />
                  Economic Confidence Model (ECM)
                </CardTitle>
                <CardDescription>
                  Advanced cycle analysis based on Martin Armstrong's research
                </CardDescription>
              </CardHeader>
              <CardContent>
                <div className="text-center py-12 text-gray-500">
                  <Activity className="w-12 h-12 mx-auto mb-4 opacity-50" />
                  <p>Detailed cycle analysis will be displayed here</p>
                  <p className="text-sm">Feature coming soon</p>
                </div>
              </CardContent>
            </Card>
          </TabsContent>
        </Tabs>
      </main>
    </div>
  )
}

export default App

