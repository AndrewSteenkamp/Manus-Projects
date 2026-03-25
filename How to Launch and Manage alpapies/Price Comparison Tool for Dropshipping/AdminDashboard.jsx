import { useState, useEffect } from 'react'
import { BarChart, Bar, XAxis, YAxis, CartesianGrid, Tooltip, ResponsiveContainer, PieChart, Pie, Cell } from 'recharts'
import { Card, CardContent, CardHeader, CardTitle } from '@/components/ui/card.jsx'
import { Tabs, TabsContent, TabsList, TabsTrigger } from '@/components/ui/tabs.jsx'
import { Badge } from '@/components/ui/badge.jsx'
import { Button } from '@/components/ui/button.jsx'
import { TrendingUp, DollarSign, MousePointer, Users, RefreshCw } from 'lucide-react'

const API_BASE_URL = 'http://localhost:5000/api'

const AdminDashboard = () => {
  const [analytics, setAnalytics] = useState(null)
  const [summary, setSummary] = useState(null)
  const [earnings, setEarnings] = useState(null)
  const [loading, setLoading] = useState(true)
  const [selectedPeriod, setSelectedPeriod] = useState(30)

  useEffect(() => {
    fetchAnalytics()
  }, [selectedPeriod])

  const fetchAnalytics = async () => {
    setLoading(true)
    try {
      // Fetch analytics data
      const [analyticsRes, summaryRes, earningsRes] = await Promise.all([
        fetch(`${API_BASE_URL}/affiliate/analytics?days=${selectedPeriod}`),
        fetch(`${API_BASE_URL}/affiliate/analytics/summary`),
        fetch(`${API_BASE_URL}/affiliate/earnings/estimate?days=${selectedPeriod}`)
      ])

      const analyticsData = await analyticsRes.json()
      const summaryData = await summaryRes.json()
      const earningsData = await earningsRes.json()

      setAnalytics(analyticsData)
      setSummary(summaryData)
      setEarnings(earningsData)
    } catch (error) {
      console.error('Error fetching analytics:', error)
    } finally {
      setLoading(false)
    }
  }

  const COLORS = ['#0088FE', '#00C49F', '#FFBB28', '#FF8042', '#8884D8']

  if (loading) {
    return (
      <div className="flex items-center justify-center h-64">
        <RefreshCw className="w-8 h-8 animate-spin" />
        <span className="ml-2">Loading analytics...</span>
      </div>
    )
  }

  return (
    <div className="p-6 space-y-6">
      <div className="flex items-center justify-between">
        <h1 className="text-3xl font-bold">Affiliate Dashboard</h1>
        <div className="flex items-center gap-2">
          <select 
            value={selectedPeriod} 
            onChange={(e) => setSelectedPeriod(Number(e.target.value))}
            className="px-3 py-2 border rounded-md"
          >
            <option value={7}>Last 7 days</option>
            <option value={30}>Last 30 days</option>
            <option value={90}>Last 90 days</option>
          </select>
          <Button onClick={fetchAnalytics} size="sm">
            <RefreshCw className="w-4 h-4 mr-2" />
            Refresh
          </Button>
        </div>
      </div>

      {/* Summary Cards */}
      <div className="grid gap-4 md:grid-cols-2 lg:grid-cols-4">
        <Card>
          <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
            <CardTitle className="text-sm font-medium">Total Clicks</CardTitle>
            <MousePointer className="h-4 w-4 text-muted-foreground" />
          </CardHeader>
          <CardContent>
            <div className="text-2xl font-bold">{analytics?.total_clicks || 0}</div>
            <p className="text-xs text-muted-foreground">
              Last {selectedPeriod} days
            </p>
          </CardContent>
        </Card>

        <Card>
          <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
            <CardTitle className="text-sm font-medium">Estimated Earnings</CardTitle>
            <DollarSign className="h-4 w-4 text-muted-foreground" />
          </CardHeader>
          <CardContent>
            <div className="text-2xl font-bold">${earnings?.total_estimated_earnings || 0}</div>
            <p className="text-xs text-muted-foreground">
              Based on industry averages
            </p>
          </CardContent>
        </Card>

        <Card>
          <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
            <CardTitle className="text-sm font-medium">Conversion Rate</CardTitle>
            <TrendingUp className="h-4 w-4 text-muted-foreground" />
          </CardHeader>
          <CardContent>
            <div className="text-2xl font-bold">{summary?.conversion_rate || 0}%</div>
            <p className="text-xs text-muted-foreground">
              Estimated conversion
            </p>
          </CardContent>
        </Card>

        <Card>
          <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
            <CardTitle className="text-sm font-medium">Active Vendors</CardTitle>
            <Users className="h-4 w-4 text-muted-foreground" />
          </CardHeader>
          <CardContent>
            <div className="text-2xl font-bold">{analytics?.clicks_by_vendor?.length || 0}</div>
            <p className="text-xs text-muted-foreground">
              Generating clicks
            </p>
          </CardContent>
        </Card>
      </div>

      <Tabs defaultValue="overview" className="space-y-4">
        <TabsList>
          <TabsTrigger value="overview">Overview</TabsTrigger>
          <TabsTrigger value="vendors">Vendors</TabsTrigger>
          <TabsTrigger value="earnings">Earnings</TabsTrigger>
        </TabsList>

        <TabsContent value="overview" className="space-y-4">
          <div className="grid gap-4 md:grid-cols-2">
            {/* Daily Clicks Chart */}
            <Card>
              <CardHeader>
                <CardTitle>Daily Clicks</CardTitle>
              </CardHeader>
              <CardContent>
                <ResponsiveContainer width="100%" height={300}>
                  <BarChart data={analytics?.daily_clicks || []}>
                    <CartesianGrid strokeDasharray="3 3" />
                    <XAxis dataKey="date" />
                    <YAxis />
                    <Tooltip />
                    <Bar dataKey="clicks" fill="#8884d8" />
                  </BarChart>
                </ResponsiveContainer>
              </CardContent>
            </Card>

            {/* Vendor Distribution */}
            <Card>
              <CardHeader>
                <CardTitle>Clicks by Vendor</CardTitle>
              </CardHeader>
              <CardContent>
                <ResponsiveContainer width="100%" height={300}>
                  <PieChart>
                    <Pie
                      data={analytics?.clicks_by_vendor || []}
                      cx="50%"
                      cy="50%"
                      labelLine={false}
                      label={({ vendor, percent }) => `${vendor} ${(percent * 100).toFixed(0)}%`}
                      outerRadius={80}
                      fill="#8884d8"
                      dataKey="clicks"
                    >
                      {(analytics?.clicks_by_vendor || []).map((entry, index) => (
                        <Cell key={`cell-${index}`} fill={COLORS[index % COLORS.length]} />
                      ))}
                    </Pie>
                    <Tooltip />
                  </PieChart>
                </ResponsiveContainer>
              </CardContent>
            </Card>
          </div>
        </TabsContent>

        <TabsContent value="vendors" className="space-y-4">
          <Card>
            <CardHeader>
              <CardTitle>Vendor Performance</CardTitle>
            </CardHeader>
            <CardContent>
              <div className="space-y-4">
                {analytics?.clicks_by_vendor?.map((vendor, index) => (
                  <div key={vendor.vendor} className="flex items-center justify-between p-4 border rounded-lg">
                    <div className="flex items-center gap-3">
                      <div 
                        className="w-4 h-4 rounded-full" 
                        style={{ backgroundColor: COLORS[index % COLORS.length] }}
                      />
                      <div>
                        <h3 className="font-medium">{vendor.vendor}</h3>
                        <p className="text-sm text-muted-foreground">{vendor.clicks} clicks</p>
                      </div>
                    </div>
                    <Badge variant="outline">
                      {earnings?.vendor_breakdown?.find(v => v.vendor_name === vendor.vendor)?.commission_rate || 0}% commission
                    </Badge>
                  </div>
                ))}
              </div>
            </CardContent>
          </Card>
        </TabsContent>

        <TabsContent value="earnings" className="space-y-4">
          <Card>
            <CardHeader>
              <CardTitle>Earnings Breakdown</CardTitle>
              <p className="text-sm text-muted-foreground">
                Estimates based on {earnings?.assumptions?.conversion_rate} conversion rate and {earnings?.assumptions?.avg_order_value} average order value
              </p>
            </CardHeader>
            <CardContent>
              <div className="space-y-4">
                {earnings?.vendor_breakdown?.map((vendor, index) => (
                  <div key={vendor.vendor_name} className="flex items-center justify-between p-4 border rounded-lg">
                    <div className="flex items-center gap-3">
                      <div 
                        className="w-4 h-4 rounded-full" 
                        style={{ backgroundColor: COLORS[index % COLORS.length] }}
                      />
                      <div>
                        <h3 className="font-medium">{vendor.vendor_name}</h3>
                        <p className="text-sm text-muted-foreground">
                          {vendor.clicks} clicks • {vendor.commission_rate}% commission
                        </p>
                      </div>
                    </div>
                    <div className="text-right">
                      <div className="font-medium">${vendor.estimated_earnings}</div>
                      <div className="text-sm text-muted-foreground">estimated</div>
                    </div>
                  </div>
                ))}
              </div>
              
              <div className="mt-6 p-4 bg-muted rounded-lg">
                <div className="flex items-center justify-between">
                  <span className="font-medium">Total Estimated Earnings</span>
                  <span className="text-2xl font-bold">${earnings?.total_estimated_earnings || 0}</span>
                </div>
                <p className="text-sm text-muted-foreground mt-2">
                  {earnings?.assumptions?.note}
                </p>
              </div>
            </CardContent>
          </Card>
        </TabsContent>
      </Tabs>
    </div>
  )
}

export default AdminDashboard

